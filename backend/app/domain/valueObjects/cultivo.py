from app.domain.exceptions import ErrorDatosContextoInvalidos


class Cultivo:
    def __init__(self, value: str) -> None:
        clean = (value or "").strip()
        if not clean:
            raise ErrorDatosContextoInvalidos("El cultivo es obligatorio")
        if len(clean) > 50:
            raise ErrorDatosContextoInvalidos("El cultivo supera la longitud permitida")
        self._value = clean

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Cultivo) and self._value == other._value
