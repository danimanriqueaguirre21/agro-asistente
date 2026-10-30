from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class IdentidadAutenticada:
    agricultor_id: str


class PuertoVerificadorToken(ABC):
    @abstractmethod
    def verificar(self, token: str) -> IdentidadAutenticada:
        """Valida un token y devuelve la identidad del agricultor."""
