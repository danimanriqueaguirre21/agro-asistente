from datetime import datetime, timedelta, timezone

import jwt

from app.domain.ports.output.token_issuer_port import PuertoEmisorToken


class EmisorTokenJwt(PuertoEmisorToken):
    def __init__(self, secret: str, algorithm: str, expire_minutes: int) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def emitir_token(self, sujeto: str, claims: dict[str, str]) -> str:
        ahora = datetime.now(timezone.utc)
        payload = {
            "sub": sujeto,
            "email": claims.get("email", ""),
            "exp": ahora + timedelta(minutes=self._expire_minutes),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)
