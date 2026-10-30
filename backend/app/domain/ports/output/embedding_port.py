from abc import ABC, abstractmethod


class EmbeddingPort(ABC):
    """Puerto de salida para convertir texto en embeddings.

    El dominio no conoce el proveedor HTTP/SDK. La implementación concreta
    vive en infraestructura (ExternalEmbeddingAdapter).
    """

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """Genera el vector de un texto."""

    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Genera vectores para una lista de textos."""
