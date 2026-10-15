# Writers

A writer is the writing skill the Content Developer applies when it writes or revises `draft.md`. It composes the prose only, under the brief, the grounding, the story frame, the outline and the mode (`SKILL.md`, "Delegating to an agent"). This file is the registry: which writer each mode uses by default, and the exact bytes each writer name stands for. `scripts/resolve_writer.py` reads it; nothing else restates it.

**Frozen means frozen.** A registered file is pinned by its SHA-256. It is never edited in place: an improvement is a new writer with its own name and row, adopted by changing the mode default below. The resolver fails on any hash mismatch, so a modified file can never run under a registered name. Never re-pin a hash to make a run pass.

Product Story currently defaults to frozen Writing V2 (why: `docs/decisions/0003-writer-selection-frozen-v2-default-better-writing-challenger.md`). A challenger (Better Writing plus a thin adapter) is evaluated outside this distribution; it is not registered and not included.

## Mode defaults

| Mode | Default writer |
|---|---|
| product-story | writing-v2 |
| commercial-proposal | none |

`none`: no writing skill; the developer writes under its own file and the mode's writing rules.

## Per-run override

The brief's `Writer` row selects the writer for that run: `default` (or an absent row) uses the mode default above; a writer name from the registry below, or `none`, overrides it. The resolved writer is recorded in the draft header's `Writer:` line (`scripts/stamp_header.py`) and carried into the freeze header.

## Registry

One row per pinned file. A writer made of several files (for example an adapter plus a pinned upstream skill) has one row per file under the same name; every file must match its hash, and the first row is the file the delegation names.

| Writer | Status | File | SHA-256 |
|---|---|---|---|
| writing-v2 | Writing V2 0.2.0, frozen | writers/decision-artifact-writing-v2.md | be61b6165fd04593d73d74f43901bf15d81e1c8abae904582824e7098757e66d |

`writers/decision-artifact-writing-v2.md` is byte-identical to the file validated in the Writing V2 experiment (Stage 1 and Stage 2; the experiment records are not distributed); its frontmatter still reads "experimental" because the bytes are frozen. Its provenance is the pinned SHA-256 above. Writer resolution and `scripts/writer_selftest.sh` depend only on this file and its hash; the selftest's optional check of the maintainer's validation copy prints SKIP in this distribution. Upstream attribution for the material the writer condenses: `THIRD_PARTY_NOTICES.md`.
