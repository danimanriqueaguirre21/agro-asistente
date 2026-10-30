"""Genera el dataset sintético de HU-08 y sus particiones.

Las etiquetas salen de reglas de simulación. No son observaciones de predios
ni umbrales agronómicos. No lee MySQL, SENAMHI ni los archivos de HU-07.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

SEMILLA = 42
VERSION_REGLAS = "sintetica-hu08-v1"
ORIGEN = "sintetico_ejercicio_academico"
POR_CELDA = 80
FRACCION_PRUEBA = 0.2
CULTIVOS = ("papa", "maíz", "quinua", "haba", "cebada")
REGIONES = ("Huancayo", "Jauja", "Concepción", "Chupaca", "Tarma", "Junín")
ETAPAS = (
    "siembra",
    "emergencia",
    "desarrollo_vegetativo",
    "floracion",
    "llenado",
    "maduracion",
)
FAMILIAS = ("meteorologico", "plaga_enfermedad", "suelo_agua_manejo")
NIVELES = ("bajo", "medio", "alto")
SUELOS = ("seco", "adecuado", "encharcado")
VARIABLES = (
    "familia_escenario",
    "cultivo",
    "region",
    "etapa_fenologica",
    "temperatura_c",
    "precipitacion_mm",
    "dias_sin_lluvia",
    "sintoma_observado",
    "proporcion_afectada",
    "condicion_suelo",
)
AQUI = Path(__file__).resolve().parent


def puntos_meteorologico(temperatura: float | None, precipitacion: float | None, etapa: str) -> int:
    puntaje = 0
    aplico_frio = False
    if temperatura is not None and temperatura <= 4 and etapa in ("emergencia", "floracion"):
        puntaje += 2
        aplico_frio = True
    elif temperatura is not None and temperatura <= 7 and etapa in ("emergencia", "floracion", "llenado"):
        puntaje += 1
        aplico_frio = True
    if not aplico_frio and temperatura is not None and temperatura >= 25 and etapa == "floracion":
        puntaje += 1
    if precipitacion is not None and precipitacion >= 40 and etapa in ("emergencia", "floracion", "llenado"):
        puntaje += 2
    elif precipitacion is not None and precipitacion >= 22:
        puntaje += 1
    return puntaje


def puntos_plaga(sintoma: bool, proporcion: float, etapa: str) -> int:
    if not sintoma:
        return 0
    puntaje = 0
    if proporcion >= 0.55:
        puntaje += 2
    if proporcion >= 0.35 and etapa in ("emergencia", "floracion"):
        puntaje += 2
    elif proporcion >= 0.25 and etapa == "llenado":
        puntaje += 1
    return puntaje


def puntos_suelo(
    condicion: str,
    dias_sin_lluvia: int,
    precipitacion: float | None,
    etapa: str,
) -> int:
    puntaje = 0
    if condicion == "encharcado" and precipitacion is not None and precipitacion >= 28:
        puntaje += 2
    elif condicion == "encharcado":
        puntaje += 1
    if condicion == "seco" and dias_sin_lluvia >= 15:
        puntaje += 2
    elif condicion == "seco" and 8 <= dias_sin_lluvia <= 14:
        puntaje += 1
    if condicion != "adecuado" and etapa in ("emergencia", "floracion"):
        puntaje += 2
    elif condicion != "adecuado" and etapa == "llenado":
        puntaje += 1
    return puntaje


def a_nivel(puntaje: int) -> str:
    if puntaje <= 1:
        return "bajo"
    if puntaje <= 3:
        return "medio"
    return "alto"


def _temperatura(rng: random.Random) -> float | None:
    sorteo = rng.random()
    if sorteo < 0.15:
        return None
    if sorteo < 0.40:
        return round(rng.uniform(-1.5, 4.0), 1)
    if sorteo < 0.55:
        return round(rng.uniform(4.1, 7.0), 1)
    if sorteo < 0.70:
        return round(rng.uniform(25.0, 30.0), 1)
    return round(rng.uniform(8.0, 22.0), 1)


def _precipitacion(rng: random.Random) -> float | None:
    sorteo = rng.random()
    if sorteo < 0.15:
        return None
    if sorteo < 0.45:
        return round(rng.uniform(40.0, 75.0), 1)
    if sorteo < 0.65:
        return round(rng.uniform(22.0, 39.9), 1)
    return round(rng.uniform(0.0, 21.9), 1)


def _dias(rng: random.Random) -> int:
    sorteo = rng.random()
    if sorteo < 0.35:
        return rng.randint(15, 28)
    if sorteo < 0.60:
        return rng.randint(8, 14)
    return rng.randint(0, 7)


def _sintoma_y_proporcion(rng: random.Random) -> tuple[bool, float]:
    if rng.random() >= 0.62:
        return False, 0.0
    sorteo = rng.random()
    if sorteo < 0.30:
        return True, round(rng.uniform(0.05, 0.24), 2)
    if sorteo < 0.60:
        return True, round(rng.uniform(0.25, 0.54), 2)
    return True, round(rng.uniform(0.55, 0.90), 2)


def _condicion(rng: random.Random) -> str:
    return rng.choices(SUELOS, weights=(0.38, 0.24, 0.38), k=1)[0]


def nuevo_escenario(rng: random.Random, familia: str) -> dict[str, object]:
    sintoma, proporcion = _sintoma_y_proporcion(rng)
    fila = {
        "familia_escenario": familia,
        "cultivo": rng.choice(CULTIVOS),
        "region": rng.choice(REGIONES),
        "etapa_fenologica": rng.choice(ETAPAS),
        "temperatura_c": _temperatura(rng),
        "precipitacion_mm": _precipitacion(rng),
        "dias_sin_lluvia": _dias(rng),
        "sintoma_observado": sintoma,
        "proporcion_afectada": proporcion,
        "condicion_suelo": _condicion(rng),
    }
    fila["nivel_riesgo"] = a_nivel(_puntaje(fila))
    return fila


def _puntaje(fila: dict[str, object]) -> int:
    familia = str(fila["familia_escenario"])
    etapa = str(fila["etapa_fenologica"])
    if familia == "meteorologico":
        return puntos_meteorologico(fila["temperatura_c"], fila["precipitacion_mm"], etapa)  # type: ignore[arg-type]
    if familia == "plaga_enfermedad":
        return puntos_plaga(bool(fila["sintoma_observado"]), float(fila["proporcion_afectada"]), etapa)
    if familia == "suelo_agua_manejo":
        return puntos_suelo(
            str(fila["condicion_suelo"]),
            int(fila["dias_sin_lluvia"]),
            fila["precipitacion_mm"],  # type: ignore[arg-type]
            etapa,
        )
    raise ValueError(familia)


def clave_variables(fila: dict[str, object]) -> tuple[object, ...]:
    return tuple(fila[nombre] for nombre in VARIABLES)


def construir_muestra(rng: random.Random) -> list[dict[str, object]]:
    celdas: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    vistos: set[tuple[object, ...]] = set()
    intentos = 0
    while intentos < 60000:
        intentos += 1
        if all(len(celdas[(familia, nivel)]) >= POR_CELDA for familia in FAMILIAS for nivel in NIVELES):
            break
        familia = FAMILIAS[(intentos - 1) % len(FAMILIAS)]
        fila = nuevo_escenario(rng, familia)
        clave = clave_variables(fila)
        if clave in vistos:
            continue
        cubeta = celdas[(familia, str(fila["nivel_riesgo"]))]
        if len(cubeta) >= POR_CELDA:
            continue
        vistos.add(clave)
        cubeta.append(fila)
    faltantes = [
        f"{familia}/{nivel}:{len(celdas[(familia, nivel)])}"
        for familia in FAMILIAS
        for nivel in NIVELES
        if len(celdas[(familia, nivel)]) < POR_CELDA
    ]
    if faltantes:
        raise SystemExit("No se llenaron las celdas: " + ", ".join(faltantes))
    muestra: list[dict[str, object]] = []
    for familia in FAMILIAS:
        for nivel in NIVELES:
            muestra.extend(celdas[(familia, nivel)])
    return muestra


def identificar(filas: list[dict[str, object]]) -> None:
    ordenadas = sorted(filas, key=lambda fila: json.dumps(clave_variables(fila), ensure_ascii=False))
    filas[:] = ordenadas
    for indice, fila in enumerate(filas, start=1):
        fila["id"] = f"hu08-sint-{indice:04d}"
        fila["origen"] = ORIGEN
        fila["es_observacion_real"] = False
        fila["version_reglas"] = VERSION_REGLAS


def partir(rng: random.Random, filas: list[dict[str, object]]) -> tuple[list[str], list[str]]:
    grupos: dict[tuple[str, str], list[str]] = defaultdict(list)
    for fila in filas:
        grupos[(str(fila["familia_escenario"]), str(fila["nivel_riesgo"]))].append(str(fila["id"]))
    entrenamiento: list[str] = []
    prueba: list[str] = []
    for familia in FAMILIAS:
        for nivel in NIVELES:
            identificadores = grupos[(familia, nivel)][:]
            rng.shuffle(identificadores)
            corte = int(round(len(identificadores) * FRACCION_PRUEBA))
            prueba.extend(identificadores[:corte])
            entrenamiento.extend(identificadores[corte:])
    entrenamiento.sort()
    prueba.sort()
    return entrenamiento, prueba


def exactitud_de_un_rasgo(filas: list[dict[str, object]], rasgo: str) -> float:
    valores = [fila[rasgo] for fila in filas]
    if rasgo in ("temperatura_c", "precipitacion_mm", "dias_sin_lluvia", "proporcion_afectada"):
        presentes = sorted(float(valor) for valor in valores if valor is not None)
        if not presentes:
            cortes: list[float] = []
        else:
            cortes = [presentes[int(len(presentes) * fraccion)] for fraccion in (0.25, 0.5, 0.75)]

        def grupo(valor: object) -> str:
            if valor is None:
                return "nulo"
            numero = float(valor)
            if numero <= cortes[0]:
                return "q1"
            if numero <= cortes[1]:
                return "q2"
            if numero <= cortes[2]:
                return "q3"
            return "q4"
    else:
        def grupo(valor: object) -> str:
            return str(valor)

    cubetas: dict[str, list[str]] = defaultdict(list)
    for fila in filas:
        cubetas[grupo(fila[rasgo])].append(str(fila["nivel_riesgo"]))
    aciertos = 0
    for etiquetas in cubetas.values():
        moda = Counter(etiquetas).most_common(1)[0][0]
        aciertos += sum(1 for etiqueta in etiquetas if etiqueta == moda)
    return aciertos / len(filas)


def escribir_jsonl(ruta: Path, filas: list[dict[str, object]]) -> None:
    lineas = [
        json.dumps(fila, ensure_ascii=False, sort_keys=True)
        for fila in filas
    ]
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def fila_publica(fila: dict[str, object]) -> dict[str, object]:
    orden = (
        "id",
        "origen",
        "es_observacion_real",
        "version_reglas",
        *VARIABLES,
        "nivel_riesgo",
    )
    return {clave: fila[clave] for clave in orden}


def distribuir(filas: list[dict[str, object]]) -> dict[str, int]:
    return {nivel: sum(1 for fila in filas if fila["nivel_riesgo"] == nivel) for nivel in NIVELES}


def main() -> None:
    rng = random.Random(SEMILLA)
    filas = construir_muestra(rng)
    identificar(filas)
    entrenamiento, prueba = partir(rng, filas)
    por_id = {str(fila["id"]): fila for fila in filas}
    filas_entrenamiento = [fila_publica(por_id[identificador]) for identificador in entrenamiento]
    filas_prueba = [fila_publica(por_id[identificador]) for identificador in prueba]
    filas_publicas = [fila_publica(fila) for fila in filas]

    ruta_dataset = AQUI / "dataset_hu08_sintetico.jsonl"
    escribir_jsonl(ruta_dataset, filas_publicas)
    escribir_jsonl(AQUI / "entrenamiento.jsonl", filas_entrenamiento)
    escribir_jsonl(AQUI / "prueba.jsonl", filas_prueba)

    solape = sorted(set(entrenamiento) & set(prueba))
    if solape:
        raise SystemExit("Hay identificadores en las dos particiones.")
    if sorted(entrenamiento + prueba) != sorted(por_id):
        raise SystemExit("Las particiones no cubren el dataset.")

    repetidos = len(filas) - len({clave_variables(fila) for fila in filas})
    if repetidos:
        raise SystemExit(f"Hay {repetidos} registros duplicados en las variables.")
    for fila in filas:
        proporcion = float(fila["proporcion_afectada"])
        if not 0 <= proporcion <= 1:
            raise SystemExit("proporcion_afectada fuera de rango.")
        if not fila["sintoma_observado"] and proporcion != 0:
            raise SystemExit("Hay proporción sin síntoma.")
        if fila["nivel_riesgo"] not in NIVELES or fila["es_observacion_real"] is not False:
            raise SystemExit("Etiqueta o marca de origen inválida.")

    nulos = {
        nombre: sum(1 for fila in filas if fila[nombre] is None)
        for nombre in VARIABLES
    }
    rasgos = {nombre: round(exactitud_de_un_rasgo(filas, nombre), 4) for nombre in VARIABLES}
    peor = max(rasgos.values())
    if peor >= 0.8:
        raise SystemExit(f"Una sola variable predice demasiado la etiqueta: {peor}")

    resumen = hashlib.sha256(ruta_dataset.read_bytes()).hexdigest()
    controles = {
        "semilla": SEMILLA,
        "version_reglas": VERSION_REGLAS,
        "registros": len(filas),
        "por_familia_y_nivel": POR_CELDA,
        "distribucion": distribuir(filas),
        "distribucion_entrenamiento": distribuir(filas_entrenamiento),
        "distribucion_prueba": distribuir(filas_prueba),
        "entrenamiento": len(entrenamiento),
        "prueba": len(prueba),
        "solape_particiones": len(solape),
        "duplicados_de_variables": repetidos,
        "nulos": nulos,
        "exactitud_maxima_de_una_variable": rasgos,
        "sha256_dataset": resumen,
        "es_observacion_real": False,
        "etiqueta": "supuesto_de_simulacion",
    }
    (AQUI / "controles.json").write_text(
        json.dumps(controles, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (AQUI / "ids_particiones.json").write_text(
        json.dumps(
            {
                "semilla": SEMILLA,
                "fraccion_prueba": FRACCION_PRUEBA,
                "estratificacion": "familia_escenario y nivel_riesgo",
                "entrenamiento": entrenamiento,
                "prueba": prueba,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    escribir_resumen(controles)
    escribir_informe(controles, filas)
    print(json.dumps({"registros": len(filas), "sha256": resumen, "rasgos": rasgos}, ensure_ascii=False))


def escribir_resumen(controles: dict[str, object]) -> None:
    distribucion = controles["distribucion"]
    entrenamiento = controles["distribucion_entrenamiento"]
    prueba = controles["distribucion_prueba"]
    assert isinstance(distribucion, dict)
    assert isinstance(entrenamiento, dict)
    assert isinstance(prueba, dict)
    lineas = [
        "# Distribución del dataset sintético HU-08",
        "",
        "Ejercicio académico. Las etiquetas son supuestos de simulación, no riesgo agrícola observado.",
        "",
        f"- Semilla: {controles['semilla']}.",
        f"- Reglas: `{controles['version_reglas']}`.",
        f"- Registros: {controles['registros']}.",
        f"- Entrenamiento: {controles['entrenamiento']}. Prueba: {controles['prueba']}.",
        f"- SHA-256 de `dataset_hu08_sintetico.jsonl`: `{controles['sha256_dataset']}`.",
        "",
        "Cada familia aporta 80 registros a cada nivel. El total de cada nivel es 240.",
        "",
        "| Nivel | Total | Entrenamiento | Prueba |",
        "|---|---:|---:|---:|",
    ]
    for nivel in NIVELES:
        lineas.append(
            f"| {nivel} | {distribucion[nivel]} | {entrenamiento[nivel]} | {prueba[nivel]} |"
        )
    lineas.extend(
        [
            "",
            "La partición es estratificada por familia y nivel, con fracción de prueba 0,2.",
            "Los identificadores están en `ids_particiones.json`.",
            "El entrenamiento posterior debe leer `entrenamiento.jsonl` y evaluar en `prueba.jsonl`.",
            "",
        ]
    )
    (AQUI / "resumen_distribucion.md").write_text("\n".join(lineas), encoding="utf-8")


def escribir_informe(controles: dict[str, object], filas: list[dict[str, object]]) -> None:
    nulos = controles["nulos"]
    rasgos = controles["exactitud_maxima_de_una_variable"]
    assert isinstance(nulos, dict)
    assert isinstance(rasgos, dict)
    cultivos = Counter(str(fila["cultivo"]) for fila in filas)
    regiones = Counter(str(fila["region"]) for fila in filas)
    etapas = Counter(str(fila["etapa_fenologica"]) for fila in filas)
    lineas = [
        "# Controles de calidad del dataset sintético HU-08",
        "",
        "Este conjunto es un ejercicio académico de clasificación. Todos los registros tienen `es_observacion_real` en false y `origen` en `sintetico_ejercicio_academico`. No salen de MySQL, de SENAMHI ni de HU-07.",
        "",
        "Las etiquetas `bajo`, `medio` y `alto` las asignan las reglas de `reglas_etiquetado_sintetico.md`. Son supuestos de simulación. No son umbrales agronómicos validados ni riesgo observado en un predio.",
        "",
        "## Controles",
        "",
        f"- Semilla del generador y de la partición: {controles['semilla']}.",
        f"- Registros: {controles['registros']}. Duplicados en las variables de clasificación: {controles['duplicados_de_variables']}.",
        f"- Solape entre entrenamiento y prueba: {controles['solape_particiones']}.",
        f"- SHA-256: `{controles['sha256_dataset']}`.",
        "",
        "| Variable | Valores nulos | Exactitud de la mejor constante por grupo |",
        "|---|---:|---:|",
    ]
    for nombre in VARIABLES:
        lineas.append(f"| {nombre} | {nulos[nombre]} | {rasgos[nombre]} |")
    lineas.extend(
        [
            "",
            "La exactitud de una sola variable es la de predecir, en cada grupo de esa variable, la etiqueta más frecuente del grupo. En temperatura, precipitación, días sin lluvia y proporción, los grupos son cuartiles más el grupo nulo. Ninguna variable llega a 0,80. La etiqueta no sale de un umbral sobre una sola columna.",
            "",
            "Los nulos están solo en `temperatura_c` y `precipitacion_mm`. El resto de las variables está completo. Un nulo suma cero en la regla y no se sustituye por un número.",
            "",
            "## Variedad",
            "",
            "Cultivos: " + ", ".join(f"{nombre} {cantidad}" for nombre, cantidad in sorted(cultivos.items())) + ".",
            "",
            "Regiones de texto: " + ", ".join(f"{nombre} {cantidad}" for nombre, cantidad in sorted(regiones.items())) + ".",
            "",
            "Etapas: " + ", ".join(f"{nombre} {cantidad}" for nombre, cantidad in sorted(etapas.items())) + ".",
            "",
            "`cultivo` y `region` no entran en la fórmula. Están para que el ejercicio no use un único cultivo ni un único lugar. Los nombres de región no son mediciones hechas en esos distritos.",
            "",
            "## Limitaciones",
            "",
            "- La etapa es la variable suelta que más se acerca a la etiqueta "
            f"(exactitud {rasgos['etapa_fenologica']}) porque varias reglas piden `emergencia` o `floracion` para llegar a `alto`. "
            "No la determina: esas etapas también aparecen en `bajo` y `medio`. Por eso el muestreo deja más filas en esas dos etapas.",
            "- `cultivo` y `region` no cambian la etiqueta. Un modelo que se apoye en ellos estará usando variación que esta simulación no relaciona con el nivel.",
            "- No hay observaciones reales ni etiquetas de daño en campo.",
            "- Las unidades Celsius y mm las define la simulación. No fueron leídas del adaptador SENAMHI.",
            "- La etapa pertenece a un vocabulario de ejercicio, no a un calendario validado.",
            "- El síntoma simulado no es un diagnóstico.",
            "- El dataset no debe integrarse al backend ni usarse para aconsejar a un agricultor.",
            "- No se entrenó un modelo en esta generación.",
            "",
        ]
    )
    (AQUI / "informe_controles_calidad.md").write_text("\n".join(lineas), encoding="utf-8")


if __name__ == "__main__":
    main()
