"""Experimento preliminar HU-07: TF-IDF + regresión logística.

Usa las categorías propuestas de consultas_trabajo.jsonl.
No aprueba el dataset ni modifica el archivo original.
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
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

SEED = 42
TEST_SIZE = 0.20

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

# Informes existentes: sacar de las 1600 o excluir de entrenamiento.
EXCLUIR = {
    "trabajo-hu07-ead432668d": "Consulta compuesta. El informe pide sacarla de las 1600.",
    "trabajo-hu07-77fa929ec0": "Consulta compuesta. El informe pide sacarla de las 1600.",
    "trabajo-hu07-b7bf806a37": "Consulta compuesta. El informe pide sacarla de las 1600.",
    "trabajo-hu07-7791383f85": "Consulta compuesta. El informe pide sacarla de las 1600.",
    "trabajo-hu07-4da2de2e03": "El informe pide excluirla de entrenamiento por paráfrasis de ilustrativo-007.",
}

PAR = ("trabajo-hu07-d6612d79a4", "trabajo-hu07-628a8b17ab")

AQUI = Path(__file__).resolve().parent
DATOS = (
    AQUI.parents[1]
    / "preparacion"
    / "dataset_trabajo_hu07"
    / "consultas_trabajo.jsonl"
)
AMBIGUA = DATOS.with_name("cola_ambigua.jsonl")
FUERA = DATOS.with_name("fuera_de_alcance.jsonl")


def leer_jsonl(path: Path) -> list[dict]:
    filas = []
    with path.open(encoding="utf-8") as handle:
        for numero, linea in enumerate(handle, start=1):
            linea = linea.strip()
            if not linea:
                continue
            try:
                filas.append(json.loads(linea))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Línea {numero} ilegible en {path.name}: {exc}") from exc
    return filas


def contar_lineas(path: Path) -> int:
    if not path.is_file():
        return 0
    with path.open(encoding="utf-8") as handle:
        return sum(1 for linea in handle if linea.strip())


def validar(filas: list[dict]) -> None:
    vistos: set[str] = set()
    for indice, fila in enumerate(filas, start=1):
        for campo in ("id", "text", "proposed_category"):
            valor = fila.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                raise SystemExit(f"Registro {indice}: falta el campo {campo}.")
        if fila["id"] in vistos:
            raise SystemExit(f"Identificador repetido: {fila['id']}.")
        vistos.add(fila["id"])
        if fila["proposed_category"] not in CATEGORIAS:
            raise SystemExit(
                f"{fila['id']}: categoría no válida '{fila['proposed_category']}'."
            )


def reunir_par(filas: list[dict], train: np.ndarray, test: np.ndarray) -> tuple[np.ndarray, np.ndarray, str]:
    posicion = {fila["id"]: i for i, fila in enumerate(filas)}
    a = posicion.get(PAR[0])
    b = posicion.get(PAR[1])
    train_lista = train.tolist()
    test_lista = test.tolist()
    train_set = set(train_lista)
    test_set = set(test_lista)
    if a is None or b is None:
        return train, test, "El par no está completo en el conjunto usado."
    if (a in train_set and b in train_set) or (a in test_set and b in test_set):
        return train, test, "El par ya quedó en la misma partición."
    mover = a if a in test_set else b
    clase = filas[mover]["proposed_category"]
    candidatos = [
        i
        for i in train_lista
        if filas[i]["proposed_category"] == clase and i not in {a, b}
    ]
    if not candidatos:
        test_lista = [i for i in test_lista if i != mover]
        train_lista.append(mover)
        return np.array(train_lista), np.array(test_lista), "Par reunido en entrenamiento, sin reemplazo."
    reemplazo = candidatos[0]
    train_lista = [i for i in train_lista if i != reemplazo]
    train_lista.append(mover)
    test_lista = [i for i in test_lista if i != mover]
    test_lista.append(reemplazo)
    return (
        np.array(train_lista),
        np.array(test_lista),
        "Par reunido en la misma partición, con un reemplazo de la misma clase.",
    )


def main() -> None:
    if not DATOS.is_file():
        raise SystemExit(f"No se encuentra el dataset: {DATOS}")

    originales = leer_jsonl(DATOS)
    validar(originales)

    excluidas = [fila for fila in originales if fila["id"] in EXCLUIR]
    faltan = sorted(set(EXCLUIR) - {fila["id"] for fila in excluidas})
    if faltan:
        raise SystemExit("No aparecen en el dataset: " + ", ".join(faltan))

    usadas = [fila for fila in originales if fila["id"] not in EXCLUIR]
    textos = [fila["text"] for fila in usadas]
    etiquetas = [fila["proposed_category"] for fila in usadas]
    indices = np.arange(len(usadas))
    train_idx, test_idx = train_test_split(
        indices,
        test_size=TEST_SIZE,
        random_state=SEED,
        stratify=etiquetas,
    )
    train_idx, test_idx, nota_par = reunir_par(usadas, train_idx, test_idx)

    pipeline = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    analyzer="word",
                    ngram_range=(1, 2),
                    min_df=2,
                    sublinear_tf=True,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    C=1.0,
                    solver="lbfgs",
                    max_iter=2000,
                    random_state=SEED,
                ),
            ),
        ]
    )

    x_train = [textos[i] for i in train_idx]
    y_train = [etiquetas[i] for i in train_idx]
    x_test = [textos[i] for i in test_idx]
    y_test = [etiquetas[i] for i in test_idx]
    pipeline.fit(x_train, y_train)
    predichas = pipeline.predict(x_test)

    reporte = classification_report(
        y_test,
        predichas,
        labels=CATEGORIAS,
        output_dict=True,
        zero_division=0,
    )
    matriz = confusion_matrix(y_test, predichas, labels=CATEGORIAS).tolist()
    por_categoria = {
        categoria: {
            "precision": reporte[categoria]["precision"],
            "recall": reporte[categoria]["recall"],
            "f1": reporte[categoria]["f1-score"],
            "support": reporte[categoria]["support"],
        }
        for categoria in CATEGORIAS
    }

    distribucion_usada = Counter(etiquetas)
    distribucion_train = Counter(y_train)
    distribucion_test = Counter(y_test)
    metricas = {
        "caracter": "preliminar",
        "definitivo": False,
        "dataset_aprobado": False,
        "etiquetas": "proposed_category, sin aprobación humana",
        "accuracy": accuracy_score(y_test, predichas),
        "precision_macro": precision_score(y_test, predichas, average="macro", zero_division=0),
        "recall_macro": recall_score(y_test, predichas, average="macro", zero_division=0),
        "f1_macro": f1_score(y_test, predichas, average="macro", zero_division=0),
        "precision_weighted": precision_score(
            y_test, predichas, average="weighted", zero_division=0
        ),
        "recall_weighted": recall_score(y_test, predichas, average="weighted", zero_division=0),
        "f1_weighted": f1_score(y_test, predichas, average="weighted", zero_division=0),
        "por_categoria": por_categoria,
        "conjunto": "prueba",
        "nota": "Métricas del conjunto de prueba. No se usó para elegir parámetros.",
    }

    versiones = {
        "python": sys.version.split()[0],
        "plataforma": platform.platform(),
        "scikit-learn": sklearn.__version__,
        "numpy": np.__version__,
        "joblib": joblib.__version__,
    }
    config = {
        "seed": SEED,
        "test_size": TEST_SIZE,
        "vectorizador": {
            "tipo": "TfidfVectorizer",
            "lowercase": True,
            "analyzer": "word",
            "ngram_range": [1, 2],
            "min_df": 2,
            "sublinear_tf": True,
        },
        "clasificador": {
            "tipo": "LogisticRegression",
            "C": 1.0,
            "solver": "lbfgs",
            "max_iter": 2000,
            "random_state": SEED,
        },
        "ajuste_de_parametros": "No hubo búsqueda. La configuración es fija.",
        "umbral_de_abstencion": "No calculado en este experimento.",
    }

    modelo_path = AQUI / "modelo_tfidf_logreg.joblib"
    joblib.dump(pipeline, modelo_path)

    (AQUI / "metricas.json").write_text(
        json.dumps(metricas, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (AQUI / "matriz_confusion.json").write_text(
        json.dumps({"labels": CATEGORIAS, "matrix": matriz}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (AQUI / "versiones.json").write_text(
        json.dumps(versiones, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    particiones = {
        "nota_par": nota_par,
        "entrenamiento": [usadas[i]["id"] for i in train_idx],
        "prueba": [usadas[i]["id"] for i in test_idx],
    }
    (AQUI / "ids_particiones.json").write_text(
        json.dumps(particiones, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    manifiesto = {
        "experimento": "hu07-tfidf-logreg-preliminar",
        "dataset": str(DATOS.relative_to(AQUI.parents[3])).replace("\\", "/"),
        "dataset_modificado": False,
        "dataset_aprobado": False,
        "approval_status": "no_aprobado",
        "origen": "sintetico_preparacion",
        "consultas_reales": 0,
        "registros_leidos": len(originales),
        "excluidos": [
            {"id": fila["id"], "motivo": EXCLUIR[fila["id"]], "proposed_category": fila["proposed_category"]}
            for fila in excluidas
        ],
        "anexos_no_cargados": {
            "cola_ambigua.jsonl": contar_lineas(AMBIGUA),
            "fuera_de_alcance.jsonl": contar_lineas(FUERA),
        },
        "registros_usados": len(usadas),
        "distribucion_usada": dict(distribucion_usada),
        "entrenamiento": len(train_idx),
        "prueba": len(test_idx),
        "distribucion_entrenamiento": dict(distribucion_train),
        "distribucion_prueba": dict(distribucion_test),
        "integrado_en_produccion": False,
        "pmv1_modificado": False,
        "modelo": modelo_path.name,
    }
    (AQUI / "manifiesto_experimento.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lineas = [
        "# Informe técnico — experimento preliminar HU-07",
        "",
        "Experimento técnico sobre categorías propuestas. El dataset no está aprobado. Las consultas son sintéticas. Las métricas no son un resultado definitivo ni describen consultas reales de productores.",
        "",
        "## Datos",
        "",
        f"- Archivo leído, sin modificar: `{manifiesto['dataset']}`.",
        f"- Registros leídos: {len(originales)}.",
        f"- Usados en el experimento: {len(usadas)}.",
        f"- Entrenamiento: {len(train_idx)}. Prueba: {len(test_idx)}. Semilla: {SEED}.",
        f"- Partición del par de la polilla del olluco: {nota_par}",
        "",
        "Excluidos del entrenamiento:",
        "",
    ]
    for fila in excluidas:
        lineas.append(f"- `{fila['id']}` ({fila['proposed_category']}): {EXCLUIR[fila['id']]}")
    lineas.extend(
        [
            "",
            f"No se cargaron los anexos: cola ambigua ({manifiesto['anexos_no_cargados']['cola_ambigua.jsonl']}) y fuera de alcance ({manifiesto['anexos_no_cargados']['fuera_de_alcance.jsonl']}).",
            "",
            "Distribución usada, por categoría propuesta:",
            "",
        ]
    )
    for categoria in CATEGORIAS:
        lineas.append(
            f"- {categoria}: {distribucion_usada[categoria]} "
            f"(entrenamiento {distribucion_train[categoria]}, prueba {distribucion_test[categoria]})"
        )
    lineas.extend(
        [
            "",
            "## Modelo",
            "",
            "Pipeline de `TfidfVectorizer` (palabras y bigramas, `min_df=2`, `sublinear_tf`) y `LogisticRegression` (`C=1.0`, `solver=lbfgs`, `max_iter=2000`). No hubo búsqueda de parámetros. El conjunto de prueba no se usó para elegir la configuración.",
            "",
            "## Métricas en prueba",
            "",
            f"- Accuracy: {metricas['accuracy']:.4f}",
            f"- Precision macro: {metricas['precision_macro']:.4f}",
            f"- Recall macro: {metricas['recall_macro']:.4f}",
            f"- F1 macro: {metricas['f1_macro']:.4f}",
            f"- F1 ponderado: {metricas['f1_weighted']:.4f}",
            "",
            "| Categoría | Precision | Recall | F1 | Soporte |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for categoria in CATEGORIAS:
        item = por_categoria[categoria]
        lineas.append(
            f"| {categoria} | {item['precision']:.4f} | {item['recall']:.4f} | {item['f1']:.4f} | {int(item['support'])} |"
        )
    lineas.extend(["", "Matriz de confusión (filas: etiqueta propuesta; columnas: predicción), en el orden de las ocho categorías:", "", "```"])
    for fila_matriz in matriz:
        lineas.append(" ".join(f"{valor:4d}" for valor in fila_matriz))
    peor = sorted(por_categoria.items(), key=lambda item: item[1]["f1"])[:3]
    lineas.extend(
        [
            "```",
            "",
            "Categorías con F1 más bajo en esta prueba: "
            + ", ".join(f"{nombre} ({datos['f1']:.4f})" for nombre, datos in peor)
            + ".",
            "",
            "## Limitaciones",
            "",
            "- Las etiquetas son propuestas. No hay aprobación humana registrada.",
            "- El texto es sintético. El resultado no dice cómo respondería el modelo a consultas reales.",
            "- El modelo no está integrado al PMV1, al RAG ni a producción.",
            "- No se calculó un umbral de abstención.",
            "- La división es estratificada y reproducible, con el par cercano de la polilla del olluco forzado a la misma partición. No se rehizo una búsqueda general de paráfrasis.",
            "",
            "Versiones: "
            + ", ".join(f"{clave} {valor}" for clave, valor in versiones.items())
            + ".",
            "",
        ]
    )
    (AQUI / "informe_tecnico.md").write_text("\n".join(lineas), encoding="utf-8")
    print(json.dumps({
        "usados": len(usadas),
        "entrenamiento": len(train_idx),
        "prueba": len(test_idx),
        "accuracy": round(metricas["accuracy"], 4),
        "f1_macro": round(metricas["f1_macro"], 4),
        "modelo": str(modelo_path),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
