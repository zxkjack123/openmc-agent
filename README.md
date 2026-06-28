# openmc-agent

> **Pure open-source AI agent for OpenMC Monte Carlo simulations.**
> Zero private dependencies. Community-first.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenMC](https://img.shields.io/badge/OpenMC-%E2%89%A5%200.14-blue)](https://docs.openmc.org/)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple)](https://modelcontextprotocol.io)
[![CI](https://github.com/zxkjack123/openmc-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/zxkjack123/openmc-agent/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-14%2F14%20passed-brightgreen)]()
[![Benchmarks](https://img.shields.io/badge/benchmarks-4%2F4%20implemented-brightgreen)]()

`openmc-agent` is a VS Code Copilot Chat agent that builds, validates, runs,
and post-processes [OpenMC](https://docs.openmc.org/) Monte Carlo simulations.
It uses the [openmc-validator-mcp](https://github.com/zxkjack123/openmc-validator-mcp)
server (14 deterministic validation tools) to catch model errors **before**
execution — eliminating the costly "submit → queue → fail → fix → resubmit" loop.

## Quick Start

### Prerequisites

```bash
# 1. Install OpenMC (conda-forge)
conda create -n openmc-env -c conda-forge python=3.11 openmc
conda activate openmc-env

# 2. Install openmc-validator
pip install openmc-validator

# 3. Set cross-sections path
export OPENMC_CROSS_SECTIONS=/path/to/endfb-viii.0/cross_sections.xml

# 4. (Optional) Install openmc-templates for pre-built materials/models
git clone https://github.com/zxkjack123/openmc-templates.git
export OPENMC_TEMPLATES_DIR=$(pwd)/openmc-templates
```

### Configure VS Code

Add to your `.mcp.json` or VS Code settings:

```json
{
  "servers": {
    "openmc-validator": {
      "command": "openmc-validator",
      "args": []
    }
  }
}
```

Then open this repo in VS Code and say: `@OpenMC Agent build a PWR pin-cell model`

## Architecture

```
┌──────────────────────────────────────────────────┐
│                  OpenMC Agent                     │
│  (openmc-agent.agent.md)                         │
│                                                   │
│  Workflow: A→B→C→D→E→F→G→H                       │
│                                                   │
│  A: Requirements    │ Parse user intent          │
│  B: Build           │ Construct OpenMC model     │
│  C: Validate + Fix  │ 14 openmc-validator checks │
│  D: Execute         │ local / SLURM backend      │
│  E: Post-process    │ Tally extraction + plots   │
│  F: Evaluate        │ Benchmark comparison       │
│  G: Audit           │ Physical plausibility      │
│  H: Deliver         │ Structured summary         │
│                                                   │
│  Tools: 6 core + 14 openmc-validator             │
│  Agents: Explore, Critical Thinking              │
│  Backends: local (default), slurm                │
│  Skills: benchmark-runner, input-repair          │
└──────────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌──────────────────┐
│ openmc-validator │  │ openmc-templates  │
│ (14 tools)       │  │ (materials/models)│
└─────────────────┘  └──────────────────┘
```

## Repository Structure

```
openmc-agent/
├── openmc-agent.agent.md    # Agent definition
├── CONSTITUTION.md          # Policy index
├── README.md                # This file
├── LICENSE                  # MIT
├── CHANGELOG.md
├── .opencode/               # opencode IDE config (agents, commands, skills)
├── instructions/
│   └── openmc-evaluation.instructions.md  # Evaluation feedback loop
├── skills/
│   ├── openmc-benchmark-runner/SKILL.md   # Benchmark execution
│   └── openmc-input-repair/SKILL.md       # Validation repair
├── backends/
│   ├── README.md            # Backend reference (local, slurm, scnet)
│   └── local_executor.py    # Local execution backend
├── benchmarks/
│   ├── README.md            # Benchmark catalog (4 implemented)
│   ├── criticality/godiva/  # GODIVA bare sphere (ICSBEP)
│   ├── criticality/pwr-pin-cell/  # PWR pin-cell (OECD/NEA)
│   ├── shielding/concrete-penetration/  # Concrete slab (ORNL)
│   └── fusion/liquid-breeder-blanket/   # LiPb breeder blanket
├── docs/
│   ├── architecture.md
│   ├── benchmark-protocol.md
│   └── evaluation-framework.md
├── tests/
│   ├── test_agent_contract.py    # 10 contract tests
│   └── test_e2e_godiva_pipeline.py  # 4 pipeline tests (1 slow)
├── .github/workflows/
│   └── ci.yml                # GitHub Actions CI
├── scripts/
│   └── check_tool_budget.py
└── memories/repo/
    └── workflow-patterns.md
```

## Benchmarks

| Benchmark | Category | Key Metric | Reference | Status |
|-----------|----------|-----------|-----------|--------|
| GODIVA | criticality | k_eff = 0.9992 ± 200 pcm | ICSBEP HEU-MET-FAST-001 | ✅ |
| PWR Pin Cell | criticality | k_eff ≈ 1.175 ± 500 pcm | OECD/NEA | ✅ |
| Concrete Penetration | shielding | flux attenuation ≈ 0.01 | ORNL | ✅ |
| Liquid Breeder Blanket | fusion | TBR ≈ 1.15 ± 10% | OpenMC examples | ✅ |

## Test Status

| Suite | Count | Status |
|-------|-------|--------|
| Contract | 10 | ✅ 10/10 pass |
| E2E Pipeline | 4 | ✅ 4/4 pass (1 slow) |
| Tool Budget | 1 | ✅ 20/25 |

```bash
# Run all non-slow tests
pytest tests/ -v -k "not slow"

# Run full suite (requires OpenMC + cross sections)
pytest tests/ -v
```

## Dependencies

| Dependency | Required? | Role |
|-----------|-----------|------|
| [openmc-validator-mcp](https://github.com/zxkjack123/openmc-validator-mcp) | **Yes** | 14 validation/cross-check/conversion/template tools |
| [openmc-templates](https://github.com/zxkjack123/openmc-templates) | Recommended | Pre-built materials and model templates |
| OpenMC ≥ 0.14 | For execution | Monte Carlo transport engine |
| ENDF/B-VIII.0 cross-sections | For execution | Nuclear data library |

**Optional pluggable KB** (NOT required, NOT in core tool list):

| Extension | Purpose |
|-----------|---------|
| [semantic-scholar-mcp](https://github.com/zxkjack123/semantic-scholar-mcp) | Literature search for benchmark references |
| [crawl4ai-mcp](https://github.com/zxkjack123/crawl4ai-mcp-server) | Web search for OpenMC docs/Q&A |
| [dify-knowledge-mcp](https://github.com/zxkjack123/dify-knowledge-mcp-server) | Custom knowledge base |

## Comparison: OpenMC Agent vs. Simulation Builder

| Feature | OpenMC Agent (here) | Simulation Builder (copilot-agents) |
|---------|---------------------|-------------------------------------|
| **Scope** | OpenMC only | OpenMC, MCNP, FISPACT-II, DAGMC, natf, tricys |
| **HPC submission** | SLURM script generation (manual submit) | Automatic via scnetresource-router |
| **KB integration** | Pluggable (none built-in) | Built-in dify-knowledge + session-memory |
| **Dependencies** | 100% open-source | Requires private MCP servers |
| **Target audience** | OpenMC community, collaborators | Internal ASIPP team |
| **License** | MIT | Private |

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
