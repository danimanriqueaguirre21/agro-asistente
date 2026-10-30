"""Puente para importar ragas 0.4.x con langchain-community 0.4 (sin Vertex AI)."""

from __future__ import annotations

import sys
import types


def aplicar_compatibilidad_langchain() -> None:
    """ragas.llms.base importa ChatVertexAI/VertexAI que langchain-community 0.4 ya no exporta."""

    class ChatVertexAI:  # pragma: no cover
        """Marcador. El juez PMV1 usa Ollama u OpenAI."""

    class VertexAI:  # pragma: no cover
        """Marcador. El juez PMV1 usa Ollama u OpenAI."""

    class VertexAIModelGarden:  # pragma: no cover
        """Marcador."""

    _registrar(
        "langchain_community.chat_models.vertexai",
        ChatVertexAI=ChatVertexAI,
    )
    _registrar(
        "langchain_community.llms.vertexai",
        VertexAI=VertexAI,
        VertexAIModelGarden=VertexAIModelGarden,
    )


def _registrar(nombre: str, **attrs: object) -> None:
    existente = sys.modules.get(nombre)
    if existente is not None:
        for clave, valor in attrs.items():
            setattr(existente, clave, valor)
        return
    modulo = types.ModuleType(nombre)
    for clave, valor in attrs.items():
        setattr(modulo, clave, valor)
    sys.modules[nombre] = modulo
