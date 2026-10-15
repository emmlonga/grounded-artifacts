#!/usr/bin/env python3
"""Words per `##` section of a Markdown artifact, against the outline's word caps.

This is `wc -w` per section: HTML comments (draft and freeze headers) and Markdown syntax are not
counted; headings and table cells are, because they take page space. Caps are read from the outline
in order ("Word cap: N" per section, optional "Total cap: N", optional "Fit guardrail: N"); section i of
the draft is checked against cap i. Calibrate profiles with the same counter so words-per-page stays
comparable.

Every reading is a planning diagnostic, never a gate: the caps and the total cap are the budget the first
draft is written to; the fit guardrail (calibration x pages) is the reading above which a preview render is likely to
fail. The rendered page maximum is binding and is enforced by render.sh max_pages, not here. A reading prints OK,
ADVISORY (over planning cap) or ADVISORY (over fit guardrail: preview likely to fail); none is a finding, a reopen or
a cut once the preview passes (SKILL.md step 12, budget rule).

Usage: wordcount.py draft.md [--outline outline.md]
Exit:  0 always when the outline is found or not given · 2 outline not found
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdtext  # noqa: E402

WORD = re.compile(r"\w", re.U)
OVER_CAP = "ADVISORY (over planning cap)"
OVER_GUARD = "ADVISORY (over fit guardrail: preview likely to fail)"


def count(text):
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return sum(1 for tok in text.split() if WORD.search(tok))


def sections(md):
    md = mdtext.COMMENT.sub("", md)
    out = [["(before first ## section)", []]]
    for line in md.splitlines():
        if re.match(r"^\s*\|?\s*:?-{3,}", line):
            continue
        if line.startswith("## "):
            out.append([line[3:].strip(), [line[3:]]])
        else:
            out[-1][1].append(line)
    return [(title, count("\n".join(body))) for title, body in out]


def caps(outline):
    text = mdtext.COMMENT.sub("", mdtext.read(outline))
    per = [int(n.replace(",", "")) for n in re.findall(r"Word cap:\**\s*([\d,]+)", text)]
    total = re.search(r"Total cap:\**\s*([\d,]+)", text)
    guard = re.search(r"Fit guardrail:\**\s*([\d,]+)", text)
    num = lambda m: int(m.group(1).replace(",", "")) if m else None
    return per, num(total), num(guard)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("--outline")
    a = ap.parse_args()

    if a.outline and not os.path.exists(a.outline):
        print(f"wordcount: outline not found: {a.outline}")
        return 2
    secs = sections(mdtext.read(a.md))
    pre, body = secs[0], secs[1:]
    per, total_cap, guard = caps(a.outline) if a.outline else ([], None, None)
    if a.outline and len(per) != len(body):
        print(f"WARNING: {len(body)} ## sections in {a.md} but {len(per)} word caps in {a.outline}")

    total = pre[1] + sum(n for _, n in body)
    tcap = total_cap if total_cap is not None else (sum(per) if per else None)
    over = False
    print(f"{'section':<52}{'words':>7}{'cap':>7}  status")
    print(f"{pre[0]:<52}{pre[1]:>7}{'-':>7}")
    for i, (title, n) in enumerate(body):
        cap = per[i] if i < len(per) else None
        status = "" if cap is None else ("OK" if n <= cap else OVER_CAP)
        over |= cap is not None and n > cap
        print(f"{title[:50]:<52}{n:>7}{cap if cap is not None else '-':>7}  {status}")
    tstatus = "" if tcap is None else ("OK" if total <= tcap else OVER_CAP)
    over |= tcap is not None and total > tcap
    print(f"{'TOTAL':<52}{total:>7}{tcap if tcap is not None else '-':>7}  {tstatus}")
    over_guard = guard is not None and total > guard
    if guard is not None:
        print(f"{'FIT GUARDRAIL':<52}{total:>7}{guard:>7}  {OVER_GUARD if over_guard else 'OK'}")
    if not a.outline:
        print("wordcount: (no outline, caps not checked)")
        return 0
    print("wordcount: " + (OVER_GUARD if over_guard else OVER_CAP if over else "OK"))
    return 0

if __name__ == "__main__":
    sys.exit(main())
