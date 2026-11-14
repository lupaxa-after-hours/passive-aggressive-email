<p align="center">
  <a href="https://github.com/lupaxa-after-hours">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/after-hours/readme-logo.png" alt="After Hours" />
  </a>
</p>

<h1 align="center">Passive Aggressive Email</h1>

Write workplace email that stays polite while the irritation shows through.
Complete notes, follow-ups, reminders, complaints, corrections, deadline
chases, meeting replies, and short phrases. The humour is the courtesy.
Nothing is sent.

It runs entirely offline. No API keys, no model, and no network. Python
3.11+ and the standard library are enough. Names, topics, and deadlines
you supply are copied through as literal text. The tool does not invent
email addresses, and it does not invent a date you did not provide.

The PyPI name is `lupaxa-passive-aggressive-email`. The import path is
`lupaxa.passive_aggressive_email`. The console script is
`passive-aggressive-email`. `lupaxa` is a namespace package — there is
no `lupaxa/__init__.py`.

## What it Does

Each command fills sentence templates from a built-in vocabulary. The
aggression level changes the wording, the implied criticism, and the
sign-off. It does not simply make the email longer.

| Level | Name                   | Behaviour                                                          |
| ----- | ---------------------- | ------------------------------------------------------------------ |
| 1     | Genuinely Polite       | Courteous, with little or no irritation.                           |
| 2     | Subtly Irritated       | A careful reminder, and a hint that this is not the first time.    |
| 3     | Professionally Annoyed | Formal language with the frustration showing. This is the default. |
| 4     | Barely Concealed Fury  | Pointed remarks about delay, omission, and repeated explanation.   |
| 5     | Nuclear Politeness     | Exaggerated courtesy. Still no insults, threats, or profanity.     |

Pass `--seed` when you want the same email again. The same seed, the same
arguments, and the same vocabulary version produce the same text.
`--plausible` keeps the point and drops the lines that would be hard to
defend in a forwarding chain.

## Install

```bash
pip install lupaxa-passive-aggressive-email
```

## Commands

```bash
passive-aggressive-email generate --level 5
passive-aggressive-email followup --attempts 4
passive-aggressive-email reminder --topic "Timesheets"
passive-aggressive-email complaint --topic "Office kitchen"
passive-aggressive-email correction --topic "Incorrect figures"
passive-aggressive-email deadline --due "Last Friday"
passive-aggressive-email meeting --type unnecessary
passive-aggressive-email reply "They ignored my email"
passive-aggressive-email phrases --count 10
passive-aggressive-email translate "You clearly didn't read this"
passive-aggressive-email signoff --level 5
passive-aggressive-email escalation --level 4
passive-aggressive-email reply-all --level 5
passive-aggressive-email generate --plausible --level 5
```

| Command      | What it Writes                                                                |
| ------------ | ----------------------------------------------------------------------------- |
| `generate`   | A complete email. A workplace topic is chosen when you do not supply one.     |
| `followup`   | A chase for an unanswered note. `--attempts` is how many you already sent.    |
| `reminder`   | A reminder about a task or a fact already communicated.                       |
| `complaint`  | Constructive feedback that is clearly annoyed.                                |
| `correction` | A polite correction. It does not invent the day the document went out.        |
| `deadline`   | A chase for overdue work. `--due` and `--deadline` are the same date text.    |
| `meeting`    | A reply to a meeting: question it, decline it, or chase the actions.          |
| `reply`      | A reply to a short situation, as an argument or on stdin.                     |
| `phrases`    | Standalone lines, optionally from one category.                               |
| `translate`  | A direct sentence rewritten in workplace language. Unrecognised text is kept. |
| `signoff`    | Sign-offs for the chosen level.                                               |
| `escalation` | A line about copying a wider audience. Nothing is addressed or sent.          |
| `reply-all`  | An awkwardly public correction or clarification.                              |

Complaint `--category` values: `communication`, `deadline`, `incomplete`,
`mistakes`, `etiquette`, `meetings`, `responsiveness`, `general`, `random`.

Meeting `--type` values: `unnecessary`, `declined`, `reschedule`,
`followup`, `attendance`, `summary`, `random`.

Phrase `--category` values: `reminder`, `disappointment`, `correction`,
`followup`, `escalation`, `gratitude`, `disagreement`, `clarification`,
`random`.

| Flag           | Meaning                                                       |
| -------------- | ------------------------------------------------------------- |
| `--level`      | Passive-aggression intensity, 1 to 5. Default 3.              |
| `--count`      | How many results to generate, 1 to 100.                       |
| `--seed`       | Repeatable generation.                                        |
| `--recipient`  | Recipient name. Omitted names use `Hi there,` or `Hi team,`.  |
| `--sender`     | Name printed under the sign-off.                              |
| `--topic`      | What the email is about.                                      |
| `--deadline`   | Deadline wording. `deadline` also accepts `--due`.            |
| `--attempts`   | Previous follow-ups, 1 to 20.                                 |
| `--paragraphs` | Body paragraphs, 1 to 8. Default 3.                           |
| `--plausible`  | Keep the point, drop the obviously hostile lines.             |
| `--format`     | `text`, `json`, or `markdown`.                                |
| `--output`     | Write the result to a file.                                   |
| `--force`      | Overwrite an existing output file.                            |
| `--verbose`    | Diagnostics on stderr. Tracebacks only appear with this flag. |
| `--quiet`      | Hide warnings.                                                |
| `--config`     | TOML configuration file.                                      |
| `--version`    | Print `passive-aggressive-email x.y.z` and exit 0.            |

`reply` and `translate` classify common workplace wording with offline
keyword rules. When a situation does not match, the reply still includes
the text you supplied. Translation substitutes known phrases once. It
does not keep rewriting its own output.

## Examples

These are the exact texts those seeds print with the built-in vocabulary.

### A Level 5 Email

```bash
passive-aggressive-email generate --level 5 --seed 5
```

```text
Subject: The request that has now been repeated, still with you

Hi there,

The information has not changed since it was first sent. The subject is still the request that has now been repeated.

Is the expectation that I will keep asking?

Should I take the silence as the decision?

Thank you for your continued attention to this matter, whenever that may begin,
```

### A Follow-up

```bash
passive-aggressive-email followup --attempts 3 --topic "Project update" --recipient James --sender Alex --seed 4
```

```text
Subject: Following up once again

Hi James,

I am writing again about Project update, further to my previous three emails.

I appreciate that this may not have reached the top of your list, although it would help to know whether the original request has been reviewed.

I look forward to your response.

Thanks,

Alex
```

### A Reminder

```bash
passive-aggressive-email reminder --topic "Timesheets" --deadline Friday --seed 8
```

```text
Subject: A further reminder about Timesheets

Hi there,

As previously mentioned, a reminder about Timesheets.

This was due Friday, as previously noted.

Is there anything further you need from me?

I look forward to your reply,
```

### A Complaint

```bash
passive-aggressive-email complaint --category etiquette --topic "Office kitchen" --level 4 --seed 2
```

```text
Subject: Feedback on Office kitchen

Hi there,

I am writing about Office kitchen, which has now come up more than once.

Please treat Office kitchen as a shared-space matter rather than a personal exception.

Could we agree a way forward on Office kitchen?

Grateful for an update,
```

### A Correction

```bash
passive-aggressive-email correction --topic "Incorrect figures" --level 5 --seed 3
```

```text
Subject: Re: Incorrect figures, for clarity

Hi there,

I am more than happy to clarify Incorrect figures again, although the correct version was in the original note.

I am more than happy to explain it again, although it was explained the first time.

I trust this clarifies matters, including the part that was already written down.

Thanks,
```

### A Deadline

```bash
passive-aggressive-email deadline --topic "Quarterly report" --due "Last Friday" --seed 6
```

```text
Subject: Overdue: Quarterly report

Hi there,

For the avoidance of doubt, Quarterly report has passed the point we agreed.

Quarterly report was due Last Friday, and I have not yet seen it.

Could you let me know where Quarterly report now stands?

With thanks in advance,
```

### A Meeting

```bash
passive-aggressive-email meeting --type unnecessary --seed 9
```

```text
Subject: Meeting on the unanswered request

Hi there,

Thank you for arranging time on the unanswered request.

I am not sure we need a meeting if the note already covers it.

Could we settle the unanswered request by email instead?

Kind regards,
```

### A Reply

```bash
passive-aggressive-email reply --level 5 --seed 1 "They asked a question I already answered"
```

```text
Subject: Re: the project update, as previously discussed

Hi there,

I would have thought this was already understood. I am responding to this: They asked a question I already answered.

I am more than happy to explain it again, although it was explained the first time.

I remain available for the reply that is still outstanding.

Kind regards,
```

### Phrases

```bash
passive-aggressive-email phrases --count 4 --category reminder --seed 2
```

```text
The requirement has not changed.
Just a gentle reminder.
Circling back on the outstanding item.
A further reminder, as the first one is still open.
```

### Translation

```bash
passive-aggressive-email translate "You didn't read my email"
```

```text
As the relevant information was included in my original correspondence, I would encourage another review of the previous message.
```

```bash
passive-aggressive-email translate "Stop wasting my time" --level 5
```

```text
I would appreciate a more considered approach to how we allocate our collective time moving forward, particularly where the answer has already been provided.
```

A sentence with no matching rule is printed unchanged. Translation does
not use `--seed`.

### Sign-offs

```bash
passive-aggressive-email signoff --level 5 --count 4 --seed 1
```

```text
With thanks,
Thank you for your continued attention to this matter, whenever that may begin,
With every confidence that this will eventually be addressed,
In anticipation of a response,
```

### Escalation

```bash
passive-aggressive-email escalation --level 4 --seed 7
```

```text
I've copied in the relevant stakeholders to ensure everyone has the same information.
```

### Reply All

```bash
passive-aggressive-email reply-all --level 5 --seed 12
```

```text
Subject: Re: the work that was already due — for the wider group

Hi there,

I am copying everyone, because the private version of this note about the work that was already due did not land.

To be clear, in front of the team: The explanation has already been provided.

I would rather not have needed the extra audience for the work that was already due.

Thank you for your continued attention to this matter, whenever that may begin,
```

### Plausible Deniability

The same seed as the level 5 email above, with the overt lines removed.

```bash
passive-aggressive-email generate --plausible --level 5 --seed 5
```

```text
Subject: Another note on the correction that is still outstanding

Hi there,

After several unanswered notes, I am writing again about the correction that is still outstanding.

I am choosing to treat the delay as unintentional. The detail is in the earlier note.

Would it help if I restated what was already clear?

In anticipation of a response,
```

## Output

`--format text` is the default and is safe to copy into a mail client.
`--format json` is the only thing written to stdout for that run:

```bash
passive-aggressive-email generate --seed 11 --recipient James --topic "Missing report" --format json
```

```json
{
  "level": 3,
  "plausible": false,
  "results": [
    {
      "situation": "general",
      "level": 3,
      "plausible": false,
      "subject": "Following up on Missing report",
      "greeting": "Hi James,",
      "paragraphs": [
        "To reiterate the original request, this note is about Missing report.",
        "As I'm sure you're aware, this was already sent.",
        "Has this had a chance to be reviewed?"
      ],
      "signoff": "Kind regards,",
      "text": "Subject: Following up on Missing report\n\nHi James,\n\nTo reiterate the original request, this note is about Missing report.\n\nAs I'm sure you're aware, this was already sent.\n\nHas this had a chance to be reviewed?\n\nKind regards,",
      "recipient": "James"
    }
  ],
  "mode": "generate",
  "vocabulary_version": "1",
  "seed": 11
}
```

The seed is included only when you passed `--seed`. Phrase commands
return a list of strings. `--format markdown` uses a subject line, the
greeting, the paragraphs, and the sign-off.

`--output email.txt` writes the file and leaves an existing file alone
unless you also pass `--force`. Diagnostics and warnings go to stderr.
Colour is used for text labels when stdout is a terminal. `--no-colour`,
or `NO_COLOR`, turns it off.

## Configuration

The tool works with no configuration file. An optional TOML file can set
the defaults. Command-line options win.

```toml
level = 3
format = "text"
count = 1
paragraphs = 3
sender = "Alex"
greeting = "hi"
plausible = false
colour = true
vocabulary = ["extra-words.toml"]
templates = ["extra-patterns.toml"]
```

`greeting` is `hi`, `hello`, `dear`, or `team`. `colour` and `color` are
the same setting. Do not set both.

Search order:

1. `--config`
2. `PASSIVE_AGGRESSIVE_EMAIL_CONFIG`
3. `./passive-aggressive-email.toml`
4. `$XDG_CONFIG_HOME/passive-aggressive-email/config.toml`, or `~/.config/passive-aggressive-email/config.toml`

A missing default file is ignored. A missing file passed with `--config`
is an error. Extra vocabulary and templates are data only. Placeholders
are `{name}` and optional `[ ... ]` clauses. Invalid entries are skipped
with a warning. They are never executed.

## Exit Codes

| Result                       | Exit |
| ---------------------------- | ---- |
| Success                      | 0    |
| Generation failed            | 1    |
| Invalid arguments or config  | 2    |
| Input or output file error   | 3    |
| Vocabulary or template error | 4    |

A closed output pipe is still success. `--help` exits 0.

## Library

```python
from lupaxa.passive_aggressive_email import followup, generate, translate

generate(level=5, count=2, seed=5)
followup(attempts=3, recipient="James", sender="Alex", topic="Project update", seed=4)
translate("You didn't read my email")
```

The same functions back the commands: `generate`, `followup`, `reminder`,
`complaint`, `correction`, `deadline`, `meeting`, `reply`, `phrases`,
`translate`, `signoffs`, `escalations`, and `reply_all`. Pass `seed` when
a caller needs the same result twice.

## Development

```bash
make init
make python-install-dev
make python-check
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
