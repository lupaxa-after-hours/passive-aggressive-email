"""Command-line interface for passive-aggressive-email."""

from __future__ import annotations

import argparse
import contextlib
import os
import sys
import traceback
from pathlib import Path

from lupaxa.passive_aggressive_email.catalogue import Catalogue, load_catalogue
from lupaxa.passive_aggressive_email.config import Settings, discover_config, load_settings
from lupaxa.passive_aggressive_email.exceptions import (
    IOProblem,
    PassiveAggressiveEmailError,
    UsageError,
)
from lupaxa.passive_aggressive_email.formatting import render_result
from lupaxa.passive_aggressive_email.models import (
    COMPLAINT_CATEGORIES,
    FORMATS,
    GREETINGS,
    MAX_ATTEMPTS,
    MAX_COUNT,
    MAX_LEVEL,
    MAX_PARAGRAPHS,
    MEETING_TYPES,
    MIN_ATTEMPTS,
    MIN_COUNT,
    MIN_LEVEL,
    MIN_PARAGRAPHS,
    PHRASE_CATEGORIES,
    VOCABULARY_VERSION,
)
from lupaxa.passive_aggressive_email.service import (
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
from lupaxa.passive_aggressive_email.version import get_version


def main(argv: list[str] | None = None) -> int:
    """Run one command. Returns a process exit code."""
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return int(code) if isinstance(code, int) else 2
    try:
        return _run(args)
    except BrokenPipeError:
        with contextlib.suppress(OSError):
            sys.stdout.close()
        return 0
    except PassiveAggressiveEmailError as exc:
        print(f"error: {exc}", file=sys.stderr)
        if args.verbose:
            traceback.print_exc(file=sys.stderr)
        return exc.code
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        if getattr(args, "verbose", False):
            traceback.print_exc(file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    """Return the passive-aggressive-email argument parser."""
    parser = argparse.ArgumentParser(
        prog="passive-aggressive-email",
        description=(
            "Generate professionally polite, passive-aggressive workplace email. Nothing is sent."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"passive-aggressive-email {get_version()}"
    )
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--config", help="TOML configuration file.")
    shared.add_argument("--format", dest="output_format", help="text, json, or markdown.")
    shared.add_argument("--output", help="Write the result to this file.")
    shared.add_argument("--force", action="store_true", help="Overwrite an existing output file.")
    shared.add_argument("--verbose", action="store_true", help="Print diagnostics on stderr.")
    shared.add_argument("--quiet", action="store_true", help="Hide warnings.")
    shared.add_argument("--colour", action="store_true", help="Colour text labels.")
    shared.add_argument("--no-colour", action="store_true", help="Do not colour text labels.")
    shared.add_argument("--seed", type=int, default=None, help="Repeatable random seed.")

    generated = argparse.ArgumentParser(add_help=False, parents=[shared])
    generated.add_argument(
        "--level", type=_level, default=None, help="Passive-aggression level, 1 to 5."
    )
    generated.add_argument(
        "--count", type=_count, default=None, help=f"How many results, {MIN_COUNT} to {MAX_COUNT}."
    )
    generated.add_argument(
        "--plausible", action="store_true", help="Keep the irritation professionally deniable."
    )
    generated.add_argument(
        "--no-plausible", action="store_true", help="Allow more pointed wording."
    )

    mail = argparse.ArgumentParser(add_help=False, parents=[generated])
    mail.add_argument("--recipient", default=None, help="Recipient name, inserted as literal text.")
    mail.add_argument("--sender", default=None, help="Sender name, inserted as literal text.")
    mail.add_argument("--topic", default=None, help="Subject matter, inserted as literal text.")
    mail.add_argument("--paragraphs", type=_paragraphs, default=None, help="Body paragraph count.")
    mail.add_argument(
        "--greeting", choices=GREETINGS, default=None, help="hi, hello, dear, or team."
    )

    dated = argparse.ArgumentParser(add_help=False)
    dated.add_argument(
        "--deadline",
        default=argparse.SUPPRESS,
        help="Deadline text, inserted literally. No date is invented.",
    )
    dated.add_argument(
        "--due", dest="deadline", default=argparse.SUPPRESS, help="Same as --deadline."
    )

    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("generate", parents=[mail], help="Generate a workplace email.")

    follow = commands.add_parser(
        "followup", parents=[mail, dated], help="Chase an unanswered request."
    )
    follow.add_argument(
        "--attempts", type=_attempts, default=1, help="How many earlier emails to mention."
    )

    commands.add_parser(
        "reminder", parents=[mail, dated], help="Remind someone of an existing request."
    )

    complaint_parser = commands.add_parser(
        "complaint", parents=[mail], help="Write a polite complaint."
    )
    complaint_parser.add_argument("--category", default="random", help="Complaint category.")

    commands.add_parser("correction", parents=[mail], help="Correct a mistake, politely.")

    due = commands.add_parser("deadline", parents=[mail, dated], help="Chase overdue work.")
    due.add_argument(
        "--attempts", type=_attempts, default=1, help="How many earlier chases to mention."
    )

    meeting_parser = commands.add_parser("meeting", parents=[mail], help="Respond to a meeting.")
    meeting_parser.add_argument("--type", dest="kind", default="random", help="Meeting situation.")

    reply_parser = commands.add_parser("reply", parents=[mail], help="Reply to a short situation.")
    reply_parser.add_argument(
        "text", nargs="?", help="The situation. Read from stdin when omitted."
    )

    phrases_parser = commands.add_parser(
        "phrases", parents=[generated], help="Print standalone lines."
    )
    phrases_parser.add_argument("--category", default="random", help="Phrase category.")

    translate_parser = commands.add_parser(
        "translate", parents=[shared], help="Soften a direct sentence."
    )
    translate_parser.add_argument(
        "text", nargs="?", help="The sentence. Read from stdin when omitted."
    )
    translate_parser.add_argument(
        "--level", type=_level, default=None, help="Passive-aggression level, 1 to 5."
    )

    commands.add_parser("signoff", parents=[generated], help="Print a sign-off.")
    commands.add_parser(
        "escalation", parents=[generated], help="Suggest copying a wider audience. Nothing is sent."
    )
    commands.add_parser("reply-all", parents=[mail], help="Write an awkwardly public email.")
    return parser


def _run(args: argparse.Namespace) -> int:
    if args.verbose and args.quiet:
        raise UsageError("choose either --verbose or --quiet")
    if args.colour and args.no_colour:
        raise UsageError("choose either --colour or --no-colour")
    if getattr(args, "plausible", False) and getattr(args, "no_plausible", False):
        raise UsageError("choose either --plausible or --no-plausible")
    path = discover_config(args.config)
    settings = load_settings(path) if path else Settings()
    level = settings.level if getattr(args, "level", None) is None else args.level
    count = settings.count if getattr(args, "count", None) is None else args.count
    paragraphs = (
        settings.paragraphs if getattr(args, "paragraphs", None) is None else args.paragraphs
    )
    output_format = _format(args.output_format, settings)
    sender = settings.sender if getattr(args, "sender", None) in (None, "") else args.sender
    if getattr(args, "sender", None) is None:
        sender = settings.sender
    greeting = settings.greeting if getattr(args, "greeting", None) is None else args.greeting
    plausible = settings.plausible
    if getattr(args, "plausible", False):
        plausible = True
    if getattr(args, "no_plausible", False):
        plausible = False
    catalogue = load_catalogue([*settings.vocabulary, *settings.templates])
    if catalogue.warnings and not args.quiet:
        for warning in catalogue.warnings:
            print(f"warning: {warning}", file=sys.stderr)
    payload = _dispatch(
        args,
        level=level,
        count=count,
        paragraphs=paragraphs,
        sender=sender,
        greeting=greeting,
        plausible=plausible,
        catalogue=catalogue,
    )
    payload["mode"] = args.command
    payload["vocabulary_version"] = catalogue.version or VOCABULARY_VERSION
    if args.seed is not None and "seed" not in payload:
        payload["seed"] = args.seed
    if args.verbose:
        print(
            f"passive-aggressive-email: command={args.command} level={payload.get('level', '')} "
            f"format={output_format} vocabulary={catalogue.version}",
            file=sys.stderr,
        )
    text = render_result(payload, output_format, colour=_use_colour(args, settings, output_format))
    _emit(text, args.output, args.force)
    return 0


def _dispatch(
    args: argparse.Namespace,
    *,
    level: int,
    count: int,
    paragraphs: int,
    sender: str,
    greeting: str,
    plausible: bool,
    catalogue: Catalogue,
) -> dict[str, object]:
    """Build the structured result for one command."""
    command = args.command
    shared = {
        "level": level,
        "count": count,
        "paragraphs": paragraphs,
        "sender": sender,
        "greeting_style": greeting,
        "plausible": plausible,
        "seed": args.seed,
        "catalogue": catalogue,
        "recipient": getattr(args, "recipient", None) or "",
        "topic": getattr(args, "topic", None) or "",
        "deadline": getattr(args, "deadline", None) or "",
    }
    if command == "generate":
        results = generate(**shared)
    elif command == "followup":
        results = followup(attempts=args.attempts, **shared)
    elif command == "reminder":
        results = reminder(**shared)
    elif command == "complaint":
        _known(args.category, COMPLAINT_CATEGORIES, "complaint category")
        results = complaint(category=args.category, **shared)
    elif command == "correction":
        results = correction(**shared)
    elif command == "deadline":
        results = deadline(attempts=args.attempts, **shared)
    elif command == "meeting":
        _known(args.kind, MEETING_TYPES, "meeting type")
        results = meeting(kind=args.kind, **shared)
    elif command == "reply":
        results = reply(situation=_text_input(args), **shared)
    elif command == "reply-all":
        results = reply_all(**shared)
    elif command == "phrases":
        _known(args.category, PHRASE_CATEGORIES, "phrase category")
        lines = phrases(
            category=args.category,
            level=level,
            count=count,
            seed=args.seed,
            plausible=plausible,
            catalogue=catalogue,
        )
        return _phrase_payload(level, plausible, args.category, lines)
    elif command == "signoff":
        lines = signoffs(
            level=level, count=count, seed=args.seed, plausible=plausible, catalogue=catalogue
        )
        return _phrase_payload(level, plausible, "signoff", lines)
    elif command == "escalation":
        lines = escalations(
            level=level, count=count, seed=args.seed, plausible=plausible, catalogue=catalogue
        )
        return _phrase_payload(level, plausible, "escalation", lines)
    elif command == "translate":
        rewritten = translate(_text_input(args), level=level)
        return {"level": level, "plausible": False, "results": [rewritten], "text": rewritten}
    else:
        raise UsageError(f"unknown command {command}")
    return {"level": level, "plausible": plausible, "results": results}


def _phrase_payload(
    level: int, plausible: bool, situation: str, lines: list[str]
) -> dict[str, object]:
    return {"level": level, "plausible": plausible, "situation": situation, "results": lines}


def _text_input(args: argparse.Namespace) -> str:
    if getattr(args, "text", None):
        return str(args.text)
    if sys.stdin.isatty():
        raise UsageError("missing input text")
    try:
        incoming = sys.stdin.read()
    except OSError as exc:
        raise UsageError("missing input text") from exc
    if not incoming.strip():
        raise UsageError("missing input text")
    return incoming


def _emit(text: str, output: str | None, force: bool) -> None:
    if not output:
        sys.stdout.write(text)
        return
    path = Path(output)
    if path.exists() and not force:
        raise IOProblem(f"output file already exists: {path}")
    if path.is_dir():
        raise IOProblem(f"output path is a directory: {path}")
    try:
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise IOProblem(f"could not write {path}: {exc.strerror or exc}") from exc


def _format(value: str | None, settings: Settings) -> str:
    chosen = settings.output_format if value is None else value
    if chosen not in FORMATS:
        raise UsageError("format must be text, json, or markdown")
    return chosen


def _use_colour(args: argparse.Namespace, settings: Settings, output_format: str) -> bool:
    if args.no_colour or os.environ.get("NO_COLOR"):
        return False
    if args.colour:
        return output_format == "text" and not args.output and sys.stdout.isatty()
    return bool(
        settings.colour and output_format == "text" and not args.output and sys.stdout.isatty()
    )


def _known(value: str, allowed: tuple[str, ...], label: str) -> None:
    if value not in allowed:
        raise UsageError(f"unknown {label} {value!r}")


def _level(value: str) -> int:
    return _range(value, MIN_LEVEL, MAX_LEVEL, "level")


def _count(value: str) -> int:
    return _range(value, MIN_COUNT, MAX_COUNT, "count")


def _paragraphs(value: str) -> int:
    return _range(value, MIN_PARAGRAPHS, MAX_PARAGRAPHS, "paragraphs")


def _attempts(value: str) -> int:
    return _range(value, MIN_ATTEMPTS, MAX_ATTEMPTS, "attempts")


def _range(value: str, low: int, high: int, name: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{name} must be an integer") from exc
    if number < low or number > high:
        raise argparse.ArgumentTypeError(f"{name} must be from {low} to {high}")
    return number
