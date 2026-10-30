from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ComandoRegistrarAgricultor:
    nombres: str
    apellidos: str
    email: str
    contrasena: str


@dataclass(frozen=True)
class ResultadoRegistrarAgricultor:
    id: str
    nombres: str
    apellidos: str
    email: str


class PuertoRegistrarAgricultor(ABC):
    @abstractmethod
    def ejecutar(self, comando: ComandoRegistrarAgricultor) -> ResultadoRegistrarAgricultor:
        """Registra un agricultor y devuelve sus datos públicos."""
