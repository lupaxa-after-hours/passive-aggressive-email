"""Built-in and user-supplied vocabulary. User files are data, never code."""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
from typing import Any

from lupaxa.passive_aggressive_email.exceptions import DataFileError, TemplateError
from lupaxa.passive_aggressive_email.lexicon import OVERT, SIGNOFFS, WORDS
from lupaxa.passive_aggressive_email.models import VOCABULARY_VERSION
from lupaxa.passive_aggressive_email.patterns import PATTERNS

SLOT_RE = re.compile(r"\{([a-z_]+)\}")
OPTIONAL_RE = re.compile(r"\[([^\[\]]*)\]")
SPECIAL_SLOTS = frozenset({"recipient", "sender", "topic", "deadline", "attempts", "situation"})


@dataclass
class Catalogue:
    """Words and templates the engine is allowed to use."""

    version: str
    words: dict[str, dict[int, list[str]]]
    patterns: dict[str, dict[int, list[tuple[str, bool]]]]
    signoffs: dict[int, list[str]]
    overt: set[str]
    warnings: list[str] = field(default_factory=list)

    def groups(self) -> set[str]:
        """Return pattern group names."""
        return set(self.patterns)

    def slots(self) -> set[str]:
        """Return every placeholder the engine knows."""
        return set(self.words) | set(self.patterns) | set(SPECIAL_SLOTS)

    def choose(
        self,
        group: str,
        level: int,
        rng: Random,
        *,
        plausible: bool,
    ) -> str:
        """Pick one template, preferring the requested intensity."""
        pool = self._pool(self.patterns.get(group, {}), level, plausible)
        if not pool:
            raise TemplateError(f"no usable templates for {group} at level {level}")
        return _weighted(pool, rng)

    def pick(self, category: str, level: int, rng: Random, *, plausible: bool) -> str:
        """Pick one vocabulary item."""
        pool = self._pool(
            {
                lv: [(text, False) for text in items]
                for lv, items in self.words.get(category, {}).items()
            },
            level,
            plausible,
        )
        if not pool:
            raise TemplateError(f"no usable vocabulary for {category} at level {level}")
        return _weighted(pool, rng)

    def signoff(self, level: int, rng: Random, *, plausible: bool) -> str:
        """Pick a sign-off that matches the intensity and the deniability mode."""
        chosen: list[tuple[str, int]] = []
        for item_level, items in self.signoffs.items():
            if item_level > level:
                continue
            weight = _weight(item_level, level)
            for text in items:
                if plausible and text in self.overt:
                    continue
                chosen.append((text, weight))
        if not chosen:
            raise TemplateError("no usable sign-off")
        return _weighted(chosen, rng)

    def _pool(
        self,
        levels: dict[int, list[tuple[str, bool]]],
        level: int,
        plausible: bool,
    ) -> list[tuple[str, int]]:
        chosen: list[tuple[str, int]] = []
        for item_level, items in levels.items():
            if item_level > level:
                continue
            weight = _weight(item_level, level)
            for text, overt in items:
                if plausible and (overt or text in self.overt):
                    continue
                chosen.append((text, weight))
        return chosen


def load_builtin() -> Catalogue:
    """Return the shipped vocabulary."""
    catalogue = Catalogue(
        version=VOCABULARY_VERSION,
        words={
            name: {level: list(items) for level, items in levels.items()}
            for name, levels in WORDS.items()
        },
        patterns={
            name: {level: list(items) for level, items in levels.items()}
            for name, levels in PATTERNS.items()
        },
        signoffs={level: list(items) for level, items in SIGNOFFS.items()},
        overt=set(OVERT),
    )
    _fill_floor(catalogue.patterns)
    _fill_floor(catalogue.words)
    for group, levels in catalogue.patterns.items():
        for level, items in levels.items():
            for text, _overt in items:
                problem = pattern_problem(text, catalogue.slots())
                if problem:
                    raise DataFileError(f"built-in template {group}.{level} is invalid: {problem}")
    return catalogue


def load_catalogue(paths: list[str]) -> Catalogue:
    """Load the built-in catalogue and merge any user files."""
    catalogue = load_builtin()
    loaded = False
    for raw in paths:
        path = Path(raw)
        if not path.is_file():
            raise DataFileError(f"vocabulary or template file not found: {path}")
        _merge_file(path, catalogue)
        loaded = True
    if loaded:
        catalogue.version = f"{VOCABULARY_VERSION}+custom"
    return catalogue


def _fill_floor(mapping: dict[str, dict[int, list[Any]]]) -> None:
    """Give every category a level-1 entry so mild requests still render."""
    for levels in mapping.values():
        if not levels or 1 in levels:
            continue
        mildest = min(levels)
        items = levels[mildest]
        if items and isinstance(items[0], tuple):
            plain = [item for item in items if not item[1]]
            levels[1] = plain or list(items)
        else:
            levels[1] = list(items)


def pattern_problem(text: str, slots: set[str]) -> str | None:
    """Return a reason a template is unsafe, or None when it is usable."""
    depth = 0
    for char in text:
        if char == "[":
            depth += 1
            if depth > 1:
                return "nested optional clauses are not allowed"
        elif char == "]":
            depth -= 1
            if depth < 0:
                return "unbalanced brackets"
    if depth != 0:
        return "unbalanced brackets"
    for match in SLOT_RE.finditer(text):
        name = match.group(1)
        if name not in slots:
            return f"unknown placeholder {{{name}}}"
    if text.count("{") != len(SLOT_RE.findall(text)) or text.count("}") != len(
        SLOT_RE.findall(text)
    ):
        return "invalid placeholder syntax"
    return None


def _merge_file(path: Path, catalogue: Catalogue) -> None:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise DataFileError(f"invalid template file: {path}") from exc
    if not isinstance(data, dict):
        catalogue.warnings.append(f"{path}: ignored because the root is not a table")
        return
    for key, value in data.items():
        if key == "words" and isinstance(value, dict):
            _merge_levels(path, "words", value, catalogue, patterns=False)
        elif key == "patterns" and isinstance(value, dict):
            _merge_levels(path, "patterns", value, catalogue, patterns=True)
        elif key == "signoffs" and isinstance(value, dict):
            _merge_signoffs(path, value, catalogue)
        else:
            catalogue.warnings.append(f"{path}: ignored unknown key {key}")


def _merge_levels(
    path: Path,
    kind: str,
    value: dict[str, object],
    catalogue: Catalogue,
    *,
    patterns: bool,
) -> None:
    for name, raw in value.items():
        found = _read_level_map(path, kind, str(name), raw, catalogue, allow_braces=patterns)
        if patterns:
            kept: dict[int, list[tuple[str, bool]]] = {}
            for level, items in found.items():
                valid: list[tuple[str, bool]] = []
                for text in items:
                    problem = pattern_problem(text, catalogue.slots() | {str(name)})
                    if problem:
                        catalogue.warnings.append(
                            f"{path}: ignored '{text}' in patterns.{name}.{level}: {problem}"
                        )
                        continue
                    valid.append((text, False))
                if valid:
                    kept[level] = valid
            bucket = catalogue.patterns.setdefault(str(name), {})
            for level, pairs in kept.items():
                bucket.setdefault(level, []).extend(pairs)
        else:
            bucket_words = catalogue.words.setdefault(str(name), {})
            for level, items in found.items():
                bucket_words.setdefault(level, []).extend(items)


def _merge_signoffs(path: Path, value: dict[str, object], catalogue: Catalogue) -> None:
    found = _read_level_map(path, "signoffs", "signoff", value, catalogue, allow_braces=False)
    for level, items in found.items():
        catalogue.signoffs.setdefault(level, []).extend(items)


def _read_level_map(
    path: Path,
    kind: str,
    name: str,
    value: object,
    catalogue: Catalogue,
    *,
    allow_braces: bool,
) -> dict[int, list[str]]:
    found: dict[int, list[str]] = {}
    if isinstance(value, list):
        found[2] = _strings(path, f"{kind}.{name}", value, catalogue, allow_braces=allow_braces)
        return found
    if not isinstance(value, dict):
        catalogue.warnings.append(
            f"{path}: ignored {kind}.{name} because it is not a table or list"
        )
        return found
    for key, items in value.items():
        try:
            level = int(str(key))
        except ValueError:
            catalogue.warnings.append(f"{path}: ignored {kind}.{name}.{key} (level must be 1 to 5)")
            continue
        if level < 1 or level > 5:
            catalogue.warnings.append(f"{path}: ignored {kind}.{name}.{key} (level must be 1 to 5)")
            continue
        if not isinstance(items, list):
            catalogue.warnings.append(
                f"{path}: ignored {kind}.{name}.{key} because it is not a list"
            )
            continue
        found[level] = _strings(
            path,
            f"{kind}.{name}.{level}",
            items,
            catalogue,
            allow_braces=allow_braces,
        )
    return found


def _strings(
    path: Path,
    label: str,
    items: list[object],
    catalogue: Catalogue,
    *,
    allow_braces: bool,
) -> list[str]:
    kept: list[str] = []
    for item in items:
        if not isinstance(item, str) or not item.strip():
            catalogue.warnings.append(f"{path}: ignored an empty or non-text entry in {label}")
            continue
        text = " ".join(item.split())
        if not allow_braces and ("{" in text or "}" in text):
            catalogue.warnings.append(
                f"{path}: ignored '{text}' in {label} because it contains braces"
            )
            continue
        kept.append(text)
    return kept


def _weight(item_level: int, requested: int) -> int:
    gap = requested - item_level
    if gap <= 0:
        return 8
    if gap == 1:
        return 3
    return 1


def _weighted(pool: list[tuple[str, int]], rng: Random) -> str:
    names = [text for text, _weight in pool]
    weights = [weight for _text, weight in pool]
    return rng.choices(names, weights=weights, k=1)[0]
