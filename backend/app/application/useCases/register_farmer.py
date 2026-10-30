from app.domain.entities.farmer import Farmer
from app.domain.exceptions import (
    DuplicateEmailError,
    InvalidFarmerDataError,
    InvalidPasswordError,
)
from app.domain.ports.input.register_farmer_port import (
    RegisterFarmerCommand,
    RegisterFarmerPort,
    RegisterFarmerResult,
)
from app.domain.ports.output.farmer_repository_port import FarmerRepositoryPort
from app.domain.ports.output.password_hasher_port import PasswordHasherPort
from app.domain.valueObjects.email import Email
from app.domain.valueObjects.password_hash import PasswordHash

MIN_PASSWORD_LENGTH = 8


class RegisterFarmer(RegisterFarmerPort):
    def __init__(
        self,
        farmer_repository: FarmerRepositoryPort,
        password_hasher: PasswordHasherPort,
    ) -> None:
        self._farmer_repository = farmer_repository
        self._password_hasher = password_hasher

    def execute(self, command: RegisterFarmerCommand) -> RegisterFarmerResult:
        names = (command.names or "").strip()
        last_names = (command.last_names or "").strip()
        if not names:
            raise InvalidFarmerDataError("Los nombres son obligatorios")
        if not last_names:
            raise InvalidFarmerDataError("Los apellidos son obligatorios")

        password = command.password or ""
        if not password.strip():
            raise InvalidPasswordError("La contraseña es obligatoria")
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordError("La contraseña debe tener al menos 8 caracteres")

        email = Email(command.email)
        if self._farmer_repository.exists_by_email(email):
            raise DuplicateEmailError("El correo electrónico ya está registrado")

        password_hash = PasswordHash(self._password_hasher.hash_password(password))
        farmer = Farmer.register(
            names=names,
            last_names=last_names,
            email=email,
            password_hash=password_hash,
        )
        self._farmer_repository.save(farmer)
        return RegisterFarmerResult(
            id=farmer.id,
            names=farmer.names,
            last_names=farmer.last_names,
            email=farmer.email.value,
        )
