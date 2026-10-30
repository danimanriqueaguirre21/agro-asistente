from datetime import datetime, timezone
from uuid import uuid4

from app.domain.exceptions import InvalidContextDataError
from app.domain.valueObjects.crop import Crop
from app.domain.valueObjects.region import Region


class AgriculturalContext:
    def __init__(
        self,
        context_id: str,
        farmer_id: str,
        plot_name: str | None,
        crop: Crop,
        region: Region,
        notes: str | None,
        is_selected: bool,
        created_at: datetime,
    ) -> None:
        self.id = context_id
        self.farmer_id = farmer_id
        self.plot_name = plot_name
        self.crop = crop
        self.region = region
        self.notes = notes
        self.is_selected = is_selected
        self.created_at = created_at

    @classmethod
    def create(
        cls,
        farmer_id: str,
        plot_name: str | None,
        crop: Crop,
        region: Region,
        notes: str | None,
    ) -> "AgriculturalContext":
        if not (farmer_id or "").strip():
            raise InvalidContextDataError("El agricultor es obligatorio")
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return cls(
            context_id=str(uuid4()),
            farmer_id=farmer_id.strip(),
            plot_name=_optional_text(plot_name, 120, "El nombre del predio"),
            crop=crop,
            region=region,
            notes=_optional_text(notes, 500, "Las notas"),
            is_selected=False,
            created_at=now,
        )

    def mark_selected(self) -> None:
        self.is_selected = True

    def mark_unselected(self) -> None:
        self.is_selected = False


def _optional_text(value: str | None, max_length: int, label: str) -> str | None:
    if value is None:
        return None
    clean = value.strip()
    if not clean:
        return None
    if len(clean) > max_length:
        raise InvalidContextDataError(f"{label} superan la longitud permitida")
    return clean
