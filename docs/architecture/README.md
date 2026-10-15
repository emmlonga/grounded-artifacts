# Architecture

How the system is designed. These documents explain; they do not override the runtime files (`../../SKILL.md`, `agents/`, `modes/`, `templates/`, `writers/`, `scripts/`, `profiles/`).

| File | Role |
|---|---|
| `agent-instruction-standards.md` | Design standard for the agent files and the runbook. **Runtime dependency:** §5 and §5a (canonical finding schema, verdict rule, severity scale, shared audience questions) are read at runtime by `agents/grounding-integrity-auditor.md`, `agents/audience-auditor.md` and `agents/content-developer.md`, and cited by `templates/adjudication.md` and `SKILL.md`. Do not move or renumber those sections without updating those files |

This release documents the implemented V0 system only. Later designs (an automated workflow layer, a slide-deck branch) are not built and are not described here.
