from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from griffin.domain.models import CharacterPublicInfo
from griffin.services.esi_characters import ESICharactersService
from griffin.infra.ports import HTTPPort

class FakeHTTP(HTTPPort):
    def __init__(self, payload: Mapping[str, Any]) -> None:
        self._payload = payload
        self.last_url: str | None = None

    def get_json(self, url: str, params: Mapping[str, Any] | None = None) -> Any:
        self.last_url = url
        return dict(self._payload)

def test_get_public_character_maps_fields() -> None:
    payload = {
        "name": "Test Pilot",
        "corporation_id": 123,
        "alliance_id": 456,
        "security_status": 4.2,
        "birthday": "2020-01-02T03:04:05Z",
        "race_id": 7,
    }

    fake_http = FakeHTTP(payload)
    service = ESICharactersService(http=fake_http)

    char = service.get_public_character(42)

    assert isinstance(char, CharacterPublicInfo)
    assert char.character_id == 42
    assert char.name == "Test Pilot"
    assert char.corporation_id == 123
    assert char.alliance_id == 456
    assert char.security_status == 4.2
    assert char.race_id == 7
    assert char.birthday == datetime(2020, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    assert "42" in (fake_http.last_url or "")
