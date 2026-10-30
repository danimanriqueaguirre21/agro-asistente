from app.domain.ports.output.embedding_port import EmbeddingPort


class EmbeddingProviderNotConfiguredError(RuntimeError):
    """El proveedor concreto de embeddings aún no ha sido seleccionado."""


class ExternalEmbeddingAdapter(EmbeddingPort):
    """Adaptador de salida para una API externa de embeddings.

    Fase 1: queda preparado y lee credenciales desde variables de entorno.
    No invoca todavía un proveedor concreto (OpenAI, Gemini, Hugging Face, etc.).
    """

    def __init__(self, api_url: str = "", api_key: str = "", model: str = "") -> None:
        self._api_url = api_url
        self._api_key = api_key
        self._model = model

    def embed_text(self, text: str) -> list[float]:
        self._ensure_ready(text)
        raise EmbeddingProviderNotConfiguredError(self._pending_message())

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        self._ensure_ready(texts[0])
        raise EmbeddingProviderNotConfiguredError(self._pending_message())

    def _ensure_ready(self, text: str) -> None:
        if not text or not text.strip():
            raise ValueError("El texto a embebir no puede estar vacío.")

    def _pending_message(self) -> str:
        return (
            "ExternalEmbeddingAdapter está preparado, pero el proveedor concreto "
            "de embeddings aún no ha sido seleccionado. Las credenciales deben "
            "configurarse únicamente con EMBEDDING_API_URL, EMBEDDING_API_KEY y "
            "EMBEDDING_MODEL."
        )
