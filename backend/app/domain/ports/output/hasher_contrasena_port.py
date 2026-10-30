from abc import ABC, abstractmethod


class PuertoHasherContrasena(ABC):
    @abstractmethod
    def hashear_contrasena(self, contrasena: str) -> str:
        """Genera el hash de una contraseña en texto plano."""

    @abstractmethod
    def verificar_contrasena(self, contrasena: str, hash_contrasena: str) -> bool:
        """Comprueba una contraseña contra un hash almacenado."""
