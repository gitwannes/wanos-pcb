<!-- --- file: docs/todo/phaseR-requirements.md -->

# WanOS PCB Phase R — Requirements / architecture

**wanos-pcb-v1** — spec locks, external plant, field wiring, migration reference. **No schematic until R2 closes.**

**Status:** **R1 Done** (2026-09-01) · **R2** open.

**Related:** [`board-spec.md`](../board-spec.md) · [`field-wiring.md`](../field-wiring.md) · [`gpio-interface.md`](../gpio-interface.md) · [`io-expander-map.md`](../io-expander-map.md) · [`projects/wanos-board/components.xlsx`](../../projects/wanos-board/components.xlsx) · Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **R1** | Resolve spec + BOM contradictions | **Done** (2026-09-01) |
| **R2** | Architecture + external plant + field wiring + mechanical | **open** |

---

## R1 — Shipped summary (2026-09-01)

**Canonical detail:** [`board-spec.md`](../board-spec.md) · [`field-wiring.md`](../field-wiring.md) · [`io-expander-map.md`](../io-expander-map.md) · [`components.xlsx`](../../projects/wanos-board/components.xlsx).

| Topic | Lock |
|---|---|
| 12 V opto | **Expander B P6** (`EXP_B_P6_12V_MON`) |
| kWh aux | **Expander A P7** |
| Doors | **2× 2-pin** J2, J3 (pin1=GND, pin2=signal) |
| kWh | **2× 2-pin** J6, J7 |
| Buttons | **1× 4-pin** J8 straight; Cat5 → [`field-wiring.md`](../field-wiring.md) § 5 |
| LCD | **1× 4-pin** J16; both modules paralleled; **no 2nd header v1** |
| 4-pin I²C pinout | WISC **2.6.4 J7**: GND, SDA, SCL, 3V3 |
| SHT31 | **TCA9546A** U5 @ **0x70**; **4× 4-pin** J9–J12; all **`0x44`**; ~4–5 m Cat5 |
| PCA9615 | **Not used v1** |
| I²C pull-ups | **R9, R10 = 2k2** only |
| SSR | **J13** 5-pin vertical (WISC J1 parity) |
| Silkscreen font | [Printed Circuit Board 7](https://www.fontspace.com/printed-circuit-board-7-font-f15777) → [`reference/silkscreen/README.md`](../reference/silkscreen/README.md) |
| WISC KiCad home | [`reference/wisc-board/`](../reference/wisc-board/) (was `docs/wisc_boards/`) |

### R1 DoD

- [x] Locks in [`board-spec.md`](../board-spec.md) + [`io-expander-map.md`](../io-expander-map.md)
- [x] [`field-wiring.md`](../field-wiring.md) published
- [x] [`components.xlsx`](../../projects/wanos-board/components.xlsx) updated
- [x] Last DoD: all `docs/**/*.md` + README audited

---

## R2 — wanos-pcb-v1 architecture lock

**Prereq:** R1 closed.

### Scope lock

| Term | Meaning |
|---|---|
| **WISC** | Current production board (reference under [`reference/wisc-board/`](../reference/wisc-board/)) |
| **wanos-pcb-v1** | This repo board revision |
| **WISC-equivalent subset** | [`gpio-interface.md`](../gpio-interface.md) § WISC — **V1a** |
| **Future WanOS** | Full board software → **V1b** (main repo, version TBD) |

### On-board locks (kickoff)

1. Pi 4 vs 5; 85×56 mounting; MH1–MH4 standoffs; enclosure clearance
2. Pi **BCM** table: SSR (4× + safety), I²C, SPI/HDMI, optional INT from expanders
3. JLCPCB: bare PCB vs SMT scope (which refs hand-soldered)
4. Prototype revision label on silk (e.g. `wanos-pcb-v1.0`)
5. **V1a** adapter strategy vs WISC field wiring

### External plant (off-board — must document)

| Topic | Planned doc |
|---|---|
| External DIN SSR modules, coil voltage, JST → SSR wiring | `docs/external-plant.md` |
| Grounding, 12 V return, SSR return | `docs/grounding.md` (or § in field-wiring) |

**External 12 V safety chain:** document how site temp safety **cuts 12 V** and how opto detects loss (hard-lock with WanOS).

### Field / migration

- [ ] Reuse vs replace WISC harnesses — [`reference/wisc-board/`](../reference/wisc-board/)
- [ ] Sauna cabinet environment (humidity, temperature at PCB)
- [ ] EN 60335-2-53: list assumptions; hardware thermal cutoff remains operator responsibility

### Reference material (pre-S1)

- [ ] **Datasheet pack** in `projects/wanos-board/datasheets/` (PCA9554, TCA9546A, SHT31, PC817, PN2222, Molex HDMI, SMBJ12A)
- [ ] WISC site photos / as-built (pipeline Manual)

### R2 DoD

- [ ] [`design.yaml`](../../projects/wanos-board/design.yaml) + [`constraints.md`](../../projects/wanos-board/constraints.md) match locks
- [ ] [`gpio-interface.md`](../gpio-interface.md) — locked BCM tables
- [ ] `docs/external-plant.md`, grounding published or explicitly deferred with rationale
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Info — WISC migration reference

**Home:** [`docs/reference/wisc-board/`](../reference/wisc-board/) — summaries + read-only KiCad trees (`211201 wisc2-5-3/`, `220313 wisc2-6-4-HDMI/`).

Fab exports / cache → `_donotcommit/` (gitignored).

**Feeds:** R2 harness parity, **V1a**, cutover runbook ([`phaseV-verify.md`](phaseV-verify.md) § Cutover).

---

## Operator requests (verbatim)

**2026-08-31**

> new repo  
> goal = PCB creation (no code) for the WanOS electronics board  
> Kicad files / all that is needed to send to JLCPCB  
> create same docs & todo / MD structure

**2026-08-31**

> wanos-pcb-v1 is this board's revision … current wanos uses WISC boards … wanos does not do what this PCB is capable of — later version of wanos

**2026-08-31**

> also triage as info item: I'll add/upload (later) the current WISC board layout … migrate from the current wanos & wisc board to the new wanos with the wanos pcb

**2026-08-31**

> put all in triage (and add kicad & code items as well if there are any): full go

---

## Out of scope (R track)

- WanOS application **implementation** (main repo — **V1b**)
- CE / formal compliance sign-off unless later triaged
