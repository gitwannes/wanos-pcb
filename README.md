# wanos-pcb

KiCad design and JLCPCB fabrication pack for the **WanOS electronics board** — the Raspberry Pi carrier that wires local GPIO (pulse meters, door contacts, SHT11 buses, sauna/IR SSR outputs) into the [WanOS](https://github.com/gitwannes/wanos) runtime.

**Scope:** hardware design only. Application logic stays in the main WanOS repo.

---

## Repository layout

```text
wanos-pcb/
├── docs/
│   ├── board-overview.md      # What the board must do (product reference)
│   ├── gpio-interface.md      # Pi pin / connector contract vs WanOS config_hardware.yaml
│   ├── jlcpcb-ordering.md     # Fab export checklist and JLCPCB order notes
│   ├── kicad-setup.md         # Local KiCad + tooling
│   └── todo/                  # Pipeline + phased delivery specs
├── projects/
│   └── wanos-board/           # KiCad project root
│       ├── design.yaml        # Design intent for agents / kickoff
│       ├── constraints.md     # Schematic + layout rules
│       ├── bom-targets.yaml   # Preferred LCSC parts (filled during design)
│       ├── datasheets/        # Reference PDFs (gitignored when large)
│       └── fabrication/       # Gerber / BOM / CPL outputs for JLCPCB
└── README.md
```

---

## Quick links

| Doc | Purpose |
|---|---|
| [`docs/todo/pipeline.md`](docs/todo/pipeline.md) | Ordered backlog (Sequence / Done / Ops) |
| [`docs/gpio-interface.md`](docs/gpio-interface.md) | GPIO and field-wiring contract |
| [`docs/jlcpcb-ordering.md`](docs/jlcpcb-ordering.md) | What to export and upload |
| [`projects/wanos-board/design.yaml`](projects/wanos-board/design.yaml) | Block diagram + open questions |

---

## Workflow

1. **Kickoff** a pipeline item (`kickoff R1`, `kickoff S1`, …) — lock requirements in the matching phase file before schematic edits.
2. **Design** in KiCad under `projects/wanos-board/` (schematic → layout → ERC/DRC clean).
3. **Export** Gerbers, drill, BOM, and centroid (CPL) into `projects/wanos-board/fabrication/`.
4. **Order** via JLCPCB using [`docs/jlcpcb-ordering.md`](docs/jlcpcb-ordering.md).
5. **Bring-up** on the WanOS Pi; update product docs + close the phase in `docs/todo/`.

**DoD (every phase):** Last step = audit and update all `docs/**/*.md` (+ this README) against shipped artifacts.

---

## Related repos

| Repo | Role |
|---|---|
| [gitwannes/wanos](https://github.com/gitwannes/wanos) | Runtime, `config_hardware.yaml`, sauna/IR control |
| [kicad-cursor](https://github.com/) (local: `C:/data/git/kicad-cursor`) | Optional Cursor + KiCad MCP workflow reference |
