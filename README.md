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
│   ├── remotepcb.md             # wanos-remote plant module
│   ├── field-wiring.md          # JST pinouts + Cat5
│   ├── gpio-interface.md        # Pi BCM map (R2)
│   ├── external-plant.md        # Off-board SSR + 12 V
│   ├── grounding.md
│   ├── reference/
│   │   ├── datasheets/          # PDF pack (gitignored binaries)
│   │   ├── silkscreen/
│   │   └── wisc-board/
│   └── todo/
├── projects/wanos-board/        # Main Pi carrier
│   ├── wanos-board.kicad_pro
│   ├── components.xlsx          # BOM: column board = main | remote
│   └── …
├── projects/wanos-remote/       # Plant remote (pulse + 1-Wire)
│   ├── wanos-remote.kicad_pro
│   ├── wanos-remote.kicad_sch
│   └── design.yaml
└── README.md
```

---

## Pipeline (summary)

| Step | Id | What |
|---|---|---|
| ~~…~~ | ~~**R / Ops1 / S / Gate-S1**~~ | ~~Requirements + main schematic~~ **Done** **2026-09-21** |
| **1** | **Ops-Remote1** | Operator: clean + check **wanos-remote** schematic |
| **2** | **L1** | Main carrier PCB layout |
| **3** | **Gate-L1** | Layout sign-off |
| **4–5** | **Ops2, J1** | Fab readiness + JLCPCB order |
| **6** | **Ops3** | Receiving inspection |
| **7–8** | **V1a, V1b** | Bring-up / extended software |

Full backlog → [`docs/todo/pipeline.md`](docs/todo/pipeline.md).

---

## Quick links

| Doc | Purpose |
|---|---|
| [`docs/board-spec.md`](docs/board-spec.md) | **wanos-pcb-v1** specification |
| [`docs/remotepcb.md`](docs/remotepcb.md) | **wanos-remote** plant module |
| [`docs/gpio-interface.md`](docs/gpio-interface.md) | Pi BCM + software strategy (**wanos-pcb-v1**) |
| [`docs/gpio-map.md`](docs/gpio-map.md) | WISC production BCM inventory |
| [`docs/external-plant.md`](docs/external-plant.md) | DIN SSR + 12 V plant |
| [`docs/field-wiring.md`](docs/field-wiring.md) | Connector pinouts |
| [`docs/schematic-signoff.md`](docs/schematic-signoff.md) | Gate-S1 record (Done) |
| [`docs/reference/datasheets/README.md`](docs/reference/datasheets/README.md) | Datasheet pack |
| [`docs/kicad-setup.md`](docs/kicad-setup.md) | Konnect + KiCad 10 (**Ops1** Done) |
| [`projects/wanos-board/components.xlsx`](projects/wanos-board/components.xlsx) | BOM / LCSC seed |

---

## Workflow

1. ~~**`kickoff` / S1 / Gate-S1**~~ — **Done** (schematic signed **2026-09-21**).
2. **Ops-Remote1** — operator cleans + checks [`projects/wanos-remote/`](projects/wanos-remote/).
3. **`implement` L1** — main carrier layout (after Gate-S1).
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
