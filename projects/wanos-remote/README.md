<!-- --- file: projects/wanos-remote/README.md --- -->

# wanos-remote

Universal plant remote PCB: **4×** opto pulse + **4×** DS18B20 (DS2482-800), Cat5 to main **TCA9548A**.

| Doc | Role |
|---|---|
| [`docs/remotepcb.md`](../../docs/remotepcb.md) | Canonical design locks |
| [`design.yaml`](design.yaml) | Project intent |
| [`components.xlsx`](../wanos-board/components.xlsx) | BOM — filter **`board=remote`** |

## KiCad

- Project: `wanos-remote.kicad_pro`
- Schematic: `wanos-remote.kicad_sch` (A3)
- Symbols: `wanos-remote.kicad_sym` (DS2482-800, TLP281-4)
- Regenerate schematic: `python projects/wanos-remote/_regen_schematic.py`

## Instances

| Board | Mux | Use |
|---|---|---|
| #1 | U5 ch 5 | 4× water YF + 2× pipe temp |
| #2 | U5 ch 6 | 2× kWh S0 + 1× temp |

Same PCB / same I²C straps (`MCP 0x22`, `DS2482 0x18`). Never enable ch 5 and 6 together.

## Status

Schematic **v0.1** — open in KiCad, run ERC, nudge wires to pins as needed (generator uses global labels; some IC pin attachments may need manual cleanup). Layout not started (40×60 hold).
