from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.agricultural_context import AgriculturalContext


@dataclass(frozen=True)
class CreateAgriculturalContextCommand:
    farmer_id: str
    plot_name: str | None
    crop: str
    region: str
    notes: str | None


@dataclass(frozen=True)
class SelectAgriculturalContextCommand:
    farmer_id: str
    context_id: str


@dataclass(frozen=True)
class AgriculturalContextResult:
    id: str
    farmer_id: str
    plot_name: str | None
    crop: str
    region: str
    notes: str | None
    is_selected: bool
    created_at: str


class CreateAgriculturalContextPort(ABC):
    @abstractmethod
    def execute(self, command: CreateAgriculturalContextCommand) -> AgriculturalContextResult:
        """Crea un contexto agrícola para el agricultor autenticado."""


class ListAgriculturalContextsPort(ABC):
    @abstractmethod
    def execute(self, farmer_id: str) -> list[AgriculturalContextResult]:
        """Lista los contextos del agricultor autenticado."""


class SelectAgriculturalContextPort(ABC):
    @abstractmethod
    def execute(self, command: SelectAgriculturalContextCommand) -> AgriculturalContextResult:
        """Selecciona un contexto propio del agricultor autenticado."""


def context_to_result(context: AgriculturalContext) -> AgriculturalContextResult:
    return AgriculturalContextResult(
        id=context.id,
        farmer_id=context.farmer_id,
        plot_name=context.plot_name,
        crop=context.crop.value,
        region=context.region.value,
        notes=context.notes,
        is_selected=context.is_selected,
        created_at=context.created_at.isoformat(),
    )
