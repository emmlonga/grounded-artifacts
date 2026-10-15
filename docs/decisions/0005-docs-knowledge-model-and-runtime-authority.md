# Docs never define the runtime

Status: Accepted
Date: 2026-10-01

## Context
Design notes, plans and experiment records were once mixed, so it was hard to tell what the system is, why it is that way, and what was merely history. Old plans were read as if they still governed.

## Decision
Active workflow semantics are defined outside `docs/`, only by `SKILL.md`, `agents/`, `modes/`, `templates/`, `writers/`, `scripts/` and `profiles/`. Documents under `docs/` are organised by the role they play: `architecture/` (how the system is designed), `decisions/` (accepted choices in force) and `case-studies/` (lessons from real applications). They explain and record. Where one disagrees with a runtime file, the runtime file governs. The maintainer keeps validation records and an evolution backlog separately. Being written in the backlog is never adoption.

## Consequences
- A change enters the workflow only through the runtime files, with the evidence and regression testing it needs. The decision record or architecture text is updated afterwards.
- Known exception, deliberately kept: the auditors and the developer read the canonical finding schema (§5) and the shared audience questions (§5a) of `../architecture/agent-instruction-standards.md` at runtime (`agents/*.md`, `templates/adjudication.md`, `SKILL.md`). Those sections are runtime-authoritative even though the file lives under `docs/`. Relocating them would be a runtime change.

## Evidence
- `SKILL.md` is the only file that defines the sequence. Agents, templates and modes are cited, never restated (`SKILL.md`, opening paragraph).
