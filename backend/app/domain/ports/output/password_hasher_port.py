from abc import ABC, abstractmethod


class PasswordHasherPort(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Genera el hash de una contraseña en texto plano."""

    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Comprueba una contraseña contra un hash almacenado."""
