from dataclasses import dataclass


@dataclass(frozen=True)
class ObservacionMeteorologica:
    """Observación meteorológica normalizada. No describe un formato de proveedor externo."""

    identificador_estacion: str
    nombre_estacion: str | None
    latitud: float | None
    longitud: float | None
    altitud: float | None
    fecha_hora: str | None
    temperatura: float | None
    punto_rocio: float | None
    precipitacion: float | None
