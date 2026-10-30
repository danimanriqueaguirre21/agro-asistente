from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ComandoObtenerObservacionesMeteorologicas:
    limite: int = 10
    fecha_hora: str | None = None
    caja_geografica: tuple[float, float, float, float] | None = None
    identificador_estacion: str | None = None
    nombre_variable: str | None = None
    orden: str | None = None


@dataclass(frozen=True)
class ResultadoObservacionMeteorologica:
    identificador_estacion: str
    nombre_estacion: str | None
    latitud: float | None
    longitud: float | None
    altitud: float | None
    fecha_hora: str | None
    temperatura: float | None
    punto_rocio: float | None
    precipitacion: float | None


class PuertoObtenerObservacionesMeteorologicas(ABC):
    @abstractmethod
    def ejecutar(
        self, comando: ComandoObtenerObservacionesMeteorologicas
    ) -> list[ResultadoObservacionMeteorologica]:
        """Obtiene observaciones meteorológicas recientes normalizadas."""
