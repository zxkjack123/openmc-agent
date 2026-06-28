# Liquid Breeder Blanket Benchmark

Fusion tritium breeding blanket benchmark with 14.1 MeV D-T source.

## Configuration

| Parameter | Value |
|-----------|-------|
| Source | 14.1 MeV D-T, mono-directional |
| First wall | RAFM steel, 5 cm |
| Breeder | Li17Pb83, 90% Li-6 enrichment, 60 cm |
| Neutron multiplier | Beryllium, 20 cm |
| Shield | RAFM steel, 5 cm |
| TBR tally | Li-6 + Li-7 (n,Xt) in breeder zone |
| Boundaries | Reflective in x, y; vacuum at back face |

## Reference

- OpenMC fusion blanket examples
- Reference TBR ≈ 1.15 for 90% Li-6 enrichment

## Running

```bash
export OPENMC_CROSS_SECTIONS=/path/to/cross_sections.xml
python model.py
```
