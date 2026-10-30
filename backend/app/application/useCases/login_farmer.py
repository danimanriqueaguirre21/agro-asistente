from app.domain.exceptions import InvalidCredentialsError, InvalidEmailError
from app.domain.ports.input.login_farmer_port import (
    AuthenticatedFarmer,
    LoginFarmerCommand,
    LoginFarmerPort,
    LoginFarmerResult,
)
from app.domain.ports.output.farmer_repository_port import FarmerRepositoryPort
from app.domain.ports.output.password_hasher_port import PasswordHasherPort
from app.domain.ports.output.token_issuer_port import TokenIssuerPort
from app.domain.valueObjects.email import Email

INVALID_CREDENTIALS = "Credenciales inválidas"


class LoginFarmer(LoginFarmerPort):
    def __init__(
        self,
        farmer_repository: FarmerRepositoryPort,
        password_hasher: PasswordHasherPort,
        token_issuer: TokenIssuerPort,
    ) -> None:
        self._farmer_repository = farmer_repository
        self._password_hasher = password_hasher
        self._token_issuer = token_issuer

    def execute(self, command: LoginFarmerCommand) -> LoginFarmerResult:
        password = command.password or ""
        if not password.strip():
            raise InvalidCredentialsError(INVALID_CREDENTIALS)

        try:
            email = Email(command.email)
        except InvalidEmailError:
            raise

        farmer = self._farmer_repository.find_by_email(email)
        if farmer is None:
            raise InvalidCredentialsError(INVALID_CREDENTIALS)

        if not self._password_hasher.verify_password(password, farmer.password_hash.value):
            raise InvalidCredentialsError(INVALID_CREDENTIALS)

        access_token = self._token_issuer.issue_token(
            subject=farmer.id,
            claims={"email": farmer.email.value},
        )
        return LoginFarmerResult(
            access_token=access_token,
            token_type="bearer",
            farmer=AuthenticatedFarmer(
                id=farmer.id,
                names=farmer.names,
                last_names=farmer.last_names,
                email=farmer.email.value,
            ),
        )
