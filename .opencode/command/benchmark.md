---
description: Run benchmark evaluation for an OpenMC simulation result.
agent: openmc-build
---

Run the benchmark evaluation framework on an OpenMC simulation output.

Steps:

1. Locate the simulation output (statepoint.h5, summary.h5)
2. Extract key metrics: k_eff, tally results, uncertainties, relative errors
3. Compare against benchmark reference values (if available in benchmarks/)
4. Compute C/E ratios and statistical measures
5. Generate an evaluation report following the format in `instructions/openmc-evaluation.instructions.md`

If the simulation hasn't been run yet, suggest running `/run` first.

$ARGUMENTS
