<!-- --- file: docs/todo/phaseJ-jlcpcb.md -->

# WanOS PCB Phase J — JLCPCB fabrication pack

Gerber, drill, BOM, CPL, and order for **wanos-pcb-v1**.

**Status:** **J1** open — blocked on **Ops2**.

**Related:** [`jlcpcb-ordering.md`](../jlcpcb-ordering.md) · [`component-selection.md`](../component-selection.md) · [`projects/wanos-board/components.xlsx`](../../projects/wanos-board/components.xlsx) · [`fabrication/JLCPCB_BOM_Template.xls`](../../projects/wanos-board/fabrication/JLCPCB_BOM_Template.xls) · Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **J1** | Export, validate LCSC, place order | **open** (after Ops2) |

---

## Ops2 — Pre-J1 fab readiness (Sequence #8)

**Prereq:** **Gate-L1** closed. Detail in pipeline Manual § Ops2.

### Decisions (lock before export)

| Topic | Options / notes |
|---|---|
| Prototype qty | Record in order notes |
| Board ID | `wanos-pcb-v1.0` (or operator lock) on silk + JLC comment |
| SMT assembly | Which refs JLC assembles vs bench hand-solder (J40, JST, terminals) |
| Stencil | Required for SMT prototype? |
| Stackup | 2-layer 1.6 mm ENIG per [`board-spec.md`](../board-spec.md) § 8 |

### Ops2 DoD

- [ ] Assembly split documented in this section
- [ ] Operator go to proceed to **J1** export

---

## J1 — Fabrication pack

### Prereqs

- **Ops2** closed

### KiCad / Konnect export (implement phase)

| Output | Tool |
|---|---|
| Gerber + drill zip | Konnect fab pipeline and/or `kicad-cli pcb export gerbers` |
| `bom.csv` | Konnect / `kicad-cli sch export bom` — LCSC column |
| Centroid CPL | Konnect / `kicad-cli pcb export pos` |
| Optional PDF | Assembly + schematic for bench |

Destination: `projects/wanos-board/fabrication/`

### LCSC validation

- [ ] Every SMT line in `components.xlsx` — C-number in stock at JLC
- [ ] Substitutes noted if any part obsolete

### J1 DoD

- [ ] Gerber zip spot-checked (Gerber viewer)
- [ ] JLCPCB order placed — record order id, qty, date here
- [ ] **Spare parts bag** list (pipeline Manual) if applicable
- [ ] Ready for **Ops3** receiving
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Out of scope

- Board power-on (**V1a** — after **Ops3**)
