from abc import ABC, abstractmethod
from dataclasses import dataclass

CATEGORIAS_TEMATICAS = (
    "riego",
    "fertilizacion_nutricion",
    "plagas",
    "enfermedades_cultivos",
    "siembra_manejo_cultivo",
    "clima_heladas",
    "suelos",
    "cosecha_poscosecha",
)
CATEGORIAS_TEMATICAS_CONJUNTO = frozenset(CATEGORIAS_TEMATICAS)
SALIDA_SIN_CATEGORIA = "sin categoría"
MOTIVO_MARGEN_INSUFICIENTE = "margen_insuficiente"


@dataclass(frozen=True)
class PuntuacionModelo:
    """Dos clases punteras del modelo. Ambas pertenecen a las ocho categorías."""

    clase_primera: str
    puntuacion_primera: float
    clase_segunda: str
    puntuacion_segunda: float


class PuertoClasificadorConsultas(ABC):
    """Puerto de salida. No aplica el umbral ni conoce el endpoint."""

    @abstractmethod
    def puntuar(self, texto: str) -> PuntuacionModelo:
        """Devuelve las dos clases con mayor puntuación del modelo cargado."""
