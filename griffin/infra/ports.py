from __future__ import annotations

from typing import Any, Mapping, Protocol

class HTTPPort(Protocol):
    """Minimal sync HTTP abstraction for services."""

    def get_json(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        ...
