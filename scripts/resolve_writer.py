#!/usr/bin/env python3
"""Resolve the run's writer from the brief and the writer registry, and verify its frozen bytes.

Reads the brief's `| Mode |` and optional `| Writer |` rows. Writer `default` (or no row) takes the mode default from
KIT/writers/README.md ("Mode defaults"); a registered name or `none` overrides it. Every file registered under the
resolved name must match its pinned SHA-256 ("Registry"); a mismatch fails, so a modified file never runs under a
registered name. Prints two lines:

  Writer: <name> (<default for <mode> | override in brief>) · <status> · <file> sha256 <hex> [· <file> sha256 <hex> …]
  Writing skill: <absolute path of the first registered file> | none

The Writer line is the run provenance (stamp_header.py writes it into the draft header); the Writing skill line goes
on the delegation line of draft and draft-revise runs only (SKILL.md, "Delegating to an agent").

Usage: resolve_writer.py artifact_brief.md
Exit:  0 resolved and verified · 1 a registered file is missing or does not match its hash
       · 2 the brief's mode or writer is not in the registry (or the brief has no Mode row)
"""
import hashlib
import os
import re
import sys

# WRITER_REGISTRY points at another registry (tests only). Registry paths are relative to the kit: the registry's grandparent.
REGISTRY = os.path.abspath(os.environ.get("WRITER_REGISTRY") or
                           os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "writers", "README.md"))
KIT = os.path.dirname(os.path.dirname(REGISTRY))


class WriterError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def table(text, heading):
    """Rows (lists of cells) of the first Markdown table under `## <heading>`, header and rule excluded."""
    section = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not section:
        raise WriterError(2, f"no '## {heading}' section in {REGISTRY}")
    rows = [[c.strip() for c in line.strip().strip("|").split("|")]
            for line in section.group(1).splitlines() if line.strip().startswith("|")]
    return rows[2:]


def field(text, name):
    m = re.search(rf"^\|\s*{re.escape(name)}\s*\|\s*([^|]*?)\s*\|", text, re.M)
    return m.group(1) if m else None


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def resolve(brief_path):
    """Return (writer line, writing-skill path or None). Raise WriterError on any failure."""
    with open(brief_path, encoding="utf-8") as f:
        brief = f.read()
    with open(REGISTRY, encoding="utf-8") as f:
        registry = f.read()

    mode = field(brief, "Mode")
    defaults = {r[0]: r[1] for r in table(registry, "Mode defaults")}
    if mode not in defaults:
        raise WriterError(2, f"brief Mode {mode!r} has no default writer in writers/README.md")
    chosen = (field(brief, "Writer") or "default").strip("` ")
    if chosen in ("", "default"):
        name, why = defaults[mode], f"default for {mode}"
    else:
        name, why = chosen, "override in brief"
    if name == "none":
        return f"Writer: none ({why})", None

    rows = [r for r in table(registry, "Registry") if r[0] == name]
    if not rows:
        raise WriterError(2, f"writer {name!r} is not in the registry (writers/README.md)")
    parts = [f"{name} ({why})", rows[0][1]]
    for _, _, rel, pinned in rows:
        path = os.path.join(KIT, rel)
        if not os.path.isfile(path):
            raise WriterError(1, f"{rel} is missing")
        actual = sha256(path)
        if actual != pinned:
            raise WriterError(1, f"{rel} sha256 {actual} does not match the pinned {pinned}: the frozen writer "
                                 f"'{name}' was modified. Restore the pinned bytes (git checkout); never re-pin to run")
        parts.append(f"{rel} sha256 {pinned}")
    return "Writer: " + " · ".join(parts), os.path.join(KIT, rows[0][2])


def main():
    if len(sys.argv) != 2:
        print("usage: resolve_writer.py artifact_brief.md")
        return 2
    try:
        line, path = resolve(sys.argv[1])
    except WriterError as e:
        print(f"resolve_writer: FAIL - {e}")
        return e.code
    print(line)
    print(f"Writing skill: {path or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
