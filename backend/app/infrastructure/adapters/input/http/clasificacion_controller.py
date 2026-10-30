from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.domain.exceptions import ErrorClasificadorNoDisponible, ErrorTextoConsultaInvalido
from app.domain.ports.input.clasificar_consulta_port import ComandoClasificarConsulta
from app.domain.valueObjects.texto_consulta import TextoConsulta
from app.infrastructure.adapters.input.http.dependencia_autenticacion import (
    dependencia_agricultor_autenticado,
)
from app.infrastructure.composition import CompositionRoot


class ClasificacionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=TextoConsulta.MAX_LENGTH)


class ClasificacionResponse(BaseModel):
    categoria: str
    abstencion: bool
    motivo_abstencion: str | None
    clase_primera: str
    puntuacion_primera: float
    clase_segunda: str
    puntuacion_segunda: float
    margen: float
    puntuaciones_calibradas: bool


def create_clasificacion_router(container: CompositionRoot) -> APIRouter:
    router = APIRouter(prefix="/api/v1/clasificacion", tags=["clasificacion"])
    agricultor_autenticado = dependencia_agricultor_autenticado(container)

    @router.post("", response_model=ClasificacionResponse)
    def clasificar_consulta(
        payload: ClasificacionRequest,
        farmer_id: str = Depends(agricultor_autenticado),
    ) -> ClasificacionResponse:
        del farmer_id
        try:
            resultado = container.puerto_clasificar_consulta.ejecutar(
                ComandoClasificarConsulta(texto=payload.text)
            )
        except ErrorTextoConsultaInvalido as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        except ErrorClasificadorNoDisponible as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(error),
            ) from error
        return ClasificacionResponse(
            categoria=resultado.categoria,
            abstencion=resultado.abstencion,
            motivo_abstencion=resultado.motivo_abstencion,
            clase_primera=resultado.clase_primera,
            puntuacion_primera=resultado.puntuacion_primera,
            clase_segunda=resultado.clase_segunda,
            puntuacion_segunda=resultado.puntuacion_segunda,
            margen=resultado.margen,
            puntuaciones_calibradas=resultado.puntuaciones_calibradas,
        )

    return router
