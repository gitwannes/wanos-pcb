<!-- --- file: projects/wanos-board/constraints.md -->

# PCB / schematic constraints — wanos-pcb-v1

Applies to `projects/wanos-board/`. Canonical spec → [`docs/board-spec.md`](../../docs/board-spec.md). R1 + **R2** locks → [`field-wiring.md`](../../docs/field-wiring.md), [`gpio-interface.md`](../../docs/gpio-interface.md).

---

## Board

- **Revision:** **wanos-pcb-v1.0** (silk)
- **Target Pi:** Raspberry Pi **4** (re-use production unit)
- **2-layer**, **85 × 56 mm**, **1.6 mm**, **ENIG** — outline / **M2.5** holes per WISC **2.6.4** reference
- Pi carrier (not a HAT); mounting **MH1–MH4**

---

## Schematic

- Net names: `EXP_A_*`, `EXP_B_*`, `I2C_SCL`, `I2C_SDA`, `GPIO_SSR_*`, `GPIO_EINK_*` — see [`io-expander-map.md`](../../docs/io-expander-map.md), [`gpio-interface.md`](../../docs/gpio-interface.md)
- SSR outputs: **Pi GPIO** → 470 Ω → PN2222A — **not** expander PWM
- 12 V monitor: **`EXP_B_P6_12V_MON`** (locked)
- PCA9554: **`0x20`** (U1), **`0x21`** (U2); **INT pins NC**
- TCA9548A @ **`0x70`**; five SHT31 plant ports **J9–J12**, **J18** (ch 0–4); **J16** LCD on root I²C
- I²C pull-ups: **2k2** on SCL/SDA only (**R9**, **R10**)
- **No PCA9615** on v1
- **J14** only for 12 V (**J15** dropped)
- **J17** KF301 **5 V** screw in; **J41** USB-C **DNP** v1
- **J40** **+5VA** on pins **2 & 4** (header injection)
- Decoupling: 100 nF per IC; 1 µF bulk near expanders/mux

---

## Footprints

- From [`component-selection.md`](../../docs/component-selection.md) and [`components.xlsx`](components.xlsx)
- SSR **J13**: `JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical` (WISC parity)
- HDMI **J1**: Molex **208658-1052** (LCSC **C6990958**)
- Silkscreen: Wannes logos — **no** CC BY-NC-SA icon ([`reference/silkscreen/README.md`](../../docs/reference/silkscreen/README.md))

---

## Layout zones

[`board-spec.md`](../../docs/board-spec.md) § 7 — Pi left, logic top, field right, SSR/12V bottom.

- Lock HDMI/SPI before Freerouting
- Separate SSR/12V from I²C
- **L2 (pi_power):** **Q6** ideal diode carries **full Pi 5 V current** — wide/short traces **F1 → Q6 → +5VA → FB1** (manual check: [`phaseL-layout.md`](../../docs/todo/phaseL-layout.md) § L2)

---

## Manufacturing

- **JLCPCB:** full **PCBA** including **J40** (R2) — confirm BOM/CPL at **Ops2/J1**

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
