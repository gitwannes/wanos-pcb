<!-- --- file: docs/todo/phaseR-requirements.md -->

# WanOS PCB Phase R — Requirements / architecture

**wanos-pcb-v1** — spec locks, external plant, field wiring, migration reference.

**Status:** **R1 Done** (2026-09-01) · **R2 Done** (2026-09-01).

**Related:** [`board-spec.md`](../board-spec.md) · [`field-wiring.md`](../field-wiring.md) · [`gpio-interface.md`](../gpio-interface.md) · [`external-plant.md`](../external-plant.md) · [`grounding.md`](../grounding.md) · Sequence → [`pipeline.md`](../pipeline.md) (archived).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **R1** | Resolve spec + BOM contradictions | **Done** (2026-09-01) |
| **R2** | Architecture + external plant + field wiring + mechanical | **Done** (2026-09-01) |

---

## R1 — Shipped summary (2026-09-01)

**Canonical detail:** [`board-spec.md`](../board-spec.md) · [`field-wiring.md`](../field-wiring.md) · [`io-expander-map.md`](../io-expander-map.md).

| Topic | Lock |
|---|---|
| 12 V opto | **Expander B P6** (`EXP_B_P6_12V_MON`) |
| kWh aux | **Expander A P7** |
| Doors | **2× 2-pin** J2, J3 |
| kWh | **2× 2-pin** J6, J7 |
| Buttons | **1× 4-pin** J8; Cat5 → [`field-wiring.md`](../field-wiring.md) § 5 |
| LCD | **1× 4-pin** J16; paralleled; **no 2nd header v1** |
| 4-pin I²C pinout | WISC **2.6.4 J7** |
| SHT31 | **TCA9546A** @ **0x70**; **J9–J12**; **`0x44`**; ~4–5 m Cat5 |
| PCA9615 | **Not used v1** |
| I²C pull-ups | **R9, R10 = 2k2** |
| SSR field | **J13** 5-pin (WISC J1 parity) |
| Silkscreen font | [Printed Circuit Board 7](https://www.fontspace.com/printed-circuit-board-7-font-f15777) |

---

## R2 — Shipped summary (2026-09-01)

**Canonical detail:** [`board-spec.md`](../board-spec.md) · [`gpio-interface.md`](../gpio-interface.md) · [`hdmi-spi-eink.md`](../hdmi-spi-eink.md) · [`external-plant.md`](../external-plant.md) · [`grounding.md`](../grounding.md) · [`design.yaml`](../../projects/wanos-board/design.yaml).

| Topic | Lock |
|---|---|
| Pi | **Pi 4** (re-use production unit) |
| Mechanical | **85×56 mm**, **M2.5** holes — WISC **2.6.4** reference |
| Pi power | **J41** USB-C on PCB |
| 12 V | **J14** only (**J15** dropped); post-safety **+12VA** |
| HDMI J1 | Molex **208658-1052** (LCSC **C6990958**); pinout [`hdmi-spi-eink.md`](../hdmi-spi-eink.md) |
| Pi BCM | [`gpio-interface.md`](../gpio-interface.md) — SSR, I²C, e-ink SPI |
| I²C addr | U1 **`0x20`**, U2 **`0x21`**, U5 **`0x70`** |
| PCA9554 INT | **NC** v1 |
| External SSR | **4×** Omron **G3PJ-225B DC12-24** — [`external-plant.md`](../external-plant.md) |
| Temp safety | Independent; cuts **12 V** off-board |
| Grounding | [`grounding.md`](../grounding.md) |
| Software | **No adapter** — operator updates **wanos** when switching from WISC; **one Pi** |
| Silk | **`wanos-pcb-v1.0`** + Wannes logos; **no** CC BY-NC-SA |
| JLC | Full **PCBA** incl. **J40** |
| Datasheets | [`reference/datasheets/`](../reference/datasheets/README.md) — 12/13; `usb-c-j41.pdf` later |
| Harness | Reuse where pinout matches; SHT11→SHT31 tails re-wire |

### R2 DoD

- [x] [`design.yaml`](../../projects/wanos-board/design.yaml) + [`constraints.md`](../../projects/wanos-board/constraints.md) match locks
- [x] [`gpio-interface.md`](../gpio-interface.md) — locked BCM tables
- [x] [`external-plant.md`](../external-plant.md), [`grounding.md`](../grounding.md) published
- [x] Last DoD: all `docs/**/*.md` + README audited

---

## Info — WISC migration reference

**Home:** [`docs/reference/wisc-board/`](../reference/wisc-board/) — read-only KiCad + summaries. Feeds **V1a** cutover ([`phaseV-verify.md`](phaseV-verify.md)).

---

## Operator requests (verbatim)

**2026-08-31** — new repo; KiCad + JLCPCB; docs/todo structure; wanos-pcb-v1 vs WISC; full triage.

**2026-09-01** — R2 kickoff Q&A; drop **J15**; datasheet pack; close R2.

---

## Out of scope (R track)

- WanOS application **implementation** (main repo — **V1a** / **V1b**)
- CE / formal compliance sign-off unless later triaged
