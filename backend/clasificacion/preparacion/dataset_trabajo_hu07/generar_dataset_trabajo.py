# -*- coding: utf-8 -*-
"""Arma el dataset de trabajo HU-07 y comprueba duplicados.

No entrena, no aprueba y no escribe fuera de esta carpeta.
Los bancos de textos viven en bancos/*.txt: una consulta por línea.
Una línea puede llevar un tabulador y, después, una observación de frontera.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AQUI = Path(__file__).resolve().parent
BANCOS = AQUI / "bancos"

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
META_POR_CLASE = 200
CULTIVOS = [
    "maíz amarillo duro",
    "maíz amiláceo",
    "maíz choclo",
    "granadilla",
    "mandarina",
    "zanahoria",
    "cebada",
    "quinua",
    "arveja",
    "frijol",
    "papaya",
    "plátano",
    "cacao",
    "café",
    "olluco",
    "palta",
    "piña",
    "trigo",
    "yuca",
    "haba",
    "kion",
    "maca",
    "naranja",
    "papa",
    "tangelo",
]
PROVINCIAS = [
    "Chanchamayo",
    "Concepción",
    "Huancayo",
    "Chupaca",
    "Satipo",
    "Tarma",
    "Jauja",
    "Yauli",
    "Junín",
]
LEMA = {
    "riego": r"\b(riego|riegos|regar|regando|regué|riegue|riega)\b",
    "fertilizacion_nutricion": r"\b(abono|abonar|abona|fertilizante|fertilizar|nutriente|nutrientes|compost|urea|guano)\b",
    "plagas": r"\b(plaga|plagas|insecto|insectos|pulgón|pulgones|gusano|gusanos|ácaro|ácaros)\b",
    "enfermedades_cultivos": r"\b(enfermedad|enfermedades|hongo|hongos|roya|mildiu|mancha|manchas)\b",
    "siembra_manejo_cultivo": r"\b(siembra|sembrar|sembré|siembro|aporque|aporcar|maleza|malezas)\b",
    "clima_heladas": r"\b(helada|heladas|granizo|clima|sequía|viento)\b",
    "suelos": r"\b(suelo|suelos|terreno|erosión|drenaje|compactado)\b",
    "cosecha_poscosecha": r"\b(cosecha|cosechar|cosecho|secado|almacén|almacenar|oreo)\b",
}
FRASES_PRUEBA_BACKEND = [
    "¿Cómo riego la papa en floración?",
    "¿Cómo riego la papa en floración para evitar encharcamiento?",
    "¿Cómo riego la papa?",
    "¿Cómo riego?",
    "¿Qué hago?",
    "¿Qué puedo hacer para mejorar el cultivo de papa?",
]


def norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"^[^\wáéíóúüñ]+|[^\wáéíóúüñ]+$", "", text, flags=re.UNICODE)
    return text


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-záéíóúüñ0-9]+", norm(text), flags=re.UNICODE))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def esqueleto(text: str) -> str:
    salida = norm(text)
    for nombre in CULTIVOS + PROVINCIAS:
        salida = re.sub(rf"\b{re.escape(nombre.lower())}\b", " ", salida)
    salida = re.sub(r"\s+", " ", salida).strip()
    return salida


def palabras(text: str) -> int:
    return len(re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+", text))


def id_de(text: str) -> str:
    digest = hashlib.sha256(unicodedata.normalize("NFC", text).encode("utf-8")).hexdigest()
    return "trabajo-hu07-" + digest[:10]


def cultivo_de(text: str) -> str | None:
    hallados = [c for c in CULTIVOS if re.search(rf"\b{re.escape(c)}\b", text, flags=re.IGNORECASE)]
    if len(hallados) == 1:
        return hallados[0]
    return None


def region_de(text: str) -> str | None:
    hallados = [p for p in PROVINCIAS if re.search(rf"\b{re.escape(p)}\b", text)]
    if len(hallados) == 1:
        return hallados[0]
    return None


def leer_banco(categoria: str) -> list[dict]:
    ruta = BANCOS / f"{categoria}.txt"
    filas = []
    for n, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), start=1):
        if not linea.strip():
            continue
        if "\t" in linea:
            texto, obs = linea.split("\t", 1)
        else:
            texto, obs = linea, ""
        filas.append({"text": texto.strip(), "observations": obs.strip(), "linea": n})
    return filas


def leer_jsonl_textos(ruta: Path, campo: str) -> list[tuple[str, str]]:
    if not ruta.exists():
        return []
    salida = []
    for line in ruta.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        texto = obj.get(campo)
        if isinstance(texto, str) and texto.strip():
            salida.append((ruta.name, texto))
    return salida


def cargar_externos() -> tuple[list[tuple[str, str]], list[str]]:
    notas = []
    pares: list[tuple[str, str]] = []
    ilustr = json.loads(
        (ROOT / "backend/clasificacion/muestras/muestra_ilustrativa_v1.json").read_text(encoding="utf-8")
    )
    for item in ilustr["items"]:
        pares.append((f"ilustrativo:{item['id']}", item["text"]))
    pares += leer_jsonl_textos(
        ROOT / "backend/clasificacion/experimentos/hu07_preliminar/dataset_hu07_preliminar_revision.jsonl",
        "text",
    )
    pares += leer_jsonl_textos(ROOT / "piloto_hu07_v2/aceptadas_v2.jsonl", "text")
    pares += leer_jsonl_textos(ROOT / "piloto_hu07_v2/rechazadas_v2.jsonl", "text")
    baseline = json.loads((ROOT / "backend/evaluation/data/pmv1_baseline.json").read_text(encoding="utf-8"))
    for item in baseline["items"]:
        pares.append((f"ragas:{item['id']}", item["question"]))
    for md in (ROOT / "knowledge").glob("*.md"):
        for n, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            if len(line.strip()) >= 25:
                pares.append((f"knowledge:{md.name}:{n}", line.strip()))
    for frase in FRASES_PRUEBA_BACKEND:
        pares.append(("prueba-backend", frase))
    candidatos_800 = [
        p
        for p in ROOT.glob("**/*800*")
        if ".venv" not in p.parts
        and ".git" not in p.parts
        and p.suffix.lower() in {".json", ".jsonl", ".txt", ".md"}
    ]
    if not candidatos_800:
        notas.append(
            "No aparece en el repositorio un archivo con las 800 consultas sintéticas anteriores. "
            "El cruce contra ese conjunto no se pudo ejecutar. "
            "Los nombres que contienen 800 en el entorno virtual o en objetos de git no son ese conjunto."
        )
    return pares, notas


def pares_similares(filas: list[dict], umbral_j: float, umbral_s: float, tope: int = 30):
    toks = [(i, tokens(f["text"]), norm(f["text"])) for i, f in enumerate(filas)]
    hallados = []
    cercano = {"jaccard": 0.0, "sequence": 0.0, "a": "", "b": ""}
    for a in range(len(toks)):
        for b in range(a + 1, len(toks)):
            jac = jaccard(toks[a][1], toks[b][1])
            ratio = SequenceMatcher(None, toks[a][2], toks[b][2]).ratio() if jac >= 0.30 else 0.0
            if jac > cercano["jaccard"]:
                cercano = {
                    "jaccard": round(jac, 3),
                    "sequence": round(ratio, 3),
                    "a": filas[toks[a][0]]["id"],
                    "b": filas[toks[b][0]]["id"],
                }
            if jac >= umbral_j or ratio >= umbral_s:
                hallados.append(
                    {
                        "a": filas[toks[a][0]]["id"],
                        "b": filas[toks[b][0]]["id"],
                        "jaccard": round(jac, 3),
                        "sequence": round(ratio, 3),
                    }
                )
                if len(hallados) >= tope:
                    return hallados, cercano
    return hallados, cercano


def cruces(filas: list[dict], externos: list[tuple[str, str]], tope: int = 40):
    ext = [(nombre, tokens(texto), norm(texto)) for nombre, texto in externos]
    hallados = []
    for fila in filas:
        ft, fn = tokens(fila["text"]), norm(fila["text"])
        for nombre, et, en in ext:
            jac = jaccard(ft, et)
            ratio = SequenceMatcher(None, fn, en).ratio() if jac >= 0.35 else 0.0
            if jac >= 0.55 or ratio >= 0.80:
                hallados.append(
                    {
                        "id": fila["id"],
                        "fuente": nombre,
                        "jaccard": round(jac, 3),
                        "sequence": round(ratio, 3),
                    }
                )
                if len(hallados) >= tope:
                    return hallados
    return hallados


def leer_aux(nombre: str) -> list[dict]:
    ruta = BANCOS / nombre
    return [json.loads(line) for line in ruta.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    errores: list[str] = []
    registros = []
    for categoria in CATEGORIAS:
        banco = leer_banco(categoria)
        if len(banco) != META_POR_CLASE:
            errores.append(f"{categoria}: {len(banco)} líneas, se esperaban {META_POR_CLASE}")
        for fila in banco:
            fila["proposed_category"] = categoria
            fila["id"] = id_de(fila["text"])
            registros.append(fila)

    ids = [r["id"] for r in registros]
    if len(ids) != len(set(ids)):
        errores.append("hay identificadores repetidos")
    normas = [norm(r["text"]) for r in registros]
    if len(normas) != len(set(normas)):
        errores.append("hay textos duplicados tras normalizar")
    esqueletos = [esqueleto(r["text"]) for r in registros]
    repetidos = [k for k, v in Counter(esqueletos).items() if v > 1]
    if repetidos:
        errores.append(f"esqueletos repetidos al enmascarar cultivo y provincia: {len(repetidos)}")

    internos, par_cercano = pares_similares(registros, 0.60, 0.84)
    if internos:
        errores.append(f"pares internos sobre el umbral: {len(internos)}")

    externos, notas_fuente = cargar_externos()
    externos_hallados = cruces(registros, externos)
    if externos_hallados:
        errores.append(f"cruces con fuentes excluidas: {len(externos_hallados)}")

    if errores:
        reporte = {"errores": errores, "muestra_internos": internos[:10], "muestra_cruces": externos_hallados[:10]}
        (AQUI / "controles_fallidos.json").write_text(
            json.dumps(reporte, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        raise SystemExit("La generación no pasó los controles. Ver controles_fallidos.json")

    oficiales = []
    for r in registros:
        oficiales.append(
            {
                "id": r["id"],
                "text": r["text"],
                "proposed_category": r["proposed_category"],
                "origin": "sintetico_preparacion",
                "review_status": "pendiente_revision_humana",
                "observations": r["observations"],
                "is_real_query": False,
                "crop": cultivo_de(r["text"]),
                "region": region_de(r["text"]),
            }
        )

    ambiguas = []
    for bruto in leer_aux("cola_ambigua.jsonl"):
        ambiguas.append(
            {
                "id": "ambigua-" + hashlib.sha256(bruto["text"].encode("utf-8")).hexdigest()[:10],
                "text": bruto["text"],
                "candidate_categories": bruto["candidate_categories"],
                "reason": bruto["reason"],
                "status": "pendiente",
                "resolved_category": "",
                "origin": "sintetico_preparacion",
                "review_status": "pendiente_revision_humana",
                "observations": bruto.get("observations", ""),
                "is_real_query": False,
            }
        )
    fuera = []
    for bruto in leer_aux("fuera_de_alcance.jsonl"):
        fuera.append(
            {
                "id": "fuera-" + hashlib.sha256(bruto["text"].encode("utf-8")).hexdigest()[:10],
                "text": bruto["text"],
                "disposition": "fuera_de_alcance",
                "reason": bruto["reason"],
                "proposed_category": None,
                "origin": "sintetico_preparacion",
                "review_status": "pendiente_revision_humana",
                "observations": bruto.get("observations", ""),
                "is_real_query": False,
            }
        )

    ruta_jsonl = AQUI / "consultas_trabajo.jsonl"
    ruta_jsonl.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in oficiales) + "\n",
        encoding="utf-8",
    )
    (AQUI / "cola_ambigua.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in ambiguas) + "\n",
        encoding="utf-8",
    )
    (AQUI / "fuera_de_alcance.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in fuera) + "\n",
        encoding="utf-8",
    )

    conteo = Counter(r["proposed_category"] for r in oficiales)
    longitudes = {c: {"menos_de_12": 0, "de_12_a_30": 0, "mas_de_30": 0} for c in CATEGORIAS}
    lemas = {c: 0 for c in CATEGORIAS}
    con_cultivo = 0
    con_region = 0
    con_observacion = 0
    for r in oficiales:
        n = palabras(r["text"])
        cubo = "menos_de_12" if n < 12 else "mas_de_30" if n > 30 else "de_12_a_30"
        longitudes[r["proposed_category"]][cubo] += 1
        if re.search(LEMA[r["proposed_category"]], r["text"].lower()):
            lemas[r["proposed_category"]] += 1
        if r["crop"]:
            con_cultivo += 1
        if r["region"]:
            con_region += 1
        if r["observations"]:
            con_observacion += 1

    controles = {
        "registros": len(oficiales),
        "distribucion": dict(conteo),
        "duplicados_exactos_normalizados": 0,
        "esqueletos_repetidos": 0,
        "pares_internos_sobre_umbral": 0,
        "par_mas_cercano_bajo_el_umbral": par_cercano,
        "cruces_fuentes_excluidas": 0,
        "fuentes_externas_comparadas": len(externos),
        "notas_de_cruce": notas_fuente,
        "umbral_interno": "Jaccard de tokens >= 0.60 o SequenceMatcher >= 0.84",
        "umbral_externo": "Jaccard >= 0.55 o SequenceMatcher >= 0.80",
        "longitudes": longitudes,
        "lema_de_clase": lemas,
        "con_cultivo_unico_de_la_lista": con_cultivo,
        "con_region_unica": con_region,
        "con_observacion_de_frontera": con_observacion,
        "ambiguas": len(ambiguas),
        "fuera_de_alcance": len(fuera),
        "pendientes": sum(1 for r in oficiales if r["review_status"] == "pendiente_revision_humana"),
        "consultas_reales": sum(1 for r in oficiales if r["is_real_query"]),
        "sha256_jsonl": hashlib.sha256(ruta_jsonl.read_bytes()).hexdigest(),
    }
    (AQUI / "controles.json").write_text(
        json.dumps(controles, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({k: controles[k] for k in ("registros", "distribucion", "lema_de_clase", "longitudes", "ambiguas", "fuera_de_alcance", "sha256_jsonl")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
