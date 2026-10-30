from fastapi.testclient import TestClient

from app.domain.exceptions import ErrorObservacionesMeteorologicas
from app.domain.ports.input.obtener_observaciones_meteorologicas_port import (
    ResultadoObservacionMeteorologica,
)
from app import main as main_module


class _PuertoFalso:
    def __init__(self, resultado=None, error: Exception | None = None) -> None:
        self._resultado = resultado or []
        self._error = error
        self.comandos = []

    def ejecutar(self, comando):
        self.comandos.append(comando)
        if self._error is not None:
            raise self._error
        return self._resultado


def test_weather_observations_endpoint_normaliza_respuesta() -> None:
    falso = _PuertoFalso(
        [
            ResultadoObservacionMeteorologica(
                identificador_estacion="0-604-1-18470502",
                nombre_estacion=None,
                latitud=-11.9,
                longitud=-75.0,
                altitud=4600.0,
                fecha_hora="2026-06-21T05:00:00Z",
                temperatura=2.85,
                punto_rocio=-16.35,
                precipitacion=0.0,
            )
        ]
    )
    original = main_module.container.puerto_obtener_observaciones_meteorologicas
    main_module.container.puerto_obtener_observaciones_meteorologicas = falso
    try:
        client = TestClient(main_module.app)
        response = client.get("/api/v1/weather/observations?limit=3")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 1
        assert payload[0]["station_id"] == "0-604-1-18470502"
        assert payload[0]["air_temperature"] == 2.85
        assert payload[0]["station_name"] is None
        assert payload[0]["dewpoint_temperature"] == -16.35
        assert payload[0]["precipitation"] == 0.0
        assert falso.comandos[0].limite == 3
    finally:
        main_module.container.puerto_obtener_observaciones_meteorologicas = original


def test_weather_observations_endpoint_503_si_proveedor_falla() -> None:
    falso = _PuertoFalso(
        error=ErrorObservacionesMeteorologicas(
            "No se pudieron obtener las observaciones meteorológicas."
        )
    )
    original = main_module.container.puerto_obtener_observaciones_meteorologicas
    main_module.container.puerto_obtener_observaciones_meteorologicas = falso
    try:
        client = TestClient(main_module.app)
        response = client.get("/api/v1/weather/observations")
        assert response.status_code == 503
        assert "observaciones meteorológicas" in response.json()["detail"]
    finally:
        main_module.container.puerto_obtener_observaciones_meteorologicas = original


def test_weather_bbox_invalido_devuelve_400() -> None:
    client = TestClient(main_module.app)
    response = client.get("/api/v1/weather/observations?bbox=1,2,3")
    assert response.status_code == 400
    assert "bbox" in response.json()["detail"]
