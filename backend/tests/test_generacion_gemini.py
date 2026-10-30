import httpx
import pytest

from app.domain.exceptions import ErrorGeneracionTexto
from app.infrastructure.adapters.output.generation.adaptador_generacion_gemini import (
    AdaptadorGeneracionGemini,
)
from app.infrastructure.composition import CompositionRoot
from app.infrastructure.config.settings import Settings
from app.domain.ports.output.text_generation_port import PasajeRecuperado


class _RespuestaFalsa:
    def __init__(self, status_code: int, payload: dict[str, object]) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict[str, object]:
        return self._payload


class _ClienteFalso:
    def __init__(self, respuesta: _RespuestaFalsa | Exception) -> None:
        self._respuesta = respuesta
        self.llamadas: list[tuple[str, dict[str, object], dict[str, str]]] = []

    def post(
        self,
        url: str,
        json: dict[str, object],
        headers: dict[str, str] | None = None,
        timeout: int | None = None,
    ) -> _RespuestaFalsa:
        self.llamadas.append((url, json, headers or {}))
        if isinstance(self._respuesta, Exception):
            raise self._respuesta
        return self._respuesta


def _adaptador(cliente: _ClienteFalso, modelo: str = "gemini-2.5-flash") -> AdaptadorGeneracionGemini:
    return AdaptadorGeneracionGemini(
        api_key="clave-de-prueba",
        model=modelo,
        timeout_seconds=5,
        cliente_http=cliente,
    )


def _cuerpo_gemini(texto: str) -> dict[str, object]:
    return {"candidates": [{"content": {"parts": [{"text": texto}]}}]}


def test_gemini_devuelve_el_texto_con_metodo_gemini() -> None:
    cliente = _ClienteFalso(_RespuestaFalsa(200, _cuerpo_gemini("Riega sin encharcar.")))
    generado = _adaptador(cliente).generar(
        "¿Cómo riego la papa?",
        "papa",
        "Huancayo",
        pasajes=[PasajeRecuperado(titulo="Riego", extracto="Riegos frecuentes en floración.")],
    )
    assert generado.metodo_generacion == "gemini"
    assert "encharcar" in generado.texto_respuesta
    url, payload, cabeceras = cliente.llamadas[0]
    assert url.endswith("/models/gemini-2.5-flash:generateContent")
    assert cabeceras["x-goog-api-key"] == "clave-de-prueba"
    assert "papa" in str(payload["contents"])
    assert "Junín" in str(payload["systemInstruction"])


def test_gemini_sin_clave_no_llama_al_servicio() -> None:
    cliente = _ClienteFalso(_RespuestaFalsa(200, _cuerpo_gemini("no debe usarse")))
    adaptador = AdaptadorGeneracionGemini(api_key="", model="gemini-2.5-flash", cliente_http=cliente)
    with pytest.raises(ErrorGeneracionTexto, match="GEMINI_API_KEY"):
        adaptador.generar("¿Cómo riego?", "papa", "Huancayo")
    assert cliente.llamadas == []


def test_gemini_modelo_ausente_es_error_controlado() -> None:
    cliente = _ClienteFalso(
        _RespuestaFalsa(404, {"error": {"message": "models/otro is not found"}})
    )
    with pytest.raises(ErrorGeneracionTexto, match="no está disponible"):
        _adaptador(cliente, modelo="otro").generar("¿Cómo riego?", "papa", "Huancayo")


def test_gemini_error_http_no_incluye_la_clave() -> None:
    cliente = _ClienteFalso(_RespuestaFalsa(400, {"error": {"message": "API key not valid"}}))
    with pytest.raises(ErrorGeneracionTexto, match="API key not valid") as error:
        _adaptador(cliente).generar("¿Cómo riego?", "papa", "Huancayo")
    assert "clave-de-prueba" not in str(error.value)


def test_gemini_respuesta_vacia_es_error_controlado() -> None:
    cliente = _ClienteFalso(_RespuestaFalsa(200, _cuerpo_gemini("  ")))
    with pytest.raises(ErrorGeneracionTexto, match="vacío"):
        _adaptador(cliente).generar("¿Cómo riego?", "papa", "Huancayo")


def test_gemini_sin_conexion_es_error_controlado() -> None:
    request = httpx.Request("POST", "https://generativelanguage.googleapis.com")
    cliente = _ClienteFalso(httpx.ConnectError("connection refused", request=request))
    with pytest.raises(ErrorGeneracionTexto, match="no está disponible"):
        _adaptador(cliente).generar("¿Cómo riego?", "papa", "Huancayo")


def test_composicion_usa_gemini_cuando_el_proveedor_es_gemini() -> None:
    settings = Settings(
        _env_file=None,
        generation_provider="gemini",
        gemini_api_key="clave-de-prueba",
        gemini_model="gemini-2.5-flash",
    )
    contenedor = CompositionRoot(settings)
    adaptador = contenedor.puerto_generacion_texto
    assert isinstance(adaptador, AdaptadorGeneracionGemini)
    assert adaptador._model == "gemini-2.5-flash"
