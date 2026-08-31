<!-- --- file: docs/todo/phaseJ-jlcpcb.md -->

# WanOS PCB Phase J — JLCPCB fabrication pack

Gerber, drill, BOM, and centroid exports plus order record for JLCPCB.

**Status:** **J1** open — blocked on **L1**.

**Related:** Checklist → [`jlcpcb-ordering.md`](../jlcpcb-ordering.md). Output dir → [`projects/wanos-board/fabrication/`](../../projects/wanos-board/fabrication/). Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **J1** | Export + zip + JLCPCB order parameters | **open** (after L1) |

---

## J1 — Fabrication pack

### Prereqs

- **L1** closed — DRC clean

### Scope (stub — refine at J1 kickoff)

- Export all layers + drill to `fabrication/`
- BOM CSV (+ LCSC columns if SMT)
- Centroid / CPL for assembly side
- Zip per [`jlcpcb-ordering.md`](../jlcpcb-ordering.md)
- Record order id, qty, lead time, and stackup choices in this section

### J1 DoD (stub)

- [ ] `fabrication/` contains reproducible export set (or script path documented)
- [ ] Gerber zip verified (Gerber viewer spot-check)
- [ ] JLCPCB order placed (or operator confirms manual order)
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Out of scope (J track)

- Functional Pi test (**V1**)
