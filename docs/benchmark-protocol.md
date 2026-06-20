# Benchmark Protocol

> How benchmarks are defined, executed, and compared in the evaluation feedback loop.

## Benchmark Definition

Each benchmark is a directory under `benchmarks/<category>/<name>/` containing:

```
benchmarks/<category>/<name>/
├── benchmark.yaml   # Required: metadata, reference values, run settings
├── model.py         # Required: Python model that produces the benchmark
├── README.md        # Required: provenance and interpretation notes
└── statepoint.N.h5  # Optional (git-lfs): pre-computed reference statepoint
```

## benchmark.yaml Schema

```yaml
# Required fields
name: "string"              # Short identifier
category: "string"          # criticality | shielding | fusion | activation
description: "string"       # One-paragraph physical description
geometry: "CSG | DAGMC"    # Geometry representation
source: "string"            # Provenance (ICSBEP ID, publication DOI, etc.)

# Required: key metrics with reference values
metrics:
  <metric_name>:
    reference: <float>      # Expected value
    tolerance_pcm: <float>  # For k-eff; omit for other metrics
    tolerance_pct: <float>  # For non-k-eff metrics (percentage)

# Required: simulation settings that achieve the reference values
settings:
  particles: <int>
  batches: <int>
  inactive: <int>

# Required: cross-section library
cross_sections: "ENDF/B-VIII.0"

# Optional
notes: "string"             # Additional context
```

## Pass/Fail Criteria

| Metric Type | Pass Condition |
|------------|---------------|
| k-eff | \|Δ\| ≤ tolerance_pcm AND 0.99 ≤ C/E ≤ 1.01 |
| Flux/spectra | Relative difference ≤ 5% for ≥80% of bins |
| TBR | Deviation ≤ 5% |
| Nuclear heating | Deviation ≤ 10% |
| Rel. error (any tally) | σ/mean ≤ 0.05 |

## Evaluation Report Template

```
## Evaluation Report
**Model**: <description>
**Benchmark**: <name>
**Date**: YYYY-MM-DD

### Comparison
| Metric | User Value | Reference | Deviation | Status |
|--------|-----------|-----------|-----------|--------|
| k-eff  | 1.23456 ± 0.00012 | 1.23500 | -44 pcm | PASS |
| TBR    | 1.145 ± 0.005 | 1.150 | -0.4% | PASS |

### Overall
**Passed**: N/M | **Failed**: K/M | **Status**: PASS | CONDITIONAL | FAIL

### Diagnoses
[Only if failures exist]
- [DIAGNOSIS] <finding> → <recommendation>
```

## Benchmark Selection Logic

When selecting a benchmark for a user model:

1. **Exact match**: Same geometry type + same physics domain + same key metrics.
2. **Partial match**: Same physics domain + same key metrics, different geometry.
3. **Nearest neighbor**: Closest physics domain match, different metrics.
4. **No match**: Skip evaluation, note `[EVAL: SKIPPED — no matching benchmark]`.

## Minimum Benchmark Suite

The agent should ship with at least 4 benchmarks covering:

1. **Criticality** — GODIVA bare sphere (ICSBEP HEU-MET-FAST-001).
2. **LWR** — PWR pin-cell (OECD/NEA benchmarks).
3. **Fusion** — Generic fusion blanket (OpenMC examples).
4. **Shielding** — Concrete penetration (ORNL benchmarks).

These provide baseline validation that OpenMC produces correct physics results.
