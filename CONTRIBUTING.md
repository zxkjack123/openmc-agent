# Contributing to openmc-agent

Thanks for your interest in contributing! This project aims to build a pure open-source OpenMC AI agent for the VS Code Copilot Chat ecosystem.

## Getting Started

1. Clone this repo alongside the required dependencies:
   ```bash
   git clone https://github.com/zxkjack123/openmc-agent.git
   git clone https://github.com/openmc-dev/openmc.git
   git clone https://github.com/openmc-dev/openmc-templates.git
   git clone https://github.com/zxkjack123/openmc-validator-mcp.git
   ```

2. Open `openmc-agent.code-workspace` in VS Code.

3. Run the tests:
   ```bash
   cd openmc-agent
   pip install pyyaml pytest h5py
   pytest tests/ -v -k "not slow"   # contract + fast E2E
   ```

4. Run the full suite (requires OpenMC installed + cross sections):
   ```bash
   export OPENMC_CROSS_SECTIONS=/path/to/cross_sections.xml
   pytest tests/ -v                  # all 14 tests
   ```

## Areas to Contribute

| Area | Description | Priority |
|------|-------------|----------|
| **SLURM backend** | Implement `SlurmExecutor` in `backends/` per the backend contract | High |
| **Benchmarks** | Add new `model.py` + `benchmark.yaml` to `benchmarks/` | Medium |
| **openmc-input-repair** | Extend the repair table in the SKILL.md with more error→fix mappings | Medium |
| **E2E tests** | Add integration tests for new benchmarks | Medium |
| **Pluggable KB** | Documentation/skill for optional knowledge-base tools | Low |

## Current Benchmarks

| Benchmark | Category | Key Metric | Status |
|-----------|----------|-----------|--------|
| GODIVA | criticality | k_eff | ✅ |
| PWR Pin Cell | criticality | k_eff | ✅ |
| Concrete Penetration | shielding | flux attenuation | ✅ |
| Liquid Breeder Blanket | fusion | TBR | ✅ |

New benchmarks should follow `benchmarks/<category>/<name>/` with `benchmark.yaml`, `model.py`, and `README.md`.

## Guidelines

- **No private dependencies**: This is pure open-source. Do NOT add references to scnetresource-router, dify-knowledge, session-memory, plausibility-check, de-ai-fier, formatforge, tikz-writer, citation-lint, manuscript-lint, factcheck-gate, image-worker, fusion-terms, or fusion-materials.
- **Tool budget**: Core tool list ≤ 20, hard cap ≤ 25. Run `python scripts/check_tool_budget.py` before committing.
- **Agent definition**: `openmc-agent.agent.md` uses YAML frontmatter. Run `pytest tests/test_agent_contract.py -v` after changes.
- **Skills**: Follow the SKILL.md format (see existing skills for template).
- **License**: All contributions under MIT.

## Questions?

Open an issue or start a discussion in the repository.
