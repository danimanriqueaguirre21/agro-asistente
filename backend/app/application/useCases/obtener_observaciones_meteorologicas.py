from app.domain.ports.input.obtener_observaciones_meteorologicas_port import (
    ComandoObtenerObservacionesMeteorologicas,
    PuertoObtenerObservacionesMeteorologicas,
    ResultadoObservacionMeteorologica,
)
from app.domain.ports.output.puerto_observaciones_meteorologicas import (
    FiltroObservacionesMeteorologicas,
    PuertoObservacionesMeteorologicas,
)


class ObtenerObservacionesMeteorologicas(PuertoObtenerObservacionesMeteorologicas):
    def __init__(self, puerto_observaciones: PuertoObservacionesMeteorologicas) -> None:
        self._puerto_observaciones = puerto_observaciones

    def ejecutar(
        self, comando: ComandoObtenerObservacionesMeteorologicas
    ) -> list[ResultadoObservacionMeteorologica]:
        filtro = FiltroObservacionesMeteorologicas(
            limite=comando.limite,
            fecha_hora=comando.fecha_hora,
            caja_geografica=comando.caja_geografica,
            identificador_estacion=comando.identificador_estacion,
            nombre_variable=comando.nombre_variable,
            orden=comando.orden,
        )
        observaciones = self._puerto_observaciones.obtener_recientes(filtro)
        return [
            ResultadoObservacionMeteorologica(
                identificador_estacion=item.identificador_estacion,
                nombre_estacion=item.nombre_estacion,
                latitud=item.latitud,
                longitud=item.longitud,
                altitud=item.altitud,
                fecha_hora=item.fecha_hora,
                temperatura=item.temperatura,
                punto_rocio=item.punto_rocio,
                precipitacion=item.precipitacion,
            )
            for item in observaciones
        ]
