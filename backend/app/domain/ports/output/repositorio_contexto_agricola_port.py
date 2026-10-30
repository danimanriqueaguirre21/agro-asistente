from abc import ABC, abstractmethod

from app.domain.entities.contexto_agricola import ContextoAgricola


class PuertoRepositorioContextoAgricola(ABC):
    @abstractmethod
    def guardar(self, contexto: ContextoAgricola) -> None:
        """Persiste un contexto agrícola nuevo."""

    @abstractmethod
    def listar_por_agricultor(self, agricultor_id: str) -> list[ContextoAgricola]:
        """Devuelve los contextos pertenecientes al agricultor."""

    @abstractmethod
    def buscar_por_id_para_agricultor(
        self, contexto_id: str, agricultor_id: str
    ) -> ContextoAgricola | None:
        """Obtiene un contexto si pertenece al agricultor. None si no existe o no es suyo."""

    @abstractmethod
    def seleccionar_para_agricultor(
        self, contexto_id: str, agricultor_id: str
    ) -> ContextoAgricola | None:
        """Marca el contexto como seleccionado y desmarca los demás del mismo agricultor."""
