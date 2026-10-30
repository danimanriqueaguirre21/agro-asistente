"""Evalúa el modelo HU-08 ya entrenado sobre prueba.jsonl.

No reentrena, no lee el entrenamiento para ajustar nada y no escribe
en el conjunto de prueba ni en el archivo del modelo.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

from preprocesamiento_riesgo_hu08 import NIVELES, ORDEN_VARIABLES  # noqa: E402

ARCHIVO_PRUEBA = AQUI / "prueba.jsonl"
ARCHIVO_PARTICIONES = AQUI / "ids_particiones.json"
ARCHIVO_MODELO = AQUI / "modelo_riesgo_hu08.joblib"
ARCHIVO_METRICAS = AQUI / "metricas_prueba_hu08.json"
ARCHIVO_MATRIZ = AQUI / "matriz_confusion_prueba_hu08.json"
ARCHIVO_INFORME = AQUI / "informe_evaluacion_prueba_hu08.md"
REGISTROS_ESPERADOS = 144
VARIABLES_CON_NULO = {"temperatura_c", "precipitacion_mm"}


def _sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def _fallar(mensaje: str) -> None:
    raise SystemExit(mensaje)


def cargar_prueba() -> list[dict[str, object]]:
    if not ARCHIVO_PRUEBA.is_file():
        _fallar("No se encuentra prueba.jsonl.")
    filas: list[dict[str, object]] = []
    with ARCHIVO_PRUEBA.open(encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            if not linea.strip():
                continue
            try:
                fila = json.loads(linea)
            except json.JSONDecodeError as error:
                _fallar(f"La línea {numero} de prueba.jsonl no es JSON válido: {error}.")
            if not isinstance(fila, dict):
                _fallar(f"La línea {numero} de prueba.jsonl no es un objeto.")
            filas.append(fila)
    if len(filas) != REGISTROS_ESPERADOS:
        _fallar(
            f"Se esperaban {REGISTROS_ESPERADOS} registros de prueba y hay {len(filas)}."
        )
    particiones = json.loads(ARCHIVO_PARTICIONES.read_text(encoding="utf-8"))
    identificadores = [str(fila.get("id", "")) for fila in filas]
    if any(not identificador for identificador in identificadores):
        _fallar("Hay un registro de prueba sin identificador.")
    if len(set(identificadores)) != len(identificadores):
        _fallar("Hay identificadores repetidos en prueba.jsonl.")
    if set(identificadores) != set(particiones["prueba"]):
        _fallar("prueba.jsonl no coincide con los identificadores reservados para la prueba.")
    if set(identificadores) & set(particiones["entrenamiento"]):
        _fallar("El conjunto de prueba comparte identificadores con el entrenamiento.")
    for fila in filas:
        etiqueta = fila.get("nivel_riesgo")
        if etiqueta not in NIVELES:
            _fallar(
                f"El registro {fila.get('id')} no tiene una etiqueta bajo, medio o alto."
            )
        for nombre in ORDEN_VARIABLES:
            if nombre not in fila:
                _fallar(f"Al registro {fila.get('id')} le falta la variable {nombre}.")
            if fila[nombre] is None and nombre not in VARIABLES_CON_NULO:
                _fallar(
                    f"El registro {fila.get('id')} tiene nulo en {nombre}, "
                    "y esa variable no admite ausencia."
                )
    return filas


def matriz_de(filas: list[dict[str, object]]) -> tuple[np.ndarray, np.ndarray]:
    matriz = np.empty((len(filas), len(ORDEN_VARIABLES)), dtype=object)
    etiquetas = np.empty(len(filas), dtype=object)
    for i, fila in enumerate(filas):
        for j, nombre in enumerate(ORDEN_VARIABLES):
            matriz[i, j] = fila[nombre]
        etiquetas[i] = fila["nivel_riesgo"]
    return matriz, etiquetas


def cargar_modelo():
    if not ARCHIVO_MODELO.is_file():
        _fallar("No se encuentra modelo_riesgo_hu08.joblib.")
    import joblib

    modelo = joblib.load(ARCHIVO_MODELO)
    clases = {str(clase) for clase in modelo.named_steps["clasificador"].classes_}
    if clases != set(NIVELES):
        _fallar("El modelo guardado no tiene las clases bajo, medio y alto.")
    return modelo


def decimal(valor: float) -> str:
    return f"{valor:.4f}".replace(".", ",")


def escribir_informe(metricas: dict[str, object], matriz: list[list[int]]) -> None:
    por_categoria = metricas["por_categoria"]
    assert isinstance(por_categoria, dict)
    f1 = {nivel: float(por_categoria[nivel]["f1"]) for nivel in NIVELES}
    mejor = max(NIVELES, key=lambda nivel: f1[nivel])
    peor = min(NIVELES, key=lambda nivel: f1[nivel])
    reales = metricas["registros_por_etiqueta_real"]
    predichos = metricas["registros_por_categoria_predicha"]
    assert isinstance(reales, dict) and isinstance(predichos, dict)
    confusiones = []
    for i, real in enumerate(NIVELES):
        for j, predicha in enumerate(NIVELES):
            if i == j:
                continue
            cantidad = matriz[i][j]
            if cantidad:
                confusiones.append(f"{cantidad} de `{real}` se predijeron como `{predicha}`")
    diferencia = max(f1.values()) - min(f1.values())
    if diferencia < 0.05:
        equilibrio = "Las tres F1 están a menos de 0,05 entre sí. El desempeño es equilibrado."
    else:
        equilibrio = (
            f"La diferencia entre la F1 más alta y la más baja es {decimal(diferencia)}. "
            "El desempeño no es equilibrado."
        )
    lineas = [
        "# Evaluación en el conjunto de prueba — HU-08",
        "",
        "Esta evaluación compara las predicciones del modelo ya entrenado con las etiquetas sintéticas de `prueba.jsonl`. No mide riesgo agrícola real ni valida una metodología agronómica.",
        "",
        "No se reentrenó el modelo. No se usaron estos registros para elegir parámetros, umbrales ni reglas. No se calcularon probabilidades.",
        "",
        "## Resultado",
        "",
        f"- Registros evaluados: {metricas['registros']}.",
        f"- Predicciones correctas: {metricas['correctas']}.",
        f"- Predicciones incorrectas: {metricas['incorrectas']}.",
        f"- Accuracy: {decimal(float(metricas['accuracy']))}.",
        f"- Macro-F1: {decimal(float(metricas['macro_f1']))}.",
        "",
        "| Categoría real | Registros | Predichos como esa categoría | Precisión | Recall | F1 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for nivel in NIVELES:
        datos = por_categoria[nivel]
        lineas.append(
            f"| {nivel} | {reales[nivel]} | {predichos[nivel]} | "
            f"{decimal(float(datos['precision']))} | {decimal(float(datos['recall']))} | "
            f"{decimal(float(datos['f1']))} |"
        )
    lineas.extend(
        [
            "",
            "## Matriz de confusión",
            "",
            "Filas: etiqueta sintética. Columnas: predicción. Orden: bajo, medio, alto.",
            "",
            "| Real \\ Predicha | bajo | medio | alto |",
            "|---|---:|---:|---:|",
        ]
    )
    for i, nivel in enumerate(NIVELES):
        celdas = " | ".join(str(valor) for valor in matriz[i])
        lineas.append(f"| {nivel} | {celdas} |")
    errores_por_real = {
        nivel: int(sum(matriz[i]) - matriz[i][i]) for i, nivel in enumerate(NIVELES)
    }
    mayor_confusion = max(
        ((matriz[i][j], NIVELES[i], NIVELES[j]) for i in range(3) for j in range(3) if i != j),
        key=lambda item: item[0],
    )
    lineas.extend(
        [
            "",
            "## Lectura de las cifras",
            "",
            f"La F1 más alta es la de `{mejor}` ({decimal(f1[mejor])}). La más baja es la de `{peor}` ({decimal(f1[peor])}).",
            "",
            "Los errores están fuera de la diagonal: " + "; ".join(confusiones) + ".",
            "",
            (
                f"De las {metricas['incorrectas']} predicciones incorrectas, "
                + ", ".join(
                    f"{errores_por_real[nivel]} tienen etiqueta real `{nivel}`"
                    for nivel in NIVELES
                )
                + "."
            ),
            "",
            (
                f"La confusión más numerosa es `{mayor_confusion[1]}` predicho como "
                f"`{mayor_confusion[2]}` ({mayor_confusion[0]} registros)."
            ),
            "",
            equilibrio,
            "",
            "Esas cifras describen el acuerdo con la etiqueta sintética. No identifican una causa agronómica.",
            "",
            "## Limitaciones",
            "",
            "- Las etiquetas de referencia salen de `reglas_etiquetado_sintetico.md`. Acertarlas no demuestra un riesgo observado en un predio.",
            "- El conjunto tiene 144 registros sintéticos, 48 por categoría. No representa agricultores de Junín.",
            "- El preprocesamiento imputa temperatura y precipitación ausentes con la mediana aprendida en el entrenamiento. La regla de simulación, en cambio, no suma puntos cuando el dato falta.",
            "- No se informa una probabilidad. El bosque puede calcular puntuaciones, y esta evaluación no las trata como confianza calibrada.",
            "",
            "## Reproducir",
            "",
            "```text",
            "python backend/clasificacion/experimentos/hu08_riesgo/evaluar_modelo_riesgo_hu08.py",
            "```",
            "",
            f"SHA-256 de `prueba.jsonl`: `{metricas['sha256_prueba']}`.",
            "",
            f"SHA-256 de `modelo_riesgo_hu08.joblib`: `{metricas['sha256_modelo']}`.",
            "",
        ]
    )
    ARCHIVO_INFORME.write_text("\n".join(lineas), encoding="utf-8")


def main() -> None:
    hash_prueba_antes = _sha256(ARCHIVO_PRUEBA)
    hash_modelo_antes = _sha256(ARCHIVO_MODELO)
    filas = cargar_prueba()
    matriz, etiquetas = matriz_de(filas)
    modelo = cargar_modelo()
    predichas = modelo.predict(matriz)
    if len(predichas) != REGISTROS_ESPERADOS:
        _fallar("El modelo no devolvió una predicción por cada registro de prueba.")
    for predicha in predichas:
        if str(predicha) not in NIVELES:
            _fallar(f"El modelo devolvió una categoría fuera del prototipo: {predicha}.")
    precision, recall, f1, soporte = precision_recall_fscore_support(
        etiquetas,
        predichas,
        labels=NIVELES,
        zero_division=0,
    )
    matriz_conteo = confusion_matrix(etiquetas, predichas, labels=NIVELES).tolist()
    correctas = int(sum(matriz_conteo[i][i] for i in range(len(NIVELES))))
    reales = {nivel: int(soporte[i]) for i, nivel in enumerate(NIVELES)}
    predichos = {
        nivel: int(sum(fila[i] for fila in matriz_conteo))
        for i, nivel in enumerate(NIVELES)
    }
    metricas: dict[str, object] = {
        "conjunto": "prueba.jsonl",
        "registros": REGISTROS_ESPERADOS,
        "correctas": correctas,
        "incorrectas": REGISTROS_ESPERADOS - correctas,
        "accuracy": float(accuracy_score(etiquetas, predichas)),
        "macro_f1": float(f1_score(etiquetas, predichas, average="macro", labels=NIVELES)),
        "orden_categorias": list(NIVELES),
        "por_categoria": {
            nivel: {
                "precision": float(precision[i]),
                "recall": float(recall[i]),
                "f1": float(f1[i]),
                "soporte": int(soporte[i]),
            }
            for i, nivel in enumerate(NIVELES)
        },
        "registros_por_etiqueta_real": reales,
        "registros_por_categoria_predicha": predichos,
        "modelo": "modelo_riesgo_hu08.joblib",
        "reentrenado": False,
        "probabilidades_usadas": False,
        "sha256_prueba": hash_prueba_antes,
        "sha256_modelo": hash_modelo_antes,
    }
    ARCHIVO_METRICAS.write_text(
        json.dumps(metricas, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    ARCHIVO_MATRIZ.write_text(
        json.dumps(
            {
                "orden": list(NIVELES),
                "filas": "etiqueta_real",
                "columnas": "categoria_predicha",
                "matriz": matriz_conteo,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    escribir_informe(metricas, matriz_conteo)
    if _sha256(ARCHIVO_PRUEBA) != hash_prueba_antes:
        _fallar("La evaluación modificó prueba.jsonl.")
    if _sha256(ARCHIVO_MODELO) != hash_modelo_antes:
        _fallar("La evaluación modificó el modelo serializado.")
    print(json.dumps({
        "registros": metricas["registros"],
        "accuracy": metricas["accuracy"],
        "macro_f1": metricas["macro_f1"],
        "correctas": metricas["correctas"],
        "incorrectas": metricas["incorrectas"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
