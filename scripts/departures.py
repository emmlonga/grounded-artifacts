#!/usr/bin/env python3
"""Post-freeze departure report: what an owner-edited artifact changed against the frozen one.

Prints "Post-freeze changes requiring owner confirmation": a list for the owner, never a verdict, never an
edit to the owner's file. Reliable subset (documented in SKILL.md step 19):
  numbers      every numeric or number-word token added, removed or changed, mapped to a constant when one of
               the grounding's accepted or stale renderings contains it; a stale rendering in the edited text
  qualifiers   a hedge or scope word present in a frozen sentence and absent from its edited counterpart
  attribution  a first-person-singular / plural switch between a frozen sentence and its counterpart
  new content  edited sentences with no counterpart in the frozen artifact (new or substantially rewritten)
Counterparts are matched by token overlap; a pure rewording with the same numbers, qualifiers and actor is not
reported. Not detected: a chronology change expressed without a number, a claim strengthened by word choice, a
fact dropped by deleting a whole sentence (deletions are listed only when they carry a number or constant).

Usage:
  departures.py --frozen final/content_final.md --edited final/<name>-owner.docx [--grounding grounding.md]
Exit: 0 (always, unless an input cannot be read: 2). The report is advisory.
"""
import argparse
import difflib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare  # noqa: E402
import mdtext  # noqa: E402

NUMBER_WORDS = r"(?:a |one |two |three |four |five |six |seven |eight |nine |ten |twelve |twenty |fifty |hundred |thousand |million |billion )"
NUM = re.compile(r"(?<![\w-])(?:\d[\d,.]*(?:\s?[–-]\s?\d[\d,.]*)?\s?(?:%|×|x|k|km|h)?|" + NUMBER_WORDS +
                 r"(?:hundred|thousand|million|billion)s?)(?![\w])", re.I)
QUALIFIERS = ["about", "roughly", "approximately", "around", "at most", "at least", "up to", "nearly", "almost",
              "eventually", "later", "initially", "at the time", "in hindsight", "potentially", "possibly", "mainly",
              "mostly", "often", "sometimes", "at times", "some", "several", "a few", "most", "not only", "not just",
              "one contributor", "also depended", "alongside", "still", "only", "never", "silently", "explicitly",
              "estimate", "directional", "we were still", "subset"]
SINGULAR = re.compile(r"\b(I|my|me)\b")
PLURAL = re.compile(r"\b(we|our|us|the team|the company)\b", re.I)


def headings(text):
    return {re.sub(r"^#+\s*", "", l.strip()).strip().lower() for l in text.splitlines() if l.strip().startswith("#")}


def sentences(text, skip=()):
    out = []
    for para in mdtext.COMMENT.sub("", text).split("\n"):
        p = para.strip()
        if not p or p.startswith("#") or p.startswith("---"):
            continue
        if p.startswith("|"):
            if re.match(r"^\s*\|?\s*:?-{3,}", p):
                continue
            for cell in mdtext.cells(p):
                out.extend(sentences(cell, skip))
            continue
        if re.search(r"\S {2,}\S", p):
            # a table row in DOCX plain text (cells separated by runs of spaces): compare cell by cell
            for cell in re.split(r" {2,}", p):
                out.extend(sentences(cell, skip))
            continue
        if p.lower() in skip or (len(p.split()) <= 10 and not re.search(r"[.!?]$", p)):
            continue  # a heading rendered as a plain line (DOCX text), or a title line
        p = re.sub(r"^\s*([-+*]|\d+[.)])\s+", "", p)
        for s in re.split(r"(?<=[.!?])\s+(?=[\"“(A-Z])", p):
            if len(s) > 12:
                out.append(s.strip())
    return out


def tokens(s):
    return set(re.findall(r"[a-z0-9]+", s.lower())) - {"the", "a", "an", "and", "of", "to", "in", "it", "that", "we", "i", "our", "its", "was", "were", "is", "on", "for", "with", "as", "by"}


def numbers(s):
    return [m.group(0).strip().lower() for m in NUM.finditer(s)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frozen", required=True, help="the frozen artifact (content_final.md or its DOCX)")
    ap.add_argument("--edited", required=True, help="the owner-edited artifact (DOCX or Markdown)")
    ap.add_argument("--grounding")
    a = ap.parse_args()
    try:
        F = mdtext.read(a.frozen)
        E = mdtext.read(a.edited)
    except Exception as e:  # noqa: BLE001
        print(f"departures: cannot read input: {e}")
        return 2
    consts = []
    if a.grounding:
        g = mdtext.read(a.grounding)
        for c in mdtext.find_table(g, "accepted", "stale") or []:
            consts.append((mdtext.col(c, "id") or "?", mdtext.variants(mdtext.col(c, "accepted")),
                           mdtext.variants(mdtext.col(c, "stale"))))

    def const_for(num):
        for cid, acc, stale in consts:
            for v in acc + stale:
                if num and num in v.lower():
                    return cid
        return ""

    heads = headings(F) | headings(E)
    fs, es = sentences(F, heads), sentences(E, heads)
    fvocab = set()
    for s_ in fs:
        fvocab |= tokens(s_)
    ftok = [tokens(s) for s in fs]
    etok = [tokens(s) for s in es]
    # best counterpart for each edited sentence
    pairs = {}
    used = set()
    for j, et in enumerate(etok):
        best, bi = 0.0, None
        for i, ft in enumerate(ftok):
            if not ft or not et:
                continue
            r = len(ft & et) / len(ft | et)
            if r > best:
                best, bi = r, i
        if bi is not None and best >= 0.25:
            pairs[j] = (bi, best)
            used.add(bi)
    rows = []  # (type, before, after, note)
    # 1. numbers, whole-document
    fn, en = [], []
    for s in fs:
        fn += numbers(s)
    for s in es:
        en += numbers(s)
    from collections import Counter
    cf, ce = Counter(fn), Counter(en)
    for n in sorted(set(cf) - set(ce)):
        where = next((s for s in fs if n in numbers(s)), "")
        rows.append(("number removed", where, "", const_for(n)))
    for n in sorted(set(ce) - set(cf)):
        where = next((s for s in es if n in numbers(s)), "")
        rows.append(("number added", "", where, const_for(n)))
    for n in sorted(set(cf) & set(ce)):
        if cf[n] != ce[n]:
            rows.append(("number count changed", f"'{n}' x{cf[n]}", f"'{n}' x{ce[n]}", const_for(n)))
    # 2. stale renderings in the edited text; accepted renderings lost
    for cid, acc, stale in consts:
        for v in stale:
            if mdtext.find_lines(E, v):
                rows.append(("stale rendering", "", v, cid))
        inF = [v for v in acc if mdtext.find_lines(F, v)]
        inE = [v for v in acc if mdtext.find_lines(E, v)]
        if inF and not inE:
            rows.append(("constant no longer in an accepted rendering (dropped or re-rendered)", "; ".join(inF), "", cid))
        elif set(inF) != set(inE):
            rows.append(("rendering changed", "; ".join(inF), "; ".join(inE) or "(none)", cid))
    # 3. qualifiers and attribution on matched pairs
    for j, (i, r) in sorted(pairs.items()):
        f, e = fs[i], es[j]
        fl, el = f.lower(), e.lower()
        dropped = [q for q in QUALIFIERS
                   if re.search(r"\b" + re.escape(q) + r"\b", fl) and not re.search(r"\b" + re.escape(q) + r"\b", el)]
        dropped = [q for q in dropped if not any(q != o and q in o for o in dropped)]
        if dropped:
            rows.append(("qualifier dropped: " + ", ".join("'%s'" % q for q in dropped), f, e, ""))
        fsg, fpl = bool(SINGULAR.search(f)), bool(PLURAL.search(f))
        esg, epl = bool(SINGULAR.search(e)), bool(PLURAL.search(e))
        if (fsg and not fpl and epl and not esg) or (fpl and not fsg and esg and not epl):
            rows.append(("attribution switched (I / we)", f, e, ""))
    # 4. new or substantially rewritten sentences
    reworded = 0
    for j, e in enumerate(es):
        if j in pairs:
            continue
        new_words = sorted(w for w in tokens(e) if len(w) >= 5 and w.isalpha() and w not in fvocab)
        if numbers(e) or new_words:
            rows.append(("new sentence with new facts or terms: " + ", ".join(new_words[:6]), "", e, ""))
        else:
            reworded += 1
    # 5. sentences removed with a number or constant (facts gone)
    for i, f in enumerate(fs):
        if i not in used and numbers(f):
            rows.append(("sentence with a figure removed", f, "", ""))

    print("Post-freeze changes requiring owner confirmation")
    print(f"frozen: {os.path.basename(a.frozen)} ({len(fs)} sentences) · edited: {os.path.basename(a.edited)} ({len(es)} sentences) · "
          f"{len(pairs)} matched, {len(es) - len(pairs)} unmatched")
    if reworded:
        print(f"({reworded} sentence(s) rewritten from the frozen text's own vocabulary and figures: not listed)")
    if not rows:
        print("none detected (the reliable subset: numbers, constants, qualifiers, I/we, new sentences)")
        return 0
    for t, b, af, note in rows:
        print(f"- [{t}]" + (f" ({note})" if note else ""))
        if b:
            print(f"    before: {b[:200]}")
        if af:
            print(f"    after:  {af[:200]}")
    print(f"{len(rows)} item(s); each is a question for the owner, not a finding. Record the confirmed ones under "
          f"'## Post-freeze changes' in grounding.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
