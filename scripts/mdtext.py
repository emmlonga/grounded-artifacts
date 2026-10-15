"""Shared helpers for the V0 check scripts: read grounding tables, normalize text, find terms.

Tables are located by their header row, not by section number, so the grounding template can be
edited freely as long as the column names stay. Multiple renderings in one cell are separated by ';'.
"""
import re
import subprocess
import unicodedata

EMPTY = {"", "-", "—", "–", "n/a", "none", "na"}
TRANS = {" ": " ", " ": " ", " ": " ", "‘": "'", "’": "'", "“": '"', "”": '"',
         "–": "-", "—": "-", "…": "...", "*": "", "`": "", "•": " ", "◦": " "}
COMMENT = re.compile(r"<!--.*?-->", re.S)


def read(path):
    if path.lower().endswith(".docx"):
        return subprocess.run(["pandoc", "-t", "plain", "--wrap=none", path],
                              capture_output=True, text=True, check=True).stdout
    with open(path, encoding="utf-8") as f:
        return f.read()


def tables(md):
    """Yield (header_cells, rows) for every pipe table in a Markdown string."""
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            head = cells(lines[i])
            rows = []
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            yield head, rows
        else:
            i += 1


def cells(line):
    parts = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [p.strip().replace("\\|", "|") for p in parts]


def find_table(md, *needles):
    """First table whose header contains every needle (case-insensitive); rows as dicts keyed by header."""
    for head, rows in tables(md):
        low = [h.lower() for h in head]
        if all(any(n in h for h in low) for n in needles):
            return [dict(zip(low, r)) for r in rows]
    return None


def col(row, needle):
    for k, v in row.items():
        if needle in k:
            return v
    return ""


def variants(cell):
    out = []
    for v in cell.split(";"):
        v = v.strip().strip("`").strip().strip('"').strip("'").strip()
        if v.lower() not in EMPTY:
            out.append(v)
    return out


def normalize_map(text, strip_accents=False):
    """Casefolded, typographically normalized text plus the original index of every output character."""
    out, idx = [], []
    for i, ch in enumerate(text):
        n = TRANS.get(ch, ch)
        n = unicodedata.normalize("NFKD" if strip_accents else "NFKC", n)
        if strip_accents:
            n = "".join(c for c in n if not unicodedata.combining(c))
        for c in n.casefold():
            out.append(c)
            idx.append(i)
    return "".join(out), idx


def term_regex(term, strip_accents=False):
    toks = normalize_map(term, strip_accents)[0].split()
    return re.compile(r"(?<!\w)" + r"\s+".join(re.escape(t) for t in toks) + r"(?!\w)")


def find_lines(text, term, strip_accents=False, spans_to_skip=()):
    """Line numbers (1-based) of every occurrence of term in text; matches inside spans_to_skip are ignored."""
    norm, idx = normalize_map(text, strip_accents)
    found = []
    for m in term_regex(term, strip_accents).finditer(norm):
        start = idx[m.start()]
        if any(a <= start < b for a, b in spans_to_skip):
            continue
        found.append(text.count("\n", 0, start) + 1)
    return found


def spans(text, term, strip_accents=False):
    norm, idx = normalize_map(text, strip_accents)
    return [(idx[m.start()], idx[m.end() - 1] + 1) for m in term_regex(term, strip_accents).finditer(norm)]
