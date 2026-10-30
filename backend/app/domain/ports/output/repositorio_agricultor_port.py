from abc import ABC, abstractmethod

from app.domain.entities.agricultor import Agricultor
from app.domain.valueObjects.email import Email


class PuertoRepositorioAgricultor(ABC):
    @abstractmethod
    def existe_por_correo(self, email: Email) -> bool:
        """Indica si ya existe un agricultor con el correo dado."""

    @abstractmethod
    def buscar_por_correo(self, email: Email) -> Agricultor | None:
        """Busca un agricultor por correo. None si no existe."""

    @abstractmethod
    def guardar(self, agricultor: Agricultor) -> None:
        """Persiste un agricultor nuevo."""
