<!-- --- file: docs/todo/phaseV-verify.md -->

# WanOS PCB Phase V — Verification / bring-up

Bench and on-Pi validation against WanOS `config_hardware.yaml` and safety behaviour.

**Status:** **V1** open — blocked on boards from **J1**.

**Related:** GPIO contract → [`gpio-interface.md`](../gpio-interface.md). Runtime → [wanos](https://github.com/gitwannes/wanos). Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **V1** | Bring-up + WanOS smoke | **open** (after J1 boards arrive) |

---

## V1 — Bring-up

### Prereqs

- Populated boards received from JLCPCB
- WanOS Pi available with current `config_hardware.yaml`

### Scope (stub — refine at V1 kickoff)

- Visual inspection, continuity on safety / SSR paths
- Pi boot: verify all SSR lines idle before WanOS arms
- Pulse input sanity (scope or meter simulator)
- One SHT11 header read in WanOS stub or live
- Document any **board errata** (wire mods, bodge) in this section

### V1 DoD (stub)

- [ ] Checklist executed and results recorded
- [ ] Errata (if any) documented; follow-up triaged to **S/L** or Ops
- [ ] Last DoD: all `docs/**/*.md` + README audited

---

## Out of scope (V track)

- WanOS feature work unrelated to this carrier
- Production quantity orders (operator Ops)
