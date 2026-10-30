from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SubmitQueryCommand:
    farmer_id: str
    text: str


@dataclass(frozen=True)
class QueryContextResult:
    id: str
    crop: str
    region: str
    plot_name: str | None


@dataclass(frozen=True)
class QueryEvidenceResult:
    document_id: str
    document_title: str
    chunk_id: str
    excerpt: str
    similarity_score: float
    rank_order: int


@dataclass(frozen=True)
class SubmitQueryResult:
    id: str
    text: str
    answer: str
    generation_method: str
    created_at: str
    context: QueryContextResult
    evidences: tuple[QueryEvidenceResult, ...]


class SubmitQueryPort(ABC):
    @abstractmethod
    def execute(self, command: SubmitQueryCommand) -> SubmitQueryResult:
        """Registra una consulta agrícola y genera una respuesta inicial."""
