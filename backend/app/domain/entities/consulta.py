from datetime import datetime, timezone
from uuid import uuid4

from app.domain.exceptions import ErrorDatosConsultaInvalidos
from app.domain.valueObjects.texto_consulta import TextoConsulta


class Consulta:
    def __init__(
        self,
        consulta_id: str,
        agricultor_id: str,
        contexto_id: str,
        texto: TextoConsulta,
        creado_en: datetime,
    ) -> None:
        self.id = consulta_id
        self.agricultor_id = agricultor_id
        self.contexto_id = contexto_id
        self.texto = texto
        self.creado_en = creado_en

    @classmethod
    def crear(cls, agricultor_id: str, contexto_id: str, texto: TextoConsulta) -> "Consulta":
        if not (agricultor_id or "").strip():
            raise ErrorDatosConsultaInvalidos("El agricultor es obligatorio")
        if not (contexto_id or "").strip():
            raise ErrorDatosConsultaInvalidos("El contexto agrícola es obligatorio")
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)
        return cls(
            consulta_id=str(uuid4()),
            agricultor_id=agricultor_id.strip(),
            contexto_id=contexto_id.strip(),
            texto=texto,
            creado_en=ahora,
        )
