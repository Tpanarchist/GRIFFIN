"""
Minimal CLI entrypoint for G.R.I.F.F.I.N.

Provides a simple `main()` used by tests and manual invocation.
Keep dependencies minimal for the scaffold.
"""
from __future__ import annotations

from typing import Tuple

from griffin.infra.config import load_config
from griffin.core.version import get_version


def main(argv: Tuple[str, ...] = ()) -> int:
    cfg = load_config()
    ver = get_version()
    banner = f"G.R.I.F.F.I.N. v{ver} — {cfg.app_name}"
    print(banner)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
