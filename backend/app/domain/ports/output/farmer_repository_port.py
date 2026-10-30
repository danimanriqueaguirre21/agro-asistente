from abc import ABC, abstractmethod

from app.domain.entities.farmer import Farmer
from app.domain.valueObjects.email import Email


class FarmerRepositoryPort(ABC):
    @abstractmethod
    def exists_by_email(self, email: Email) -> bool:
        """Indica si ya existe un agricultor con el correo dado."""

    @abstractmethod
    def find_by_email(self, email: Email) -> Farmer | None:
        """Busca un agricultor por correo. None si no existe."""

    @abstractmethod
    def save(self, farmer: Farmer) -> None:
        """Persiste un agricultor nuevo."""
