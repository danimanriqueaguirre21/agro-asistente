from app.domain.exceptions import InvalidPasswordError


class PasswordHash:
    def __init__(self, value: str) -> None:
        if value is None or not str(value).strip():
            raise InvalidPasswordError("El hash de la contraseña es obligatorio")
        self._value = str(value)

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PasswordHash) and self._value == other._value
