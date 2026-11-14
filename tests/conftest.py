"""Keep tests away from a developer's real configuration file."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _isolated_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    monkeypatch.delenv("PASSIVE_AGGRESSIVE_EMAIL_CONFIG", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)
    os.environ.pop("NO_COLOR", None)
    return None
