# Grounded Artifacts

**An agentic workflow for turning source material into grounded, audience-specific decision artifacts.**

**truth → editorial selection → structure → writing → verification**

Built for high-stakes artifacts where factual correctness isn't enough. The system keeps four questions apart: what is true, what matters, what the reader needs to understand, and how to say it well.

```
Sources
   ↓
Grounding               what may be said            Integrity audit against the sources
   ↓
Story frame  ← owner decision: what matters
   ↓
Editorial selection     what reaches the reader     Audience audit
   ↓
Lean outline            what the reader must grasp  Integrity + Audience audits
   ↓
Writer                  how it is said              Integrity + Audience audits, owner read
   ↓
Rendered artifact       does the page still say it  scripted checks + page-by-page QA
```

It is a Claude Code kit for turning source documents into a short, audience-specific decision artifact, such as a buyer-facing proposal or a written product story. Every claim traces to a source. Each stage is audited by the lens that can judge it. The result renders deterministically to DOCX, and you check the rendered pages before anything is final.

## The problem

Ask a model to "write a three-page proposal from these documents" and you get one of two failures: fluent text with claims the sources do not support, or a faithful text that reads like the sources rearranged.

Factual grounding fixes the first failure and does nothing for the second. A grounded draft can be true in every sentence and still fail the reader. It gives every supported fact equal weight and tells no particular story. Compressing it drops qualifiers, so "aimed to reduce" becomes "reduced". Planning labels leak into the prose. It runs past the page limit. Each audit round adds material and nothing pays for it.

This kit treats a short artifact as five layers, each with its own authority, artifact and check:

| Layer | Question | Artifact | Checked by |
|---|---|---|---|
| **Truth** | What may be said? | source readiness triage, factual grounding (claims, constants, open items, what must not be said) | Integrity auditor against the sources; owner source reads |
| **Editorial selection** | What matters for this reader? | story frame (thesis, spine, critical decisions, demoted subplots), editorial classification of each claim | Audience auditor; owner frame gate |
| **Structure** | What must the reader understand, and where? | lean outline (reader question, takeaway, essential propositions per section) | both auditors |
| **Writing** | What is the least evidence that makes it convincing? | draft, written under a pinned writing skill, with evidence treated as permission rather than obligation | both auditors (the Audience auditor reads it cold first); owner first-draft read |
| **Verification** | Does the rendered document still say exactly that? | frozen content, DOCX, PDF, page images | scripts (constants, forbidden phrasing, anonymized names, sentence diff, page budget, PDF identity) and a rendered-page QA checklist |

The rule that ties the layers together: the grounding says what may be said, the story frame says what matters, the outline says what the reader must understand, and the writer decides the minimum evidence. The rendered page count binds. Word counts are planning aids.

## Who it is for

People who must produce a short, high-stakes document from a larger body of material that they own or can vouch for, and who are willing to make the editorial decisions themselves. The workflow is run by that person (the **owner**) in a Claude Code session. It asks the owner questions instead of inventing answers, and it never approves its own output.

It is not for slides, for writing without sources, or for writing the source material itself.

## Modes

| Mode | Artifact | Defaults |
|---|---|---|
| `commercial-proposal` | A buyer-facing proposal that lets the buyer decide or align on what is bought, what it costs and what they must do, without unsupported promises | `plain` profile; no writing skill; editorial gates off by default; integrity risks such as accidental warranties and hidden costs |
| `product-story` | A first-person written story of a product the author built, read by evaluators against explicit criteria (2 to 3 pages) | `plain` profile; frozen Writing V2; editorial gates required; authenticity check; anonymization enforced by script |

A mode file (`modes/`) sets the required elements, default narrative, integrity risks, audience questions and source checklist.

## How a run works

`SKILL.md` is the runbook and the only file that defines the sequence. In outline:

1. **Set up and brief.** Create a project folder outside this repository, copy `templates/artifact_brief.md`, and fill it with the audience, objective, evaluation criteria, page budget, guardrails and confidentiality instructions. The owner approves the brief.
2. **Source readiness.** The Content Developer triages the sources against `templates/source-input-contract.md` and asks only the questions that would otherwise force invention.
3. **Factual grounding (pass A)**, audited by the Grounding Integrity Auditor against the sources.
4. **Story frame**, approved by the owner at a short gate, then **editorial classification (pass B)**, audited by the Audience Auditor.
5. **Lean outline**, audited by both auditors.
6. **Draft**, with a preview render and at most one readability-only fit pass. The owner reads the draft once, then both auditors audit it. The developer adjudicates every finding before revising.
7. **Freeze, render and Render QA** of every page image, then the owner's own edit, followed by a report that lists anything the edit changed in numbers, qualifiers or attribution.

Findings use one canonical schema with a severity (P0, P1, P2) and a repair locus (SOURCE, READINESS, GROUNDING, FRAME, OUTLINE, DRAFT). A defect is repaired at the layer it came from, and every layer that depends on that layer is revised in turn.

## Requirements

- [Claude Code](https://claude.com/claude-code). The runbook delegates stages to fresh subagents.
- `pandoc` and Python 3 with `pymupdf` (`pip install pymupdf`).
- PDF conversion: Microsoft Word on macOS (driven by AppleScript), or LibreOffice (`soffice`) as the fallback. The render script is `zsh`. macOS with Word is the only tested platform.
- Optional: poppler (`pdftoppm`), so that agents can read PDF sources as page images.

Build the render profile's reference document once, from your own pandoc installation (it is not distributed; see `THIRD_PARTY_NOTICES.md`):

```bash
python3 profiles/build_reference_docx.py plain
```

Check the install:

```bash
scripts/selftest.sh
```

```bash
scripts/writer_selftest.sh
```

`selftest.sh` renders a synthetic fixture and proves that every check fails on a planted defect. The first run may ask macOS to allow automation of Microsoft Word. `writer_selftest.sh` checks writer resolution and the frozen-writer hash guard.

## Starting a run

```bash
KIT="$PWD"
P=~/artifacts/my-proposal
mkdir -p "$P"/{sources,audits,final/pages,notes}
cp "$KIT/templates/artifact_brief.md" "$P/"
```

Then follow `SKILL.md` from step 1, in a Claude Code session opened on the project folder. Keep project folders outside this repository: they hold your real sources.

Optional: make the kit discoverable to Claude Code as a skill (its skill name is `grounded-decision-artifact`) and its agents as named subagents:

```bash
ln -s "$PWD" ~/.claude/skills/grounded-decision-artifact
```

```bash
ln -s "$PWD"/agents/*-*.md ~/.claude/agents/
```

## Writer selection

A **writer** is the writing skill the Content Developer applies when it writes or revises the draft. It governs expression only. It never reaches the grounding, frame or outline stages or any auditor.

- `writers/README.md` is the registry. `product-story` defaults to `writing-v2` and `commercial-proposal` to `none`.
- The brief's `Writer` row overrides the default for one run: use `default`, a registered name, or `none`.
- Registered writers are pinned by SHA-256. `scripts/resolve_writer.py` refuses to run a writer whose bytes changed, and `scripts/stamp_header.py` records the resolved writer in the draft header. An improvement becomes a new registered writer. A frozen writer is never edited in place.

## Repository layout

| Path | Contents |
|---|---|
| `SKILL.md` | The runbook: 19 steps, the delegation message, what may go to an external model, and an enforcement table that says how each rule is checked |
| `agents/` | `content-developer.md`, `grounding-integrity-auditor.md`, `audience-auditor.md` |
| `modes/` | `commercial-proposal.md`, `product-story.md` |
| `templates/` | Brief, source input contract, readiness, grounding, story frame, outline, draft and freeze headers, adjudication, Render QA checklist, AI usage note |
| `writers/` | Writer registry and the frozen Writing V2 skill |
| `scripts/` | `render.sh` (pandoc → DOCX → PDF → page images → checks), `compare.py`, `check_names.py`, `wordcount.py`, `pdfcheck.py`, `stamp_header.py`, `resolve_writer.py`, `departures.py`, and the self-tests |
| `profiles/` | `profiles/plain/profile.md` (typography and calibration) and `build_reference_docx.py`, which generates each profile's `reference.docx` from your pandoc installation |
| `docs/` | Design standard for the agent files (part of it is read at runtime), decision records, and a case study. See `docs/README.md` |
| `examples/` | Public teaching examples, derived from real runs and generalized (`examples/README.md`) |

## Maturity and limitations

- **V0.** The owner orchestrates by hand, following the runbook. There is no state file, scheduler or plugin packaging. Possible later versions (an automated workflow layer, a slide-deck branch) are not built, and nothing here depends on them.
- **Evidence is small.** The design comes from a few real runs (one commercial proposal, a few runs of one product story) plus synthetic fixtures. The decision records and the case study say what each choice rests on. Treat the workflow as a considered method, not a benchmarked one.
- **DOCX only.** The tested PDF path is Microsoft Word on macOS, and the profile calibration was measured with it. The LibreOffice fallback is less exercised, so re-measure the calibration before you rely on a page budget with it.
- **Cost.** A run has several owner gates and audit rounds, by design. The first reference case, run before V0's cost controls, took about a day of orchestration (`docs/case-studies/commercial-proposal.md`). For a low-stakes document this is the wrong tool.
- **Auditor regression fixtures are not included.** The maintainer's fixture pair contains client material. `scripts/selftest.sh` covers the scripts and the render path, not the agents' judgment.
- The workflow enforces the confidentiality and anonymization instructions you record in the grounding. It does not interpret NDAs or decide what is safe to share.

## Examples

[`examples/commercial-proposal/`](examples/commercial-proposal/README.md) walks through one alignment-stage proposal end to end: the brief, where the sources pulled apart, what each layer decided, a real audit round, and the resulting proposal. It is derived from a real run and generalized for publication.

[`examples/product-story/`](examples/product-story/README.md) shows a two-page product story built from a synthetic test fixture: a readiness check that blocks on unsupported claims, the ownership line written into the grounding, and audits catching the same overstatement at three layers.

## Third-party material

Writing V2 condenses material from two MIT-licensed writing skills. The render profile's reference document is generated locally from pandoc and is not distributed. Details are in `THIRD_PARTY_NOTICES.md`.

## License

MIT. See `LICENSE`. Third-party attributions are in `THIRD_PARTY_NOTICES.md`.
