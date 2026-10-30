"""Línea base RAGAS del PMV1. Ejecutar desde backend/: python -m evaluation.run_baseline"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from app.infrastructure.config.settings import Settings, get_settings
from evaluation.dataset import cargar_dataset
from evaluation.pipeline import (
    construir_generacion,
    construir_recuperacion,
    ejecutar_dataset,
    exigir_indice_chroma,
    filas_ragas,
)
from evaluation.preflight import EvaluacionOficialNoEjecutable, exigir_ollama_disponible
from evaluation.ragas_runner import describir_configuracion, ejecutar_ragas

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def main() -> int:
    settings = _settings_de_evaluacion()
    try:
        exigir_ollama_disponible(settings)
        recuperacion = construir_recuperacion(settings)
        exigir_indice_chroma(recuperacion)
        generacion = construir_generacion(settings)
        dataset = cargar_dataset()
        muestras = ejecutar_dataset(dataset, recuperacion, generacion)
        scores = ejecutar_ragas(muestras, settings)
    except EvaluacionOficialNoEjecutable as error:
        print(str(error), file=sys.stderr)
        return 2

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    samples_path = RESULTS_DIR / f"pmv1_baseline_samples_{stamp}.json"
    scores_path = RESULTS_DIR / f"pmv1_baseline_scores_{stamp}.json"
    payload_samples = {
        "dataset_id": dataset.id,
        "generated_at": stamp,
        "generation_provider": settings.generation_provider,
        "ollama_model": settings.ollama_model,
        "samples": [
            {
                "id": item.id,
                "question": item.question,
                "answer": item.answer,
                "contexts": item.contexts,
                "ground_truth": item.ground_truth,
                "source_documents": item.source_documents,
                "generation_method": item.generation_method,
            }
            for item in muestras
        ],
        "ragas_rows": filas_ragas(muestras),
    }
    samples_path.write_text(json.dumps(payload_samples, ensure_ascii=False, indent=2), encoding="utf-8")
    scores_path.write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Muestras reales: {samples_path}")
    print(f"Puntuaciones RAGAS: {scores_path}")
    print(json.dumps(scores.get("averages", {}), ensure_ascii=False, indent=2))
    return 0


def _settings_de_evaluacion() -> Settings:
    get_settings.cache_clear()
    return get_settings()


if __name__ == "__main__":
    config = describir_configuracion(_settings_de_evaluacion())
    print("Configuración RAGAS prevista:", flush=True)
    print(f"  juez={config.llm_provider} modelo={config.llm_model}", flush=True)
    print(f"  métricas={', '.join(config.metric_names)}", flush=True)
    sys.exit(main())
