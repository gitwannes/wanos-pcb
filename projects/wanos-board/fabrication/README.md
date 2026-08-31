<!-- --- file: projects/wanos-board/fabrication/README.md -->

# Fabrication outputs

Generated Gerber, drill, BOM, and centroid files for JLCPCB live here.

**Do not hand-edit** Gerbers — regenerate from KiCad per [`docs/jlcpcb-ordering.md`](../../../docs/jlcpcb-ordering.md).

| File pattern | Purpose |
|---|---|
| `*.gbr` / `*.gbrjob` | Copper, mask, silk, outline |
| `*.drl` | Drill hits |
| `bom.csv` | Bill of materials |
| `*.pos` / `*-pos.csv` | SMT centroid (CPL) |
| `wanos-board-gerbers.zip` | Upload bundle for PCB fab |

Binary outputs are gitignored; commit this README and any export scripts once **J1** defines the repeatable flow.
