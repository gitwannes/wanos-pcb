<!-- --- file: docs/todo/phaseL-layout.md -->

# WanOS PCB Phase L — Layout

PCB layout for **wanos-pcb-v1** (85 × 56 mm). DRC clean before **Gate-L1** and **Ops2**.

**Status:** **L1** open — blocked on **Gate-S1**.

**Related:** [`board-spec.md`](../board-spec.md) § 7 · [`constraints.md`](../../projects/wanos-board/constraints.md) · Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **L1** | Placement, routing, DRC, silkscreen | **open** (after Gate-S1) |
| **L2** | Pi-power high-current layout (manual) | **open** (during / after L1) |

---

## L2 — Pi-power high-current layout (manual)

**From schematic (pi_power):** **Q6** `AO3401A` is the 5 V ideal diode — **full Pi load** flows **F1 → Q6 → +5VA → FB1 → J40**.

### Operator manual check (before Gate-L1)

- [ ] **Q6 trace width / copper** sized for **≥ 3 A** peak (Pi 4 + peripherals), short path **F1 → Q6 → +5VA**
- [ ] **F1 → Q6** and **Q6 → bulk (`C1`) / `FB1`** kept tight; avoid thin necks or long detours
- [ ] **Thermal:** Q6 `Rds(on)` × I² — verify pad/via strategy if the FET runs warm under load
- [ ] **Silk / assy note** near **Q6** optional: “5 V ideal diode — high current”

**Agent reminder:** flag **L2** whenever routing pi-power or reviewing layout DRC.

---

## L1 — Layout

### Prereqs

- **Gate-S1** closed
- Footprints assigned in schematic

### KiCad deliverables (implement phase)

| Task | Notes |
|---|---|
| `wanos-board.kicad_pcb` | Board outline 85×56 mm; MH1–MH4 |
| Zone placement | [`board-spec.md`](../board-spec.md) § 7 — Pi left, logic top, field right, SSR bottom |
| Route | Lock **HDMI/SPI** first; Freerouting/Konnect for other nets |
| DRC | Rules per [`board-spec.md`](../board-spec.md) § 8.2 |
| 3D | Pi header + HDMI clearance check |
| **Silkscreen** | Label all JST (J2=…); **`wanos-pcb-v1`** + rev; pin-1 marks; polarity |

### Layout checklist

- [ ] **L2:** **Q6** carries full Pi current — see [§ L2](#l2--pi-power-high-current-layout-manual)
- [ ] SSR / 12 V area isolated from I²C ([`board-spec.md`](../board-spec.md) § 6)
- [ ] Decoupling at each PCA9554 / TCA9548A
- [ ] Test pads TP1–TP10 accessible
- [ ] Copper pour / grounding per [`grounding.md`](../grounding.md)
- [ ] Assembly drawing notes for hand-solder TH parts (JST, terminals, J40)

### L1 DoD

- [ ] DRC pass or waivers documented
- [ ] Silkscreen reviewed for installer clarity
- [ ] Ready for **Gate-L1** (Sequence #7)
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Gate-L1 — Operator layout sign-off

**Pipeline Sequence #7**. **Prereq:** L1 DRC clean.

- [ ] Operator reviews layout PDF + 3D — zones, connector access, silk labels
- [ ] Sign-off recorded here before **Ops2** / **J1**

---

## Out of scope

- Fab order (**J1**)
- Power-on test (**V1a**)
