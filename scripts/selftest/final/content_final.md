<!--
FREEZE HEADER - not rendered
Frozen: 2026-09-28 from draft.md v1 (pipeline self-test fixture)
-->
# Project Harbor: faster delivery-time estimates

*Render self-test for the V0 kit*

## The opportunity

At a mid-size logistics company, dispatchers re-quoted delivery times by hand for every delayed order. I saw that the delay was not in the data but in the handoff between two teams, and that fixing the handoff would matter more that quarter than a new model.

## What we built

We shipped a delivery-time estimate that dispatchers could trust without re-checking it.

- A shared status feed replaced the daily spreadsheet.
- Dispatchers saw one estimate, with the reason it changed.
- We ran a pilot of six weeks with two regional teams.

| Decision | Alternative rejected | Why |
|---|---|---|
| Fix the handoff first | Train a new model | The data was already good enough |
| Pilot with two teams | Launch everywhere | Setbacks stay small and visible |

## The outcome

Activation rose by 20% during the pilot, and manual re-quotes fell by about half. The main learning was to measure the handoff before touching the model.
