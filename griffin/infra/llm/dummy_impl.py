from __future__ import annotations

from typing import Iterable, Dict

class DummyLLM:
    """Deterministic local LLM used as a safe fallback when the real LLM fails.

    Returns a concise, structured markdown response suitable for the Aspirational layer.
    """

    def __init__(self, *, system_default: str | None = None, temperature_default: float = 0.0) -> None:
        self.system_default = system_default or "You are a helpful assistant."
        self.temperature_default = temperature_default

    def complete(
        self,
        messages: Iterable[Dict[str, str]],
        *,
        system: str | None = None,
        temperature: float | None = None,
    ) -> str:
        user_text = " ".join(m.get("content", "") for m in messages if m.get("role") == "user")
        # Simple deterministic template that is safe for dev use.
        return (
            "## Objectives\n"
            "- Prioritize safety: avoid engaging unknown fleets and scout exits.\n\n"
            "## Constraints\n"
            "- No direct in-game automation; always require pilot confirmation for risky actions.\n\n"
            "## Guidance\n"
            f"- Recon first: use scouts, safe bookmarks, and prescout systems. Intent: {user_text}\n"
            "- Travel fit: cloaking, directional scanners, safe bookmarks, and preplanned escape routes.\n"
            "- Fleet up when uncertain; avoid solo deep incursions."
        )
