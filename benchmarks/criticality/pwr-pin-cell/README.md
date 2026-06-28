# PWR Pin-Cell Benchmark

Standard light-water reactor (LWR) pin-cell criticality benchmark.

## Configuration

| Parameter | Value |
|-----------|-------|
| Fuel | UO2, 3.3 wt% U-235 |
| Fuel density | 10.297 g/cm³ |
| Fuel radius | 0.4096 cm |
| Gap | He, 0.418 cm outer radius |
| Cladding | Zircaloy-4, 0.475 cm outer radius |
| Moderator | H2O, 0.740 g/cm³ |
| Lattice pitch | 1.26 cm (square) |
| Boundaries | Reflective (infinite lattice) |
| Temperature | 300 K (default) |

## Reference

- OECD/NEA PWR pin-cell benchmarks
- Reference k_eff ≈ 1.175 with ENDF/B-VIII.0

## Running

```bash
export OPENMC_CROSS_SECTIONS=/path/to/cross_sections.xml
python model.py
```
