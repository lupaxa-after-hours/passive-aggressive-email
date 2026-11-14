"""Turn a filled template into a readable sentence."""

from __future__ import annotations

import re

from lupaxa.passive_aggressive_email.exceptions import GenerationError

TOPIC_MARK = "\ue000"
RECIPIENT_MARK = "\ue001"
SENDER_MARK = "\ue002"
DEADLINE_MARK = "\ue003"
ATTEMPTS_MARK = "\ue004"
SITUATION_MARK = "\ue005"

_SPACES = re.compile(r"[ \t]+")
_SPACE_BEFORE_PUNCT = re.compile(r" +([,.;:!?])")
_SPACE_AFTER_PUNCT = re.compile(r"([,.;:!?])([A-Za-z])")
_AFTER_STOP = re.compile(r"([.!?])\s+([a-z])")
_THE_THE = re.compile(r"\b([Tt]he)\s+[Tt]he\b")
_ARTICLE = re.compile(r"\b([Aa]n?)\s+([A-Za-z0-9][A-Za-z0-9-]*)")


def polish(text: str, literals: dict[str, str] | None = None, *, stop: bool = True) -> str:
    """Clean spacing and articles. Literal insertions stay character-for-character."""
    inserted: list[str] = []
    for mark, value in (literals or {}).items():
        if mark not in text:
            continue
        cleaned = " ".join(value.split())
        inserted.append(cleaned)
        text = cleaned.join(text.split(mark))
    text = _tidy(text)
    text = _THE_THE.sub(r"\1", text)
    if not any(text.startswith(value) for value in inserted if value):
        text = _capitalise(text)
    text = _AFTER_STOP.sub(lambda match: f"{match.group(1)} {match.group(2).upper()}", text)
    text = _ARTICLE.sub(_fix_article, text)
    if stop:
        text = _ensure_stop(text)
    text = _tidy(text)
    if not text or text in ".!?,":
        raise GenerationError("generated text was empty")
    return text


def _tidy(text: str) -> str:
    text = _SPACES.sub(" ", text.replace("\n", " ")).strip()
    text = _SPACE_BEFORE_PUNCT.sub(r"\1", text)
    text = _SPACE_AFTER_PUNCT.sub(r"\1 \2", text)
    return text.strip()


def _capitalise(text: str) -> str:
    chars = list(text)
    for index, char in enumerate(chars):
        if char.isalpha():
            chars[index] = char.upper()
            break
    return "".join(chars)


def _ensure_stop(text: str) -> str:
    if text and text[-1] not in ".!?,":
        return text + "."
    return text


def _fix_article(match: re.Match[str]) -> str:
    word = match.group(2)
    article = _article_for(word)
    if match.group(1)[0].isupper():
        article = article.capitalize()
    return f"{article} {word}"


def _article_for(word: str) -> str:
    folded = word.casefold()
    if folded.startswith("uni"):
        return "a"
    if folded.startswith(("un", "um", "ul", "up", "ur", "ut", "ug", "hour", "honour", "honest")):
        return "an"
    if folded[:1] in "aeio":
        return "an"
    return "a"
