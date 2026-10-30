from app.domain.ports.output.text_generation_port import (
    GeneratedAnswer,
    RetrievedPassage,
    TextGenerationPort,
)


class TemplateGenerationAdapter(TextGenerationPort):
    """Respuesta inicial por plantilla para PMV1. No invoca un modelo de IA."""

    METHOD = "template"
    NO_RESULTS_MARK = "No se encontró información suficiente en la base de conocimiento."

    def generate(
        self,
        query_text: str,
        crop: str,
        region: str,
        passages: list[RetrievedPassage] | None = None,
    ) -> GeneratedAnswer:
        header = (
            f"Consulta recibida para el cultivo de {crop} en la región {region}. "
            f"Tu pregunta fue: {query_text} "
        )
        relevant = [item for item in (passages or []) if (item.excerpt or "").strip()]
        if not relevant:
            answer = (
                f"{header}"
                f"{self.NO_RESULTS_MARK} "
                "Esta es una respuesta inicial de PMV1. "
                "No se inventó evidencia. Todavía no se utiliza un modelo de IA externo."
            )
            return GeneratedAnswer(answer_text=answer, generation_method=self.METHOD)

        fragments: list[str] = []
        for index, passage in enumerate(relevant, start=1):
            title = passage.title.strip() or "documento agrícola"
            fragments.append(f"{index}) {title}: {passage.excerpt.strip()}")
        joined = " ".join(fragments)
        answer = (
            f"{header}"
            "Esta respuesta inicial está basada en información recuperada de la base "
            f"de conocimiento: {joined} "
            "La generación sigue siendo una plantilla de PMV1. No se utiliza un modelo de IA externo."
        )
        return GeneratedAnswer(answer_text=answer, generation_method=self.METHOD)
