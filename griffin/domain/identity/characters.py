"""
Minimal domain models for G.R.I.F.F.I.N. used by initial tests.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class Pilot:
    name: str
    character_id: Optional[str] = None

@dataclass
class CharacterPublicInfo:
    character_id: int
    name: str
    corporation_id: Optional[int] = None
    alliance_id: Optional[int] = None
    security_status: Optional[float] = None
    birthday: Optional[datetime] = None
    race_id: Optional[int] = None
