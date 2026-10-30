import httpx

from app.domain.exceptions import ErrorGeneracionTexto
from app.domain.ports.output.text_generation_port import (
    PasajeRecuperado,
    PuertoGeneracionTexto,
    RespuestaGenerada,
)
from app.infrastructure.adapters.output.generation.adaptador_generacion_ollama import (
    INSTRUCCION_SISTEMA,
    construir_prompt_agricola,
)


class AdaptadorGeneracionGemini(PuertoGeneracionTexto):
    """Adaptador hacia la API de Gemini. El dominio no conoce este proveedor."""

    METHOD = "gemini"

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        timeout_seconds: int = 60,
        cliente_http: object | None = None,
    ) -> None:
        self._api_key = (api_key or "").strip()
        self._model = (model or "").strip()
        self._base_url = (base_url or "").rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._cliente = cliente_http

    def generar(
        self,
        texto_consulta: str,
        cultivo: str,
        region: str,
        pasajes: list[PasajeRecuperado] | None = None,
    ) -> RespuestaGenerada:
        if not self._api_key:
            raise ErrorGeneracionTexto(
                "No se pudo generar la respuesta: falta la clave de Gemini (GEMINI_API_KEY)."
            )
        if not self._model:
            raise ErrorGeneracionTexto(
                "No se pudo generar la respuesta: falta el modelo de Gemini (GEMINI_MODEL)."
            )
        if not self._base_url:
            raise ErrorGeneracionTexto(
                "No se pudo generar la respuesta: falta la URL de Gemini (GEMINI_BASE_URL)."
            )

        prompt = construir_prompt_agricola(texto_consulta, cultivo, region, pasajes)
        payload = {
            "systemInstruction": {"parts": [{"text": INSTRUCCION_SISTEMA}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }
        try:
            respuesta_http = self._post(payload)
        except httpx.TimeoutException as error:
            raise ErrorGeneracionTexto(
                "No se pudo generar la respuesta: Gemini excedió el tiempo de espera."
            ) from error
        except httpx.RequestError as error:
            raise ErrorGeneracionTexto(
                "No se pudo generar la respuesta: Gemini no está disponible."
            ) from error

        return RespuestaGenerada(
            texto_respuesta=_texto_desde_respuesta(respuesta_http, self._model),
            metodo_generacion=self.METHOD,
        )

    def _post(self, payload: dict[str, object]) -> object:
        url = f"{self._base_url}/models/{self._model}:generateContent"
        cabeceras = {"x-goog-api-key": self._api_key}
        if self._cliente is not None:
            return self._cliente.post(
                url,
                json=payload,
                headers=cabeceras,
                timeout=self._timeout_seconds,
            )
        with httpx.Client(timeout=self._timeout_seconds) as cliente:
            return cliente.post(url, json=payload, headers=cabeceras)


def _texto_desde_respuesta(respuesta_http: object, modelo: str) -> str:
    status_code = int(getattr(respuesta_http, "status_code", 0) or 0)
    cuerpo, json_valido = _json_intento(respuesta_http)
    if status_code >= 400:
        detalle = _detalle_error(cuerpo) or f"el servicio respondió HTTP {status_code}"
        if status_code == 404 or "not found" in detalle.lower() or "modelo" in detalle.lower():
            raise ErrorGeneracionTexto(
                f"No se pudo generar la respuesta: el modelo '{modelo}' no está disponible en Gemini."
            )
        raise ErrorGeneracionTexto(f"No se pudo generar la respuesta: {detalle}.")
    if not json_valido or not isinstance(cuerpo, dict):
        raise ErrorGeneracionTexto(
            "No se pudo generar la respuesta: Gemini devolvió un formato inválido."
        )
    texto = _extraer_texto(cuerpo)
    if not texto:
        raise ErrorGeneracionTexto(
            "No se pudo generar la respuesta: Gemini devolvió un texto vacío."
        )
    return texto


def _detalle_error(cuerpo: object) -> str:
    if not isinstance(cuerpo, dict):
        return ""
    error = cuerpo.get("error")
    if isinstance(error, dict):
        return str(error.get("message") or "").strip()
    if isinstance(error, str):
        return error.strip()
    return ""


def _extraer_texto(cuerpo: dict[str, object]) -> str:
    candidatos = cuerpo.get("candidates")
    if not isinstance(candidatos, list) or not candidatos:
        return ""
    primero = candidatos[0]
    if not isinstance(primero, dict):
        return ""
    contenido = primero.get("content")
    if not isinstance(contenido, dict):
        return ""
    partes = contenido.get("parts")
    if not isinstance(partes, list):
        return ""
    textos = [
        str(parte.get("text") or "").strip()
        for parte in partes
        if isinstance(parte, dict) and str(parte.get("text") or "").strip()
    ]
    return "\n".join(textos).strip()


def _json_intento(respuesta_http: object) -> tuple[object, bool]:
    lector = getattr(respuesta_http, "json", None)
    if not callable(lector):
        return {}, False
    try:
        return lector(), True
    except (TypeError, ValueError):
        return {}, False
