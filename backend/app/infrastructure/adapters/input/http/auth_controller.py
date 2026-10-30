from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.domain.exceptions import (
    ErrorContrasenaInvalida,
    ErrorCorreoDuplicado,
    ErrorCorreoInvalido,
    ErrorCredencialesInvalidas,
    ErrorDatosAgricultorInvalidos,
    ErrorDominio,
)
from app.domain.ports.input.iniciar_sesion_agricultor_port import ComandoIniciarSesionAgricultor
from app.domain.ports.input.registrar_agricultor_port import ComandoRegistrarAgricultor
from app.infrastructure.composition import CompositionRoot


class RegisterFarmerRequest(BaseModel):
    names: str = Field(min_length=1)
    last_names: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class RegisterFarmerResponse(BaseModel):
    id: str
    names: str
    last_names: str
    email: str


class LoginFarmerRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class AuthenticatedFarmerResponse(BaseModel):
    id: str
    names: str
    last_names: str
    email: str


class LoginFarmerResponse(BaseModel):
    access_token: str
    token_type: str
    farmer: AuthenticatedFarmerResponse


def create_auth_router(container: CompositionRoot) -> APIRouter:
    router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

    @router.post(
        "/register",
        status_code=status.HTTP_201_CREATED,
        response_model=RegisterFarmerResponse,
    )
    def register(payload: RegisterFarmerRequest) -> RegisterFarmerResponse:
        command = ComandoRegistrarAgricultor(
            nombres=payload.names,
            apellidos=payload.last_names,
            email=payload.email,
            contrasena=payload.password,
        )
        try:
            result = container.puerto_registrar_agricultor.ejecutar(command)
        except ErrorCorreoDuplicado as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        except (ErrorCorreoInvalido, ErrorContrasenaInvalida, ErrorDatosAgricultorInvalidos) as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        except ErrorDominio as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

        return RegisterFarmerResponse(
            id=result.id,
            names=result.nombres,
            last_names=result.apellidos,
            email=result.email,
        )

    @router.post(
        "/login",
        status_code=status.HTTP_200_OK,
        response_model=LoginFarmerResponse,
    )
    def login(payload: LoginFarmerRequest) -> LoginFarmerResponse:
        command = ComandoIniciarSesionAgricultor(
            email=payload.email,
            contrasena=payload.password,
        )
        try:
            result = container.puerto_iniciar_sesion_agricultor.ejecutar(command)
        except ErrorCredencialesInvalidas as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(error),
            ) from error
        except ErrorCorreoInvalido as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        except ErrorDominio as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

        return LoginFarmerResponse(
            access_token=result.access_token,
            token_type=result.token_type,
            farmer=AuthenticatedFarmerResponse(
                id=result.agricultor.id,
                names=result.agricultor.nombres,
                last_names=result.agricultor.apellidos,
                email=result.agricultor.email,
            ),
        )

    return router
