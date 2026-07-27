#!/usr/bin/env python3
"""Microsoft Azure Fundamentals AZ-900 terminal study center.

Run: python3 az900.py
"""
import importlib
import os
import pkgutil
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import drills
import engine
import vocab
from engine import C, QuitRound, banner, get_input, wrap

DOMAINS = {
    1: ("Cloud Concepts", "25-30"),
    2: ("Azure Architecture & Services", "35-40"),
    3: ("Management & Governance", "30-35"),
}

# 45 questions split by official domain weight (28% / 38% / 34%)
EXAM_SPLIT = {1: 13, 2: 17, 3: 15}
EXAM_MINUTES = 45


def load_topics():
    import topics as topics_pkg
    mods = []
    for info in pkgutil.iter_modules(topics_pkg.__path__):
        if info.name.startswith("d"):
            mods.append(importlib.import_module(f"topics.{info.name}"))
    mods.sort(key=lambda m: (m.TOPIC["domain"], m.TOPIC["id"]))
    return mods


def main_menu(mods, progress):
    banner("MICROSOFT AZURE FUNDAMENTALS AZ-900 STUDY CENTER")
    total_q = sum(len(m.QUESTIONS) for m in mods)
    print(wrap(f"{len(mods)} topics | {total_q} questions | infinite shared-"
               f"responsibility, hierarchy, and SLA drills | 45-question exam "
               f"simulator"))
    by_domain = {}
    for i, m in enumerate(mods, 1):
        by_domain.setdefault(m.TOPIC["domain"], []).append((i, m))
    for d, (name, pct) in DOMAINS.items():
        if d not in by_domain:
            continue
        print(C.YELLOW + C.BOLD + f"\n  Domain {d}.0 {name} ({pct}%)" + C.RESET)
        for i, m in by_domain[d]:
            t = m.TOPIC
            n_missed = len(progress.get("missed", {}).get(t["id"], {}))
            tag = C.RED + f"  [{n_missed} missed]" + C.RESET if n_missed else ""
            print(f"   {i:>2}) {t['id']}  {t['short']}{tag}")
    print(C.CYAN + C.BOLD + "\n  Drills & modes" + C.RESET)
    print("    E) Exam simulator (45 questions, weighted, timed)")
    print("    G) Azure gym (infinite generated problems)")
    print("    S) Service blitz")
    print("    A) Acronym blitz")
    print("    V) Vocab arcade (every term + confusable pairs, 8 question styles)")
    print("    R) Review ALL missed questions")
    print("    T) Stats & weakest topics")
    print("    Q) Quit")


def exam_sim(mods, progress):
    banner("EXAM SIMULATOR", C.RED)
    print(wrap(f"45 questions weighted like the real exam ({', '.join(f'D{d} {n}' for d, n in EXAM_SPLIT.items())}). "
               f"The real exam allows about {EXAM_MINUTES} minutes; the timer "
               "here is informational. Microsoft's passing score is 700 on a "
               "1-1000 scale - treat 80%+ here as passing territory. Type q to "
               "abandon."))
    if not get_input("  Start? (y/n): ").lower().startswith("y"):
        return
    by_domain = {}
    for m in mods:
        by_domain.setdefault(m.TOPIC["domain"], []).append(m)
    paper = []
    for d, want in EXAM_SPLIT.items():
        pool = []
        for m in by_domain.get(d, []):
            for q in m.QUESTIONS:
                pool.append((m.TOPIC["id"], q))
        random.shuffle(pool)
        paper.extend([(d, tid, q) for tid, q in pool[:want]])
    random.shuffle(paper)

    score = {d: 0 for d in DOMAINS}
    asked = {d: 0 for d in DOMAINS}
    missed_items = []
    start = time.monotonic()
    for i, (d, tid, q) in enumerate(paper, 1):
        elapsed = (time.monotonic() - start) / 60
        left = EXAM_MINUTES - elapsed
        clock = (C.RED if left < 10 else C.DIM) + f"[{elapsed:.0f} min elapsed]" + C.RESET
        print(f"\n{clock}")
        engine.show_question(i, len(paper), q)
        try:
            correct = engine.ask(q)
        except QuitRound:
            print(C.DIM + "\n  Exam abandoned." + C.RESET)
            break
        asked[d] += 1
        if correct:
            score[d] += 1
        else:
            missed_items.append((tid, q))
        engine.record_answer(progress, tid, q, correct)
    engine.save_progress(progress)

    total_asked = sum(asked.values())
    if not total_asked:
        return
    total_score = sum(score.values())
    mins = (time.monotonic() - start) / 60
    banner("SCORE REPORT", C.RED)
    print(f"  Time: {mins:.0f} of {EXAM_MINUTES} minutes")
    print()
    for d, (name, pct) in DOMAINS.items():
        if not asked[d]:
            continue
        dp = 100.0 * score[d] / asked[d]
        color = C.GREEN if dp >= 80 else C.YELLOW if dp >= 65 else C.RED
        bar = "█" * int(dp / 5)
        print(color + f"  {d}.0 {name:<30} {score[d]:>2}/{asked[d]:<2} {dp:>3.0f}% {bar}" + C.RESET)
    print()
    print(engine.grade_line(total_score, total_asked))
    pct = 100.0 * total_score / total_asked
    verdict = ("PASS territory - you would likely clear 700/1000."
               if pct >= 80 else
               "Below the passing line - drill your weakest domains above.")
    print((C.GREEN if pct >= 80 else C.RED) + C.BOLD + f"  {verdict}" + C.RESET)
    engine.record_session(progress, "Exam simulator", total_score, total_asked)
    if missed_items:
        engine.review_and_retake(missed_items, progress, "Exam simulator")


def review_all(mods, progress):
    qs = []
    for m in mods:
        missed = progress.get("missed", {}).get(m.TOPIC["id"], {})
        for q in m.QUESTIONS:
            if engine.qkey(q) in missed:
                qs.append((m.TOPIC["id"], q))
    if not qs:
        print(C.GREEN + "\n  Review pile is empty - nothing missed. Nice." + C.RESET)
        return
    banner(f"GLOBAL REVIEW - {len(qs)} MISSED QUESTIONS", C.MAGENTA)
    random.shuffle(qs)
    score, asked, missed = engine._run_round(qs, progress)
    if asked:
        print()
        print(engine.grade_line(score, asked))
        engine.record_session(progress, "Global review", score, asked)
    if missed:
        engine.review_and_retake(missed, progress, "Global review")


def stats(mods, progress):
    banner("PROGRESS REPORT", C.CYAN)
    rows = []
    for m in mods:
        t = m.TOPIC
        s = progress["topics"].get(t["id"], {"right": 0, "wrong": 0})
        answered = s["right"] + s["wrong"]
        acc = 100.0 * s["right"] / answered if answered else None
        rows.append((t["id"], t["short"], answered, acc,
                     len(progress.get("missed", {}).get(t["id"], {}))))
    print(f"  {'ID':<5} {'Topic':<32} {'Answered':>8} {'Accuracy':>9} {'Missed':>7}")
    print("  " + "-" * 66)
    for tid, short, answered, acc, miss in rows:
        acc_s = f"{acc:.0f}%" if acc is not None else "-"
        color = C.RESET if acc is None else C.GREEN if acc >= 80 else \
            C.YELLOW if acc >= 65 else C.RED
        print(color + f"  {tid:<5} {short:<32} {answered:>8} {acc_s:>9} {miss:>7}" + C.RESET)
    seen = [r for r in rows if r[3] is not None]
    if seen:
        weakest = sorted(seen, key=lambda r: r[3])[:3]
        print(C.MAGENTA + "\n  Focus next: " +
              ", ".join(f"{t} ({a:.0f}%)" for t, _, _, a, _ in weakest) + C.RESET)
    hist = progress.get("history", [])[-5:]
    if hist:
        print(C.DIM + "\n  Recent sessions:" + C.RESET)
        for h in hist:
            when = time.strftime("%b %d %H:%M", time.localtime(h["ts"]))
            print(C.DIM + f"    {when}  {h['label']:<20} {h['score']}/{h['total']}" + C.RESET)


def main():
    mods = load_topics()
    if not mods:
        print("No topic modules found in topics/ - run from the study-games directory.")
        sys.exit(1)
    progress = engine.load_progress()
    while True:
        main_menu(mods, progress)
        try:
            choice = get_input("\n  Choose a topic number or mode letter: ").upper()
        except QuitRound:
            choice = "Q"
        if choice == "Q":
            print(C.CYAN + "\n  Good luck on the exam! (700 to pass - you've got this)\n" + C.RESET)
            return
        try:
            if choice == "E":
                exam_sim(mods, progress)
            elif choice == "G":
                drills.azure_gym()
            elif choice == "S":
                drills.service_blitz()
            elif choice == "A":
                drills.acronym_blitz()
            elif choice == "V":
                vocab.arcade(mods, progress)
            elif choice == "R":
                review_all(mods, progress)
            elif choice == "T":
                stats(mods, progress)
            elif choice.isdigit() and 1 <= int(choice) <= len(mods):
                engine.topic_menu(mods[int(choice) - 1], progress)
            else:
                continue
        except QuitRound:
            continue
        try:
            engine.press_enter("\n  [Enter for main menu] ")
        except QuitRound:
            pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
