from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.contexto_agricola import ContextoAgricola


@dataclass(frozen=True)
class ComandoCrearContextoAgricola:
    agricultor_id: str
    nombre_predio: str | None
    cultivo: str
    region: str
    observaciones: str | None


@dataclass(frozen=True)
class ComandoSeleccionarContextoAgricola:
    agricultor_id: str
    contexto_id: str


@dataclass(frozen=True)
class ResultadoContextoAgricola:
    id: str
    agricultor_id: str
    nombre_predio: str | None
    cultivo: str
    region: str
    observaciones: str | None
    esta_seleccionado: bool
    creado_en: str


class PuertoCrearContextoAgricola(ABC):
    @abstractmethod
    def ejecutar(self, comando: ComandoCrearContextoAgricola) -> ResultadoContextoAgricola:
        """Crea un contexto agrícola para el agricultor autenticado."""


class PuertoListarContextosAgricolas(ABC):
    @abstractmethod
    def ejecutar(self, agricultor_id: str) -> list[ResultadoContextoAgricola]:
        """Lista los contextos del agricultor autenticado."""


class PuertoSeleccionarContextoAgricola(ABC):
    @abstractmethod
    def ejecutar(self, comando: ComandoSeleccionarContextoAgricola) -> ResultadoContextoAgricola:
        """Selecciona un contexto propio del agricultor autenticado."""


def contexto_a_resultado(contexto: ContextoAgricola) -> ResultadoContextoAgricola:
    return ResultadoContextoAgricola(
        id=contexto.id,
        agricultor_id=contexto.agricultor_id,
        nombre_predio=contexto.nombre_predio,
        cultivo=contexto.cultivo.value,
        region=contexto.region.value,
        observaciones=contexto.observaciones,
        esta_seleccionado=contexto.esta_seleccionado,
        creado_en=contexto.creado_en.isoformat(),
    )
