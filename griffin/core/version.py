from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as _load_version

__all__ = ["__version__", "get_version"]


def get_version() -> str:
    try:
        return _load_version("griffin")
    except PackageNotFoundError:
        # Local / editable installs before packaging
        return "0.1.0"


__version__ = get_version()
