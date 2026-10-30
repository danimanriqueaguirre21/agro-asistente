from app.domain.exceptions import ErrorClasificadorNoDisponible
from app.domain.ports.input.clasificar_consulta_port import (
    ComandoClasificarConsulta,
    PuertoClasificarConsulta,
    ResultadoClasificacionConsulta,
)
from app.domain.ports.output.puerto_clasificador_consultas import (
    CATEGORIAS_TEMATICAS_CONJUNTO,
    MOTIVO_MARGEN_INSUFICIENTE,
    SALIDA_SIN_CATEGORIA,
    PuertoClasificadorConsultas,
    PuntuacionModelo,
)
from app.domain.valueObjects.texto_consulta import TextoConsulta


def decidir_clasificacion(
    puntuacion: PuntuacionModelo,
    margen_minimo: float,
) -> ResultadoClasificacionConsulta:
    """Aplica el umbral. `sin categoría` es abstención, no una clase del modelo."""

    if (
        puntuacion.clase_primera not in CATEGORIAS_TEMATICAS_CONJUNTO
        or puntuacion.clase_segunda not in CATEGORIAS_TEMATICAS_CONJUNTO
        or puntuacion.clase_primera == SALIDA_SIN_CATEGORIA
        or puntuacion.clase_segunda == SALIDA_SIN_CATEGORIA
    ):
        raise ErrorClasificadorNoDisponible(
            "El clasificador devolvió una clase fuera de las ocho categorías."
        )
    margen = puntuacion.puntuacion_primera - puntuacion.puntuacion_segunda
    abstencion = margen < margen_minimo
    return ResultadoClasificacionConsulta(
        categoria=SALIDA_SIN_CATEGORIA if abstencion else puntuacion.clase_primera,
        abstencion=abstencion,
        motivo_abstencion=MOTIVO_MARGEN_INSUFICIENTE if abstencion else None,
        clase_primera=puntuacion.clase_primera,
        puntuacion_primera=puntuacion.puntuacion_primera,
        clase_segunda=puntuacion.clase_segunda,
        puntuacion_segunda=puntuacion.puntuacion_segunda,
        margen=margen,
        puntuaciones_calibradas=False,
    )


class ClasificarConsulta(PuertoClasificarConsulta):
    def __init__(
        self,
        puerto_clasificador: PuertoClasificadorConsultas,
        margen_minimo: float,
    ) -> None:
        self._puerto_clasificador = puerto_clasificador
        self._margen_minimo = margen_minimo

    def ejecutar(self, comando: ComandoClasificarConsulta) -> ResultadoClasificacionConsulta:
        texto = TextoConsulta(comando.texto).value
        puntuacion = self._puerto_clasificador.puntuar(texto)
        return decidir_clasificacion(puntuacion, self._margen_minimo)
