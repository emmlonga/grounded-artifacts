# Commercial-proposal case: lessons

The first reference case was an alignment-stage commercial proposal for a client, written from two governing source documents. It was produced before V0 existed, with a hand-written prompt, cross-model audits and a scripted DOCX build. This note keeps what the run taught and where each lesson lives in V0.

Generalized for publication: no client, people, commercial terms or figures, dates, language or industry.

**Evidence strength.** This is one engagement, and the counts below are approximate. The V0 mechanisms are design responses to this case (and to later product-story runs). They are not fixes measured against it.

## The record, in brief

| Item | Value |
|---|---|
| Sources | 2 governing documents (a commercial annex and a much longer implementation plan); 1 explicitly excluded |
| Brief | Embedded in a ~2,800-word prompt: artifact type, buyer persona, objective, several candidate framings, ownership taxonomy, required sections, output language, word ceiling |
| Grounding | 4 versions to freeze over 3 audit rounds, 2 more after (chain audit, owner changes); final size ~8,900 words, 2.2× its ceiling |
| Outline | 3 versions to freeze over 2 rounds, 2 more after |
| Draft | 4 versions to freeze; body grew from 1,600 to 2,060 words against an outline cap of 1,980 |
| Audits | 8 rounds, all cross-model, two lenses per round (completeness and cohesion; a non-technical buyer), plus one holistic chain audit and one promise-precision audit |
| Verdicts | APPROVE WITH TARGETED FIXES in every round after the first; no P0 after round 1 of any stage |
| Wrong findings | About 2 per round, rejected or adapted by the developer on source-fidelity grounds |
| Render | Scripted DOCX build, Word to PDF, page images, sentence diff. The build shrank the body to 10 pt to fit; the owner rebuilt it at 12 pt (~320 words/page) |
| After freeze | The owner changed 2 commercial terms, about 5 vocabulary choices and 1 editorial guardrail |
| Wall clock | ~24 h, including 2 usage-limit breaks and 1 context compaction |

## What worked, and where it lives in V0

| Lesson | V0 mechanism |
|---|---|
| Truth before narrative: a grounding written and audited before any outline | Step order in `SKILL.md`; `templates/grounding.md` |
| Claim classes with a definition of what each obliges; "preserving is not showing" kept the draft from becoming a list of disclaimers | Grounding §4 |
| A constants table: no number drifted until the owner changed one on purpose | Grounding §5; `scripts/compare.py` reads it |
| Candidate framings validated against the sources (SUPPORTED / WITH QUALIFICATION / UNSUPPORTED / CONFLICTING) | Grounding §3; brief field |
| Open items classified by where they get resolved, which let a short document stay short | Grounding §7; the commercial-proposal mode's venues |
| A non-widening precedence rule: a commercial simplification never widens a technical limit; used twice to reject audit suggestions | Grounding §1 conflict rule |
| An audience-facing anchor proved the thing could be explained simply before any narrative work | Grounding §2 |
| Two independent lenses that disagreed productively | Both auditors at every stage |
| "Decisions for owner" plus binding handoff rules with per-section word caps | Outline template; an owner gate opens only when that section is non-empty |
| Developer adjudication with source verification caught auditor errors every round | Revise instruction; `templates/adjudication.md` |
| Rendered-page inspection plus a text diff: both necessary, neither sufficient | `scripts/render.sh`; `templates/render-qa-checklist.md` |
| Files were the only state that survived interruptions | Every stage reads and writes files; fresh agents per run |

## What failed, the cause, and the V0 response

| Failure | Root cause | V0 response |
|---|---|---|
| Grounding grew to 2.2× its ceiling | Each audit added a control surface; one file served two readers | Size target per mode, reported once as an advisory reading (never a finding); history moved out of artifacts into adjudication files |
| The page budget was disconnected from typography; the renderer made content fit by shrinking type | No words-per-page calibration | Measured calibration line per profile; word caps per section; `wordcount.py`; body size fixed by the reference document; the rendered page count binds |
| The draft re-inflated through audits | Findings did not state their word cost; additions were free | `Words +/-` column in the finding schema; "name what is removed" rule |
| Persuasive auditor wording adopted with drift | No mandatory recheck against the source | Adjudication first; auditor wording verified against the grounding or the source; suggested wording non-binding |
| Per-artifact audits missed scattering across layers | Nobody read the chain as a whole | Chain questions folded into the draft audit (Audience lens) |
| The renderer and Render QA were the same agent; the owner found the defects | Self-review of the render | The renderer is a script; Render QA is a checklist applied to page images |
| Post-freeze owner edits were outside the process | No step for them | Owner-edit step with "Post-freeze changes" in the grounding and a departure report |
| Stage prompts rewritten by hand each time (3,000–6,000 words) | No reusable prompts | Three short agent files, one mode per run |
| The compare script had hard-coded tokens | Constants lived in prose | `compare.py` reads the grounding's constants and terminology tables |

## Cost lesson

The full process took about a day of orchestration for a five-page proposal. That was right for a commercial commitment and would be wrong for a three-page story. V0 keeps one audit round by default (a second only for an open P0 or P1) and opens the owner gates at grounding and outline only when there is a real decision. The product-story mode was built to test whether the method generalizes at a fraction of the cost.
