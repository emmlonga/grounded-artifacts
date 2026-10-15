#!/usr/bin/env python3
"""Fail if any real name or detail from the grounding's anonymization map appears in the given files.

Reads the table whose header has a "Real" column (grounding template, "Anonymization map").
Matching is case-, accent- and line-break-insensitive, on whole words. Output names the map row
and its anonymized rendering, never the real term, so the report itself can be shared.

Usage: check_names.py --grounding grounding.md FILE [FILE ...]      (.md, .txt or .docx)
Exit:  0 clean · 1 leak found · 3 no anonymization map in the grounding (nothing checked)
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdtext  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grounding", required=True)
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()

    rows = mdtext.find_table(mdtext.read(a.grounding), "real", "anonymized")
    terms = []
    for r in rows or []:
        for v in mdtext.variants(mdtext.col(r, "real")):
            terms.append((mdtext.col(r, "id") or "?", mdtext.col(r, "anonymized") or "?", v))
    if not terms:
        print(f"check_names: SKIPPED - no anonymization map rows in {a.grounding}")
        return 3

    leaks = 0
    for path in a.files:
        text = mdtext.read(path)
        for rid, anon, term in terms:
            for line in mdtext.find_lines(text, term, strip_accents=True):
                leaks += 1
                print(f"LEAK {path}:{line}: map row {rid} (use '{anon}')")
    n = len(a.files)
    if leaks:
        print(f"check_names: FAIL - {leaks} leak(s) across {n} file(s); {len(terms)} real variant(s) checked")
        return 1
    print(f"check_names: PASS - {len(terms)} real variant(s) checked in {n} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
