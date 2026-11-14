"""Shared constants for passive-aggressive-email."""

from __future__ import annotations

VOCABULARY_VERSION = "1"

MIN_LEVEL = 1
MAX_LEVEL = 5
MIN_COUNT = 1
MAX_COUNT = 100
MIN_PARAGRAPHS = 1
MAX_PARAGRAPHS = 8
MIN_ATTEMPTS = 1
MAX_ATTEMPTS = 20

FORMATS = ("text", "json", "markdown")
GREETINGS = ("hi", "hello", "dear", "team")

MEETING_TYPES = (
    "unnecessary",
    "declined",
    "reschedule",
    "followup",
    "attendance",
    "summary",
    "random",
)
COMPLAINT_CATEGORIES = (
    "communication",
    "deadline",
    "incomplete",
    "mistakes",
    "etiquette",
    "meetings",
    "responsiveness",
    "general",
    "random",
)
PHRASE_CATEGORIES = (
    "reminder",
    "disappointment",
    "correction",
    "followup",
    "escalation",
    "gratitude",
    "disagreement",
    "clarification",
    "random",
)

EMAIL_MODES = (
    "generate",
    "followup",
    "reminder",
    "complaint",
    "correction",
    "deadline",
    "meeting",
    "reply",
    "reply-all",
)
PHRASE_MODES = ("phrases", "signoff", "escalation")

ATTEMPT_WORDS = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
}

WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
