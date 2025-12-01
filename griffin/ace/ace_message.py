from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Literal

from griffin.core.atoms import MessageId, Timestamp

MessageRole = Literal["user", "system", "tool", "agent", "event"]

@dataclass
class ACEMessage:
    """Minimal message primitive flowing through ACE layers."""

    id: MessageId = field(default_factory=MessageId)
    created_at: Timestamp = field(default_factory=Timestamp.now)
    source: str = "cli"
    role: MessageRole = "user"
    channel: str = "default"
    content: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat(),
            "source": self.source,
            "role": self.role,
            "channel": self.channel,
            "content": self.content,
            "meta": dict(self.meta),
        }
