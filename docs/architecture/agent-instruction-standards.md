# Agent instruction standards for V0

**Purpose:** rules for writing the three V0 agent files (`agents/content-developer.md`, `agents/grounding-integrity-auditor.md`, `agents/audience-auditor.md`) and the runbook, so they stay short, unambiguous and maintainable.
**Source:** instruction-design practices extracted from the author's earlier multi-agent instruction corpus. That corpus is private: the maintainer's copy of this file cites it by file and line, and those citations are omitted here; no rule depends on them. Its runtime and governance concepts (runners, grants, issue lifecycle, qualification, freeze hashes) are deliberately not imported.
**Date:** 2026-09-28

---

## 1. File shape

Every agent file has this order and nothing else. A body past about 150 lines means procedure has leaked in from the runbook or a template.

1. **Frontmatter**: `name`, `description`. The description says what the agent does, when to use it, and when never to use it. It is the only text that drives selection.
2. **Purpose**: one paragraph.
3. **Not this role**: one negation per line. "You are not a general editor. You are not the owner's voice."
4. **Inputs**: a numbered read order, and the rule for a missing input (Section 3).
5. **Step 0**: a precheck that runs before any mode or stage. Developer: source readiness. Auditors: blind expectations (Section 4).
6. **Modes** (developer) or **stage questions** (auditors). "Use exactly one mode per run." Each mode has *Use when*, numbered *You must* steps, and *Do not use for*.
7. **Outputs**: the fixed skeleton and the closed verdict vocabulary (Section 5).
8. **Reasoning duties**: the judgement this role supplies that no template can.
9. **Never**: a terse list of prohibitions, verbs first, placed just before the stop states.
10. **Stop states** and the escalation format (Section 6).
11. **Last line**: `Return to coordinator.` (Section 7)

Templates, the mode files and the runbook are **cited, never restated**. "Do not restate any of it back. Cite it." One place defines the sequence: the runbook. Agent files never describe what happens after them.

No word-count floors anywhere. Length ceilings are allowed with their reason. "Length is not evidence of rigor." (The floors were removed because they forced padding.)

## 2. Role boundaries

- State what the role optimizes for in one question, then a "Do not optimize for" list. Developer: "a selective, coherent artifact that lets this audience reach the objective with low reader effort and without a false statement"; shortness is not the goal. Auditor: "the difference between a sound artifact and an unsound one".
- A verdict is a finding, not an authorization. An auditor's APPROVE does not freeze anything; the owner does. A developer's DONE does not advance the stage; the coordinator does.
- Test boundaries by meaning, not topic. The question for the developer is not "is this a wording change?" but "does this change what the artifact claims, or only how an established claim is presented?" Presentation is the developer's call; claims are the grounding's.
- **Authority model.** Grounding governs what may be claimed. The story frame governs what matters: thesis, spine, critical decisions, demoted subplots, owner-choice promotions; it cites claims and never authorizes one. The outline governs narrative architecture: section order, takeaways, essential propositions, exclusions, closed decisions. The draft governs wording, and the writer decides the minimum evidence that makes each proposition convincing: grounded evidence is permission to use, not an obligation to render. **Neither the frame nor the outline authorizes a claim absent from the grounding.**

## 3. Inputs

- List inputs in read order. Grounding mode: brief → source input contract → mode checklist → sources. Frame mode: brief → grounding (pass A) → readiness. Outline and draft modes: brief → grounding → story frame → previous artifact → adjudication. Auditors: brief → grounding → artifact under audit → previous findings and adjudication; the stage- and lens-specific orders are in §4.
- Missing input rule. A missing **governing** input (brief, grounding, the approved story frame for an outline or draft, or the frozen outline for a draft) returns `BLOCKED(<missing input>)` and nothing else; do not proceed from a partial set. A missing **supporting** input (a previous adjudication, a profile calibration): state the limitation, continue where safe, never invent what it would have said.
- Authority is separate from evidence. The grounding is authority for claims; sources are evidence for the grounding; auditor findings are evidence for a revision, never authority for a new claim. Quote authority verbatim when citing it; do not paraphrase a constant.

## 4. Auditors: blind expectations

Before reading the artifact under audit, the auditor writes at most ten expectations, each one capable of changing the verdict. The inputs are stage- and lens-specific, because at the grounding stage the grounding is itself the artifact, and because the Audience lens must read the draft as a first-time reader:

| Stage | Integrity: expectations from | Audience: expectations from |
|---|---|---|
| Grounding audit (pass A) | brief, readiness file, mode; then the grounding against the sources | not run at pass A |
| Frame audit (story frame + grounding pass B) | not run | brief, readiness file, mode; then the frame and the pass-B classes |
| Outline audit | brief, approved grounding, approved frame (the frame's beats are checked for traceability to pass-A claims, never for prose) | brief, approved grounding, approved frame |
| Draft audit | brief, approved grounding, approved frame, approved outline | **brief and mode only**; then a cold read of the draft with the §5a answers frozen; then frame, grounding and outline as diagnostic inputs |

Examples: "the total price appears exactly once in the summary, in its accepted rendering"; "the outcome is stated directionally, with no absolute metric"; "the author's role is stated in the first two sections". The auditor does not revise them afterwards to agree with what it found. The expectations open the findings file.

This costs one short list and removes the main failure of reactive auditing: judging the artifact by what it contains instead of by what it had to contain.

**Scoped rounds** (round 2 and every scoped audit of a walk-forward): expectations first, derived from the Required outcome cells of the findings under repair and the governing inputs; then the adjudication; then the changed regions. The findings predate the revision, so the expectations stay blind. The delegation line names the findings under repair.

## 5. Outputs

- **Closed verdict vocabulary.** Auditors use exactly one of `APPROVE` / `APPROVE WITH TARGETED FIXES` / `REVISE` / `NOT AUDITABLE`. `NOT AUDITABLE` applies when a governing precondition prevents judgement (an unreadable source, a stage input absent, a confidentiality restriction that removes the evidence); it names the missing precondition and is never "probably fine". Otherwise the precedence is `REVISE > APPROVE WITH TARGETED FIXES > APPROVE`: any open P0 or P1 means `REVISE`; only P2 findings means `APPROVE WITH TARGETED FIXES`; no findings means `APPROVE`.
- **Severity, canonical for the whole workflow.** `P0` blocking: a false or unsupported claim, a contradiction with a governing source or the grounding, a wrong constant, a scope or commitment the sources do not support, or a failure of the artifact's objective. `P1` major: an important omission, a likely misunderstanding by the audience, an unclear output or value, a hidden unresolved item, a structural or narrative flaw, or a confidentiality breach. `P2` improvement: wording, redundancy, optional support, minor organization. P0 and P1 block the gate; P2 may be accepted as residual. Not a finding at any severity: any word-count reading (cap, total or guardrail) when the preview render passes the page maximum, a header or version field, or a field-size heuristic in a template. A signpost, label or count that does no reader-facing work is a finding (Audience lens) with locus DRAFT; it is never a reopen.
- **Canonical finding schema.** One table, used by both auditors and mirrored column for column in the developer's adjudication so producer and consumer never drift:

  `ID | Severity | Location | Problem | Evidence | Consequence | Repair locus | Required outcome | Suggested direction (non-binding) | Suggested wording (non-binding, optional) | Words +/-`

  The adjudication table repeats `ID | Severity | Location | Problem | Repair locus` (Evidence and Consequence are not mirrored, so the locus follows Problem there) and adds `Disposition | Reason | Change made`. The plan and the agent prompts reference this schema; they do not restate it.
- **Repair locus**, exactly one of five values:

  | Locus | Meaning |
  |---|---|
  | SOURCE | The source must be corrected or clarified by the owner; no agent edits it; it becomes a Source Clarification |
  | READINESS | The triage's classification or questions are wrong or incomplete; fixing it may require the grounding to be rerun |
  | GROUNDING | The semantic contract omitted, misclassified or misstated supported material |
  | FRAME | Grounding adequate; the selected thesis, a spine beat, a critical decision, a demotion or a promotion choice is wrong for the audience, or a beat states more than its cited claims hold; pass-B classes follow the repair |
  | OUTLINE | Grounding and frame adequate; architecture, placement, takeaway, essential proposition, exclusion or a closed decision is defective |
  | DRAFT | Grounding and outline adequate; wording caused the defect |

  The locus is a diagnosis; the coordinator routes. Disposition and locus are independent.
- **Reopen status.** Each row under `## Upstream reopens` in an adjudication carries a `Status`, exactly one of: `REQUIRED` (the default; always for P0/P1) or `DEFERRED (owner, <date>)` (P2 only, set by the owner; the grounding-compliant fallback stands and the freeze header lists the deferral under accepted residuals). No other value exists; a reopen is never "optional". The coordinator runs every REQUIRED reopen; a DEFERRED reopen does not walk. A P0 or P1 may reopen upstream when the repair changes truth, ownership, the causal model, the selection or a mandatory element. A P2's default repair locus is the current artifact; it reopens upstream only when the artifact cannot be truthfully repaired from its frozen inputs and the issue is not wording, a budget reading, a metadata discrepancy or a requirement an earlier audit created.
- **Owner and coordinator findings.** A content defect the owner or coordinator finds at a source read of changed claim text, at the first-draft read, at the freeze read or at Render QA is written to `audits/freeze-gate-findings.md` in the canonical finding schema above, with a Repair locus, and adjudicated in the stage adjudication of its locus like an auditor finding.
- **Materiality of P0 and P1.** Every P0 or P1 finding states in its Consequence cell the material belief, fact, scope, obligation, commitment, expectation or decision the defect could change. The developer never rewrites an auditor's severity: if the stated severity is not substantiated by the finding's evidence and consequence, the finding is preserved as written and adjudicated normally (ADAPT or REJECT the severity or required outcome, with the reason). A severity the developer has explicitly adjudicated as unsubstantiated does not by itself trigger a second round.
- **Findings lead with the problem, not the fix.** The schema's column order enforces this. Auditors do not dictate wording unless an authority (a constant, a MUST NOT SAY row) does.
- **Severity does not choose the disposition.** The developer's adjudication assigns `ADOPT` / `ADAPT` / `REJECT` / `DEFER` / `NO_ACTION` with a one-line cost-benefit reason; `NO_ACTION` on a P2 is a correct outcome, not a failure. A P0/P1 `REJECT` cites the source.
- **Discrimination.** "APPROVE with notes is a real result. If you can only reach APPROVE by finding nothing, you are not usable. Do not pad." The prompt must not prime an outcome: never tell an auditor that previous rounds always found something.
- **Artifacts hold current truth only.** The artifact header carries its version and the versions that govern it. Revision history and the reasons for changes live in the adjudication file, never in the artifact body. In the first reference case the grounding header grew a five-version changelog; that history goes in `audits/` now.
- **Delta-first re-review.** On a second round the auditor reads the adjudication first, verifies the changed regions, and may raise a finding on an unchanged region only if it is P0 or P1, labelled **`LATE FINDING`** in the Problem cell, with the reason it was not raised before.

## 5a. Shared audience questions

The six questions, canonical for the whole workflow:

1. What is the main point: what is proposed, or what was achieved?
2. How does it work, or how did it get done?
3. What concrete output or result does the audience get or see?
4. What value, and how is it evidenced or measured?
5. What is in and what is out: scope, trade-offs, what was not done?
6. What should the audience decide, do or ask next?

- The **Content Developer** answers them privately as completion work at the draft stage: no file, no packet; then runs the private macro check; its return message says only "six-question self-check done; macro check done".
- The **Audience Auditor** answers them cold at the draft stage and freezes the answers before reading the grounding.
- The two sets of answers never meet. Agent files cite this section and do not restate the questions.

## 6. Escalation and stop states

- Escalate before producing, not after. The developer's readiness triage exists so that grounding does not invent and then ask.
- One escalation format, already in the plan: **Missing** / **Why it matters** / **Question** / **If unavailable**. Add the decision owner when it is not the artifact owner. The "if unavailable" line is the best result within what is currently known, so that a "no" costs no cycle.
- Say what is *not* an escalation. Developer: choosing a table over a list, a heading's wording, section order within the outline's sequence. Auditor: preferring different phrasing.
- Escalate on churn: the third occurrence of the same finding class on the same artifact goes to the owner as a decision, not into another revision. A cap reading is not a finding class and never escalates.
- Stop states, parameterized: developer `DONE` / `SOURCE CLARIFICATION REQUIRED` / `BLOCKED(<missing input>)`; auditor: the four verdicts. Stop at the verdict. "A verdict that arrives with a next step attached has stopped being independent."

## 7. Handoff

- The last line of every output is `Return to coordinator.` Add one clause only when the role knows a fact the coordinator cannot derive (a source that turned out stale, a constant that appears nowhere). State domain facts, never routing. (A repeated disclaimer paragraph that appeared 73 times in the source corpus was removed for carrying no information.)
- Every handoff covers: what was done; evidence; blockers; non-blocking items; which gates remain. For the developer this is the adjudication table plus a three-line summary; for auditors, the verdict line plus the findings table.
- When the coordinator delegates, the delegation carries the task verbatim, the file paths, and the expected stop state. Returns quote readings (word counts, page counts, check results) verbatim; the coordinator never re-derives them.

## 8. Developer completion guard

Before returning `DONE`, the developer runs and reports this list. Its readings are quoted in the handoff.

1. Every frame beat, MUST COMMUNICATE row and MUST INCLUDE obligation has a home (outline: coverage table; draft: section reference).
2. Every constant appears only in an accepted rendering; no stale rendering; no forbidden phrase; no real name from the anonymization map. Quote the check output.
3. The `wordcount.py` reading and, at the draft stage, the preview page reading, quoted. Word-count readings (caps, total, guardrail) are planning diagnostics: reported, not repaired, once the preview passes the page maximum. A preview over the page maximum is a content defect.
4. Changed regions re-read as a stranger: the surrounding prose still means what it did; superseded text was replaced, not left beside its replacement.
5. Dependents of every change walked. When a value or a qualifier changed, search the artifact for words the change makes false; *every*, *all*, *both*, *complete*, *always* are the highest-yield search.
6. Nothing added once the preview is at the page maximum without something named as removed.
7. Draft stage: no clause is present only because it was grounded or listed in the outline; each carries a reader-facing job (advances, explains, evidences or orients). Labels, pointers, counts and stated trade-offs are judged by function: kept when they help orientation, progression or comprehension, dropped when they only expose a planning field.

## 9. Rationalization guard

A short table in the developer file pairing the excuse with the required response.

| Excuse | Required response |
|---|---|
| "The auditor's wording is clearer" | Verify it against the source or the grounding first; adopt only if it preserves every qualifier |
| "The source is silent, but this is obviously true" | It is an OPEN item or a Source Clarification, not a sentence |
| "It fits if the type is smaller" | It does not fit. Content defect at the draft: cut or relocate; never the type, never the caps |
| "This addition is necessary" | Name what is removed to pay for it |
| "This is just presentation" | Ask whether any claim, number, qualifier or order changed. If yes, it is content |
| "Two sources differ slightly; the difference is immaterial" | Record the conflict and apply the declared precedence, or escalate |
| "The outline lists it, so it must appear" | The outline lists propositions; evidence is permission. Use it where it explains something, or leave it |
| "An auditor asked for a pointer / a stated cost / a label" | Preserve the fact by order and attachment; a pointer, a stated cost or a label enters the prose only when it does reader-facing work |
| "It is important in the source" | Not a reason for MUST COMMUNICATE; the frame decides what matters |

## 10. Enforcement honesty

The runbook carries one table saying, for each rule, how it is enforced: **checked by script** (caps, constants, stale renderings, forbidden phrases, names, page count), **checked by an auditor** (claim classes, semantic rules, audience criteria, authenticity), or **prohibited only** (no silent reconciliation, no invention). A rule that is only prohibited is a rule nobody can check afterwards, and the table makes that visible instead of implied.

## 11. Testing the prompts

- **Dry-run each prompt on a real case before trusting it.** Five static reviews of an instruction passed one that could not be executed; only a live run found it. A real product-story run was the dry run for V0.
- **Run two regression fixtures** (both auditors, draft stage, inputs: the brief, grounding, approved outline and draft of one real case). An auditor that fails everything would score perfectly on defects; the pair tests discrimination. The maintainer's fixture pair comes from the commercial-proposal reference case and contains client material, so it is not distributed.
  - **Negative:** a draft with known material defects (three known classes in the maintainer's fixture). Expected: across the two lenses at least two of the known material defect classes are found, and each verdict follows the canonical severity and verdict rule: it must not be `APPROVE` or `APPROVE WITH TARGETED FIXES` while a known P0/P1 stands unresolved. No verdict is prescribed independently of the severity rule.
  - **Positive:** the corrected revision of that draft, same brief, grounding and outline. Expected: no P0 or P1 on the known classes; verdict `APPROVE` or `APPROVE WITH TARGETED FIXES`.
  - **Frame fixture (0.3.0):** both controls also give the auditors a minimal `story-frame.md` reconstructed from the fixture's grounding and outline (owner decision NOT REQUIRED); it adds no fact and no selection.
  - No finding counts, no severity of individual findings, no wording are prescribed. Cadence: the fixtures run once after a coherent batch of prompt changes, not after each edit.
- **Depth must vary.** The same prompts on a three-page story and on a proposal must produce visibly different process depth. If both cost the same, the mode design failed.
- **Record known gaps** next to any pass, in the case notes.

## 12. Versioning, lightly

Each agent file carries a `version:` line in its frontmatter and one line in `agents/CHANGELOG.md` per change: version, date, what changed, why. Retest trigger: any change to an auditor prompt re-runs the clean control. No hashes, no freeze records; that machinery belongs to the larger system of the source corpus and is not needed while one person maintains three files.

Three wording lessons from the source corpus's own revision record apply directly: do not prime an auditor with the history of past findings; do not claim environment guarantees the agent does not have (an auditor told its inputs are immutable when they are not learns to trust a boundary that is absent); bound every duty, because "an instruction that cannot be followed is not one".

## 13. Anti-patterns to avoid in the V0 files

From the source corpus's maintainability review and improvement plan: the same rule paraphrased in several places, each going stale on its own; checking only the files that were edited; a rule inside a code fence mistaken for a rule in force; producer and consumer formats drifting apart (the auditor's finding table and the developer's adjudication table must use the same column names); checks with no negative proof; history kept inside live artifacts; triggers keyed to topic instead of to what changed; every finding creating work because `NO_ACTION` did not exist; a stale sentence left beside its replacement.
