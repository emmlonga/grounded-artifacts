# Mode: product-story

A first-person written story of a product the author actually built, read by interviewers who judge it against explicit criteria and then use it as the basis for a presentation and a deep-dive conversation. Reference case: a written product story for a product-manager hiring process (2–3 pages, max 3, English).

## Defaults

| Setting | Default |
|---|---|
| Render profile | plain |
| Budget | max 3 pages, 2–3 preferred. Planning budget ~1,150–1,200 words at the plain calibration (~420 words/page), allocated to section caps as a planning aid; fit guardrail = calibration × pages (1,260 at 12 pt) is the reading above which a preview is likely to fail; the rendered page maximum and readable density are binding. Every word-count reading is advisory and never a finding once a preview passes |
| Grounding size | advisory readings from `wordcount.py`, per section: claim classes (§4) about 1,200 words; whole file about 2,500 (tables included). Reported once by the Integrity lens; never repaired by compressing claim text |
| Editorial gates | **required** (story frame gate and first-draft read): a three-page story from a rich source almost always has more than one plausible story. The owner may set "not required" in the brief for a thin source |
| Material map | on in the readiness file when the source is much richer than the artifact or the triage sees several plausible stories |
| external_audit | anonymized-only |
| Integrity risks | on (this section) |
| Audience questions | on (this section) |
| Authenticity check | **on** (Audience auditor, outline and draft audits) |

## MUST INCLUDE: the five required elements, as coverage obligations

Each element is an obligation the artifact must demonstrably meet, not a checklist of sub-items. The grounding records the obligation at pass A; the story frame and the outline decide which grounded evidence meets it; one demonstrable answer per element is enough.

1. **Opportunity:** the core user problem or business opportunity, and why it was the right problem for the business and users at that time.
2. **Vision and strategy:** the product vision, the strategy to get there, the key trade-offs, and the link to the broader business strategy.
3. **How — collaboration and execution:** the core team, how it worked together to define, build, validate or launch, and the author's own role. Its demonstrable answer is at least one concrete working mechanic from the grounding that shows how the team actually operated (planning or refinement, disagreement resolution, testing or validation, delivery cadence, rollout observation, blocker handling, or another grounded mechanic). A mechanic is a practice the reader can picture: what the team did, when or how often, and what it was for. Naming the roles, stating ownership boundaries, or attaching a participle to a role ("refining with the developers") does not meet it; one mechanic does, and more are the writer's choice, never a requirement.
4. **Stakeholders:** the key stakeholders outside the core team, and how the author aligned them, managed expectations, and communicated progress and setbacks.
5. **Outcome and reflection:** the results, how success was measured, the biggest learnings, and what the author would do differently today.

## Claim rules

- **MUST PRESERVE:** the truthfulness of the story and the author's actual role. Owned versus influenced stays distinct; "we" is never upgraded to "I", nor "I" diluted to "we" where the author decided.
- **MUST NOT SAY:** any real name in the anonymization map; any absolute metric the owner marked sensitive (use the approved proportional or directional rendering); any outcome without evidence in the sources.
- **Confidentiality:** the workflow does not interpret NDAs. It enforces the owner's anonymization and confidentiality instructions as recorded in the grounding; `scripts/check_names.py` enforces the map on every draft, the final and the rendered text.
- **Evaluation criteria** (from the brief; in the reference case: product sense, product execution, narrative clarity): the grounding maps each criterion to evidence at pass A, the frame's critical decisions name what each demonstrates, and the audience audit checks each is demonstrably answered, not just mentioned.

## Writing rules (authenticity)

1. First person; the author's decisions read as decisions. The rejected alternative and the cost appear where they inform the judgment the reader is assessing (the frame's critical decisions), not for every decision the grounding records.
2. Every section carries at least one specific, verifiable detail from the grounding: a number in its approved rendering, a moment, a concrete artifact, a named (anonymized) team or partner.
3. Judgment calls and setbacks appear as they happened, including what the author got wrong. Hindsight is marked as hindsight by wording and placement, never by a label.
4. No generic PM phrasing: no "drove alignment", "leveraged", "stakeholder buy-in" or "data-driven" without who, what and how.
5. Selective over complete: grounded evidence is permission to use, not an obligation to render. Evidence appears where it explains, proves or makes a proposition concrete; what does no reader-facing work stays out. A label, pointer, count or stated trade-off is kept when it helps the reader orient or follow the argument, and dropped when it only exposes a planning field. A guardrail (a MUST PRESERVE or MUST NOT SAY row, an accepted rendering, a permitted alternative) bounds what the prose may say; it is not content: it is shown only where its fact does reader-facing work, once, in plain words rather than in the row's wording.

## Integrity risks

Checked by the Integrity auditor at the outline and draft audits:

1. Team action rewritten as personal ownership.
2. Retrospective learning presented as contemporaneous rationale.
3. Causal attribution stronger than the evidence supports.
4. A sensitive or approximate metric rendered more precisely than the owner allowed.
5. The story depending on unresolved `[OPEN]` / `[INFERRED]` material.
6. A source aim or direction of change rendered as an achieved state or a property of the situation.

## Audience questions

Asked by the Audience auditor after the shared six (standard §5a) and the chain questions:

1. Is the author's own judgment visible in each required element?
2. Does the opening give the outcome?
3. Would the interviewer know what to probe in each section?
4. Does any decision carry a rejected alternative or a cost only because a rule asked for it, and does any label, pointer or count reach the reader without helping the reader orient or follow the argument?

## Reserve as deep-dive backlog

The reserve holds what the interviewers are likely to probe in the deep dive: the frame's demoted subplots, alternatives considered, numbers behind directional claims (only those the owner allows), team conflicts, what was cut. The grounding's open items hold the questions the story invites that the sources do not answer; the outline lists the reserve items each section invites questions about.

## AI usage note

At the owner-edit step, write `notes/ai-usage.md` from `templates/ai-usage-note.md`. The reference case asked the author to explain how AI was used.

## Default narrative

Case order, with the outcome previewed in the opening paragraph. The story frame decides emphasis and load within this order; it does not change the order without an outline closed decision.

1. Opportunity and why then (the opening paragraph orients the reader on who the author was, where, and what changed, and previews the outcome in one sentence).
2. Vision, strategy and trade-offs.
3. How the team built it, and the author's role.
4. Stakeholders, alignment and setbacks.
5. Outcomes, measurement, learnings, and what the author would do differently.

Optional modules (activated by the frame or the outline): a small quantitative results table (only approved renderings); a one-line timeline strip.

## Source checklist

For the source readiness triage, in addition to the generic contract. The sources must make recoverable:

- Material for each of the five required elements: (1) the opportunity and why it was the right problem then; (2) the vision, strategy, key trade-offs and link to the broader business strategy; (3) the core team, how it worked, and the author's role; (4) the stakeholders outside the team and how they were aligned, kept informed of progress and setbacks; (5) the results, how success was measured, the learnings, and what the author would do differently.
- The author's actual role and personal decisions, distinct from the team's, including who identified the opportunity and who shaped the vision (Product Sense is judged on the author's own judgment).
- Evidence of the outcome (directional is acceptable if labelled).
- Setbacks, and what changed because of them.
- Learnings, and what the author would do differently.
- Anonymization choices for every real name (company, product, people, partners, code names) and, for each sensitive metric, whether it may appear as absolute, proportional or directional.
