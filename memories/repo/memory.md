# openmc-agent Memory

## Project Context

- **Type**: Pure open-source VS Code Copilot Chat agent
- **Target**: OpenMC Monte Carlo simulation community
- **Core dependency**: openmc-validator-mcp (14 tools)
- **No private dependencies**: scnetresource-router, dify-knowledge, session-memory, plausibility-check, de-ai-fier are NOT referenced
- **Two-system architecture**: openmc-agent (open-source) + copilot-agents/Simulation Builder (private ASIPP)

## Conventions

- Agent definition: `openmc-agent.agent.md` (YAML frontmatter + markdown workflow)
- Instructions: `instructions/*.instructions.md`
- Skills: `skills/*/SKILL.md`
- Backends: `backends/README.md`
- Benchmarks: `benchmarks/<category>/<name>/`

## Key Decisions

1. Pure open-source — no private MCP servers referenced (2026-06-20)
2. SLURM generates scripts but never auto-submits (2026-06-20)
3. Pluggable KB — semantic-scholar, crawl4ai, dify-knowledge in README but not in core tool list (2026-06-20)
4. Tool budget: 20 core tools, 25 hard cap (2026-06-20)

## Known Gaps

- Benchmark stubs need real model.py + benchmark.yaml filled in
- No E2E integration test (requires real OpenMC + cross-sections)
- Local backend not yet tested with real OpenMC execution
