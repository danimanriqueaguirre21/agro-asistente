from app.domain.ports.input.gestionar_contexto_port import (
    ComandoCrearContextoAgricola,
    ComandoSeleccionarContextoAgricola,
    PuertoCrearContextoAgricola,
    PuertoListarContextosAgricolas,
    PuertoSeleccionarContextoAgricola,
    ResultadoContextoAgricola,
)
from app.domain.ports.input.incorporar_conocimiento_port import (
    ComandoIncorporarConocimiento,
    PuertoIncorporarConocimiento,
    PuertoListarDocumentosConocimiento,
    ResultadoDocumentoConocimiento,
)
from app.domain.ports.input.indexar_conocimiento_port import (
    PuertoIndexarConocimiento,
    ResultadoIndexarConocimiento,
)
from app.domain.ports.input.iniciar_sesion_agricultor_port import (
    AgricultorAutenticado,
    ComandoIniciarSesionAgricultor,
    PuertoIniciarSesionAgricultor,
    ResultadoIniciarSesionAgricultor,
)
from app.domain.ports.input.registrar_agricultor_port import (
    ComandoRegistrarAgricultor,
    PuertoRegistrarAgricultor,
    ResultadoRegistrarAgricultor,
)
from app.domain.ports.input.registrar_consulta_port import (
    ComandoRegistrarConsulta,
    PuertoRegistrarConsulta,
    ResultadoContextoConsulta,
    ResultadoEvidenciaConsulta,
    ResultadoRegistrarConsulta,
)

__all__ = [
    "AgricultorAutenticado",
    "ComandoCrearContextoAgricola",
    "ComandoIncorporarConocimiento",
    "ComandoIniciarSesionAgricultor",
    "ComandoRegistrarAgricultor",
    "ComandoRegistrarConsulta",
    "ComandoSeleccionarContextoAgricola",
    "PuertoCrearContextoAgricola",
    "PuertoIncorporarConocimiento",
    "PuertoIndexarConocimiento",
    "PuertoIniciarSesionAgricultor",
    "PuertoListarContextosAgricolas",
    "PuertoListarDocumentosConocimiento",
    "PuertoRegistrarAgricultor",
    "PuertoRegistrarConsulta",
    "PuertoSeleccionarContextoAgricola",
    "ResultadoContextoAgricola",
    "ResultadoContextoConsulta",
    "ResultadoDocumentoConocimiento",
    "ResultadoEvidenciaConsulta",
    "ResultadoIndexarConocimiento",
    "ResultadoIniciarSesionAgricultor",
    "ResultadoRegistrarAgricultor",
    "ResultadoRegistrarConsulta",
]
