from __future__ import annotations

import logging
import os
import sys
from functools import lru_cache
from typing import Literal, Optional

from pydantic import BaseModel, Field

EnvName = Literal["dev", "test", "prod"]

class GriffinConfig(BaseModel):
    env: EnvName = Field(default="dev")
    log_level: str = Field(default="INFO")
    esi_base_url: str = Field(
        default="https://esi.evetech.net/latest",
        description="Base URL for ESI calls (no trailing slash).",
    )
    data_dir: str = Field(
        default_factory=lambda: os.getenv("GRIFFIN_DATA_DIR", "data"),
        description="Root directory for cached / derived data.",
    )
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key; if None, AIChat falls back to OPENAI_API_KEY env var.",
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        description="Default OpenAI chat model for ACE/LLM usage.",
    )

@lru_cache(maxsize=1)
def get_config() -> GriffinConfig:
    """Global config singleton built from env vars."""
    return GriffinConfig(
        env=os.getenv("GRIFFIN_ENV", "dev"),  # type: ignore[arg-type]
        log_level=os.getenv("GRIFFIN_LOG_LEVEL", "INFO"),
        openai_api_key=os.getenv("OPENAI_API_KEY", None),
        openai_model=os.getenv("GRIFFIN_OPENAI_MODEL", "gpt-4o-mini"),
    )

def setup_logging(level: Optional[str] = None) -> None:
    """Set up basic logging for CLI / services."""
    cfg = get_config()
    target = (level or cfg.log_level).upper()

    logging.basicConfig(
        level=getattr(logging, target, logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
    )
