from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.domain.entities.documento_conocimiento import DocumentoConocimiento
from app.domain.exceptions import (
    ErrorArchivoConocimientoNoEncontrado,
    ErrorDocumentoConocimientoDuplicado,
    ErrorDocumentoConocimientoInvalido,
    ErrorDominio,
)
from app.domain.ports.input.incorporar_conocimiento_port import (
    ComandoIncorporarConocimiento,
    ResultadoDocumentoConocimiento,
)
from app.infrastructure.adapters.input.http.dependencia_autenticacion import (
    dependencia_agricultor_autenticado,
)
from app.infrastructure.composition import CompositionRoot


class IngestKnowledgeRequest(BaseModel):
    title: str = Field(min_length=1, max_length=DocumentoConocimiento.LONGITUD_MAXIMA_TITULO)
    topic: str = Field(min_length=1, max_length=DocumentoConocimiento.LONGITUD_MAXIMA_TEMA)
    content: str = Field(min_length=1, max_length=DocumentoConocimiento.LONGITUD_MAXIMA_CONTENIDO)


class KnowledgeDocumentResponse(BaseModel):
    id: str
    title: str
    topic: str
    source_path: str
    content_hash: str
    chunk_count: int
    ingested_at: str
    status: str


class IndexKnowledgeResponse(BaseModel):
    indexed_documents: int
    total_chunks: int
    collection: str
    documents: list[KnowledgeDocumentResponse]


def _documento_response(resultado: ResultadoDocumentoConocimiento) -> KnowledgeDocumentResponse:
    return KnowledgeDocumentResponse(
        id=resultado.id,
        title=resultado.titulo,
        topic=resultado.tema,
        source_path=resultado.ruta_origen,
        content_hash=resultado.hash_contenido,
        chunk_count=resultado.cantidad_fragmentos,
        ingested_at=resultado.incorporado_en,
        status=resultado.estado,
    )


def create_knowledge_router(container: CompositionRoot) -> APIRouter:
    router = APIRouter(prefix="/api/v1/knowledge", tags=["knowledge"])
    require_authenticated_farmer = dependencia_agricultor_autenticado(container)

    @router.post(
        "/ingest",
        status_code=status.HTTP_201_CREATED,
        response_model=KnowledgeDocumentResponse,
    )
    def ingest_knowledge(
        payload: IngestKnowledgeRequest,
        _farmer_id: str = Depends(require_authenticated_farmer),
    ) -> KnowledgeDocumentResponse:
        command = ComandoIncorporarConocimiento(
            titulo=payload.title,
            tema=payload.topic,
            contenido=payload.content,
        )
        try:
            result = container.puerto_incorporar_conocimiento.ejecutar(command)
        except ErrorDocumentoConocimientoDuplicado as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        except ErrorDocumentoConocimientoInvalido as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        except ErrorDominio as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        return _documento_response(result)

    @router.post("/index", response_model=IndexKnowledgeResponse)
    def index_knowledge(
        _farmer_id: str = Depends(require_authenticated_farmer),
    ) -> IndexKnowledgeResponse:
        try:
            result = container.puerto_indexar_conocimiento.ejecutar()
        except ErrorArchivoConocimientoNoEncontrado as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        except ErrorDominio as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        return IndexKnowledgeResponse(
            indexed_documents=result.documentos_indexados,
            total_chunks=result.total_fragmentos,
            collection=container.settings.chroma_collection,
            documents=[_documento_response(item) for item in result.documentos],
        )

    @router.get("/documents", response_model=list[KnowledgeDocumentResponse])
    def list_knowledge_documents(
        _farmer_id: str = Depends(require_authenticated_farmer),
    ) -> list[KnowledgeDocumentResponse]:
        results = container.puerto_listar_documentos_conocimiento.ejecutar()
        return [_documento_response(item) for item in results]

    return router
