from pathlib import Path

import httpx
import pytest

from app.domain.exceptions import ErrorObservacionesMeteorologicas
from app.domain.ports.output.puerto_observaciones_meteorologicas import (
    FiltroObservacionesMeteorologicas,
    PuertoObservacionesMeteorologicas,
)
from app.infrastructure.adapters.output.senamhi.adaptador_senamhi_wis2 import (
    AdaptadorSenamhiWis2,
)
from app.infrastructure.composition import CompositionRoot
from app.infrastructure.config.settings import Settings


class _RespuestaFalsa:
    def __init__(self, status_code: int, payload: object) -> None:
        self.status_code = status_code
        self._payload = payload
        self._invalid_json = isinstance(payload, Exception)

    def json(self) -> object:
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


class _ClienteFalso:
    def __init__(self, respuesta: _RespuestaFalsa | Exception) -> None:
        self._respuesta = respuesta
        self.llamadas: list[tuple[str, dict[str, object], int | None]] = []

    def get(
        self, url: str, params: dict[str, object] | None = None, timeout: int | None = None
    ) -> _RespuestaFalsa:
        self.llamadas.append((url, params or {}, timeout))
        if isinstance(self._respuesta, Exception):
            raise self._respuesta
        return self._respuesta


def _feature(
    *,
    station: str = "0-604-1-18470502",
    report_id: str = "0-604-1-18470502-202606210500",
    report_time: str = "2026-06-21T05:00:00Z",
    name: str = "air_temperature",
    value: object = 2.85,
    geometry: object = {"type": "Point", "coordinates": [-75.06186, -11.92717, 4649.5]},
    feature_id: str = "feat-1",
) -> dict[str, object]:
    return {
        "type": "Feature",
        "id": feature_id,
        "geometry": geometry,
        "properties": {
            "name": name,
            "value": value,
            "reportTime": report_time,
            "phenomenonTime": report_time,
            "reportId": report_id,
            "wigos_station_identifier": station,
            "units": "Celsius",
        },
    }


def _geojson(*features: dict[str, object]) -> dict[str, object]:
    return {"type": "FeatureCollection", "features": list(features)}


def _adaptador(cliente: _ClienteFalso) -> AdaptadorSenamhiWis2:
    return AdaptadorSenamhiWis2(
        base_url="https://wis.senamhi.gob.pe/oapi",
        coleccion="urn:wmo:md:pe-senamhi:synop-hourly",
        timeout_seconds=8,
        cliente_http=cliente,
    )


def test_respuesta_valida_agrupa_variables_en_modelo_interno() -> None:
    payload = _geojson(
        _feature(name="air_temperature", value=2.85, feature_id="t"),
        _feature(name="dewpoint_temperature", value=-16.35, feature_id="d"),
        _feature(
            name="total_precipitation_or_total_water_equivalent",
            value=0.0,
            feature_id="p",
        ),
    )
    cliente = _ClienteFalso(_RespuestaFalsa(200, payload))
    observaciones = _adaptador(cliente).obtener_recientes(
        FiltroObservacionesMeteorologicas(limite=7, orden="-reportTime")
    )

    assert len(observaciones) == 1
    item = observaciones[0]
    assert item.identificador_estacion == "0-604-1-18470502"
    assert item.nombre_estacion is None
    assert item.latitud == -11.92717
    assert item.longitud == -75.06186
    assert item.altitud == 4649.5
    assert item.fecha_hora == "2026-06-21T05:00:00Z"
    assert item.temperatura == 2.85
    assert item.punto_rocio == -16.35
    assert item.precipitacion == 0.0

    url, params, timeout = cliente.llamadas[0]
    assert timeout == 8
    assert url.endswith("/collections/urn%3Awmo%3Amd%3Ape-senamhi%3Asynop-hourly/items")
    assert params["f"] == "json"
    assert params["limit"] == 7
    assert params["sortby"] == "-reportTime"


def test_sin_features_devuelve_lista_vacia() -> None:
    cliente = _ClienteFalso(_RespuestaFalsa(200, {"type": "FeatureCollection", "features": []}))
    assert _adaptador(cliente).obtener_recientes() == []


def test_feature_sin_geometry_no_inventa_coordenadas() -> None:
    cliente = _ClienteFalso(
        _RespuestaFalsa(200, _geojson(_feature(geometry=None, value=10.2)))
    )
    item = _adaptador(cliente).obtener_recientes()[0]
    assert item.latitud is None
    assert item.longitud is None
    assert item.altitud is None
    assert item.temperatura == 10.2


def test_feature_sin_temperatura_deja_none() -> None:
    cliente = _ClienteFalso(
        _RespuestaFalsa(
            200,
            _geojson(
                _feature(
                    name="total_precipitation_or_total_water_equivalent",
                    value=1.5,
                )
            ),
        )
    )
    item = _adaptador(cliente).obtener_recientes()[0]
    assert item.temperatura is None
    assert item.precipitacion == 1.5


def test_feature_sin_precipitacion_deja_none() -> None:
    cliente = _ClienteFalso(
        _RespuestaFalsa(200, _geojson(_feature(name="air_temperature", value=8.1)))
    )
    item = _adaptador(cliente).obtener_recientes()[0]
    assert item.precipitacion is None
    assert item.temperatura == 8.1


def test_valores_nulos_no_se_inventan() -> None:
    cliente = _ClienteFalso(
        _RespuestaFalsa(200, _geojson(_feature(name="air_temperature", value=None)))
    )
    item = _adaptador(cliente).obtener_recientes()[0]
    assert item.temperatura is None
    assert item.punto_rocio is None
    assert item.precipitacion is None


def test_error_http_es_controlado() -> None:
    cliente = _ClienteFalso(_RespuestaFalsa(503, {"code": "error"}))
    with pytest.raises(ErrorObservacionesMeteorologicas, match="observaciones meteorológicas"):
        _adaptador(cliente).obtener_recientes()


def test_timeout_es_controlado() -> None:
    request = httpx.Request("GET", "https://wis.senamhi.gob.pe/oapi/collections/x/items")
    cliente = _ClienteFalso(httpx.TimeoutException("timed out", request=request))
    with pytest.raises(ErrorObservacionesMeteorologicas, match="observaciones meteorológicas"):
        _adaptador(cliente).obtener_recientes()


def test_json_invalido_es_controlado() -> None:
    cliente = _ClienteFalso(_RespuestaFalsa(200, ValueError("invalid json")))
    with pytest.raises(ErrorObservacionesMeteorologicas, match="observaciones meteorológicas"):
        _adaptador(cliente).obtener_recientes()


def test_conversion_envia_parametros_del_filtro() -> None:
    cliente = _ClienteFalso(_RespuestaFalsa(200, _geojson()))
    _adaptador(cliente).obtener_recientes(
        FiltroObservacionesMeteorologicas(
            limite=3,
            fecha_hora="2026-09-21T00:00:00Z/2026-09-21T03:00:00Z",
            caja_geografica=(-76.5, -13.0, -73.8, -10.8),
            identificador_estacion="0-604-1-18470502",
            nombre_variable="air_temperature",
            orden="-reportTime",
        )
    )
    _url, params, _timeout = cliente.llamadas[0]
    assert params["datetime"] == "2026-09-21T00:00:00Z/2026-09-21T03:00:00Z"
    assert params["bbox"] == "-76.5,-13.0,-73.8,-10.8"
    assert params["wigos_station_identifier"] == "0-604-1-18470502"
    assert params["name"] == "air_temperature"


def test_dominio_del_puerto_no_conoce_proveedor() -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "domain"
        / "ports"
        / "output"
        / "puerto_observaciones_meteorologicas.py"
    ).read_text(encoding="utf-8").lower()
    assert "httpx" not in source
    assert "wis2" not in source
    assert "ogc" not in source
    assert "senamhi.gob.pe" not in source


def test_composition_expone_puerto_meteorologico() -> None:
    container = CompositionRoot(Settings(_env_file=None))
    assert isinstance(container.puerto_observaciones_meteorologicas, PuertoObservacionesMeteorologicas)
    assert isinstance(container.puerto_observaciones_meteorologicas, AdaptadorSenamhiWis2)
