"""Offline checks for every command, the seed, and the exit codes."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lupaxa.passive_aggressive_email import (
    complaint,
    correction,
    deadline,
    escalations,
    followup,
    generate,
    meeting,
    phrases,
    reminder,
    reply,
    reply_all,
    signoffs,
    translate,
)
from lupaxa.passive_aggressive_email.catalogue import load_builtin, load_catalogue, pattern_problem
from lupaxa.passive_aggressive_email.cli import main
from lupaxa.passive_aggressive_email.exceptions import DataFileError, TemplateError, UsageError
from lupaxa.passive_aggressive_email.models import WEEKDAYS


def test_builtin_catalogue_loads() -> None:
    """Shipped templates are valid before any user file is involved."""
    catalogue = load_builtin()
    assert catalogue.version == "1"
    assert "generate_open" in catalogue.patterns


def test_every_email_command_and_seed() -> None:
    """Each email command returns a subject, and a seed repeats."""
    calls = [
        lambda: generate(seed=4, count=2),
        lambda: followup(seed=4, attempts=3),
        lambda: reminder(seed=4, topic="Timesheets"),
        lambda: complaint(seed=4, category="etiquette", topic="Office kitchen"),
        lambda: correction(seed=4, topic="Incorrect figures"),
        lambda: deadline(seed=4, deadline="Last Friday", topic="Quarterly report"),
        lambda: meeting(seed=4, kind="unnecessary"),
        lambda: reply(situation="They ignored my email", seed=4),
        lambda: reply_all(seed=4, level=5),
    ]
    for call in calls:
        first = call()
        second = call()
        assert first == second
        assert first[0]["subject"]
        assert "Subject:" in str(first[0]["text"])
        assert "@" not in str(first[0]["text"])


def test_levels_change_signoffs_and_plausible_mode_stays_defensible() -> None:
    """Level 5 can be pointed. Plausible mode keeps the nuclear sign-off out."""
    polite = set(signoffs(level=1, count=20, seed=1))
    nuclear = set(signoffs(level=5, count=30, seed=1))
    deniable = set(signoffs(level=5, count=30, seed=1, plausible=True))
    assert all("patience" not in line.casefold() for line in polite)
    assert any("patience" in line.casefold() for line in nuclear)
    assert all("patience" not in line.casefold() for line in deniable)


def test_followup_attempts_and_literal_names() -> None:
    """Attempt counts and names are copied through, including brace-like text."""
    mail = followup(attempts=3, recipient="Sam {topic}", sender="Alex", seed=2)[0]
    assert "three" in str(mail["text"])
    assert "Sam {topic}" in str(mail["text"])
    assert mail["sender"] == "Alex"
    assert str(mail["text"]).rstrip().endswith("Alex")


def test_deadline_uses_supplied_date_and_correction_invents_none() -> None:
    """A supplied due date appears. A correction does not invent a weekday."""
    chased = deadline(deadline="Last Friday", topic="Quarterly report", seed=1)[0]
    assert "Last Friday" in str(chased["text"])
    fixed = correction(topic="Incorrect figures", seed=3, level=5)[0]
    folded = str(fixed["text"]).casefold()
    assert not any(day in folded for day in WEEKDAYS)


def test_meeting_complaint_and_reply() -> None:
    """Meeting types, complaint flavour, and reply context are honoured."""
    note = meeting(kind="unnecessary", seed=6, level=5)[0]
    assert "meeting" in str(note["subject"]).casefold() or "meeting" in str(note["text"]).casefold()
    kitchen = complaint(category="etiquette", topic="Office kitchen", seed=1)[0]
    assert "Office kitchen" in str(kitchen["text"])
    assert "shared-space" in str(kitchen["text"])
    answered = reply(situation="They asked a question I already answered", seed=1)[0]
    assert "already answered" in str(answered["text"])
    with pytest.raises(UsageError):
        meeting(kind="karaoke")


def test_phrases_translation_signoff_escalation_and_reply_all() -> None:
    """The short commands and the translator stay offline and rule-based."""
    lines = phrases(category="reminder", count=4, seed=3, level=5)
    assert len(lines) == 4
    assert len(set(lines)) >= 1
    assert "review of the previous message" in translate("You didn't read my email", level=3)
    assert "collective time" in translate("Stop wasting my time", level=3)
    assert translate("The cat sat on the mat", level=5) == "The cat sat on the mat"
    assert signoffs(level=1, seed=1)[0].endswith(",")
    assert escalations(level=4, seed=2)
    public = reply_all(level=5, seed=8)[0]
    assert "wider" in str(public["text"]).casefold() or "everyone" in str(public["text"]).casefold() or "group" in str(public["text"]).casefold()


def test_user_template_skips_unknown_placeholders() -> None:
    """Braces are allowed in templates, and unknown names are skipped."""
    path = Path("extra.toml")
    path.write_text(
        "\n".join(
            [
                "[words.opening]",
                '2 = ["As a courtesy,", "bad {verb}", ""]',
                "[patterns.generate_open]",
                '1 = ["Please {not_real} about {topic}.", "Please look at {topic} today."]',
            ]
        ),
        encoding="utf-8",
    )
    catalogue = load_catalogue([str(path)])
    warnings = " ".join(catalogue.warnings)
    assert "unknown placeholder" in warnings
    assert any("Please look at {topic} today." in text for text, _flag in catalogue.patterns["generate_open"][1])
    problem = pattern_problem("Hello {not_real}.", catalogue.slots())
    assert problem is not None
    assert TemplateError.code == 4


def test_invalid_template_file() -> None:
    """Broken TOML is a vocabulary error, not a crash."""
    path = Path("broken.toml")
    path.write_text("this = [", encoding="utf-8")
    with pytest.raises(DataFileError, match="invalid template file"):
        load_catalogue([str(path)])


def test_cli_json_markdown_file_and_config(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    """JSON is valid, files are protected, and the CLI overrides configuration."""
    assert main(["generate", "--seed", "4", "--format", "json", "--quiet"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["mode"] == "generate"
    assert payload["seed"] == 4
    assert payload["results"][0]["subject"]
    assert main(["followup", "--attempts", "2", "--seed", "1", "--format", "markdown"]) == 0
    assert "**Subject:**" in capsys.readouterr().out
    target = tmp_path / "email.txt"
    assert main(["generate", "--seed", "1", "--output", str(target)]) == 0
    assert target.read_text(encoding="utf-8").startswith("Subject:")
    assert main(["generate", "--seed", "1", "--output", str(target)]) == 3
    config = tmp_path / "passive-aggressive-email.toml"
    config.write_text('level = 1\nformat = "json"\ncount = 2\nsender = "Alex"\n', encoding="utf-8")
    assert main(["generate", "--config", str(config), "--seed", "9"]) == 0
    saved = json.loads(capsys.readouterr().out)
    assert saved["level"] == 1
    assert len(saved["results"]) == 2
    assert saved["results"][0]["sender"] == "Alex"


def test_invalid_arguments_and_stdin(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """Bad flags and a missing reply exit 2. Stdin is accepted when it has text."""
    assert main(["generate", "--level", "9"]) == 2
    assert main(["meeting", "--type", "karaoke"]) == 2
    assert main(["reply"]) == 2
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO("Someone ignored my request\n"))
    assert main(["reply", "--seed", "1"]) == 0
    assert "ignored" in capsys.readouterr().out.casefold()
    assert main(["--help"]) == 0
