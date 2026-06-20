# Evaluation Framework

> How the OpenMC Agent evaluates simulation quality — from validation through benchmark comparison to delivery.

## Quality Pipeline

```
Input Model
    │
    ▼
Stage C: Validator Checks (14 tools)
    │  └── Deterministic: structural errors, interface mismatches
    │  └── Auto-repair: max 2 iterations
    │
    ▼
Stage D: Execution
    │  └── Runtime errors, convergence warnings
    │
    ▼
Stage E: Post-Processing
    │  └── Tally extraction, derived quantities
    │
    ▼
Stage F: Benchmark Comparison
    │  └── Statistical: C/E, deviation, rel. error
    │  └── Conditional pass/fail
    │
    ▼
Stage G: Pre-Delivery Audit
    │  └── Physical plausibility (L2-Standard)
    │  └── Blocking pass/fail
    │
    ▼
Delivery
```

## Evaluation Dimensions

### D1 — Structural Correctness (Stage C)

| Check | Tool | Severity |
|-------|------|----------|
| Material definitions | validate_materials | Error ≥ Warning blocks |
| Geometry integrity | validate_geometry | Error ≥ Warning blocks |
| Settings sanity | validate_settings | Error ≥ Warning blocks |
| Tally consistency | validate_tallies | Error ≥ Warning blocks |
| Cross-section availability | check_cross_section_library | Warning logs, Error blocks |
| Energy filter coverage | check_energy_filter_coverage | Warning logs |
| Tally-geometry consistency | check_tally_filter_consistency | Warning logs |
| End-to-end model | validate_model | Error ≥ Warning blocks |

### D2 — Numerical Accuracy (Stage F)

| Metric | Pass Threshold | Evaluation |
|--------|---------------|------------|
| k-eff | \|Δ\| ≤ 500 pcm, 0.99 ≤ C/E ≤ 1.01 | Benchmark comparison |
| Flux spectra | ≤5% relative diff for ≥80% bins | Energy-bin-wise comparison |
| TBR | ≤5% deviation | Fusion benchmarks only |
| Heating | ≤10% deviation | Shielding/fusion benchmarks |
| Rel. error | σ/mean ≤ 0.05 | All tallies |

### D3 — Physical Plausibility (Stage G)

| Check | Method |
|-------|--------|
| Unit consistency | §1 — all quantities have units |
| Energy cutoffs | §2 — bounds match physics domain |
| Order-of-magnitude | §3 — results within typical range |
| Conservation | §4 — particle/energy balance |
| Cross-validation | §5 — at least one independent comparison |

## Scoring

| Overall Status | Condition |
|---------------|-----------|
| **PASS** | D1 all pass + D2 all pass + D3 all pass |
| **CONDITIONAL** | D1 all pass + D2 1-2 marginal fails + D3 all pass |
| **FAIL** | D1 any blocking error remaining OR D2 ≥3 fails OR D3 any fail |

CONDITIONAL results are delivered with warnings and the specific deviations flagged.
FAIL results block delivery entirely — the user must address issues.
