# Documentation map

**Runtime authority is outside `docs/`.** The active workflow is defined only by `../SKILL.md`, `../agents/`, `../modes/`, `../templates/`, `../writers/`, `../scripts/` and `../profiles/`. Documents here explain the system and record why durable choices were made. They never override a runtime file: where they disagree, the runtime file governs.

One documented exception: the auditors, the developer, `../templates/adjudication.md` and `../SKILL.md` read the canonical finding schema (§5) and the shared audience questions (§5a) of `architecture/agent-instruction-standards.md` at runtime. Those sections are a runtime dependency that lives under `docs/` (`decisions/0005-docs-knowledge-model-and-runtime-authority.md`).

| Folder | Purpose |
|---|---|
| `architecture/` | How the system is designed: the standard for the agent files and the runbook |
| `decisions/` | Accepted choices currently in force, as short records with a public-safe summary of their evidence (index in `decisions/README.md`) |
| `case-studies/` | Generalized lessons from real applications of the workflow |

The maintainer also keeps validation records (experiments, regression and control runs, replays, reader studies) and an evolution backlog (open hypotheses and candidate improvements). These are built on client and personal material and are not part of this distribution. Where a decision depends on them, the decision record summarizes the evidence.
