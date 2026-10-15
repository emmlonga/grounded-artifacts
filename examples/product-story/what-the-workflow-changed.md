# What the workflow changed

This example is a workflow run on a **synthetic test fixture**. The planning document, the owner and the owner's answers were written to test the workflow, and no real person or company is described. For publication, the fictional setting was generalized: no country, and placeholder bank and partner names. The workflow's behavior below is as the run recorded it.

**The source was built with traps.** An AI planning session drafted it, and the owner had not reviewed it. It includes an unsourced "retention up 35%", an inferred board goal, an unmarked "legal and marketing were aligned throughout", a "5% holdout" that contradicts the pilot description, and no record of who found the problem or who set the vision. A fluent writer would turn every one of them into a confident sentence.

The thread through every stage below is **ownership**. A product story is judged on the author's own judgment, so "I" where the source supports only "we", "the team" or "I recommended" is a false claim, however natural it sounds.

## 1. Source readiness: stop before inventing

The readiness check returned **BLOCKED**, for three reasons: who identified the opportunity and set the vision was unknown; an unmarked "35%" conflicted with the owner's own line that the exact number was unknown; and the plan was not owner-reviewed, so its unmarked lines were not usable. It asked six questions, each with what the artifact would say if the answer was unavailable. The owner's answers:

| Question | Owner's answer | What it changed |
|---|---|---|
| Who found the problem and set the vision? | The research team surfaced it; the head of product set the vision. Mine: the rewards-tier recommendation, the PRD, the pilot design, the pause, the CFO reporting | The story credits the team and the head of product. "I found the problem" and "my vision" became must-not-say rows |
| Who cut the rewards tier? | I recommended it; the steering committee approved | "I recommended…; the committee approved", never "I cut" |
| Is "35%" supported? | No, it was the planning agent's estimate. Withdraw it | Retention is stated as directional, with no figure |
| Was "primary bank" the strategic goal? | Unknown; do not use | The strategy link runs only through deposits leaving |
| Was marketing involved? | No; withdraw the line | Only "legal and compliance were consulted weekly" survives |
| Were the trade-off reasons given at the time? | Unknown; accept the fallback | The decisions are stated without claiming the reasons were argued then; "one quarter" stays an aim |

After the answers, the verdict became **READY WITH GAPS**. Every gap is carried as an open item, a must-not-say row or a stated limitation, never filled in. One more conflict surfaced: the plan's "5% holdout" contradicted the answer that the 5% *received* the feature. The later owner statement governs, and "holdout" became a forbidden rendering.

## 2. Grounding: the ownership line, written down

`grounding-excerpt.md` holds the result. The rows that did the most work:

- **C16 MUST PRESERVE**, the ownership boundary: problem-finding belongs to the research team and the vision to the head of product. The author's own actions are listed one by one. Running the pilot and fixing the bug stay "we"; the pause and the customer letter are "I".
- **Must not say, each with its permitted alternative:** any outcome figure; company-wide impact; "primary bank"; "marketing was aligned"; "I found the problem"; "shipped in one quarter"; "holdout".
- **Constants with stale renderings:** "35%", "5% holdout" and "shipped in one quarter" are listed as stale, so `scripts/compare.py` fails a draft that uses them.
- **Anonymization map:** the bank, the code name, the partner and three absolute customer counts are replaced. `scripts/check_names.py` fails any draft, rendered text or edited DOCX that contains a real name.

## 3. Audits: the same error, caught at three layers

Both auditors ran at each stage. The developer adjudicated every finding against the grounding before editing.

| Stage | Finding | Fix |
|---|---|---|
| Grounding (P1) | The first-person rule covered running the pilot and the bug fix, which the source states as "we" | The first-person scope was narrowed clause by clause |
| Grounding (P1) | The audience anchor dropped "with the data analyst" from the pilot design | Qualifier restored |
| Grounding (P1) | The criteria mapping credited the author's product sense with evidence that belonged to others | Mapping corrected, and the mismatch with the brief's objective ("found the right problem") recorded as a decision for the owner |
| Outline (P1) | A section title read "I cut the rewards tier" | "I recommended launching without the rewards tier to aim to ship in one quarter" |
| Outline (P1) | The governing thought said the author's actions "let" the outcome happen, a causal claim the comparison does not support | Causal link removed; outcome stated as a comparison |
| Outline (P1) | Legal and compliance consultation was rendered as the author's action | Separate clause with no actor |
| Draft (P1) | The draft never said the pilot was randomly assigned, so the only outcome evidence looked open to selection bias | "Pilot customers, the 5% who received the feature, were assigned at random." |
| Draft (P2) | A heading, "the trade-offs I made", credited the author with the engineering lead's decision | "Vision, strategy and the trade-offs" |
| Draft (P2) | A scope sentence about pilot customers also covered the fee-product observation, whose population is unknown | The scope now names the retention and deposit results only |

**Not adopted:** an auditor suggested explaining the missing figures with "I can no longer access the dashboards". The grounding holds that only as background, not as a claim the story may make. The developer kept "(directional; the exact figure is unavailable)" and raised it as a decision for the owner.

## 4. Writing and render

The draft was written with **Writing V2**, the frozen default writer for product stories (`../../writers/README.md`), from the audited grounding and outline. Two audit rounds followed. The final round returned APPROVE (Integrity) and APPROVE WITH TARGETED FIXES (Audience). It renders to 2 pages with the `plain` profile. `scripts/render.sh` run with this grounding passes every check: all nine constants appear only in accepted renderings, no real-name variant from the map appears, and no sentence is lost in rendering. Read `final-artifact.md` against `source-input.md` to see the difference:

- every outcome sentence says "compared with the rest of the base" and "directional";
- "I" appears only where the grounding allows it;
- the setback is told with the author's actual actions (pause, customer letter) and the team's (the fix);
- no customer counts, names or figures the owner withheld appear;
- the hindsight lessons are marked as hindsight ("Looking back").

## What this example does not show

- **The story frame.** The run predates it. Today a story frame and an owner frame gate sit between grounding and outline, and the claim classes above would be set against the frame (pass B).
- **A real owner or real readers.** The owner's answers were written for the test, and the auditors are AI agents. The example shows how the workflow handles unsupported claims. It is not evidence about how human readers respond.
