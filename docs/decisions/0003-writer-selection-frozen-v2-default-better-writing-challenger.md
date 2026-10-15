# Frozen Writing V2 is the product-story writer; Better Writing is the challenger

Status: Accepted
Date: 2026-10-01

## Context
A preregistered experiment compared Writing V2 with Better Writing (an MIT-licensed upstream writing skill) used through a thin adapter. It closed with V2 roughly matching Better Writing. The plan's default consequence for that result was to adopt Better Writing with an adapter and archive V2. Blind preference had favoured V2 in both stages.

## Decision
Retain frozen Writing V2 as the current product-story writing capability. Develop Better Writing plus a thin grounded-artifact adapter as the maintained challenger. Replace V2 only when real-artifact evidence shows no meaningful loss of quality. No further bespoke V2 development (no v3). Better Writing stays an upstream dependency, not a fork.

## Consequences
- `writers/README.md` is the only registry. `product-story` defaults to `writing-v2` and `commercial-proposal` to `none`. The brief's `Writer` row overrides the default for one run. Registered files are pinned by SHA-256, and `scripts/resolve_writer.py` fails on any mismatch. A frozen writer is never edited or re-pinned. An improvement is a new writer with its own row.
- A writer reaches only the draft and draft-revise runs. Grounding, frame, outline and the auditors never read one (`SKILL.md` delegation line, checked by `scripts/writer_selftest.sh`).
- The challenger is not registered and not included in this distribution.
- Departing from the experiment plan's default consequence was the owner's deliberate call.

## Evidence (summary; the underlying records are not distributed)
- The two-stage comparison ran on one product-story fixture. Each stage had four blind readers, a keyed comprehension check and a preservation gate (passed by both arms). Comprehension answers matched the key on both arms. The preregistered criterion that V2 "clearly beats" Better Writing on reader effort was not met. All four blind readers in the final stage preferred V2.
- Reader rereads tracked reading order rather than arm, so the effort measure was weak in both stages.
- Strength: a small reader study on one artifact type.
