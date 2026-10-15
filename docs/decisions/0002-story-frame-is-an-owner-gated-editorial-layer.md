# The story frame is a distinct, owner-gated editorial layer

Status: Accepted
Date: 2026-09-30

## Context
Editorial choices were being made during grounding and outlining: the thesis, the tension, which supported facts carry the story, the title. They were never recorded and never gated. The owner's "Decisions for owner" gate opened only for uncertainty about facts or ownership, so framing disputes surfaced late, as rewrites.

## Decision
Between factual grounding and the outline, the workflow keeps an explicit story frame. It is a short artifact: thesis, transformation and tension, a spine with claim IDs, critical decisions, closing evidence, demoted subplots, and owner-choice promotions. The Content Developer writes it, the Audience Auditor audits it for selectivity, and the owner approves it at a frame gate when the brief requires editorial gates. Grounding is split into two passes: pass A is factual, with no editorial class; pass B classifies the claims after the frame exists. The owner's first read of the rendered draft is a second editorial gate.

## Consequences
- The frame, not the grounding, says what matters. The outline serves the frame, and both auditors have frame-stage questions.
- The two editorial gates exist only when the brief's "Editorial gates" line says required. The mode sets the default.
- Open questions, not part of this decision: frame size, how later owner promotions accumulate, and how fine-grained pass A should be.
- Runtime definition: `SKILL.md` steps 6, 7 and 13; `templates/story-frame.md`; `agents/content-developer.md` (frame mode).

## Evidence (summary; the underlying records are not distributed)
- Before the frame: a retrospective of a product-story run found that the missing editorial layer caused late framing disputes and rewrites. The layer was designed from that analysis.
- After the frame: in a replay of the same story, the owner judged the frame gate and the first-draft read to be the gates that most earned their place. The editorial decision moved before the outline and held.
- Strength: one story, observed before and after the change. Not yet tested on other genres.
