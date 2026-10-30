from datetime import datetime, timezone
from uuid import uuid4

from app.domain.exceptions import InvalidFarmerDataError
from app.domain.valueObjects.email import Email
from app.domain.valueObjects.password_hash import PasswordHash


class Farmer:
    def __init__(
        self,
        farmer_id: str,
        names: str,
        last_names: str,
        email: Email,
        password_hash: PasswordHash,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.id = farmer_id
        self.names = names
        self.last_names = last_names
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def register(
        cls,
        names: str,
        last_names: str,
        email: Email,
        password_hash: PasswordHash,
    ) -> "Farmer":
        clean_names = (names or "").strip()
        clean_last_names = (last_names or "").strip()
        if not clean_names:
            raise InvalidFarmerDataError("Los nombres son obligatorios")
        if not clean_last_names:
            raise InvalidFarmerDataError("Los apellidos son obligatorios")
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        full_name = f"{clean_names} {clean_last_names}".strip()
        if len(full_name) > 120:
            raise InvalidFarmerDataError("El nombre completo supera la longitud permitida")
        return cls(
            farmer_id=str(uuid4()),
            names=clean_names,
            last_names=clean_last_names,
            email=email,
            password_hash=password_hash,
            created_at=now,
            updated_at=now,
        )

    @property
    def full_name(self) -> str:
        return f"{self.names} {self.last_names}".strip()
