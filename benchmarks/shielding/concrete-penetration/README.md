# Concrete Penetration Shielding Benchmark

Neutron shielding benchmark: 2 MeV source → 60 cm concrete slab.

## Configuration

| Parameter | Value |
|-----------|-------|
| Source | 2 MeV point, mono-directional |
| Slab material | Ordinary concrete (2.3 g/cm³) |
| Slab thickness | 60 cm |
| Tallies | Flux in 6 × 10 cm segments |
| Boundaries | Reflective in x, y; vacuum at slab faces |

## Reference

- ORNL shielding benchmarks
- Flux attenuation ≈ 0.01 at 50 cm depth

## Running

```bash
export OPENMC_CROSS_SECTIONS=/path/to/cross_sections.xml
python model.py
```
