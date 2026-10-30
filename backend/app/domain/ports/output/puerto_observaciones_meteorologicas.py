from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.observacion_meteorologica import ObservacionMeteorologica


@dataclass(frozen=True)
class FiltroObservacionesMeteorologicas:
    """Criterios de consulta recientes. El dominio no conoce parámetros de un API concreto."""

    limite: int = 10
    fecha_hora: str | None = None
    caja_geografica: tuple[float, float, float, float] | None = None
    identificador_estacion: str | None = None
    nombre_variable: str | None = None
    orden: str | None = None


class PuertoObservacionesMeteorologicas(ABC):
    """Puerto de salida para observaciones meteorológicas recientes."""

    @abstractmethod
    def obtener_recientes(
        self, filtro: FiltroObservacionesMeteorologicas | None = None
    ) -> list[ObservacionMeteorologica]:
        """Devuelve observaciones recientes según el filtro, sin inventar valores."""
