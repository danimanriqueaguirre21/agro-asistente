from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.exceptions import ErrorEscenarioRiesgoInvalido, ErrorPredictorRiesgoNoDisponible
from app.domain.ports.input.predecir_riesgo_port import ComandoPredecirRiesgo
from app.domain.ports.output.puerto_predictor_riesgo import (
    CONDICIONES_SUELO,
    FAMILIAS_ESCENARIO,
    EscenarioRiesgo,
)
from app.infrastructure.adapters.input.http.dependencia_autenticacion import (
    dependencia_agricultor_autenticado,
)
from app.infrastructure.composition import CompositionRoot


class EscenarioRiesgoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    familia_escenario: str
    cultivo: str = Field(min_length=1)
    region: str = Field(min_length=1)
    etapa_fenologica: str = Field(min_length=1)
    temperatura_c: float | None = None
    precipitacion_mm: float | None = None
    dias_sin_lluvia: int
    sintoma_observado: bool
    proporcion_afectada: float
    condicion_suelo: str

    @field_validator("familia_escenario", "cultivo", "region", "etapa_fenologica", "condicion_suelo")
    @classmethod
    def texto_presente(cls, valor: object) -> str:
        if not isinstance(valor, str):
            raise ValueError("debe ser texto")
        limpio = valor.strip()
        if not limpio:
            raise ValueError("es obligatorio")
        return limpio

    @field_validator("familia_escenario")
    @classmethod
    def familia_conocida(cls, valor: str) -> str:
        if valor not in FAMILIAS_ESCENARIO:
            raise ValueError("familia_escenario no pertenece al prototipo")
        return valor

    @field_validator("condicion_suelo")
    @classmethod
    def suelo_conocido(cls, valor: str) -> str:
        if valor not in CONDICIONES_SUELO:
            raise ValueError("condicion_suelo no pertenece al prototipo")
        return valor

    @field_validator("dias_sin_lluvia", mode="before")
    @classmethod
    def dias_entero(cls, valor: object) -> int:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("dias_sin_lluvia debe ser un entero")
        return valor

    @field_validator("sintoma_observado", mode="before")
    @classmethod
    def sintoma_booleano(cls, valor: object) -> bool:
        if not isinstance(valor, bool):
            raise ValueError("sintoma_observado debe ser true o false")
        return valor

    @field_validator("temperatura_c", "precipitacion_mm", "proporcion_afectada", mode="before")
    @classmethod
    def numero_o_nulo(cls, valor: object) -> float | None:
        if valor is None:
            return None
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("debe ser numérico o nulo")
        return float(valor)

    @field_validator("proporcion_afectada")
    @classmethod
    def proporcion_en_rango(cls, valor: float | None) -> float:
        if valor is None or not 0 <= valor <= 1:
            raise ValueError("proporcion_afectada debe estar entre 0 y 1")
        return valor

    @model_validator(mode="after")
    def proporcion_sin_sintoma(self) -> "EscenarioRiesgoRequest":
        if not self.sintoma_observado and self.proporcion_afectada != 0:
            raise ValueError("Si sintoma_observado es false, proporcion_afectada debe ser 0.")
        return self


class PrediccionRiesgoResponse(BaseModel):
    categoria_predicha: str
    identificador_modelo: str
    version_reglas: str
    naturaleza: str
    es_riesgo_agricola_validado: bool


def create_riesgo_router(container: CompositionRoot) -> APIRouter:
    router = APIRouter(prefix="/api/v1/riesgo", tags=["riesgo"])
    agricultor_autenticado = dependencia_agricultor_autenticado(container)

    @router.post("", response_model=PrediccionRiesgoResponse)
    def predecir_riesgo(
        payload: EscenarioRiesgoRequest,
        farmer_id: str = Depends(agricultor_autenticado),
    ) -> PrediccionRiesgoResponse:
        del farmer_id
        comando = ComandoPredecirRiesgo(
            escenario=EscenarioRiesgo(
                familia_escenario=payload.familia_escenario,
                cultivo=payload.cultivo,
                region=payload.region,
                etapa_fenologica=payload.etapa_fenologica,
                temperatura_c=payload.temperatura_c,
                precipitacion_mm=payload.precipitacion_mm,
                dias_sin_lluvia=payload.dias_sin_lluvia,
                sintoma_observado=payload.sintoma_observado,
                proporcion_afectada=payload.proporcion_afectada,
                condicion_suelo=payload.condicion_suelo,
            )
        )
        try:
            resultado = container.puerto_predecir_riesgo.ejecutar(comando)
        except ErrorEscenarioRiesgoInvalido as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
        except ErrorPredictorRiesgoNoDisponible as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(error),
            ) from error
        return PrediccionRiesgoResponse(
            categoria_predicha=resultado.categoria_predicha,
            identificador_modelo=resultado.identificador_modelo,
            version_reglas=resultado.version_reglas,
            naturaleza=resultado.naturaleza,
            es_riesgo_agricola_validado=resultado.es_riesgo_agricola_validado,
        )

    return router
