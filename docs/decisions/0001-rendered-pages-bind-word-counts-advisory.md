# Rendered pages bind; word counts are advisory

Status: Accepted
Date: 2026-09-30

## Context
In one product-story run, a draft that rendered within its page limit was still over its planning word cap. The caps then behaved as requirements. The overrun triggered a decision for the owner, an outline revision, a long compression revise and extra findings about metadata, and none of these consulted the render.

## Decision
Two things bind: the rendered page maximum at the profile's typography, and readable density (Render QA). Every `wordcount.py` reading is a planning diagnostic: the section caps, the total cap and the fit guardrail. Once a preview passes the page maximum, word-count variance alone is never a finding, a reopen, a decision for the owner or a reason to cut. A preview over the page maximum is a content defect at the DRAFT locus.

## Consequences
- Auditors and the developer do not raise cap overruns once the preview passes. `scripts/wordcount.py` reports its readings as ADVISORY and does not fail.
- The first draft is still written to the caps as its budget.
- Enforcement: `SKILL.md` ("Budget rule" and the enforcement table), the Never lists in the agent files, and `scripts/render.sh` (which fails a render over the page maximum).
- Open question, not part of this decision: how far the grounding and the frame may exceed their size targets without cost.

## Evidence (summary; the underlying records are not distributed)
- A retrospective of the run described above classified caps-as-requirements as a defect to fix immediately.
- In a later replay of the same story under this rule, every draft version was over its planning cap. No finding and no cut was made on a word count. The one real cut came from a preview that rendered four pages.
- Strength: one story, observed before and after the change.
