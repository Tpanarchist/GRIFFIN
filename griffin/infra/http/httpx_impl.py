from __future__ import annotations

from typing import Any, Mapping, Optional

import httpx

from griffin.infra.config import get_config
from griffin.infra.ports import HTTPPort

class HTTPXHTTPPort(HTTPPort):
    """Thin httpx-based HTTPPort implementation."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 10.0) -> None:
        cfg = get_config()
        self._client = httpx.Client(timeout=timeout)
        self._base_url = (base_url or cfg.esi_base_url).rstrip("/")

    @property
    def base_url(self) -> str:
        return self._base_url

    def build_url(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return self._base_url + path

    def get_json(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        resp = self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "HTTPXHTTPPort":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
