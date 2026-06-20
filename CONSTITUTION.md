# openmc-agent Constitution

> Lightweight policy index — this is a pure open-source project.
> When two rules conflict, the lower-numbered section wins (1 > 2 > 3).

## 1. Quality Gates

- `openmc-agent.agent.md` Stage C — mandatory input validation (14 checks via openmc-validator).
- `openmc-agent.agent.md` Stage G — Pre-Delivery Audit (L2-Standard physical plausibility).
- `instructions/openmc-evaluation.instructions.md` — benchmark evaluation feedback loop.
- `skills/openmc-input-repair/SKILL.md` — auto-repair loop (max 2 iterations).

Validation failures are **blocking**: do NOT skip to execution with unresolved errors.

## 2. Backend Policy

| Backend | What it does | Requires |
|---------|-------------|----------|
| `local` (default) | Runs `openmc.run()` in-process | OpenMC installed + `OPENMC_CROSS_SECTIONS` set |
| `slurm` | Generates `submit.sh` script | None — user submits manually |
| `scnet` | NOT INCLUDED — see private copilot-agents overlay | N/A |

The SLURM backend applies resource safety margins: CPU +20%, wall time ×1.5, memory +30%.

## 3. Open-Source Boundary

- **Zero private dependencies**: No scnetresource-router, dify-knowledge, session-memory, plausibility-check, or de-ai-fier references.
- **Pluggable KB**: semantic-scholar, crawl4ai, and dify-knowledge may be configured by users but are never required.
- **Community-first design**: All tools are publicly available. The agent works standalone with just `pip install openmc openmc-validator`.

## 4. Model Construction Order

Always build OpenMC models in this order:
Materials → Geometry (Surfaces → Regions → Cells → Universes → Lattices) → Settings → Tallies

## 5. Tool Budget

- **Target**: ≤20 tools (6 core + 14 openmc-validator).
- **Hard cap**: 25 tools.
- Pluggable KB tools (semantic-scholar, crawl4ai, dify-knowledge) are NOT in the core tool list — users add them externally.

## Revision

- 2026-06-20 — initial draft for openmc-agent v0.1.0 open-source skeleton.
