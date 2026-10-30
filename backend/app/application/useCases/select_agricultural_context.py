from app.domain.exceptions import ContextNotFoundError
from app.domain.ports.input.manage_context_port import (
    AgriculturalContextResult,
    SelectAgriculturalContextCommand,
    SelectAgriculturalContextPort,
    context_to_result,
)
from app.domain.ports.output.agricultural_context_repository_port import (
    AgriculturalContextRepositoryPort,
)


class SelectAgriculturalContext(SelectAgriculturalContextPort):
    def __init__(self, context_repository: AgriculturalContextRepositoryPort) -> None:
        self._context_repository = context_repository

    def execute(self, command: SelectAgriculturalContextCommand) -> AgriculturalContextResult:
        selected = self._context_repository.select_for_farmer(
            command.context_id,
            command.farmer_id,
        )
        if selected is None:
            raise ContextNotFoundError("Contexto agrícola no encontrado")
        return context_to_result(selected)
