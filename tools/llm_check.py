from __future__ import annotations

import traceback
import sys

from griffin.infra.llm_simpleaichat import SimpleAIChatLLM
from griffin.infra.config import get_config

def main() -> int:
    cfg = get_config()
    print("Config openai_api_key set:", bool(cfg.openai_api_key))
    print("Config openai_model:", cfg.openai_model)
    try:
        llm = SimpleAIChatLLM()
        has_ai = getattr(llm, "_ai", None) is not None
        print("SimpleAIChatLLM initialized, underlying AIChat present:", has_ai)
        return 0 if has_ai else 2
    except Exception:
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
