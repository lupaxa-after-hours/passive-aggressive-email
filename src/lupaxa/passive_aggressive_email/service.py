"""High-level generation used by the library and the command-line tool."""

from __future__ import annotations

from random import Random
from typing import Any, TypeAlias

from lupaxa.passive_aggressive_email.catalogue import Catalogue, load_builtin
from lupaxa.passive_aggressive_email.engine import Engine
from lupaxa.passive_aggressive_email.exceptions import UsageError
from lupaxa.passive_aggressive_email.models import ATTEMPT_WORDS, COMPLAINT_CATEGORIES, MEETING_TYPES, PHRASE_CATEGORIES
from lupaxa.passive_aggressive_email.polish import polish
from lupaxa.passive_aggressive_email.translate import translate_text

JsonObject: TypeAlias = dict[str, object]

_REPLY_RULES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("already answered", "already told", "didn't read", "did not read", "clearly didn't"), "ignored"),
    (("ignored", "no reply", "no response", "haven't heard", "didn't reply", "did not reply"), "chase"),
    (("meeting", "pointless", "calendar"), "meeting"),
    (("late", "overdue", "deadline"), "deadline"),
    (("wrong", "incorrect", "mistake"), "correction"),
)

_FLAVOUR: dict[str, str] = {
    "communication": "The difficulty with {topic} is that a clear reply is still missing.",
    "deadline": "The date attached to {topic} has not been met.",
    "incomplete": "What came back on {topic} is not the finished piece.",
    "mistakes": "The same error on {topic} has now appeared more than once.",
    "etiquette": "Please treat {topic} as a shared-space matter rather than a personal exception.",
    "meetings": "{topic} did not need another meeting to remain unresolved.",
    "responsiveness": "Messages about {topic} are still waiting on a response.",
    "general": "This is about {topic}, and it is not a new request.",
}


def generate(**kwargs: Any) -> list[JsonObject]:
    """Return complete emails for a random workplace situation."""
    return _emails("generate", "general", **kwargs)


def followup(*, attempts: int = 1, **kwargs: Any) -> list[JsonObject]:
    """Return chase emails that mention the earlier messages."""
    return _emails("followup", "followup", attempts=attempts, **kwargs)


def reminder(**kwargs: Any) -> list[JsonObject]:
    """Return reminders, with a due date only when one was supplied."""
    return _emails("reminder", "reminder", **kwargs)


def complaint(*, category: str = "random", **kwargs: Any) -> list[JsonObject]:
    """Return a professionally worded complaint."""
    return _emails("complaint", category, categories=COMPLAINT_CATEGORIES, **kwargs)


def correction(**kwargs: Any) -> list[JsonObject]:
    """Return an email that corrects a mistake without inventing a date."""
    return _emails("correction", "correction", **kwargs)


def deadline(**kwargs: Any) -> list[JsonObject]:
    """Return an email about overdue work."""
    return _emails("deadline", "deadline", **kwargs)


def meeting(*, kind: str = "random", **kwargs: Any) -> list[JsonObject]:
    """Return a response to a meeting."""
    return _emails("meeting", kind, categories=MEETING_TYPES, **kwargs)


def reply(*, situation: str, **kwargs: Any) -> list[JsonObject]:
    """Return a reply that keeps the supplied situation as literal text."""
    text = " ".join(situation.split())
    if not text:
        raise UsageError("missing input text")
    kind = _classify(text)
    return _emails(f"reply_{kind}", kind, situation_text=text, **kwargs)


def reply_all(**kwargs: Any) -> list[JsonObject]:
    """Return an awkwardly public workplace email."""
    return _emails("replyall", "reply-all", **kwargs)


def phrases(*, category: str = "random", **kwargs: Any) -> list[str]:
    """Return standalone lines."""
    return _lines("phrase", category, PHRASE_CATEGORIES, **kwargs)


def signoffs(**kwargs: Any) -> list[str]:
    """Return sign-offs for the requested intensity."""
    engine, count = _phrase_engine(**kwargs)
    found: list[str] = []
    for _ in range(count):
        found.append(_unique(found, engine.signoff))
    return found


def escalations(**kwargs: Any) -> list[str]:
    """Return lines about widening the audience. Nothing is sent."""
    return _lines("escalation", "line", ("line",), **kwargs)


def translate(text: str, *, level: int = 3) -> str:
    """Rewrite a direct sentence. The seed is irrelevant: the rules are fixed."""
    return translate_text(text, level=level)


def _emails(
    prefix: str,
    situation: str,
    *,
    categories: tuple[str, ...] | None = None,
    recipient: str = "",
    sender: str = "",
    topic: str = "",
    deadline: str = "",
    attempts: int = 1,
    situation_text: str = "",
    paragraphs: int = 3,
    level: int = 3,
    count: int = 1,
    seed: int | None = None,
    plausible: bool = False,
    greeting_style: str = "hi",
    catalogue: Catalogue | None = None,
    **kwargs: Any,
) -> list[JsonObject]:
    if kwargs:
        unexpected = ", ".join(sorted(kwargs))
        raise UsageError(f"unexpected arguments: {unexpected}")
    rng = Random(seed) if seed is not None else Random()
    book = catalogue or load_builtin()
    emails: list[JsonObject] = []
    seen: set[str] = set()
    for _ in range(count):
        chosen = _choice(rng, situation, categories)
        item = _one_email(
            book,
            rng,
            prefix=prefix,
            situation=chosen,
            recipient=recipient,
            sender=sender,
            topic=topic,
            deadline=deadline,
            attempts=attempts,
            situation_text=situation_text,
            paragraphs=paragraphs,
            level=level,
            plausible=plausible,
            greeting_style=greeting_style,
        )
        text = str(item["text"])
        if text in seen:
            item = _one_email(
                book,
                rng,
                prefix=prefix,
                situation=chosen,
                recipient=recipient,
                sender=sender,
                topic=topic,
                deadline=deadline,
                attempts=attempts,
                situation_text=situation_text,
                paragraphs=paragraphs,
                level=level,
                plausible=plausible,
                greeting_style=greeting_style,
            )
            text = str(item["text"])
        seen.add(text)
        emails.append(item)
    return emails


def _one_email(
    catalogue: Catalogue,
    rng: Random,
    *,
    prefix: str,
    situation: str,
    recipient: str,
    sender: str,
    topic: str,
    deadline: str,
    attempts: int,
    situation_text: str,
    paragraphs: int,
    level: int,
    plausible: bool,
    greeting_style: str,
) -> JsonObject:
    chosen_topic = topic.strip() or catalogue.pick("topic", level, rng, plausible=plausible)
    group = prefix if prefix != "meeting" else f"meeting_{situation}"
    if prefix == "meeting":
        group = f"meeting_{situation}"
    engine = Engine(
        catalogue,
        rng,
        level,
        plausible=plausible,
        literals={
            "topic": chosen_topic,
            "recipient": recipient.strip(),
            "sender": sender.strip(),
            "deadline": deadline.strip(),
            "attempts": _attempts_phrase(attempts),
            "situation": situation_text.strip(),
        },
    )
    subject_group = f"{group}_subject"
    if subject_group not in engine.catalogue.patterns:
        subject_group = "reply_subject"
    subject = _subject_case(engine.render(subject_group, stop=False))
    body = _body(engine, group, paragraphs, deadline=deadline.strip(), situation=situation)
    closing = engine.signoff()
    hello = _greeting(recipient, greeting_style)
    text = _render_text(subject, hello, body, closing, sender.strip())
    item: JsonObject = {
        "situation": situation,
        "level": level,
        "plausible": plausible,
        "subject": subject,
        "greeting": hello,
        "paragraphs": body,
        "signoff": closing,
        "text": text,
    }
    if recipient.strip():
        item["recipient"] = recipient.strip()
    if sender.strip():
        item["sender"] = sender.strip()
    if deadline.strip():
        item["deadline"] = deadline.strip()
    if situation_text.strip():
        item["context"] = situation_text.strip()
    return item


def _body(engine: Engine, group: str, paragraphs: int, *, deadline: str, situation: str) -> list[str]:
    roles = ["open", "point", "ask"]
    if deadline and f"{group}_dated" in engine.catalogue.patterns:
        roles[1] = "dated"
    while len(roles) < paragraphs:
        roles.insert(-1, "point")
    lines = [engine.render(f"{group}_{role}") for role in roles[:paragraphs]]
    flavour = _FLAVOUR.get(situation)
    skip = {"general", "followup", "reminder", "correction", "deadline", "reply-all"}
    if flavour and paragraphs >= 2 and situation not in skip:
        lines[1] = polish(engine.expand(flavour, depth=0), engine.literal_marks())
    return lines


def _lines(prefix: str, category: str, categories: tuple[str, ...], **kwargs: Any) -> list[str]:
    engine, count = _phrase_engine(**kwargs)
    chosen = _choice(engine.rng, category, categories)
    group = f"{prefix}_{chosen}"

    def produce() -> str:
        return engine.render(group)

    found: list[str] = []
    for _ in range(count):
        found.append(_unique(found, produce))
    return found


def _phrase_engine(**kwargs: Any) -> tuple[Engine, int]:
    level = int(kwargs.get("level", 3))
    count = int(kwargs.get("count", 1))
    seed = kwargs.get("seed")
    plausible = bool(kwargs.get("plausible", False))
    catalogue = kwargs.get("catalogue")
    book = catalogue if isinstance(catalogue, Catalogue) else load_builtin()
    rng = Random(seed) if isinstance(seed, int) else Random()
    engine = Engine(book, rng, level, plausible=plausible, literals={})
    return engine, count


def _unique(found: list[str], produce: object) -> str:
    maker = produce if callable(produce) else None
    if maker is None:
        raise UsageError("internal generation error")
    for _ in range(12):
        line = str(maker())
        if line not in found:
            return line
    return str(maker())


def _choice(rng: Random, value: str, categories: tuple[str, ...] | None) -> str:
    if categories is None:
        return value
    allowed = [item for item in categories if item != "random"]
    if value == "random":
        return rng.choice(allowed)
    if value not in allowed:
        kind = "category"
        raise UsageError(f"unknown {kind} {value!r}")
    return value


def _attempts_phrase(attempts: int) -> str:
    if attempts <= 1:
        return "my earlier email"
    word = ATTEMPT_WORDS.get(attempts, str(attempts))
    return f"my previous {word} emails"


def _subject_case(text: str) -> str:
    """Capitalise the first letter of a subject line."""
    chars = list(text)
    for index, char in enumerate(chars):
        if char.isalpha():
            chars[index] = char.upper()
            return "".join(chars)
    return text


def _greeting(recipient: str, style: str) -> str:
    name = recipient.strip()
    if style == "team" or not name:
        if style == "dear" and not name:
            return "Hello,"
        if style == "hello" and not name:
            return "Hello,"
        if style == "team":
            return "Hi team,"
        return "Hi there,"
    if style == "dear":
        return f"Dear {name},"
    if style == "hello":
        return f"Hello {name},"
    return f"Hi {name},"


def _render_text(subject: str, greeting: str, paragraphs: list[str], signoff: str, sender: str) -> str:
    lines = [f"Subject: {subject}", "", greeting, ""]
    for index, paragraph in enumerate(paragraphs):
        if index:
            lines.append("")
        lines.append(paragraph)
    lines.extend(["", signoff])
    if sender:
        lines.extend(["", sender])
    return "\n".join(lines)


def _classify(text: str) -> str:
    folded = text.casefold()
    for needles, kind in _REPLY_RULES:
        if any(needle in folded for needle in needles):
            return kind
    return "general"
