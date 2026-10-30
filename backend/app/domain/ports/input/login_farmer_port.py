from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class LoginFarmerCommand:
    email: str
    password: str


@dataclass(frozen=True)
class AuthenticatedFarmer:
    id: str
    names: str
    last_names: str
    email: str


@dataclass(frozen=True)
class LoginFarmerResult:
    access_token: str
    token_type: str
    farmer: AuthenticatedFarmer


class LoginFarmerPort(ABC):
    @abstractmethod
    def execute(self, command: LoginFarmerCommand) -> LoginFarmerResult:
        """Autentica a un agricultor y emite un token de acceso."""
