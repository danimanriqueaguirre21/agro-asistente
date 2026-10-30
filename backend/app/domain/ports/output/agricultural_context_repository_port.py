from abc import ABC, abstractmethod

from app.domain.entities.agricultural_context import AgriculturalContext


class AgriculturalContextRepositoryPort(ABC):
    @abstractmethod
    def save(self, context: AgriculturalContext) -> None:
        """Persiste un contexto agrícola nuevo."""

    @abstractmethod
    def list_by_farmer(self, farmer_id: str) -> list[AgriculturalContext]:
        """Devuelve los contextos pertenecientes al agricultor."""

    @abstractmethod
    def find_by_id_for_farmer(self, context_id: str, farmer_id: str) -> AgriculturalContext | None:
        """Obtiene un contexto si pertenece al agricultor. None si no existe o no es suyo."""

    @abstractmethod
    def select_for_farmer(self, context_id: str, farmer_id: str) -> AgriculturalContext | None:
        """Marca el contexto como seleccionado y desmarca los demás del mismo agricultor."""
