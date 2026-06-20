"""Local execution backend for OpenMC models via subprocess."""
import glob
import os
import subprocess
from pathlib import Path


class LocalExecutor:
    """Run OpenMC models locally via subprocess.

    Conforms to the BackendExecutor interface defined in backends/README.md.
    """

    def __init__(self, cross_sections: str | None = None):
        self.cross_sections = cross_sections or os.environ.get("OPENMC_CROSS_SECTIONS")

    def prepare(self, model_dir: str) -> None:
        """Verify model directory and cross sections are available."""
        model_path = Path(model_dir) / "model.py"
        if not model_path.exists():
            raise FileNotFoundError(f"model.py not found in {model_dir}")
        if not self.cross_sections:
            raise EnvironmentError(
                "OPENMC_CROSS_SECTIONS must be set or passed to LocalExecutor"
            )

    def run(self, model_dir: str) -> subprocess.CompletedProcess:
        """Execute model.py in model_dir and capture output."""
        env = os.environ.copy()
        env["OPENMC_CROSS_SECTIONS"] = self.cross_sections
        return subprocess.run(
            ["python", "model.py"],
            cwd=model_dir,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def cleanup(self, model_dir: str) -> None:
        """Remove generated XML files from model_dir."""
        for pattern in ["*.xml"]:
            for f in Path(model_dir).glob(pattern):
                try:
                    f.unlink()
                except OSError:
                    pass  # best-effort cleanup

    def find_statepoint(self, model_dir: str) -> Path | None:
        """Discover the statepoint file globbing statepoint.*.h5."""
        matches = list(Path(model_dir).glob("statepoint.*.h5"))
        return matches[0] if matches else None
