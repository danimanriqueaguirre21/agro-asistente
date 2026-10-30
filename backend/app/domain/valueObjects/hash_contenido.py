import hashlib
import re

from app.domain.exceptions import ErrorDocumentoConocimientoInvalido

_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


class HashContenido:
    """SHA-256 del contenido. Es determinista: el mismo texto produce el mismo valor."""

    def __init__(self, value: str) -> None:
        clean = (value or "").strip().lower()
        if not _SHA256_HEX.fullmatch(clean):
            raise ErrorDocumentoConocimientoInvalido("El hash de contenido es inválido")
        self._value = clean

    @classmethod
    def desde_contenido(cls, contenido: str) -> "HashContenido":
        digest = hashlib.sha256(contenido.encode("utf-8")).hexdigest()
        return cls(digest)

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, HashContenido) and self._value == other._value

    def __str__(self) -> str:
        return self._value
