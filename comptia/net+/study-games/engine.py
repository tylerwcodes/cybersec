"""Shared quiz engine for the Network+ study games.

Pure standard library. Handles question rendering, answer checking,
scoring, flashcards, term matching, and persistent progress tracking.
"""
import hashlib
import json
import os
import random
import textwrap
import time

WIDTH = 78
PROGRESS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".progress.json")


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"


class QuitRound(Exception):
    """User typed q/quit — bail out of the current activity."""


def wrap(text, indent=0):
    pad = " " * indent
    return textwrap.fill(text, WIDTH, initial_indent=pad, subsequent_indent=pad)


def banner(title, color=C.CYAN):
    print()
    print(color + C.BOLD + "=" * WIDTH + C.RESET)
    print(color + C.BOLD + title.center(WIDTH) + C.RESET)
    print(color + C.BOLD + "=" * WIDTH + C.RESET)


def get_input(prompt="> "):
    try:
        s = input(C.BOLD + prompt + C.RESET).strip()
    except EOFError:
        raise QuitRound()
    if s.lower() in ("q", "quit", "exit"):
        raise QuitRound()
    return s


def press_enter(msg="  [Enter to continue, q to quit] "):
    get_input(msg)


def normalize(s):
    s = s.lower().strip().rstrip(".")
    for ch in ("-", "_", "/", ","):
        s = s.replace(ch, " ")
    return " ".join(s.split())


def qkey(q):
    return hashlib.md5(q["q"].encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------- progress ---

def load_progress():
    try:
        with open(PROGRESS_PATH) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"missed": {}, "topics": {}, "history": []}


def save_progress(p):
    try:
        with open(PROGRESS_PATH, "w") as f:
            json.dump(p, f, indent=1)
    except OSError:
        pass


def record_answer(progress, topic_id, q, correct):
    t = progress["topics"].setdefault(topic_id, {"right": 0, "wrong": 0})
    missed = progress["missed"].setdefault(topic_id, {})
    key = qkey(q)
    if correct:
        t["right"] += 1
        if key in missed:
            del missed[key]
            if not missed:
                del progress["missed"][topic_id]
    else:
        t["wrong"] += 1
        missed[key] = missed.get(key, 0) + 1


def record_session(progress, label, score, total):
    progress["history"].append({
        "label": label, "score": score, "total": total, "ts": time.time(),
    })
    save_progress(progress)


# ---------------------------------------------------------- question types ---

def show_question(num, total, q):
    print()
    print(C.BLUE + C.BOLD + f"--- Question {num}/{total} " + "-" * max(1, WIDTH - 16 - len(f"{num}{total}")) + C.RESET)
    print(wrap(q["q"]))


def feedback(correct, detail, q):
    if correct:
        print(C.GREEN + C.BOLD + "  ✔ Correct!" + C.RESET)
    else:
        print(C.RED + C.BOLD + "  ✘ Incorrect." + C.RESET + " " + detail)
    print(C.DIM + wrap("» " + q["explain"], indent=2) + C.RESET)


def ask_mc(q):
    letters = "ABCD"
    order = list(range(4))
    random.shuffle(order)
    for i, orig in enumerate(order):
        print(wrap(f"  {letters[i]}) {q['choices'][orig]}", indent=2))
    while True:
        ans = get_input("  Answer (A-D): ").upper()
        if ans in letters:
            break
        print("  Enter A, B, C, or D.")
    picked = order[letters.index(ans)]
    correct = picked == q["answer"]
    right_letter = letters[order.index(q["answer"])]
    feedback(correct, f"Correct answer: {right_letter}) {q['choices'][q['answer']]}", q)
    return correct


def ask_tf(q):
    while True:
        ans = normalize(get_input("  True or False (t/f): "))
        if ans in ("t", "true", "f", "false"):
            break
        print("  Enter T or F.")
    picked = ans.startswith("t")
    correct = picked == q["answer"]
    feedback(correct, f"Correct answer: {'True' if q['answer'] else 'False'}", q)
    return correct


def ask_fill(q):
    ans = normalize(get_input("  Your answer: "))
    accepted = [normalize(a) for a in q["answers"]]
    correct = ans in accepted
    feedback(correct, f"Correct answer: {q['answers'][0]}", q)
    return correct


def ask_match(q):
    pairs = q["pairs"]
    letters = "ABCDEF"[: len(pairs)]
    rights = list(range(len(pairs)))
    random.shuffle(rights)
    for i, p in enumerate(pairs):
        print(wrap(f"  {i + 1}. {p[0]}", indent=2))
    print()
    for i, ri in enumerate(rights):
        print(wrap(f"  {letters[i]}. {pairs[ri][1]}", indent=2))
    picks = []
    for i in range(len(pairs)):
        while True:
            ans = get_input(f"  Match for {i + 1} (letter): ").upper()
            if ans in letters:
                picks.append(rights[letters.index(ans)])
                break
            print(f"  Enter one of {letters}.")
    wrong = [i for i, p in enumerate(picks) if p != i]
    correct = not wrong
    if wrong:
        detail = "; ".join(f"{i + 1} → {pairs[i][1]}" for i in wrong)
        feedback(False, "Correct pairs: " + detail, q)
    else:
        feedback(True, "", q)
    return correct


def ask_order(q):
    items = q["items"]
    shuffled = list(range(len(items)))
    while shuffled == list(range(len(items))):
        random.shuffle(shuffled)
    for i, orig in enumerate(shuffled):
        print(wrap(f"  {i + 1}. {items[orig]}", indent=2))
    print(wrap(f"  Enter the item numbers in the correct order (e.g. '3 1 4 2').", indent=2))
    while True:
        raw = get_input("  Order: ").replace(",", " ").split()
        try:
            seq = [int(x) - 1 for x in raw]
        except ValueError:
            seq = None
        if seq and sorted(seq) == list(range(len(items))):
            break
        print(f"  Enter each number 1-{len(items)} exactly once.")
    picked = [shuffled[i] for i in seq]
    correct = picked == list(range(len(items)))
    detail = "Correct order: " + " → ".join(items)
    feedback(correct, detail, q)
    return correct


ASKERS = {"mc": ask_mc, "tf": ask_tf, "fill": ask_fill, "match": ask_match, "order": ask_order}


def ask(q):
    return ASKERS[q["type"]](q)


# ------------------------------------------------------------------- modes ---

def grade_line(score, total):
    pct = 100.0 * score / total if total else 0.0
    if pct >= 90:
        msg, color = "Outstanding — exam ready on this topic!", C.GREEN
    elif pct >= 80:
        msg, color = "Strong — around the passing line. Polish the misses.", C.GREEN
    elif pct >= 65:
        msg, color = "Getting there — review the explanations you missed.", C.YELLOW
    else:
        msg, color = "Needs work — reread this chapter of the study guide.", C.RED
    return color + C.BOLD + f"  Score: {score}/{total} ({pct:.0f}%)  {msg}" + C.RESET


def format_answer(q):
    """A human-readable correct answer for review screens."""
    t = q["type"]
    if t == "mc":
        return q["choices"][q["answer"]]
    if t == "tf":
        return "True" if q["answer"] else "False"
    if t == "fill":
        return q["answers"][0]
    if t == "match":
        return "; ".join(f"{a} = {b}" for a, b in q["pairs"])
    if t == "order":
        return " → ".join(q["items"])
    return ""


def _run_round(items, progress):
    """Ask each (topic_id, question) item once, recording to progress.

    Returns (score, asked, missed_items) where missed_items keeps the same
    (topic_id, question) shape so a retake can drill exactly those.
    """
    score = 0
    asked = 0
    missed = []
    for i, (tid, q) in enumerate(items, 1):
        show_question(i, len(items), q)
        try:
            correct = ask(q)
        except QuitRound:
            print(C.DIM + "\n  Round ended early." + C.RESET)
            break
        asked += 1
        if correct:
            score += 1
        else:
            missed.append((tid, q))
        if progress is not None and tid:
            record_answer(progress, tid, q, correct)
    if progress is not None:
        save_progress(progress)
    return score, asked, missed


def show_review(missed_items):
    """Walk through each missed question showing the correct answer + why."""
    banner(f"REVIEW — {len(missed_items)} MISSED QUESTION(S)", C.MAGENTA)
    print(C.DIM + wrap("Read each one, then retake to lock it in. Enter to step "
                       "through; q to stop reviewing.") + C.RESET)
    try:
        for i, (_tid, q) in enumerate(missed_items, 1):
            print()
            print(C.BLUE + C.BOLD + f"--- Missed {i}/{len(missed_items)} " +
                  "-" * 40 + C.RESET)
            print(wrap(q["q"]))
            print(C.GREEN + C.BOLD + wrap("  Correct answer: " + format_answer(q),
                                          indent=2) + C.RESET)
            print(C.DIM + wrap("» " + q["explain"], indent=2) + C.RESET)
            press_enter()
    except QuitRound:
        pass


def review_and_retake(missed_items, progress, label):
    """Offer to review the missed questions and retake a quiz built from them,
    looping on whatever is still missed until the pile is empty or the user quits."""
    while missed_items:
        n = len(missed_items)
        print()
        print(C.YELLOW + C.BOLD +
              f"  You missed {n} question{'s' if n != 1 else ''} this round." + C.RESET)
        print("""  What next?
    R) Review the missed questions (see answers + explanations)
    T) Retake a quiz of ONLY the missed questions
    Enter) Done — back to the menu""")
        try:
            choice = get_input("  Choose (R/T/Enter): ").lower()
        except QuitRound:
            return
        if choice == "r":
            show_review(missed_items)
        elif choice == "t":
            retake = list(missed_items)
            random.shuffle(retake)
            print(C.CYAN + C.BOLD + f"\n  Retaking {len(retake)} missed question(s)..."
                  + C.RESET)
            score, asked, still = _run_round(retake, progress)
            if not asked:
                return
            print()
            print(grade_line(score, asked))
            if progress is not None:
                record_session(progress, label + " (retake)", score, asked)
            # Only the questions reached this round can be cleared; anything the
            # user skipped by quitting stays on the list.
            reached = set(id(q) for _t, q in retake[:asked])
            missed_items = still + [it for it in missed_items
                                    if id(it[1]) not in reached]
            if not missed_items:
                print(C.GREEN + C.BOLD +
                      "\n  Perfect — you cleared every missed question! 🎉" + C.RESET)
                return
        else:
            return


def run_quiz(questions, progress=None, topic_id=None, label="Quiz", limit=None,
             allow_retake=True):
    """Run a quiz round. Typing q mid-question ends the round (not the app).

    After the round, if any questions were missed, offer to review them and
    retake a quiz built only from the misses (repeating until all are cleared).
    """
    qs = list(questions)
    random.shuffle(qs)
    if limit:
        qs = qs[:limit]
    items = [(topic_id, q) for q in qs]
    start = time.monotonic()
    score, asked, missed = _run_round(items, progress)
    if asked:
        mins = (time.monotonic() - start) / 60
        print()
        print(grade_line(score, asked))
        print(C.DIM + f"  Time: {mins:.1f} min" + C.RESET)
        if progress is not None:
            record_session(progress, label, score, asked)
    if allow_retake and asked and missed:
        review_and_retake(missed, progress, label)
    return score, asked


def flashcards(terms):
    deck = list(terms)
    random.shuffle(deck)
    missed = []
    print(C.DIM + wrap("Think of the definition, press Enter to reveal, then grade "
                       "yourself: (y) knew it / (n) missed it. q to quit.") + C.RESET)
    try:
        while deck:
            term, definition = deck.pop(0)
            print()
            print(C.YELLOW + C.BOLD + "  ★ " + term + C.RESET)
            get_input("  [Enter to reveal] ")
            print(wrap(definition, indent=4))
            while True:
                g = get_input("  Knew it? (y/n): ").lower()
                if g in ("y", "n"):
                    break
            if g == "n":
                missed.append((term, definition))
            if not deck and missed:
                print(C.MAGENTA + f"\n  Recycling {len(missed)} missed card(s)..." + C.RESET)
                deck, missed = missed, []
        print(C.GREEN + C.BOLD + "\n  Deck complete!" + C.RESET)
    except QuitRound:
        print(C.DIM + "\n  Flashcards ended." + C.RESET)


def term_match(terms, rounds=3, per_round=5):
    total = 0
    score = 0
    pool = list(terms)
    random.shuffle(pool)
    try:
        for r in range(rounds):
            if len(pool) < per_round:
                pool = list(terms)
                random.shuffle(pool)
            batch = [pool.pop() for _ in range(per_round)]
            q = {
                "q": f"Round {r + 1}: match each term to its definition.",
                "pairs": [[t, d] for t, d in batch],
                "explain": "Review any pairs you missed — these are core exam vocabulary.",
                "type": "match",
            }
            show_question(r + 1, rounds, q)
            if ask_match(q):
                score += 1
            total += 1
        print()
        print(grade_line(score, total))
    except QuitRound:
        print(C.DIM + "\n  Match game ended." + C.RESET)


def review_missed(mod, progress):
    topic_id = mod.TOPIC["id"]
    missed = progress.get("missed", {}).get(topic_id, {})
    qs = [q for q in mod.QUESTIONS if qkey(q) in missed]
    if not qs:
        print(C.GREEN + "\n  Nothing to review — no missed questions for this topic!" + C.RESET)
        return
    print(C.MAGENTA + f"\n  Reviewing {len(qs)} previously missed question(s). "
          "Answer correctly to clear them." + C.RESET)
    run_quiz(qs, progress, topic_id, label=f"Review {topic_id}")


def topic_menu(mod, progress):
    t = mod.TOPIC
    while True:
        stats = progress["topics"].get(t["id"], {"right": 0, "wrong": 0})
        answered = stats["right"] + stats["wrong"]
        acc = 100.0 * stats["right"] / answered if answered else 0
        n_missed = len(progress.get("missed", {}).get(t["id"], {}))
        banner(f"{t['id']}  {t['short']}")
        print(wrap(t["title"]))
        print(C.DIM + f"  Lifetime: {answered} answered, {acc:.0f}% accuracy, "
              f"{n_missed} in review pile" + C.RESET)
        print(f"""
  1) Full quiz          ({len(mod.QUESTIONS)} questions)
  2) Quick 10           (random sample)
  3) Flashcards         ({len(mod.TERMS)} terms)
  4) Term match         (beat the definitions)
  5) Review missed      ({n_missed} queued)
  0) Back
""")
        try:
            choice = get_input("  Choose: ")
        except QuitRound:
            return
        if choice == "1":
            run_quiz(mod.QUESTIONS, progress, t["id"], label=f"Full {t['id']}")
        elif choice == "2":
            run_quiz(mod.QUESTIONS, progress, t["id"], label=f"Quick {t['id']}", limit=10)
        elif choice == "3":
            flashcards(mod.TERMS)
        elif choice == "4":
            term_match(mod.TERMS)
        elif choice == "5":
            review_missed(mod, progress)
        elif choice == "0":
            return
