# <Stage> adjudication — <artifact name>

<!-- Written by the Content Developer before revising (revise instruction). One file per stage:
     audits/grounding-adjudication.md, audits/frame-adjudication.md, audits/outline-adjudication.md,
     audits/draft-adjudication.md.
     A second round appends "## Round 2" with the same shape. The first five columns mirror the auditors'
     finding table (canonical schema: docs/architecture/agent-instruction-standards.md §5); Evidence and Consequence
     are not mirrored, so Repair locus follows Problem here. -->

## Round 1

**Artifact:** <file> v<N> → v<N+1> · **Findings:** audits/<stage>-integrity.md (<verdict>), audits/<stage>-audience.md (<verdict>)

| ID | Severity | Location | Problem | Repair locus | Disposition | Reason | Change made |
|---|---|---|---|---|---|---|---|
| I-01 | | | | | | | |
| A-01 | | | | | | | |

<!-- Disposition: ADOPT / ADAPT / REJECT / DEFER / NO_ACTION, with a one-line cost-benefit Reason.
     Severity does not choose the disposition; NO_ACTION on a P2 is a valid outcome.
     A P0 or P1 REJECT quotes, in Reason, the source, grounding or outline closed-decision line it relies on.
     ADAPT states what was done instead. DEFER says to whom and when.
     Repair locus: the locus never determines the disposition; adjudicate first. The auditor's locus may be rejected
     or adapted with a reason. Only when the disposition is ADOPT or ADAPT and the accepted locus is upstream of this
     artifact (SOURCE / READINESS / GROUNDING / FRAME / OUTLINE): apply the grounding-compliant fallback in the current
     artifact now, and record the reopen under "## Upstream reopens"; a SOURCE locus also becomes a Source
     Clarification in audits/source-readiness.md. A P2 reopens upstream only when the current artifact cannot be
     truthfully repaired from its frozen inputs (standard §5); a word-count reading or a header version is never
     a finding; a signpost that does no reader-facing work is a DRAFT finding and never a reopen. A pass-B class change (MUST COMMUNICATE / MAY SAY / RESERVE) made after the frame
     gate never happens silently: the adopted finding is a row in the current stage's adjudication with a REQUIRED
     FRAME reopen, and the class change itself is a row in audits/frame-adjudication.md when the frame is revised.
     Only genuinely unresolved choices go under Decisions for owner.
     Findings from audits/freeze-gate-findings.md (owner or coordinator: a source read, the first-draft read, the freeze read or Render QA) are adjudicated here,
     in the adjudication of their locus, exactly like auditor findings. -->

**Net words:** +<N> / −<N> · sections over cap: <none / list>
**Summary:** <what changed> · <what was rejected, and on what authority> · <what remains open>
**Open P0/P1 after this revision:** <none / IDs>
**Decisions for owner:** <none / list, including any finding class seen for the third time>

## Upstream reopens

<!-- Empty when no ADOPT/ADAPT finding has an upstream locus. The coordinator routes these (SKILL.md, walk-forward rule).
     Status is exactly one of (standard §5): REQUIRED (the default; always for P0/P1) or DEFERRED (owner, <date>)
     (P2 only; only the owner sets it; the fallback already applied stands; the freeze header lists it under accepted
     residuals). Never "optional". When you think the owner may reasonably defer a P2 reopen, write it REQUIRED and put
     a one-line case for deferral under Decisions for owner. -->

| Finding | Repair locus | Required reopen | Status |
|---|---|---|---|
