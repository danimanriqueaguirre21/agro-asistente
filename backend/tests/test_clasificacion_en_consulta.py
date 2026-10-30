from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.application.services.servicio_recuperacion_rag import FragmentoRecuperado
from app.application.useCases.registrar_consulta import RegistrarConsulta
from app.domain.entities.contexto_agricola import ContextoAgricola
from app.domain.exceptions import ErrorClasificadorNoDisponible
from app.domain.ports.input.clasificar_consulta_port import (
    PuertoClasificarConsulta,
    ResultadoClasificacionConsulta,
)
from app.domain.ports.input.registrar_consulta_port import ComandoRegistrarConsulta
from app.domain.ports.output.puerto_clasificador_consultas import (
    CATEGORIAS_TEMATICAS_CONJUNTO,
    SALIDA_SIN_CATEGORIA,
)
from app.domain.ports.output.text_generation_port import (
    PuertoGeneracionTexto,
    RespuestaGenerada,
)
from app.domain.valueObjects.cultivo import Cultivo
from app.domain.valueObjects.region import Region
from app.main import app

CONSULTA = "¿Cada cuántos días abro el surco para la papa de Huancayo?"


class _Repositorio:
    def __init__(self) -> None:
        self.contextos_seleccionados = {}
        self.consultas = []
        self.respuestas = []

    def buscar_contexto_seleccionado(self, agricultor_id: str):
        return self.contextos_seleccionados.get(agricultor_id)

    def guardar_consulta(self, consulta) -> None:
        self.consultas.append(consulta)

    def guardar_respuesta(self, respuesta) -> None:
        self.respuestas.append(respuesta)


class _Evidencias:
    def guardar_todas(self, evidencias) -> None:
        return None


class _Generacion(PuertoGeneracionTexto):
    def __init__(self) -> None:
        self.llamadas = []

    def generar(self, texto_consulta, cultivo, region, pasajes=None):
        self.llamadas.append(
            {
                "texto_consulta": texto_consulta,
                "cultivo": cultivo,
                "region": region,
                "pasajes": list(pasajes or []),
            }
        )
        return RespuestaGenerada(
            texto_respuesta=f"FAKE:{cultivo}:{region}:{texto_consulta}",
            metodo_generacion="template",
        )


class _Rag:
    def __init__(self) -> None:
        self.consultas = []

    def recuperar(self, texto_consulta: str) -> list[FragmentoRecuperado]:
        self.consultas.append(texto_consulta)
        return []


class _Clasificador(PuertoClasificarConsulta):
    def __init__(self, resultado: ResultadoClasificacionConsulta | None = None, error: Exception | None = None) -> None:
        self.resultado = resultado or _resultado("riego", False, None, 0.62, 0.20)
        self.error = error
        self.textos = []

    def ejecutar(self, comando):
        self.textos.append(comando.texto)
        if self.error is not None:
            raise self.error
        return self.resultado


def _resultado(categoria, abstencion, motivo, primera, segunda) -> ResultadoClasificacionConsulta:
    return ResultadoClasificacionConsulta(
        categoria=categoria,
        abstencion=abstencion,
        motivo_abstencion=motivo,
        clase_primera="riego" if categoria == SALIDA_SIN_CATEGORIA else categoria,
        puntuacion_primera=primera,
        clase_segunda="suelos",
        puntuacion_segunda=segunda,
        margen=primera - segunda,
        puntuaciones_calibradas=False,
    )


def _caso(clasificador: _Clasificador):
    repo = _Repositorio()
    repo.contextos_seleccionados["farmer-a"] = ContextoAgricola(
        contexto_id=str(uuid4()),
        agricultor_id="farmer-a",
        nombre_predio="Parcela 1",
        cultivo=Cultivo("papa"),
        region=Region("Huancayo"),
        observaciones=None,
        esta_seleccionado=True,
        creado_en=datetime.now(timezone.utc).replace(tzinfo=None),
    )
    generacion = _Generacion()
    rag = _Rag()
    caso = RegistrarConsulta(repo, generacion, rag, _Evidencias(), clasificador)
    return caso, generacion, rag, clasificador


def test_la_consulta_recibe_una_categoria_de_las_ocho() -> None:
    caso, generacion, rag, clasificador = _caso(_Clasificador())
    resultado = caso.ejecutar(ComandoRegistrarConsulta(agricultor_id="farmer-a", texto=CONSULTA))

    assert resultado.clasificacion is not None
    assert resultado.clasificacion.categoria in CATEGORIAS_TEMATICAS_CONJUNTO
    assert resultado.error_clasificacion is None
    assert rag.consultas == [CONSULTA]
    assert generacion.llamadas[0]["texto_consulta"] == CONSULTA
    assert resultado.respuesta == f"FAKE:papa:Huancayo:{CONSULTA}"
    assert clasificador.textos == [CONSULTA]


def test_la_abstencion_se_conserva_y_no_es_una_clase() -> None:
    clasificador = _Clasificador(
        _resultado(SALIDA_SIN_CATEGORIA, True, "margen_insuficiente", 0.40, 0.30)
    )
    caso, generacion, rag, _ = _caso(clasificador)
    resultado = caso.ejecutar(ComandoRegistrarConsulta(agricultor_id="farmer-a", texto=CONSULTA))

    assert resultado.clasificacion is not None
    assert resultado.clasificacion.categoria == SALIDA_SIN_CATEGORIA
    assert resultado.clasificacion.abstencion is True
    assert resultado.clasificacion.clase_primera in CATEGORIAS_TEMATICAS_CONJUNTO
    assert SALIDA_SIN_CATEGORIA not in CATEGORIAS_TEMATICAS_CONJUNTO
    assert rag.consultas == [CONSULTA]
    assert "sin categoría" not in generacion.llamadas[0]["texto_consulta"]
    assert resultado.respuesta.startswith("FAKE:")


def test_un_error_del_clasificador_no_inventa_categoria() -> None:
    clasificador = _Clasificador(error=ErrorClasificadorNoDisponible("No se encuentra el modelo v2."))
    caso, generacion, rag, _ = _caso(clasificador)
    resultado = caso.ejecutar(ComandoRegistrarConsulta(agricultor_id="farmer-a", texto=CONSULTA))

    assert resultado.clasificacion is None
    assert resultado.error_clasificacion == "No se encuentra el modelo v2."
    assert resultado.respuesta == f"FAKE:papa:Huancayo:{CONSULTA}"
    assert rag.consultas == [CONSULTA]
    assert len(clasificador.textos) == 1


def test_el_clasificador_se_consulta_una_sola_vez() -> None:
    caso, _, _, clasificador = _caso(_Clasificador())
    caso.ejecutar(ComandoRegistrarConsulta(agricultor_id="farmer-a", texto=CONSULTA))
    assert clasificador.textos == [CONSULTA]


def test_la_consulta_http_sigue_exigiendo_jwt() -> None:
    response = TestClient(app).post("/api/v1/queries", json={"text": CONSULTA})
    assert response.status_code == 401
