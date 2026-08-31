<!-- --- file: docs/todo/phaseS-schematic.md -->

# WanOS PCB Phase S — Schematic (+ KiCad project)

KiCad schematic and project for **wanos-pcb-v1**. ERC clean before **Gate-S1** and **L1**.

**Status:** **S1** open — blocked on **R2**.

**Related:** [`board-spec.md`](../board-spec.md) · [`io-expander-map.md`](../io-expander-map.md) · [`hdmi-spi-eink.md`](../hdmi-spi-eink.md) · [`component-selection.md`](../component-selection.md) · [`projects/wanos-board/components.xlsx`](../../projects/wanos-board/components.xlsx) · [`kicad-setup.md`](../kicad-setup.md) · Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **S1** | KiCad project + schematic + ERC | **open** (after R2) |

---

## S1 — KiCad schematic wanos-pcb-v1

### Prereqs

- **R1** + **R2** closed
- **Ops1** Konnect + KiCad 10 usable ([`kicad-setup.md`](../kicad-setup.md))
- Datasheet pack in `projects/wanos-board/datasheets/` (pipeline Manual)

### KiCad deliverables (implement phase)

| Artifact | Action |
|---|---|
| `wanos-board.kicad_pro` | Create project; link to `design.yaml` revision **wanos-pcb-v1** |
| `wanos-board.kicad_sch` | Root + hierarchical sheets (see below) |
| Symbol libraries | JLC/LCSC symbols for U1–U4, Q1–Q4, J1, passives — validate footprints vs [`components.xlsx`](../../projects/wanos-board/components.xlsx) |
| `bom-targets.yaml` | Sync key parts from xlsx |

### Target schematic sheets

| Sheet | Source |
|---|---|
| `Pi_Power` | Pi header J40, optional J41, 5 V ferrite FB1 |
| `IO_Expanders` | [`io-expander-map.md`](../io-expander-map.md) |
| `SSR_Drivers` | Pi GPIO → R/Q → J8; 12 V rail ref |
| `Safety_12V_Mon` | U4 opto, R32, R33, C17 |
| `HDMI_SPI` | J1 — [`hdmi-spi-eink.md`](../hdmi-spi-eink.md) |
| `Connectors` | J2–J7 field JST (+ LCD JSTs from R1) |
| `LEDs` | Activity + status |

Use Konnect schematic tools and/or manual KiCad; **ERC** via `kicad-cli` or Konnect.

### Pre-ERC checklist

- [ ] Connector pin counts match **R1** locks
- [ ] 12 V opto on single locked expander pin
- [ ] 8× 4k7 pull-ups allocated per I²C segment diagram
- [ ] Four SSR strings + Pi GPIO net names match **R2** BCM table
- [ ] PCA9554 A0–A2 tied; unique I²C addresses
- [ ] HDMI nets named per hdmi-spi-eink doc

### S1 DoD

- [ ] `wanos-board.kicad_sch` + `.kicad_pro` in repo
- [ ] ERC pass or waivers recorded here
- [ ] Ready for **Gate-S1** operator sign-off (pipeline Sequence #5)
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Gate-S1 — Operator schematic sign-off

**Pipeline Sequence #5** (not a letter subphase). **Prereq:** S1 ERC clean.

- [ ] Operator reviews schematic PDF (or KiCad) — connector orientation, SSR path, 12 V opto, net names
- [ ] Sign-off recorded (date + name) in this section before **L1** starts

---

## Out of scope

- PCB placement (**L1**)
- Gerber export (**J1**)
