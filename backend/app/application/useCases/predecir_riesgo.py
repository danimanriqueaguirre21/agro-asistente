from app.domain.exceptions import ErrorEscenarioRiesgoInvalido, ErrorPredictorRiesgoNoDisponible
from app.domain.ports.input.predecir_riesgo_port import (
    ComandoPredecirRiesgo,
    PuertoPredecirRiesgo,
    ResultadoPrediccionRiesgo,
)
from app.domain.ports.output.puerto_predictor_riesgo import (
    CATEGORIAS_RIESGO_CONJUNTO,
    CONDICIONES_SUELO,
    FAMILIAS_ESCENARIO,
    IDENTIFICADOR_MODELO_RIESGO,
    NATURALEZA_RIESGO,
    VERSION_REGLAS_RIESGO,
    EscenarioRiesgo,
    PuertoPredictorRiesgo,
)


class PredecirRiesgoAgricola(PuertoPredecirRiesgo):
    def __init__(self, puerto_predictor: PuertoPredictorRiesgo) -> None:
        self._puerto_predictor = puerto_predictor

    def ejecutar(self, comando: ComandoPredecirRiesgo) -> ResultadoPrediccionRiesgo:
        escenario = _validar_escenario(comando.escenario)
        categoria = self._puerto_predictor.predecir(escenario)
        if categoria not in CATEGORIAS_RIESGO_CONJUNTO:
            raise ErrorPredictorRiesgoNoDisponible(
                "El modelo de riesgo devolvió una categoría que no pertenece al prototipo."
            )
        return ResultadoPrediccionRiesgo(
            categoria_predicha=categoria,
            identificador_modelo=IDENTIFICADOR_MODELO_RIESGO,
            version_reglas=VERSION_REGLAS_RIESGO,
            naturaleza=NATURALEZA_RIESGO,
            es_riesgo_agricola_validado=False,
        )


def _validar_escenario(escenario: EscenarioRiesgo) -> EscenarioRiesgo:
    familia = _texto(escenario.familia_escenario, "familia_escenario")
    if familia not in FAMILIAS_ESCENARIO:
        raise ErrorEscenarioRiesgoInvalido(
            "familia_escenario debe ser meteorologico, plaga_enfermedad o suelo_agua_manejo."
        )
    condicion = _texto(escenario.condicion_suelo, "condicion_suelo")
    if condicion not in CONDICIONES_SUELO:
        raise ErrorEscenarioRiesgoInvalido(
            "condicion_suelo debe ser seco, adecuado o encharcado."
        )
    if not isinstance(escenario.sintoma_observado, bool):
        raise ErrorEscenarioRiesgoInvalido("sintoma_observado debe ser true o false.")
    if not isinstance(escenario.dias_sin_lluvia, int) or isinstance(escenario.dias_sin_lluvia, bool):
        raise ErrorEscenarioRiesgoInvalido("dias_sin_lluvia debe ser un entero.")
    proporcion = _numero_opcional(escenario.proporcion_afectada, "proporcion_afectada", obligatorio=True)
    if proporcion is None or not 0 <= proporcion <= 1:
        raise ErrorEscenarioRiesgoInvalido("proporcion_afectada debe estar entre 0 y 1.")
    if not escenario.sintoma_observado and proporcion != 0:
        raise ErrorEscenarioRiesgoInvalido(
            "Si sintoma_observado es false, proporcion_afectada debe ser 0."
        )
    temperatura = _numero_opcional(escenario.temperatura_c, "temperatura_c", obligatorio=False)
    precipitacion = _numero_opcional(escenario.precipitacion_mm, "precipitacion_mm", obligatorio=False)
    return EscenarioRiesgo(
        familia_escenario=familia,
        cultivo=_texto(escenario.cultivo, "cultivo"),
        region=_texto(escenario.region, "region"),
        etapa_fenologica=_texto(escenario.etapa_fenologica, "etapa_fenologica"),
        temperatura_c=temperatura,
        precipitacion_mm=precipitacion,
        dias_sin_lluvia=escenario.dias_sin_lluvia,
        sintoma_observado=escenario.sintoma_observado,
        proporcion_afectada=proporcion,
        condicion_suelo=condicion,
    )


def _texto(valor: object, nombre: str) -> str:
    if not isinstance(valor, str):
        raise ErrorEscenarioRiesgoInvalido(f"{nombre} debe ser texto.")
    limpio = valor.strip()
    if not limpio:
        raise ErrorEscenarioRiesgoInvalido(f"{nombre} es obligatorio.")
    return limpio


def _numero_opcional(valor: object, nombre: str, obligatorio: bool) -> float | None:
    if valor is None:
        if obligatorio:
            raise ErrorEscenarioRiesgoInvalido(f"{nombre} es obligatorio.")
        return None
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ErrorEscenarioRiesgoInvalido(f"{nombre} debe ser numérico.")
    return float(valor)
