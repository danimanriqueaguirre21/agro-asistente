"""Segunda versión experimental HU-07.

No modifica el modelo v1 ni el dataset original.
No usa las consultas de inferencia para elegir parámetros ni el umbral.
"""

from __future__ import annotations

import json
import platform
import sys
from collections import Counter
from pathlib import Path

import joblib
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score
from sklearn.pipeline import Pipeline

SEED = 42
COBERTURA_MINIMA = 0.85

CATEGORIAS = [
    "riego",
    "fertilizacion_nutricion",
    "plagas",
    "enfermedades_cultivos",
    "siembra_manejo_cultivo",
    "clima_heladas",
    "suelos",
    "cosecha_poscosecha",
]

EXCLUIR = {
    "trabajo-hu07-ead432668d",
    "trabajo-hu07-77fa929ec0",
    "trabajo-hu07-b7bf806a37",
    "trabajo-hu07-7791383f85",
    "trabajo-hu07-4da2de2e03",
}

# Palabras funcionales. No incluye términos de la decisión agrícola
# (agua, abono, hoja, suelo, grano, tallo, semilla).
FUNCIONALES = [
    "a", "al", "algo", "como", "con", "cuando", "de", "del", "donde",
    "el", "ella", "ellas", "ellos", "en", "es", "esa", "esas", "ese",
    "eso", "esos", "esta", "este", "esto", "estos", "ha", "hay", "la",
    "las", "le", "les", "lo", "los", "mas", "más", "me", "mi", "muy",
    "o", "para", "por", "que", "se", "si", "sin", "su", "sus", "te",
    "un", "una", "y", "ya",
]

AQUI = Path(__file__).resolve().parent
V1 = AQUI.parent / "hu07_tfidf_preliminar"
DATOS = AQUI.parents[1] / "preparacion" / "dataset_trabajo_hu07" / "consultas_trabajo.jsonl"
AMBIGUA = DATOS.with_name("cola_ambigua.jsonl")
FUERA = DATOS.with_name("fuera_de_alcance.jsonl")


def leer_jsonl(path: Path) -> list[dict]:
    filas = []
    with path.open(encoding="utf-8") as handle:
        for linea in handle:
            if linea.strip():
                filas.append(json.loads(linea))
    return filas


def pipeline_de(min_df: int, c_valor: float, funcionales: bool, sin_acentos: bool) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    analyzer="word",
                    ngram_range=(1, 2),
                    min_df=min_df,
                    sublinear_tf=True,
                    strip_accents="unicode" if sin_acentos else None,
                    stop_words=FUNCIONALES if funcionales else None,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    C=c_valor,
                    solver="lbfgs",
                    max_iter=2000,
                    random_state=SEED,
                ),
            ),
        ]
    )


def metricas_de(y_true: list[str], y_pred: list[str]) -> dict:
    reporte = classification_report(
        y_true,
        y_pred,
        labels=CATEGORIAS,
        output_dict=True,
        zero_division=0,
    )
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0, labels=CATEGORIAS),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0, labels=CATEGORIAS),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0, labels=CATEGORIAS),
        "f1_weighted": f1_score(y_true, y_pred, average="weighted", zero_division=0, labels=CATEGORIAS),
        "por_categoria": {
            categoria: {
                "precision": reporte[categoria]["precision"],
                "recall": reporte[categoria]["recall"],
                "f1": reporte[categoria]["f1-score"],
                "support": reporte[categoria]["support"],
            }
            for categoria in CATEGORIAS
        },
        "matriz": confusion_matrix(y_true, y_pred, labels=CATEGORIAS).tolist(),
    }


def margen_y_pred(proba: np.ndarray, clases: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    orden = np.argsort(proba, axis=1)
    primera = orden[:, -1]
    segunda = orden[:, -2]
    p1 = proba[np.arange(len(proba)), primera]
    p2 = proba[np.arange(len(proba)), segunda]
    return p1 - p2, clases[primera], clases[segunda], p1


def elegir_umbral(y_true: np.ndarray, proba: np.ndarray, clases: np.ndarray) -> dict:
    margen, pred, _, p1 = margen_y_pred(proba, clases)
    candidatos = []
    for paso in range(0, 31):
        corte = round(paso / 100, 2)
        quedar = margen >= corte
        cobertura = float(quedar.mean())
        fila = {"margen_minimo": corte, "cobertura": cobertura, "f1_macro_clasificadas": None, "accuracy_clasificadas": None}
        if cobertura >= COBERTURA_MINIMA and int(quedar.sum()) > 0:
            fila["f1_macro_clasificadas"] = float(
                f1_score(
                    y_true[quedar],
                    pred[quedar],
                    average="macro",
                    labels=CATEGORIAS,
                    zero_division=0,
                )
            )
            fila["accuracy_clasificadas"] = float(accuracy_score(y_true[quedar], pred[quedar]))
        candidatos.append(fila)
    validos = [fila for fila in candidatos if fila["f1_macro_clasificadas"] is not None]
    elegido = max(
        validos,
        key=lambda fila: (fila["f1_macro_clasificadas"], fila["cobertura"], -fila["margen_minimo"]),
    )
    return {"elegido": elegido, "barrido": candidatos, "regla": (
        "Se elige el margen mínimo que maximiza el macro-F1 de las consultas no abstenidas "
        f"en la validación cruzada interna, con cobertura de al menos {COBERTURA_MINIMA:.0%}. "
        "El conjunto de prueba no entra en esta elección."
    )}


def aplicar(modelo, textos: list[str], corte: float) -> list[dict]:
    proba = modelo.predict_proba(textos)
    clases = np.array(modelo.named_steps["clf"].classes_)
    margen, pred, segunda, p1 = margen_y_pred(proba, clases)
    filas = []
    for i, texto in enumerate(textos):
        abstenida = bool(margen[i] < corte)
        filas.append(
            {
                "text": texto,
                "predicha": None if abstenida else str(pred[i]),
                "categoria_puntera": str(pred[i]),
                "segunda": str(segunda[i]),
                "puntuacion": round(float(p1[i]), 4),
                "margen": round(float(margen[i]), 4),
                "salida": "sin categoría" if abstenida else str(pred[i]),
                "motivo": "margen_insuficiente" if abstenida else "margen_suficiente",
            }
        )
    return filas


def resumen_abstencion(y_true: list[str], filas: list[dict]) -> dict:
    clasificadas = [i for i, fila in enumerate(filas) if fila["salida"] != "sin categoría"]
    if not clasificadas:
        return {"clasificadas": 0, "cobertura": 0.0, "abstencion": 1.0}
    y_ok = [y_true[i] for i in clasificadas]
    y_hat = [filas[i]["salida"] for i in clasificadas]
    return {
        "n": len(filas),
        "clasificadas": len(clasificadas),
        "abstenciones": len(filas) - len(clasificadas),
        "cobertura": len(clasificadas) / len(filas),
        "abstencion": (len(filas) - len(clasificadas)) / len(filas),
        "accuracy_clasificadas": accuracy_score(y_ok, y_hat),
        "f1_macro_clasificadas": f1_score(y_ok, y_hat, average="macro", labels=CATEGORIAS, zero_division=0),
        "errores_entre_clasificadas": int(sum(a != b for a, b in zip(y_ok, y_hat))),
    }


def main() -> None:
    particiones = json.loads((V1 / "ids_particiones.json").read_text(encoding="utf-8"))
    metricas_v1_guardadas = json.loads((V1 / "metricas.json").read_text(encoding="utf-8"))
    originales = leer_jsonl(DATOS)
    por_id = {fila["id"]: fila for fila in originales}
    train_ids = particiones["entrenamiento"]
    test_ids = particiones["prueba"]
    if set(train_ids) & set(test_ids):
        raise SystemExit("Hay identificadores repetidos entre entrenamiento y prueba.")
    for identificador in train_ids + test_ids:
        if identificador not in por_id:
            raise SystemExit(f"Falta el identificador {identificador}.")
        if identificador in EXCLUIR:
            raise SystemExit(f"{identificador} estaba excluido y aparece en una partición.")

    x_train = [por_id[i]["text"] for i in train_ids]
    y_train = [por_id[i]["proposed_category"] for i in train_ids]
    x_test = [por_id[i]["text"] for i in test_ids]
    y_test = [por_id[i]["proposed_category"] for i in test_ids]

    consultas_inferencia = json.loads((V1 / "consultas_inferencia.json").read_text(encoding="utf-8"))["casos"]
    textos_inferencia = {caso["text"].casefold().strip() for caso in consultas_inferencia}
    if any(texto.casefold().strip() in textos_inferencia for texto in x_train):
        raise SystemExit("Una consulta de inferencia está en el entrenamiento.")

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    rejilla = []
    for min_df in (1, 2):
        for c_valor in (1.0, 4.0):
            for funcionales in (False, True):
                for sin_acentos in (False, True):
                    modelo = pipeline_de(min_df, c_valor, funcionales, sin_acentos)
                    puntajes = cross_val_score(
                        modelo,
                        x_train,
                        y_train,
                        cv=cv,
                        scoring="f1_macro",
                        n_jobs=1,
                    )
                    rejilla.append(
                        {
                            "min_df": min_df,
                            "C": c_valor,
                            "sin_palabras_funcionales": funcionales,
                            "sin_acentos": sin_acentos,
                            "f1_macro_cv_media": float(puntajes.mean()),
                            "f1_macro_cv_std": float(puntajes.std()),
                        }
                    )
                    print(
                        f"min_df={min_df} C={c_valor} funcionales={funcionales} "
                        f"acentos={sin_acentos} f1={puntajes.mean():.4f}",
                        flush=True,
                    )

    mejor = max(rejilla, key=lambda fila: (fila["f1_macro_cv_media"], -fila["min_df"], -fila["C"]))
    modelo_cv = pipeline_de(
        mejor["min_df"],
        mejor["C"],
        mejor["sin_palabras_funcionales"],
        mejor["sin_acentos"],
    )
    oof = cross_val_predict(
        modelo_cv,
        x_train,
        y_train,
        cv=cv,
        method="predict_proba",
        n_jobs=1,
    )
    clases_oof = np.array(CATEGORIAS)
    # cross_val_predict ordena las columnas como el estimador, que sigue el orden de aparición.
    # Se reordena con un ajuste auxiliar sobre una copia pequeña no: se lee classes_ de un pliegue.
    # Para alinear, se entrena el pipeline una vez y se usa su classes_ si coincide el shape.
    referencia = pipeline_de(
        mejor["min_df"],
        mejor["C"],
        mejor["sin_palabras_funcionales"],
        mejor["sin_acentos"],
    )
    referencia.fit(x_train, y_train)
    clases_oof = np.array(referencia.named_steps["clf"].classes_)
    if oof.shape[1] != len(clases_oof):
        raise SystemExit("La validación cruzada no devolvió una columna por categoría.")
    umbral = elegir_umbral(np.array(y_train), oof, clases_oof)
    corte = umbral["elegido"]["margen_minimo"]

    modelo_v1 = joblib.load(V1 / "modelo_tfidf_logreg.joblib")
    pred_v1 = modelo_v1.predict(x_test).tolist()
    metricas_v1 = metricas_de(y_test, pred_v1)
    if abs(metricas_v1["accuracy"] - metricas_v1_guardadas["accuracy"]) > 1e-9:
        raise SystemExit("La accuracy recomputada de v1 no coincide con metricas.json.")

    pred_v2 = referencia.predict(x_test).tolist()
    metricas_v2 = metricas_de(y_test, pred_v2)
    abstencion_prueba = resumen_abstencion(y_test, aplicar(referencia, x_test, corte))

    def sonda(filas_fuente: list[dict], campo_texto: str = "text") -> dict:
        textos = [fila[campo_texto] for fila in filas_fuente]
        salidas = aplicar(referencia, textos, corte)
        return {
            "n": len(salidas),
            "abstenciones": sum(1 for fila in salidas if fila["salida"] == "sin categoría"),
            "con_categoria_forzada": sum(1 for fila in salidas if fila["salida"] != "sin categoría"),
            "filas": [
                {
                    "id": filas_fuente[i].get("id"),
                    "salida": salidas[i]["salida"],
                    "categoria_puntera": salidas[i]["categoria_puntera"],
                    "segunda": salidas[i]["segunda"],
                    "puntuacion": salidas[i]["puntuacion"],
                    "margen": salidas[i]["margen"],
                }
                for i in range(len(salidas))
            ],
        }

    sonda_fuera = sonda(leer_jsonl(FUERA))
    sonda_ambigua = sonda(leer_jsonl(AMBIGUA))
    lectura_inferencia = []
    for caso in consultas_inferencia:
        salida = aplicar(referencia, [caso["text"]], corte)[0]
        salida_v1 = modelo_v1.predict([caso["text"]])[0]
        proba_v1 = modelo_v1.predict_proba([caso["text"]])[0]
        clases_v1 = list(modelo_v1.named_steps["clf"].classes_)
        lectura_inferencia.append(
            {
                "id": caso["id"],
                "tipo": caso["tipo"],
                "esperada": caso.get("esperada"),
                "v1": salida_v1,
                "v1_puntuacion": round(float(np.max(proba_v1)), 4),
                "v2_sin_abstencion": salida["categoria_puntera"],
                "v2_salida": salida["salida"],
                "v2_puntuacion": salida["puntuacion"],
                "v2_margen": salida["margen"],
                "usada_para_ajustar": False,
            }
        )

    joblib.dump(referencia, AQUI / "modelo_tfidf_logreg_v2.joblib")
    (AQUI / "metricas.json").write_text(
        json.dumps(
            {
                "caracter": "preliminar_v2",
                "definitivo": False,
                "dataset_aprobado": False,
                "conjunto": "prueba_bloqueada_de_v1",
                "v1": {k: metricas_v1[k] for k in ("accuracy", "precision_macro", "recall_macro", "f1_macro", "f1_weighted", "por_categoria")},
                "v2": {k: metricas_v2[k] for k in ("accuracy", "precision_macro", "recall_macro", "f1_macro", "f1_weighted", "por_categoria")},
                "abstencion_en_prueba": abstencion_prueba,
                "nota": "La abstención se eligió con validación cruzada interna del entrenamiento. Estas cifras de prueba no sirvieron para elegir el umbral.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (AQUI / "matriz_confusion.json").write_text(
        json.dumps(
            {"labels": CATEGORIAS, "v1": metricas_v1["matriz"], "v2": metricas_v2["matriz"]},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (AQUI / "rejilla_validacion.json").write_text(
        json.dumps({"mejor": mejor, "rejilla": rejilla}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (AQUI / "umbral_abstencion.json").write_text(
        json.dumps(umbral, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (AQUI / "sonda_no_usada_para_ajustar.json").write_text(
        json.dumps(
            {
                "nota": "Estas sondas no eligieron parámetros ni el umbral. No son una evaluación formal.",
                "fuera_de_alcance": sonda_fuera,
                "cola_ambigua": sonda_ambigua,
                "inferencia_ilustrativa": lectura_inferencia,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    versiones = {
        "python": sys.version.split()[0],
        "plataforma": platform.platform(),
        "scikit-learn": sklearn.__version__,
        "numpy": np.__version__,
        "joblib": joblib.__version__,
    }
    (AQUI / "versiones.json").write_text(json.dumps(versiones, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (AQUI / "ids_particiones.json").write_text(
        json.dumps(
            {
                "misma_prueba_que_v1": True,
                "validacion": "StratifiedKFold de 5 pliegues dentro del entrenamiento de v1",
                "seed": SEED,
                "entrenamiento": train_ids,
                "prueba": test_ids,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    manifiesto = {
        "experimento": "hu07-tfidf-logreg-v2",
        "modelo_v1_modificado": False,
        "dataset_modificado": False,
        "dataset_aprobado": False,
        "origen": "sintetico_preparacion",
        "consultas_reales": 0,
        "integrado_en_produccion": False,
        "configuracion": mejor,
        "margen_minimo": corte,
        "abstencion": "sin categoría cuando el margen entre las dos clases punteras es menor que el corte. No significa fuera de alcance.",
        "entrenamiento": len(train_ids),
        "prueba": len(test_ids),
        "modelo": "modelo_tfidf_logreg_v2.joblib",
    }
    (AQUI / "manifiesto_experimento.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    def tabla(metricas: dict) -> list[str]:
        lineas = [
            "| Categoría | Precision | Recall | F1 | Soporte |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
        for categoria in CATEGORIAS:
            item = metricas["por_categoria"][categoria]
            lineas.append(
                f"| {categoria} | {item['precision']:.4f} | {item['recall']:.4f} | {item['f1']:.4f} | {int(item['support'])} |"
            )
        return lineas

    lineas = [
        "# Segunda versión experimental — HU-07",
        "",
        "El dataset sigue sin aprobación humana. Las consultas son sintéticas. Esta comparación no describe agricultores reales y la versión no entra en producción.",
        "",
        "## Errores de la prueba ilustrativa",
        "",
        "Esos tres textos no se usaron para entrenar ni para elegir esta configuración.",
        "",
        "- Sulfato de potasio en el cafeto. `potasio`, `sulfato`, `cafeto` y `llenando` no aparecen en el entrenamiento, así que no están en el vocabulario. El modelo vio `grano`, y esa palabra cae sobre todo en cosecha (20 de 44 usos en entrenamiento). `abono` empujaba a fertilización, pero no alcanzó.",
        "- Tallo seco de granadilla. `pudrición` sí empuja a enfermedades. `tallo` pesa más hacia plagas y está repartido (9 y 9). La puntuación quedó en un casi empate, 0,19 frente a 0,17.",
        "- Palo del frijol. `palo` y `trepe` no están en el entrenamiento. `tutor` y `amarro` aparecen una sola vez y la versión 1 los descartó con `min_df=2`. El aporte mayor hacia cosecha fue la palabra funcional `lo`.",
        "- Fuera de alcance. El modelo solo conoce ocho clases y siempre elige una. Una puntuación baja no identifica una consulta fuera de alcance.",
        "- Empates. Un margen pequeño indica dos categorías agrícolas próximas, no una consulta ajena al cultivo.",
        "- Las puntuaciones de `predict_proba` no están calibradas.",
        "",
        "En la prueba bloqueada de la versión 1, riego fue la clase con más confusiones: 6 de 40, sobre todo con fertilización y cosecha. El patrón encaja con palabras compartidas (`grano`, `seco`), no con un fallo de lectura del archivo.",
        "",
        "## Qué se cambió",
        "",
        "Se buscó, solo dentro de las 1.276 consultas de entrenamiento de la versión 1, entre `min_df` 1 o 2, `C` 1 o 4, quitar o no las palabras funcionales, y unir o no los acentos. El criterio fue el macro-F1 medio de 5 pliegues estratificados, semilla 42. La prueba de 319 consultas quedó cerrada.",
        "",
        f"Configuración elegida: min_df={mejor['min_df']}, C={mejor['C']}, "
        f"sin palabras funcionales={mejor['sin_palabras_funcionales']}, "
        f"sin acentos={mejor['sin_acentos']}. "
        f"Macro-F1 de validación: {mejor['f1_macro_cv_media']:.4f}.",
        "",
        f"Abstención: devolver `sin categoría` si el margen entre las dos clases punteras es menor que {corte:.2f}. "
        "Ese corte salió del barrido sobre las probabilidades fuera de pliegue del entrenamiento, "
        f"exigiendo al menos {COBERTURA_MINIMA:.0%} de consultas clasificadas. "
        "`sin categoría` es abstención. No es `fuera_de_alcance` y no es una novena clase.",
        "",
        "No se añadieron frases para cubrir potasio, cafeto o el palo del frijol. Habría sido usar la prueba de inferencia para forzar el acierto.",
        "",
        "## Comparación en la misma prueba",
        "",
        f"- Versión 1. Accuracy {metricas_v1['accuracy']:.4f}. Macro-F1 {metricas_v1['f1_macro']:.4f}.",
        f"- Versión 2, sin abstención. Accuracy {metricas_v2['accuracy']:.4f}. Macro-F1 {metricas_v2['f1_macro']:.4f}.",
        "",
        "Versión 2:",
        "",
        *tabla(metricas_v2),
        "",
        "Con el umbral ya fijado, en esa misma prueba:",
        "",
        f"- Clasificadas: {abstencion_prueba['clasificadas']} de {abstencion_prueba['n']} ({abstencion_prueba['cobertura']:.1%}).",
        f"- Abstenciones: {abstencion_prueba['abstenciones']} ({abstencion_prueba['abstencion']:.1%}).",
        f"- Accuracy entre las clasificadas: {abstencion_prueba['accuracy_clasificadas']:.4f}.",
        f"- Macro-F1 entre las clasificadas: {abstencion_prueba['f1_macro_clasificadas']:.4f}.",
        f"- Errores entre las clasificadas: {abstencion_prueba['errores_entre_clasificadas']}.",
        "",
        "Esas cifras de abstención en prueba no se usaron para mover el corte.",
        "",
        "## Sondas que no ajustaron el modelo",
        "",
        f"- Anexo fuera de alcance, {sonda_fuera['n']} consultas: {sonda_fuera['abstenciones']} abstenidas y {sonda_fuera['con_categoria_forzada']} siguieron recibiendo una de las ocho.",
        f"- Cola ambigua, {sonda_ambigua['n']} consultas: {sonda_ambigua['abstenciones']} abstenidas y {sonda_ambigua['con_categoria_forzada']} recibieron una categoría.",
        "",
        "Lectura posterior de las 21 consultas ilustrativas, también sin usarla para ajustar:",
        "",
        "| Id | v1 | v2 | Salida v2 | Margen |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for fila in lectura_inferencia:
        lineas.append(
            f"| {fila['id']} | {fila['v1']} | {fila['v2_sin_abstencion']} | {fila['v2_salida']} | {fila['v2_margen']:.4f} |"
        )
    lineas.extend(
        [
            "",
            "## Datos que faltan para evaluar la abstención",
            "",
            "- Consultas fuera de alcance confirmadas por una persona, separadas de las agrícolas ambiguas, y que no entren al entrenamiento. Doce ejemplos sintéticos no alcanzan.",
            "- Consultas agrícolas con dos decisiones de igual peso, marcadas como ambiguas y no forzadas a una clase. Dieciséis ejemplos pendientes no alcanzan.",
            "- Etiquetas resueltas del conjunto principal. Hoy siguen siendo propuestas.",
            "- Consultas reales de productores, en otro conjunto, antes de hablar de uso en chacra.",
            "",
            "## Limitaciones",
            "",
            "- El macro-F1 alto sigue midiendo textos sintéticos con la etiqueta propuesta.",
            "- Quitar palabras funcionales o bajar `min_df` no crea las palabras que el entrenamiento nunca vio.",
            "- El corte se calculó con modelos de pliegues y se aplica al modelo reajustado con todo el entrenamiento. La escala del margen puede moverse un poco.",
            "- Una puntuación baja no se traduce a fuera de alcance.",
            "- `predict_proba` no está calibrada.",
            "- El PMV1, el RAG, RAGAS, la taxonomía y la base de conocimientos no se modificaron.",
            "",
            "Versiones: " + ", ".join(f"{clave} {valor}" for clave, valor in versiones.items()) + ".",
            "",
        ]
    )
    (AQUI / "informe_tecnico.md").write_text("\n".join(lineas), encoding="utf-8")
    print(
        json.dumps(
            {
                "config": mejor,
                "margen": corte,
                "f1_v1": round(metricas_v1["f1_macro"], 4),
                "f1_v2": round(metricas_v2["f1_macro"], 4),
                "acc_v2": round(metricas_v2["accuracy"], 4),
                "abstencion_prueba": abstencion_prueba["abstencion"],
                "accuracy_clasificadas": round(abstencion_prueba["accuracy_clasificadas"], 4),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
