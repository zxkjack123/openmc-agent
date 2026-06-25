# openmc-agent Project Snapshot

**Generated**: 2026-06-20
**Purpose**: Brownfield bootstrap for Plan Architect — avoid redundant repo exploration on every plan.

## Architecture

Pure open-source OpenMC AI agent for VS Code Copilot Chat. 8-stage pipeline (A→H).
Zero private dependencies. Community-first design.

## Key Modules

| Module | Path | Responsibility |
|--------|------|---------------|
| Agent Definition | `openmc-agent.agent.md` | 8-stage workflow, 20 tools, agent delegation |
| Constitution | `CONSTITUTION.md` | Policy index: quality gates, backend policy, open-source boundary |
| Evaluation Instructions | `instructions/openmc-evaluation.instructions.md` | Benchmark comparison protocol |
| Benchmark Runner Skill | `skills/openmc-benchmark-runner/SKILL.md` | Load benchmark → execute → compare → report |
| Input Repair Skill | `skills/openmc-input-repair/SKILL.md` | Parse validator errors → diagnose → fix (max 2 iterations) |
| Backend Contract | `backends/README.md` | BackendExecutor interface (prepare/run/cleanup) |
| Benchmark Catalog | `benchmarks/README.md` | 4 stubs (godiva, pwr-pin, iter-tbm, fusion-blanket) |
| Architecture Docs | `docs/architecture.md` | Component diagram, tool budget, quality gates |
| Evaluation Docs | `docs/evaluation-framework.md` | D1-D4 evaluation dimensions |
| Benchmark Protocol | `docs/benchmark-protocol.md` | YAML schema, pass/fail criteria |
| Contract Tests | `tests/test_agent_contract.py` | 10 tests — ALL PASSING |
| Budget Check Script | `scripts/check_tool_budget.py` | Tool count + blocklist check |

## Test Commands

```bash
pytest tests/test_agent_contract.py -v    # 10 contract tests
python scripts/check_tool_budget.py       # Tool budget verification
```

## CI

None yet (GitHub Actions not configured).

## Dependencies

- OpenMC ≥ 0.14 (0.15.4.dev available in environment)
- openmc-validator-mcp (MCP server, not Python importable; 14 tools via MCP)
- OPENMC_CROSS_SECTIONS: /home/gw/NucData/nndc_hdf5/cross_sections.xml (ENDF/B-VIII.0)
- YAML, pathlib (stdlib)
