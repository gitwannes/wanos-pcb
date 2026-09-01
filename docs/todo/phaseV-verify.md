<!-- --- file: docs/todo/phaseV-verify.md -->

# WanOS PCB Phase V — Verification / bring-up

Bench validation, migration, and future full-board software integration.

**Status:** **V1a** open after **Ops3**; **V1b** hold.

**Related:** [`gpio-interface.md`](../gpio-interface.md) · [`hdmi-spi-eink.md`](../hdmi-spi-eink.md) · [`field-wiring.md`](../field-wiring.md) (R2) · [wanos](https://github.com/gitwannes/wanos) · Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **V1a** | wanos-pcb-v1 + **current WanOS** (WISC-equivalent subset) | **open** (after Ops3) |
| **V1b** | Full board + **future WanOS code** | **hold** |

---

## Ops3 — Receiving + first-article inspection (Sequence #10)

**Prereq:** **J1** boards shipped.

- [ ] Package intact; board rev matches order (`wanos-pcb-v1`)
- [ ] Measure outline ~85×56 mm; mounting holes
- [ ] Visual: solder, connector orientation, no swarf
- [ ] Spot-check critical footprints (J1 HDMI, J40, U4 opto, Q1–Q4)
- [ ] **Do not apply power** until **V1a** checklist started

Record results here (date).

---

## V1a — Current WanOS on wanos-pcb-v1

### Context

- Production: **WanOS + WISC** today.
- **V1a:** prove **wanos-pcb-v1** with **current WanOS** using **WISC-equivalent** logical map before production cutover.
- **HDMI→SPI:** complete physical verification ([`hdmi-spi-eink.md`](../hdmi-spi-eink.md)) before e-ink depends on this board.

### Prereqs

- **Ops3** passed
- **R2** V1a wiring / adapter documented
- [`external-plant.md`](../external-plant.md) / [`field-wiring.md`](../field-wiring.md) available for bench hookup

### Paper test checklist (no new WanOS code required for baseline)

| Step | Check |
|---|---|
| 1 | Visual + continuity (GND, no shorts on Pi 5V) |
| 2 | Pi boot with board seated; no smoke |
| 3 | SSR outputs idle before WanOS arms GPIO |
| 4 | 12 V present → opto state correct; **12 V removed** → detect + WanOS critical / lock (as wired today) |
| 5 | kWh pulse (pin 12 logical) |
| 6 | Water pulses + doors (WISC subset pins) |
| 7 | SHT11 paths as wired for V1a adapter |
| 8 | One SSR channel toggle (bench load — safe current) |
| 9 | Optional: WISC e-ink via HDMI after cable/panel verification |
| 10 | Log errata / bodges below |

### Deliverables (docs, not code)

- [ ] **`docs/installer-one-pager.md`** — field connections; external SSR; no mains on PCB
- [ ] **Errata log** (this section) — green wires, part subs
- [ ] Operator **go/no-go** to replace WISC in production

### V1a DoD

- [ ] Checklist complete; results recorded
- [ ] Cutover runbook draft updated (§ below)
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Cutover runbook (pipeline Manual)

**Target doc:** `docs/cutover-wisc-to-wanos-pcb-v1.md` (create at V1a close-out).

| Section | Content |
|---|---|
| Preconditions | V1a go, backup WISC board, WanOS version pinned |
| Downtime window | Operator defines |
| Steps | Power down → swap board → rewire per field-wiring → smoke test |
| Rollback | Reinstall WISC; restore prior wiring |
| Future | Full board features when **V1b** WanOS ships |

---

## V1b — Full wanos-pcb-v1 + future WanOS (hold)

**Blocked on WanOS software** in [gitwannes/wanos](https://github.com/gitwannes/wanos) (version **TBD**).

### WanOS code scope (main repo — not implemented here)

| Area | Work |
|---|---|
| I²C expanders | Driver for PCA9554 A/B — pulse, door, button inputs |
| SHT31 plant | TCA9546A mux + **J9–J12**; replace SHT11 bit-bang where deployed |
| Extra I/O | Bathroom 2 meters, 2× kWh, on-board I²C LCDs |
| 12 V hard-lock | Integrate expander opto net with sauna safety state machine |
| `config_hardware.yaml` | New schema for expander map vs raw BCM |

Triage future WanOS work in **wanos** pipeline when commanded — pointer only here.

### V1b DoD (stub)

- [ ] Full [`board-spec.md`](../board-spec.md) feature checklist on bench
- [ ] WanOS release noted with version id
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Out of scope

- WanOS **implementation** in this repo (**V1b** = main repo)
- WISC board repair
