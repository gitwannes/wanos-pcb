# wanos-pcb

[![License: Source Available](https://img.shields.io/badge/License-Source%20Available-lightgrey.svg)](LICENSE)

KiCad design and JLCPCB fabrication for **wanos-pcb-v1** — first-generation WanOS Pi carrier.

**Today:** WanOS runs on **WISC** boards (legacy, not in this repo). **Target:** **wanos-pcb-v1** + future WanOS (version TBD). Code → [gitwannes/wanos](https://github.com/gitwannes/wanos).

---

## Repository layout

```text
wanos-pcb/
├── docs/
│   ├── board-spec.md            # wanos-pcb-v1 electrical spec (canonical)
│   ├── board-overview.md
│   ├── component-selection.md
│   ├── hdmi-spi-eink.md
│   ├── io-expander-map.md
│   ├── gpio-interface.md
│   ├── jlcpcb-ordering.md
│   ├── kicad-setup.md
│   └── todo/                    # Pipeline + phases
├── projects/wanos-board/
│   ├── components.xlsx
│   ├── design.yaml
│   └── fabrication/
└── README.md
```

---

## Pipeline (summary)

| Step | Id | What |
|---|---|---|
| 1–2 | **R1, R2** | Fix spec/BOM; lock architecture, plant, field wiring |
| 3 | **Ops1** | Konnect + KiCad 10 + Cursor |
| 4–5 | **S1, Gate-S1** | KiCad schematic + operator sign-off |
| 6–7 | **L1, Gate-L1** | Layout + silkscreen + sign-off |
| 8–9 | **Ops2, J1** | Fab readiness + JLCPCB order |
| 10 | **Ops3** | Receiving inspection |
| 11–12 | **V1a, V1b** | Bring-up (current WanOS) / full board (future WanOS code) |

Full backlog + Manual checks → [`docs/todo/pipeline.md`](docs/todo/pipeline.md).

---

## Quick links

| Doc | Purpose |
|---|---|
| [`docs/todo/pipeline.md`](docs/todo/pipeline.md) | Sequence + gates + must-not-forget list |
| [`docs/board-spec.md`](docs/board-spec.md) | **wanos-pcb-v1** specification |
| [`docs/kicad-setup.md`](docs/kicad-setup.md) | Konnect setup (**Ops1**) |
| [`projects/wanos-board/components.xlsx`](projects/wanos-board/components.xlsx) | BOM / LCSC seed |

---

## Workflow

1. **`kickoff R1`** → **`kickoff R2`** — locks before KiCad.
2. **`implement`** — **S1** (schematic) → **L1** (layout) → **J1** (fab).
3. Operator **Gate-S1** / **Gate-L1** sign-offs between phases.
4. **`V1a`** — prove board with current WanOS; **`V1b`** when future WanOS supports full board.

**DoD (every phase):** audit all `docs/**/*.md` + this README.

---

## Related repos

| Repo | Role |
|---|---|
| [gitwannes/wanos](https://github.com/gitwannes/wanos) | Runtime (WISC today; **V1b** code later) |
| [Konnect](https://github.com/mixelpixx/Konnect) | KiCad MCP automation |

---

## License

Source available — personal use OK, no redistribution. Same terms as [wanos](https://github.com/gitwannes/wanos), adapted for PCB design files. See [LICENSE](LICENSE).

Copyright (c) 2026 [Johan Wannes Hofmans](https://github.com/gitwannes). All rights reserved.
