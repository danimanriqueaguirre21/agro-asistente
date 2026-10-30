from app.domain.exceptions import ErrorContextoNoEncontrado
from app.domain.ports.input.gestionar_contexto_port import (
    ComandoSeleccionarContextoAgricola,
    PuertoSeleccionarContextoAgricola,
    ResultadoContextoAgricola,
    contexto_a_resultado,
)
from app.domain.ports.output.repositorio_contexto_agricola_port import (
    PuertoRepositorioContextoAgricola,
)


class SeleccionarContextoAgricola(PuertoSeleccionarContextoAgricola):
    def __init__(self, repositorio_contexto: PuertoRepositorioContextoAgricola) -> None:
        self._repositorio_contexto = repositorio_contexto

    def ejecutar(self, comando: ComandoSeleccionarContextoAgricola) -> ResultadoContextoAgricola:
        seleccionado = self._repositorio_contexto.seleccionar_para_agricultor(
            comando.contexto_id,
            comando.agricultor_id,
        )
        if seleccionado is None:
            raise ErrorContextoNoEncontrado("Contexto agrícola no encontrado")
        return contexto_a_resultado(seleccionado)
