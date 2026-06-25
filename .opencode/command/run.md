---
description: Build and optionally run an OpenMC simulation from model files or specifications.
agent: openmc-build
---

Build an OpenMC simulation model following the constitution's construction order:

1. **Materials** — define all nuclides/elements with correct density and units
2. **Geometry** — create surfaces, regions, cells, universes, and lattices in order
3. **Settings** — set run mode, batches, particles, inactive batches, source
4. **Tallies** — define filters, scores, and nuclide bins

After building:

- Run Stage C validation (mandatory, blocking)
- If validation passes, execute via the specified backend:
  - `local`: run `openmc.run()` in-process
  - `slurm`: generate `submit.sh` with safety margins (CPU +20%, wall time ×1.5, memory +30%)
- Post-process results and generate a summary report

Usage: `/run [backend: local|slurm] [description of the model]`

$ARGUMENTS
