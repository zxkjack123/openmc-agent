# Architecture

> OpenMC Agent architecture and design decisions.

## Overview

`openmc-agent` is a VS Code Copilot Chat agent specialized in OpenMC Monte Carlo simulations.
It follows an 8-stage pipeline (A→H) with a strict quality gate at each stage boundary.

## Design Principles

1. **Pure open-source**: Zero private dependencies. Works with only `pip install openmc openmc-validator`.
2. **Deterministic validation first**: 14 openmc-validator checks run before any execution.
3. **Pluggable backends**: Local and SLURM built-in; private HPC overlay possible but not included.
4. **Evaluation-driven**: Every simulation is compared against benchmarks (Stage F).
5. **Auto-repair with limits**: Input validation errors trigger auto-fix (max 2 iterations), then escalation.

## Component Diagram

```
openmc-agent.agent.md (agent definition)
│
├── instructions/
│   └── openmc-evaluation.instructions.md
│       └── Calls: skills/openmc-benchmark-runner/SKILL.md
│
├── skills/
│   ├── openmc-benchmark-runner/SKILL.md
│   └── openmc-input-repair/SKILL.md
│
├── backends/
│   └── README.md (backend contract)
│
├── benchmarks/
│   └── */ (benchmark definitions)
│
├── docs/ (this directory)
│
├── tests/
│   └── test_agent_contract.py
│
└── scripts/
    └── check_tool_budget.py
```

## Tool Budget

| Category | Tools | Count |
|----------|-------|-------|
| Core | read, edit, execute, search, todo, agent | 6 |
| Validator | validate_materials, validate_geometry, validate_settings, validate_tallies, validate_model | 5 |
| Cross-check | check_cross_section_library, check_energy_filter_coverage, check_tally_filter_consistency | 3 |
| Converter | convert_spectrum_openmc_to_fispact, extract_tally_summary | 2 |
| Template | list_templates, get_template, list_materials, get_material | 4 |
| **Total** | | **20** |

Hard cap: 25. Current: 20. Budget margin: 5 slots.

## Agent Delegation

| Sub-agent | Delegated In | Purpose |
|-----------|-------------|---------|
| Explore | Stage A, Stage E | Codebase exploration, file search |
| Critical Thinking | Stage A (optional), Stage C (CT review) | Assumption validation, methodology review |

## Quality Gates

| Gate | Stage | Type | Blocking? |
|------|-------|------|-----------|
| Input validation | C | Deterministic (14 validators) | Yes |
| Auto-repair limit | C | Iteration cap (2) | Yes |
| Benchmark evaluation | F | Statistical (C/E, deviation) | Conditional |
| Pre-delivery audit | G | Physical plausibility (L2) | Yes |

## Backend Contract

See `backends/README.md` for the full backend interface specification.

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-20 | Pure open-source, no private deps | Community-first release; private HPC tools live in copilot-agents |
| 2026-06-20 | Two-system architecture | OpenMC Agent (open-source) + Simulation Builder (private) serve different audiences |
| 2026-06-20 | SLURM script generation, not submission | Avoids dependency on private scnetresource-router |
| 2026-06-20 | Pluggable KB (none built-in) | Keeps agent lightweight; users add KB tools externally |
