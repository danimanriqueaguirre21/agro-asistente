from datetime import datetime, timezone
from uuid import uuid4

from app.domain.exceptions import ErrorDatosContextoInvalidos
from app.domain.valueObjects.cultivo import Cultivo
from app.domain.valueObjects.region import Region


class ContextoAgricola:
    def __init__(
        self,
        contexto_id: str,
        agricultor_id: str,
        nombre_predio: str | None,
        cultivo: Cultivo,
        region: Region,
        observaciones: str | None,
        esta_seleccionado: bool,
        creado_en: datetime,
    ) -> None:
        self.id = contexto_id
        self.agricultor_id = agricultor_id
        self.nombre_predio = nombre_predio
        self.cultivo = cultivo
        self.region = region
        self.observaciones = observaciones
        self.esta_seleccionado = esta_seleccionado
        self.creado_en = creado_en

    @classmethod
    def crear(
        cls,
        agricultor_id: str,
        nombre_predio: str | None,
        cultivo: Cultivo,
        region: Region,
        observaciones: str | None,
    ) -> "ContextoAgricola":
        if not (agricultor_id or "").strip():
            raise ErrorDatosContextoInvalidos("El agricultor es obligatorio")
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)
        return cls(
            contexto_id=str(uuid4()),
            agricultor_id=agricultor_id.strip(),
            nombre_predio=_texto_opcional(nombre_predio, 120, "El nombre del predio"),
            cultivo=cultivo,
            region=region,
            observaciones=_texto_opcional(observaciones, 500, "Las notas"),
            esta_seleccionado=False,
            creado_en=ahora,
        )

    def marcar_seleccionado(self) -> None:
        self.esta_seleccionado = True

    def marcar_no_seleccionado(self) -> None:
        self.esta_seleccionado = False


def _texto_opcional(value: str | None, max_length: int, etiqueta: str) -> str | None:
    if value is None:
        return None
    limpio = value.strip()
    if not limpio:
        return None
    if len(limpio) > max_length:
        raise ErrorDatosContextoInvalidos(f"{etiqueta} superan la longitud permitida")
    return limpio
