"""Version string shape. Never pin a literal release number."""

from __future__ import annotations

import re

from lupaxa.passive_aggressive_email import __version__, get_version


def test_version_is_semantic() -> None:
    """The package version is a dotted numeric release, with an optional suffix."""
    assert re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.]+)?", __version__)
    assert get_version() == __version__
