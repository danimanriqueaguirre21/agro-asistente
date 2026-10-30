from app.domain.entities.agricultural_context import AgriculturalContext
from app.domain.ports.input.manage_context_port import (
    AgriculturalContextResult,
    CreateAgriculturalContextCommand,
    CreateAgriculturalContextPort,
    context_to_result,
)
from app.domain.ports.output.agricultural_context_repository_port import (
    AgriculturalContextRepositoryPort,
)
from app.domain.valueObjects.crop import Crop
from app.domain.valueObjects.region import Region


class CreateAgriculturalContext(CreateAgriculturalContextPort):
    def __init__(self, context_repository: AgriculturalContextRepositoryPort) -> None:
        self._context_repository = context_repository

    def execute(self, command: CreateAgriculturalContextCommand) -> AgriculturalContextResult:
        context = AgriculturalContext.create(
            farmer_id=command.farmer_id,
            plot_name=command.plot_name,
            crop=Crop(command.crop),
            region=Region(command.region),
            notes=command.notes,
        )
        self._context_repository.save(context)
        return context_to_result(context)
