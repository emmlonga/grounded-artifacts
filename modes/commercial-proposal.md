# Mode: commercial-proposal

A buyer-facing proposal that must let the buyer decide (or align) on what they are buying, what it costs and what they must do, without a promise the sources do not support. Reference case: an alignment-stage proposal for a client (`docs/case-studies/commercial-proposal.md`).

## Defaults

| Setting | Default |
|---|---|
| Render profile | plain, or a house profile added under `profiles/` |
| Budget | set in the brief; in the reference case a 5-page alignment proposal with tables held ~1,500 body words at its profile's calibration (~300 words/page); measure your own profile |
| Grounding size target | 2,500 words |
| external_audit | set in the brief |
| Integrity risks | **on** (this file's section; Integrity auditor, outline and draft audits) |
| Authenticity check | off |
| Editorial gates | not required by default (the brief may require them when several value propositions compete or the proposal is highly compressed); the story frame is still written and governs pass B |
| Material map | off unless the readiness triage sees competing value propositions |

## MUST INCLUDE

The grounding classes each of these as MUST INCLUDE, or records why it is absent (OPEN item with venue):

1. What is bought: the concrete capability or deliverable, not the technology.
2. Investment: total and per stage, in the constants table.
3. Payment structure.
4. Acceptance principle per stage (at alignment maturity: the principle; at definitive: the criteria).
5. Recurring costs: who pays what after delivery; no figure without source support.
6. Support boundary: what support is included, for how long, and what is not (defect correction versus other support).
7. Responsibilities: what the buyer must provide.
8. Future scope: what is explicitly not included now.

## Maturity rules

- **Alignment:** approximate timing ("about 4 weeks"), acceptance principle rather than criteria, open items classified by venue and allowed to stay open; ends with explicit alignment questions.
- **Definitive:** exact values and dates, acceptance criteria, contractual precision; an open item on a MUST INCLUDE field is a blocker.

Open-item venues: OK FOR ALIGNMENT · IMPLEMENTATION QUALIFICATION · DEFINITIVE PROPOSAL / CONTRACT · FUTURE PHASE.

## Optional modules (activated by the grounding, not by default)

| Module | Activate when the grounding shows | Content |
|---|---|---|
| Build vs buy | the buyer will compare with a market product | what is owned and controlled, what is reused, why |
| Trust model / human review | outputs need review before use | what the system prepares, what a person confirms, what is never inferred silently |
| Scope pedagogy | scope is bounded by structure, not by a list | domain → supported structures → reference family, with representative in/out examples |
| Confidentiality clause | the buyer's data is sensitive | one positive sentence on how data is handled, pending approval |

## Default narrative (from the reference case's approved outline)

1. Decision summary: problem, what is proposed, expected result, delivery, investment, what to align.
2. The problem and what will be built (input → what the product prepares → what the user receives).
3. Why an owned capability (build-vs-buy module).
4. What the first version covers and what stays out (scope-pedagogy module).
5. How it is delivered, validated and what it costs (stages, acceptance principle, investment table, recurring costs).
6. Conditions and responsibilities.
7. What we want to align to move forward.

Nothing before the investment section asks for a decision; nothing after it reopens explanation.

## Integrity risks

Checked by the Integrity auditor at the outline and draft audits: accidental warranties; acceptance ambiguity; hidden costs; ownership vagueness; open-ended support; future scope presented as included.

## Audience questions

None beyond the shared six until C-1 is implemented.

## Source checklist

For the source readiness triage, in addition to the generic contract. The sources must make recoverable:

- Commercial constants: price, payment, timeline, support allowance, cost responsibility.
- Scope boundaries, with representative inclusions and exclusions.
- Ownership and reuse positions (what the buyer will own, control, license; what the proposer retains).
- Client dependencies.
- Delivery stages and the acceptance principle for each.
- Which items are decided and which are open.
- Framing hypotheses to validate (from the brief), with what the sources say about each.
