from abc import ABC, abstractmethod
from dataclasses import dataclass

CATEGORIAS_RIESGO = ("bajo", "medio", "alto")
CATEGORIAS_RIESGO_CONJUNTO = frozenset(CATEGORIAS_RIESGO)
IDENTIFICADOR_MODELO_RIESGO = "bosque_aleatorio_profundidad12_hoja1"
VERSION_REGLAS_RIESGO = "sintetica-hu08-v1"
NATURALEZA_RIESGO = "prototipo_academico_sintetico"
FAMILIAS_ESCENARIO = ("meteorologico", "plaga_enfermedad", "suelo_agua_manejo")
CONDICIONES_SUELO = ("seco", "adecuado", "encharcado")


@dataclass(frozen=True)
class EscenarioRiesgo:
    familia_escenario: str
    cultivo: str
    region: str
    etapa_fenologica: str
    temperatura_c: float | None
    precipitacion_mm: float | None
    dias_sin_lluvia: int
    sintoma_observado: bool
    proporcion_afectada: float
    condicion_suelo: str


class PuertoPredictorRiesgo(ABC):
    @abstractmethod
    def predecir(self, escenario: EscenarioRiesgo) -> str:
        """Devuelve solo la categoría del prototipo. No calibra probabilidades."""
