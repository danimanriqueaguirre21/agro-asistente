import re

from app.domain.exceptions import ErrorCorreoInvalido

_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


class Email:
    def __init__(self, value: str) -> None:
        if value is None or not str(value).strip():
            raise ErrorCorreoInvalido("El correo electrónico es obligatorio")
        normalized = str(value).strip().lower()
        if not _EMAIL_PATTERN.match(normalized):
            raise ErrorCorreoInvalido("El correo electrónico no tiene un formato válido")
        self._value = normalized

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Email) and self._value == other._value

    def __str__(self) -> str:
        return self._value
