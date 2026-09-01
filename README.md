# wanos-pcb

[![License: Source Available](https://img.shields.io/badge/License-Source%20Available-lightgrey.svg)](LICENSE)

KiCad design and JLCPCB fabrication for **wanos-pcb-v1** — first-generation WanOS Pi carrier.

**Today:** WanOS runs on **WISC** boards (legacy reference in-repo). **Target:** **wanos-pcb-v1** + future WanOS (version TBD). Code → [gitwannes/wanos](https://github.com/gitwannes/wanos).

---

## Repository layout

```text
wanos-pcb/
├── docs/
│   ├── board-spec.md            # wanos-pcb-v1 electrical spec (canonical)
│   ├── field-wiring.md          # JST pinouts + Cat5 (R1 locks)
│   ├── board-overview.md
│   ├── component-selection.md
│   ├── reference/
│   │   ├── silkscreen/          # PCB font + logo assets
│   │   └── wisc-board/          # WISC summaries + read-only KiCad
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
| ~~1~~ | ~~**R1**~~ | ~~Spec + BOM contradictions~~ **Done** |
| 2 | **R2** | Architecture, external plant, mechanical |
| 3 | **Ops1** | Konnect + KiCad 10 + Cursor |
| 4–5 | **S1, Gate-S1** | Schematic + sign-off |
| 6–7 | **L1, Gate-L1** | Layout + silkscreen + sign-off |
| 8–9 | **Ops2, J1** | Fab readiness + JLCPCB order |
| 10 | **Ops3** | Receiving inspection |
| 11–12 | **V1a, V1b** | Bring-up / full board (future WanOS) |

Full backlog → [`docs/todo/pipeline.md`](docs/todo/pipeline.md).

---

## Quick links

| Doc | Purpose |
|---|---|
| [`docs/board-spec.md`](docs/board-spec.md) | **wanos-pcb-v1** specification |
| [`docs/field-wiring.md`](docs/field-wiring.md) | Connector pinouts |
| [`docs/reference/silkscreen/README.md`](docs/reference/silkscreen/README.md) | Silkscreen font (WISC parity) |
| [`docs/kicad-setup.md`](docs/kicad-setup.md) | Konnect setup (**Ops1**) |
| [`projects/wanos-board/components.xlsx`](projects/wanos-board/components.xlsx) | BOM / LCSC seed |

---

## Workflow

1. **`kickoff R2`** — architecture locks before KiCad.
2. **`implement`** — **S1** → **L1** → **J1**.
3. Operator **Gate-S1** / **Gate-L1** between phases.
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

Source available — personal use OK, no redistribution. See [LICENSE](LICENSE).

Copyright (c) 2026 [Johan Wannes Hofmans](https://github.com/gitwannes). All rights reserved.
