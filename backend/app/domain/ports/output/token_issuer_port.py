from abc import ABC, abstractmethod


class PuertoEmisorToken(ABC):
    @abstractmethod
    def emitir_token(self, sujeto: str, claims: dict[str, str]) -> str:
        """Emite un token de acceso para el sujeto autenticado."""
