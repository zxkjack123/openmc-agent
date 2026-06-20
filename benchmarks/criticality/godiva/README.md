# Benchmark: GODIVA

**ICSBEP Designation**: HEU-MET-FAST-001

## Physical Description

A bare sphere of highly enriched uranium (HEU) metal:

| Parameter | Value |
|-----------|-------|
| Geometry | Sphere, radius 8.7407 cm |
| Material | HEU metal, ~93.7 wt% U-235 |
| Density | 18.74 g/cm³ |
| Boundary | Vacuum |
| Core mass | ~52.5 kg HEU |

The GODIVA reactor was originally assembled at Los Alamos Scientific Laboratory
(now LANL) in 1951–1952 and operated as a fast burst reactor.  It is among the
most thoroughly characterised fast critical benchmarks in the ICSBEP Handbook.

## Reference

- **Source**: ICSBEP Handbook, HEU-MET-FAST-001
- **Evaluated k-eff**: 0.9992 ± 100 pcm (ENDF/B-VIII.0)
- **Benchmark tolerance**: ±200 pcm

## Model Approximations

The model uses a three-isotope approximation of the HEU fuel:

| Nuclide | Weight fraction (wt%) |
|---------|----------------------|
| U-234   | 1.02                 |
| U-235   | 93.71                |
| U-238   | 5.27                 |

Trace impurities (primarily daughter products of uranium decay) are omitted.
The specified 200 pcm tolerance is wide enough to absorb the small reactivity
bias introduced by this simplification.

## Running

```bash
cd benchmarks/criticality/godiva
OPENMC_CROSS_SECTIONS=/path/to/nndc_hdf5/cross_sections.xml python model.py
```

This exports `geometry.xml`, `materials.xml`, and `settings.xml`.  Run the
exported model with:

```bash
OPENMC_CROSS_SECTIONS=/path/to/nndc_hdf5/cross_sections.xml openmc
```

## Expected Output

| Metric | Expected value | Tolerance |
|--------|---------------|-----------|
| k-eff  | 0.9992        | ±200 pcm  |

With 10 000 particles per batch × 150 batches (50 inactive, 100 active), a
typical simulation yields a statistical uncertainty of ≤ 50 pcm.
