# Network+ N10-009 Terminal Study Games

An interactive, terminal-based study suite covering **every objective** of the
CompTIA Network+ N10-009 exam. Pure Python 3 standard library — no installs, no
internet, no dependencies.

## Run it

```bash
cd study-games
python3 netplus.py
```

Works on macOS, Linux, and Windows (any Python 3.6+). Progress saves
automatically to `.progress.json` in this folder.

## What's inside

- **25 topic modules** — one per exam objective (1.1 through 5.5), with
  **1,000+ questions** and **650+ flashcard terms** total.
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
| **E** | Exam simulator | 90 questions weighted exactly like the real exam (D1 21, D2 18, D3 17, D4 13, D5 21), timed, with a per-domain score report |
| **S** | Subnetting gym | Infinitely generated subnetting problems in 3 difficulty levels — mask conversion, network/broadcast/usable ranges, and VLSM design |
| **P** | Port blitz | The official 20-protocol port table, asked forward and backward, with streak bonuses |
| **A** | Acronym blitz | All 160+ acronyms from the official objectives, fuzzy-graded |
| **R** | Review all missed | Every missed question across all topics, until you clear it |
| **T** | Stats | Accuracy per topic and your three weakest areas |

## Controls

- Answer with the letter (A–D), `t`/`f`, typed text, or numbers as prompted.
- Type **`q`** at any prompt to end the current round and return to the menu.
- Ordering questions: enter the item numbers in order, e.g. `3 1 4 2`.
- After a round with misses, choose **R** to review them, **T** to retake a quiz
  of just those questions, or **Enter** to return to the menu.

## How the subnetting gym grades you

Problems are generated live and checked with Python's `ipaddress` module, so the
math is always exact and you get unlimited practice. Each answer comes with the
"magic number" method worked out, so you learn the technique, not just the result.

## Files

- `netplus.py` — the launcher (run this)
- `engine.py` — quiz engine: question types, scoring, flashcards, progress
- `drills.py` — subnetting generator, port table, acronym list
- `topics/d?_?.py` — the 25 question-bank modules (one per objective)
- `validate.py` — schema checker for the topic modules

The written study guide that pairs with these games is in `../study-guide/`.
