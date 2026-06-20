---
name: "openmc-benchmark-runner"
description: "Run OpenMC benchmarks, compare results against reference values, produce evaluation reports. OpenMC benchmark 运行, 基准对比, C/E analysis."
revision: 1
---

# Skill: OpenMC Benchmark Runner

## When to Use

- Stage F of the OpenMC Agent workflow (evaluation feedback loop).
- Comparing a user-built model against known reference results.
- Validating that OpenMC installation produces correct physics results.

## When NOT to Use

- Building new models from scratch (use OpenMC Agent Stage B).
- Debugging geometry or material errors (use `openmc-validator` + `skills/openmc-input-repair/SKILL.md`).

## Workflow

### 1. Load Benchmark Definition

Read `benchmarks/<category>/<name>/benchmark.yaml`:

```yaml
name: "godiva"
category: "criticality"
description: "GODIVA bare highly-enriched uranium sphere"
geometry: "CSG"
metrics:
  k_eff:
    reference: 0.9992
    tolerance_pcm: 200
settings:
  particles: 10000
  batches: 50
  inactive: 20
cross_sections: "ENDF/B-VIII.0"
```

### 2. Execute Benchmark

Run the benchmark `model.py` with the specified settings:

```bash
cd benchmarks/<category>/<name>/
export OPENMC_CROSS_SECTIONS=<path>
python model.py
```

### 3. Extract Results

```python
import openmc

sp = openmc.StatePoint("statepoint.50.h5")
k_eff = sp.k_combined
# Extract tally results as defined in benchmark.yaml metrics
```

### 4. Compare Against Reference

Compute and report:
- k-eff: absolute difference in pcm, C/E ratio.
- Other metrics: relative deviation.

### 5. Write Evaluation Report

Output to `<output_dir>/evaluation.md` following the template in
`instructions/openmc-evaluation.instructions.md`.

## Inputs & Outputs

| Input | Type | Source |
|-------|------|--------|
| Benchmark name/category | string | User or auto-detected from model |
| Benchmark YAML | file | `benchmarks/<category>/<name>/benchmark.yaml` |
| Benchmark model | file | `benchmarks/<category>/<name>/model.py` |

| Output | Type | Destination |
|--------|------|-------------|
| Evaluation report | file | `<output_dir>/evaluation.md` |
| Benchmark statepoint | HDF5 | `benchmarks/<category>/<name>/statepoint.*.h5` |

## Common Pitfalls

1. **Wrong cross-section library**: Benchmark reference values assume ENDF/B-VIII.0. Using a different library will cause systematic deviations.
2. **Insufficient particles**: Benchmark default particle counts are chosen for statistical convergence. Reducing particles will increase rel. error.
3. **Batch mismatch**: Ensure `inactive` batches match benchmark settings — active batch count affects k-eff uncertainty estimation.

## Revision Log

- rev 1 (2026-06-20): Initial skill for openmc-agent v0.1.0.
