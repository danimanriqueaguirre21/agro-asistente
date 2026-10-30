from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.ports.input.incorporar_conocimiento_port import ResultadoDocumentoConocimiento


@dataclass(frozen=True)
class ResultadoIndexarConocimiento:
    documentos_indexados: int
    total_fragmentos: int
    documentos: tuple[ResultadoDocumentoConocimiento, ...]


class PuertoIndexarConocimiento(ABC):
    @abstractmethod
    def ejecutar(self) -> ResultadoIndexarConocimiento:
        """Indexa los documentos de conocimiento registrados para la recuperación RAG."""
