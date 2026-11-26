"""Built-in phrases. User files never live here and nothing here is executed."""

from __future__ import annotations

# level -> phrases. Higher levels are more pointed. Overt lines are listed in OVERT.
WORDS: dict[str, dict[int, tuple[str, ...]]] = {
    "opening": {
        1: ("I hope this finds you well.", "A short note from me.", "Just a quick update."),
        2: ("As previously mentioned,", "Just circling back,", "For completeness,"),
        3: (
            "For the avoidance of doubt,",
            "As outlined in my earlier correspondence,",
            "To reiterate the original request,",
        ),
        4: (
            "As I am sure you are aware,",
            "I appreciate this may have been overlooked,",
            "I would have thought this was already understood,",
        ),
        5: (
            "Per my earlier note, which remains unanswered,",
            "With the original request still outstanding,",
            "For the avoidance of any further doubt,",
        ),
    },
    "nudge": {
        1: ("when you have a moment", "at your convenience", "if that still works"),
        2: ("when you are next able", "before this slips further", "so we can close it"),
        3: ("rather than at some later point", "without another reminder", "this week, ideally"),
        4: (
            "before I send this round again",
            "as a priority, not a suggestion",
            "without a further chase",
        ),
        5: (
            "before the silence becomes the answer",
            "at the first opportunity you actually have",
            "today, if that is not too direct",
        ),
    },
    "disappointment": {
        1: ("No urgency beyond the usual.", "Happy to work around your diary."),
        2: ("I appreciate this may have been overlooked.", "I know diaries fill up."),
        3: ("It would help to know the request was seen.", "A short reply would settle it."),
        4: (
            "The lack of a reply is becoming the issue.",
            "This has now been outstanding for some time.",
        ),
        5: (
            "The continued silence is difficult to read as anything but a choice.",
            "I am choosing to treat the delay as unintentional.",
        ),
    },
    "already": {
        1: ("The detail is in the earlier note.", "The original message has the context."),
        2: ("This was covered in the earlier email.", "The previous note still stands."),
        3: (
            "As I'm sure you're aware, this was already sent.",
            "The earlier message has the full request.",
        ),
        4: (
            "I would have thought this was already understood.",
            "The explanation has already been provided.",
        ),
        5: (
            "I am more than happy to explain it again, although it was explained the first time.",
            "The information has not changed since it was first sent.",
        ),
    },
    "gratitude": {
        1: ("Thank you.", "Many thanks.", "With thanks."),
        2: ("Thank you for looking at this.", "Grateful for a reply.", "Thanks in advance."),
        3: (
            "Thank you for your attention to this.",
            "I do appreciate a response.",
            "With thanks for picking this up.",
        ),
        4: (
            "Thank you for any attention this eventually receives.",
            "Grateful for a reply whenever it arrives.",
        ),
        5: (
            "Thank you for your continued attention to this matter, whenever that may begin.",
            "With every confidence that this will eventually be addressed.",
        ),
    },
    "question": {
        1: (
            "Could you confirm when you can look at this?",
            "Would you mind sending a short reply?",
        ),
        2: ("Has this had a chance to be reviewed?", "Is there anything further you need from me?"),
        3: (
            "Are you able to confirm that the original request was read?",
            "Shall I assume this is waiting on you?",
        ),
        4: (
            "Is there a reason this is still unanswered?",
            "Would it help if I restated what was already clear?",
        ),
        5: (
            "Should I take the silence as the decision?",
            "Is the expectation that I will keep asking?",
        ),
    },
    "closing": {
        1: ("I look forward to hearing from you.", "Happy to discuss if useful."),
        2: ("A reply when you can would be welcome.", "I look forward to your response."),
        3: ("I would appreciate a clear answer.", "Please do come back to me on this."),
        4: (
            "I will need a reply rather than another delay.",
            "I look forward to a response that moves this on.",
        ),
        5: (
            "I look forward to your reply, which I trust will now arrive.",
            "I remain available for the reply that is still outstanding.",
        ),
    },
    "escalation": {
        1: ("Happy to keep this between us for now.",),
        2: ("I can copy the wider team if that would help.",),
        3: (
            "I have included the wider team for visibility.",
            "I may need to widen the conversation if this stays open.",
        ),
        4: (
            "I have copied the relevant stakeholders so everyone has the same information.",
            ("Given the continued lack of progress, it seemed appropriate to broaden the conversation."),
        ),
        5: (
            "I have copied the relevant management alias so this is no longer only my problem.",
            "The next note, if one is required, will not be a private one.",
        ),
    },
    "management": {
        1: ("the team", "the people involved"),
        2: ("the wider team", "the relevant colleagues"),
        3: ("the programme lead", "the relevant stakeholders"),
        4: ("the management alias", "the steering group"),
        5: ("the fictional leadership mailbox", "the generic escalation list"),
    },
    "ignored": {
        1: ("In case the earlier note was missed,",),
        2: ("I have not yet seen a reply,",),
        3: ("I appreciate this may have been overlooked,",),
        4: ("This is another chase of a message that has not been answered,",),
        5: ("After several unanswered notes,",),
    },
    "reminder": {
        1: ("Just a gentle reminder.", "A light prompt on the earlier request."),
        2: ("A reminder of what was already agreed.", "Circling back on the outstanding item."),
        3: (
            "A further reminder, as the first one is still open.",
            "The requirement has not changed.",
        ),
        4: (
            "Another reminder, which I had hoped would be unnecessary.",
            "The original instruction still applies.",
        ),
        5: (
            "A reminder of something that should not need reminding.",
            "The request is unchanged, even if the response is not.",
        ),
    },
    "topic": {
        1: (
            "the open request",
            "the outstanding item",
            "the earlier question",
            "the shared action",
        ),
        2: ("the project update", "the missing report", "the timesheets", "the document review"),
        3: (
            "the unanswered request",
            "the overdue action",
            "the figures we already discussed",
            "the meeting actions",
        ),
        4: (
            "the item that is still with you",
            "the work that was already due",
            "the correction that is still outstanding",
        ),
        5: (
            "the request that has now been repeated",
            "the matter that remains exactly where I left it",
        ),
    },
}

SIGNOFFS: dict[int, tuple[str, ...]] = {
    1: ("Kind regards,", "Best wishes,", "Thanks,"),
    2: ("Kind regards,", "Many thanks,", "With thanks,"),
    3: ("Kind regards,", "With thanks in advance,", "I look forward to your reply,"),
    4: ("In anticipation of a response,", "With continued optimism,", "Grateful for an update,"),
    5: (
        "With what remains of my patience,",
        "With every confidence that this will eventually be addressed,",
        "Thank you for your continued attention to this matter, whenever that may begin,",
    ),
}

# Plausible-deniability sign-offs stay outwardly ordinary, including at level 5.
PLAUSIBLE_SIGNOFFS: dict[int, tuple[str, ...]] = {
    1: SIGNOFFS[1],
    2: SIGNOFFS[2],
    3: ("Kind regards,", "With thanks,", "I look forward to your reply,"),
    4: ("Kind regards,", "In anticipation of a response,", "With thanks,"),
    5: (
        "Kind regards,",
        "In anticipation of a response,",
        "With thanks for your attention to this,",
    ),
}

# Lines that are too pointed for plausible-deniability mode.
OVERT = frozenset(
    {
        "before the silence becomes the answer",
        "at the first opportunity you actually have",
        "The continued silence is difficult to read as anything but a choice.",
        "Thank you for your continued attention to this matter, whenever that may begin.",
        "With every confidence that this will eventually be addressed.",
        "I am more than happy to explain it again, although it was explained the first time.",
        "Should I take the silence as the decision?",
        "Is the expectation that I will keep asking?",
        "I look forward to your reply, which I trust will now arrive.",
        "I have copied the relevant management alias so this is no longer only my problem.",
        "The next note, if one is required, will not be a private one.",
        "A reminder of something that should not need reminding.",
        "the matter that remains exactly where I left it",
        "With what remains of my patience,",
        "Thank you for your continued attention to this matter, whenever that may begin,",
        "With every confidence that this will eventually be addressed,",
    }
)

# phrase, minimum level, replacement. Longer needles are applied first.
PHRASES: tuple[tuple[int, str, str], ...] = (
    (1, "you clearly didn't read this", "the relevant information was in the earlier note"),
    (
        3,
        "you clearly didn't read this",
        ("as the relevant information was included in my original correspondence, I would encourage another review of the previous message"),
    ),
    (
        5,
        "you clearly didn't read this",
        ("as the relevant information was included in my original correspondence, another review of that message would be a good use of the time already spent explaining it"),
    ),
    (1, "you didn't read my email", "the relevant information was in my earlier email"),
    (
        3,
        "you didn't read my email",
        ("as the relevant information was included in my original correspondence, I would encourage another review of the previous message"),
    ),
    (
        5,
        "you didn't read my email",
        ("as the relevant information was included in my original correspondence, I would encourage another review of the previous message rather than a further explanation"),
    ),
    (1, "you did not read my email", "the relevant information was in my earlier email"),
    (
        3,
        "you did not read my email",
        ("as the relevant information was included in my original correspondence, I would encourage another review of the previous message"),
    ),
    (1, "stop wasting my time", "I would appreciate a more focused conversation"),
    (
        3,
        "stop wasting my time",
        ("I would appreciate a more considered approach to how we allocate our collective time moving forward"),
    ),
    (
        5,
        "stop wasting my time",
        ("I would appreciate a more considered approach to how we allocate our collective time moving forward, particularly where the answer has already been provided"),
    ),
    (1, "this meeting is pointless", "I am not sure this meeting is the best use of the time"),
    (
        5,
        "this meeting is pointless",
        ("thank you for arranging another meeting to discuss the points already covered extensively in our previous meeting"),
    ),
    (
        3,
        "this meeting is pointless",
        "I am not convinced a further meeting will add to what has already been discussed",
    ),
    (2, "you ignored my email", "I have not yet seen a reply to my earlier email"),
    (4, "you ignored my request", "I have yet to receive a response to the original request"),
)
