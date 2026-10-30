"""Entrena el clasificador sintético de HU-08.

Usa solo entrenamiento.jsonl. La elección del modelo sale de validación
cruzada dentro de ese archivo. No lee prueba.jsonl.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
from sklearn import __version__ as sklearn_version
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

RAIZ = Path(__file__).resolve().parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from preprocesamiento_riesgo_hu08 import (  # noqa: E402
    ETIQUETA,
    NIVELES,
    ORDEN_VARIABLES,
    construir_columnas,
    marcar_ausentes,
)

SEMILLA = 42
PLIEGUES = 5
ARCHIVO_ENTRENAMIENTO = RAIZ / "entrenamiento.jsonl"
ARCHIVO_PARTICIONES = RAIZ / "ids_particiones.json"
ARCHIVO_MODELO = RAIZ / "modelo_riesgo_hu08.joblib"
ARCHIVO_METRICAS = RAIZ / "metricas_validacion_cruzada_hu08.json"
ARCHIVO_CONFIGURACION = RAIZ / "configuracion_seleccionada_hu08.json"
ARCHIVO_INFORME = RAIZ / "informe_tecnico_hu08.md"
ARCHIVO_INSTRUCCIONES = RAIZ / "instrucciones_reproduccion_hu08.md"


def cargar_entrenamiento() -> list[dict[str, object]]:
    filas = []
    with ARCHIVO_ENTRENAMIENTO.open(encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.strip():
                filas.append(json.loads(linea))
    particiones = json.loads(ARCHIVO_PARTICIONES.read_text(encoding="utf-8"))
    identificadores = {str(fila["id"]) for fila in filas}
    esperados = set(particiones["entrenamiento"])
    if identificadores != esperados:
        raise SystemExit("entrenamiento.jsonl no coincide con los identificadores de entrenamiento.")
    if identificadores & set(particiones["prueba"]):
        raise SystemExit("El entrenamiento contiene identificadores del conjunto de prueba.")
    if len(filas) != 576:
        raise SystemExit(f"Se esperaban 576 filas de entrenamiento y hay {len(filas)}.")
    return filas


def matriz_variables(filas: list[dict[str, object]]) -> tuple[np.ndarray, np.ndarray]:
    matriz = np.empty((len(filas), len(ORDEN_VARIABLES)), dtype=object)
    etiquetas = np.empty(len(filas), dtype=object)
    for i, fila in enumerate(filas):
        if fila.get("es_observacion_real") is not False:
            raise SystemExit("Hay una fila marcada como observación real.")
        etiqueta = fila.get(ETIQUETA)
        if etiqueta not in NIVELES:
            raise SystemExit(f"Etiqueta no permitida: {etiqueta}")
        for j, nombre in enumerate(ORDEN_VARIABLES):
            if nombre not in fila:
                raise SystemExit(f"Falta la variable {nombre}.")
            matriz[i, j] = fila[nombre]
        etiquetas[i] = etiqueta
    return matriz, etiquetas


def construir_pipeline(estimador: object, escalar_numericas: bool) -> Pipeline:
    return Pipeline(
        [
            (
                "marcar_ausentes",
                FunctionTransformer(
                    marcar_ausentes,
                    feature_names_out="one-to-one",
                    validate=False,
                ),
            ),
            ("columnas", construir_columnas(escalar_numericas)),
            ("clasificador", estimador),
        ]
    )


def candidatos() -> list[dict[str, object]]:
    lista: list[dict[str, object]] = []
    for c_valor in (0.1, 1.0, 4.0):
        lista.append(
            {
                "nombre": f"regresion_logistica_C{c_valor}",
                "familia": "regresion_logistica",
                "escalar_numericas": True,
                "complejidad": 0 if c_valor == 0.1 else (1 if c_valor == 1.0 else 2),
                "parametros": {
                    "C": c_valor,
                    "solver": "lbfgs",
                    "max_iter": 2000,
                    "random_state": SEMILLA,
                },
                "estimador": LogisticRegression(
                    C=c_valor,
                    solver="lbfgs",
                    max_iter=2000,
                    random_state=SEMILLA,
                ),
            }
        )
    for profundidad in (6, 12, None):
        for hoja in (1, 4):
            texto_profundidad = "sin_limite" if profundidad is None else str(profundidad)
            lista.append(
                {
                    "nombre": f"bosque_aleatorio_profundidad{texto_profundidad}_hoja{hoja}",
                    "familia": "bosque_aleatorio",
                    "escalar_numericas": False,
                    "complejidad": 10 + (99 if profundidad is None else profundidad) - hoja,
                    "parametros": {
                        "n_estimators": 200,
                        "max_depth": profundidad,
                        "min_samples_leaf": hoja,
                        "random_state": SEMILLA,
                        "n_jobs": 1,
                    },
                    "estimador": RandomForestClassifier(
                        n_estimators=200,
                        max_depth=profundidad,
                        min_samples_leaf=hoja,
                        random_state=SEMILLA,
                        n_jobs=1,
                    ),
                }
            )
    return lista


def evaluar(pipeline: Pipeline, matriz: np.ndarray, etiquetas: np.ndarray) -> dict[str, object]:
    cortes = StratifiedKFold(n_splits=PLIEGUES, shuffle=True, random_state=SEMILLA)
    macro: list[float] = []
    exactitud: list[float] = []
    predicciones = np.empty(len(etiquetas), dtype=object)
    for entrenamiento, validacion in cortes.split(matriz, etiquetas):
        copia = clone(pipeline)
        copia.fit(matriz[entrenamiento], etiquetas[entrenamiento])
        predichas = copia.predict(matriz[validacion])
        predicciones[validacion] = predichas
        macro.append(float(f1_score(etiquetas[validacion], predichas, average="macro", labels=NIVELES)))
        exactitud.append(float(accuracy_score(etiquetas[validacion], predichas)))
    precision, recall, f1, soporte = precision_recall_fscore_support(
        etiquetas,
        predicciones,
        labels=NIVELES,
        zero_division=0,
    )
    return {
        "macro_f1_por_pliegue": [round(valor, 6) for valor in macro],
        "accuracy_por_pliegue": [round(valor, 6) for valor in exactitud],
        "macro_f1_media": float(np.mean(macro)),
        "macro_f1_desviacion": float(np.std(macro)),
        "accuracy_media": float(np.mean(exactitud)),
        "accuracy_desviacion": float(np.std(exactitud)),
        "por_categoria_oof": {
            nivel: {
                "precision": float(precision[i]),
                "recall": float(recall[i]),
                "f1": float(f1[i]),
                "soporte": int(soporte[i]),
            }
            for i, nivel in enumerate(NIVELES)
        },
        "matriz_confusion_oof": confusion_matrix(etiquetas, predicciones, labels=NIVELES).tolist(),
    }


def elegir(resultados: list[dict[str, object]]) -> dict[str, object]:
    return max(
        resultados,
        key=lambda item: (
            round(float(item["macro_f1_media"]), 6),
            round(float(item["accuracy_media"]), 6),
            -int(item["complejidad"]),
        ),
    )


def contar_nulos(matriz: np.ndarray) -> dict[str, int]:
    conteo = {}
    for indice, nombre in enumerate(ORDEN_VARIABLES):
        conteo[nombre] = int(sum(valor is None for valor in matriz[:, indice]))
    return conteo


def escribir_informe(
    nulos: dict[str, int],
    resultados: list[dict[str, object]],
    elegido: dict[str, object],
    nombres_salida: list[str],
) -> None:
    def decimal(valor: object) -> str:
        return f"{float(valor):.4f}".replace(".", ",")

    lineas = [
        "# Informe técnico — entrenamiento HU-08",
        "",
        "Prototipo académico. Las métricas miden si el clasificador reproduce las etiquetas sintéticas del conjunto de entrenamiento mediante validación cruzada. No miden riesgo agrícola real y no usan `prueba.jsonl`.",
        "",
        "## Modelo seleccionado",
        "",
        f"Configuración: `{elegido['nombre']}`.",
        "",
        f"Criterio, aplicado solo a la validación cruzada: mayor macro-F1 media; en empate a seis decimales, mayor accuracy media; si continúa el empate, menor complejidad. La regresión logística se considera más simple que el bosque aleatorio.",
        "",
        f"Macro-F1 media: {decimal(elegido['macro_f1_media'])}. Accuracy media: {decimal(elegido['accuracy_media'])}.",
        "",
        "El pipeline guardado se reajustó con los 576 registros de entrenamiento después de la elección. Ese reajuste no se usó para comparar modelos.",
        "",
        "## Variables",
        "",
        "Entran, en este orden: " + ", ".join(f"`{nombre}`" for nombre in ORDEN_VARIABLES) + ".",
        "",
        "No entran `id`, `origen`, `es_observacion_real`, `version_reglas` ni la etiqueta `nivel_riesgo`.",
        "",
        "`sintoma_observado` se codifica como texto `true` o `false` antes de la imputación. Esa conversión no sustituye un nulo por cero.",
        "",
        "## Valores ausentes",
        "",
        "No se eliminó ninguna de las 576 filas. Un nulo de JSON se representa como NaN y el imputador del pliegue lo trata. No se escribe cero en el lugar del dato faltante.",
        "",
        "| Variable | Nulos en entrenamiento | Tratamiento dentro del pipeline |",
        "|---|---:|---|",
    ]
    for nombre in ORDEN_VARIABLES:
        if nombre in ("temperatura_c", "precipitacion_mm"):
            tratamiento = "Mediana del pliegue de entrenamiento e indicador de ausencia."
        elif nombre in ("dias_sin_lluvia", "proporcion_afectada"):
            tratamiento = "Mediana del pliegue. En este archivo no hay nulos."
        else:
            tratamiento = "Moda del pliegue y codificación one-hot. En este archivo no hay nulos."
        lineas.append(f"| {nombre} | {nulos[nombre]} | {tratamiento} |")
    lineas.extend(
        [
            "",
            "La mediana y la moda se calculan solo con las filas de entrenamiento de cada pliegue. La regresión logística, además, estandariza sus variables numéricas después de imputar. El bosque aleatorio no las estandariza.",
            "",
            "El indicador de ausencia vale 1 cuando el valor original faltaba y 0 cuando estaba presente. No es el valor imputado de la temperatura ni de la precipitación.",
            "",
            "## Semilla y configuración",
            "",
            f"- Semilla: {SEMILLA}.",
            f"- Validación: StratifiedKFold de {PLIEGUES} pliegues, con barajado y la misma semilla.",
            "- Regresión logística: solver `lbfgs`, máximo 2000 iteraciones, C en 0,1, 1 y 4.",
            "- Bosque aleatorio: 200 árboles, `n_jobs` 1, profundidad 6, 12 o sin límite, y mínimo de muestras por hoja 1 o 4.",
            f"- scikit-learn {sklearn_version}.",
            "",
            "## Comparación",
            "",
            "Todas las cifras de esta tabla son medias de los cinco pliegues. Las métricas por categoría salen de las predicciones fuera de pliegue, otra vez solo sobre entrenamiento.",
            "",
            "| Configuración | Macro-F1 | Accuracy | F1 bajo | F1 medio | F1 alto |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for item in resultados:
        por_categoria = item["por_categoria_oof"]
        assert isinstance(por_categoria, dict)
        lineas.append(
            "| "
            + str(item["nombre"])
            + f" | {decimal(item['macro_f1_media'])} | {decimal(item['accuracy_media'])} | "
            + f"{decimal(por_categoria['bajo']['f1'])} | {decimal(por_categoria['medio']['f1'])} | "
            + f"{decimal(por_categoria['alto']['f1'])} |"
        )
    por_categoria = elegido["por_categoria_oof"]
    assert isinstance(por_categoria, dict)
    matriz = elegido["matriz_confusion_oof"]
    lineas.extend(
        [
            "",
            "### Categorías del modelo seleccionado",
            "",
            "Predicciones fuera de pliegue. El orden de la matriz es bajo, medio, alto. Cada fila es la etiqueta sintética y cada columna es la predicción.",
            "",
            "| Categoría | Precisión | Recall | F1 | Soporte |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for nivel in NIVELES:
        datos = por_categoria[nivel]
        lineas.append(
            f"| {nivel} | {decimal(datos['precision'])} | {decimal(datos['recall'])} | "
            f"{decimal(datos['f1'])} | {datos['soporte']} |"
        )
    lineas.extend(["", "```text"])
    for fila in matriz:
        lineas.append(" ".join(str(valor) for valor in fila))
    lineas.extend(
        [
            "```",
            "",
            "## Salida del preprocesamiento",
            "",
            "El pipeline conservó el orden de entrada de las diez variables. La codificación one-hot y los indicadores de ausencia amplían esa entrada. Los nombres de salida del modelo guardado son:",
            "",
        ]
    )
    for nombre in nombres_salida:
        lineas.append(f"- `{nombre}`")
    lineas.extend(
        [
            "",
            "## Limitaciones",
            "",
            "- Las etiquetas son supuestos de simulación de `reglas_etiquetado_sintetico.md`. Un macro-F1 alto solo diría que el modelo se acerca a esas reglas, no que predice daño en un predio.",
            "- No hay observaciones reales de agricultores ni unidades leídas de SENAMHI.",
            "- `cultivo` y `region` no definen la etiqueta sintética. Si el modelo les da peso, está usando variación que la simulación no relacionó con el nivel.",
            "- La etapa pesa en las reglas. Parte del resultado puede venir de esa variable y no de una relación agronómica.",
            "- La mediana no reproduce la regla de simulación, que trata el nulo como ausencia de puntos y no como el valor típico.",
            "- Esta corrida no evalúa `prueba.jsonl`. Esa evaluación queda fuera de esta actividad.",
            "- El modelo no está integrado al backend.",
            "",
            "## Archivos de esta actividad",
            "",
            "- `preprocesamiento_riesgo_hu08.py`",
            "- `entrenar_modelo_riesgo_hu08.py`",
            "- `configuracion_seleccionada_hu08.json`",
            "- `metricas_validacion_cruzada_hu08.json`",
            "- `modelo_riesgo_hu08.joblib`",
            "- `informe_tecnico_hu08.md`",
            "- `instrucciones_reproduccion_hu08.md`",
            "",
            "## Reproducir",
            "",
            "```text",
            "python entrenar_modelo_riesgo_hu08.py",
            "```",
            "",
            "El comando se ejecuta en `backend/clasificacion/experimentos/hu08_riesgo`. También funciona con la ruta absoluta del script, porque lee y escribe junto a ese archivo.",
            "",
        ]
    )
    ARCHIVO_INFORME.write_text("\n".join(lineas), encoding="utf-8")


def escribir_instrucciones() -> None:
    texto = """# Reproducir el entrenamiento HU-08

Prototipo académico. El comando vuelve a entrenar con `entrenamiento.jsonl` y la semilla 42. No lee `prueba.jsonl` y no modifica los JSONL.

Requisitos ya usados por el proyecto: Python 3.13, scikit-learn 1.9 y joblib. No hace falta pandas.

```text
python "backend/clasificacion/experimentos/hu08_riesgo/entrenar_modelo_riesgo_hu08.py"
```

También se puede ejecutar desde esta carpeta:

```text
python entrenar_modelo_riesgo_hu08.py
```

El script sobrescribe solo los artefactos de entrenamiento de HU-08: el joblib, las métricas, la configuración, este instructivo y el informe técnico.

Para cargar después el pipeline hace falta que este directorio esté en la ruta de importación, porque el preprocesamiento vive en `preprocesamiento_riesgo_hu08.py`:

```text
import sys
from pathlib import Path
import joblib

carpeta = Path("backend/clasificacion/experimentos/hu08_riesgo")
sys.path.insert(0, str(carpeta))
pipeline = joblib.load(carpeta / "modelo_riesgo_hu08.joblib")
```

La entrada de `predict` es una matriz con las diez variables en el orden guardado en `configuracion_seleccionada_hu08.json`. Un valor ausente se pasa como `None` o como NaN. No se rellena con cero antes de llamar al pipeline.
"""
    ARCHIVO_INSTRUCCIONES.write_text(texto, encoding="utf-8")


def main() -> None:
    if ARCHIVO_ENTRENAMIENTO.name != "entrenamiento.jsonl":
        raise SystemExit("El entrenamiento solo puede leer entrenamiento.jsonl.")
    filas = cargar_entrenamiento()
    matriz, etiquetas = matriz_variables(filas)
    nulos = contar_nulos(matriz)
    if nulos["temperatura_c"] == 0 and nulos["precipitacion_mm"] == 0:
        raise SystemExit("Se esperaban nulos de temperatura o precipitación y no se encontraron.")
    resultados = []
    for candidato in candidatos():
        pipeline = construir_pipeline(candidato["estimador"], bool(candidato["escalar_numericas"]))
        metricas = evaluar(pipeline, matriz, etiquetas)
        metricas["nombre"] = candidato["nombre"]
        metricas["familia"] = candidato["familia"]
        metricas["complejidad"] = candidato["complejidad"]
        metricas["parametros"] = candidato["parametros"]
        metricas["escalar_numericas"] = candidato["escalar_numericas"]
        resultados.append(metricas)
    elegido = elegir(resultados)
    ganador = next(item for item in candidatos() if item["nombre"] == elegido["nombre"])
    pipeline_final = construir_pipeline(ganador["estimador"], bool(ganador["escalar_numericas"]))
    pipeline_final.fit(matriz, etiquetas)
    nombres_salida = [str(nombre) for nombre in pipeline_final.named_steps["columnas"].get_feature_names_out()]
    joblib.dump(pipeline_final, ARCHIVO_MODELO)
    comparacion = []
    for item in resultados:
        visible = {clave: valor for clave, valor in item.items() if clave != "estimador"}
        comparacion.append(visible)
    ARCHIVO_METRICAS.write_text(
        json.dumps(
            {
                "conjunto": "entrenamiento.jsonl",
                "prueba_jsonl_consultada": False,
                "registros": len(filas),
                "semilla": SEMILLA,
                "pliegues": PLIEGUES,
                "nulos": nulos,
                "criterio_seleccion": [
                    "mayor macro_f1_media",
                    "mayor accuracy_media",
                    "menor complejidad",
                ],
                "modelos": comparacion,
                "seleccionado": elegido["nombre"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    ARCHIVO_CONFIGURACION.write_text(
        json.dumps(
            {
                "modelo": elegido["nombre"],
                "familia": elegido["familia"],
                "parametros": elegido["parametros"],
                "escalar_numericas": elegido["escalar_numericas"],
                "semilla": SEMILLA,
                "pliegues": PLIEGUES,
                "orden_variables_entrada": list(ORDEN_VARIABLES),
                "nombres_salida": nombres_salida,
                "etiqueta": ETIQUETA,
                "niveles": list(NIVELES),
                "artefacto": ARCHIVO_MODELO.name,
                "registros_entrenamiento": len(filas),
                "prueba_jsonl_consultada": False,
                "tratamiento_ausentes": {
                    "temperatura_c": "mediana e indicador de ausencia",
                    "precipitacion_mm": "mediana e indicador de ausencia",
                    "resto_numerico": "mediana",
                    "categoricas": "moda y one-hot",
                    "relleno_con_cero": False,
                    "filas_eliminadas": 0,
                },
                "versiones": {
                    "python": sys.version.split()[0],
                    "scikit_learn": sklearn_version,
                    "numpy": np.__version__,
                    "joblib": joblib.__version__,
                },
                "macro_f1_media_validacion": elegido["macro_f1_media"],
                "accuracy_media_validacion": elegido["accuracy_media"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    escribir_informe(nulos, resultados, elegido, nombres_salida)
    escribir_instrucciones()
    print(elegido["nombre"])
    print(round(float(elegido["macro_f1_media"]), 4))
    print(round(float(elegido["accuracy_media"]), 4))


if __name__ == "__main__":
    main()
