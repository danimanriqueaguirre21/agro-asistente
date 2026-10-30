import jwt

from app.domain.exceptions import InvalidTokenError
from app.domain.ports.output.token_verifier_port import AuthenticatedIdentity, TokenVerifierPort


class JwtTokenVerifier(TokenVerifierPort):
    def __init__(self, secret: str, algorithm: str) -> None:
        self._secret = secret
        self._algorithm = algorithm

    def verify(self, token: str) -> AuthenticatedIdentity:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=[self._algorithm],
            )
        except jwt.ExpiredSignatureError as error:
            raise InvalidTokenError("No autenticado") from error
        except jwt.InvalidTokenError as error:
            raise InvalidTokenError("No autenticado") from error

        farmer_id = payload.get("sub")
        if not farmer_id:
            raise InvalidTokenError("No autenticado")
        return AuthenticatedIdentity(farmer_id=str(farmer_id))
