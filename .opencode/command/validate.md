---
description: Validate OpenMC model files using openmc-validator before execution.
agent: openmc-build
---

Validate the OpenMC model in the current workspace. Run these checks in order:

1. **Materials** — validate nuclide names, density units, composition consistency
2. **Geometry** — validate surface references, cell definitions, universe hierarchy
3. **Settings** — validate run mode, batch/particle counts, source definition
4. **Tallies** — validate filter bin ordering, score names, nuclide references
5. **Cross-section library** — verify requested nuclides exist in the configured library
6. **Full model** — end-to-end validation of the complete model

If any check fails, use the `openmc-input-repair` skill to attempt auto-repair (max 2 iterations).
Report a summary table of all checks with pass/fail status.

$ARGUMENTS
