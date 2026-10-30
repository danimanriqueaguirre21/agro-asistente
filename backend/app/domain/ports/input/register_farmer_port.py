from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterFarmerCommand:
    names: str
    last_names: str
    email: str
    password: str


@dataclass(frozen=True)
class RegisterFarmerResult:
    id: str
    names: str
    last_names: str
    email: str


class RegisterFarmerPort(ABC):
    @abstractmethod
    def execute(self, command: RegisterFarmerCommand) -> RegisterFarmerResult:
        """Registra un agricultor y devuelve sus datos públicos."""
