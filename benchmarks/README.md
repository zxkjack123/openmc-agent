# Benchmarks

This directory contains validated OpenMC benchmark definitions for the evaluation feedback loop.

## Catalog

| Name | Category | Geometry | Source | Status |
|------|----------|----------|--------|--------|
| GODIVA | criticality | CSG | ICSBEP HEU-MET-FAST-001 | ✅ implemented |
| PWR Pin Cell | criticality | CSG | — | ⬜ planned |
| ITER TBM | fusion | CSG | — | ⬜ planned |
| Fusion Blanket | fusion | CSG | — | ⬜ planned |

## Structure

Each benchmark lives in its own directory:

```
benchmarks/<category>/<name>/
├── benchmark.yaml   # Benchmark metadata and reference values
├── model.py         # OpenMC Python model
├── README.md        # Benchmark description and provenance
└── statepoint.N.h5  # Reference statepoint (git-lfs tracked)
```

## Adding a Benchmark

1. Create `benchmarks/<category>/<name>/` directory.
2. Write `benchmark.yaml` with metadata, reference values, and settings.
3. Write `model.py` that reproduces the benchmark configuration.
4. Run `model.py` and commit the reference `statepoint.N.h5` with git-lfs.
5. Add entry to this INDEX.md.

### benchmark.yaml Schema

```yaml
name: "godiva"
category: "criticality"
description: "GODIVA bare highly-enriched uranium sphere"
geometry: "CSG"
source: "ICSBEP HEU-MET-FAST-001"
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
