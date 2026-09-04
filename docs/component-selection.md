<!-- --- file: docs/component-selection.md -->

# wanos-pcb-v1 — component selection (JLCPCB-compatible)

Verified JLCPCB-compatible parts for **wanos-pcb-v1**, aligned with [`board-spec.md`](board-spec.md) (R1 locks **2026-09-01**).

**BOM seed:** [`projects/wanos-board/components.xlsx`](../projects/wanos-board/components.xlsx) (LCSC column — validate stock at **J1**).

**Field connectors:** designators and pinouts → [`field-wiring.md`](field-wiring.md).

---

## 1. JST XH connectors (2.50 mm pitch)

| MPN pattern | Pins | wanos use |
|---|---:|---|
| **B2B-XH-A** | 2 | Doors **J2–J3**, kWh **J6–J7** |
| **B4B-XH-A** | 4 | Buttons **J8**, SHT31 **J9–J12**, LCD **J16** |
| **B5B-XH-A** | 5 | SSR **J13** (vertical) |
| **B6B-XH-A** | 6 | Water **J4–J5** |

**KiCad footprints (vertical):**

```text
Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical
Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical
Connector_JST:JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical
Connector_JST:JST_XH_B6B-XH-A_1x06_P2.50mm_Vertical
```

---

## 2. Screw terminals (12 V)

- **KF301-2P** — **J14** (12 V in) and **J17** (5 V in); both on **`pi_power.kicad_sch`**

Footprint: `TerminalBlock_Phoenix_MKDS-2-5.08_1x02`.

---

## 3. HDMI (e-ink SPI)

- **Molex 208658-1052** — **J1** (LCSC **C6990958**) — `Connector_HDMI:HDMI_Molex_208658-1052`

Pin mapping → [`hdmi-spi-eink.md`](hdmi-spi-eink.md).

---

## 4. I²C ICs

| Part | Ref | Role |
|---|---|---|
| **PCA9554PW** × 2 | U1, U2 | 8-bit expanders |
| **TCA9546A** | U5 | 4-ch I²C mux @ **0x70** (SHT31 @ **0x44**) |
| ~~PCA9615DP~~ | — | **Not used v1** |

Footprints: `Package_SO:TSSOP-16_4.4x5mm_P0.65mm` (9554, 9546).

Net map → [`io-expander-map.md`](io-expander-map.md).

---

## 5. Other active parts

| Part | Ref | Role |
|---|---|---|
| **PN2222A-TA** × 5 | Q1–Q5 | SSR field drivers + safety gate **Q5** (SOT-23) |
| **PC817A** SMD | U4 | 12 V opto |
| **SMBJ12A** | D3 | 12 V TVS (SMD SMB) — [`smbj12a.pdf`](reference/datasheets/smbj12a.pdf) |
| **BZT52C5V6** | D1 | 5 V overvoltage clamp (SMD SOD-123, shunt to GND) — family ref [`bzx85c.pdf`](reference/datasheets/bzx85c.pdf) |
| **AO3401A** | Q6 | 5 V ideal diode / reverse block (P-FET SOT-23, gate tied to drain) |
| **RVT1A101M0605** | C1 | +5VA bulk 100 µF 10 V (SMD 6.3×5.4 mm) |
| **BLM21PG331SN1** | FB1 | Pi 5 V ferrite |
| **SMD1206P200TF** | F1 | 5 V input polyfuse 2 A hold (resettable, 1206, LCSC C545216) |
| **500 mA polyfuse** | F2 | HDMI panel 5 V (1206, LCSC C369233) |

---

## 6. Passives (R1 locks)

| Ref | Value | Role |
|---|---|---|
| **R9**, **R10** | **2k2** | I²C SCL/SDA pull-ups on **`io_expanders.kicad_sch`** (4–5 m Cat5 @ 100 kHz) |
| **C3**, **C4** | 100 nF | PCA9554 VCC decoupling (**U1**, **U2** on **`io_expanders.kicad_sch`**) |
| **C6**, **C7** | 100 nF | TCA9546A VCC decoupling (**U5** on **`i2c_plant.kicad_sch`**) |
| **R34**–**R36** | 10 kΩ | Exp B button **P0–P2** pull-ups (**`io_expanders.kicad_sch`**) |
| **R37**–**R40** | 10 kΩ | Water YF OD pull-ups → **`+3V3`** (**`water_meters.kicad_sch`**) |
| **R41**–**R44** | **330 Ω** | Water series field → expander (**`water_meters.kicad_sch`**) |
| **C18**–**C21** | 100 nF | Water debounce (**`water_meters.kicad_sch`**) |
| R1–R4 | 470 Ω | SSR field base (**Q1–Q4**) |
| R5–R8 | 10 kΩ | SSR field base pulldown (base → emitter / **`SAFETY_BUS`**) |
| **R14** | 470 Ω | **Q5** base (**GPIO_SSR_SAFETY**) |
| **R15** | 10 kΩ | **Q5** base pulldown → **GND** |
| **R16** | 10 kΩ | **`SAFETY_BUS`** pull-up → **`+5VA`** |
| C8–C12 | 100 nF | SSR driver decoupling (C–E per **Q1–Q5**) |
| R17–R18, R23–R24 | **1k0** | Door / kWh activity LEDs (**`io_expanders.kicad_sch`**) |
| R19–R22 | **1k0** | Water activity LEDs (**`water_meters.kicad_sch`**) |
| R25–R28 | **1k0** | SSR activity LEDs (**`ssr_drivers.kicad_sch`**, **`+5VA`** → **`SSR_*`**) |
| R29 | **2k0** | Status LED (**+5VA**) |
| R30 | **6k8** | Status LED (**+12V**) |
| R32 | **1k5** | Opto LED |
| R33 + C17 | 10k + 100 nF | Opto RC (optional) |

**Not populated v1:** **R11–R13** (PCA9615 segment removed).

---

## 7. BOM summary

| Function | Part | Connector / ref |
|---|---|---|
| HDMI / e-ink | Molex 208658-1052 | J1 |
| Doors | JST XH 2-pin × 2 | J2, J3 |
| Water | JST XH 6-pin × 2 | J4, J5 — YF-B6/B10, **`+5VA`** |
| kWh | JST XH 2-pin × 2 | J6, J7 |
| Buttons | JST XH 4-pin | J8 |
| SHT31 plant | JST XH 4-pin × 4 | J9–J12 |
| SSR | JST XH **5-pin** vertical | J13 |
| 12 V | KF301 2P | J14 |
| LCD | JST XH 4-pin × 1 | J16 |
| Expanders | PCA9554PW × 2 | U1, U2 |
| I²C mux | TCA9546A | U5 |
| SSR drivers | PN2222A × 5 | Q1–Q5 |
| 12 V monitor | PC817A | U4 |
| Pi header | 2×20 | J40 |
| 5 V in | KF301 2P | **J17** |
| ~~Pi USB-C~~ | — | **J41 DNP v1** |

**External (not assembled):** LCD modules, SHT31 sensor boards, external DIN SSRs.

**Datasheets:** [`reference/datasheets/README.md`](reference/datasheets/README.md) (14/15 on disk; `usb-c-j41.pdf` deferred — J41 DNP v1).

Validate LCSC stock before **J1**.

---

## 8. Silkscreen

Font: [Printed Circuit Board 7](https://www.fontspace.com/printed-circuit-board-7-font-f15777) — see [`reference/silkscreen/README.md`](reference/silkscreen/README.md).
