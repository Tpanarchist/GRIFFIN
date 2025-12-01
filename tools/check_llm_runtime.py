from __future__ import annotations

import sys
import traceback
from pathlib import Path

# Ensure project root is on sys.path so 'griffin' package imports work.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from griffin.infra.config import get_config
    from griffin.infra.llm_simpleaichat import SimpleAIChatLLM
except Exception:
    traceback.print_exc()
    sys.exit(2)

def main() -> int:
    cfg = get_config()
    print("Config.openai_api_key present:", bool(cfg.openai_api_key))
    print("Environment OPENAI_API_KEY present:", bool(__import__('os').getenv("OPENAI_API_KEY")))
    print("Config.openai_model:", cfg.openai_model)
    try:
        llm = SimpleAIChatLLM()
        has_ai = getattr(llm, "_ai", None) is not None
        print("SimpleAIChatLLM initialized; underlying AIChat present:", has_ai)
        return 0 if has_ai else 3
    except Exception:
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
