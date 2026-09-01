# WanOS PCB — Implementation pipeline

Ordered backlog + closed history. Specs / DoD / locks live in the lettered phase files — not here.

**Last updated:** 2026-08-31 (full triage — gates, ops, KiCad, migration)

---

## How to use

| Band | Meaning |
|---|---|
| **Done** | Closed (shipped or cancelled) — archive only |
| **Sequence** | All open work, in order. Status: **open** \| **coding** \| **hold** |
| **Ops** | Operator / fab / non-lettered leftovers |

**Status:** `open` = eligible · `coding` = actively being implemented right now · `hold` = parked (prereq, assess-only, or pause).

**Size:** `low` · `mid` · `high` (delivery weight, not calendar days).

**Detail files:**

| Letter | Affinity | File |
|---|---|---|
| **R** | Requirements / architecture | [`phaseR-requirements.md`](phaseR-requirements.md) |
| **S** | Schematic (+ KiCad project) | [`phaseS-schematic.md`](phaseS-schematic.md) |
| **L** | Layout | [`phaseL-layout.md`](phaseL-layout.md) |
| **J** | JLCPCB fabrication pack | [`phaseJ-jlcpcb.md`](phaseJ-jlcpcb.md) |
| **V** | Verification / bring-up | [`phaseV-verify.md`](phaseV-verify.md) |

**Product reference** → `docs/` outside `todo/` — [`board-spec.md`](../board-spec.md) (**wanos-pcb-v1**).

**DoD (every phase):** Last step = audit & update all `docs/**/*.md` (+ root README) against shipped artifacts.

When a phase finishes: Sequence → **Done**; trim Sequence only.

---

## Done

| Phase | Notes |
|---|---|
| **Triage** | Input docs promoted **2026-08-31** |
| **Triage** | Full backlog (gates, ops, KiCad, migration) **2026-08-31** |
| **R1** | Spec + BOM contradictions locked **2026-09-01** — [`field-wiring.md`](../field-wiring.md), [`phaseR-requirements.md`](phaseR-requirements.md) § R1 |

---

## Sequence

All open items. **Detail** = phase file section.

```text
#   Status Size Id           What                                               Detail
──  ────── ──── ──────────── ────────────────────────────────────────────────── ──────────────────────────
1   open   high R2           wanos-pcb-v1 architecture + plant + field wiring   phaseR § R2
2   open   mid  Ops1          Konnect + KiCad 10 + Cursor on build machine       pipeline Manual § Ops1
3   open   high S1            KiCad schematic wanos-pcb-v1 (ERC clean)           phaseS § S1
4   open   low  Gate-S1       Operator schematic sign-off (PDF / review)         pipeline Manual § Gate-S1
5   open   high L1            PCB layout 85×56 mm (DRC clean)                    phaseL § L1
6   open   low  Gate-L1       Operator layout sign-off + silkscreen review       pipeline Manual § Gate-L1
7   open   mid  Ops2           Pre-J1 fab readiness (assembly split, qty, stencil) pipeline Manual § Ops2
8   open   mid  J1            JLCPCB export + order + LCSC validate              phaseJ § J1
9   open   low  Ops3           Receiving + first-article inspection               pipeline Manual § Ops3
10  open   mid  V1a           Bring-up: current WanOS / WISC-equivalent subset   phaseV § V1a
11  hold   mid  V1b           Full wanos-pcb-v1 + future WanOS code              phaseV § V1b
```

Near-term: **R2** → **Ops1** ∥ **S1** (after R2) → gates → **J1** → **V1a**. Production WanOS stays on **WISC** until **V1a** go.

---

## Manual checks

### Reference & migration (info)

| Item | Status | Notes |
|---|---|---|
| **Info — WISC board reference upload** | Done | KiCad under [`reference/wisc-board/`](../reference/wisc-board/) |
| **Info — WISC site photos / as-built** | open | Photos of WISC install, SSR cabinet, 12 V safety wiring; complements WISC KiCad |
| **WanOS on WISC (production)** | open | [wanos](https://github.com/gitwannes/wanos); not blocked by this repo |
| **Future WanOS ↔ full board (code)** | hold | Main repo: expanders, SHT31, `config_hardware.yaml` — **V1b**; version TBD |
| **Cutover runbook** | open | WISC out → wanos-pcb-v1 in; rollback; downtime — [`phaseV-verify.md`](phaseV-verify.md) § Cutover |

### Requirements & docs (R / pre-S1)

| Item | Status | Notes |
|---|---|---|
| **External SSR + 12 V plant model** | open | Off-board DIN SSRs, coil V, ext. temp safety that cuts 12 V — [`phaseR-requirements.md`](phaseR-requirements.md) § R2 |
| **Field harness pinouts** | Done | [`field-wiring.md`](../field-wiring.md) (R1); grounding still R2 |
| **Grounding / return scheme** | open | Pi GND, field GND, 12 V return, SSR return — R2 → product doc |
| **Reuse vs new WISC field cables** | open | After WISC reference upload |
| **Pi + enclosure mechanical** | open | Standoffs, height, HDMI bend, cutouts — R2 |
| **Datasheet pack** | open | PCA9554, TCA9546A, SHT31, PC817, PN2222, Molex HDMI, TVS → `projects/wanos-board/datasheets/` |
| **EN 60335-2-53 assumptions** | hold | Spec cites sauna context; formal safety case = operator |
| **Sauna environment** | open | Humidity, temp at board, cable routing — R2 note |
| **CE / product marking** | hold | Only if scoped later |

### Design gates

| Item | Status | Notes |
|---|---|---|
| **Gate-S1 — schematic sign-off** | open | Sequence #5; operator review before **L1** |
| **Gate-L1 — layout sign-off** | open | Sequence #7; connector orientation, zones, **`wanos-pcb-v1` rev on silk** |
| **HDMI→SPI physical verification** | open | Cable + WISC panel before relying on e-ink — [`hdmi-spi-eink.md`](../hdmi-spi-eink.md); before **V1a** e-ink test |
| **Silkscreen / assembly drawing** | open | Label every JST; polarity; installer hints — **L1** / **Ops2** |

### Tooling (Ops1)

| Item | Status | Notes |
|---|---|---|
| **Ops1 — Konnect + KiCad + Cursor** | open | [`kicad-setup.md`](../kicad-setup.md); [Konnect](https://github.com/mixelpixx/Konnect) |

### Fab & order (Ops2 / J1)

| Item | Status | Notes |
|---|---|---|
| **Ops2 — pre-J1 fab readiness** | open | Sequence #8; SMT vs hand (JST, terminals, Pi header), prototype qty, stencil |
| **LCSC stock validation** | hold | `components.xlsx` C-numbers at **J1** |
| **Prototype revision ID** | open | e.g. `wanos-pcb-v1.0` on silk + order notes |
| **Spare parts bag** | open | Extra JST, terminals, LEDs — after first order |

### Receive & bring-up (Ops3 / V1)

| Item | Status | Notes |
|---|---|---|
| **Ops3 — receiving inspection** | open | Sequence #10; visual, dimensions, critical footprints before power-on |
| **V1a paper test checklist** | open | [`phaseV-verify.md`](phaseV-verify.md) § V1a |
| **12 V loss / hard-lock test** | open | Opto + WanOS behaviour — **V1a** |
| **Errata log** | open | Green-wire / bodge notes — **V1a** |
| **Installer / electrician one-pager** | open | Field connections; no mains on PCB — **V1a** close-out |

---

## Changelog

| Date | Change |
|---|---|
| 2026-08-31 | Full triage: Sequence gates Ops2/3, Manual backlog, KiCad/code pointers |
| 2026-08-31 | Info: WISC board reference upload |
| 2026-08-31 | Input docs promoted; Sequence R1–V1b |
| 2026-09-01 | R1 Done; WISC KiCad → `reference/wisc-board/`; field-wiring + silkscreen docs |
