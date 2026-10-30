from app.domain.ports.output.text_generation_port import (
    PasajeRecuperado,
    PuertoGeneracionTexto,
    RespuestaGenerada,
)


class AdaptadorGeneracionPlantilla(PuertoGeneracionTexto):
    """Respuesta inicial por plantilla para PMV1. No invoca un modelo de IA."""

    METHOD = "template"
    MARCA_SIN_RESULTADOS = "No se encontró información suficiente en la base de conocimiento."

    def generar(
        self,
        texto_consulta: str,
        cultivo: str,
        region: str,
        pasajes: list[PasajeRecuperado] | None = None,
    ) -> RespuestaGenerada:
        encabezado = (
            f"Consulta recibida para el cultivo de {cultivo} en la región {region}. "
            f"Tu pregunta fue: {texto_consulta} "
        )
        relevantes = [item for item in (pasajes or []) if (item.extracto or "").strip()]
        if not relevantes:
            respuesta = (
                f"{encabezado}"
                f"{self.MARCA_SIN_RESULTADOS} "
                "Esta es una respuesta inicial de PMV1. "
                "No se inventó evidencia. Todavía no se utiliza un modelo de IA externo."
            )
            return RespuestaGenerada(texto_respuesta=respuesta, metodo_generacion=self.METHOD)

        fragmentos: list[str] = []
        for indice, pasaje in enumerate(relevantes, start=1):
            titulo = pasaje.titulo.strip() or "documento agrícola"
            fragmentos.append(f"{indice}) {titulo}: {pasaje.extracto.strip()}")
        unidos = " ".join(fragmentos)
        respuesta = (
            f"{encabezado}"
            "Esta respuesta inicial está basada en información recuperada de la base "
            f"de conocimiento: {unidos} "
            "La generación sigue siendo una plantilla de PMV1. No se utiliza un modelo de IA externo."
        )
        return RespuestaGenerada(texto_respuesta=respuesta, metodo_generacion=self.METHOD)
