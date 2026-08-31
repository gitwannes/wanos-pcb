<!-- --- file: docs/todo/phaseR-requirements.md -->

# WanOS PCB Phase R — Requirements / architecture

**wanos-pcb-v1** — spec locks, external plant, field wiring, migration reference. **No schematic until R2 closes.**

**Status:** **R1** + **R2** open.

**Related:** [`board-spec.md`](../board-spec.md) · [`gpio-interface.md`](../gpio-interface.md) · [`io-expander-map.md`](../io-expander-map.md) · [`projects/wanos-board/components.xlsx`](../../projects/wanos-board/components.xlsx) · Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **R1** | Resolve spec + BOM contradictions | **open** |
| **R2** | Architecture + external plant + field wiring + mechanical | **open** (after R1) |

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

## R1 — Resolve contradictions (blocking)

**Must close before R2 kickoff.**

### 12 V monitor pin (safety-critical)

- One expander pin, one net — not “kWh aux OR 12 V” on Expander A P7.
- **R1 lock:** 12 V opto → **Expander B P6** (recommended) or Pi GPIO; drop second kWh **or** add capacity.

### Connectors vs `components.xlsx`

| Issue | Current BOM | Required fix |
|---|---|---|
| Sauna buttons | J6 = 3-pin | **4-pin** (3 signals + GND) |
| Door sensors | J2 = single 2-pin | **Two doors** → 2×2-pin or 1×4-pin |
| LCD modules | Not in xlsx | **2× dedicated I²C LCD** JST headers |
| I²C pull-ups | R9–R16 = 8× 4k7 | Segment diagram — which bus each pair serves |

### Four SHT31s / one PCA9615

- **R1 decision:** mux (e.g. TCA9548A), multiple plant connectors, or defer.

### Net list cleanup

- Align [`io-expander-map.md`](../io-expander-map.md); remove ambiguous `EXP_A_P7_KWH_AUX_OR_12V_MON` once resolved.

### R1 DoD

- [ ] Locks in [`board-spec.md`](../board-spec.md) + [`io-expander-map.md`](../io-expander-map.md)
- [ ] [`components.xlsx`](../../projects/wanos-board/components.xlsx) updated
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## R2 — wanos-pcb-v1 architecture lock

**Prereq:** R1 closed.

### Scope lock

| Term | Meaning |
|---|---|
| **WISC** | Current production board (not in this repo) |
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

Target product docs (create at R2 close-out):

| Topic | Planned doc |
|---|---|
| External DIN SSR modules, coil voltage, JST → SSR wiring | `docs/external-plant.md` |
| JST pinouts, wire gauge, max cable length (pulses, SHT31 plant) | `docs/field-wiring.md` |
| Pi GND, field GND, 12 V return, SSR return | `docs/grounding.md` (or § in field-wiring) |

**External 12 V safety chain:** document how site temp safety **cuts 12 V** and how opto on wanos-pcb-v1 detects loss (hard-lock story with WanOS).

### Field / migration

- [ ] Reuse vs replace WISC harnesses (needs WISC reference — pipeline Manual **Info — WISC**)
- [ ] Sauna cabinet environment (humidity, temperature at PCB)
- [ ] EN 60335-2-53: list assumptions; hardware thermal cutoff remains operator responsibility

### Reference material (pre-S1)

- [ ] **Datasheet pack** in `projects/wanos-board/datasheets/` (PCA9554, PCA9615, SHT31, PC817, PN2222, Molex HDMI, SMBJ12A)
- [ ] WISC site photos / as-built (pipeline Manual)

### R2 DoD

- [ ] [`design.yaml`](../../projects/wanos-board/design.yaml) + [`constraints.md`](../../projects/wanos-board/constraints.md) match locks
- [ ] [`gpio-interface.md`](../gpio-interface.md) — locked connector + BCM tables
- [ ] `docs/external-plant.md`, `docs/field-wiring.md` (and grounding) published or explicitly deferred with rationale
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Info — WISC migration reference (not a delivery phase)

**Pipeline:** Manual **Info — WISC board reference upload**.

### Operator request (verbatim, 2026-08-31)

> I'll add/upload (later) the current WISC board layout which wanos uses today - goal here being to migrate from the current wanos & wisc board to the new wanos with the wanos pcb (which version of wanos this will be I can't say)

### When uploaded

- **Home:** `docs/reference/wisc-board/`
- **Feeds:** R2 harness parity, **V1a**, cutover runbook ([`phaseV-verify.md`](phaseV-verify.md) § Cutover)

### Open

- Target **WanOS** version for **V1b** — main repo decision
- Cutover strategy — after WISC reference available

---

## Out of scope (R track)

- WanOS application **implementation** (main repo — tracked under **V1b**)
- CE / formal compliance sign-off unless later triaged
