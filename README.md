# wanos-pcb

[![License: Source Available](https://img.shields.io/badge/License-Source%20Available-lightgrey.svg)](LICENSE)

KiCad design and JLCPCB fabrication for **wanos-pcb-v1** — first-generation WanOS Pi carrier.

**Today:** WanOS runs on **WISC** boards (legacy reference in-repo). **Target:** **wanos-pcb-v1** + updated **wanos**. Code → [gitwannes/wanos](https://github.com/gitwannes/wanos).

---

## Repository layout

```text
wanos-pcb/
├── docs/
│   ├── board-spec.md            # wanos-pcb-v1 electrical spec (canonical)
│   ├── field-wiring.md          # JST pinouts + Cat5
│   ├── gpio-interface.md        # Pi BCM map (R2)
│   ├── external-plant.md        # Off-board SSR + 12 V
│   ├── grounding.md
│   ├── reference/
│   │   ├── datasheets/          # PDF pack (gitignored binaries)
│   │   ├── silkscreen/
│   │   └── wisc-board/
│   └── todo/
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
| ~~1–2~~ | ~~**R1, R2**~~ | ~~Requirements / architecture~~ **Done** |
| 3 | **Ops1** | Konnect + KiCad 10 + Cursor |
| 4–5 | **S1, Gate-S1** | Schematic + sign-off |
| 6–7 | **L1, Gate-L1** | Layout + silkscreen + sign-off |
| 8–9 | **Ops2, J1** | Fab readiness + JLCPCB order |
| 10 | **Ops3** | Receiving inspection |
| 11–12 | **V1a, V1b** | Bring-up / extended software |

Full backlog → [`docs/todo/pipeline.md`](docs/todo/pipeline.md).

---

## Quick links

| Doc | Purpose |
|---|---|
| [`docs/board-spec.md`](docs/board-spec.md) | **wanos-pcb-v1** specification |
| [`docs/gpio-interface.md`](docs/gpio-interface.md) | Pi BCM + software strategy |
| [`docs/external-plant.md`](docs/external-plant.md) | DIN SSR + 12 V plant |
| [`docs/field-wiring.md`](docs/field-wiring.md) | Connector pinouts |
| [`docs/reference/datasheets/README.md`](docs/reference/datasheets/README.md) | Datasheet pack |
| [`docs/kicad-setup.md`](docs/kicad-setup.md) | Konnect setup (**Ops1**) |
| [`projects/wanos-board/components.xlsx`](projects/wanos-board/components.xlsx) | BOM / LCSC seed |

---

## Workflow

1. ~~**`kickoff R2`**~~ — **Done** (2026-09-01).
2. **`implement`** — **S1** → **L1** → **J1** (after **Ops1**).
3. Operator **Gate-S1** / **Gate-L1** between phases.
4. **`V1a`** — board + updated **wanos**; cutover from WISC.

**DoD (every phase):** audit all `docs/**/*.md` + this README.

---

## Related repos

| Repo | Role |
|---|---|
| [gitwannes/wanos](https://github.com/gitwannes/wanos) | Runtime (WISC today; wanos-pcb-v1 at **V1a**) |
| [Konnect](https://github.com/mixelpixx/Konnect) | KiCad MCP automation |

---

## License

Source available — personal use OK, no redistribution. See [LICENSE](LICENSE).

Copyright (c) 2026 [Johan Wannes Hofmans](https://github.com/gitwannes). All rights reserved.
