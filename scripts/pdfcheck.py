#!/usr/bin/env python3
"""Post-render identity check: does this PDF carry the sentences of this Markdown?

The DOCX text check in compare.py cannot see a PDF that Word saved from the wrong document (the shared
render-folder incident, fixed 2026-10-01, in which concurrent renders contaminated each other's PDFs). This check reads the PDF
itself (pymupdf), normalizes it exactly as compare.py normalizes rendered text, and requires the Markdown's
title, every heading and (by default) every sentence to be present.

Usage:
  pdfcheck.py --md content_final.md --pdf final/x.pdf [--min-found 1.0]
Exit: 0 PASS · 1 FAIL (foreign or truncated PDF) · 2 unreadable input
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare  # noqa: E402
import mdtext  # noqa: E402


def headings(md_plain_raw):
    out = []
    for line in mdtext.COMMENT.sub("", md_plain_raw).splitlines():
        s = line.strip()
        if s.startswith("#"):
            out.append(compare.norm(s.lstrip("#").strip()))
    return [h for h in out if h]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--min-found", type=float, default=1.0,
                    help="fraction of Markdown sentences that must appear in the PDF (default 1.0)")
    a = ap.parse_args()
    try:
        import pymupdf
        doc = pymupdf.open(a.pdf)
        pdf_text = " ".join(page.get_text("text") for page in doc)
    except Exception as e:  # noqa: BLE001
        print(f"pdf identity: FAIL (cannot read {a.pdf}: {e})")
        return 2
    md_raw = mdtext.read(a.md)
    rendered = compare.norm(pdf_text)
    sents = compare.sentences(compare.md_to_lines(md_raw))
    heads = headings(md_raw)
    missing_s = [s for s in sents if s not in rendered]
    missing_h = [h for h in heads if h not in rendered]
    found = (len(sents) - len(missing_s)) / len(sents) if sents else 1.0
    ok = found >= a.min_found and not missing_h
    print(f"pdf identity: {'PASS' if ok else 'FAIL'} "
          f"({len(sents) - len(missing_s)}/{len(sents)} sentences, {len(heads) - len(missing_h)}/{len(heads)} headings found in {os.path.basename(a.pdf)})")
    for h in missing_h:
        print("  MISSING HEADING:", h[:120])
    for s in missing_s[:10]:
        print("  MISSING:", s[:140])
    if len(missing_s) > 10:
        print(f"  ... {len(missing_s) - 10} more")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
