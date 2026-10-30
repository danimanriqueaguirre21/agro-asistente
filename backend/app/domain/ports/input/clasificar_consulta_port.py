from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ComandoClasificarConsulta:
    texto: str


@dataclass(frozen=True)
class ResultadoClasificacionConsulta:
    categoria: str
    abstencion: bool
    motivo_abstencion: str | None
    clase_primera: str
    puntuacion_primera: float
    clase_segunda: str
    puntuacion_segunda: float
    margen: float
    puntuaciones_calibradas: bool


class PuertoClasificarConsulta(ABC):
    @abstractmethod
    def ejecutar(self, comando: ComandoClasificarConsulta) -> ResultadoClasificacionConsulta:
        """Clasifica una consulta o se abstiene. No llama al RAG ni a la generación."""
