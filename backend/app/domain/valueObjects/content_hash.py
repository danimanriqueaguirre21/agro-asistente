import hashlib
import re

from app.domain.exceptions import InvalidKnowledgeDocumentError

_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


class ContentHash:
    """SHA-256 del contenido. Es determinista: el mismo texto produce el mismo valor."""

    def __init__(self, value: str) -> None:
        clean = (value or "").strip().lower()
        if not _SHA256_HEX.fullmatch(clean):
            raise InvalidKnowledgeDocumentError("El hash de contenido es inválido")
        self._value = clean

    @classmethod
    def from_content(cls, content: str) -> "ContentHash":
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return cls(digest)

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ContentHash) and self._value == other._value

    def __str__(self) -> str:
        return self._value
