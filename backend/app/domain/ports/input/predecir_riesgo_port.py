from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.ports.output.puerto_predictor_riesgo import EscenarioRiesgo


@dataclass(frozen=True)
class ComandoPredecirRiesgo:
    escenario: EscenarioRiesgo


@dataclass(frozen=True)
class ResultadoPrediccionRiesgo:
    categoria_predicha: str
    identificador_modelo: str
    version_reglas: str
    naturaleza: str
    es_riesgo_agricola_validado: bool


class PuertoPredecirRiesgo(ABC):
    @abstractmethod
    def ejecutar(self, comando: ComandoPredecirRiesgo) -> ResultadoPrediccionRiesgo:
        """Predice una categoría sintética. No consulta RAG ni genera texto."""
