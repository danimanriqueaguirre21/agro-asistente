from __future__ import annotations

from dataclasses import dataclass, field

from app.application.services.servicio_recuperacion_rag import ServicioRecuperacionRag
from app.domain.ports.output.text_generation_port import PasajeRecuperado, PuertoGeneracionTexto
from app.infrastructure.adapters.output.chroma.chroma_vector_store_adapter import (
    ChromaVectorStoreAdapter,
)
from app.infrastructure.adapters.output.embedding.local_lexical_embedding_adapter import (
    LocalLexicalEmbeddingAdapter,
)
from app.infrastructure.adapters.output.generation.adaptador_generacion_ollama import (
    AdaptadorGeneracionOllama,
)
from app.infrastructure.config.settings import Settings
from evaluation.dataset import DatasetEvaluacion, ItemEvaluacion
from evaluation.preflight import EvaluacionOficialNoEjecutable, exigir_proveedor_ollama


@dataclass
class MuestraPipeline:
    id: str
    question: str
    ground_truth: str
    answer: str
    contexts: list[str]
    crop: str
    region: str
    source_documents: list[str]
    generation_method: str
    retrieved_document_titles: list[str] = field(default_factory=list)


def construir_recuperacion(settings: Settings) -> ServicioRecuperacionRag:
    embedding = LocalLexicalEmbeddingAdapter(dimension=settings.embedding_dimension)
    almacen = ChromaVectorStoreAdapter(
        persist_dir=settings.chroma_persist_dir,
        collection_name=settings.chroma_collection,
    )
    return ServicioRecuperacionRag(
        embedding_port=embedding,
        almacen_vectores=almacen,
        top_k=settings.rag_top_k,
        similitud_minima=settings.rag_min_similarity,
    )


def construir_generacion(settings: Settings) -> PuertoGeneracionTexto:
    exigir_proveedor_ollama(settings)
    return AdaptadorGeneracionOllama(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
        timeout_seconds=settings.ollama_timeout_seconds,
    )


def exigir_indice_chroma(recuperacion: ServicioRecuperacionRag) -> int:
    almacen = recuperacion._almacen_vectores
    coleccion = getattr(almacen, "_collection", None)
    if coleccion is None:
        raise EvaluacionOficialNoEjecutable(
            "EVALUACIÓN OFICIAL DETENIDA: no se pudo inspeccionar Chroma."
        )
    cantidad = int(coleccion.count())
    if cantidad < 1:
        raise EvaluacionOficialNoEjecutable(
            "EVALUACIÓN OFICIAL DETENIDA: la colección Chroma está vacía. "
            "Indexe el conocimiento (POST /api/v1/knowledge/index) antes de RAGAS. "
            "Esa indexación usa el catálogo de MySQL."
        )
    return cantidad


def ejecutar_item(
    item: ItemEvaluacion,
    recuperacion: ServicioRecuperacionRag,
    generacion: PuertoGeneracionTexto,
) -> MuestraPipeline:
    fragmentos = recuperacion.recuperar(item.question)
    pasajes = [
        PasajeRecuperado(titulo=fragmento.titulo_documento, extracto=fragmento.extracto)
        for fragmento in fragmentos
    ]
    generada = generacion.generar(
        texto_consulta=item.question,
        cultivo=item.crop,
        region=item.region,
        pasajes=pasajes,
    )
    return MuestraPipeline(
        id=item.id,
        question=item.question,
        ground_truth=item.ground_truth,
        answer=generada.texto_respuesta,
        contexts=[fragmento.extracto for fragmento in fragmentos],
        crop=item.crop,
        region=item.region,
        source_documents=list(item.source_documents),
        generation_method=generada.metodo_generacion,
        retrieved_document_titles=[fragmento.titulo_documento for fragmento in fragmentos],
    )


def ejecutar_dataset(
    dataset: DatasetEvaluacion,
    recuperacion: ServicioRecuperacionRag,
    generacion: PuertoGeneracionTexto,
) -> list[MuestraPipeline]:
    return [ejecutar_item(item, recuperacion, generacion) for item in dataset.items]


def filas_ragas(muestras: list[MuestraPipeline]) -> list[dict[str, object]]:
    """Campos de RAGAS 0.3 (user_input/response/retrieved_contexts/reference) más aliases clásicos."""
    filas: list[dict[str, object]] = []
    for muestra in muestras:
        filas.append(
            {
                "user_input": muestra.question,
                "response": muestra.answer,
                "retrieved_contexts": list(muestra.contexts),
                "reference": muestra.ground_truth,
                "question": muestra.question,
                "answer": muestra.answer,
                "contexts": list(muestra.contexts),
                "ground_truth": muestra.ground_truth,
            }
        )
    return filas
