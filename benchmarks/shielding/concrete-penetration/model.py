#!/usr/bin/env python3
"""Concrete penetration shielding benchmark — neutron flux vs depth."""
import openmc
import numpy as np


def build_model() -> openmc.Model:
    """Build a 1D slab shielding benchmark.

    Geometry:
        Source plane → 60 cm concrete slab
        Tallies: flux in 6×10 cm axial bins along penetration direction.
    """
    # ── Materials ──
    # Ordinary concrete (simplified: O, Si, Ca, H, with standard density)
    concrete = openmc.Material(name="Concrete")
    concrete.set_density("g/cm3", 2.3)
    concrete.add_nuclide("H1", 0.01, "wo")
    concrete.add_nuclide("O16", 0.529, "wo")
    concrete.add_nuclide("Si28", 0.337, "wo")
    concrete.add_nuclide("Ca40", 0.044, "wo")
    concrete.add_nuclide("Al27", 0.034, "wo")
    concrete.add_nuclide("Fe56", 0.014, "wo")
    concrete.add_nuclide("Na23", 0.016, "wo")
    concrete.add_nuclide("K39", 0.013, "wo")
    concrete.add_nuclide("Mg24", 0.002, "wo")
    concrete.add_nuclide("C12", 0.001, "wo")

    materials = openmc.Materials([concrete])

    # ── Geometry ──
    slab_length = 60.0  # cm
    # Surfaces: axial planes along z; vacuum on left, periodic on right, reflective on sides
    z0 = openmc.ZPlane(z0=0.0, boundary_type="vacuum")
    z_planes = [openmc.ZPlane(z0=float(z)) for z in np.linspace(10, slab_length, 6)]
    z_end = openmc.ZPlane(z0=slab_length, boundary_type="vacuum")
    # Infinite in x and y via reflective boundaries
    x_left = openmc.XPlane(x0=-10.0, boundary_type="reflective")
    x_right = openmc.XPlane(x0=10.0, boundary_type="reflective")
    y_bot = openmc.YPlane(y0=-10.0, boundary_type="reflective")
    y_top = openmc.YPlane(y0=10.0, boundary_type="reflective")

    all_z = [z0] + z_planes + [z_end]
    xy_region = +x_left & -x_right & +y_bot & -y_top

    cells = []
    for i in range(len(all_z) - 1):
        region = +all_z[i] & -all_z[i + 1] & xy_region
        cells.append(openmc.Cell(fill=concrete, region=region, name=f"slab_{i+1}"))

    root = openmc.Universe(cells=cells)
    geometry = openmc.Geometry(root)

    # ── Settings ──
    settings = openmc.Settings()
    settings.particles = 50000
    settings.batches = 20
    settings.inactive = 5
    settings.run_mode = "fixed source"

    source = openmc.IndependentSource()
    source.space = openmc.stats.Point((0.0, 0.0, -1.0))
    source.angle = openmc.stats.Monodirectional((0.0, 0.0, 1.0))
    # 2 MeV neutron source (fission-spectrum average)
    source.energy = openmc.stats.Discrete([2.0e6], [1.0])
    settings.source = source

    # ── Tallies ──
    energy_filter = openmc.EnergyFilter([1.0e-5, 1.0, 1.0e5, 2.0e7])
    cell_filter = openmc.CellFilter(cells)

    flux_tally = openmc.Tally(name="flux per slab segment")
    flux_tally.filters = [cell_filter, energy_filter]
    flux_tally.scores = ["flux"]

    tallies = openmc.Tallies([flux_tally])

    return openmc.Model(geometry=geometry, materials=materials,
                        settings=settings, tallies=tallies)


if __name__ == "__main__":
    model = build_model()
    model.export_to_xml()
    print("Concrete shielding model exported")
