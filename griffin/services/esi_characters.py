from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Optional

from griffin.domain.models import CharacterPublicInfo
from griffin.infra.ports import HTTPPort

class ESICharactersService:
    """High-level wrapper around ESI character endpoints."""

    def __init__(self, http: HTTPPort, base_path: str = "/characters") -> None:
        self._http = http
        self._base_path = base_path.rstrip("/")

    def _build_url(self, character_id: int) -> str:
        # http port might have build_url; if not, just use the full string.
        base = getattr(self._http, "base_url", "").rstrip("/")
        if base:
            return f"{base}{self._base_path}/{character_id}/"
        return f"{self._base_path}/{character_id}/"

    def get_public_character(self, character_id: int) -> CharacterPublicInfo:
        url = self._build_url(character_id)
        data: Mapping[str, Any] = self._http.get_json(url)

        birthday_raw: Optional[str] = data.get("birthday")  # type: ignore[assignment]
        birthday: Optional[datetime] = None

        if birthday_raw:
            # ESI uses ISO8601 with Z
            birthday = datetime.fromisoformat(birthday_raw.replace("Z", "+00:00"))

        return CharacterPublicInfo(
            character_id=character_id,
            name=str(data.get("name", "")),
            corporation_id=data.get("corporation_id"),
            alliance_id=data.get("alliance_id"),
            security_status=data.get("security_status"),
            birthday=birthday,
            race_id=data.get("race_id"),
        )
