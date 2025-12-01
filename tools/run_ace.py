from __future__ import annotations

import logging
from griffin.ace.stack import ACEStack
from griffin.ace.ace_message import ACEMessage
from griffin.infra.config import get_config

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    cfg = get_config()
    logging.getLogger(__name__).info("Config: openai_model=%s, openai_api_key_set=%s", cfg.openai_model, bool(cfg.openai_api_key))

    stack = ACEStack.from_config()
    query = "ace: given my goal of safer nullsec roaming, what high-level rules should I adopt?"
    msg = ACEMessage(source="cli", role="user", content=query)
    reply = stack.send(msg)

    print("---- ACE Reply ----")
    print(reply.content)
    print("-------------------")

if __name__ == '__main__':
    main()
