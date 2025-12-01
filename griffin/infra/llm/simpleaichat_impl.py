from __future__ import annotations

from typing import Iterable, Dict, Optional
import logging

try:
    from simpleaichat import AIChat
except Exception:  # pragma: no cover - optional runtime dependency
    AIChat = None  # type: ignore

from griffin.infra.config import get_config


class SimpleAIChatLLM:
    """Adapter for simpleaichat.AIChat.

    This implementation is defensive: it attempts to initialize AIChat and on
    failure leaves a helpful error path so the caller can see diagnostic logs.
    """

    def __init__(
        self,
        *,
        system_default: str = "You are a helpful assistant.",
        temperature_default: float = 0.7,
    ) -> None:
        cfg = get_config()
        import os as _os
        logging.getLogger(__name__).info(
            "LLM init: cfg.openai_api_key set=%s, env.OPENAI_API_KEY set=%s",
            bool(cfg.openai_api_key),
            bool(_os.getenv("OPENAI_API_KEY")),
        )
        self._system_default = system_default
        self._temperature_default = temperature_default
        self._ai = None

        if AIChat is None:
            logging.getLogger(__name__).info(
                "simpleaichat package not available; SimpleAIChatLLM will be disabled."
            )
            return

        # Try to construct AIChat but capture and log any errors so caller sees reason.
        try:
            # If cfg.openai_api_key is None, AIChat will fall back to environment variables.
            self._ai = AIChat(
                api_key=cfg.openai_api_key,
                model=cfg.openai_model,
                console=False,
                save_messages=False,
                system=system_default,
            )
            logging.getLogger(__name__).info("SimpleAIChatLLM initialized with model=%s", cfg.openai_model)
        except Exception as exc:
            # Keep _ai as None and surface logs so failure reason is visible.
            logging.getLogger(__name__).exception("Failed to initialize simpleaichat.AIChat: %s", exc)
            self._ai = None

    def complete(
        self,
        messages: Iterable[Dict[str, str]],
        *,
        system: str | None = None,
        temperature: float | None = None,
    ) -> str:
        """Return a textual completion for the provided chat history.

        If the underlying AIChat failed to initialize, raise a helpful error so
        the caller can see why the aspirational layer fell back to echo.
        """
        if self._ai is None:
            raise RuntimeError(
                "simpleaichat.AIChat unavailable or failed to initialize. "
                "Check that the 'simpleaichat' package is installed and OPENAI_API_KEY "
                "is set in the environment, then try again. See logs for details."
            )

        prompt = "\n".join(m.get("content", "") for m in messages if m.get("role") == "user")
        params = {
            "temperature": self._temperature_default if temperature is None else temperature
        }

        if system:
            return self._ai(prompt, system=system, params=params)
        return self._ai(prompt, params=params)
