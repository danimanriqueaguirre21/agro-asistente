from abc import ABC, abstractmethod

from app.domain.entities.consulta import Consulta
from app.domain.entities.contexto_agricola import ContextoAgricola
from app.domain.entities.respuesta import Respuesta


class PuertoRepositorioConsulta(ABC):
    @abstractmethod
    def buscar_contexto_seleccionado(self, agricultor_id: str) -> ContextoAgricola | None:
        """Obtiene el contexto seleccionado del agricultor. None si no hay uno propio."""

    @abstractmethod
    def guardar_consulta(self, consulta: Consulta) -> None:
        """Persiste una consulta agrícola."""

    @abstractmethod
    def guardar_respuesta(self, respuesta: Respuesta) -> None:
        """Persiste la respuesta asociada a una consulta."""
