"""Offline phrase substitution. Rules run once, on the original text only."""

from __future__ import annotations

from lupaxa.passive_aggressive_email.exceptions import UsageError
from lupaxa.passive_aggressive_email.lexicon import PHRASES
from lupaxa.passive_aggressive_email.polish import polish


def translate_text(text: str, *, level: int) -> str:
    """Rewrite a direct line. Unrecognised text is returned unchanged."""
    source = " ".join(text.split())
    if not source:
        raise UsageError("missing input text")
    rules = [rule for rule in PHRASES if rule[0] <= level]
    rules.sort(key=lambda rule: (len(rule[1]), rule[0]), reverse=True)
    occupied = [False] * len(source)
    folded = source.casefold()
    spans: list[tuple[int, int, str]] = []
    for _minimum, needle, replacement in rules:
        start = 0
        wanted = needle.casefold()
        while True:
            index = folded.find(wanted, start)
            if index < 0:
                break
            end = index + len(wanted)
            if _free(occupied, index, end) and _boundary(source, index, end):
                spans.append((index, end, replacement))
                for cursor in range(index, end):
                    occupied[cursor] = True
                break
            start = index + 1
    if not spans:
        return source
    spans.sort()
    pieces: list[str] = []
    cursor = 0
    for start, end, replacement in spans:
        pieces.append(source[cursor:start])
        pieces.append(replacement)
        cursor = end
    pieces.append(source[cursor:])
    rewritten = "".join(pieces)
    if rewritten.casefold() == source.casefold():
        return source
    return polish(rewritten)


def _free(occupied: list[bool], start: int, end: int) -> bool:
    return not any(occupied[start:end])


def _boundary(text: str, start: int, end: int) -> bool:
    before = text[start - 1] if start else " "
    after = text[end] if end < len(text) else " "
    return not before.isalnum() and not after.isalnum()
