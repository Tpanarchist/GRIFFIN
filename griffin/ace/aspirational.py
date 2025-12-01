from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any, Iterable, Dict

from griffin.ace.ace_message import ACEMessage
from griffin.ace.prompts import ACE_ASPIRATIONAL_SYSTEM_PROMPT
import logging
from typing import Any

@dataclass
class AspirationalLayer:
    llm: Any

    def evaluate(
        self,
        msg: ACEMessage,
        telemetry: Mapping[str, Any] | None = None,
    ) -> ACEMessage:
        """Turn a northbound question into southbound guidance using the LLM.

        The returned ACEMessage is an agent reply containing the LLM's guidance.
        """
        content_lines = [msg.content]
        if telemetry:
            content_lines.append("\\nTelemetry:")
            for k, v in telemetry.items():
                content_lines.append(f"- {k}: {v}")

        messages: Iterable[Dict[str, str]] = [
            {"role": "user", "content": "\\n".join(content_lines)}
        ]

        # Call the configured LLM directly and let any runtime errors surface so they are visible in logs.
        logging.getLogger(__name__).info("Invoking LLM.complete (system prompt applied).")
        guidance = self.llm.complete(
            messages,
            system=ACE_ASPIRATIONAL_SYSTEM_PROMPT,
            temperature=0.0,
        )

        return ACEMessage(
            source="aspirational",
            role="agent",
            channel=msg.channel,
            content=guidance,
            meta={"in_reply_to": str(msg.id), "layer": "aspirational"},
        )
