from datetime import datetime, timezone
from uuid import uuid4

from app.domain.exceptions import ErrorDatosConsultaInvalidos


class Respuesta:
    def __init__(
        self,
        respuesta_id: str,
        consulta_id: str,
        texto_respuesta: str,
        metodo_generacion: str,
        creado_en: datetime,
    ) -> None:
        self.id = respuesta_id
        self.consulta_id = consulta_id
        self.texto_respuesta = texto_respuesta
        self.metodo_generacion = metodo_generacion
        self.creado_en = creado_en

    @classmethod
    def crear(cls, consulta_id: str, texto_respuesta: str, metodo_generacion: str) -> "Respuesta":
        if not (consulta_id or "").strip():
            raise ErrorDatosConsultaInvalidos("La consulta es obligatoria")
        respuesta_limpia = (texto_respuesta or "").strip()
        if not respuesta_limpia:
            raise ErrorDatosConsultaInvalidos("La respuesta generada es obligatoria")
        metodo_limpio = (metodo_generacion or "").strip()
        if not metodo_limpio:
            raise ErrorDatosConsultaInvalidos("El método de generación es obligatorio")
        if len(metodo_limpio) > 40:
            raise ErrorDatosConsultaInvalidos("El método de generación supera la longitud permitida")
        ahora = datetime.now(timezone.utc).replace(tzinfo=None)
        return cls(
            respuesta_id=str(uuid4()),
            consulta_id=consulta_id.strip(),
            texto_respuesta=respuesta_limpia,
            metodo_generacion=metodo_limpio,
            creado_en=ahora,
        )
