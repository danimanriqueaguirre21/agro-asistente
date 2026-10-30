import hashlib
import re
import unicodedata

from app.domain.ports.output.embedding_port import EmbeddingPort

_TOKEN = re.compile(r"[a-z0-9áéíóúüñ]+", re.IGNORECASE)


class LocalLexicalEmbeddingAdapter(EmbeddingPort):
    """Embedding léxico local por hashing de tokens.

    No es un embedding semántico neuronal ni una API externa de IA.
    Sirve para que Chroma pueda indexar y recuperar por solapamiento de términos
    en el PMV1. El punto de sustitución sigue siendo ExternalEmbeddingAdapter
    (Sesión 3).
    """

    DEFAULT_DIMENSION = 128

    def __init__(self, dimension: int = DEFAULT_DIMENSION) -> None:
        if dimension < 8:
            raise ValueError("La dimensión del embedding local debe ser al menos 8")
        self._dimension = dimension

    def embed_text(self, text: str) -> list[float]:
        clean = (text or "").strip()
        if not clean:
            raise ValueError("El texto a embebir no puede estar vacío.")
        return self._vector(clean)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(item) for item in texts]

    def _vector(self, text: str) -> list[float]:
        tokens = _tokenize(text)
        values = [0.0] * self._dimension
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self._dimension
            values[index] += 1.0
        return _l2_normalize(values)


def _tokenize(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFC", text.lower())
    tokens = _TOKEN.findall(normalized)
    if tokens:
        return tokens
    return [normalized]


def _l2_normalize(values: list[float]) -> list[float]:
    norm = sum(item * item for item in values) ** 0.5
    if norm == 0:
        fallback = [0.0] * len(values)
        fallback[0] = 1.0
        return fallback
    return [item / norm for item in values]
