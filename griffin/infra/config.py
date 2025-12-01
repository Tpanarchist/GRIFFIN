"""
Application configuration for G.R.I.F.F.I.N.

Minimal dataclass-based config to avoid external deps in the scaffold.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    app_name: str = "griffin"
    debug: bool = False

def load_config() -> AppConfig:
    return AppConfig()
