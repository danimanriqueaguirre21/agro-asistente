from app.application.services.fragmentador_documentos import FragmentadorDocumentos, FragmentoDocumento
from app.domain.entities.documento_conocimiento import DocumentoConocimiento
from app.domain.exceptions import ErrorArchivoConocimientoNoEncontrado
from app.domain.ports.input.incorporar_conocimiento_port import documento_a_resultado
from app.domain.ports.input.indexar_conocimiento_port import (
    PuertoIndexarConocimiento,
    ResultadoIndexarConocimiento,
)
from app.domain.ports.output.embedding_port import EmbeddingPort
from app.domain.ports.output.repositorio_documento_conocimiento_port import (
    PuertoRepositorioDocumentoConocimiento,
)
from app.domain.ports.output.vector_store_port import VectorRecord, VectorStorePort


class IndexarConocimiento(PuertoIndexarConocimiento):
    def __init__(
        self,
        repositorio_conocimiento: PuertoRepositorioDocumentoConocimiento,
        embedding_port: EmbeddingPort,
        almacen_vectores: VectorStorePort,
        fragmentador: FragmentadorDocumentos,
    ) -> None:
        self._repositorio_conocimiento = repositorio_conocimiento
        self._embedding_port = embedding_port
        self._almacen_vectores = almacen_vectores
        self._fragmentador = fragmentador

    def ejecutar(self) -> ResultadoIndexarConocimiento:
        documentos = self._repositorio_conocimiento.listar_todos()
        indexados: list[DocumentoConocimiento] = []
        total_fragmentos = 0
        for documento in documentos:
            fragmentos = self._indexar_documento(documento)
            if fragmentos is None:
                continue
            total_fragmentos += len(fragmentos)
            documento.cantidad_fragmentos = len(fragmentos)
            self._repositorio_conocimiento.actualizar_cantidad_fragmentos(
                documento.id, len(fragmentos)
            )
            indexados.append(documento)
        return ResultadoIndexarConocimiento(
            documentos_indexados=len(indexados),
            total_fragmentos=total_fragmentos,
            documentos=tuple(
                documento_a_resultado(item, estado="indexed") for item in indexados
            ),
        )

    def _indexar_documento(
        self, documento: DocumentoConocimiento
    ) -> list[FragmentoDocumento] | None:
        try:
            contenido = self._repositorio_conocimiento.leer_contenido(documento)
        except (FileNotFoundError, ErrorArchivoConocimientoNoEncontrado):
            return None
        fragmentos = self._fragmentador.fragmentar(contenido, documento)
        if not fragmentos:
            return []
        embeddings = self._embedding_port.embed_texts(
            [fragmento.contenido for fragmento in fragmentos]
        )
        registros = [
            VectorRecord(
                id=fragmento.fragmento_id,
                embedding=embedding,
                content=fragmento.contenido,
                metadata={
                    "document_id": fragmento.documento_id,
                    "document_title": fragmento.titulo,
                    "topic": fragmento.tema,
                    "content_hash": fragmento.hash_contenido,
                    "chunk_index": fragmento.indice_fragmento,
                    "source_path": fragmento.ruta_origen,
                },
            )
            for fragmento, embedding in zip(fragmentos, embeddings, strict=True)
        ]
        self._almacen_vectores.upsert(registros)
        return fragmentos
