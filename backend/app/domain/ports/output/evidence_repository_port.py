from abc import ABC, abstractmethod

from app.domain.entities.evidence import Evidence


class EvidenceRepositoryPort(ABC):
    @abstractmethod
    def save_all(self, evidences: list[Evidence]) -> None:
        """Persiste las evidencias asociadas a una consulta."""

    @abstractmethod
    def list_by_query_id(self, query_id: str) -> list[Evidence]:
        """Obtiene las evidencias persistidas de una consulta."""
