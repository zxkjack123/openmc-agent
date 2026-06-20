#!/usr/bin/env python3
"""GODIVA bare sphere — ICSBEP HEU-MET-FAST-001 benchmark model."""
import openmc


def build_model() -> openmc.Model:
    """Build GODIVA bare sphere model and return it.

    Returns:
        openmc.Model: Configured GODIVA eigenvalue model.
    """
    # Material: HEU (3-isotope approximation)
    heu = openmc.Material(name="HEU")
    heu.set_density("g/cm3", 18.74)
    heu.add_nuclide("U234", 1.02, "wo")
    heu.add_nuclide("U235", 93.71, "wo")
    heu.add_nuclide("U238", 5.27, "wo")

    # Geometry: bare sphere, vacuum boundary
    sphere = openmc.Sphere(r=8.7407, boundary_type="vacuum")
    cell = openmc.Cell(fill=heu, region=-sphere)
    root = openmc.Universe(cells=[cell])
    geometry = openmc.Geometry(root)

    # Settings: eigenvalue, 150 batches (50 inactive, 100 active)
    settings = openmc.Settings()
    settings.batches = 150
    settings.inactive = 50
    settings.particles = 10000
    settings.run_mode = "eigenvalue"
    source = openmc.IndependentSource(space=openmc.stats.Point())
    settings.source = source

    return openmc.Model(geometry=geometry, settings=settings)


if __name__ == "__main__":
    model = build_model()
    model.export_to_xml()
    print("GODIVA model exported: geometry.xml, materials.xml, settings.xml")
