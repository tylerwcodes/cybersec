# Security+ SY0-701 Terminal Study Games

An interactive, terminal-based study suite covering **every objective** of the
CompTIA Security+ SY0-701 exam. Pure Python 3 standard library — no installs,
no internet, no dependencies.

## Run it

```bash
cd study-games
python3 secplus.py
```

Works on macOS, Linux, and Windows (any Python 3.6+). Progress saves
automatically to `.progress.json` in this folder.

## What's inside

- **28 topic modules** — one per exam objective (1.1 through 5.6), with
  **1,170+ questions** and **740+ flashcard terms** total.
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
| **E** | Exam simulator | 90 questions weighted exactly like the real exam (D1 11, D2 20, D3 16, D4 25, D5 18), timed, with a per-domain score report |
| **C** | Control classifier gym | Objective 1.1 drilled to reflex — scenarios classified by category (technical/managerial/operational/physical) and type (preventive/deterrent/detective/corrective/compensating/directive) |
| **P** | Port & protocol blitz | The Sec+ port table forward and backward, plus "name the secure replacement" (Telnet→SSH, LDAP→LDAPS, SNMP→SNMPv3, …), with streak bonuses |
| **A** | Acronym blitz | All 285 acronyms from the official objectives, fuzzy-graded |
| **R** | Review all missed | Every missed question across all topics, until you clear it |
| **T** | Stats | Accuracy per topic and your three weakest areas |

## Controls

- Answer with the letter (A–D), `t`/`f`, typed text, or numbers as prompted.
- Type **`q`** at any prompt to end the current round and return to the menu.
- Ordering questions: enter the item numbers in order, e.g. `3 1 4 2`.
- After a round with misses, choose **R** to review them, **T** to retake a quiz
  of just those questions, or **Enter** to return to the menu.

## Files

- `secplus.py` — the launcher (run this)
- `engine.py` — quiz engine: question types, scoring, flashcards, progress
- `drills.py` — control classifier, port/secure-protocol tables, acronym list
- `topics/d?_?.py` — the 28 question-bank modules (one per objective)
- `validate.py` — schema checker for the topic modules

The written study guide that pairs with these games is in `../study-guide/`.
