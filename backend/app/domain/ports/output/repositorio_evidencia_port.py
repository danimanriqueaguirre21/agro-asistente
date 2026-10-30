from abc import ABC, abstractmethod

from app.domain.entities.evidencia import Evidencia


class PuertoRepositorioEvidencia(ABC):
    @abstractmethod
    def guardar_todas(self, evidencias: list[Evidencia]) -> None:
        """Persiste las evidencias asociadas a una consulta."""

    @abstractmethod
    def listar_por_consulta_id(self, consulta_id: str) -> list[Evidencia]:
        """Obtiene las evidencias persistidas de una consulta."""
