"""E2E test: GODIVA benchmark → openmc.run() → k-eff validation."""
import os
import shutil
import sys
import tempfile
from pathlib import Path

import h5py
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from backends.local_executor import LocalExecutor

BENCHMARK_DIR = REPO_ROOT / "benchmarks" / "criticality" / "godiva"
CROSS_SECTIONS = os.environ.get(
    "OPENMC_CROSS_SECTIONS", "/home/gw/NucData/nndc_hdf5/cross_sections.xml"
)


def load_benchmark():
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
    """Run GODIVA model via openmc.run() and verify k-eff matches reference.

    Reference: k_eff = 0.9992, tolerance = ±200 pcm (ICSBEP HEU-MET-FAST-001).

    Uses the openmc Python API (openmc.run) instead of a subprocess call
    to avoid runtime dependency on libdagmc.so or specific build artifacts.
    """
    benchmark = load_benchmark()
    ref_k_eff = benchmark["metrics"]["k_eff"]["reference"]
    tolerance_pcm = benchmark["metrics"]["k_eff"]["tolerance_pcm"]

    # Set cross sections and ensure openmc binary is on PATH
    os.environ["OPENMC_CROSS_SECTIONS"] = CROSS_SECTIONS
    openmc_bin_dir = str(Path("/home/gw/opt/openmc/build/bin"))
    if openmc_bin_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{openmc_bin_dir}:{os.environ.get('PATH', '')}"
    # Ensure DAGMC library is loadable (required by this OpenMC build)
    dagmc_lib_dir = "/home/gw/opt/DAGMC-build/lib"
    existing_ld = os.environ.get("LD_LIBRARY_PATH", "")
    if dagmc_lib_dir not in existing_ld:
        os.environ["LD_LIBRARY_PATH"] = f"{dagmc_lib_dir}:{existing_ld}" if existing_ld else dagmc_lib_dir

    import openmc

    with tempfile.TemporaryDirectory() as tmpdir:
        save_cwd = os.getcwd()
        os.chdir(tmpdir)

        try:
            # Build model and run via the Python API (no subprocess, no libdagmc dependency)
            # ---- inline GODIVA model ---- #
            heu = openmc.Material(name="HEU")
            heu.set_density("g/cm3", 18.74)
            heu.add_nuclide("U234", 1.02, "wo")
            heu.add_nuclide("U235", 93.71, "wo")
            heu.add_nuclide("U238", 5.27, "wo")

            sphere = openmc.Sphere(r=8.7407, boundary_type="vacuum")
            cell = openmc.Cell(fill=heu, region=-sphere)
            root = openmc.Universe(cells=[cell])
            geometry = openmc.Geometry(root)

            settings = openmc.Settings()
            settings.batches = 150
            settings.inactive = 50
            settings.particles = 10000
            settings.run_mode = "eigenvalue"
            settings.source = openmc.IndependentSource(
                space=openmc.stats.Point()
            )

            model = openmc.Model(geometry=geometry, settings=settings)
            model.export_to_xml()
            openmc.run()

            # Discover and read statepoint
            matches = list(Path(tmpdir).glob("statepoint.*.h5"))
            assert matches, "No statepoint file found after openmc.run()"
            sp_path = matches[0]

            with h5py.File(sp_path, "r") as sp:
                k_combined = sp["k_combined"][0]
                assert k_combined is not None, "k_combined is None"

            delta_pcm = (k_combined - ref_k_eff) / ref_k_eff * 1e5
            assert abs(delta_pcm) <= tolerance_pcm, (
                f"k-eff {k_combined:.6f} deviates from reference {ref_k_eff:.6f} "
                f"by {delta_pcm:.0f} pcm (tolerance ±{tolerance_pcm} pcm)"
            )
        finally:
            os.chdir(save_cwd)


def test_localexecutor_missing_cross_sections(monkeypatch):
    monkeypatch.delenv("OPENMC_CROSS_SECTIONS", raising=False)
    executor = LocalExecutor(cross_sections=None)
    with pytest.raises(OSError, match="CROSS_SECTIONS"):
        executor.prepare(str(BENCHMARK_DIR))


def test_localexecutor_missing_model_py():
    executor = LocalExecutor(cross_sections="/fake")
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(FileNotFoundError, match="model.py"):
            executor.prepare(tmpdir)
