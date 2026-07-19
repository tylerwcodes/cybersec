#!/usr/bin/env python3
"""Validate a topic question-bank module against the required schema.

Usage: python3 validate.py topics/d1_1.py
"""
import importlib.util
import sys


def validate(path):
    spec = importlib.util.spec_from_file_location("mod_under_test", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    assert isinstance(m.TOPIC, dict), "TOPIC must be a dict"
    missing = {"id", "domain", "title", "short"} - set(m.TOPIC)
    assert not missing, f"TOPIC missing keys: {missing}"
    assert isinstance(m.TOPIC["domain"], int), "TOPIC['domain'] must be int"

    assert isinstance(m.TERMS, list) and len(m.TERMS) >= 15, \
        f"TERMS needs >= 15 entries (got {len(m.TERMS)})"
    for t in m.TERMS:
        assert isinstance(t, tuple) and len(t) == 2 and all(isinstance(x, str) for x in t), \
            f"Bad TERMS entry: {t!r}"

    assert isinstance(m.QUESTIONS, list) and len(m.QUESTIONS) >= 30, \
        f"QUESTIONS needs >= 30 entries (got {len(m.QUESTIONS)})"
    for i, q in enumerate(m.QUESTIONS):
        where = f"QUESTIONS[{i}]"
        assert isinstance(q, dict), f"{where} not a dict"
        t = q.get("type")
        assert t in ("mc", "tf", "fill", "match", "order"), f"{where} bad type: {t}"
        assert isinstance(q.get("q"), str) and q["q"].strip(), f"{where} missing q"
        assert isinstance(q.get("explain"), str) and q["explain"].strip(), f"{where} missing explain"
        if t == "mc":
            assert isinstance(q.get("choices"), list) and len(q["choices"]) == 4, \
                f"{where} mc needs exactly 4 choices"
            assert isinstance(q.get("answer"), int) and 0 <= q["answer"] < 4, \
                f"{where} mc answer must be int 0-3"
        elif t == "tf":
            assert isinstance(q.get("answer"), bool), f"{where} tf answer must be bool"
        elif t == "fill":
            assert isinstance(q.get("answers"), list) and q["answers"] and \
                all(isinstance(a, str) for a in q["answers"]), f"{where} fill needs answers list"
        elif t == "match":
            assert isinstance(q.get("pairs"), list) and 4 <= len(q["pairs"]) <= 6, \
                f"{where} match needs 4-6 pairs"
            for p in q["pairs"]:
                assert len(p) == 2, f"{where} bad pair {p!r}"
        elif t == "order":
            assert isinstance(q.get("items"), list) and 4 <= len(q["items"]) <= 7, \
                f"{where} order needs 4-7 items"

    counts = {}
    for q in m.QUESTIONS:
        counts[q["type"]] = counts.get(q["type"], 0) + 1
    print(f"OK {path}: {len(m.QUESTIONS)} questions {counts}, {len(m.TERMS)} terms")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        validate(p)
