from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class RespuestaGenerada:
    texto_respuesta: str
    metodo_generacion: str


@dataclass(frozen=True)
class PasajeRecuperado:
    """Pasaje recuperado para construir la respuesta inicial. No es un LLM."""

    titulo: str
    extracto: str


class PuertoGeneracionTexto(ABC):
    """Puerto de salida para generar el texto de una respuesta agrícola.

    PMV1 usa un SLM local (Ollama) detrás de un adaptador de infraestructura.
    El dominio no conoce el proveedor concreto ni el nombre del modelo.
    """

    @abstractmethod
    def generar(
        self,
        texto_consulta: str,
        cultivo: str,
        region: str,
        pasajes: list[PasajeRecuperado] | None = None,
    ) -> RespuestaGenerada:
        """Genera una respuesta a partir de la consulta, el contexto y pasajes recuperados."""
