---
description: "OpenMC benchmark evaluation feedback loop: run benchmarks, compare results, auto-diagnose deviations, and record evaluation quality metrics. 基准评测闭环协议, benchmark 对比, C/E 分析, 偏差诊断."
applyTo: "openmc-agent"
revision: 1
---

# OpenMC Evaluation Feedback Loop — 基准评测闭环协议

**Trigger**: Stage F of the OpenMC Agent workflow (after post-processing, before delivery audit).

## Protocol

### Step 1 — Benchmark Matching

Identify the closest benchmark(s) from `benchmarks/` that match the current model:

1. Read `benchmarks/INDEX.md` for the benchmark catalog.
2. Match by: code (OpenMC), geometry type (CSG/DAGMC), physics domain (criticality/shielding/fusion), and key metrics (k-eff/TBR/flux).
3. If no exact match, use the nearest benchmark and note `[BENCHMARK: approximate match — <deviation rationale>]`.

### Step 2 — Benchmark Execution

Run the matched benchmark using `skills/openmc-benchmark-runner/SKILL.md`:

1. Load benchmark definition from `benchmarks/<category>/<name>/`.
2. Build benchmark model from `model.py` and `meta.yaml`.
3. Run with benchmark-standard settings (not user settings — use benchmark particle count and batch config).
4. Extract key metrics from the benchmark statepoint.

### Step 3 — Comparison

For each key metric, compute:

| Metric | Formula | Pass Threshold |
|--------|---------|---------------|
| k-eff C/E | `k_user / k_benchmark` | 0.99 ≤ C/E ≤ 1.01 |
| k-eff Δ (pcm) | `(k_user - k_benchmark) × 1e5` | \|Δ\| ≤ 500 pcm |
| Flux rel. diff. | `|φ_user - φ_benchmark| / φ_benchmark` per bin | ≤ 5% for ≥80% of bins |
| TBR deviation | `|TBR_user - TBR_benchmark| / TBR_benchmark` | ≤ 5% |
| Rel. error | `σ / mean` for each tally | ≤ 0.05 for key tallies |

### Step 4 — Deviation Diagnosis

If any metric fails the pass threshold:

1. **k-eff deviation** → Check: material densities, geometry dimensions, cross-section library version, batch convergence.
2. **Flux deviation** → Check: energy filter bin edges, source spectrum definition, tally normalization.
3. **TBR deviation** → Check: Li-6 enrichment, breeder zone thickness, neutron multiplier material.
4. **High rel. error** → Check: particle count, variance reduction, tally convergence.

Record diagnosis in the evaluation report with `[DIAGNOSIS]` tags.

### Step 5 — Evaluation Report

Write `<output_dir>/evaluation.md`:

```markdown
## Evaluation Report

**Model**: <model description>
**Benchmark**: <benchmark name/tag>
**Date**: <YYYY-MM-DD>

### Comparison Results
| Metric | User Value | Benchmark Value | Deviation | Pass/Fail |
|--------|-----------|----------------|-----------|-----------|
| k-eff | 1.23456 ± 0.00012 | 1.23500 | -44 pcm | PASS |
| ... | ... | ... | ... | ... |

### Overall
- **Passed**: N/M metrics
- **Failed**: K/M metrics
- **Status**: PASS | CONDITIONAL | FAIL

### Diagnoses
- [DIAGNOSIS] <finding> → <recommendation>
```

## Pass/Fail Policy

- **PASS**: All metrics within thresholds → proceed to Stage G (Pre-Delivery Audit).
- **CONDITIONAL**: 1–2 metrics marginally fail → flag in delivery with `[EVAL: CONDITIONAL — <metric> deviates by <value>]`, proceed to Stage G.
- **FAIL**: ≥3 metrics fail or any metric deviates by >2× threshold → block delivery, report to user, return to Stage B for model revision.

## Skill Integration

This protocol delegates benchmark execution to `skills/openmc-benchmark-runner/SKILL.md`.
If that skill file is unavailable, fall back to manual benchmark execution with the same comparison table.
