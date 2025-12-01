from __future__ import annotations

from typing import Protocol, Iterable, Dict

class LLMPort(Protocol):
    """Abstract interface for LLM chat backends."""

    def complete(
        self,
        messages: Iterable[Dict[str, str]],
        *,
        system: str | None = None,
        temperature: float | None = None,
        ) -> str:
        """Return a full text completion given a chat history."""
        ...
