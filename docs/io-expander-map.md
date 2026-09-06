<!-- --- file: docs/io-expander-map.md -->

# wanos-pcb-v1 — I/O expander schematic block

Two **PCA9554PW** expanders plus **TCA9548A** I²C mux on the Pi local bus. Ready for KiCad sheet **IO_EXPANDERS** (R1 locked **2026-09-01**).

Field pinouts → [`field-wiring.md`](field-wiring.md).

---

## 1. Common I²C bus (local)

- Nets: `I2C_SCL`, `I2C_SDA` (from Raspberry Pi 40-pin header, BCM3/BCM2)
- Pull-ups: **2k2** to 3.3 V on SCL and SDA (**R9**, **R10**) — sized for 4–5 m Cat5 on mux channels @ 100 kHz
- Devices on local bus:
  - PCA9554PW Expander A (**U1**)
  - PCA9554PW Expander B (**U2**)
  - **TCA9548A** mux (**U5**, address **`0x70`**)
  - **J16** LCD I²C (both modules paralleled on one 4-pin header; root bus, not muxed)

**Not on v1:** PCA9615 differential driver (**U3** omitted).

**KiCad sheet:** [`io_expanders.kicad_sch`](../projects/wanos-board/io_expanders.kicad_sch) — **U1**, **U2**, **R9**/**R10**, door/kWh activity **D11**–**D12** / **D17**–**D18** / **R17**–**R18** / **R23**–**R24**, button pull-ups **R34**–**R36**, **C3**/**C4**. Water front-end → [`water_meters.kicad_sch`](../projects/wanos-board/water_meters.kicad_sch). **TCA9548A** (**U5**) + **C6**/**C7** + **J9–J12**/**J18**/**J16** on [`i2c_plant.kicad_sch`](../projects/wanos-board/i2c_plant.kicad_sch).

### PCA9554 address straps (hardware pins — not GPIO)

Address = `0x20 + (A2<<2) + (A1<<1) + A0`. **Direct tie** to **`+3V3`** or **GND** — no address pull resistors on v1.

| IC | I²C addr | Pin 1 (A0) | Pin 2 (A1) | Pin 3 (A2) |
|---|---|---|---|---|
| **U1** | `0x20` | GND | GND | GND |
| **U2** | `0x21` | **`+3V3`** | GND | GND |

| Pin | Both ICs |
|---|---|
| **8** | GND |
| **9** (INT) | **NC** v1 — polled I²C only |
| **16** (VCC) | **`+3V3`** + **100 nF** to GND (**C3** @ U1, **C4** @ U2) |

---

## 2. PCA9554PW — Expander A (meters + doors + kWh)

**Part:** `U1` — PCA9554PW (TSSOP-16) on **`io_expanders.kicad_sch`**  
**Power:** pin **16** → **`+3V3`** (**C3** 100 nF); pin **8** → GND  
**I²C address:** `0x20` (A0–A2 = low — § 1)

| Pin | Net | Field |
|---|---|---|
| P0 | `EXP_A_P0_DOOR_BATH` | Bathroom door (**J3**) |
| P1 | `EXP_A_P1_DOOR_SAUNA` | Sauna door (**J2**) |
| P2 | `EXP_A_P2_WM_B1_COLD` | Bathroom 1 cold (**J4** RJ45) — via **`water_meters.kicad_sch`** |
| P3 | `EXP_A_P3_WM_B1_HOT` | Bathroom 1 hot (**J4**) — via **`water_meters.kicad_sch`** |
| P4 | `EXP_A_P4_WM_B2_COLD` | Bathroom 2 cold (**J4**) — via **`water_meters.kicad_sch`** |
| P5 | `EXP_A_P5_WM_B2_HOT` | Bathroom 2 hot (**J4**) — via **`water_meters.kicad_sch`** |
| P6 | `EXP_A_P6_KWH_MAIN` | kWh main (**J6**) |
| P7 | `EXP_A_P7_KWH_AUX` | kWh aux (**J7**) |

**Doors / kWh (this sheet):** activity LED **1k0** (**D11**–**D12**, **D17**–**D18** / **R17**–**R18**, **R23**–**R24**) — **`+3V3`** → R → LED → GPIO. Debounce **100 nF** still target for doors/kWh (not yet separate sheet).

### Water meters (YF-B6/B10) — separate sheet

Canonical: [`field-wiring.md`](field-wiring.md) § 2a · schematic [`water_meters.kicad_sch`](../projects/wanos-board/water_meters.kicad_sch).

| Field net | Series | Pull-up | Debounce | TVS | Activity | Expander net |
|---|---|---|---|---|---|---|
| `WM_B1_COLD` | **R41** 330 Ω | **R37** 10k → **`+3V3`** | **C18** 100 nF | **D25** | **D13** / **R19** | `EXP_A_P2_WM_B1_COLD` |
| `WM_B1_HOT` | **R42** 330 Ω | **R38** 10k | **C19** 100 nF | **D26** | **D14** / **R20** | `EXP_A_P3_WM_B1_HOT` |
| `WM_B2_COLD` | **R43** 330 Ω | **R39** 10k | **C20** 100 nF | **D27** | **D15** / **R21** | `EXP_A_P4_WM_B2_COLD` |
| `WM_B2_HOT` | **R44** 330 Ω | **R40** 10k | **C21** 100 nF | **D28** | **D16** / **R22** | `EXP_A_P5_WM_B2_HOT` |

Sensor **VDD** = **`+5VA`** on **J4** (RJ45 pin **4**); **D29** **SMBJ5.0A** clamps **`+5VA`** at the jack. Output is **open-drain** — **no MOSFET**. Idle HIGH, pulse LOW. Cat5 map → [`field-wiring.md`](field-wiring.md) § 2a.

### Door / kWh activity LEDs (this sheet)

| Refs | Value | Nets |
|---|---|---|
| **D11**–**D12**, **R17**–**R18** | 1k0 | **J2** sauna door, **J3** bathroom door |
| **D17**–**D18**, **R23**–**R24** | 1k0 | **J6** kWh main, **J7** kWh aux |

Status LEDs (**D23**/**D24**) on **`pi_power.kicad_sch`**; SSR activity (**D19**–**D22**) on **`ssr_drivers.kicad_sch`**.

---

## 3. PCA9554PW — Expander B (buttons + 12 V monitor)

**Part:** `U2` — PCA9554PW (TSSOP-16) on **`io_expanders.kicad_sch`**  
**Power:** pin **16** → **`+3V3`** (**C4** 100 nF); pin **8** → GND  
**I²C address:** `0x21` (A0 = high, A1–A2 = low — § 1)

| Pin | Net | Field |
|---|---|---|
| P0 | `EXP_B_P0_BTN1` | Sauna LCD button 1 (**J8**) |
| P1 | `EXP_B_P1_BTN2` | Sauna LCD button 2 (**J8**) |
| P2 | `EXP_B_P2_BTN3` | Sauna LCD button 3 (**J8**) |
| P3 | — | **NC** v1 |
| P4 | — | **NC** v1 |
| P5 | — | **NC** v1 |
| P6 | `EXP_B_P6_12V_MON` | **12 V opto monitor (U4)** — safety-critical |
| P7 | — | **NC** v1 |

**Buttons:** Active-low to **GND** when pressed (**J8**). Pull-up **R34**–**R36** (10 kΩ → **`+3V3`**) on **P0**–**P2**.

**Unused GPIO (P3, P4, P5, P7):** hardware **NC** — no nets, no pull resistors. Firmware: configure as **output LOW** at PCA9554 init (see [`gpio-interface.md`](gpio-interface.md)).

### 3.1 Pull-up strategy (why not every pin?)

| Pin group | Pull bias | Why |
|---|---|---|
| **I²C** SCL/SDA | **R9**/**R10** 2k2 | Bus requirement — not GPIO |
| **Exp A** doors / kWh | Activity LED **1k0** path (for now) | Idle bias via LED string; dedicated 10k + RC still preferred |
| **Exp A** water P2–P5 | **R37**–**R40** 10k on **`water_meters.kicad_sch`** | YF OD → must pull to **`+3V3`** (not 5 V) |
| **Exp B** P0–P2 (buttons) | **R34**–**R36** 10 kΩ | Switch shorts to **GND** when pressed |
| **Exp B** P6 (12 V mon) | **R33** on **`pi_power.kicad_sch`** | Opto open-collector output |
| **Exp B** P3–P5, P7 | **NC** — no hardware bias | Unused; firmware drives **LOW** as output |
| Address **A0–A2** | Direct **GND** / **`+3V3`** tie | Strap, not pull resistor |

Do **not** pull YF signal lines to **`+5VA`** into the PCA9554. Do **not** use a MOSFET for YF-B6/B10 (OD already level-safe with 3.3 V pull-up).

---

## 4. 12 V monitor (safety-critical)

**R1 lock:** optocoupler output → **`EXP_B_P6_12V_MON`** only.

- 12 V → **R32** **1k5** → optocoupler LED (**U4** PC817) on **`pi_power.kicad_sch`**
- Transistor → pull-up to 3.3 V → Expander B P6
- Optional RC: 10 kΩ + 100 nF

Logic: **LOW** = 12 V present; **HIGH** = 12 V missing → hard-lock.

---

## 5. SHT31 plant — TCA9548A mux

Five SHT31 modules share I²C address **`0x44`**. **U5** (**TCA9548A**, 8-ch) selects one channel at a time. Channels **5–7** are NC. **J16** LCD stays on the root Pi I²C bus.

| Mux ch | JST | Sensor |
|---:|---|---|
| 0 | **J9** | Bathroom |
| 1 | **J10** | Cinema |
| 2 | **J11** | Sauna mid |
| 3 | **J12** | Sauna high |
| 4 | **J18** | Spare (location TBD) |
| 5–7 | — | NC |

Each used channel: **4-pin JST**, WISC **2.6.4 J7** pinout (GND, SDA, SCL, 3V3) over **~4–5 m Cat5**.

Software: write mux channel select byte to **`0x70`**, then read SHT31 at **`0x44`**.

---

## 6. Decoupling and layout

| Ref | Value | IC | Sheet |
|---|---|---|---|
| **C3** | 100 nF | **U1** VCC | `io_expanders.kicad_sch` |
| **C4** | 100 nF | **U2** VCC | `io_expanders.kicad_sch` |
| **C6** | 100 nF | **U5** VCC | `i2c_plant.kicad_sch` |
| **C7** | 100 nF | **U5** (bulk optional) | `i2c_plant.kicad_sch` |

One **100 nF** per expander at the chip is sufficient; **C5** was dropped (duplicate / unwired).

**Layout:** U1 near **right-edge** field JST inputs; U2 near button + LCD zone; U5 near I²C cluster; SHT31 JSTs grouped on top/right edge.

---

## 7. Net naming (KiCad)

Use the `EXP_A_*` / `EXP_B_*` names in § 2–3. Do not use legacy `EXP_A_P7_KWH_AUX_OR_12V_MON`.
