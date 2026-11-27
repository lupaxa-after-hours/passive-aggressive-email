"""Sentence templates. A trailing overt flag marks lines hidden in plausible mode."""

from __future__ import annotations

from typing import Any

# group -> level -> (template, overt)
_RAW: Any = {
    "generate_subject": {
        1: (("Update on {topic}", False), ("Note: {topic}", False)),
        2: (("Checking in on {topic}", False), ("A reminder about {topic}", False)),
        3: (("Following up on {topic}", False), ("Regarding {topic}", False)),
        4: (("Another note on {topic}", False), ("Still outstanding: {topic}", False)),
        5: (("Following up once again on {topic}", True), ("{topic}, still with you", True)),
    },
    "generate_open": {
        1: (("I hope you are well. I am writing about {topic}.", False),),
        2: (("{opening} I wanted to check in on {topic}.", False),),
        3: (("{opening} this note is about {topic}.", False),),
        4: (("{ignored} I am writing again about {topic}.", False),),
        5: (("{already} The subject is still {topic}.", True),),
    },
    "generate_point": {
        1: (("Happy to take this {nudge}.", False),),
        2: (("{disappointment}", False),),
        3: (("{already}", False), ("{disappointment}", False)),
        4: (("{disappointment} {already}", False),),
        5: (("{disappointment}", True), ("{question}", True)),
    },
    "generate_ask": {
        1: (("{question}", False), ("{closing}", False)),
        2: (("Could you come back to me {nudge}?", False),),
        3: (("{question}", False),),
        4: (("Please reply {nudge}.", False),),
        5: (("{closing}", True),),
    },
    "followup_subject": {
        1: (("Following up on {topic}", False),),
        2: (("Following up again on {topic}", False),),
        3: (("Following up once again", False), ("Further to {topic}", False)),
        4: (("Still awaiting a reply on {topic}", False),),
        5: (("Following up once again", True),),
    },
    "followup_open": {
        1: (("I am following up on {attempts} regarding {topic}.", False),),
        2: (("I am writing again about {topic}, further to {attempts}.", False),),
        3: ((("I am following up on {attempts} regarding {topic}, as I have yet to receive a response."), False)),
        4: (("{ignored} this is about {topic}, and it refers to {attempts}.", False),),
        5: ((("I am following up on {attempts} regarding {topic}, which I will now assume has been seen."), True)),
    },
    "followup_point": {
        1: (("Please let me know if you need anything else from me.", False),),
        2: (("{disappointment}", False),),
        3: ((("I appreciate that this may not have reached the top of your list, although it would help to know whether the original request has been reviewed."), False)),
        4: (("{already} {disappointment}", False),),
        5: (("{question}", True),),
    },
    "followup_ask": {
        1: (("{closing}", False),),
        3: (("I look forward to your response.", False),),
        5: (("A reply {nudge} would be welcome.", True),),
    },
    "reminder_subject": {
        1: (("Reminder: {topic}", False),),
        3: (("A further reminder about {topic}", False),),
        5: (("Reminder, again: {topic}", True),),
    },
    "reminder_open": {
        1: (("This is a gentle reminder about {topic}.", False),),
        3: (("{opening} a reminder about {topic}.", False),),
        5: (("{reminder}", True),),
    },
    "reminder_point": {
        1: (("The earlier note still has the detail.", False),),
        3: (("{already}", False),),
        5: (("{disappointment}", True),),
    },
    "reminder_dated": {
        1: (("The timing we discussed was {deadline}.", False),),
        3: (("This was due {deadline}, as previously noted.", False),),
        5: (("The deadline of {deadline} has not moved, even if the work has.", True),),
    },
    "reminder_ask": {
        1: (("{question}", False),),
        3: (("Could you confirm this {nudge}?", False),),
        5: (("{closing}", True),),
    },
    "complaint_subject": {
        1: (("A note about {topic}", False),),
        3: (("Feedback on {topic}", False),),
        5: (("Regarding {topic}", True),),
    },
    "complaint_open": {
        1: (("I wanted to raise {topic} while it is still a small thing.", False),),
        3: (("I am writing about {topic}, which has now come up more than once.", False),),
        5: (("{opening} I am raising {topic} again because the first note did not settle it.", True)),
    },
    "complaint_point": {
        1: (("It would help if we could agree a simple standard.", False),),
        3: (("{disappointment} I would like this handled as ordinary workplace practice.", False),),
        5: (("The pattern around {topic} is now hard to describe as an oversight.", True),),
    },
    "complaint_ask": {
        1: (("Could we agree a way forward on {topic}?", False),),
        3: (("Please treat {topic} as something that needs a change, not another discussion.", False)),
        5: (("{question}", True),),
    },
    "correction_subject": {
        1: (("Clarification on {topic}", False),),
        3: (("Correction: {topic}", False),),
        5: (("Re: {topic}, for clarity", True),),
    },
    "correction_open": {
        1: (("A small clarification on {topic}.", False),),
        3: (("I am more than happy to clarify {topic} again.", False),),
        5: ((("I am more than happy to clarify {topic} again, although the correct version was in the original note."), True)),
    },
    "correction_point": {
        1: (("The earlier document is the one to use.", False),),
        3: (("{already}", False),),
        5: (("{already}", True),),
    },
    "correction_ask": {
        1: (("Please use that version going forward.", False),),
        3: (("I trust this clarifies matters.", False),),
        5: (("I trust this clarifies matters, including the part that was already written down.", True)),
    },
    "deadline_subject": {
        1: (("Update needed: {topic}", False),),
        3: (("Overdue: {topic}", False),),
        5: (("{topic} is still outstanding", True),),
    },
    "deadline_open": {
        1: (("I am writing because {topic} is now overdue.", False),),
        3: (("{opening} {topic} has passed the point we agreed.", False),),
        5: (("I am writing because {topic} is overdue, and the reminder has already been sent.", True)),
    },
    "deadline_dated": {
        1: (("I am writing because {topic} was due {deadline}.", False),),
        3: (("{topic} was due {deadline}, and I have not yet seen it.", False),),
        5: (("The commitment for {topic} was {deadline}. That date has passed.", True),),
    },
    "deadline_point": {
        1: (("A short progress note would be enough.", False),),
        3: (("{disappointment}", False),),
        5: (("If this needs to be re-planned, please say so rather than leave it open.", True),),
    },
    "deadline_ask": {
        1: (("Could you let me know where {topic} now stands?", False),),
        3: (("Please send an update {nudge}.", False),),
        5: (("{escalation}", True),),
    },
    "meeting_unnecessary_subject": {
        1: (("Meeting on {topic}", False),),
        5: (("Another meeting on {topic}", True),),
    },
    "meeting_unnecessary_open": {
        1: (("Thank you for the invitation to discuss {topic}.", False),),
        3: (("Thank you for arranging time on {topic}.", False),),
        5: ((("Thank you for arranging another meeting to discuss the points already covered on {topic}."), True)),
    },
    "meeting_unnecessary_point": {
        1: (("I am not sure we need a meeting if the note already covers it.", False),),
        5: (("I am sure the additional alignment will be invaluable.", True),),
    },
    "meeting_unnecessary_ask": {
        1: (("Could we settle {topic} by email instead?", False),),
        5: (("{question}", True),),
    },
    "meeting_declined_subject": {
        1: (("Unable to attend: {topic}", False),),
        3: (("Declining the meeting on {topic}", False),),
    },
    "meeting_declined_open": {
        1: (("Thank you for the invitation regarding {topic}.", False),),
        3: (("Thank you for the invitation. I will not be attending the meeting on {topic}.", False)),
    },
    "meeting_declined_point": {
        1: (("I am content for the discussion to proceed without me.", False),),
        4: ((("My attendance will not change a decision that the diary invite has already framed."), False)),
    },
    "meeting_declined_ask": {
        1: (("Please send the notes afterwards.", False),),
        3: (("A written summary will be quite enough.", False),),
    },
    "meeting_reschedule_subject": {
        2: (("Reschedule of {topic}", False),),
        4: (("{topic} has moved again", False),),
    },
    "meeting_reschedule_open": {
        2: (("I see the meeting on {topic} has moved.", False),),
        5: (("I see the meeting on {topic} has been rescheduled again.", True),),
    },
    "meeting_reschedule_point": {
        2: (("Please hold the new time if you can.", False),),
        5: (("Another move makes it harder to treat the time as agreed.", True),),
    },
    "meeting_reschedule_ask": {
        2: (("Could you confirm the slot that will actually happen?", False),),
        5: (("{question}", True),),
    },
    "meeting_followup_subject": {
        2: (("Actions from the meeting on {topic}", False),),
        4: (("Still open after the meeting on {topic}", False),),
    },
    "meeting_followup_open": {
        2: (("A note on the actions we noted for {topic}.", False),),
        4: (("{ignored} the actions on {topic} are still open.", False),),
    },
    "meeting_followup_point": {
        2: (("The list itself has not changed.", False),),
        5: (("{already}", True),),
    },
    "meeting_followup_ask": {
        2: (("Could you send progress {nudge}?", False),),
        5: (("{closing}", True),),
    },
    "meeting_attendance_subject": {
        2: (("Do I need to attend {topic}?", False),),
        5: (("Attendance at {topic}", True),),
    },
    "meeting_attendance_open": {
        2: (("Could you confirm whether I am needed for {topic}?", False),),
        5: (("I am unclear what my presence adds to {topic}.", True),),
    },
    "meeting_attendance_point": {
        2: (("I can read the notes if that is enough.", False),),
        5: (("If the decision is already made, my calendar can stay as it is.", True),),
    },
    "meeting_attendance_ask": {
        2: (("Please say if I should decline.", False),),
        5: (("{question}", True),),
    },
    "meeting_summary_subject": {
        2: (("Summary of {topic}", False),),
        5: (("Summary of a meeting about {topic}", True),),
    },
    "meeting_summary_open": {
        2: (("A short summary of the discussion on {topic}.", False),),
        5: (("We met about {topic} and left with the same open points we arrived with.", True),),
    },
    "meeting_summary_point": {
        2: (("The useful next step is a written owner for each action.", False),),
        5: (("The hour itself did not add a decision.", True),),
    },
    "meeting_summary_ask": {
        2: (("Please correct this if I have missed an outcome.", False),),
        5: (("{closing}", True),),
    },
    "reply_subject": {
        1: (("Re: {topic}", False),),
        3: (("Following up on {topic}", False),),
        5: (("Re: {topic}, as previously discussed", True),),
    },
    "reply_chase_open": {
        2: (("I am responding to this: {situation}", False),),
        4: (("{ignored} and I am responding to this: {situation}", False),),
    },
    "reply_chase_point": {
        2: (("I have not yet seen a reply on {topic}.", False),),
        5: (("{disappointment}", True),),
    },
    "reply_chase_ask": {
        2: (("{question}", False),),
        5: (("{closing}", True),),
    },
    "reply_ignored_open": {
        3: (("I am responding to this: {situation}", False),),
        5: (("{already} I am responding to this: {situation}", True),),
    },
    "reply_ignored_point": {
        3: (("The earlier message still has the answer.", False),),
        5: (("{already}", True),),
    },
    "reply_ignored_ask": {
        3: (("Another look at that note should be enough.", False),),
        5: (("{closing}", True),),
    },
    "reply_meeting_open": {
        2: (("I am responding to this: {situation}", False),),
        5: (("On the meeting point, I am responding to this: {situation}", True),),
    },
    "reply_meeting_point": {
        2: (("I would rather settle {topic} in writing.", False),),
        5: (("A further meeting is not the missing ingredient.", True),),
    },
    "reply_meeting_ask": {
        2: (("{question}", False),),
        5: (("{closing}", True),),
    },
    "reply_deadline_open": {
        2: (("I am responding to this: {situation}", False),),
        4: (("{opening} I am responding to this: {situation}", False),),
    },
    "reply_deadline_point": {
        2: (("{topic} still needs an update.", False),),
        5: (("{disappointment}", True),),
    },
    "reply_deadline_ask": {
        2: (("Could you send the status {nudge}?", False),),
        5: (("{closing}", True),),
    },
    "reply_correction_open": {
        2: (("I am responding to this: {situation}", False),),
        5: (("To correct the record, I am responding to this: {situation}", True),),
    },
    "reply_correction_point": {
        2: (("{already}", False),),
        5: (("The correction was in the original note.", True),),
    },
    "reply_correction_ask": {
        2: (("I trust this clarifies matters.", False),),
        5: (("{closing}", True),),
    },
    "reply_general_open": {
        1: (("I am responding to this: {situation}", False),),
        3: (("{opening} I am responding to this: {situation}", False),),
        5: (("{already} I am responding to this: {situation}", True),),
    },
    "reply_general_point": {
        1: (("I wanted to reply properly on {topic}.", False),),
        3: (("{disappointment}", False),),
        5: (("{question}", True),),
    },
    "reply_general_ask": {
        1: (("{closing}", False),),
        3: (("Please tell me what you need in order to close {topic}.", False),),
        5: (("{closing}", True),),
    },
    "replyall_subject": {
        2: (("Re: {topic}", False),),
        5: (("Re: {topic} — for the wider group", True),),
    },
    "replyall_open": {
        2: (("I am sending this to the wider group so there is one record of {topic}.", False),),
        5: ((("I am copying everyone, because the private version of this note about {topic} did not land."), True)),
    },
    "replyall_point": {
        2: (("{already}", False),),
        5: (("To be clear, in front of {management}: {already}", True),),
    },
    "replyall_ask": {
        2: (("Please reply on this thread so the correction stays visible.", False),),
        5: (("I would rather not have needed the extra audience for {topic}.", True),),
    },
    "phrase_reminder": {
        1: (("Just a gentle reminder.", False), ("A light prompt, when you can.", False)),
        3: (("{reminder}", False),),
        5: (("For clarity, I will repeat the information provided earlier.", True),),
    },
    "phrase_disappointment": {
        2: (("{disappointment}", False),),
        4: (("I appreciate that this may not have been immediately obvious.", False),),
        5: (("{disappointment}", True),),
    },
    "phrase_correction": {
        2: (("The earlier version is the correct one.", False),),
        4: (("For clarity, I'll repeat the information provided earlier.", False),),
        5: (("{already}", True),),
    },
    "phrase_followup": {
        2: (("Just circling back on the earlier note.", False),),
        4: (("As outlined in my earlier correspondence, this is still open.", False),),
        5: (("As I'm sure you'll recall from our previous discussions, this is still waiting.", True)),
    },
    "phrase_escalation": {
        2: (("{escalation}", False),),
        4: ((("I've copied in the relevant stakeholders to ensure everyone has the same information."), False)),
        5: (("{escalation}", True),),
    },
    "phrase_gratitude": {
        1: (("{gratitude}", False),),
        5: (("{gratitude}", True),),
    },
    "phrase_disagreement": {
        2: (("I see it differently, and I would rather say so plainly.", False),),
        4: (("I am not sure that reading matches the note we already have.", False),),
        5: (("I will treat that as your view, and the written record as the other view.", True),),
    },
    "phrase_clarification": {
        2: (("For completeness, the earlier note is the one to use.", False),),
        4: (("I trust this clarifies matters.", False),),
        5: (("As I'm sure you're aware, this was already set out.", True),),
    },
    "escalation_line": {
        1: (("Happy to keep this between us for now.", False),),
        2: (("I can include the wider team if that would help.", False),),
        3: (("I've included the wider team for visibility.", False),),
        4: (
            ((("I've copied in the relevant stakeholders to ensure everyone has the same information."), False)),
            ((("Given the continued lack of progress, it seemed appropriate to broaden the conversation."), False)),
        ),
        5: (("{escalation}", True), ("I have copied {management} so this is visible.", True)),
    },
}


def _flatten(levels: Any) -> dict[int, tuple[tuple[str, bool], ...]]:
    """Unwrap the extra tuple layer long strings picked up while being wrapped."""
    fixed: dict[int, tuple[tuple[str, bool], ...]] = {}
    for level, items in levels.items():
        rows: list[tuple[str, bool]] = []
        for item in items:
            current: Any = item
            while isinstance(current, tuple) and len(current) == 1 and isinstance(current[0], tuple):
                current = current[0]
            if isinstance(current, tuple) and len(current) == 2 and isinstance(current[0], str):
                rows.append((current[0], bool(current[1])))
        fixed[int(level)] = tuple(rows)
    return fixed


PATTERNS: dict[str, dict[int, tuple[tuple[str, bool], ...]]] = {name: _flatten(levels) for name, levels in _RAW.items()}
