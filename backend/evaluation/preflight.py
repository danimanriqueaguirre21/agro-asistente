from __future__ import annotations

import os

import httpx

from app.infrastructure.config.settings import Settings


class EvaluacionOficialNoEjecutable(RuntimeError):
    """Falta un requisito para la línea base oficial (no se sustituye por plantilla)."""


def exigir_proveedor_ollama(settings: Settings) -> None:
    proveedor = (settings.generation_provider or "").strip().lower()
    if proveedor != "ollama":
        raise EvaluacionOficialNoEjecutable(
            "EVALUACIÓN OFICIAL DETENIDA: GENERATION_PROVIDER debe ser 'ollama'. "
            f"Valor actual: {settings.generation_provider!r}. "
            "No se utiliza template para la línea base RAGAS."
        )
    if not (settings.ollama_base_url or "").strip():
        raise EvaluacionOficialNoEjecutable(
            "EVALUACIÓN OFICIAL DETENIDA: falta OLLAMA_BASE_URL."
        )
    if not (settings.ollama_model or "").strip():
        raise EvaluacionOficialNoEjecutable(
            "EVALUACIÓN OFICIAL DETENIDA: falta OLLAMA_MODEL."
        )


def exigir_ollama_disponible(settings: Settings, cliente_http: object | None = None) -> dict[str, object]:
    exigir_proveedor_ollama(settings)
    base = settings.ollama_base_url.rstrip("/")
    url = f"{base}/api/tags"
    try:
        if cliente_http is not None:
            respuesta = cliente_http.get(url, timeout=5)
        else:
            respuesta = httpx.get(url, timeout=5)
    except httpx.HTTPError as error:
        raise EvaluacionOficialNoEjecutable(
            "EVALUACIÓN OFICIAL DETENIDA: Ollama no está disponible. "
            f"No se pudo contactar {url}. Arranque Ollama y no use template."
        ) from error

    status_code = int(getattr(respuesta, "status_code", 0) or 0)
    if status_code >= 400:
        raise EvaluacionOficialNoEjecutable(
            f"EVALUACIÓN OFICIAL DETENIDA: Ollama respondió HTTP {status_code} en /api/tags."
        )
    payload = _json(respuesta)
    modelos = _nombres_modelo(payload)
    esperado = settings.ollama_model.strip()
    if esperado not in modelos:
        raise EvaluacionOficialNoEjecutable(
            "EVALUACIÓN OFICIAL DETENIDA: el modelo configurado no está instalado en Ollama. "
            f"OLLAMA_MODEL={esperado}. Instálelo con `ollama pull {esperado}`."
        )
    return {"models": modelos, "selected": esperado}


def proveedor_juez_ragas() -> str:
    return (os.environ.get("RAGAS_LLM_PROVIDER") or "ollama").strip().lower()


def _json(respuesta: object) -> object:
    lector = getattr(respuesta, "json", None)
    if not callable(lector):
        return {}
    try:
        return lector()
    except ValueError:
        return {}


def _nombres_modelo(payload: object) -> set[str]:
    if not isinstance(payload, dict):
        return set()
    nombres: set[str] = set()
    for item in payload.get("models") or []:
        if isinstance(item, dict):
            nombre = str(item.get("name") or item.get("model") or "").strip()
            if nombre:
                nombres.add(nombre)
    return nombres
