"""Allow ``python -m lupaxa.passive_aggressive_email`` to run the CLI."""

from __future__ import annotations

from lupaxa.passive_aggressive_email.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
