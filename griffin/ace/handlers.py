from __future__ import annotations

import asyncio
from typing import Any

from griffin.ace.ace_message import ACEMessage

async def echo_handler(msg: ACEMessage) -> ACEMessage:
    await asyncio.sleep(0)  # simulate async work
    return ACEMessage(
        content=f"echo-handler: {msg.content}",
        source="echo-handler",
        role="agent",
        channel=msg.channel,
        meta={"in_reply_to": str(msg.id)},
    )
