from app.domain.exceptions import InvalidQueryTextError


class QueryText:
    MAX_LENGTH = 2000

    def __init__(self, value: str) -> None:
        if value is None:
            raise InvalidQueryTextError("El texto de la consulta es obligatorio")
        clean = str(value).strip()
        if not clean:
            raise InvalidQueryTextError("El texto de la consulta es obligatorio")
        if len(clean) > self.MAX_LENGTH:
            raise InvalidQueryTextError("El texto de la consulta supera la longitud permitida")
        self._value = clean

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, QueryText) and self._value == other._value

    def __str__(self) -> str:
        return self._value
