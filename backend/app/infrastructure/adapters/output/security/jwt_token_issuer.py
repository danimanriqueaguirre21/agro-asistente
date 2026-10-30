from datetime import datetime, timedelta, timezone

import jwt

from app.domain.ports.output.token_issuer_port import TokenIssuerPort


class JwtTokenIssuer(TokenIssuerPort):
    def __init__(self, secret: str, algorithm: str, expire_minutes: int) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def issue_token(self, subject: str, claims: dict[str, str]) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "email": claims.get("email", ""),
            "exp": now + timedelta(minutes=self._expire_minutes),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)
