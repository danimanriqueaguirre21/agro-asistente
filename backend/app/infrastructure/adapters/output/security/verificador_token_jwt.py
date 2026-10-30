import jwt

from app.domain.exceptions import ErrorTokenInvalido
from app.domain.ports.output.token_verifier_port import IdentidadAutenticada, PuertoVerificadorToken


class VerificadorTokenJwt(PuertoVerificadorToken):
    def __init__(self, secret: str, algorithm: str) -> None:
        self._secret = secret
        self._algorithm = algorithm

    def verificar(self, token: str) -> IdentidadAutenticada:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=[self._algorithm],
            )
        except jwt.ExpiredSignatureError as error:
            raise ErrorTokenInvalido("No autenticado") from error
        except jwt.InvalidTokenError as error:
            raise ErrorTokenInvalido("No autenticado") from error

        agricultor_id = payload.get("sub")
        if not agricultor_id:
            raise ErrorTokenInvalido("No autenticado")
        return IdentidadAutenticada(agricultor_id=str(agricultor_id))
