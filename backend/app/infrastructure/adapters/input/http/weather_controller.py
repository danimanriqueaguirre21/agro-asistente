from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.domain.exceptions import ErrorDominio, ErrorObservacionesMeteorologicas
from app.domain.ports.input.obtener_observaciones_meteorologicas_port import (
    ComandoObtenerObservacionesMeteorologicas,
)
from app.infrastructure.composition import CompositionRoot


class WeatherObservationResponse(BaseModel):
    station_id: str
    station_name: str | None
    latitude: float | None
    longitude: float | None
    altitude: float | None
    observation_datetime: str | None
    air_temperature: float | None
    dewpoint_temperature: float | None
    precipitation: float | None


def create_weather_router(container: CompositionRoot) -> APIRouter:
    router = APIRouter(prefix="/api/v1/weather", tags=["weather"])

    @router.get("/observations", response_model=list[WeatherObservationResponse])
    def list_weather_observations(
        limit: int = Query(default=10, ge=1, le=50),
        datetime: str | None = Query(default=None),
        bbox: str | None = Query(
            default=None,
            description="minLon,minLat,maxLon,maxLat",
        ),
        wigos_station_identifier: str | None = Query(default=None),
        name: str | None = Query(default=None),
        sortby: str | None = Query(default="-reportTime"),
    ) -> list[WeatherObservationResponse]:
        caja = _parse_bbox(bbox)
        comando = ComandoObtenerObservacionesMeteorologicas(
            limite=limit,
            fecha_hora=datetime,
            caja_geografica=caja,
            identificador_estacion=wigos_station_identifier,
            nombre_variable=name,
            orden=sortby,
        )
        try:
            resultados = container.puerto_obtener_observaciones_meteorologicas.ejecutar(comando)
        except ErrorObservacionesMeteorologicas as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(error),
            ) from error
        except ErrorDominio as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        return [
            WeatherObservationResponse(
                station_id=item.identificador_estacion,
                station_name=item.nombre_estacion,
                latitude=item.latitud,
                longitude=item.longitud,
                altitude=item.altitud,
                observation_datetime=item.fecha_hora,
                air_temperature=item.temperatura,
                dewpoint_temperature=item.punto_rocio,
                precipitation=item.precipitacion,
            )
            for item in resultados
        ]

    return router


def _parse_bbox(bbox: str | None) -> tuple[float, float, float, float] | None:
    if bbox is None or not str(bbox).strip():
        return None
    partes = [p.strip() for p in str(bbox).split(",")]
    if len(partes) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="bbox debe tener el formato minLon,minLat,maxLon,maxLat",
        )
    try:
        valores = tuple(float(p) for p in partes)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="bbox debe contener cuatro números",
        ) from error
    return valores  # type: ignore[return-value]
