from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.exceptions import ErrorTokenInvalido
from app.infrastructure.composition import CompositionRoot

esquema_bearer_jwt = HTTPBearer(
    auto_error=False,
    scheme_name="BearerJWT",
    bearerFormat="JWT",
    description="JWT obtenido en POST /api/v1/auth/login.",
)


def dependencia_agricultor_autenticado(container: CompositionRoot) -> Callable[..., str]:
    """Extrae el Bearer token de OpenAPI y lo valida con el verificador JWT existente."""

    def agricultor_autenticado(
        credenciales: HTTPAuthorizationCredentials | None = Depends(esquema_bearer_jwt),
    ) -> str:
        token = credenciales.credentials.strip() if credenciales is not None else ""
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autenticado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            identidad = container.puerto_verificador_token.verificar(token)
        except ErrorTokenInvalido as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(error),
                headers={"WWW-Authenticate": "Bearer"},
            ) from error
        return identidad.agricultor_id

    return agricultor_autenticado
