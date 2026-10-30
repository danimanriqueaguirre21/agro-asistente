from uuid import uuid4

from app.domain.exceptions import ErrorEvidenciaInvalida


class Evidencia:
    """Información recuperada de la base de conocimiento y asociada a una consulta."""

    LONGITUD_MAXIMA_FRAGMENTO_ID = 120

    def __init__(
        self,
        evidencia_id: str,
        consulta_id: str,
        respuesta_id: str,
        documento_id: str,
        fragmento_id: str,
        extracto: str,
        puntaje_similitud: float,
        orden_relevancia: int,
        titulo_documento: str = "",
    ) -> None:
        self.id = evidencia_id
        self.consulta_id = consulta_id
        self.respuesta_id = respuesta_id
        self.documento_id = documento_id
        self.fragmento_id = fragmento_id
        self.extracto = extracto
        self.puntaje_similitud = puntaje_similitud
        self.orden_relevancia = orden_relevancia
        self.titulo_documento = titulo_documento

    @classmethod
    def crear(
        cls,
        consulta_id: str,
        respuesta_id: str,
        documento_id: str,
        fragmento_id: str,
        extracto: str,
        puntaje_similitud: float,
        orden_relevancia: int,
        titulo_documento: str = "",
    ) -> "Evidencia":
        if not (consulta_id or "").strip():
            raise ErrorEvidenciaInvalida("La consulta es obligatoria")
        if not (respuesta_id or "").strip():
            raise ErrorEvidenciaInvalida("La respuesta es obligatoria")
        if not (documento_id or "").strip():
            raise ErrorEvidenciaInvalida("El documento de origen es obligatorio")
        fragmento_limpio = (fragmento_id or "").strip()
        if not fragmento_limpio:
            raise ErrorEvidenciaInvalida("El identificador del fragmento es obligatorio")
        if len(fragmento_limpio) > cls.LONGITUD_MAXIMA_FRAGMENTO_ID:
            raise ErrorEvidenciaInvalida("El identificador del fragmento supera la longitud permitida")
        extracto_limpio = (extracto or "").strip()
        if not extracto_limpio:
            raise ErrorEvidenciaInvalida("El contenido recuperado es obligatorio")
        try:
            puntaje = float(puntaje_similitud)
        except (TypeError, ValueError) as error:
            raise ErrorEvidenciaInvalida("La relevancia es inválida") from error
        if puntaje < 0 or puntaje > 1:
            raise ErrorEvidenciaInvalida("La relevancia debe estar entre 0 y 1")
        if (
            not isinstance(orden_relevancia, int)
            or isinstance(orden_relevancia, bool)
            or orden_relevancia < 1
        ):
            raise ErrorEvidenciaInvalida("El orden de relevancia es inválido")
        return cls(
            evidencia_id=str(uuid4()),
            consulta_id=consulta_id.strip(),
            respuesta_id=respuesta_id.strip(),
            documento_id=documento_id.strip(),
            fragmento_id=fragmento_limpio,
            extracto=extracto_limpio,
            puntaje_similitud=round(puntaje, 5),
            orden_relevancia=orden_relevancia,
            titulo_documento=(titulo_documento or "").strip(),
        )
