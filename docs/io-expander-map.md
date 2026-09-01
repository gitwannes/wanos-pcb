<!-- --- file: docs/io-expander-map.md -->

# wanos-pcb-v1 — I/O expander schematic block

Two **PCA9554PW** expanders plus **TCA9546A** I²C mux on the Pi local bus. Ready for KiCad sheet **IO_EXPANDERS** (R1 locked **2026-09-01**).

Field pinouts → [`field-wiring.md`](field-wiring.md).

---

## 1. Common I²C bus (local)

- Nets: `I2C_SCL`, `I2C_SDA` (from Raspberry Pi 40-pin header, BCM3/BCM2)
- Pull-ups: **2k2** to 3.3 V on SCL and SDA (**R9**, **R10**) — sized for 4–5 m Cat5 on mux channels @ 100 kHz
- Devices on local bus:
  - PCA9554PW Expander A (**U1**)
  - PCA9554PW Expander B (**U2**)
  - **TCA9546A** mux (**U5**, address **`0x70`**)
  - **J16** LCD I²C (both modules paralleled on one 4-pin header)

**Not on v1:** PCA9615 differential driver (**U3** omitted).

---

## 2. PCA9554PW — Expander A (meters + doors + kWh)

**Part:** `U1` — PCA9554PW (TSSOP-16)  
**Power:** VCC = 3.3 V; GND  
**I²C address:** `0x20` (U1 — A0–A2 = low)

| Pin | Net | Field |
|---|---|---|
| P0 | `EXP_A_P0_DOOR_BATH` | Bathroom door (**J3**) |
| P1 | `EXP_A_P1_DOOR_SAUNA` | Sauna door (**J2**) |
| P2 | `EXP_A_P2_WM_B1_COLD` | Bathroom 1 cold (**J4**) |
| P3 | `EXP_A_P3_WM_B1_HOT` | Bathroom 1 hot (**J4**) |
| P4 | `EXP_A_P4_WM_B2_COLD` | Bathroom 2 cold (**J5**) |
| P5 | `EXP_A_P5_WM_B2_HOT` | Bathroom 2 hot (**J5**) |
| P6 | `EXP_A_P6_KWH_MAIN` | kWh main (**J6**) |
| P7 | `EXP_A_P7_KWH_AUX` | kWh aux (**J7**) |

**Per-input hardware:** 100 nF debounce; activity LED 220–330 Ω where specified in [`board-spec.md`](board-spec.md).

---

## 3. PCA9554PW — Expander B (buttons + 12 V monitor)

**Part:** `U2` — PCA9554PW (TSSOP-16)  
**I²C address:** `0x21` (U2 — A0 = high, A1–A2 = low)

| Pin | Net | Field |
|---|---|---|
| P0 | `EXP_B_P0_BTN1` | Sauna LCD button 1 (**J8**) |
| P1 | `EXP_B_P1_BTN2` | Sauna LCD button 2 (**J8**) |
| P2 | `EXP_B_P2_BTN3` | Sauna LCD button 3 (**J8**) |
| P3 | `EXP_B_P3_UI_READY` | Spare — **DNP** v1 |
| P4 | `EXP_B_P4_UI_ERROR` | Spare — **DNP** v1 |
| P5 | `EXP_B_P5_UI_LED` | Spare — **DNP** v1 |
| P6 | `EXP_B_P6_12V_MON` | **12 V opto monitor (U4)** — safety-critical |
| P7 | `EXP_B_P7_SPARE` | Spare |

**Buttons:** Pull-up to 3.3 V; switch to GND when pressed; software debounce.

**INT pin:** **Not connected** on v1 (polled I²C only).

---

## 4. 12 V monitor (safety-critical)

**R1 lock:** optocoupler output → **`EXP_B_P6_12V_MON`** only.

- 12 V → 1 kΩ–2.2 kΩ → optocoupler LED (**U4** PC817 class)
- Transistor → pull-up to 3.3 V → Expander B P6
- Optional RC: 10 kΩ + 100 nF

Logic: **LOW** = 12 V present; **HIGH** = 12 V missing → hard-lock.

---

## 5. SHT31 plant — TCA9546A mux

Four SHT31 modules share I²C address **`0x44`**. **U5** (TCA9546A) selects one channel at a time.

| Mux ch | JST | Sensor |
|---:|---|---|
| 0 | **J9** | Bathroom |
| 1 | **J10** | Cinema |
| 2 | **J11** | Sauna mid |
| 3 | **J12** | Sauna high |

Each channel: **4-pin JST**, WISC **2.6.4 J7** pinout (GND, SDA, SCL, 3V3) over **~4–5 m Cat5**.

Software: write mux channel byte to **`0x70`**, then read SHT31 at **`0x44`**.

---

## 6. Decoupling and layout

- **100 nF** on each PCA9554 and TCA9546 VCC; optional **1 µF** bulk nearby
- Expander A near **right-edge** field JST inputs
- Expander B near **top-edge** button + LCD zone
- U5 near I²C cluster; keep SHT31 JSTs grouped on top/right edge

---

## 7. Net naming (KiCad)

Use the `EXP_A_*` / `EXP_B_*` names in § 2–3. Do not use legacy `EXP_A_P7_KWH_AUX_OR_12V_MON`.
