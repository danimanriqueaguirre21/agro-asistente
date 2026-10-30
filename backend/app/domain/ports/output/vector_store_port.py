from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class VectorRecord:
    id: str
    embedding: list[float]
    content: str
    metadata: dict[str, str | int | float]


@dataclass(frozen=True)
class VectorSearchHit:
    id: str
    content: str
    metadata: dict[str, str | int | float]
    similarity: float


class VectorStorePort(ABC):
    """Puerto de salida para indexar vectores y buscar por similitud.

    El dominio no conoce Chroma ni ningún otro almacén vectorial concreto.
    """

    @abstractmethod
    def upsert(self, records: list[VectorRecord]) -> None:
        """Inserta o reemplaza vectores/documentos por identificador."""

    @abstractmethod
    def similarity_search(self, embedding: list[float], top_k: int) -> list[VectorSearchHit]:
        """Devuelve los fragmentos más similares al vector de consulta."""
