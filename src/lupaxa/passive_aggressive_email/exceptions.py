"""Errors and process exit codes for passive-aggressive-email."""

from __future__ import annotations

EXIT_OK = 0
EXIT_GENERATION = 1
EXIT_USAGE = 2
EXIT_IO = 3
EXIT_DATA = 4


class PassiveAggressiveEmailError(Exception):
    """Base error. ``code`` is the process exit status."""

    code = EXIT_GENERATION


class GenerationError(PassiveAggressiveEmailError):
    """The generator could not produce a result."""

    code = EXIT_GENERATION


class UsageError(PassiveAggressiveEmailError):
    """The arguments or configuration are invalid."""

    code = EXIT_USAGE


class IOProblem(PassiveAggressiveEmailError):
    """An input or output file could not be used."""

    code = EXIT_IO


class DataFileError(PassiveAggressiveEmailError):
    """A vocabulary or template file could not be used."""

    code = EXIT_DATA


class TemplateError(DataFileError):
    """A template placeholder or structure is invalid."""


class VocabularyError(DataFileError):
    """A required vocabulary category is missing or empty."""
