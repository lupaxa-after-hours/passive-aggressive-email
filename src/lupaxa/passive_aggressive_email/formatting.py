"""Text, Markdown, and JSON rendering."""

from __future__ import annotations

import json
from typing import TypeAlias

JsonObject: TypeAlias = dict[str, object]


def render_result(payload: JsonObject, fmt: str, *, colour: bool = False) -> str:
    """Render a command result. Colour is reserved for a later label and is unused in text."""
    del colour
    if fmt == "json":
        return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    results = payload.get("results")
    if not isinstance(results, list):
        return ""
    if results and isinstance(results[0], str):
        return "\n".join(str(item) for item in results) + "\n"
    blocks = [_email_block(item, fmt) for item in results if isinstance(item, dict)]
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def _email_block(item: JsonObject, fmt: str) -> str:
    if fmt == "markdown":
        return _markdown(item)
    text = item.get("text")
    return str(text) if isinstance(text, str) else ""


def _markdown(item: JsonObject) -> str:
    subject = item.get("subject", "")
    greeting = item.get("greeting", "")
    paragraphs = item.get("paragraphs", [])
    signoff = item.get("signoff", "")
    sender = item.get("sender", "")
    lines = [f"**Subject:** {subject}", "", str(greeting), ""]
    if isinstance(paragraphs, list):
        for paragraph in paragraphs:
            lines.extend([str(paragraph), ""])
    lines.append(str(signoff))
    if sender:
        lines.extend(["", str(sender)])
    return "\n".join(lines).rstrip()
