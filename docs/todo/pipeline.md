<!-- --- file: docs/todo/pipeline.md -->

# WanOS PCB — Implementation pipeline

Ordered backlog + closed history. Specs / DoD / locks live in the lettered phase files — not here.

**Last updated:** 2026-09-21 (Gate-S1 Done; S archived; Ops-Remote1 next)

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
| **R** | Requirements / architecture | [`_archive/phaseR-requirements.md`](_archive/phaseR-requirements.md) (Done) |
| **S** | Schematic (+ KiCad project) | [`_archive/phaseS-schematic.md`](_archive/phaseS-schematic.md) (Done) |
| **L** | Layout | [`phaseL-layout.md`](phaseL-layout.md) |
| **J** | JLCPCB fabrication pack | [`phaseJ-jlcpcb.md`](phaseJ-jlcpcb.md) |
| **V** | Verification / bring-up | [`phaseV-verify.md`](phaseV-verify.md) |

**Product reference** → `docs/` outside `todo/` — [`board-spec.md`](../board-spec.md) (**wanos-pcb-v1**); remote → [`remotepcb.md`](../remotepcb.md).

**DoD (every phase):** Last step = audit & update all `docs/**/*.md` (+ root README) against shipped artifacts.

When a phase finishes: Sequence → **Done**; trim Sequence only. Fully Done letter tracks → `docs/todo/_archive/`.

---

## Done

| Phase | Notes |
|---|---|
| **Triage** | Input docs promoted **2026-08-31** |
| **Triage** | Full backlog (gates, ops, KiCad, migration) **2026-08-31** |
| **R1** | Spec + BOM contradictions locked **2026-09-01** |
| **R2** | Architecture + plant + BCM locked **2026-09-01** — [`_archive/phaseR-requirements.md`](_archive/phaseR-requirements.md) |
| **Ops1** | Konnect + KiCad 10 + Cursor **2026-09-01** — [`kicad-setup.md`](../kicad-setup.md) |
| **S1** | KiCad schematic **wanos-pcb-v1** ERC **0 errors** **2026-09-01** |
| **Gate-S1** | Operator schematic sign-off (Wannes) **2026-09-21** — [`schematic-signoff.md`](../schematic-signoff.md); S track → [`_archive/phaseS-schematic.md`](_archive/phaseS-schematic.md) |

---

## Sequence

All open items. **Detail** = phase file / Manual section.

```text
#   Status Size Id            What                                               Detail
──  ────── ──── ───────────── ────────────────────────────────────────────────── ──────────────────────────
1   open   mid  Ops-Remote1   Operator: clean wanos-remote schematic + check     pipeline Manual § Ops-Remote1
2   open   high L1            PCB layout 85x56 mm (DRC clean)                    phaseL § L1
3   open   low  Gate-L1       Operator layout sign-off + silkscreen review       pipeline Manual § Gate-L1
4   open   mid  Ops2          Pre-J1 fab readiness (assembly split, qty, stencil) pipeline Manual § Ops2
5   open   mid  J1            JLCPCB export + order + LCSC validate              phaseJ § J1
6   open   low  Ops3          Receiving + first-article inspection               pipeline Manual § Ops3
7   open   mid  V1a           Bring-up: wanos-pcb-v1 + updated WanOS             phaseV § V1a
8   hold   mid  V1b           Full board + future WanOS code                     phaseV § V1b
```

Near-term: **Ops-Remote1** (operator) → **L1** (main carrier) → gates → **J1** → **V1a**. Production WanOS stays on **WISC** until operator cuts over.

---

## Manual checks

### Ops-Remote1 — clean + check remote schematic (Sequence #1)

**Verbatim (2026-09-21):** next item on to-do list is for me/operator to clean the remote-PCB schematic, then to check that remote board

| Step | What |
|---|---|
| 1 | Open [`projects/wanos-remote/`](../../projects/wanos-remote/) in KiCad |
| 2 | Clean schematic (pin attachments, labels, layout on sheet) |
| 3 | Run ERC; fix or waive with notes |
| 4 | Check board vs [`remotepcb.md`](../remotepcb.md) locks |

**Canonical:** [`remotepcb.md`](../remotepcb.md) · project README [`projects/wanos-remote/README.md`](../../projects/wanos-remote/README.md).

### Reference & migration (info)

| Item | Status | Notes |
|---|---|---|
| **Info — WISC board reference upload** | Done | KiCad under [`reference/wisc-board/`](../reference/wisc-board/) |
| **Info — WISC site photos / as-built** | open | Photos of WISC install, SSR cabinet, 12 V safety wiring |
| **WanOS on WISC (production)** | open | [wanos](https://github.com/gitwannes/wanos); not blocked by this repo |
| **Future WanOS ↔ full board (code)** | hold | Main repo expanders / SHT31 — **V1b** |
| **Cutover runbook** | open | [`phaseV-verify.md`](phaseV-verify.md) § Cutover |

### Requirements & docs

| Item | Status | Notes |
|---|---|---|
| **External SSR + 12 V plant model** | Done | [`external-plant.md`](../external-plant.md) |
| **Field harness pinouts** | Done | [`field-wiring.md`](../field-wiring.md) |
| **Grounding / return scheme** | Done | [`grounding.md`](../grounding.md) |
| **Datasheet pack** | open | [`reference/datasheets/`](../reference/datasheets/README.md); `usb-c-j41.pdf` deferred |
| **EN 60335-2-53 assumptions** | hold | Formal safety case = operator |
| **CE / product marking** | hold | Only if scoped later |

### Design gates

| Item | Status | Notes |
|---|---|---|
| **Gate-S1 — schematic sign-off** | **Done** **2026-09-21** | [`schematic-signoff.md`](../schematic-signoff.md) |
| **Gate-L1 — layout sign-off** | open | After **L1** |
| **L2 — Q6 Pi high-current routing** | open | [`phaseL-layout.md`](phaseL-layout.md) § L2 |
| **HDMI→SPI physical verification** | open | Before **V1a** e-ink test |
| **Silkscreen / assembly drawing** | open | **L1** / **Ops2** |

### Tooling (Ops1)

| Item | Status | Notes |
|---|---|---|
| **Ops1 — Konnect + KiCad + Cursor** | **Done** | [`kicad-setup.md`](../kicad-setup.md) |

### Fab & order (Ops2 / J1)

| Item | Status | Notes |
|---|---|---|
| **Ops2 — pre-J1 fab readiness** | open | Sequence |
| **LCSC stock validation** | hold | At **J1** |
| **Prototype revision ID** | open | e.g. `wanos-pcb-v1.0` on silk |
| **Spare parts bag** | open | After first order |

### Receive & bring-up (Ops3 / V1)

| Item | Status | Notes |
|---|---|---|
| **Ops3 — receiving inspection** | open | Sequence |
| **V1a paper test checklist** | open | [`phaseV-verify.md`](phaseV-verify.md) |
| **12 V loss / hard-lock test** | open | **V1a** |
| **Errata log** | open | **V1a** |
| **Installer / electrician one-pager** | open | **V1a** close-out |

---

## Changelog

| Date | Change |
|---|---|
| 2026-08-31 | Full triage: Sequence gates Ops2/3, Manual backlog |
| 2026-09-01 | R1/R2/Ops1/S1 Done; R → `_archive/` |
| 2026-09-21 | Gate-S1 Done (Wannes); S → `_archive/`; Sequence **Ops-Remote1** then **L1** |
