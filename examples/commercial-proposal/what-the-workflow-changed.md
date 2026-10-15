# What the workflow changed

This example is derived from a real workflow run. Identifying details, commercial terms and case-specific facts have been generalized or reconstructed for public use. The workflow behavior and editorial problems illustrated are representative of the original run.

**How the run actually happened.** The grounding, outline and first approved draft come from the first reference case (`../../docs/case-studies/commercial-proposal.md`). That case ran before V0 existed, with the same stage order and cross-model audits. V0's developer and two auditors were later run on that approved draft as a regression control. That round, draft v3.1 → v3.2, produced the audit findings below. The story frame for this case was reconstructed afterwards from the grounding and the outline. In this run, editorial selection happened in the grounding's claim classes and in the outline, so this example does not show a frame gate.

## 1. Grounding: what may be said

- **Two sources, one precedence rule.** The commercial document governs the framing only where it is compatible with the implementation plan, and a commercial simplification never widens a technical limit. In the original run this rule was used twice to reject audit suggestions.
- **Qualified constants.** The milestones are approximate ("about week [A]"), so the bare form ("Week [A]") is a stale rendering.
- **What must not be said, each with a permitted alternative:**

| Must not say | Permitted alternative |
|---|---|
| "Supports every calculation of this kind" | Complete for a defined initial scope; other types once validated |
| "Learns automatically from corrections" | Improvements prioritized by what real use shows |
| "Saves X% of time" | The gain will be measured in real use |
| "Unsupported cases get an approximate result" | Out-of-scope cases are flagged with the reason |
| "The support hours cover defect fixes" | Defect fixes within the accepted scope do not use the allowance |
| "We host and operate it" (open-ended) | Transfer to an environment the client controls; no indefinite hosting |

- **Open items with venues.** Each of these was allowed to stay open in an alignment proposal, with the document saying where it would close: acceptance mechanics and the end of stage 3 (definitive proposal), caps on running costs (definitive proposal), the choice of calculation engine (implementation), maintenance after rollout (separate decision).
- **Candidate framings checked against the sources.** "Not another off-the-shelf tool" was SUPPORTED, and so were "build what differentiates, reuse the rest" and "the first release is bounded". "The asset is broader than the calculation engine" and "reviewed use creates an operational asset" were SUPPORTED WITH QUALIFICATION. The second carries the qualification "no automatic training".

## 2. Editorial selection: what matters

- **Thesis.** The client can own a bounded capability that prepares the specialist's interpretation with evidence, keeps the specialist reviewing and confirming, and calculates the covered cases, delivered in three stages at a stated price plus third-party running costs.
- **Two tensions the document had to hold.** "Complete" means complete for a defined initial scope. "Own" means controlling the product, not owning every component.
- **Kept out of the reader's way and held in the grounding for the definitive proposal:** technical architecture, internal scope labels, calculation states, the detailed security checklist, competitor names and prices, recurring-cost estimates, the technical acceptance package, a maintenance offer, and internal project vocabulary.

## 3. Outline: what the reader must understand, and where

- Page 1 is a decision sheet that still works when it is forwarded on its own. The sections then follow the order of the buyer's objections.
- Nothing before the investment section asks for a decision, and nothing after it reopens explanation. That rule is now in `../../modes/commercial-proposal.md`.
- There is one visual comparison (scope). Build-versus-reuse is told in prose and bullets.
- Fixed wording rules: "complete" always comes with "for the initial scope"; the stage-2 milestone is always followed by the rollout period; the document ends on the alignment questions, with no signature, acceptance or validity clause.

## 4. The audit round: draft v3.1 → v3.2

Both lenses returned REVISE. The developer adjudicated every finding against the grounding before editing. Nothing was rejected, and the net change was −32 words.

| Severity | What an auditor found | Authority | Change |
|---|---|---|---|
| P1 | The support allowance was illustrated with activities, training and transfer support, that the grounding lists as separate stage-3 deliverables | constants; delivery model | Example clause deleted |
| P1 | The last question asked whether a requirement changed the design, but the design's integration and AI-processing premises were never stated | open items; must not say | "Design premises" condition added to section 6 |
| P2 | Evidence was widened from the key parameters to "every parameter" | grounding: evidence per critical field | Back to "key parameters" |
| P2 | Milestone labels had dropped "about", and the table mixed milestones with durations | qualified constants | "~Week [A]", "~Week [B]" |
| P2 | Stage 3 was framed as having "clear acceptance", which was still open | open items | Acceptance claimed for stages 1 and 2 only |
| P2 | The post-rollout exclusion named maintenance but not support | must include | "Maintenance and support" |
| P2 | "A workflow that can evolve with use" could be read as self-learning | owner guardrail | "Improvements prioritized by what real use shows" |
| P2 | The six alignment points were merged into four, and the price had no question of its own | brief objective | Six questions |
| P2 | The draft did not say who pays for third-party usage before the transfer | constants; dependencies | Cost paragraph completed |
| P2 | A "what changes for you" block repeated the summary | — | Deleted, paying for the additions above |

The developer did not adopt three auditor wordings, each on grounding authority. "By week [A]" would turn an approximate target into a deadline. "With acceptance at each stage" would bring back the stage-3 claim. An unscoped "only integration" would be false, because the calculation engine may be an external service.

## 5. Owner decisions

- The revise found two specifics with no trace in the brief or the grounding: a named addressee, and a claim about where the reference cases came from. Each became a decision for the owner, with the default applied: omit.
- In the original run, the owner changed two commercial terms after the freeze, outside the process. That is why V0 added the owner-edit step and the departure report (`../../SKILL.md`, step 19).

## What this example does not show

It is one case. It does not show that the workflow produces better proposals in general. In the control runs on this draft, the auditors were consistent about what they detected but not about severity: the same issue was rated P2 in one run and P0 in another. That is why findings are adjudicated against the grounding rather than adopted.
