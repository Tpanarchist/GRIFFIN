from __future__ import annotations

import asyncio
import logging
from collections import OrderedDict
from typing import Any, Awaitable, Callable, Dict, Optional, Union

from griffin.ace.ace_message import ACEMessage

logger = logging.getLogger(__name__)
HandlerResult = Union[ACEMessage, Awaitable[ACEMessage]]
Handler = Callable[[ACEMessage], HandlerResult]


class ACEStack:
    """In-process ACE stack with pluggable handlers and async support.

    - Handlers are callables that accept an ACEMessage and return either an
      ACEMessage (sync) or awaitable[ACEMessage] (async).
    - Handlers are registered by name; the first-registered handler will be used
      to process messages. If no handlers are registered, a default echo reply
      is returned (preserves previous behavior).
    """

    def __init__(self) -> None:
        self._handlers: "OrderedDict[str, Handler]" = OrderedDict()

    def register_handler(self, name: str, handler: Handler) -> None:
        """Register a handler under a name. Overwrites existing name."""
        self._handlers[name] = handler
        logger.debug("Registered handler %s", name)

    def unregister_handler(self, name: str) -> None:
        """Remove a handler by name if present."""
        self._handlers.pop(name, None)
        logger.debug("Unregistered handler %s", name)

    async def send_async(self, msg: ACEMessage) -> ACEMessage:
        """Async send: dispatch to the first registered handler or default echo."""
        logger.info("ACEStack received message: %s", msg.to_dict())

        handler = next(iter(self._handlers.values()), None)
        if handler is not None:
            result = handler(msg)
            if asyncio.iscoroutine(result) or isinstance(result, Awaitable):
                reply = await result  # type: ignore[arg-type]
            else:
                reply = result  # type: ignore[assignment]
            logger.info("ACEStack replying with message: %s", reply.to_dict())
            return reply

        # Default echo behavior
        reply = ACEMessage(
            content=f"echo: {msg.content}",
            source="ace-stack",
            role="agent",
            channel=msg.channel,
            meta={"in_reply_to": str(msg.id)},
        )
        logger.info("ACEStack replying with message: %s", reply.to_dict())
        return reply

    def send(self, msg: ACEMessage) -> ACEMessage:
        """Sync-friendly send: runs the async pipeline when necessary."""
        # If an asyncio loop is already running, schedule the coroutine and wait
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Running inside an event loop: create a task and wait synchronously is unsafe.
            # Provide a simple convenience: run the handler synchronously if it's sync,
            # otherwise raise to require explicit async usage.
            handler = next(iter(self._handlers.values()), None)
            if handler is None:
                # default echo behavior
                return ACEMessage(
                    content=f"echo: {msg.content}",
                    source="ace-stack",
                    role="agent",
                    channel=msg.channel,
                    meta={"in_reply_to": str(msg.id)},
                )
            result = handler(msg)
            if asyncio.iscoroutine(result) or isinstance(result, Awaitable):
                raise RuntimeError(
                    "Async handler registered but send() called from running event loop. "
                    "Use send_async() instead."
                )
            return result  # type: ignore[return-value]

        # Not inside running loop: safe to run the async send via asyncio.run
        return asyncio.run(self.send_async(msg))
