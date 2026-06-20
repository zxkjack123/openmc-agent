# OpenMC Agent Backends

This directory documents the execution backends available for running OpenMC simulations.

## Backend Overview

| Backend | Status | Description |
|---------|--------|-------------|
| `local` | ✅ Built-in | Runs `openmc.run()` in-process on the local machine |
| `slurm` | ✅ Built-in | Generates SLURM job scripts; user submits manually |
| `scnet` | 🔒 Private overlay | HPC auto-submission via scnetresource-router (in copilot-agents, not here) |

## Local Backend

### Requirements

- OpenMC ≥ 0.14 installed (`import openmc` succeeds).
- `OPENMC_CROSS_SECTIONS` environment variable pointing to `cross_sections.xml`.
- Sufficient RAM (≈1 GB per 100k particles for typical problems).

### Usage in Agent

The agent detects the local backend automatically when:
- `openmc` is importable.
- No explicit backend override is specified.
- The model is small enough for local execution (default particle count ≤ 100k).

### Resource Estimation

```
RAM ≈ N_particles_per_batch × N_batches_active × sizeof(ParticleState)
    ≈ N_particles × 100 × 1 KB
    ≈ N_particles / 10 MB
```

For large models (>1M particles total), the agent will suggest the SLURM backend.

## SLURM Backend

### Generated Script Template

```bash
#!/bin/bash
#SBATCH --job-name=openmc-<model_name>
#SBATCH --nodes=1
#SBATCH --ntasks=<N>
#SBATCH --cpus-per-task=<M>
#SBATCH --time=<HH:MM:SS>
#SBATCH --output=openmc_%j.out
#SBATCH --error=openmc_%j.err

export OPENMC_CROSS_SECTIONS=<path>
mpirun -n $SLURM_NTASKS python model.py
```

### Resource Safety Margins

| Resource | User-specified | Applied margin |
|----------|---------------|----------------|
| CPU cores | N | N × 1.2 (min +1) |
| Wall time | T | T × 1.5 |
| Memory | M | M × 1.3 |

These margins prevent job failures from resource underestimation.

### User Action Required

The agent generates the script but **does NOT submit** it — the user must manually:

```bash
sbatch submit.sh     # Submit
squeue -u $USER      # Check status
scancel <job_id>     # Cancel if needed
```

## Private Overlay (for copilot-agents users)

If you have access to the private `copilot-agents` ecosystem, the **Simulation Builder**
agent provides additional backend capabilities:

- Automatic HPC cluster selection via `scnetresource-router`.
- Container/SIF image probing and management.
- Software catalog lookup (OpenMC, MCNP, FISPACT-II versions across clusters).
- Interactive sessions (Jupyter, code-server) on HPC nodes.
- File upload/download between local and cluster filesystems.

**This open-source agent does NOT embed or reference those private tools.**

To use the private overlay:
1. Clone `copilot-agents` (private repo).
2. Use "Simulation Builder" instead of "OpenMC Agent" for HPC-integrated workflows.
3. Or: build a local `backends/scnet/` adapter that wires the private MCP tools
   into the OpenMC Agent workflow (not included in this repo).

## Adding a New Backend

To add a custom backend:

1. Create `backends/<name>/README.md` documenting requirements and usage.
2. Implement the backend in `backends/<name>/executor.py` (convention).
3. Register it in the agent's Stage D by adding a detection condition.
4. Submit a PR to openmc-agent.

Backend executors should conform to this interface:

```python
class BackendExecutor:
    """Abstract interface for simulation backends."""

    def prepare(self, model_dir: str) -> None:
        """Set up environment before execution."""
        ...

    def run(self, model_dir: str) -> subprocess.CompletedProcess:
        """Execute the simulation. Returns completed process."""
        ...

    def cleanup(self, model_dir: str) -> None:
        """Clean up temporary files after execution."""
        ...
```
