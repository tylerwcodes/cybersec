"""Vocab Arcade: every AZ-900 term drilled with mixed question styles.

Pulls the full term bank from the 11 topic modules and pairs it with a
curated dataset of commonly-confused terms (vocab_data.PAIRS). Question
styles rotate: definition -> term, term -> definition, this-or-that
discrimination, which-definition, true/false traps, odd-one-out,
type-the-term, and 5-way match rounds.
"""
import difflib
import random

import engine
from engine import C, QuitRound, banner, get_input, grade_line, wrap

from vocab_data import PAIRS


# ------------------------------------------------------------------- bank ---

def build_bank(mods):
    """Aggregate TERMS from every topic module, deduped by term name."""
    bank = []
    seen = set()
    for m in mods:
        for term, definition in m.TERMS:
            key = term.lower()
            if key in seen:
                continue
            seen.add(key)
            bank.append({
                "tid": m.TOPIC["id"],
                "short": m.TOPIC["short"],
                "domain": m.TOPIC["domain"],
                "term": term,
                "def": definition,
            })
    return bank


def _accepted_names(term):
    """'Capital expenditure (CapEx)' -> ['capital expenditure (capex)',
    'capital expenditure', 'capex']"""
    names = [engine.normalize(term)]
    if "(" in term and term.endswith(")"):
        outside, inside = term.rsplit("(", 1)
        names.append(engine.normalize(outside))
        names.append(engine.normalize(inside[:-1]))
    return [n for n in names if n]


def _distractors(bank, target, n=3):
    """Prefer terms from the same topic, then same domain, then anywhere."""
    pools = (
        [e for e in bank if e["tid"] == target["tid"] and e is not target],
        [e for e in bank if e["domain"] == target["domain"] and e is not target],
        [e for e in bank if e is not target],
    )
    picked, used = [], {target["term"].lower()}
    for pool in pools:
        random.shuffle(pool)
        for e in pool:
            if len(picked) == n:
                return picked
            if e["term"].lower() not in used:
                picked.append(e)
                used.add(e["term"].lower())
    return picked


# --------------------------------------------------------- question styles ---
# Each asker prints one question, grades it, and returns (correct, key)
# where key identifies the vocab item(s) drilled, for miss recycling.

def q_def_to_term(bank, target=None):
    e = target or random.choice(bank)
    d = _distractors(bank, e)
    q = {
        "type": "mc",
        "q": f'Which term does this define: "{e["def"]}"',
        "choices": [e["term"]] + [x["term"] for x in d],
        "answer": 0,
        "explain": f'{e["term"]} — {e["def"]} (topic {e["tid"]} {e["short"]})',
    }
    return engine.ask_mc(q), ("term", e["term"])


def q_term_to_def(bank, target=None):
    e = target or random.choice(bank)
    d = _distractors(bank, e)
    q = {
        "type": "mc",
        "q": f'Which is the definition of {e["term"]}?',
        "choices": [e["def"]] + [x["def"] for x in d],
        "answer": 0,
        "explain": f'{e["term"]} — {e["def"]} (topic {e["tid"]} {e["short"]})',
    }
    return engine.ask_mc(q), ("term", e["term"])


def q_this_or_that(pair=None):
    p = pair or random.choice(PAIRS)
    s = random.choice(p["scenarios"])
    two = [p["a"], p["b"]]
    random.shuffle(two)
    answer = 1 + two.index(s["answer"])
    print(C.YELLOW + C.BOLD + f'  ⚔  {two[0]}  vs  {two[1]}' + C.RESET)
    print(wrap(f'"{s["stmt"]}"', indent=2))
    while True:
        ans = get_input(f"  Which term? 1) {two[0]}  2) {two[1]} : ")
        if ans in ("1", "2"):
            break
        print("  Enter 1 or 2.")
    correct = int(ans) == answer
    engine.feedback(correct, f"Correct answer: {s['answer']}",
                    {"explain": p["difference"]})
    return correct, ("pair", p["a"], p["b"])


def q_which_def(pair=None):
    p = pair or random.choice(PAIRS)
    ask_for = random.choice([p["a"], p["b"]])
    right = p["def_a"] if ask_for == p["a"] else p["def_b"]
    wrong = p["def_b"] if ask_for == p["a"] else p["def_a"]
    defs = [right, wrong]
    random.shuffle(defs)
    print(wrap(f'These two definitions cover {C.BOLD}{p["a"]}{C.RESET} and '
               f'{C.BOLD}{p["b"]}{C.RESET}.'))
    for i, d in enumerate(defs, 1):
        print(wrap(f"  {i}) {d}", indent=2))
    while True:
        ans = get_input(f"  Which one defines {ask_for}? (1/2): ")
        if ans in ("1", "2"):
            break
        print("  Enter 1 or 2.")
    correct = defs[int(ans) - 1] == right
    engine.feedback(correct, f"{ask_for}: {right}", {"explain": p["difference"]})
    return correct, ("pair", p["a"], p["b"])


def q_pair_tf(pair=None):
    p = pair or random.choice(PAIRS)
    t = random.choice(p["tf"])
    q = {
        "type": "tf",
        "q": t["stmt"],
        "answer": t["truth"],
        "explain": t["why"] + " " + p["difference"],
    }
    print(wrap(q["q"]))
    return engine.ask_tf(q), ("pair", p["a"], p["b"])


def q_odd_one_out(bank):
    by_tid = {}
    for e in bank:
        by_tid.setdefault(e["tid"], []).append(e)
    home_tid = random.choice([t for t, es in by_tid.items() if len(es) >= 3])
    home = by_tid[home_tid]
    others = [e for e in bank if e["domain"] != home[0]["domain"]]
    odd = random.choice(others)
    trio = random.sample(home, 3)
    q = {
        "type": "mc",
        "q": "Odd one out: three of these terms come from the same exam "
             "objective. Which one does NOT belong?",
        "choices": [odd["term"]] + [x["term"] for x in trio],
        "answer": 0,
        "explain": f'{odd["term"]} is a "{odd["short"]}" term ({odd["tid"]}); '
                   f'the others all come from "{home[0]["short"]}" ({home_tid}).',
    }
    return engine.ask_mc(q), ("term", odd["term"])


def q_type_term(bank, target=None):
    e = target or random.choice(bank)
    print(wrap(f'Type the term: "{e["def"]}"'))
    ans = engine.normalize(get_input("  Term: "))
    targets = _accepted_names(e["term"])
    ratio = max(difflib.SequenceMatcher(None, ans, t).ratio() for t in targets)
    if ans in targets or ratio >= 0.82:
        correct = True
    elif ratio >= 0.55 and ans:
        print(C.YELLOW + f"  Close. Official term: {e['term']}" + C.RESET)
        correct = get_input("  Count it? (y/n): ").lower().startswith("y")
    else:
        correct = False
    engine.feedback(correct, f"Correct answer: {e['term']}",
                    {"explain": f'{e["term"]} — {e["def"]}'})
    return correct, ("term", e["term"])


def q_match5(bank):
    batch = random.sample(bank, 5)
    q = {
        "type": "match",
        "q": "Match each term to its definition.",
        "pairs": [[e["term"], e["def"]] for e in batch],
        "explain": "Review any pairs you missed — core exam vocabulary.",
    }
    print(wrap(q["q"]))
    ok = engine.ask_match(q)
    return ok, ("term", batch[0]["term"])


# ------------------------------------------------------------------- modes ---

# (weight, needs_bank, asker) — this-or-that and the pair styles are weighted
# up because discriminating confusable terms is what the exam actually tests.
MIXED = [
    (3, "bank", q_def_to_term),
    (2, "bank", q_term_to_def),
    (4, "pair", q_this_or_that),
    (2, "pair", q_which_def),
    (3, "pair", q_pair_tf),
    (1, "bank", q_odd_one_out),
    (2, "bank", q_type_term),
    (1, "bank", q_match5),
]

PAIR_ONLY = [(4, "pair", q_this_or_that), (2, "pair", q_which_def),
             (3, "pair", q_pair_tf)]


def _weighted(styles):
    pool = []
    for w, kind, fn in styles:
        pool.extend([(kind, fn)] * w)
    return random.choice(pool)


def _ask_one(bank, styles, num, total):
    print()
    label = f"--- Question {num}/{total} " if total else f"--- Question {num} "
    print(C.BLUE + C.BOLD + label + "-" * max(1, 78 - len(label)) + C.RESET)
    kind, fn = _weighted(styles)
    return fn(bank) if kind == "bank" else fn()


def _redrill(bank, missed, progress):
    """Fresh questions targeted at each missed term/pair until all cleared."""
    pair_by_names = {(p["a"], p["b"]): p for p in PAIRS}
    while missed:
        n = len(missed)
        print()
        print(C.YELLOW + C.BOLD + f"  {n} vocab item{'s' if n != 1 else ''} "
              "still missed." + C.RESET)
        print(wrap("Enter to drill them with fresh questions, q for menu.", indent=2))
        try:
            engine.press_enter()
        except QuitRound:
            return
        keys = list(missed)
        random.shuffle(keys)
        cleared = []
        for i, key in enumerate(keys, 1):
            print()
            print(C.BLUE + C.BOLD + f"--- Re-drill {i}/{len(keys)} " + "-" * 50 + C.RESET)
            try:
                if key[0] == "pair":
                    p = pair_by_names[(key[1], key[2])]
                    fn = random.choice([q_this_or_that, q_which_def, q_pair_tf])
                    correct, _ = fn(p)
                else:
                    e = next(x for x in bank if x["term"] == key[1])
                    fn = random.choice([q_def_to_term, q_term_to_def, q_type_term])
                    correct, _ = fn(bank, e)
            except QuitRound:
                return
            if correct:
                cleared.append(key)
        for key in cleared:
            missed.remove(key)
        if not missed:
            print(C.GREEN + C.BOLD +
                  "\n  Perfect — every missed vocab item cleared! 🎉" + C.RESET)


def _round(bank, styles, progress, label, endless_default=False):
    raw = get_input("  How many questions? (10/25/50, Enter=25, e=endless): ").lower()
    total = None if raw.startswith("e") else \
        int(raw) if raw.isdigit() and int(raw) > 0 else 25
    score, asked, streak, best_streak = 0, 0, 0, 0
    missed = []
    n = 0
    try:
        while total is None or n < total:
            n += 1
            correct, key = _ask_one(bank, styles, n, total)
            asked += 1
            if correct:
                score += 1
                streak += 1
                best_streak = max(best_streak, streak)
                if streak and streak % 5 == 0:
                    print(C.MAGENTA + C.BOLD +
                          f"  🔥 {streak} in a row!" + C.RESET)
            else:
                streak = 0
                if key not in missed:
                    missed.append(key)
    except QuitRound:
        print(C.DIM + "\n  Round ended." + C.RESET)
    if not asked:
        return
    print()
    print(grade_line(score, asked))
    print(C.DIM + f"  Best streak: {best_streak}" + C.RESET)
    if progress is not None:
        engine.record_session(progress, label, score, asked)
    if missed:
        _redrill(bank, missed, progress)


def arcade(mods, progress):
    bank = build_bank(mods)
    while True:
        banner("VOCAB ARCADE", C.YELLOW)
        print(wrap(f"{len(bank)} terms from all 11 topics + {len(PAIRS)} "
                   "commonly-confused pairs. Eight question styles, shuffled. "
                   "Miss something and it comes back until you clear it."))
        print(f"""
  1) Mixed gauntlet     (all 8 question styles)
  2) This-or-that       (confusable pairs only — the exam's favorite trap)
  3) Match marathon     (5-term match rounds)
  4) Typing challenge   (type the term from its definition)
  0) Back
""")
        try:
            choice = get_input("  Choose: ")
        except QuitRound:
            return
        if choice == "1":
            _round(bank, MIXED, progress, "Vocab gauntlet")
        elif choice == "2":
            _round(bank, PAIR_ONLY, progress, "This-or-that")
        elif choice == "3":
            _match_marathon(bank, progress)
        elif choice == "4":
            _round(bank, [(1, "bank", q_type_term)], progress, "Vocab typing")
        elif choice == "0":
            return


def _match_marathon(bank, progress):
    print(wrap("Endless 5-term match rounds from the full bank. q to stop."))
    score, asked = 0, 0
    try:
        while True:
            print()
            print(C.BLUE + C.BOLD + f"--- Match round {asked + 1} " + "-" * 50 + C.RESET)
            ok, _ = q_match5(bank)
            asked += 1
            if ok:
                score += 1
    except QuitRound:
        pass
    if asked:
        print()
        print(grade_line(score, asked))
        if progress is not None:
            engine.record_session(progress, "Match marathon", score, asked)
