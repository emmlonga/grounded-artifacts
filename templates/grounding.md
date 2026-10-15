<!--
Grounding template. Copy to <project>/grounding.md; keep the section order.
Keep these table headers: scripts read the Constants table ("Accepted renderings", "Stale renderings"),
the Anonymization map ("Real", "Anonymized rendering") and the Terminology table ("Forbidden phrasing")
by their header row. Separate several renderings or variants in one cell with ";".
Two passes, one file. Pass A (grounding mode) establishes truth and authority: every claim row with its source,
ownership and qualifiers; constants; the map; terminology; open items; and only the classes that are not editorial
(CLAIM, MUST INCLUDE, MUST PRESERVE, MUST NOT SAY). Pass B (frame mode, after the story frame is decided) turns each
CLAIM into MUST COMMUNICATE, MAY SAY or RESERVE against the frame. Nothing is MUST COMMUNICATE before the frame exists.
Size: the mode file gives advisory readings per section from scripts/wordcount.py. Sufficiency comes first: pass A holds
enough supported claims to satisfy every MUST INCLUDE obligation, to answer every evaluation criterion and to test
every candidate framing. MUST INCLUDE obligations are §4 rows citing the mode or the brief, excluded from that count; criteria and framings are
mappings in §3, not rows; frame beats do not exist yet and later point at existing claims. A reading over the
advisory ceiling is reported once, never repaired by compressing claim text; compression of claim text is what loses
qualifiers, and any such change is re-read against the source (SKILL.md step 5).
Current truth only: no changelog here; reasons for changes live in audits/*-adjudication.md.
Language: claim text, accepted and stale renderings, forbidden phrasing and audience terms are written in the
artifact's language; everything else in the working language.
-->
# Grounding — <artifact name>

**Version:** v1 · **Date:** <YYYY-MM-DD> · **Mode:** <mode> · **Brief:** approved <YYYY-MM-DD> · **Readiness:** <verdict>, audits/source-readiness.md · **Classification:** pass A (editorial classes pending the story frame) | pass B against story-frame.md v<N>

## 1. Sources and precedence

| ID | Source | Version / date | Governs | Precedence | Read | Excluded or not read |
|---|---|---|---|---|---|---|
| S1 | | | | 1 | | |

**Conflict rule:** <which source governs which concern; a simplification in one source never widens a limit set by another>.
**Source status:** <owner-reviewed / ready for grounding / authoritative documents>. Material still marked `[OPEN]`, `[INFERRED]`, `[ESTIMATE]` or `[CONFLICT]` appears below only as an open item, a MUST NOT SAY row or reserve, never as a stated claim.

## 2. Story frame

<!-- Pass A: "Pending: story-frame.md is written after this pass is audited." Pass B: the reference line below, with
     the selected thesis quoted once so a reader of this file knows what the classes serve. The frame is the editorial
     authority; this file is the factual authority. Neither restates the other. -->

**Frame:** story-frame.md v<N> · owner decision <APPROVED / HYBRID / NOT REQUIRED>, <YYYY-MM-DD>
**Selected thesis:** <quoted from the frame>

## 3. Objective and evaluation criteria

**Objective:** <one sentence, from the brief>

| Criterion (from the brief) | Evidence that answers it | Claim or source |
|---|---|---|

**Candidate framings** (from the brief; validated at pass A so the frame can draw on them):

| Framing | Verdict | What the sources support | Source |
|---|---|---|---|

<!-- Verdicts: SUPPORTED / SUPPORTED WITH QUALIFICATION / UNSUPPORTED / CONFLICTING. -->

## 4. Claim classes

Pass A classes (factual and mandatory):

- **CLAIM**: supported by the cited source; its editorial class is assigned at pass B.
- **MUST INCLUDE**: an element the mode or the brief requires to be present. It records the obligation, not the evidence that could satisfy it ("the artifact must demonstrate stakeholder alignment", not the list of stakeholders and interactions); the frame and the outline decide which claims satisfy it. Where the requirement is a specific value (a commercial constant), the row names that value.
- **MUST PRESERVE**: a truth, qualifier or boundary that no sentence may contradict or erase. It need not be shown: preserving is not showing.
- **MUST NOT SAY**: a claim, implication or detail the artifact must not contain, with the reason and the permitted alternative.

Pass B classes (editorial, against the story frame):

- **MUST COMMUNICATE · beat n**: omitting it would break the selected thesis or an external requirement. Cites its frame beat. "Important in the source" is never a reason.
- **MAY SAY · high | low**: supported and relevant; the outline and the writer use it where it explains, proves or makes a proposition concrete, and nowhere else. High: the frame's critical decisions and closing evidence draw on it. Low: deep-dive quality detail.
- **RESERVE · <venue>**: supported, deliberately out of the main artifact (a demoted subplot or an owner-choice promotion declined), with its venue. The row keeps its ID.

<!-- MUST NOT SAY rows are derived from the brief's owner guardrails and from every point where one source is more
     generous than the governing one; each row names the permitted alternative. A pass-B class change after the frame
     gate is recorded as a row in the stage adjudication with its reason; it never happens silently. -->

| ID | Class | Claim | Source |
|---|---|---|---|
| C1 | CLAIM | | S1 §… |

## 5. Constants

<!-- A qualified constant (approximate, conditional, "up to") carries its qualifier in every accepted rendering and
     lists the bare form as a stale rendering. -->

Every number, name, date and fixed phrase the artifact may use. The artifact uses only accepted renderings; stale renderings must appear nowhere. For a sensitive metric, Value holds the approved proportional or directional form; a real absolute figure the owner flags goes in the anonymization map instead.

| ID | Value | Accepted renderings | Stale renderings | Source |
|---|---|---|---|---|
| K1 | | | | |

<!-- CONFIDENTIAL:START anonymization map. Never paste this block into an external model. -->
### Anonymization map

Owner-supplied instructions only. `scripts/check_names.py` fails on any variant in the Real column.

| ID | Real (never in artifact) | Anonymized rendering | Owner instruction |
|---|---|---|---|
| N1 | | | |
<!-- CONFIDENTIAL:END -->

## 6. Terminology

<!-- An audience term defines a term; it never asserts a state, direction or outcome. "Lead time → days from order to
     delivery" defines; "Lead time → the short delivery window customers get" asserts a state the source may only have
     named as an aim. A tracking term this file uses for its own bookkeeping (a label for a diagnosis, a phase, a
     trade-off) gets a row whose Forbidden phrasing is the label itself: the concept reaches the reader, the label never does. -->

| Internal term | Audience term | Forbidden phrasing | Note |
|---|---|---|---|

## 7. Open items

<!-- Includes the questions the story will invite that the sources do not answer (presenter preparation, Q&A). -->

| ID | Open item | What is known | Resolved where | How the artifact treats it |
|---|---|---|---|---|
| O1 | | | | |

## 8. Reserve

Grounded content deliberately kept out of the artifact, kept for an appendix, Q&A or a later artifact.

<!-- Pass A: only material a rule, the brief or the owner excludes. Reserve for space is a pass-B and outline decision:
     a claim row demoted at pass B keeps its ID and reads RESERVE · <venue> in §4; this section holds material that
     never had a claim row. -->

| ID | Content | Why it is out | Use | Source |
|---|---|---|---|---|
| R1 | | | | |

## 9. Editorial rules

<!-- At most 10. Derived writing guidance, not source facts. A rule preserves chronology, attachment and the line
     between at-the-time reasoning and hindsight through the order and wording of claims; it never prescribes a
     reader-facing signpost, pointer, label or count, and never records an audit finding as a rule. -->

1.

## 10. Decisions for owner

<!-- Real decisions only: a fact, an ownership boundary or a conflict the owner must settle. Editorial choices
     (what to promote, what to demote) go to the story frame's owner-choice promotions, not here. Leave the table
     empty when there is nothing to decide: an empty section means no owner gate. -->

| # | Decision | Options | Default if unanswered | Why it matters |
|---|---|---|---|---|

<!-- Step 19 only: add "## Post-freeze changes" (date | what changed | why | constant, MUST item or guardrail touched | source now stale?) when an owner edit touches a constant, a MUST item or a guardrail. -->
