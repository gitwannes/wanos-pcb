<!-- --- file: docs/jlcpcb-ordering.md -->

# JLCPCB ordering checklist

How to produce and upload fabrication files for the WanOS board. Exact filenames follow the KiCad project name once **S1/L1** create `wanos-board.kicad_pro`.

---

## Before export

- [ ] Schematic **ERC** clean (or documented waivers in phase file)
- [ ] PCB **DRC** clean (or documented waivers)
- [ ] Board thickness, copper weight, and surface finish locked in phase **J1**
- [ ] All LCSC C-numbers assigned for SMT parts (if using JLC assembly)

---

## Generate from KiCad

Use **Fabrication Outputs** (KiCad 8+) or `kicad-cli`:

```powershell
# Example — adjust paths after project exists
$cli = "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"
$proj = "projects/wanos-board/wanos-board"

& $cli pcb export gerbers --output "projects/wanos-board/fabrication/" "$proj.kicad_pcb"
& $cli pcb export drill --format gerber --output "projects/wanos-board/fabrication/" "$proj.kicad_pcb"
& $cli pcb export pos --format csv --units mm --side front --output "projects/wanos-board/fabrication/" "$proj.kicad_pcb"
& $cli sch export bom --output "projects/wanos-board/fabrication/bom.csv" "$proj.kicad_sch"
```

Copy outputs into `projects/wanos-board/fabrication/` (see [`fabrication/README.md`](../projects/wanos-board/fabrication/README.md)).

---

## Upload bundle

| JLCPCB step | Files |
|---|---|
| **Gerber** | Zip all `.gbr` / `.gbrjob` + drill (`.drl` or embedded) |
| **PCB order** | Layer count, dimensions, qty, color, surface finish |
| **SMT assembly** (optional) | `bom.csv` + centroid `.csv` / `.pos`; confirm LCSC parts |
| **Stencil** (if hand-soldering SMT) | Paste gerber or order stencil separately |

Recommended zip layout:

```text
wanos-board-gerbers.zip
  wanos-board-F_Cu.gbr
  wanos-board-B_Cu.gbr
  ...
  wanos-board.drl
```

---

## Default fab notes (confirm at J1)

| Parameter | Starter default | Lock at |
|---|---|---|
| Layers | 2 | J1 |
| PCB thickness | 1.6 mm | J1 |
| Copper | 1 oz | J1 |
| Surface finish | HASL (lead-free) or ENIG | J1 |
| Min track / space | Match `constraints.md` | L1 |

---

## After order

- Record JLCPCB order id + date in phase **J1** when shipped
- On receipt, run phase **V1** bring-up before closing **J1**
