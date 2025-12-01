"""
Minimal use-cases for the services layer.
"""
from typing import Dict
from griffin.domain.models import Pilot

def get_whoami(pilot: Pilot) -> Dict[str, str]:
    return {"name": pilot.name, "id": pilot.character_id or ""}
