<!-- --- file: docs/kicad-setup.md -->

# KiCad setup (WanOS PCB)

Local toolchain notes for `projects/wanos-board/`. Optional Cursor + MCP workflow mirrors the [`kicad-cursor`](https://github.com/) template repo on this machine (`C:/data/git/kicad-cursor`).

---

## Requirements

| Tool | Purpose |
|---|---|
| **KiCad 10** (or project-locked version at S1) | Schematic + PCB editor |
| **kicad-cli** | ERC/DRC and batch Gerber export |
| **Python 3.11+** + **uv** | Optional KiCad MCP servers in Cursor |

Enable **IPC API Server** in KiCad: *Preferences → Plugins → Enable IPC API Server*. Keep KiCad running when using MCP tools.

---

## Project location

```text
projects/wanos-board/
  design.yaml          # Intent + open questions
  constraints.md       # Design rules
  bom-targets.yaml     # LCSC / library parts
  wanos-board.kicad_*  # Created during S1/S1 kickoff
  fabrication/         # Gerber / BOM / CPL outputs
  datasheets/          # Reference PDFs
```

---

## Verification commands

```powershell
$cli = "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"
$sch = "projects/wanos-board/wanos-board.kicad_sch"
$pcb = "projects/wanos-board/wanos-board.kicad_pcb"

& $cli sch erc $sch
& $cli pcb drc $pcb
```

Do not mark **S1** or **L1** done until ERC/DRC pass or waivers are recorded in the phase file.

---

## LCSC parts (optional)

If using JLC assembly, import symbols/footprints via your WSL `fetchPart` flow (see `kicad-cursor/docs/setup.md`). Lock library path and part numbering at **S1 kickoff**.

---

## Agent skills (optional)

When using Cursor with MCP configured (copy/adapt from `kicad-cursor/.cursor/`):

- `@kicad-project` — paths, libraries, layout
- `@component-select` — LCSC parts
- `@schematic-design` / `@pcb-layout` — design edits
- `@design-verify` — ERC/DRC gate

Pipeline commands still apply: **kickoff** before design locks; **implement** before treating a phase as coding.
