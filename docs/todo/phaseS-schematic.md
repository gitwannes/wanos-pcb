<!-- --- file: docs/todo/phaseS-schematic.md -->

# WanOS PCB Phase S — Schematic

Hierarchical schematic, net naming, ERC, and BOM seed for the WanOS carrier board.

**Status:** **S1** open — blocked on **R1** kickoff.

**Related:** Constraints → [`projects/wanos-board/constraints.md`](../../projects/wanos-board/constraints.md). Intent → [`design.yaml`](../../projects/wanos-board/design.yaml). Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **S1** | Full schematic + ERC clean + initial BOM | **open** (after R1) |

---

## S1 — Schematic

### Prereqs

- **R1** closed — architecture and connector strategy locked
- KiCad project created under `projects/wanos-board/`

### Scope (stub — refine at S1 kickoff)

- Sheets or blocks per [`design.yaml`](../../projects/wanos-board/design.yaml)
- Net names per [`constraints.md`](../../projects/wanos-board/constraints.md)
- Every GPIO in [`gpio-interface.md`](../gpio-interface.md) reaches a named net + connector
- Power-up defaults: SSR outputs high-Z or LOW through hardware where required

### S1 DoD (stub)

- [ ] `wanos-board.kicad_sch` (+ project) in repo
- [ ] ERC pass or waivers documented
- [ ] `bom-targets.yaml` populated for fab-relevant parts
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Out of scope (S track)

- PCB placement and routing (**L1**)
- Gerber export (**J1**)
