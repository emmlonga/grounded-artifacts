# Render QA — <artifact name>

<!-- Copy to final/render-qa.md. Run by the main session after scripts/render.sh, on every page image in
     final/pages/. Paste the render summary verbatim; do not re-derive it. -->

**Rendered:** <YYYY-MM-DD> · **Profile:** <profile> (minimum body <N> pt) · **Budget:** <N> pages
**render.sh summary:** <pdf / pages / compare / names lines, verbatim>
**Pages reviewed:** page-01.png … page-<NN>.png (all)

| # | Check | Result (PASS / FAIL / N/A) | Page and evidence | Defect class |
|---|---|---|---|---|
| 1 | Page count within budget | | | |
| 2 | Heading styles applied: title, section headings and subheads look like the profile; no body text styled as a heading or the reverse | | | |
| 3 | Body text at or above the profile minimum; no paragraph visibly smaller than the rest | | | |
| 4 | No orphan headings (a heading at the foot of a page with its text on the next) | | | |
| 5 | No split small tables; a table that must split repeats its header row | | | |
| 6 | Density: no page crammed or mostly empty without reason; spacing consistent | | | |
| 7 | Headers and footers as the profile defines; page numbers correct | | | |
| 8 | Lists and numbering intact (no restarts, no stray bullets) | | | |
| 9 | No leftover markup: asterisks, pipes, `#`, HTML comments, placeholders, TODO | | | |
| 10 | compare.py: no missing sentences; constants and forbidden phrasing PASS | | | |
| 11 | check_names.py PASS (SKIPPED acceptable only when the brief requires no anonymization) | | | |
| 12 | No orphaned fragment at a page break: one or two words stranded on either side of the break (e.g. "My / reason:"), a term separated from its gloss, or a figure from its qualifier. Normal continuation of a sentence across pages is not a defect. Class: RENDERING DEFECT, P2; remedy is local (a paragraph-level keep-together set by the owner at step 19, or a one-sentence edit routed as a content defect), not a profile change | | | |

**Defect classes.** CONTENT DEFECT: the words do not fit or do not say the right thing → write it to `audits/freeze-gate-findings.md` in the canonical finding table (standard §5) with a Repair locus; the developer adjudicates it in the adjudication of its locus and the walk-forward rule applies (SKILL.md step 18). RENDERING DEFECT: the words are right but the layout is wrong → fix the profile's reference document or the build, re-render. Never fix a content defect by reducing type size, margins or spacing.

**Result:** PASS / FAIL — <defects, one line each, with class>
