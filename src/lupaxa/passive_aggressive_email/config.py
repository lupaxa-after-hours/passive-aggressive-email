"""Optional TOML defaults. The tool runs with no configuration file."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from lupaxa.passive_aggressive_email.exceptions import UsageError
from lupaxa.passive_aggressive_email.models import (
    FORMATS,
    GREETINGS,
    MAX_COUNT,
    MAX_LEVEL,
    MAX_PARAGRAPHS,
    MIN_COUNT,
    MIN_LEVEL,
    MIN_PARAGRAPHS,
)

_KEYS = {
    "level",
    "format",
    "count",
    "paragraphs",
    "sender",
    "greeting",
    "plausible",
    "colour",
    "color",
    "vocabulary",
    "templates",
}


@dataclass
class Settings:
    """Defaults that command-line options can override."""

    level: int = 3
    output_format: str = "text"
    count: int = 1
    paragraphs: int = 3
    sender: str = ""
    greeting: str = "hi"
    plausible: bool = False
    colour: bool = True
    vocabulary: list[str] = field(default_factory=list)
    templates: list[str] = field(default_factory=list)


def load_settings(path: Path) -> Settings:
    """Read a TOML file. Unknown keys and bad types are errors."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise UsageError(f"invalid configuration: {path}") from exc
    if not isinstance(data, dict):
        raise UsageError(f"invalid configuration: {path}")
    unknown = sorted(set(data) - _KEYS)
    if unknown:
        raise UsageError(f"unknown configuration key {unknown[0]!r}")
    if "colour" in data and "color" in data:
        raise UsageError("configuration sets both colour and color")
    settings = Settings()
    if "level" in data:
        settings.level = _bounded(data["level"], MIN_LEVEL, MAX_LEVEL, "level")
    if "format" in data:
        if data["format"] not in FORMATS:
            raise UsageError("configuration format must be text, json, or markdown")
        settings.output_format = str(data["format"])
    if "count" in data:
        settings.count = _bounded(data["count"], MIN_COUNT, MAX_COUNT, "count")
    if "paragraphs" in data:
        settings.paragraphs = _bounded(
            data["paragraphs"], MIN_PARAGRAPHS, MAX_PARAGRAPHS, "paragraphs"
        )
    if "sender" in data:
        settings.sender = _text(data["sender"], "sender")
    if "greeting" in data:
        if data["greeting"] not in GREETINGS:
            raise UsageError("configuration greeting must be hi, hello, dear, or team")
        settings.greeting = str(data["greeting"])
    if "plausible" in data:
        settings.plausible = _bool(data["plausible"], "plausible")
    colour = data.get("colour", data.get("color", settings.colour))
    if "colour" in data or "color" in data:
        settings.colour = _bool(colour, "colour")
    if "vocabulary" in data:
        settings.vocabulary = _paths(path, data["vocabulary"], "vocabulary")
    if "templates" in data:
        settings.templates = _paths(path, data["templates"], "templates")
    return settings


def discover_config(explicit: str | None) -> Path | None:
    """Find the configuration file. A missing default path is not an error."""
    if explicit:
        path = Path(explicit)
        if not path.is_file():
            raise UsageError(f"configuration file not found: {path}")
        return path
    env = os.environ.get("PASSIVE_AGGRESSIVE_EMAIL_CONFIG")
    if env:
        path = Path(env)
        if not path.is_file():
            raise UsageError(f"configuration file not found: {path}")
        return path
    local = Path("passive-aggressive-email.toml")
    if local.is_file():
        return local
    root = os.environ.get("XDG_CONFIG_HOME")
    base = Path(root) if root else Path.home() / ".config"
    path = base / "passive-aggressive-email" / "config.toml"
    if path.is_file():
        return path
    return None


def _bounded(value: object, low: int, high: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise UsageError(f"configuration {name} must be an integer")
    if value < low or value > high:
        raise UsageError(f"configuration {name} must be from {low} to {high}")
    return value


def _text(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise UsageError(f"configuration {name} must be text")
    return value


def _bool(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise UsageError(f"configuration {name} must be true or false")
    return value


def _paths(config: Path, value: object, name: str) -> list[str]:
    raw = [value] if isinstance(value, str) else value
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise UsageError(f"configuration {name} must be a path or a list of paths")
    paths: list[str] = []
    for item in raw:
        path = Path(str(item))
        if not path.is_absolute():
            path = config.parent / path
        paths.append(str(path))
    return paths
