# Changelog

All notable changes to openmc-agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-06-28

### Added
- PWR pin-cell benchmark (criticality): UO2 fuel, Zircaloy cladding, H2O moderator.
- Concrete penetration benchmark (shielding): 2 MeV source, 60 cm slab, flux attenuation.
- Liquid breeder blanket benchmark (fusion): Li17Pb83, 14.1 MeV D-T source, TBR tally.
- `.opencode/` project config: agents (openmc-build, openmc-explore), commands (validate, run, benchmark), skill (openmc-input-repair).
- GitHub Actions CI: contract tests (14) + tool budget check on push/PR to main.

### Fixed
- E2E test now uses `openmc.run()` API instead of `subprocess(["openmc"])` to avoid libdagmc.so dependency.
- GODIVA E2E test: all 14 tests pass (13 non-slow + 1 slow).

### Changed
- Benchmarks catalog updated: 4 benchmarks implemented (was 1 planned, 4 stubs).
- Benchmark protocol minimum suite (criticality×2, shielding×1, fusion×1) now met.

## [0.1.0] — 2026-06-28

### Added
- Initial open-source release.
- `openmc-agent.agent.md` — pure open-source OpenMC AI agent with A→H workflow.
- `instructions/openmc-evaluation.instructions.md` — benchmark evaluation feedback loop.
- `skills/openmc-benchmark-runner/SKILL.md` — benchmark execution workflow.
- `skills/openmc-input-repair/SKILL.md` — guided validation repair (max 2 iterations).
- `backends/README.md` — local and SLURM backend documentation.
- `backends/local_executor.py` — local execution backend implementation.
- `CONSTITUTION.md` — lightweight policy index.
- GODIVA benchmark (criticality, ICSBEP HEU-MET-FAST-001): model.py + benchmark.yaml.
- `docs/architecture.md`, `docs/benchmark-protocol.md`, `docs/evaluation-framework.md`.
- E2E pipeline test for GODIVA benchmark.
- Contract tests: frontmatter parseability, tool budget, private dependency blocklist, required sections.
- `scripts/check_tool_budget.py` — CI-enforceable tool budget verification.
