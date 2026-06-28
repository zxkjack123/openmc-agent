#!/usr/bin/env python3
"""Liquid breeder blanket benchmark — Li17Pb83 with 14.1 MeV D-T source."""
import openmc
import numpy as np


def build_model() -> openmc.Model:
    """Build a simplified 1D slab fusion blanket model.

    Geometry (along z-axis):
        Source plane (z=-1) → 5 cm first wall (RAFM steel) → 60 cm breeder
        (Li17Pb83) → 20 cm reflector (Be) → 5 cm shield (RAFM steel)
        → vacuum boundary.

    Tallies: Li-6(n,α)T reaction rate for TBR calculation.
    """
    # ── Materials ──
    # RAFM steel (simplified Eurofer)
    rafm = openmc.Material(name="RAFM steel")
    rafm.set_density("g/cm3", 7.8)
    rafm.add_nuclide("Fe56", 0.89, "wo")
    rafm.add_nuclide("Cr52", 0.09, "wo")
    rafm.add_nuclide("W186", 0.015, "wo")
    rafm.add_nuclide("Mn55", 0.005, "wo")

    # Li17Pb83 breeder (90% Li-6 enrichment)
    li17pb83 = openmc.Material(name="Li17Pb83 breeder")
    li17pb83.set_density("g/cm3", 9.4)
    li17pb83.add_nuclide("Li6", 0.9 * 0.006, "wo")  # 90% Li-6 enriched
    li17pb83.add_nuclide("Li7", 0.1 * 0.006, "wo")
    li17pb83.add_nuclide("Pb208", 0.524, "wo")
    li17pb83.add_nuclide("Pb207", 0.221, "wo")
    li17pb83.add_nuclide("Pb206", 0.249, "wo")

    # Beryllium neutron multiplier / reflector
    beryllium = openmc.Material(name="Beryllium")
    beryllium.set_density("g/cm3", 1.85)
    beryllium.add_nuclide("Be9", 1.0, "ao")

    materials = openmc.Materials([rafm, li17pb83, beryllium])

    # ── Geometry: 1D slab along z ──
    z_planes = [
        openmc.ZPlane(z0=0.0),     # source side of first wall
        openmc.ZPlane(z0=5.0),     # FW / breeder interface
        openmc.ZPlane(z0=65.0),    # breeder / reflector interface
        openmc.ZPlane(z0=85.0),    # reflector / shield interface
        openmc.ZPlane(z0=90.0, boundary_type="vacuum"),  # back face
    ]
    # Reflective in x, y (infinite slab approximation)
    x_left = openmc.XPlane(x0=-20.0, boundary_type="reflective")
    x_right = openmc.XPlane(x0=20.0, boundary_type="reflective")
    y_bot = openmc.YPlane(y0=-20.0, boundary_type="reflective")
    y_top = openmc.YPlane(y0=20.0, boundary_type="reflective")

    xy_region = +x_left & -x_right & +y_bot & -y_top

    fw_cell = openmc.Cell(fill=rafm,
                          region=+z_planes[0] & -z_planes[1] & xy_region,
                          name="first_wall")
    breeder_cell = openmc.Cell(fill=li17pb83,
                               region=+z_planes[1] & -z_planes[2] & xy_region,
                               name="breeder")
    reflector_cell = openmc.Cell(fill=beryllium,
                                 region=+z_planes[2] & -z_planes[3] & xy_region,
                                 name="reflector")
    shield_cell = openmc.Cell(fill=rafm,
                              region=+z_planes[3] & -z_planes[4] & xy_region,
                              name="shield")

    root = openmc.Universe(cells=[fw_cell, breeder_cell, reflector_cell, shield_cell])
    geometry = openmc.Geometry(root)

    # ── Settings ──
    settings = openmc.Settings()
    settings.particles = 20000
    settings.batches = 50
    settings.inactive = 10
    settings.run_mode = "fixed source"

    source = openmc.IndependentSource()
    source.space = openmc.stats.Point((0.0, 0.0, -1.0))
    source.angle = openmc.stats.Monodirectional((0.0, 0.0, 1.0))
    source.energy = openmc.stats.Discrete([14.1e6], [1.0])
    settings.source = source

    # ── Tallies: TBR (Li-6 + Li-7 tritium production) ──
    cell_filter = openmc.CellFilter([breeder_cell])

    tbr_tally = openmc.Tally(name="TBR")
    tbr_tally.filters = [cell_filter]
    tbr_tally.scores = ["(n,Xt)"]  # tritium production
    tbr_tally.nuclides = ["Li6", "Li7"]

    tallies = openmc.Tallies([tbr_tally])

    return openmc.Model(geometry=geometry, materials=materials,
                        settings=settings, tallies=tallies)


if __name__ == "__main__":
    model = build_model()
    model.export_to_xml()
    print("Liquid breeder blanket model exported")
