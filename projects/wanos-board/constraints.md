<!-- --- file: projects/wanos-board/constraints.md -->

# PCB / schematic constraints — wanos-pcb-v1

Applies to `projects/wanos-board/`. Canonical spec → [`docs/board-spec.md`](../../docs/board-spec.md).

---

## Board

- **Revision:** wanos-pcb-v1
- **2-layer**, **85 × 56 mm**, **1.6 mm**, **ENIG** ([`board-spec.md`](../../docs/board-spec.md) § 8)
- Pi 4/5 compatible outline (not a HAT)
- Mounting holes: M2.5/M3 per [`components.xlsx`](components.xlsx) MH1–MH4

---

## Schematic

- Net names: `EXP_A_*`, `EXP_B_*`, `I2C_SCL`, `I2C_SDA`, `GPIO_SSR_*` — see [`io-expander-map.md`](../../docs/io-expander-map.md)
- SSR outputs: **Pi GPIO** → 470 Ω → PN2222A — **not** expander PWM
- 12 V monitor: single locked net (**R1**)
- PCA9554 `A0`–`A2` tied for unique addresses
- Decoupling: 100 nF per IC; 1 µF bulk near expanders

---

## Footprints

- From [`component-selection.md`](../../docs/component-selection.md) and [`components.xlsx`](components.xlsx)
- Validate LCSC stock at **J1**

---

## Layout zones

[`board-spec.md`](../../docs/board-spec.md) § 7 — Pi left, logic top, field right, SSR/12V bottom.

- Lock HDMI/SPI before Freerouting
- Separate SSR/12V from I²C

---

## Verification

```powershell
& "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe" sch erc projects/wanos-board/wanos-board.kicad_sch
& "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe" pcb drc projects/wanos-board/wanos-board.kicad_pcb
```

Konnect DRC/ERC also acceptable when documented in phase file.

---

## Safety

- Sauna/IR SSR + 12 V hard-lock nets are **critical**
- No mains on PCB
- Fail-safe 12 V loss detection ([`board-spec.md`](../../docs/board-spec.md) § 2.2)

---

## Tooling

[`docs/kicad-setup.md`](../../docs/kicad-setup.md) — KiCad 10 + Konnect.
