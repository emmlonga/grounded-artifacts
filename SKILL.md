---
name: grounded-decision-artifact
description: V0 runbook for turning source documents into a short, audited, audience-specific DOCX (modes commercial-proposal and product-story) - brief, source readiness, factual grounding, story frame with an owner gate, editorial classification, lean outline and draft, each audited by the lens that can judge it, then freeze, deterministic pandoc render and rendered-page QA, orchestrated manually by the owner. Use when the owner wants a grounded decision artifact from a source plan. Not for slides, not for writing without sources, not for writing the source plan itself.
---

# Grounded Decision Artifact Workflow — V0 runbook

**Coordinator:** the owner in a Claude Code session, following this file. The main session may act as the Content Developer; the auditors always run fresh. **Only this file defines the sequence.** Agents, templates and modes are cited, never restated.

`KIT` = this repository. `P` = the artifact project folder. Agents: `KIT/agents/`. Templates: `KIT/templates/`. Modes: `KIT/modes/`. Schema, verdicts, severity (P0/P1/P2), repair loci and the reopen policy: `KIT/docs/architecture/agent-instruction-standards.md` §5.

**Four authorities, in order.** The grounding says what may be said. The story frame says what matters. The outline says what the reader must understand. The writer decides the minimum evidence that makes it convincing. Rendered pages bind; planning budgets are advisory.

## Delegating to an agent

Spawn a fresh subagent (Agent tool, general-purpose; or the named agent if `KIT/agents/*.md` is symlinked into `~/.claude/agents/`) with this message, filled in:

```text
Read <KIT>/agents/<agent>.md and follow it exactly.
KIT: <KIT>   PROJECT: <P>
Mode or stage: <grounding | frame | outline | draft | revise> / <grounding | frame | outline | draft> audit, round <N>
Findings under repair: <finding IDs and their files>   (revise, round 2 and scoped audits only; never a description of a defect)
Writing skill (mode draft, and revise of the draft, only): <the "Writing skill:" path printed by resolve_writer.py; omit the line if it prints none> (<its "Writer:" line>). It composes the prose only: the grounding is the factual authority; the story frame determines the narrative; the outline states the essential propositions and the available evidence; evidence is permission to use, not an obligation to render
Write: <output path(s)>
Expected stop state: <DONE | SOURCE CLARIFICATION REQUIRED | BLOCKED(...)> / one of the four verdicts
```

**Writer.** The writing skill is resolved per run, never chosen ad hoc: run `python3 "$KIT/scripts/resolve_writer.py" artifact_brief.md` before every run that writes `draft.md` (step 12, and every revise of the draft: steps 13, 14, 15 and walk-forwards that end in a draft revise). The brief's `Writer` row is `default` (the mode default in `KIT/writers/README.md`; product-story: frozen Writing V2) or a registered writer name that overrides it for this run. A non-zero exit stops the run: a registered writer whose bytes no longer match its pinned hash never runs under its name. No other delegation (readiness, grounding, frame, pass B, outline, any auditor) carries the writing skill. `stamp_header.py` records the resolved writer in the draft header's `Writer:` line; the freeze header copies it. Registered writers are frozen: an improvement is a new registered writer, never an edit in place (why: `docs/decisions/0003-writer-selection-frozen-v2-default-better-writing-challenger.md`).

Draft-stage auditors also receive `story-frame.md` and `outline.md` (the Integrity auditor before its expectations; the Audience auditor only after its cold read, as its file says). Run the two auditors in parallel where both are called. Quote their returns (verdicts, word counts, check output) as given; do not re-derive them. Do not write a dependent artifact while its governing artifact is under audit.

**Owner gates.** A gate listed in the brief's "Gate continuation pre-authorized by owner instruction" line does not stop the run: the coordinator records the continuation and goes on. The two editorial gates (steps 7 and 13) exist only when the brief's "Editorial gates" line says required (the mode sets the default). Pre-authorization is never approval of the artifact: `Artifact approval` in the freeze header stays PENDING until the owner records it.

**Owner and coordinator findings.** A content defect the owner or coordinator finds at a source read (steps 5 and 15), the first-draft read (step 13), the freeze read (step 16) or Render QA (step 18) is written to `audits/freeze-gate-findings.md` in the canonical finding table (standard §5) with a Repair locus, and adjudicated by the developer in the stage adjudication of its locus like an auditor finding.

## Steps

**1. Set up.**
```bash
mkdir -p "$P"/{sources,audits,final/pages,notes}
cp "$KIT/templates/artifact_brief.md" "$P/"
```
Place the sources in `$P/sources/` (never edit them). Pick the artifact mode (commercial-proposal or product-story) and the render profile. If the source plan is still to be written, hand the planning session `templates/source-input-contract.md` with the mode's "Source checklist" section pasted into its last section. An agent-assisted plan is reviewed by the owner as a whole and its status line set to `owner-reviewed` before step 3.

**2. Brief.** Fill `artifact_brief.md` with the owner, every field, including whether the editorial gates are required. **Owner gate:** the owner approves and dates it.

**3. Source readiness.** Delegate to `content-developer`, mode grounding. It writes `audits/source-readiness.md` (with the material map when the mode or the corpus calls for it) and stops, except in two cases where it continues into grounding: the readiness file already exists with verdict READY and no facts to confirm; or every source is an authoritative document and the verdict is READY with nothing to confirm (the owner then reviews the readiness file and the grounding together at the grounding gate). The readiness file uses the plan's substitutions; run `check_names.py` on it once the grounding map exists, before any external paste. **Otherwise pause here:** the owner reviews the triage, answers BLOCKED items and resolves the material facts to confirm under "Owner answers" (or sends the questions back to the planning session if the plan is agent-drafted). READY WITH GAPS proceeds with the gaps carried. After answers, the next grounding run re-checks only the blocked items.

**4. Grounding, pass A.** Delegate to `content-developer`, mode grounding (it resumes after readiness). It writes the factual grounding: claims as CLAIM, MUST INCLUDE as coverage obligations, MUST PRESERVE, MUST NOT SAY, constants, map, terminology, open items. On `SOURCE CLARIFICATION REQUIRED`, the owner answers in `audits/source-readiness.md` and the run repeats. **Owner gate only if** "Decisions for owner" in `grounding.md` is non-empty.

**5. Grounding audit.** Delegate `grounding-integrity-auditor` (with the sources, or owner-cleared excerpts), stage grounding, round 1. The Audience lens does not run here; it audits the frame at step 9. Then `content-developer`, revise: adjudication first, then revision. If the revision returns `SOURCE CLARIFICATION REQUIRED`, the owner answers and the revise run repeats; the frame never starts from a grounding that still says an answer is pending. **Source read:** whenever a revision shortens or rewrites claim text (the developer's return names the rows), the owner or coordinator re-reads those rows against the source input before continuing; it takes minutes and it is where qualifiers go missing. Defects go to `audits/freeze-gate-findings.md` and are adjudicated in a scoped revise. A scoped Integrity round only if a P0 or P1 is still open after the revision.

**6. Story frame.** Delegate `content-developer`, mode frame (phase 1). It writes `story-frame.md`: thesis, transformation and tension, the spine with claim IDs, critical decisions, closing evidence, demoted subplots, owner-choice promotions with proposed defaults, a provisional title. If the brief does not require the editorial gates, the same run continues into phase 2 (step 8).

**7. Frame gate.** **Owner gate** (when required): the owner reads the frame, at most a few minutes, and records under "Owner decision": approve / hybrid / corrections, with one reason. The owner's answers to the owner-choice promotions are recorded in the same table. A pre-authorized continuation records the developer's defaults as the decision.

**8. Grounding, pass B.** Delegate `content-developer`, mode frame (phase 2). It applies the owner's corrections to the frame and sets every CLAIM row's editorial class against it (MUST COMMUNICATE · beat, MAY SAY · high or low, RESERVE · venue), changing no claim text.

**9. Frame audit.** Delegate `audience-auditor`, stage frame, round 1 (the frame and the pass-B grounding; no sources). Then `content-developer`, revise, stage frame: adjudication (`audits/frame-adjudication.md`), then revision of the frame and the classes. A class change is a row in `audits/frame-adjudication.md` with the frame's demotion list updated; never silent. The owner re-decides only a changed thesis or the reversal of a decision the owner recorded at step 7 (that item only); every other change is reported at the owner's next gate. Round 2 only on an open P0/P1.

**10. Outline.** Delegate `content-developer`, mode outline. Lean: reader question, takeaway, essential propositions, available evidence, tempting exclusions, what the section leads to, format, a soft cap. **Owner gate only if** "Decisions for owner" is non-empty.

**11. Outline audit.** Both auditors, stage outline, round 1; the Integrity packet includes the frame and checks its beats trace to pass-A claims. Revise. Every `REQUIRED` row under the adjudication's `Upstream reopens` walks forward by the rule below before continuing; a `DEFERRED (owner, <date>)` row does not. Round 2 only on an open P0/P1.

**12. Draft.** Delegate `content-developer`, mode draft, with the writing skill resolved for this run (see "Writer" above). The return must quote:
```bash
python3 "$KIT/scripts/wordcount.py" draft.md --outline outline.md
python3 "$KIT/scripts/compare.py" --md draft.md --grounding grounding.md
python3 "$KIT/scripts/check_names.py" --grounding grounding.md draft.md
python3 "$KIT/scripts/stamp_header.py" draft.md
```
Inside the draft mode, before DONE (planning budget → preview → fit pass):
1. Write the draft to the planning budget (the outline's section caps and total cap), with evidence economy as the developer file defines it, and run the private six-question and macro checks.
2. Preview render, never into `final/` (the `GROUNDING` variable is required: the script's default resolves relative to the input file's folder):
```bash
mkdir -p notes/preview
GROUNDING="$P/grounding.md" "$KIT/scripts/render.sh" draft.md <profile> notes/preview/draft.docx <max_pages>
```
3. Read the `page budget` line and the last page image in `notes/preview/pages/`. If the draft uses about 0.3 page or more less than the maximum (for 3 pages: about 2.7 pages or fewer) and the whole-draft stranger re-read finds overloaded sentences, make **one fit pass**: edits only split a sentence, add a transition, make an actor and action explicit, or move a gloss or qualifier out of an overloaded sentence into its own sentence next to the claim; never a fact, example or claim. Type size is never a fitting device.
4. After a fit pass, re-run `wordcount.py` and the preview render. The return quotes both page readings and lists the fit edits.

**Budget rule.** The rendered page maximum, at the profile's typography, and readable density (Render QA) bind. Every `wordcount.py` reading is a planning diagnostic: the section caps and total cap are the budget the first draft is written to; the fit guardrail (calibration × pages) is the reading above which a preview is likely to fail. Once a preview render passes the page maximum, word-count variance alone is never a finding, a reopen, a decision for owner or a reason to cut. A preview over the page maximum is a content defect at the DRAFT locus (cut or relocate; the outline's caps are not the fix).

**13. First-draft read.** **Owner gate** (when the editorial gates are required): the owner reads the rendered preview once as a reader, about ten minutes, before any audit: the frame's story, selectivity, planning-scaffold leakage, template feel. Findings go to `audits/freeze-gate-findings.md` with a locus (FRAME, OUTLINE or DRAFT). When findings exist, delegate the developer's revise (walking forward from the locus) before step 14 so the auditors read the corrected draft; a walk from a step-13 finding ends at step 14 round 1, not at step 15. When the gates are not required, skip this step.

**14. Draft audit.** Both auditors, stage draft, round 1. The Audience auditor runs the cold read first: give it brief and mode only in the delegation line, the rest is in its file; it then answers the chain, selectivity and naturalness questions and the mode's audience questions (product-story adds the authenticity check). Revise, one scoped revise. Every `REQUIRED` row under the adjudication's `Upstream reopens` walks forward by the rule below before continuing; a `DEFERRED (owner, <date>)` row does not. A finding class seen for the third time goes to the owner as a decision, not into another revision.

**15. Close the round.** After the scoped revise, and after every walk-forward that ends in a draft revise: run the three scripts, `stamp_header.py` and the preview render; the owner or coordinator reads the changed regions against the source input (minutes) and writes any defect to `audits/freeze-gate-findings.md`. **Re-audit only if** a P0 or P1 was open after the last adjudication, or claim text in the grounding changed; then a scoped round of the lens that judges the change (Integrity at the grounding stage, with the sources, for a claim change; Audience at the draft stage for a selection or comprehension change), delta-first, LATE FINDING only for P0/P1. An owner-dictated correction of claim text (an attribution, a rendering the owner prefers), verified by the coordinator's source read against the source input, closes without a scoped Integrity round. Otherwise the round is closed by the scripts and the source read. P2-only rounds are never re-audited.

**Walk-forward rule (steps 5, 9, 11, 14, 16, 18).** Restart from the layer named in a `REQUIRED` row of `Upstream reopens` and walk forward through every dependent artifact:
- **GROUNDING** → revise grounding → source read of the changed rows (step 5) → the developer confirms each frame beat that cites a changed claim still holds (frame revise if not; the owner re-decides only a changed thesis or a reversed owner decision) → revise outline if its coverage or propositions are affected → revise draft → close the round (step 15).
- **FRAME** → revise frame (the owner re-decides only a changed thesis or a reversed owner decision; other changes are reported at the next gate) → reclassify pass B, each change a row in `audits/frame-adjudication.md` → revise outline → revise draft → close the round.
- **OUTLINE** → revise outline → revise draft → close the round.
- **READINESS** → re-check the affected items at step 3; if the verdict or a fact to confirm changes, continue from step 4.
- **SOURCE** → owner clarification first, then restart at the earliest governed layer the answer affects.

A P2's default repair locus is the current artifact (standard §5); a cap reading, a header field or a signpost is never a reopen.

Scoped audits follow the round-2 rule: the delegation line names the findings under repair; the auditor writes its expectations from their Required outcome cells and the governing inputs, then reads the adjudication, then the changed regions (standard §4).

**16. Freeze.** The owner reads the draft once against the source input, as its author (in a delegated run the coordinator does it and the freeze header records who). Any content defect goes to `audits/freeze-gate-findings.md` with a Repair locus; the developer adjudicates it in the stage adjudication of its locus; the walk-forward rule applies; freeze after the round closes (step 15). Then copy `draft.md` to `final/content_final.md`, replacing the draft header with the filled `templates/freeze_header.md` (Continuation, Freeze read, Artifact approval; deferred reopens under accepted residuals). **Owner gate:** only the owner sets `Artifact approval: APPROVED`; a pre-authorized continuation leaves it PENDING.

**17. Render.**
```bash
"$KIT/scripts/render.sh" final/content_final.md <profile> final/<name>.docx <max_pages>
```
pandoc with the profile's `reference.docx` → Word (LibreOffice fallback) → PDF → `final/pages/page-NN.png` → text → `compare.py` and `check_names.py`. Exit 0 means every script check passed.

**18. Render QA.** The main session copies `templates/render-qa-checklist.md` to `final/render-qa.md` and reviews **every** page image against it. Content defect → `audits/freeze-gate-findings.md`, same route as step 16 (adjudication at its locus, walk-forward, close the round, re-freeze). Rendering defect → fix the profile (`profiles/build_reference_docx.py`) or the build, re-render. Never shrink type to fit.

**19. Owner edit.** The owner edits the DOCX (voice, header text, cover). Re-run `check_names.py --grounding grounding.md final/<name>.docx` on the edited file, then the departure report:
```bash
python3 "$KIT/scripts/departures.py" --frozen final/content_final.md --edited final/<name>.docx --grounding grounding.md
```
It prints "Post-freeze changes requiring owner confirmation": numbers and constants added, removed or re-rendered (mapped to their K rows), stale renderings, qualifiers dropped and I/we switches between a frozen sentence and its edited counterpart, and sentences with no counterpart in the frozen artifact. It is a list for the owner, not a gate, and it never edits the owner's file; it does not see a chronology changed without a number, a claim strengthened by word choice, or a fact dropped with a whole sentence that carried no figure, so the owner's own read still closes the step. The owner confirms each item; a confirmed change to a constant, a MUST item or a guardrail is recorded under "## Post-freeze changes" in `grounding.md` (what changed, why, whether a source is now stale). product-story: write `notes/ai-usage.md` from `templates/ai-usage-note.md`.

## What may go to an external model

Set by the brief's `external_audit`. Subagents in this session are always allowed. Every file pasted into an external model must pass `check_names.py` first.

| Stage | allowed | anonymized-only | not-allowed |
|---|---|---|---|
| Grounding audit, Integrity (pass A) | agent file + standard §5 + brief + readiness + mode file + grounding + sources | subagent only, or owner-cleared excerpts instead of sources, with the redacted grounding | subagent only |
| Frame audit, Audience | agent file + §5 and §5a + brief + readiness + mode file + frame + grounding (pass B) | same, with the redacted grounding | subagent only |
| Outline audit | agent file + §5 and §5a + brief + mode file + grounding + frame + outline | same, with the redacted grounding | subagent only |
| Draft audit | agent file + §5 and §5a + brief + mode file + grounding + frame + `outline.md` + draft (Audience: brief, mode file and draft first; frame, grounding and outline only after its cold read) | same, with the redacted grounding | subagent only |

Redacted grounding (removes the anonymization map, which never leaves `grounding.md`), then verify it:
```bash
mkdir -p audits/external
sed '/<!-- CONFIDENTIAL:START/,/<!-- CONFIDENTIAL:END -->/d' grounding.md > audits/external/grounding.redacted.md
python3 "$KIT/scripts/check_names.py" --grounding grounding.md audits/external/grounding.redacted.md artifact_brief.md story-frame.md
```
Paste the external model's findings into `audits/<stage>-<lens>.md` unchanged.

## Enforcement

| Rule | How it is enforced |
|---|---|
| Page count within budget (binding); readable density (binding) | script: `render.sh` `max_pages` at the step-12 preview and at step 17; Render QA checks 1 and 6 |
| Section word caps, total budget and fit guardrail (planning diagnostics, advisory) | script: `wordcount.py` reports the reading; no actor turns it into a finding once a preview passes (developer guard 3, auditor Never lists) |
| Constants only in accepted renderings; no stale rendering; no forbidden phrasing (including grounding tracking terms) | script: `compare.py` |
| No real name or confidential figure from the anonymization map | script: `check_names.py` (frame, draft, final, rendered text, owner-edited DOCX) |
| Owner edits after the freeze: numbers, constants, qualifiers, I/we switches and new sentences listed for the owner's confirmation | script: `departures.py` at step 19 (a list, never a gate); the owner's read for everything it cannot see |
| Rendered text matches `content_final.md` | script: `compare.py --text` (sentence diff) |
| Heading styles, body size, header and footer | by construction (profile `reference.docx`); Render QA |
| Orphan headings, split tables, density | Render QA on page images (small tables kept together by the profile) |
| Readiness verdict is right | owner pause at step 3; Integrity auditor confirms or disputes at step 5 |
| Claims supported; qualifiers and attachments kept; open items open; MUST INCLUDE as obligations; no editorial class at pass A | Integrity auditor (pass A); owner or coordinator source read after any claim-text change |
| Frame beats trace to pass-A claims without stronger causality, chronology, ownership or force | Integrity auditor at the outline audit (frame in packet); developer construction rule |
| MUST COMMUNICATE set serves the frame, not the corpus; demotions and owner-choice promotions explicit; class changes recorded | Audience auditor (frame stage); adjudication rows; owner at the frame gate |
| Evaluation criteria answered; six and chain questions; selectivity; planning-scaffold leakage; authenticity | Audience auditor (outline and draft); owner first-draft read when the editorial gates are required |
| Evidence economy: evidence placed where it explains, omitted when it does no work; labels, pointers and counts kept only when they help the reader | developer guard 7 and macro check (private); Audience auditor questions 11–12; mode writing rule 5 |
| The writer is the one the brief and the mode resolve to, with its frozen bytes; it reaches only draft and draft-revise runs | script: `resolve_writer.py` (exit 1 on a hash mismatch) and `stamp_header.py` (Writer line, exit 3); coordinator, delegation line |
| Mode integrity risks | Integrity auditor, the active mode's "Integrity risks" section |
| Repair locus routed before continuing; every REQUIRED reopen walks; P2 repairs locally by default; DEFERRED set only by the owner | coordinator, walk-forward rule and standard §5 |
| Rounds closed by scripts and a source read unless a P0/P1 is open or claim text changed | coordinator, step 15 |
| Cold read frozen before frame, grounding and outline | prohibited only; visible in the audit file's section order |
| Six-question self-check and macro check private | prohibited only |
| No invention; no silent reconciliation of conflicts; nothing marked `[OPEN]`/`[INFERRED]`/`[ESTIMATE]`/`[CONFLICT]` stated as fact | prohibited only (developer); auditable against sources only at the grounding audit and the source reads |
| Auditor wording verified before adoption; additions paid for | prohibited only; made visible by the adjudication table and its "Words" line |
| Artifacts hold current truth only | prohibited only |

## Project layout

```text
P/
├── artifact_brief.md
├── sources/
├── grounding.md            story-frame.md        outline.md            draft.md
│                           (+ grounding_v1.md, story-frame_v1.md, outline_v1.md, draft_v1.md …)
├── audits/                 source-readiness.md; grounding-integrity.md, grounding-adjudication.md; frame-audience.md,
│                           frame-adjudication.md; <stage>-integrity.md, <stage>-audience.md, <stage>-adjudication.md for stage = outline, draft;
│                           freeze-gate-findings.md (owner and coordinator findings); external/ for redacted copies
├── final/                  content_final.md, <name>.docx, <name>.pdf, <name>.txt, pages/, render-qa.md
└── notes/                  ai-usage.md (product-story); preview/ (step-12 preview render, never final/)
```
