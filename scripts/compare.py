#!/usr/bin/env python3
"""Compare rendered text against the frozen Markdown, and check constants against the grounding.

Generalized from the first reference case's compare script: the sentence diff is the same method; the hard-coded
token list is replaced by the grounding's Constants table (accepted and stale renderings) and the
Terminology table (forbidden phrasing).

Usage:
  compare.py --md draft.md --grounding grounding.md                  # draft stage: token checks only
  compare.py --md content_final.md --text final/x.txt --grounding grounding.md   # after render
Exit: 0 pass · 1 a check failed
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdtext  # noqa: E402


def md_to_lines(md):
    md = mdtext.COMMENT.sub("", md)
    out = []
    for line in md.splitlines():
        if re.match(r"^\s*\|?\s*:?-{3,}", line) or re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            continue
        if line.strip().startswith("|"):
            out.extend(mdtext.cells(line))
            continue
        line = re.sub(r"^\s{0,3}(#{1,6}\s+|>\s?)", "", line)
        line = re.sub(r"^\s*([-+*]|\d+[.)])\s+", "", line)
        out.append(line)
    text = "\n".join(out)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|$])", r"\1", text)
    text = re.sub(r"(?<!\w)_|_(?!\w)", "", text)
    return text.replace("---", "-").replace("--", "-")


def norm(s):
    s = mdtext.normalize_map(s)[0]
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([,.;:?!)])", r"\1", s)
    return re.sub(r"\(\s+", "(", s).strip()


def sentences(text):
    parts = []
    for line in text.splitlines():
        for p in re.split(r"(?<=[.;:?!])\s+", norm(line)):
            p = p.strip(" -")
            if len(p) > 12:
                parts.append(p)
    return parts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--text", help="text extracted from the rendered DOCX")
    ap.add_argument("--grounding")
    a = ap.parse_args()

    md_raw = mdtext.read(a.md)
    md_plain = md_to_lines(md_raw)
    # token checks run on the Markdown with comments blanked, so reported lines match the file
    md_search = mdtext.COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), md_raw)
    failed = False

    if a.text:
        doc = norm(mdtext.read(a.text))
        md_s = sentences(md_plain)
        missing = [s for s in md_s if s not in doc]
        print(f"sentences: {len(md_s)} in markdown; missing in rendered text: {len(missing)}")
        for s in missing:
            print("  MISSING:", s[:160])
        failed |= bool(missing)

    if a.grounding:
        g = mdtext.read(a.grounding)
        consts = mdtext.find_table(g, "accepted", "stale") or []
        terms = mdtext.find_table(g, "forbidden") or []
        rendered = mdtext.read(a.text) if a.text else None
        print(f"constants: {len(consts)} row(s); terminology rows with forbidden phrasing: "
              f"{sum(1 for t in terms if mdtext.variants(mdtext.col(t, 'forbidden')))}")
        for c in consts:
            cid = mdtext.col(c, "id") or "?"
            accepted = mdtext.variants(mdtext.col(c, "accepted"))
            used = []
            for v in accepted:
                n_md = len(mdtext.find_lines(md_search, v))
                if not n_md:
                    continue
                if rendered is not None:
                    n_tx = len(mdtext.find_lines(rendered, v))
                    ok = n_tx >= n_md
                    failed |= not ok
                    used.append(f"'{v}' md={n_md} text={n_tx}{'' if ok else ' LOST IN RENDER'}")
                else:
                    used.append(f"'{v}' x{n_md}")
            for label, body in (("md", md_search), ("text", rendered)):
                if body is None:
                    continue
                skip = [s for v in accepted for s in mdtext.spans(body, v)]
                for v in mdtext.variants(mdtext.col(c, "stale")):
                    for line in mdtext.find_lines(body, v, spans_to_skip=skip):
                        failed = True
                        print(f"  STALE {cid} '{v}' in {label} (line {line})")
            print(f"  {cid}: " + ("; ".join(used) if used else "not used"))
        for t in terms:
            for v in mdtext.variants(mdtext.col(t, "forbidden")):
                for label, body in (("md", md_search), ("text", rendered)):
                    if body is None:
                        continue
                    for line in mdtext.find_lines(body, v):
                        failed = True
                        print(f"  FORBIDDEN '{v}' in {label} (line {line})")

    print("compare: FAIL" if failed else "compare: PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
