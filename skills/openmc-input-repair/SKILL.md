---
name: "openmc-input-repair"
description: "Guided repair of OpenMC input validation failures: diagnose errors from openmc-validator output, apply targeted fixes, re-validate. OpenMC 输入修复, 校验错误诊断, 自动修复."
revision: 1
---

# Skill: OpenMC Input Repair

## When to Use

- Stage C of the OpenMC Agent workflow (validation → auto-repair loop).
- `openmc-validator` returned errors with severity ≥ Warning.
- The model has been validated and found to have structural issues.

## When NOT to Use

- Pre-validation model building (use OpenMC Agent Stage B).
- Post-execution result analysis (use OpenMC Agent Stage E).
- OpenMC installation / environment issues (not input-model errors).

## Workflow

### 1. Parse Validation Output

Extract error codes and descriptions from the validator response:

```
openmc-validator/validate_materials → error MAT-001: "Negative density for material 'fuel'"
openmc-validator/validate_tallies  → error TAL-003: "Energy bins not in ascending order"
```

Group errors by domain: Materials (MAT-*), Geometry (GEO-*), Settings (SET-*), Tallies (TAL-*), Cross-sections (XS-*).

### 2. Diagnose Root Cause

For each error code, identify the likely root cause in the model:

| Error Code | Likely Root Cause | Fix |
|-----------|-------------------|-----|
| MAT-001 | Negative density | Check `material.set_density()` arguments |
| MAT-002 | Nuclide typo | Verify nuclide name against ENDF convention (e.g., `'U235'` not `'U-235'`) |
| MAT-003 | Fraction sum ≠ 1.0 | Check ao/wo fraction normalization |
| GEO-001 | Unclosed surface | Cell region references undefined surface |
| GEO-002 | Unknown universe | Universe ID used in cell not registered in geometry |
| SET-001 | batches ≤ inactive | Increase batches or decrease inactive |
| SET-002 | Missing source | Add `openmc.Source` to settings |
| TAL-003 | Energy bins not ascending | Reverse bin edges to ascending eV order |
| TAL-004 | Invalid score | Use score from `openmc.Tally.valid_scores` |
| XS-001 | Nuclide not in library | Use different nuclide or update cross_sections.xml |
| EFC-001 | Filter edge < source max | Extend energy filter upper bound |

### 3. Apply Fix

Edit the model file applying the fix from the table above. After each fix:

1. Re-run the specific validator that failed.
2. Confirm the error is resolved.
3. If new errors appear, diagnose and fix those too.

### 4. Re-validate Full Model

After all individual fixes, run `openmc-validator/validate_model` for end-to-end
re-validation.

### 5. Iteration Limit

- **Max 2 repair iterations**. After that, report unresolved errors to the user.
- Between iterations, re-read the model file for current state (it may have been
  modified by the previous iteration).
- Do not recurse indefinitely — if the same error persists after 2 iterations,
  the root cause is likely deeper than input repair can fix.

## Inputs & Outputs

| Input | Type | Source |
|-------|------|--------|
| Validation errors | JSON | openmc-validator output |
| Model file | .py | User's OpenMC Python model |

| Output | Type | Destination |
|--------|------|-------------|
| Fixed model | .py | In-place edit of model file |
| Repair log | markdown | `<output_dir>/repair_log.md` |

## Common Pitfalls

1. **Fixing symptoms not causes**: Don't just add `+1` to make fractions sum to 1.0 — check WHY they don't sum.
2. **Partial fixes breaking other validators**: Fixing a material issue may change nuclide IDs that affect tally filters. Always re-validate the full model after the repair cycle.
3. **Energy filter ordering**: OpenMC requires ascending eV — but FISPACT-II requires descending MeV. Don't mix up the conventions. Use the converter tool for cross-code transfers.

## Revision Log

- rev 1 (2026-06-20): Initial skill for openmc-agent v0.1.0.
