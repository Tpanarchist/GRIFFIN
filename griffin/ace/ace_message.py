"""
Minimal ACE message schema used by the ACE orchestrator.
"""
from typing import Any, Dict
from pydantic import BaseModel


class ACEMessage(BaseModel):
    kind: str
    payload: Dict[str, Any] = {}
