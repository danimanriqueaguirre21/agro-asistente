from abc import ABC, abstractmethod

from app.domain.entities.agricultural_context import AgriculturalContext
from app.domain.entities.query import Query
from app.domain.entities.response import Response


class QueryRepositoryPort(ABC):
    @abstractmethod
    def find_selected_context(self, farmer_id: str) -> AgriculturalContext | None:
        """Obtiene el contexto seleccionado del agricultor. None si no hay uno propio."""

    @abstractmethod
    def save_query(self, query: Query) -> None:
        """Persiste una consulta agrícola."""

    @abstractmethod
    def save_response(self, response: Response) -> None:
        """Persiste la respuesta asociada a una consulta."""
