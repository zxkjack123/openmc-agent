# Contributing to openmc-agent

Thanks for your interest in contributing! This project aims to build a pure open-source OpenMC AI agent for the VS Code Copilot Chat ecosystem.

## Getting Started

1. Clone this repo alongside the required dependencies:
   ```bash
   git clone https://github.com/your-org/openmc-agent.git
   git clone https://github.com/openmc-dev/openmc.git
   git clone https://github.com/openmc-dev/openmc-templates.git
   git clone https://github.com/your-org/openmc-validator-mcp.git
   ```

2. Open `openmc-agent.code-workspace` in VS Code.

3. Run the contract tests:
   ```bash
   cd openmc-agent
   pip install pyyaml pytest
   pytest tests/test_agent_contract.py -v
   ```

## Areas to Contribute

| Area | Description | Priority |
|------|-------------|----------|
| **Benchmarks** | Add real `model.py` + `benchmark.yaml` to `benchmarks/` | High |
| **openmc-input-repair** | Extend the repair table in the SKILL.md with more error→fix mappings | Medium |
| **Backend executors** | Implement `LocalExecutor` and `SlurmExecutor` in `backends/` | High |
| **E2E tests** | Integration tests with real OpenMC execution | Medium |
| **Pluggable KB** | Documentation/skill for optional knowledge-base tools | Low |

## Guidelines

- **No private dependencies**: This is pure open-source. Do NOT add references to scnetresource-router, dify-knowledge, session-memory, plausibility-check, de-ai-fier, formatforge, tikz-writer, citation-lint, manuscript-lint, factcheck-gate, image-worker, fusion-terms, or fusion-materials.
- **Tool budget**: Core tool list ≤ 20, hard cap ≤ 25. Run `python scripts/check_tool_budget.py` before committing.
- **Agent definition**: `openmc-agent.agent.md` uses YAML frontmatter. Run `pytest tests/test_agent_contract.py -v` after changes.
- **Skills**: Follow the SKILL.md format (see existing skills for template).
- **License**: All contributions under MIT.

## Questions?

Open an issue or start a discussion in the repository.
