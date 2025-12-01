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

    # Integration helper: build a stack wired to the Aspirational layer (simpleaichat)
    @classmethod
    def from_config(cls) -> "ACEStack":
        """Construct an ACEStack pre-configured with an Aspirational handler.

        This implementation registers a handler that lazily initializes the
        aspirational layer on first use. Lazy initialization avoids import-time
        failures and makes runtime errors visible in logs while still providing
        a deterministic DummyLLM fallback for local development.
        """
        stack = cls()

        # Holder for lazily-constructed objects
        state: Dict[str, object] = {"initialized": False, "aspirational": None}

        def ensure_initialized() -> None:
            """Attempt to initialize the aspirational layer once."""
            if state["initialized"]:
                return
            state["initialized"] = True  # attempt only once
            try:
                from griffin.ace.aspirational import AspirationalLayer  # late import
                from griffin.infra.llm_simpleaichat import SimpleAIChatLLM

                llm = SimpleAIChatLLM()
                # Ensure underlying AIChat initialized successfully before accepting.
                if getattr(llm, "_ai", None) is not None:
                    state["aspirational"] = AspirationalLayer(llm=llm)
                    logger.info("Initialized AspirationalLayer with SimpleAIChatLLM.")
                    return
                logger.info("SimpleAIChatLLM created but underlying AIChat is not available; will try DummyLLM fallback.")
            except Exception as exc:
                logger.info("SimpleAIChatLLM unavailable or failed to initialize: %s", exc)

            # Try dummy fallback
            try:
                from griffin.infra.llm_dummy import DummyLLM
                from griffin.ace.aspirational import AspirationalLayer  # ensure prompt import

                llm = DummyLLM()
                state["aspirational"] = AspirationalLayer(llm=llm)
                logger.info("Initialized AspirationalLayer with DummyLLM fallback.")
                return
            except Exception as exc2:
                logger.exception("Failed to initialize DummyLLM fallback: %s", exc2)
                state["aspirational"] = None

        def aspirational_handler(msg: ACEMessage) -> ACEMessage:
            """Handler which routes 'ace:' prefixed messages to AspirationalLayer (lazy init)."""
            text = (msg.content or "").strip()
            if not text.lower().startswith("ace:"):
                return ACEMessage(
                    source="ace-stack",
                    role="agent",
                    channel=msg.channel,
                    content=f"echo: {msg.content}",
                    meta={"in_reply_to": str(msg.id)},
                )

            # Ensure we have an aspirational implementation
            ensure_initialized()
            aspirational = state.get("aspirational")
            if aspirational is None:
                # final fallback: echo and log
                logger.warning("Aspirational layer not available; falling back to echo.")
                return ACEMessage(
                    source="ace-stack",
                    role="agent",
                    channel=msg.channel,
                    content=f"echo: {msg.content}",
                    meta={"in_reply_to": str(msg.id)},
                )

            cleaned = text.split(":", 1)[1].strip()
            inner = ACEMessage(
                source=msg.source,
                role=msg.role,
                channel=msg.channel,
                content=cleaned,
                meta=dict(msg.meta),
            )
            return aspirational.evaluate(inner, telemetry={})

        stack.register_handler("aspirational", aspirational_handler)
        return stack
