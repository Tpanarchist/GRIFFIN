"""
Small, pure atom types used across the project.
Keep implementations minimal for the initial scaffold.
"""
from dataclasses import dataclass
from typing import NewType

ID = NewType("ID", str)


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str = "unit"

    def __repr__(self) -> str:
        return f"{self.value} {self.unit}"
