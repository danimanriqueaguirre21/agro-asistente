from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ComandoIniciarSesionAgricultor:
    email: str
    contrasena: str


@dataclass(frozen=True)
class AgricultorAutenticado:
    id: str
    nombres: str
    apellidos: str
    email: str


@dataclass(frozen=True)
class ResultadoIniciarSesionAgricultor:
    access_token: str
    token_type: str
    agricultor: AgricultorAutenticado


class PuertoIniciarSesionAgricultor(ABC):
    @abstractmethod
    def ejecutar(
        self, comando: ComandoIniciarSesionAgricultor
    ) -> ResultadoIniciarSesionAgricultor:
        """Autentica a un agricultor y emite un token de acceso."""
