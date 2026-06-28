#!/usr/bin/env python3
"""PWR pin-cell benchmark — UO2 fuel, Zircaloy cladding, water moderator."""
import openmc


def build_model() -> openmc.Model:
    """Build a standard PWR pin-cell model.

    Geometry:
        Fuel:  UO2, radius 0.4096 cm
        Gap:   He (void), radius 0.418 cm
        Clad:  Zircaloy-4, radius 0.475 cm
        Water: outside clad, square lattice pitch 1.26 cm

    All boundaries reflective (infinite lattice approximation).
    """
    # ── Materials ──
    uo2 = openmc.Material(name="UO2")
    uo2.set_density("g/cm3", 10.297)
    uo2.add_nuclide("U235", 0.033, "wo")
    uo2.add_nuclide("U238", 0.967, "wo")
    uo2.add_nuclide("O16", 2.0, "ao")

    helium = openmc.Material(name="He gap")
    helium.set_density("g/cm3", 0.001598)
    helium.add_nuclide("He4", 1.0, "ao")

    zircaloy = openmc.Material(name="Zircaloy-4")
    zircaloy.set_density("g/cm3", 6.56)
    zircaloy.add_nuclide("Zr90", 0.5145, "wo")
    zircaloy.add_nuclide("Zr91", 0.1122, "wo")
    zircaloy.add_nuclide("Zr92", 0.1715, "wo")
    zircaloy.add_nuclide("Zr94", 0.1738, "wo")
    zircaloy.add_nuclide("Zr96", 0.0280, "wo")

    water = openmc.Material(name="H2O moderator")
    water.set_density("g/cm3", 0.740)
    water.add_nuclide("H1", 2.0, "ao")
    water.add_nuclide("O16", 1.0, "ao")
    water.add_s_alpha_beta("c_H_in_H2O")

    materials = openmc.Materials([uo2, helium, zircaloy, water])

    # ── Geometry ──
    pitch = 1.26
    fuel_or = openmc.ZCylinder(r=0.4096)
    gap_or = openmc.ZCylinder(r=0.418)
    clad_or = openmc.ZCylinder(r=0.475)
    left = openmc.XPlane(x0=-pitch / 2, boundary_type="reflective")
    right = openmc.XPlane(x0=pitch / 2, boundary_type="reflective")
    bottom = openmc.YPlane(y0=-pitch / 2, boundary_type="reflective")
    top = openmc.YPlane(y0=pitch / 2, boundary_type="reflective")

    fuel_region = -fuel_or
    gap_region = +fuel_or & -gap_or
    clad_region = +gap_or & -clad_or
    water_region = +clad_or & +left & -right & +bottom & -top

    fuel_cell = openmc.Cell(fill=uo2, region=fuel_region, name="fuel")
    gap_cell = openmc.Cell(fill=helium, region=gap_region, name="gap")
    clad_cell = openmc.Cell(fill=zircaloy, region=clad_region, name="clad")
    water_cell = openmc.Cell(fill=water, region=water_region, name="water")

    root = openmc.Universe(cells=[fuel_cell, gap_cell, clad_cell, water_cell])
    geometry = openmc.Geometry(root)

    # ── Settings ──
    settings = openmc.Settings()
    settings.batches = 100
    settings.inactive = 30
    settings.particles = 10000
    settings.run_mode = "eigenvalue"
    settings.source = openmc.IndependentSource(
        space=openmc.stats.Box(
            (-pitch / 2, -pitch / 2, -1), (pitch / 2, pitch / 2, 1),
        ),
        constraints={"fissionable": True},
    )

    return openmc.Model(geometry=geometry, materials=materials, settings=settings)


if __name__ == "__main__":
    model = build_model()
    model.export_to_xml()
    print("PWR pin-cell model exported: geometry.xml, materials.xml, settings.xml")
