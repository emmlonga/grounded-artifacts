# Source Input Contract

**For:** whoever writes the source plan: the owner, or a planning session run by an AI agent with the owner. The **owner** is the person the artifact speaks for and who confirms its facts (for a product story, its author).
**Purpose:** the plan, together with any documents it cites, is the only source for a short, audited artifact. This contract says what the plan must make recoverable so the artifact can be written without inventing anything. It is a checklist, not a template: cover one chosen story or offer, structure it however suits the material, and prefer complete to short; the plan is source material, not the artifact.

## 1. What the sources must make recoverable

| Area | What is needed |
|---|---|
| Context | Enough to understand the situation without the author present |
| Problem or opportunity | What existed, why it mattered then, and the evidence |
| Roles and ownership | Who did what; what the owner personally owned versus influenced |
| Decisions | The important choices, the rationale, the alternatives considered, the trade-offs |
| Execution and chronology | Major events, changes, setbacks, turning points |
| Outcomes | What happened and what supports it; directional evidence is acceptable if labelled as such |
| Uncertainty | What is unknown, disputed, estimated or inferred, stated as such |
| Source authority and uncertainty | When several sources exist, which governs which concern, as a three-column table: source, role, governs. The plan is the consolidated downstream record; the declared claim-specific authority governs each claim; where an authoritative underlying record exists it governs unless an explicit owner-approved correction or superseding decision is recorded; conflicts are never silently reconciled. Only material claims that remain inferred, estimated, open or conflicting carry a mark (section 2); owner-reviewed unmarked content is accepted input |
| Confidentiality | The owner's substitutions and anonymization instructions, or an explicit "nothing confidential" |
| Reserve material | Facts useful for questions, an appendix or a follow-up conversation that need not appear in the artifact |

## 2. Rules

1. **Unknown is a valid answer.** Write "unknown" or "cannot substantiate" rather than a plausible number or story. A gap stated honestly becomes a stated limitation; an invented fact becomes a false claim.
2. **Conflicts come with a rule.** The plan is the consolidated downstream record; the declared claim-specific authority governs each claim; where an authoritative underlying record exists it governs unless an explicit owner-approved correction or superseding decision is recorded; conflicts are never silently reconciled. If two documents or two versions disagree, state which governs, or mark the point `[CONFLICT]`.
3. **Agent-assisted plans: the owner reviews the whole plan, and only exceptions are marked.**
   - The plan starts with a status line: `Status: draft`, `owner-reviewed` or `ready for grounding`, carrying the version, review date and reviewer (`Status: owner-reviewed v3, 2026-10-02, <initials>`). Review applies only to that version: any material factual addition or change after review returns the plan to `draft` until re-reviewed. Once the owner marks a version owner-reviewed, its unmarked factual content is accepted input and needs no tag.
   - Four marks only, for material that is still not settled: `[OPEN]` (unknown or unresolved), `[INFERRED]` (an agent's or analytical inference the owner has not confirmed), `[ESTIMATE]` (an approximate figure), `[CONFLICT]` (two versions disagree). They remain exceptions in a reviewed plan and are removed only when resolved. A `[SOURCE: …]` citation is optional, where it helps.
   - The plan ends with **Material facts to confirm before grounding**: five to fifteen items at most, drawn only from the three categories where an error would damage the artifact: **metrics** (baseline, target, outcome, scale), **personal ownership** (decided, did, influenced, participated), and **decision rationale** (whether "we chose X because Y" was the reason at the time or a later reconstruction). Each item may carry a `Support` cell (document, owner confirmation, or none); the cell is optional.
4. **Authoritative documents need none of this.** When the sources are approved documents (an annex, a signed plan), the owner-review status is implicit and the precedence table is the control.
5. **Confidentiality is explicit, in its own section.** List every real name (company, product, people, clients, partners, internal code names) that must not appear, with the substitute to use, and say for each sensitive metric whether it may appear as an absolute figure, a proportion, or only a direction. If nothing is confidential, say so. The workflow enforces these instructions; it does not interpret NDAs.

## 3. How the plan will be checked

Before anything is written from it, the plan is triaged against this contract:

- **READY**: the facts the artifact's objective depends on are supported.
- **READY WITH GAPS**: desirable material is missing but nothing forces invention; each gap becomes an open item, a statement the artifact must not make, a question kept for the follow-up, or a stated limitation. An agent-assisted plan that is not yet owner-reviewed is READY WITH GAPS at best.
- **BLOCKED**: a missing fact or an unresolved conflict would force the artifact to invent or to make a materially unsupported choice; for example an unclear personal role, a success claim with no outcome evidence, or two versions disagreeing on the key decision with no rule for which governs; or the artifact's objective materially depends on a claim still marked `[OPEN]` or `[INFERRED]`.

The triage checks that every item in "Material facts to confirm" is resolved or carried as open, and may add at most ten items of its own from the same three categories (metrics, personal ownership, decision rationale) and the artifact mode's Source checklist. Questions come back only where a gap would materially weaken the artifact or require an unsupported inference, each in the form **Missing** / **Why it matters** / **Question** / **If unavailable** (what the artifact will say instead).

## 4. Mode checklist

Paste below this line the "Source checklist" section of the chosen mode file (`modes/commercial-proposal.md` or `modes/product-story.md`), replacing this paragraph.
