"""Restricted template expansion. Placeholders are names, never expressions."""

from __future__ import annotations

import re
from random import Random

from lupaxa.passive_aggressive_email.catalogue import OPTIONAL_RE, SLOT_RE, SPECIAL_SLOTS, Catalogue
from lupaxa.passive_aggressive_email.exceptions import TemplateError
from lupaxa.passive_aggressive_email.polish import ATTEMPTS_MARK, DEADLINE_MARK, RECIPIENT_MARK, SENDER_MARK, SITUATION_MARK, TOPIC_MARK, polish

_MARKS = {
    "topic": TOPIC_MARK,
    "recipient": RECIPIENT_MARK,
    "sender": SENDER_MARK,
    "deadline": DEADLINE_MARK,
    "attempts": ATTEMPTS_MARK,
    "situation": SITUATION_MARK,
}


class Engine:
    """Fill templates from one catalogue and one random stream."""

    def __init__(self, catalogue: Catalogue, rng: Random, level: int, *, plausible: bool, literals: dict[str, str]) -> None:
        self.catalogue = catalogue
        self.rng = rng
        self.level = level
        self.plausible = plausible
        self.literals = literals
        self._avoid: set[str] = set()

    def render(self, group: str, *, stop: bool = True) -> str:
        """Expand one template group into a sentence."""
        self._avoid = set()
        template = self.catalogue.choose(group, self.level, self.rng, plausible=self.plausible)
        text = self.expand(template, depth=0)
        return polish(text, self.literal_marks(), stop=stop)

    def expand(self, template: str, depth: int) -> str:
        """Substitute placeholders. Optional clauses are kept or dropped."""
        if depth > 3:
            raise TemplateError("template nesting is too deep")
        text = OPTIONAL_RE.sub(lambda match: match.group(1) if self.rng.random() < 0.5 else "", template)

        def replace(match: re.Match[str]) -> str:
            return self._slot(match.group(1), depth)

        return SLOT_RE.sub(replace, text)

    def signoff(self) -> str:
        """Return one sign-off, without adding a full stop."""
        return self.catalogue.signoff(self.level, self.rng, plausible=self.plausible)

    def _slot(self, name: str, depth: int) -> str:
        if name in SPECIAL_SLOTS:
            return _MARKS[name]
        if name in self.catalogue.words:
            word = self.catalogue.pick(name, self.level, self.rng, plausible=self.plausible)
            if word.casefold() in self._avoid:
                word = self.catalogue.pick(name, self.level, self.rng, plausible=self.plausible)
            self._avoid.add(word.casefold())
            return word
        if name in self.catalogue.patterns:
            template = self.catalogue.choose(name, self.level, self.rng, plausible=self.plausible)
            return self.expand(template, depth + 1)
        raise TemplateError(f"unknown placeholder {{{name}}}")

    def literal_marks(self) -> dict[str, str]:
        """Return the private-use marks mapped to literal user text."""
        return {
            TOPIC_MARK: self.literals.get("topic", ""),
            RECIPIENT_MARK: self.literals.get("recipient", ""),
            SENDER_MARK: self.literals.get("sender", ""),
            DEADLINE_MARK: self.literals.get("deadline", ""),
            ATTEMPTS_MARK: self.literals.get("attempts", ""),
            SITUATION_MARK: self.literals.get("situation", ""),
        }
