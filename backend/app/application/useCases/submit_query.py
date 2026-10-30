from app.application.services.rag_retrieval_service import RagRetrievalService, RetrievedSnippet
from app.domain.entities.evidence import Evidence
from app.domain.entities.query import Query
from app.domain.entities.response import Response
from app.domain.exceptions import SelectedContextNotFoundError
from app.domain.ports.input.submit_query_port import (
    QueryContextResult,
    QueryEvidenceResult,
    SubmitQueryCommand,
    SubmitQueryPort,
    SubmitQueryResult,
)
from app.domain.ports.output.evidence_repository_port import EvidenceRepositoryPort
from app.domain.ports.output.query_repository_port import QueryRepositoryPort
from app.domain.ports.output.text_generation_port import RetrievedPassage, TextGenerationPort
from app.domain.valueObjects.query_text import QueryText


class SubmitQuery(SubmitQueryPort):
    def __init__(
        self,
        query_repository: QueryRepositoryPort,
        text_generation: TextGenerationPort,
        rag_retrieval: RagRetrievalService,
        evidence_repository: EvidenceRepositoryPort,
    ) -> None:
        self._query_repository = query_repository
        self._text_generation = text_generation
        self._rag_retrieval = rag_retrieval
        self._evidence_repository = evidence_repository

    def execute(self, command: SubmitQueryCommand) -> SubmitQueryResult:
        query_text = QueryText(command.text)
        context = self._query_repository.find_selected_context(command.farmer_id)
        if context is None or context.farmer_id != command.farmer_id:
            raise SelectedContextNotFoundError(
                "Debes seleccionar un contexto agrícola antes de consultar"
            )

        query = Query.create(
            farmer_id=command.farmer_id,
            context_id=context.id,
            text=query_text,
        )
        self._query_repository.save_query(query)

        snippets = self._rag_retrieval.retrieve(query.text.value)
        generated = self._text_generation.generate(
            query_text=query.text.value,
            crop=context.crop.value,
            region=context.region.value,
            passages=_passages_from_snippets(snippets),
        )
        response = Response.create(
            query_id=query.id,
            answer_text=generated.answer_text,
            generation_method=generated.generation_method,
        )
        self._query_repository.save_response(response)

        evidences = _evidences_from_snippets(query.id, response.id, snippets)
        if evidences:
            self._evidence_repository.save_all(evidences)

        return SubmitQueryResult(
            id=query.id,
            text=query.text.value,
            answer=response.answer_text,
            generation_method=response.generation_method,
            created_at=query.created_at.isoformat(),
            context=QueryContextResult(
                id=context.id,
                crop=context.crop.value,
                region=context.region.value,
                plot_name=context.plot_name,
            ),
            evidences=tuple(_evidence_result(item) for item in evidences),
        )


def _passages_from_snippets(snippets: list[RetrievedSnippet]) -> list[RetrievedPassage]:
    return [
        RetrievedPassage(title=item.document_title, excerpt=item.excerpt)
        for item in snippets
    ]


def _evidences_from_snippets(
    query_id: str,
    response_id: str,
    snippets: list[RetrievedSnippet],
) -> list[Evidence]:
    evidences: list[Evidence] = []
    for index, snippet in enumerate(snippets, start=1):
        evidences.append(
            Evidence.create(
                query_id=query_id,
                response_id=response_id,
                document_id=snippet.document_id,
                chunk_id=snippet.chunk_id,
                excerpt=snippet.excerpt,
                similarity_score=snippet.similarity_score,
                rank_order=index,
                document_title=snippet.document_title,
            )
        )
    return evidences


def _evidence_result(evidence: Evidence) -> QueryEvidenceResult:
    return QueryEvidenceResult(
        document_id=evidence.document_id,
        document_title=evidence.document_title,
        chunk_id=evidence.chunk_id,
        excerpt=evidence.excerpt,
        similarity_score=evidence.similarity_score,
        rank_order=evidence.rank_order,
    )
