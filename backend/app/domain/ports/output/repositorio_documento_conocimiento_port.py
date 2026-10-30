from abc import ABC, abstractmethod

from app.domain.entities.documento_conocimiento import DocumentoConocimiento
from app.domain.valueObjects.hash_contenido import HashContenido


class PuertoRepositorioDocumentoConocimiento(ABC):
    @abstractmethod
    def existe_por_hash(self, hash_contenido: HashContenido) -> bool:
        """True si ya hay un documento con el mismo hash de contenido."""

    @abstractmethod
    def guardar(self, documento: DocumentoConocimiento, contenido: str) -> None:
        """Persiste metadatos y el contenido del documento."""

    @abstractmethod
    def listar_todos(self) -> list[DocumentoConocimiento]:
        """Devuelve los documentos registrados."""

    @abstractmethod
    def buscar_por_id(self, documento_id: str) -> DocumentoConocimiento | None:
        """Obtiene un documento por id. None si no existe."""

    @abstractmethod
    def leer_contenido(self, documento: DocumentoConocimiento) -> str:
        """Lee el contenido Markdown persistido del documento."""

    @abstractmethod
    def actualizar_cantidad_fragmentos(self, documento_id: str, cantidad_fragmentos: int) -> None:
        """Actualiza la cantidad de fragmentos indexados del documento."""
