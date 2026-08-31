<!-- --- file: docs/todo/phaseR-requirements.md -->

# WanOS PCB Phase R — Requirements / architecture

Board role, Pi platform, connectors, and safety/isolation strategy. **No schematic until R1 kickoff closes.**

**Status:** **R1** open — kickoff not started.

**Related:** Product home → [`board-overview.md`](../board-overview.md), [`gpio-interface.md`](../gpio-interface.md). Software map → [wanos `config_hardware.yaml`](https://github.com/gitwannes/wanos/blob/main/config_hardware.yaml). Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **R1** | Architecture kickoff — Pi model, form factor, blocks, connectors, isolation | **open** |

---

## R1 — Board architecture kickoff

### Operator request (verbatim, 2026-08-31)

> new repo  
> goal = PCB creation (no code) for the WanOS electronics board  
> Kicad files / all that is needed to send to JLCPCB  
> create same docs & todo / MD structure

### Verified facts (from WanOS software)

* GPIO inputs: kWh + two water pulses + two doors — see [`gpio-interface.md`](../gpio-interface.md).
* GPIO outputs: one safety line + IR + three sauna phases — software PWM at ~5 Hz on phases.
* Four SHT11 sensors on dedicated D/C pin pairs; 5 V bit-bang reads.
* Boot must clamp all SSR outputs OFF before WanOS arms (`hardware/actuators.py` sanitization).
* Main repo: https://github.com/gitwannes/wanos

### Open questions (must lock at kickoff)

1. **Pi platform** — Pi 4 vs Pi 5 vs CM? Header-only HAT or panel/DIN mount?
2. **SSR interface** — onboard SSRs vs screw terminals to external DIN SSRs? Coil/logic voltage?
3. **Input conditioning** — opto per input? debounce RC? TVS rating for field cables?
4. **Connectors** — terminal blocks vs pluggable headers per zone (pulse / doors / SHT11 / SSR)?
5. **Power** — Pi powered separately only, or also 5 V / 12 V field rails on-board?
6. **Layers / size** — default 2-layer; max board outline?
7. **Fab** — bare PCB only vs JLCPCB SMT assembly for which parts?
8. **LCD / I2C** — stay on separate LCD Pi (WanOS L2) or reserve footprint on this board?

### Delivery locks (empty until kickoff)

*(To be filled when operator confirms R1.)*

### R1 DoD (stub)

- [ ] All open questions above answered and locked in this section
- [ ] `design.yaml` updated with rails, blocks, board size
- [ ] `gpio-interface.md` updated if connector pinout differs from raw BCM map
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Out of scope (R track)

- WanOS application code changes (separate repo / phase there)
- CE / legal compliance sign-off (operator responsibility unless later triaged)
