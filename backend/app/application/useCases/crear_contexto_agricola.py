from app.domain.entities.contexto_agricola import ContextoAgricola
from app.domain.ports.input.gestionar_contexto_port import (
    ComandoCrearContextoAgricola,
    PuertoCrearContextoAgricola,
    ResultadoContextoAgricola,
    contexto_a_resultado,
)
from app.domain.ports.output.repositorio_contexto_agricola_port import (
    PuertoRepositorioContextoAgricola,
)
from app.domain.valueObjects.cultivo import Cultivo
from app.domain.valueObjects.region import Region


class CrearContextoAgricola(PuertoCrearContextoAgricola):
    def __init__(self, repositorio_contexto: PuertoRepositorioContextoAgricola) -> None:
        self._repositorio_contexto = repositorio_contexto

    def ejecutar(self, comando: ComandoCrearContextoAgricola) -> ResultadoContextoAgricola:
        contexto = ContextoAgricola.crear(
            agricultor_id=comando.agricultor_id,
            nombre_predio=comando.nombre_predio,
            cultivo=Cultivo(comando.cultivo),
            region=Region(comando.region),
            observaciones=comando.observaciones,
        )
        self._repositorio_contexto.guardar(contexto)
        return contexto_a_resultado(contexto)
