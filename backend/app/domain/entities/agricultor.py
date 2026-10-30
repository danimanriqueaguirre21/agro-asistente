from datetime import datetime, timezone
from uuid import uuid4

from app.domain.exceptions import ErrorDatosAgricultorInvalidos
from app.domain.valueObjects.email import Email
from app.domain.valueObjects.hash_contrasena import HashContrasena


class Agricultor:
    def __init__(
        self,
        agricultor_id: str,
        nombres: str,
        apellidos: str,
        email: Email,
        hash_contrasena: HashContrasena,
        creado_en: datetime,
        actualizado_en: datetime,
    ) -> None:
        self.id = agricultor_id
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.hash_contrasena = hash_contrasena
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en

    @classmethod
    def registrar(
        cls,
        nombres: str,
        apellidos: str,
        email: Email,
        hash_contrasena: HashContrasena,
    ) -> "Agricultor":
        nombres_limpios = (nombres or "").strip()
        apellidos_limpios = (apellidos or "").strip()
        if not nombres_limpios:
            raise ErrorDatosAgricultorInvalidos("Los nombres son obligatorios")
        if not apellidos_limpios:
            raise ErrorDatosAgricultorInvalidos("Los apellidos son obligatorios")
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)
        nombre_completo = f"{nombres_limpios} {apellidos_limpios}".strip()
        if len(nombre_completo) > 120:
            raise ErrorDatosAgricultorInvalidos("El nombre completo supera la longitud permitida")
        return cls(
            agricultor_id=str(uuid4()),
            nombres=nombres_limpios,
            apellidos=apellidos_limpios,
            email=email,
            hash_contrasena=hash_contrasena,
            creado_en=ahora,
            actualizado_en=ahora,
        )

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}".strip()
