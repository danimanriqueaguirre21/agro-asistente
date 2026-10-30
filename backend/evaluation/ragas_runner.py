from __future__ import annotations

import os
from dataclasses import dataclass

from app.infrastructure.config.settings import Settings
from evaluation.pipeline import MuestraPipeline, filas_ragas
from evaluation.preflight import EvaluacionOficialNoEjecutable, proveedor_juez_ragas


@dataclass(frozen=True)
class ConfiguracionRagas:
    metric_names: tuple[str, ...]
    llm_provider: str
    llm_model: str
    embedding_model: str | None
    requires_openai_key: bool
    notes: tuple[str, ...]


def describir_configuracion(settings: Settings) -> ConfiguracionRagas:
    proveedor = proveedor_juez_ragas()
    notas = [
        "Métricas de ragas==0.4.3: Faithfulness (fidelidad), LLMContextRecall (recuperación), ResponseRelevancy (relevancia).",
        "El juez RAGAS no vive en domain/application.",
    ]
    if proveedor == "openai":
        return ConfiguracionRagas(
            metric_names=("faithfulness", "llm_context_recall", "answer_relevancy"),
            llm_provider="openai",
            llm_model=os.environ.get("RAGAS_OPENAI_MODEL") or "gpt-4o-mini",
            embedding_model=os.environ.get("RAGAS_EMBEDDING_MODEL") or "text-embedding-3-small",
            requires_openai_key=True,
            notes=tuple(
                notas
                + [
                    "RAGAS_LLM_PROVIDER=openai usa OPENAI_API_KEY (no versionar la clave).",
                ]
            ),
        )
    return ConfiguracionRagas(
        metric_names=("faithfulness", "llm_context_recall", "answer_relevancy"),
        llm_provider="ollama",
        llm_model=settings.ollama_model,
        embedding_model=os.environ.get("RAGAS_EMBEDDING_MODEL") or settings.ollama_model,
        requires_openai_key=False,
        notes=tuple(
            notas
            + [
                "Juez local vía API compatible OpenAI de Ollama (OLLAMA_BASE_URL/v1).",
                "ResponseRelevancy necesita embeddings; por defecto reutiliza OLLAMA_MODEL. "
                "Puede instalar `nomic-embed-text` y definir RAGAS_EMBEDDING_MODEL.",
            ]
        ),
    )


def exigir_configuracion_juez(settings: Settings) -> ConfiguracionRagas:
    config = describir_configuracion(settings)
    if config.requires_openai_key and not (os.environ.get("OPENAI_API_KEY") or "").strip():
        raise EvaluacionOficialNoEjecutable(
            "EVALUACIÓN OFICIAL DETENIDA: RAGAS_LLM_PROVIDER=openai pero falta OPENAI_API_KEY. "
            "No se colocan claves en el código. Use el juez Ollama (valor por defecto) "
            "o exporta OPENAI_API_KEY en el entorno."
        )
    return config


def ejecutar_ragas(muestras: list[MuestraPipeline], settings: Settings) -> dict[str, object]:
    config = exigir_configuracion_juez(settings)
    from evaluation.ragas_compat import aplicar_compatibilidad_langchain

    aplicar_compatibilidad_langchain()
    from ragas import evaluate
    from ragas.metrics import Faithfulness, LLMContextRecall, ResponseRelevancy

    llm = _juez_llm(settings, config)
    embeddings = _juez_embeddings(settings, config)
    metricas = [
        Faithfulness(llm=llm),
        LLMContextRecall(llm=llm),
        ResponseRelevancy(llm=llm, embeddings=embeddings),
    ]
    dataset = construir_muestras_ragas(muestras)
    resultado = evaluate(dataset=dataset, metrics=metricas)
    scores = _scores_desde_resultado(resultado)
    scores["configured_metrics"] = list(config.metric_names)
    scores["judge"] = {
        "provider": config.llm_provider,
        "model": config.llm_model,
        "embedding_model": config.embedding_model,
    }
    return scores


def construir_muestras_ragas(muestras: list[MuestraPipeline]) -> object:
    from evaluation.ragas_compat import aplicar_compatibilidad_langchain

    aplicar_compatibilidad_langchain()
    from ragas.dataset_schema import EvaluationDataset, SingleTurnSample

    samples = []
    for fila in filas_ragas(muestras):
        samples.append(
            SingleTurnSample(
                user_input=str(fila["user_input"]),
                response=str(fila["response"]),
                retrieved_contexts=list(fila["retrieved_contexts"]),
                reference=str(fila["reference"]),
            )
        )
    return EvaluationDataset(samples=samples)


def _juez_llm(settings: Settings, config: ConfiguracionRagas):
    from ragas.llms import llm_factory

    client = _cliente_openai(settings, config)
    return llm_factory(config.llm_model, client=client)


def _juez_embeddings(settings: Settings, config: ConfiguracionRagas):
    from ragas.embeddings.base import embedding_factory

    client = _cliente_openai(settings, config)
    modelo = config.embedding_model or config.llm_model
    return embedding_factory(provider="openai", model=modelo, client=client)


def _cliente_openai(settings: Settings, config: ConfiguracionRagas):
    from openai import OpenAI

    if config.llm_provider == "openai":
        return OpenAI()
    base = settings.ollama_base_url.rstrip("/") + "/v1"
    return OpenAI(base_url=base, api_key=os.environ.get("RAGAS_OLLAMA_API_KEY") or "ollama")


def _scores_desde_resultado(resultado: object) -> dict[str, object]:
    if hasattr(resultado, "to_pandas"):
        frame = resultado.to_pandas()
        numeric = frame.select_dtypes(include="number")
        averages = {column: float(numeric[column].mean()) for column in numeric.columns}
        return {"averages": averages, "rows": int(len(frame))}
    if isinstance(resultado, dict):
        return {"averages": resultado, "rows": None}
    return {"averages": {"raw": str(resultado)}, "rows": None}
