"""Offline generator of politely irritated workplace email."""

from lupaxa.passive_aggressive_email.exceptions import DataFileError, GenerationError, IOProblem, PassiveAggressiveEmailError, TemplateError, UsageError, VocabularyError
from lupaxa.passive_aggressive_email.service import complaint, correction, deadline, escalations, followup, generate, meeting, phrases, reminder, reply, reply_all, signoffs, translate
from lupaxa.passive_aggressive_email.version import __version__, get_version

__all__ = [
    "DataFileError",
    "GenerationError",
    "IOProblem",
    "PassiveAggressiveEmailError",
    "TemplateError",
    "UsageError",
    "VocabularyError",
    "__version__",
    "complaint",
    "correction",
    "deadline",
    "escalations",
    "followup",
    "generate",
    "get_version",
    "meeting",
    "phrases",
    "reminder",
    "reply",
    "reply_all",
    "signoffs",
    "translate",
]
