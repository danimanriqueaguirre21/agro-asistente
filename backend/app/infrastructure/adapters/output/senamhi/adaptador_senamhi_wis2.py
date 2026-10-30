from collections import OrderedDict
from urllib.parse import quote

import httpx

from app.domain.entities.observacion_meteorologica import ObservacionMeteorologica
from app.domain.exceptions import ErrorObservacionesMeteorologicas
from app.domain.ports.output.puerto_observaciones_meteorologicas import (
    FiltroObservacionesMeteorologicas,
    PuertoObservacionesMeteorologicas,
)

VARIABLE_TEMPERATURA = "air_temperature"
VARIABLE_PUNTO_ROCIO = "dewpoint_temperature"
VARIABLE_PRECIPITACION = "total_precipitation_or_total_water_equivalent"
MENSAJE_ERROR = "No se pudieron obtener las observaciones meteorológicas."


class AdaptadorSenamhiWis2(PuertoObservacionesMeteorologicas):
    """Adaptador HTTP GET hacia el API OGC de SENAMHI WIS2. El dominio no importa este módulo."""

    def __init__(
        self,
        base_url: str,
        coleccion: str,
        timeout_seconds: int = 20,
        cliente_http: object | None = None,
    ) -> None:
        self._base_url = (base_url or "").rstrip("/")
        self._coleccion = (coleccion or "").strip()
        self._timeout_seconds = timeout_seconds
        self._cliente = cliente_http

    def obtener_recientes(
        self, filtro: FiltroObservacionesMeteorologicas | None = None
    ) -> list[ObservacionMeteorologica]:
        criterio = filtro or FiltroObservacionesMeteorologicas()
        if not self._base_url or not self._coleccion:
            raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)
        try:
            respuesta_http = self._get(criterio)
        except httpx.TimeoutException as error:
            raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR) from error
        except httpx.RequestError as error:
            raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR) from error
        return _observaciones_desde_respuesta(respuesta_http)

    def _get(self, criterio: FiltroObservacionesMeteorologicas) -> object:
        coleccion = quote(self._coleccion, safe="")
        url = f"{self._base_url}/collections/{coleccion}/items"
        parametros = _parametros_http(criterio)
        if self._cliente is not None:
            return self._cliente.get(url, params=parametros, timeout=self._timeout_seconds)
        with httpx.Client(timeout=self._timeout_seconds) as cliente:
            return cliente.get(url, params=parametros)


def _parametros_http(criterio: FiltroObservacionesMeteorologicas) -> dict[str, str | int]:
    limite = criterio.limite if criterio.limite and criterio.limite > 0 else 10
    parametros: dict[str, str | int] = {
        "f": "json",
        "limit": limite,
        "sortby": (criterio.orden or "").strip() or "-reportTime",
    }
    if criterio.fecha_hora and criterio.fecha_hora.strip():
        parametros["datetime"] = criterio.fecha_hora.strip()
    if criterio.caja_geografica is not None:
        if len(criterio.caja_geografica) != 4:
            raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)
        parametros["bbox"] = ",".join(str(valor) for valor in criterio.caja_geografica)
    if criterio.identificador_estacion and criterio.identificador_estacion.strip():
        parametros["wigos_station_identifier"] = criterio.identificador_estacion.strip()
    if criterio.nombre_variable and criterio.nombre_variable.strip():
        parametros["name"] = criterio.nombre_variable.strip()
    return parametros


def _observaciones_desde_respuesta(respuesta_http: object) -> list[ObservacionMeteorologica]:
    status_code = int(getattr(respuesta_http, "status_code", 0) or 0)
    if status_code >= 400:
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)

    cuerpo = _json_seguro(respuesta_http)
    if not isinstance(cuerpo, dict):
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)
    if "features" not in cuerpo:
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)
    features = cuerpo.get("features")
    if features is None:
        return []
    if not isinstance(features, list):
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)

    agrupadas: OrderedDict[str, dict[str, object]] = OrderedDict()
    for feature in features:
        _incorporar_feature(agrupadas, feature)
    return [_a_observacion(item) for item in agrupadas.values()]


def _incorporar_feature(agrupadas: OrderedDict[str, dict[str, object]], feature: object) -> None:
    if not isinstance(feature, dict):
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)
    properties = feature.get("properties")
    if properties is None:
        properties = {}
    if not isinstance(properties, dict):
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)

    identificador = _texto(properties.get("wigos_station_identifier"))
    fecha_hora = _texto(properties.get("reportTime") or properties.get("phenomenonTime"))
    report_id = _texto(properties.get("reportId"))
    clave = report_id or "|".join(part for part in (identificador, fecha_hora) if part)
    if not clave:
        return

    registro = agrupadas.get(clave)
    if registro is None:
        latitud, longitud, altitud = _coordenadas(feature.get("geometry"))
        registro = {
            "identificador_estacion": identificador,
            "nombre_estacion": None,
            "latitud": latitud,
            "longitud": longitud,
            "altitud": altitud,
            "fecha_hora": fecha_hora,
            "temperatura": None,
            "punto_rocio": None,
            "precipitacion": None,
        }
        agrupadas[clave] = registro
    else:
        if not registro["identificador_estacion"] and identificador:
            registro["identificador_estacion"] = identificador
        if not registro["fecha_hora"] and fecha_hora:
            registro["fecha_hora"] = fecha_hora
        if registro["latitud"] is None or registro["longitud"] is None:
            latitud, longitud, altitud = _coordenadas(feature.get("geometry"))
            if latitud is not None:
                registro["latitud"] = latitud
            if longitud is not None:
                registro["longitud"] = longitud
            if altitud is not None:
                registro["altitud"] = altitud

    variable = _texto(properties.get("name"))
    valor = _numero(properties.get("value"))
    if variable == VARIABLE_TEMPERATURA:
        registro["temperatura"] = valor
    elif variable == VARIABLE_PUNTO_ROCIO:
        registro["punto_rocio"] = valor
    elif variable == VARIABLE_PRECIPITACION:
        registro["precipitacion"] = valor


def _a_observacion(registro: dict[str, object]) -> ObservacionMeteorologica:
    identificador = str(registro.get("identificador_estacion") or "").strip()
    if not identificador:
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)
    return ObservacionMeteorologica(
        identificador_estacion=identificador,
        nombre_estacion=None,
        latitud=_opcional_float(registro.get("latitud")),
        longitud=_opcional_float(registro.get("longitud")),
        altitud=_opcional_float(registro.get("altitud")),
        fecha_hora=_texto(registro.get("fecha_hora")) or None,
        temperatura=_opcional_float(registro.get("temperatura")),
        punto_rocio=_opcional_float(registro.get("punto_rocio")),
        precipitacion=_opcional_float(registro.get("precipitacion")),
    )


def _coordenadas(geometry: object) -> tuple[float | None, float | None, float | None]:
    if geometry is None:
        return None, None, None
    if not isinstance(geometry, dict):
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)
    coordinates = geometry.get("coordinates")
    if coordinates is None:
        return None, None, None
    if not isinstance(coordinates, list) or len(coordinates) < 2:
        return None, None, None
    longitud = _numero(coordinates[0])
    latitud = _numero(coordinates[1])
    altitud = _numero(coordinates[2]) if len(coordinates) > 2 else None
    return latitud, longitud, altitud


def _json_seguro(respuesta_http: object) -> object:
    lector = getattr(respuesta_http, "json", None)
    if not callable(lector):
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR)
    try:
        return lector()
    except (ValueError, TypeError) as error:
        raise ErrorObservacionesMeteorologicas(MENSAJE_ERROR) from error


def _texto(valor: object) -> str:
    if valor is None:
        return ""
    return str(valor).strip()


def _numero(valor: object) -> float | None:
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        limpio = valor.strip()
        if not limpio:
            return None
        try:
            return float(limpio)
        except ValueError:
            return None
    return None


def _opcional_float(valor: object) -> float | None:
    if valor is None:
        return None
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return float(valor)
    return None
