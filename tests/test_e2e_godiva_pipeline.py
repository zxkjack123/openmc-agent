"""E2E test: GODIVA benchmark → LocalExecutor → k-eff validation."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import h5py
import pytest
import yaml

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from backends.local_executor import LocalExecutor

BENCHMARK_DIR = REPO_ROOT / "benchmarks" / "criticality" / "godiva"
CROSS_SECTIONS = os.environ.get(
    "OPENMC_CROSS_SECTIONS", "/home/gw/NucData/nndc_hdf5/cross_sections.xml"
)

# Locate openmc binary — check PATH first, then known build location
_OPENMC_BIN = shutil.which("openmc")
if _OPENMC_BIN is None:
    _candidate = Path("/home/gw/opt/openmc/build/bin/openmc")
    if _candidate.exists():
        _OPENMC_BIN = str(_candidate)
    else:
        _OPENMC_BIN = "openmc"  # fallback — subprocess will report error


def load_benchmark():
    """Load benchmark.yaml and return metrics dict."""
    with open(BENCHMARK_DIR / "benchmark.yaml") as f:
        return yaml.safe_load(f)


def test_godiva_model_exports_xml():
    """Verify model.py exports all three XML files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copy(BENCHMARK_DIR / "model.py", tmpdir)
        result = LocalExecutor(cross_sections=CROSS_SECTIONS).run(tmpdir)
        assert result.returncode == 0, f"model.py failed:\n{result.stderr}"
        for xml_file in ("geometry.xml", "materials.xml", "settings.xml"):
            assert Path(tmpdir, xml_file).exists(), f"Missing {xml_file}"


@pytest.mark.slow
def test_godiva_k_eff_within_tolerance():
    """Run GODIVA model and verify k-eff matches reference within tolerance.

    Reference: k_eff = 0.9992, tolerance = ±200 pcm (ICSBEP HEU-MET-FAST-001).
    """
    benchmark = load_benchmark()
    ref_k_eff = benchmark["metrics"]["k_eff"]["reference"]
    tolerance_pcm = benchmark["metrics"]["k_eff"]["tolerance_pcm"]

    executor = LocalExecutor(cross_sections=CROSS_SECTIONS)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy model to tmpdir, export XML, then run OpenMC
        shutil.copy(BENCHMARK_DIR / "model.py", tmpdir)
        result = executor.run(tmpdir)
        assert result.returncode == 0, f"model.py failed:\n{result.stderr}"

        # Run the actual Monte Carlo simulation
        env = os.environ.copy()
        env["OPENMC_CROSS_SECTIONS"] = CROSS_SECTIONS
        sim_result = subprocess.run(
            [_OPENMC_BIN], cwd=tmpdir, env=env,
            capture_output=True, text=True, check=False,
        )
        assert sim_result.returncode == 0, f"OpenMC failed:\n{sim_result.stderr}"

        # Discover and read statepoint
        sp_path = executor.find_statepoint(tmpdir)
        assert sp_path is not None, "No statepoint file found"

        with h5py.File(sp_path, "r") as sp:
            k_combined = sp["k_combined"][0]  # [0] = mean (OpenMC stores [mean, std])
            assert k_combined is not None, "k_combined is None in statepoint"

        # Compute deviation in pcm
        delta_pcm = (k_combined - ref_k_eff) / ref_k_eff * 1e5
        assert abs(delta_pcm) <= tolerance_pcm, (
            f"k-eff {k_combined:.6f} deviates from reference {ref_k_eff:.6f} "
            f"by {delta_pcm:.0f} pcm (tolerance ±{tolerance_pcm} pcm)"
        )


def test_localexecutor_missing_cross_sections(monkeypatch):
    """Verify error when OPENMC_CROSS_SECTIONS is unset."""
    monkeypatch.delenv("OPENMC_CROSS_SECTIONS", raising=False)
    executor = LocalExecutor(cross_sections=None)
    with pytest.raises(OSError, match="CROSS_SECTIONS"):
        executor.prepare(str(BENCHMARK_DIR))


def test_localexecutor_missing_model_py():
    """Verify FileNotFoundError when model.py is absent."""
    executor = LocalExecutor(cross_sections="/fake")
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(FileNotFoundError, match="model.py"):
            executor.prepare(tmpdir)
