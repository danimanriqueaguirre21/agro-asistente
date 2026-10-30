from pathlib import Path

import httpx
import pytest

from app.application.services.servicio_recuperacion_rag import FragmentoRecuperado
from app.domain.ports.output.text_generation_port import PasajeRecuperado, PuertoGeneracionTexto, RespuestaGenerada
from app.infrastructure.config.settings import Settings
from evaluation.dataset import (
    DatasetEvaluacionInvalido,
    KNOWLEDGE_DIR,
    cargar_dataset,
    validar_dataset,
)
from evaluation.pipeline import ejecutar_item, filas_ragas
from evaluation.preflight import EvaluacionOficialNoEjecutable, exigir_ollama_disponible, exigir_proveedor_ollama
from evaluation.ragas_runner import describir_configuracion


class _RecuperacionFalsa:
    def __init__(self, fragmentos: list[FragmentoRecuperado]) -> None:
        self._fragmentos = fragmentos

    def recuperar(self, texto_consulta: str) -> list[FragmentoRecuperado]:
        return self._fragmentos


class _GeneracionFalsa(PuertoGeneracionTexto):
    def generar(
        self,
        texto_consulta: str,
        cultivo: str,
        region: str,
        pasajes: list[PasajeRecuperado] | None = None,
    ) -> RespuestaGenerada:
        extra = pasajes[0].extracto if pasajes else ""
        return RespuestaGenerada(
            texto_respuesta=f"FAKE:{cultivo}:{texto_consulta}:{extra}",
            metodo_generacion="ollama",
        )


def test_dataset_oficial_es_valido() -> None:
    dataset = cargar_dataset()
    assert dataset.id == "pmv1-baseline-v1"
    assert len(dataset.items) >= 6
    for item in dataset.items:
        assert item.question
        assert item.ground_truth
        assert item.source_documents


def test_dataset_referencia_documentos_existentes() -> None:
    dataset = cargar_dataset()
    for item in dataset.items:
        for nombre in item.source_documents:
            assert (KNOWLEDGE_DIR / nombre).is_file()


def test_dataset_rechaza_pregunta_vacia() -> None:
    with pytest.raises(DatasetEvaluacionInvalido, match="vacía"):
        validar_dataset(
            {
                "id": "x",
                "items": [
                    {
                        "id": "q1",
                        "question": "   ",
                        "ground_truth": "La papa en sierra requiere riegos frecuentes en floración.",
                        "crop": "papa",
                        "region": "Junín",
                        "source_documents": ["prueba-riego-papa.md"],
                    }
                ],
            }
        )


def test_dataset_rechaza_ground_truth_vacio() -> None:
    with pytest.raises(DatasetEvaluacionInvalido, match="vacío"):
        validar_dataset(
            {
                "id": "x",
                "items": [
                    {
                        "id": "q1",
                        "question": "¿Cómo riego?",
                        "ground_truth": "",
                        "crop": "papa",
                        "region": "Junín",
                        "source_documents": ["prueba-riego-papa.md"],
                    }
                ],
            }
        )


def test_dataset_rechaza_documento_inexistente() -> None:
    with pytest.raises(DatasetEvaluacionInvalido, match="inexistente"):
        validar_dataset(
            {
                "id": "x",
                "items": [
                    {
                        "id": "q1",
                        "question": "¿Cómo riego?",
                        "ground_truth": "La papa en sierra requiere riegos frecuentes en floración.",
                        "crop": "papa",
                        "region": "Junín",
                        "source_documents": ["no-existe.md"],
                    }
                ],
            }
        )


def test_dataset_rechaza_ground_truth_no_trazable() -> None:
    with pytest.raises(DatasetEvaluacionInvalido, match="no aparece"):
        validar_dataset(
            {
                "id": "x",
                "items": [
                    {
                        "id": "q1",
                        "question": "¿Cómo riego?",
                        "ground_truth": "Aplicar un fungicida inventado cada 3 horas.",
                        "crop": "papa",
                        "region": "Junín",
                        "source_documents": ["prueba-riego-papa.md"],
                    }
                ],
            }
        )


def test_filas_ragas_tienen_campos_requeridos() -> None:
    item = cargar_dataset().items[0]
    recuperacion = _RecuperacionFalsa(
        [
            FragmentoRecuperado(
                documento_id="doc-1",
                titulo_documento="Riego",
                fragmento_id="c1",
                extracto="La papa en sierra requiere riegos frecuentes en floración.",
                puntaje_similitud=0.9,
            )
        ]
    )
    muestra = ejecutar_item(item, recuperacion, _GeneracionFalsa())  # type: ignore[arg-type]
    filas = filas_ragas([muestra])
    assert filas[0]["question"] == item.question
    assert filas[0]["ground_truth"] == item.ground_truth
    assert filas[0]["answer"].startswith("FAKE:")
    assert "floración" in filas[0]["contexts"][0]
    assert filas[0]["user_input"] == item.question
    assert filas[0]["reference"] == item.ground_truth
    assert filas[0]["retrieved_contexts"] == filas[0]["contexts"]


def test_preflight_rechaza_template() -> None:
    settings = Settings(_env_file=None, generation_provider="template")
    with pytest.raises(EvaluacionOficialNoEjecutable, match="ollama"):
        exigir_proveedor_ollama(settings)


def test_preflight_ollama_caido_es_error_controlado() -> None:
    settings = Settings(
        _env_file=None,
        generation_provider="ollama",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="modelo-configurado-via-env",
    )

    class _Cliente:
        def get(self, url: str, timeout: int | None = None):
            request = httpx.Request("GET", url)
            raise httpx.ConnectError("connection refused", request=request)

    with pytest.raises(EvaluacionOficialNoEjecutable, match="Ollama no está disponible"):
        exigir_ollama_disponible(settings, cliente_http=_Cliente())


def test_preflight_modelo_ausente() -> None:
    settings = Settings(
        _env_file=None,
        generation_provider="ollama",
        ollama_base_url="http://127.0.0.1:11434",
        ollama_model="modelo-que-no-esta",
    )

    class _Respuesta:
        status_code = 200

        def json(self) -> dict[str, object]:
            return {"models": [{"name": "otro:tag"}]}

    class _Cliente:
        def get(self, url: str, timeout: int | None = None) -> _Respuesta:
            return _Respuesta()

    with pytest.raises(EvaluacionOficialNoEjecutable, match="no está instalado"):
        exigir_ollama_disponible(settings, cliente_http=_Cliente())


def test_configuracion_ragas_documentada() -> None:
    settings = Settings(_env_file=None, generation_provider="ollama", ollama_model="qwen2.5:1.5b")
    config = describir_configuracion(settings)
    assert "faithfulness" in config.metric_names
    assert "llm_context_recall" in config.metric_names
    assert "answer_relevancy" in config.metric_names
    assert config.llm_provider == "ollama"
    assert config.requires_openai_key is False


def test_script_evaluacion_existe() -> None:
    script = Path(__file__).resolve().parents[1] / "evaluation" / "run_baseline.py"
    assert script.is_file()
    source = script.read_text(encoding="utf-8")
    assert "ejecutar_ragas" in source
    assert "exigir_ollama_disponible" in source


def test_construccion_dataset_ragas() -> None:
    from evaluation.pipeline import MuestraPipeline
    from evaluation.ragas_runner import construir_muestras_ragas

    muestra = MuestraPipeline(
        id="q1",
        question="¿Cómo riego?",
        ground_truth="La papa en sierra requiere riegos frecuentes en floración.",
        answer="Riegos frecuentes en floración.",
        contexts=["La papa en sierra requiere riegos frecuentes en floración."],
        crop="papa",
        region="Junín",
        source_documents=["prueba-riego-papa.md"],
        generation_method="ollama",
    )
    dataset = construir_muestras_ragas([muestra])
    assert len(dataset) == 1
    sample = dataset[0]
    assert sample.user_input == muestra.question
    assert sample.reference == muestra.ground_truth
    assert sample.response == muestra.answer
    assert sample.retrieved_contexts == muestra.contexts


def test_ragas_importa_con_compatibilidad() -> None:
    from evaluation.ragas_compat import aplicar_compatibilidad_langchain

    aplicar_compatibilidad_langchain()
    import ragas
    from ragas.metrics import Faithfulness, LLMContextRecall, ResponseRelevancy

    assert ragas.__version__.startswith("0.4")
    assert Faithfulness and LLMContextRecall and ResponseRelevancy
