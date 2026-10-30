from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.ports.input.clasificar_consulta_port import ResultadoClasificacionConsulta


@dataclass(frozen=True)
class ComandoRegistrarConsulta:
    agricultor_id: str
    texto: str


@dataclass(frozen=True)
class ResultadoContextoConsulta:
    id: str
    cultivo: str
    region: str
    nombre_predio: str | None


@dataclass(frozen=True)
class ResultadoEvidenciaConsulta:
    documento_id: str
    titulo_documento: str
    fragmento_id: str
    extracto: str
    puntaje_similitud: float
    orden_relevancia: int


@dataclass(frozen=True)
class ResultadoRegistrarConsulta:
    id: str
    texto: str
    respuesta: str
    metodo_generacion: str
    creado_en: str
    contexto: ResultadoContextoConsulta
    evidencias: tuple[ResultadoEvidenciaConsulta, ...]
    clasificacion: ResultadoClasificacionConsulta | None = None
    error_clasificacion: str | None = None


class PuertoRegistrarConsulta(ABC):
    @abstractmethod
    def ejecutar(self, comando: ComandoRegistrarConsulta) -> ResultadoRegistrarConsulta:
        """Registra una consulta agrícola y genera una respuesta inicial."""
