class ErrorDominio(Exception):
    """Error de regla de negocio."""


class ErrorDatosAgricultorInvalidos(ErrorDominio):
    """Datos obligatorios del agricultor inválidos o ausentes."""


class ErrorCorreoInvalido(ErrorDominio):
    """El correo electrónico no cumple el formato del dominio."""


class ErrorContrasenaInvalida(ErrorDominio):
    """La contraseña no cumple las reglas del dominio."""


class ErrorCorreoDuplicado(ErrorDominio):
    """Ya existe un agricultor con el mismo correo."""


class ErrorCredencialesInvalidas(ErrorDominio):
    """Email o contraseña incorrectos. El mensaje debe ser genérico."""


class ErrorTokenInvalido(ErrorDominio):
    """Token ausente, inválido o expirado."""


class ErrorDatosContextoInvalidos(ErrorDominio):
    """Datos del contexto agrícola inválidos."""


class ErrorContextoNoEncontrado(ErrorDominio):
    """El contexto no existe o no pertenece al agricultor autenticado."""


class ErrorTextoConsultaInvalido(ErrorDominio):
    """El texto de la consulta agrícola es inválido."""


class ErrorDatosConsultaInvalidos(ErrorDominio):
    """Datos de la consulta agrícola inválidos o ausentes."""


class ErrorContextoSeleccionadoNoEncontrado(ErrorDominio):
    """El agricultor no tiene un contexto agrícola seleccionado."""


class ErrorDocumentoConocimientoInvalido(ErrorDominio):
    """Datos del documento de conocimiento inválidos o ausentes."""


class ErrorDocumentoConocimientoDuplicado(ErrorDominio):
    """Ya existe un documento con el mismo contenido."""


class ErrorEvidenciaInvalida(ErrorDominio):
    """Datos de evidencia recuperada inválidos o ausentes."""


class ErrorArchivoConocimientoNoEncontrado(ErrorDominio):
    """El archivo Markdown del documento de conocimiento no existe."""


class ErrorGeneracionTexto(ErrorDominio):
    """No se pudo generar la respuesta técnica. El dominio no conoce el proveedor."""


class ErrorObservacionesMeteorologicas(ErrorDominio):
    """No se pudieron obtener observaciones meteorológicas. El dominio no conoce el proveedor."""


class ErrorClasificadorNoDisponible(ErrorDominio):
    """El clasificador experimental no pudo cargarse o devolvió una salida inválida."""


class ErrorEscenarioRiesgoInvalido(ErrorDominio):
    """El escenario de riesgo no cumple el formato del prototipo HU-08."""


class ErrorPredictorRiesgoNoDisponible(ErrorDominio):
    """El modelo de riesgo HU-08 no pudo cargarse o devolvió una categoría inválida."""
