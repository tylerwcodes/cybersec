# Microsoft Azure Administrator AZ-104 Terminal Study Games

An interactive, terminal-based study suite covering **every objective** of the
Microsoft Azure Administrator AZ-104 exam. Pure Python 3 standard library — no
installs, no internet, no dependencies.

## Run it

```bash
cd study-games
python3 az104.py
```

Works on macOS, Linux, and Windows (any Python 3.6+). Progress saves
automatically to `.progress.json` in this folder.

## What's inside

- **15 topic modules** — one per exam objective (1.1 through 5.2), with
  **580+ questions** and **410+ flashcard terms** total.
- **5 question formats** — multiple choice, true/false, fill-in-the-blank,
  matching, and ordering. Choices and match/order items are shuffled every time,
  so you learn the content, not the position of the answer.
- **Every answer teaches** — a 2–4 sentence explanation appears after each
  question whether you got it right or wrong.
- **Miss it, master it** — any quiz, the exam simulator, and the review modes
  end by offering to **review the questions you missed** (with correct answers
  and explanations) and **retake a quiz built only from those misses**. It loops
  on whatever you still get wrong until you've cleared every one. A perfect round
  skips the prompt entirely.

### Per-topic menu

Pick any topic number from the main menu to get:

| Mode | What it does |
|---|---|
| Full quiz | Every question for that objective |
| Quick 10 | A random 10-question sample |
| Flashcards | Self-graded term/definition cards; missed cards recycle |
| Term match | Match terms to definitions against the clock |
| Review missed | Only the questions you've previously gotten wrong |

### Global drills & modes

| Key | Mode | What it does |
|---|---|---|
| **E** | Exam simulator | 50 questions weighted exactly like the real exam (D1 12, D2 10, D3 12, D4 9, D5 7), timed, with a per-domain score report |
| **G** | Azure gym | Infinitely generated problems in 4 levels — subnetting & CIDR (usable IPs, right-size prefixes, reserved addresses), RBAC & scope (least privilege, inheritance), NSG evaluation (priority tables, first match wins, default rules), and HA & redundancy (VM SLAs, fault/update domains, storage copies, access tiers) |
| **S** | Service blitz | 55 admin-level Azure services — name the service from its description and categorize it, with streak bonuses |
| **A** | Acronym blitz | 60 AZ-104 acronyms and short names, fuzzy-graded |
| **V** | Vocab arcade | Every term from all 15 topics plus a curated bank of 32 commonly-confused pairs (NSG vs ASG, Load Balancer vs Application Gateway, LRS vs ZRS, service endpoint vs private endpoint, snapshot vs backup...). Eight question styles shuffled together: definition→term, term→definition, this-or-that discrimination, which-definition, true/false traps, odd-one-out, type-the-term, and 5-way match rounds. Missed items come back as fresh questions until you clear them |
| **R** | Review all missed | Every missed question across all topics, until you clear it |
| **T** | Stats | Accuracy per topic and your three weakest areas |

## Controls

- Answer with the letter (A–D), `t`/`f`, typed text, or numbers as prompted.
- Type **`q`** at any prompt to end the current round and return to the menu.
- Ordering questions: enter the item numbers in order, e.g. `3 1 4 2`.
- After a round with misses, choose **R** to review them, **T** to retake a quiz
  of just those questions, or **Enter** to return to the menu.

## How the Azure gym grades you

Problems are generated live from real CIDR math, the built-in RBAC role list,
NSG first-match-wins evaluation, and the VM SLA / storage redundancy tables, so
you get unlimited practice. Each answer comes with the full reasoning (the
subnet math, the rule table walk-through, or the SLA arithmetic) so you learn
the pattern, not just the answer.

## Files

- `az104.py` — the launcher (run this)
- `engine.py` — quiz engine: question types, scoring, flashcards, progress
- `drills.py` — Azure gym generators, service table, acronym list
- `vocab.py` — vocab arcade: mixed-style vocabulary game
- `vocab_data.py` — the confusable-pairs dataset (terms, differences, scenarios)
- `topics/d?_?.py` — the 15 question-bank modules (one per objective)
- `validate.py` — schema checker for the topic modules

The written study guide that pairs with these games is in `../study-guide/`.
