from app.domain.exceptions import ErrorDatosContextoInvalidos


class Region:
    def __init__(self, value: str) -> None:
        clean = (value or "").strip()
        if not clean:
            raise ErrorDatosContextoInvalidos("La región es obligatoria")
        if len(clean) > 120:
            raise ErrorDatosContextoInvalidos("La región supera la longitud permitida")
        self._value = clean

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Region) and self._value == other._value
