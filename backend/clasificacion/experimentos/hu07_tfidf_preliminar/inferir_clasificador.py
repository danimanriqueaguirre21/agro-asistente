"""Inferencia ilustrativa del modelo HU-07 ya entrenado.

No vuelve a entrenar, no escribe el modelo y no toca el dataset original.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib

AQUI = Path(__file__).resolve().parent
MODELO = AQUI / "modelo_tfidf_logreg.joblib"
CASOS = AQUI / "consultas_inferencia.json"
DATOS = (
    AQUI.parents[1]
    / "preparacion"
    / "dataset_trabajo_hu07"
    / "consultas_trabajo.jsonl"
)
# Corte solo para leer esta prueba. No es un umbral de abstención elegido con validación.
CORTE_LECTURA = 0.55


def textos_del_dataset() -> set[str]:
    vistos = set()
    with DATOS.open(encoding="utf-8") as handle:
        for linea in handle:
            linea = linea.strip()
            if not linea:
                continue
            fila = json.loads(linea)
            texto = fila.get("text")
            if isinstance(texto, str):
                vistos.add(texto.casefold().strip())
    return vistos


def main() -> None:
    if not MODELO.is_file():
        raise SystemExit(f"No está el modelo: {MODELO}")
    pipeline = joblib.load(MODELO)
    paquete = json.loads(CASOS.read_text(encoding="utf-8"))
    casos = paquete["casos"]
    conocidos = textos_del_dataset()
    repetidos = [
        caso["id"]
        for caso in casos
        if caso["text"].casefold().strip() in conocidos
    ]
    if repetidos:
        raise SystemExit("Estas consultas ya están en el dataset: " + ", ".join(repetidos))

    clases = list(pipeline.named_steps["clf"].classes_)
    textos = [caso["text"] for caso in casos]
    predichas = pipeline.predict(textos)
    probas = pipeline.predict_proba(textos)

    filas = []
    for caso, predicha, proba in zip(casos, predichas, probas):
        orden = sorted(
            ((clases[i], float(proba[i])) for i in range(len(clases))),
            key=lambda item: item[1],
            reverse=True,
        )
        primera, puntaje = orden[0]
        segunda, puntaje_2 = orden[1]
        lecturas = caso.get("lecturas") or ([caso["esperada"]] if caso.get("esperada") else [])
        if caso["tipo"] == "sin_categoria_tematica":
            coincide = False
            lectura = "El modelo igual asignó una de las ocho. No puede devolver sin categoría."
        elif caso["tipo"] == "frontera":
            coincide = predicha in lecturas
            lectura = "Coincide con una de las dos lecturas." if coincide else "No coincide con ninguna de las dos lecturas."
        else:
            coincide = predicha == caso["esperada"]
            lectura = "Coincide con la categoría esperada." if coincide else "No coincide con la categoría esperada."
        filas.append(
            {
                "id": caso["id"],
                "tipo": caso["tipo"],
                "text": caso["text"],
                "esperada": caso.get("esperada"),
                "lecturas": lecturas,
                "predicha": predicha,
                "puntuacion": round(puntaje, 4),
                "segunda": segunda,
                "puntuacion_segunda": round(puntaje_2, 4),
                "margen": round(puntaje - puntaje_2, 4),
                "coincide": coincide,
                "baja_confianza_de_lectura": puntaje < CORTE_LECTURA,
                "lectura": lectura,
            }
        )

    claras = [fila for fila in filas if fila["tipo"] == "clara"]
    aciertos = sum(1 for fila in claras if fila["coincide"])
    confusiones = [fila for fila in claras if not fila["coincide"]]
    bajas = [fila for fila in filas if fila["baja_confianza_de_lectura"]]
    resultado = {
        "caracter": "prueba ilustrativa de inferencia",
        "evaluacion_formal": False,
        "dataset_aprobado": False,
        "modelo": MODELO.name,
        "modelo_reentrenado": False,
        "corte_de_lectura": CORTE_LECTURA,
        "nota_puntuacion": "La puntuación es el máximo de predict_proba. No es una probabilidad calibrada ni un umbral de abstención.",
        "claras": len(claras),
        "aciertos_en_claras": aciertos,
        "filas": filas,
    }
    (AQUI / "resultados_inferencia.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lineas = [
        "# Prueba ilustrativa de inferencia — HU-07",
        "",
        "Esta prueba no evalúa el rendimiento del modelo. Las consultas son nuevas y sintéticas. El modelo no se volvió a entrenar y no entra al PMV1, al RAG ni a producción.",
        "",
        f"Puntuación: máximo de `predict_proba`. Por debajo de {CORTE_LECTURA:.2f} se marca solo para leer esta prueba. Ese corte no se eligió con validación.",
        "",
        f"Consultas claras: {len(claras)}. Coincidencias con la categoría esperada: {aciertos}.",
        "",
        "| Id | Esperada | Predicha | Puntuación | Segunda | Margen | Lectura |",
        "| --- | --- | --- | ---: | --- | ---: | --- |",
    ]
    for fila in filas:
        esperada = fila["esperada"] or "ninguna de las ocho"
        marca = ""
        if fila["baja_confianza_de_lectura"]:
            marca = " Baja puntuación."
        if fila["tipo"] == "clara" and not fila["coincide"]:
            marca += " Confusión."
        lineas.append(
            f"| {fila['id']} | {esperada} | {fila['predicha']} | {fila['puntuacion']:.4f} | {fila['segunda']} | {fila['margen']:.4f} | {fila['lectura']}{marca} |"
        )
    lineas.extend(["", "## Consultas", ""])
    for fila in filas:
        lineas.append(f"- **{fila['id']}** ({fila['tipo']}): {fila['text']}")
    lineas.extend(["", "## Confusiones en las consultas claras", ""])
    if confusiones:
        for fila in confusiones:
            lineas.append(
                f"- `{fila['id']}`: se esperaba {fila['esperada']} y el modelo respondió {fila['predicha']} ({fila['puntuacion']:.4f}), con {fila['segunda']} en segundo lugar."
            )
    else:
        lineas.append("- Ninguna de las dieciséis consultas claras cayó en otra categoría.")
    lineas.extend(["", "## Puntuación baja en esta lectura", ""])
    if bajas:
        for fila in bajas:
            lineas.append(
                f"- `{fila['id']}`: {fila['predicha']} con {fila['puntuacion']:.4f}. Segunda opción: {fila['segunda']} ({fila['puntuacion_segunda']:.4f})."
            )
    else:
        lineas.append(f"- Ninguna consulta quedó bajo {CORTE_LECTURA:.2f}.")
    lineas.extend(
        [
            "",
            "## Límite",
            "",
            "El pipeline siempre devuelve una de las ocho categorías. La consulta del banco no tiene categoría temática y aun así recibió una predicción. Estas coincidencias no aprueban el dataset ni sustituyen una evaluación con consultas reales.",
            "",
        ]
    )
    (AQUI / "informe_inferencia.md").write_text("\n".join(lineas), encoding="utf-8")
    print(
        json.dumps(
            {
                "claras": len(claras),
                "aciertos_en_claras": aciertos,
                "confusiones": [fila["id"] for fila in confusiones],
                "baja_puntuacion": [fila["id"] for fila in bajas],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
