from app.domain.ports.input.manage_context_port import (
    AgriculturalContextResult,
    ListAgriculturalContextsPort,
    context_to_result,
)
from app.domain.ports.output.agricultural_context_repository_port import (
    AgriculturalContextRepositoryPort,
)


class ListAgriculturalContexts(ListAgriculturalContextsPort):
    def __init__(self, context_repository: AgriculturalContextRepositoryPort) -> None:
        self._context_repository = context_repository

    def execute(self, farmer_id: str) -> list[AgriculturalContextResult]:
        contexts = self._context_repository.list_by_farmer(farmer_id)
        return [context_to_result(context) for context in contexts]
