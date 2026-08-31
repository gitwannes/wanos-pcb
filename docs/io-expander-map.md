<!-- --- file: docs/io-expander-map.md -->

# wanos-pcb-v1 — I/O expander schematic block

Two **PCA9554PW** expanders plus **PCA9615** on the Pi I²C bus. Ready for KiCad sheet **IO_EXPANDERS** after **R1** resolves open pin conflicts (see [`todo/phaseR-requirements.md`](todo/phaseR-requirements.md) § R1 checklist).

---

## 1. Common I²C bus

- Nets: `I2C_SCL`, `I2C_SDA` (from Raspberry Pi 40-pin header)
- Pull-ups: **4k7** to 3.3 V on SCL and SDA (main bus — additional segment pull-ups per [`board-spec.md`](board-spec.md) § 6.1)
- Devices on bus:
  - PCA9554PW Expander A
  - PCA9554PW Expander B
  - LCD modules (2× I²C)
  - PCA9615 (differential I²C driver for SHT31 sensors)

---

## 2. PCA9554PW — Expander A (meters + doors + kWh)

**Part:** `U_EXP_A` — PCA9554PW (TSSOP-16)  
**Power:** VCC = 3.3 V; GND

**Pins:**

- `SCL` → `I2C_SCL`
- `SDA` → `I2C_SDA`
- `A0`, `A1`, `A2` → tied to GND/VCC for I²C address (example: `0x20`)
- `INT` → optional Pi GPIO or NC

**GPIO mapping (Expander A):**

| Pin | Net (proposed) | Field |
|---|---|---|
| P0 | `EXP_A_P0_DOOR_BATH` | Bathroom door |
| P1 | `EXP_A_P1_DOOR_SAUNA` | Sauna door |
| P2 | `EXP_A_P2_WM_B1_COLD` | Bathroom 1 cold meter |
| P3 | `EXP_A_P3_WM_B1_HOT` | Bathroom 1 hot meter |
| P4 | `EXP_A_P4_WM_B2_COLD` | Bathroom 2 cold meter |
| P5 | `EXP_A_P5_WM_B2_HOT` | Bathroom 2 hot meter |
| P6 | `EXP_A_P6_KWH_MAIN` | kWh main |
| P7 | `EXP_A_P7_KWH_AUX_OR_12V_MON` | **R1:** kWh aux **or** 12 V monitor — **must not stay “either/or”** |

**Per-input hardware:**

- **100 nF** debounce on doors/meters
- Activity LED per meter/door (220–330 Ω)

---

## 3. PCA9554PW — Expander B (buttons + UI)

**Part:** `U_EXP_B` — PCA9554PW (TSSOP-16)  
**Power:** VCC = 3.3 V; GND

**Pins:**

- `SCL` → `I2C_SCL`
- `SDA` → `I2C_SDA`
- `A0`, `A1`, `A2` → second address (example: `0x21`)
- `INT` → optional Pi GPIO or NC

**GPIO mapping (Expander B):**

| Pin | Net (proposed) | Field |
|---|---|---|
| P0 | `EXP_B_P0_BTN1` | Sauna LCD button 1 |
| P1 | `EXP_B_P1_BTN2` | Sauna LCD button 2 |
| P2 | `EXP_B_P2_BTN3` | Sauna LCD button 3 |
| P3 | `EXP_B_P3_UI_READY` | Optional UI |
| P4 | `EXP_B_P4_UI_ERROR` | Optional UI |
| P5 | `EXP_B_P5_UI_LED` | Optional status |
| P6 | `EXP_B_P6_12V_MON` | **R1 candidate:** 12 V presence (opto) |
| P7 | `EXP_B_P7_SPARE` | Spare |

**Buttons:** Pull-up to 3.3 V; switch to GND when pressed; software debounce.

---

## 4. 12 V monitor (safety-critical)

**R1 must lock exactly one expander pin** for optocoupler output (see [`board-spec.md`](board-spec.md) § 2.2).

Recommended circuit:

- 12 V → 1 kΩ–2.2 kΩ → optocoupler LED
- Transistor → pull-up to 3.3 V → locked expander input
- Optional RC: 10 kΩ + 100 nF
- Part: **PC817** / **LTV-817** (U4 in [`components.xlsx`](../projects/wanos-board/components.xlsx))

Logic: LOW = 12 V present; HIGH = 12 V missing → hard-lock.

---

## 5. Decoupling and layout

- **100 nF** on each PCA9554 VCC; optional **1 µF** bulk nearby
- Expander A near **right-edge** field JST inputs
- Expander B near **top-edge** LCD + button connectors

---

## 6. SHT31 / PCA9615 (open at R1)

Four SHT31 sensors need an addressing plan (SHT31 has two I²C addresses). Options: I²C mux, multiple differential segments, or fewer live sensors — **lock at R1/R2**. Current BOM: one PCA9615 (U3) + one 4-pin JST (J7).

---

## 7. Net naming (KiCad)

Use the `EXP_A_*` / `EXP_B_*` names in § 2–3 once **R1** resolves P7 / 12 V monitor placement.
