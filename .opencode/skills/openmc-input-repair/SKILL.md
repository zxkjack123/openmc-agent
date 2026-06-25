---
description: >-
  Use when repairing OpenMC input files that failed validation. Provides
  automated fix suggestions for common model errors: missing surface
  references, unknown nuclides, invalid tally filters, geometry conflicts.
  Max 2 repair iterations before escalating to manual review.
---

# OpenMC Input Repair

This skill provides automated repair guidance for OpenMC validation failures.

## Repair Process

1. Parse the validation error report from openmc-validator
2. Match each error to a known repair pattern
3. Apply fixes (materials, geometry, settings, or tallies)
4. Re-validate — if still failing, repeat (max 2 iterations)
5. If unresolved after 2 iterations, escalate to manual review with a detailed diagnostic report

## Common Repair Patterns

### Materials
- **Unknown nuclide**: check spelling against ENDF/B library; suggest closest match
- **Invalid density unit**: convert between g/cm³, kg/m³, atom/b-cm
- **Mass fraction vs atom fraction mismatch**: detect and convert

### Geometry
- **Missing surface reference**: add the referenced surface definition
- **Cell region syntax error**: fix infix boolean expressions
- **Universe assignment conflict**: resolve duplicate universe assignments
- **DAGMC .h5m path error**: verify file path exists

### Settings
- **Invalid run mode**: map to valid enum (eigenvalue, fixed source, plot, volume)
- **Insufficient particles**: suggest minimum for target uncertainty
- **Missing source definition**: add spatial/energy/angle distribution

### Tallies
- **Filter bin ordering**: reorder energy bins to ascending
- **Invalid score name**: map to valid OpenMC score list
- **Nuclide reference mismatch**: ensure tally nuclides exist in materials
