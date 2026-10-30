from app.domain.ports.input.gestionar_contexto_port import (
    PuertoListarContextosAgricolas,
    ResultadoContextoAgricola,
    contexto_a_resultado,
)
from app.domain.ports.output.repositorio_contexto_agricola_port import (
    PuertoRepositorioContextoAgricola,
)


class ListarContextosAgricolas(PuertoListarContextosAgricolas):
    def __init__(self, repositorio_contexto: PuertoRepositorioContextoAgricola) -> None:
        self._repositorio_contexto = repositorio_contexto

    def ejecutar(self, agricultor_id: str) -> list[ResultadoContextoAgricola]:
        contextos = self._repositorio_contexto.listar_por_agricultor(agricultor_id)
        return [contexto_a_resultado(contexto) for contexto in contextos]
