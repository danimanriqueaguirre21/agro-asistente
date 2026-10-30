from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

EVALUATION_DIR = Path(__file__).resolve().parent
DATASET_PATH = EVALUATION_DIR / "data" / "pmv1_baseline.json"
KNOWLEDGE_DIR = EVALUATION_DIR.parents[1] / "knowledge"

REQUIRED_ITEM_FIELDS = (
    "id",
    "question",
    "ground_truth",
    "crop",
    "region",
    "source_documents",
)


class DatasetEvaluacionInvalido(ValueError):
    """El JSON de línea base no cumple las reglas de trazabilidad."""


@dataclass(frozen=True)
class ItemEvaluacion:
    id: str
    question: str
    ground_truth: str
    crop: str
    region: str
    source_documents: tuple[str, ...]


@dataclass(frozen=True)
class DatasetEvaluacion:
    id: str
    phase: str
    description: str
    items: tuple[ItemEvaluacion, ...]


def ruta_dataset_por_defecto() -> Path:
    return DATASET_PATH


def cargar_dataset(ruta: Path | None = None) -> DatasetEvaluacion:
    archivo = ruta or DATASET_PATH
    payload = json.loads(archivo.read_text(encoding="utf-8"))
    return validar_dataset(payload, knowledge_dir=KNOWLEDGE_DIR)


def validar_dataset(
    payload: dict[str, object],
    knowledge_dir: Path | None = None,
) -> DatasetEvaluacion:
    knowledge = knowledge_dir or KNOWLEDGE_DIR
    dataset_id = str(payload.get("id") or "").strip()
    phase = str(payload.get("phase") or "").strip()
    description = str(payload.get("description") or "").strip()
    raw_items = payload.get("items")
    if not dataset_id:
        raise DatasetEvaluacionInvalido("El dataset necesita un id.")
    if not isinstance(raw_items, list) or not raw_items:
        raise DatasetEvaluacionInvalido("El dataset necesita una lista de items no vacía.")

    items: list[ItemEvaluacion] = []
    seen_ids: set[str] = set()
    for raw in raw_items:
        if not isinstance(raw, dict):
            raise DatasetEvaluacionInvalido("Cada item debe ser un objeto JSON.")
        item = _item_desde_dict(raw)
        if item.id in seen_ids:
            raise DatasetEvaluacionInvalido(f"id duplicado en el dataset: {item.id}")
        seen_ids.add(item.id)
        _verificar_trazabilidad(item, knowledge)
        items.append(item)

    return DatasetEvaluacion(
        id=dataset_id,
        phase=phase,
        description=description,
        items=tuple(items),
    )


def _item_desde_dict(raw: dict[str, object]) -> ItemEvaluacion:
    missing = [field for field in REQUIRED_ITEM_FIELDS if field not in raw]
    if missing:
        raise DatasetEvaluacionInvalido(f"Faltan campos {missing} en un item.")
    question = str(raw["question"] or "").strip()
    ground_truth = str(raw["ground_truth"] or "").strip()
    item_id = str(raw["id"] or "").strip()
    crop = str(raw["crop"] or "").strip()
    region = str(raw["region"] or "").strip()
    sources_raw = raw["source_documents"]
    if not item_id:
        raise DatasetEvaluacionInvalido("Hay un item sin id.")
    if not question:
        raise DatasetEvaluacionInvalido(f"La pregunta de {item_id} está vacía.")
    if not ground_truth:
        raise DatasetEvaluacionInvalido(f"El ground_truth de {item_id} está vacío.")
    if not crop or not region:
        raise DatasetEvaluacionInvalido(f"{item_id} necesita cultivo y región de contexto.")
    if not isinstance(sources_raw, list) or not sources_raw:
        raise DatasetEvaluacionInvalido(f"{item_id} necesita source_documents.")
    sources = tuple(str(name).strip() for name in sources_raw if str(name).strip())
    if not sources:
        raise DatasetEvaluacionInvalido(f"{item_id} no tiene documentos fuente válidos.")
    return ItemEvaluacion(
        id=item_id,
        question=question,
        ground_truth=ground_truth,
        crop=crop,
        region=region,
        source_documents=sources,
    )


def _verificar_trazabilidad(item: ItemEvaluacion, knowledge_dir: Path) -> None:
    contenidos: list[str] = []
    for nombre in item.source_documents:
        ruta = knowledge_dir / nombre
        if not ruta.is_file():
            raise DatasetEvaluacionInvalido(
                f"{item.id} referencia un documento inexistente: {nombre}"
            )
        contenidos.append(ruta.read_text(encoding="utf-8"))
    unido = "\n".join(contenidos)
    for fragmento in _oraciones_ground_truth(item.ground_truth):
        if fragmento.lower() not in unido.lower():
            raise DatasetEvaluacionInvalido(
                f"{item.id}: el ground_truth no aparece en {list(item.source_documents)}: {fragmento}"
            )


def _oraciones_ground_truth(texto: str) -> list[str]:
    partes = [parte.strip() for parte in texto.replace(".", ".\n").split("\n")]
    return [parte.rstrip(".") for parte in partes if len(parte.strip()) > 8]
