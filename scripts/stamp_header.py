#!/usr/bin/env python3
"""Write the current grounding, story-frame and outline versions into a draft header's "Governed by" line.

Reads the `**Version:** v<N>` field of grounding.md, story-frame.md and outline.md in the project folder (default:
the draft's folder) and rewrites the "Governed by:" line inside the draft's leading HTML comment
(templates/draft_header.md) as: <the artifact_brief.md segment, kept as written> · grounding.md v<N> ·
story-frame.md v<N> · outline.md v<N>. When the project has an artifact_brief.md, it also writes the run's resolved
writer (scripts/resolve_writer.py, which verifies the writer's frozen hash) as the "Writer:" line after it, adding the
line if the header lacks it. Nothing else in the draft changes, so headers are never hand-edited.

Usage: stamp_header.py draft.md [--project P]
Exit:  0 stamped (or already current) · 1 no "Governed by:" line in the draft header
       · 2 a governing file is missing or has no Version field
       · 3 the writer does not resolve or does not match its pinned hash (nothing is written)
"""
import argparse
import os
import re
import sys

from resolve_writer import WriterError, resolve

VERSION = re.compile(r"\*\*Version:\*\*\s*v([^\s·*]+)")
GOVERNING = ("grounding.md", "story-frame.md", "outline.md")


def version(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        m = VERSION.search(f.read())
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--project")
    a = ap.parse_args()

    project = a.project or os.path.dirname(os.path.abspath(a.draft))
    stamps = []
    for name in GOVERNING:
        v = version(os.path.join(project, name))
        if v is None:
            print(f"stamp_header: FAIL - no {name} with a **Version:** field in {project}")
            return 2
        stamps.append(f"{name} v{v}")

    with open(a.draft, encoding="utf-8") as f:
        text = f.read()
    header = re.match(r"\s*<!--.*?-->", text, re.S)
    line = header and re.search(r"^Governed by:(.*)$", header.group(0), re.M)
    if not line:
        print(f"stamp_header: FAIL - no 'Governed by:' line in the header comment of {a.draft}")
        return 1

    writer = None
    brief_path = os.path.join(project, "artifact_brief.md")
    if os.path.exists(brief_path):
        try:
            writer = resolve(brief_path)[0]
        except WriterError as e:
            print(f"stamp_header: FAIL - writer: {e}")
            return 3

    brief = [s.strip() for s in line.group(1).split("·") if s.strip().startswith("artifact_brief.md")]
    new = "Governed by: " + " · ".join(brief + stamps)
    head = header.group(0)
    start, end = line.span()
    head = head[:start] + new + head[end:]
    if writer:
        old = re.search(r"^Writer:.*$", head, re.M)
        if old:
            head = head[:old.start()] + writer + head[old.end():]
        else:
            at = head.index(new) + len(new)
            head = head[:at] + "\n" + writer + head[at:]
    text = head + text[header.end():]
    with open(a.draft, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"stamp_header: {new}")
    print(f"stamp_header: {writer or 'Writer: not stamped (no artifact_brief.md in the project)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
