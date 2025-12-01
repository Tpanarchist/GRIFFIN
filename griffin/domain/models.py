"""
Minimal domain models for G.R.I.F.F.I.N. used by initial tests.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Pilot:
    name: str
    character_id: Optional[str] = None
