from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import NewType
from uuid import UUID, uuid4

# --- Typed IDs -------------------------------------------------------------

CharacterId = NewType("CharacterId", int)
CorporationId = NewType("CorporationId", int)
AllianceId = NewType("AllianceId", int)
SystemId = NewType("SystemId", int)
StructureId = NewType("StructureId", int)

# --- Time ------------------------------------------------------------------

@dataclass(frozen=True)
class Timestamp:
    """UTC timestamp wrapper with a few helpers."""

    value: datetime

    @classmethod
    def now(cls) -> "Timestamp":
        return cls(datetime.now(timezone.utc))

    def isoformat(self) -> str:
        return self.value.isoformat()

    def __str__(self) -> str:  # nice for logging / repr
        return self.isoformat()

# --- Message IDs -----------------------------------------------------------

@dataclass(frozen=True)
class MessageId:
    value: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(self.value)
