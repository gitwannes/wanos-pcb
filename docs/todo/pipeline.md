# WanOS PCB — Implementation pipeline

Ordered backlog + closed history. Specs / DoD / locks live in the lettered phase files — not here.

**Last updated:** 2026-08-31 (repo scaffold — no design phases closed yet)

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
| **R** | Requirements / architecture | [`phaseR-requirements.md`](phaseR-requirements.md) |
| **S** | Schematic | [`phaseS-schematic.md`](phaseS-schematic.md) |
| **L** | Layout | [`phaseL-layout.md`](phaseL-layout.md) |
| **J** | JLCPCB fabrication pack | [`phaseJ-jlcpcb.md`](phaseJ-jlcpcb.md) |
| **V** | Verification / bring-up | [`phaseV-verify.md`](phaseV-verify.md) |

**DoD (every phase):** Last step = audit & update all `docs/**/*.md` (+ root README) against shipped artifacts.

When a phase finishes: Sequence → **Done**; trim Sequence only.

**Product reference** (shipped behaviour / contracts) lives under `docs/` **outside** `todo/` — see User Rule *Documentation as-is vs pipeline*.

---

## Done

| Phase | Notes |
|---|---|
| *(none yet)* | Repo scaffold **2026-08-31** |

---

## Sequence

All open items. **Detail** = phase file section.

```text
#   Status Size Id           What                                               Detail
──  ────── ──── ──────────── ────────────────────────────────────────────────── ──────────────────────────
1   open   high R1           Board architecture kickoff (Pi model, form, I/O)   phaseR § R1
2   open   high S1           Schematic (blocks, ERC clean)                      phaseS § S1
3   open   high L1           PCB layout (placement, routing, DRC clean)         phaseL § L1
4   open   mid  J1           JLCPCB fab pack (Gerber + BOM + CPL)               phaseJ § J1
5   open   mid  V1           Pi bring-up vs WanOS config_hardware.yaml          phaseV § V1
```

Near-term: **R1 kickoff** before any KiCad schematic work. **S1 → L1 → J1** in order. **V1** after boards arrive.

---

## Manual checks

Not lettered product phases. Detail stays here unless re-homed.

| Item | Status | Notes |
|---|---|---|
| **KiCad + MCP setup** | open | See [`docs/kicad-setup.md`](../kicad-setup.md); optional link to local `kicad-cursor` repo |
| **LCSC / global symbol lib** | hold | Part import path locked at **S1** kickoff |
| **WanOS runtime pin map sync** | open | Canonical software map: [wanos `config_hardware.yaml`](https://github.com/gitwannes/wanos/blob/main/config_hardware.yaml) — PCB doc mirror: [`gpio-interface.md`](../gpio-interface.md) |

---

## Changelog

| Date | Change |
|---|---|
| 2026-08-31 | Initial pipeline + phase files; repo scaffold |
