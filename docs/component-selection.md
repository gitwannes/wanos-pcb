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
| **B5B-XH-A** | 5 | SSR **J13** (WISC J1 parity, vertical) |
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

- **KF301-2P** — **J14** only (**J15** dropped R2)

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
| **PN2222A-TA** × 5 | Q1–Q5 | SSR drivers + master safety (SOT-23) |
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
| **R9**, **R10** | **2k2** | I²C SCL/SDA pull-ups (4–5 m Cat5 @ 100 kHz) |
| R1–R4 | 470 Ω | SSR base |
| R5–R8 | 10k | SSR pulldown |
| R17–R28 | **1k0** | Activity LEDs |
| R29, R31 | **2k0** | Status LEDs (5 V rails) |
| R30 | **6k8** | Status LED (12 V) |
| R32 | **1k5** | Opto LED |
| R33 + C17 | 10k + 100 nF | Opto RC (optional) |

**Not populated v1:** R11–R16 (removed — no PCA9615 segment).

---

## 7. BOM summary

| Function | Part | Connector / ref |
|---|---|---|
| HDMI / e-ink | Molex 208658-1052 | J1 |
| Doors | JST XH 2-pin × 2 | J2, J3 |
| Water | JST XH 6-pin × 2 | J4, J5 |
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
