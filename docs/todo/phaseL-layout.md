<!-- --- file: docs/todo/phaseL-layout.md -->

# WanOS PCB Phase L — Layout

Footprint placement, routing, pours, and DRC for the WanOS carrier board.

**Status:** **L1** open — blocked on **S1**.

**Related:** Constraints → [`projects/wanos-board/constraints.md`](../../projects/wanos-board/constraints.md). Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **L1** | Placement, routing, DRC clean | **open** (after S1) |

---

## L1 — PCB layout

### Prereqs

- **S1** closed — schematic ERC clean and footprints assigned

### Scope (stub — refine at L1 kickoff)

- 2-layer default unless **R1** locked more
- Pi keep-out and mounting holes
- Clearance for SSR / mains field wiring (even if SSRs are off-board)
- Test points for safety line and one pulse input (TBD at kickoff)

### L1 DoD (stub)

- [ ] `wanos-board.kicad_pcb` complete
- [ ] DRC pass or waivers documented
- [ ] 3D view checked for Pi header clearance
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Out of scope (L track)

- Fab file zip (**J1**)
- Pi soak test (**V1**)
