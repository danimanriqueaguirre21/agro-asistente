from pathlib import Path

import pytest

from app.domain.ports.output.embedding_port import EmbeddingPort
from app.infrastructure.adapters.output.embedding.external_embedding_adapter import (
    EmbeddingProviderNotConfiguredError,
    ExternalEmbeddingAdapter,
)
from app.infrastructure.adapters.output.embedding.local_lexical_embedding_adapter import (
    LocalLexicalEmbeddingAdapter,
)
from app.infrastructure.composition import CompositionRoot
from app.infrastructure.config.settings import Settings

ADAPTER_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "infrastructure"
    / "adapters"
    / "output"
    / "embedding"
    / "external_embedding_adapter.py"
)


def test_composition_root_wires_local_embedding_port_by_default() -> None:
    container = CompositionRoot(Settings(_env_file=None, mysql_database="agro_asistente"))
    assert isinstance(container.embedding_port, EmbeddingPort)
    assert isinstance(container.embedding_port, LocalLexicalEmbeddingAdapter)


def test_composition_root_can_wire_external_embedding_adapter() -> None:
    settings = Settings(_env_file=None, embedding_provider="external")
    container = CompositionRoot(settings)
    assert isinstance(container.embedding_port, ExternalEmbeddingAdapter)


def test_external_adapter_does_not_call_a_real_provider() -> None:
    adapter = ExternalEmbeddingAdapter(api_url="", api_key="", model="")
    with pytest.raises(EmbeddingProviderNotConfiguredError):
        adapter.embed_text("riego de papa")


def test_external_adapter_does_not_hardcode_api_keys() -> None:
    source = ADAPTER_PATH.read_text(encoding="utf-8")
    assert "sk-" not in source
    assert "AIza" not in source
    assert "hf_" not in source


def test_local_embedding_is_deterministic_and_not_empty() -> None:
    adapter = LocalLexicalEmbeddingAdapter(dimension=32)
    first = adapter.embed_text("Riego frecuente de papa en floración")
    second = adapter.embed_text("Riego frecuente de papa en floración")
    other = adapter.embed_text("Control de heladas en sierra")
    assert first == second
    assert len(first) == 32
    assert first != other
    norm = sum(value * value for value in first) ** 0.5
    assert abs(norm - 1.0) < 1e-6


def test_local_embedding_rejects_empty_text() -> None:
    adapter = LocalLexicalEmbeddingAdapter()
    with pytest.raises(ValueError, match="vacío"):
        adapter.embed_text("   ")


def test_local_embedding_adapter_documents_it_is_not_semantic() -> None:
    source = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "infrastructure"
        / "adapters"
        / "output"
        / "embedding"
        / "local_lexical_embedding_adapter.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()
    assert "no es un embedding semántico" in lowered
    assert "openai" not in lowered
    assert "sk-" not in source
