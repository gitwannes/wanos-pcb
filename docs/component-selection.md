<!-- --- file: docs/component-selection.md -->

# wanos-pcb-v1 — component selection (JLCPCB-compatible)

Verified JLCPCB-compatible parts for **wanos-pcb-v1**, aligned with [`board-spec.md`](board-spec.md).

**BOM seed:** [`projects/wanos-board/components.xlsx`](../projects/wanos-board/components.xlsx) (LCSC column — validate stock at **J1**).

---

## 1. JST XH connectors (2.50 mm pitch)

JLCPCB supports assembly of **through-hole JST XH** headers.

**Recommended parts (straight / right-angle):**

- **B2B-XH-A(LF)(SN)** — 2-pin
- **B3B-XH-A(LF)(SN)** — 3-pin
- **B4B-XH-A(LF)(SN)** — 4-pin
- **B6B-XH-A(LF)(SN)** — 6-pin
- **B7B-XH-A(LF)(SN)** — 7-pin
- **S6B-XH-A(LF)(SN)** — 6-pin right-angle

**Use for:** door sensors, water meters (bathroom 1 and 2), kWh meters, buttons, SHT31 differential I²C, SSR outputs, LCD modules (connectors only).

**KiCad footprints:**

```text
Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical
Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical
Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical
Connector_JST:JST_XH_B6B-XH-A_1x06_P2.50mm_Vertical
Connector_JST:JST_XH_B7B-XH-A_1x07_P2.50mm_Vertical
Connector_JST:JST_XH_S6B-XH-A_1x06_P2.50mm_RightAngle
```

---

## 2. Screw terminals (power input)

For **12 V input**:

- **KF301-2P** — 2-pin, 5.08 mm pitch
- **KF301-3P** — 3-pin, 5.08 mm pitch

**KiCad footprints:**

```text
TerminalBlock:TerminalBlock_Phoenix_MKDS-2-5.08_1x02_P5.08mm
TerminalBlock:TerminalBlock_Phoenix_MKDS-2-5.08_1x03_P5.08mm
```

---

## 3. HDMI connector (SPI repurposing)

- **Molex 208658-1052** — HDMI Type-A SMT female (JLCPCB assembly compatible)

**KiCad footprint:**

```text
Connector_HDMI:HDMI_Molex_208658-1052
```

Pin mapping → [`hdmi-spi-eink.md`](hdmi-spi-eink.md).

---

## 4. I/O expanders (two identical)

- **PCA9554PW** × 2 — 8-bit I²C, TSSOP-16
- **PCA9615DP** — differential I²C driver for SHT31 plant bus

**KiCad footprints:**

```text
Package_SO:TSSOP-16_4.4x5mm_P0.65mm
Package_SO:SOIC-8_3.9x4.9mm_P1.27mm
```

Net map → [`io-expander-map.md`](io-expander-map.md).

---

## 5. Additional components

| Part | Role | Package |
|---|---|---|
| **PN2222A-TA** | SSR driver | SOT-23 |
| **SMBJ12A** | 12 V TVS | SMB |
| **BLM21PG331SN1** | Pi 5 V ferrite | 0805 |
| **PC817 / LTV-817** | 12 V presence opto | SO-4 / SOP-4 |
| Passives 0603/0805 | 470 Ω, 10k, 4k7, 220–330 Ω, 2k2–4k7, 100 nF, 1 µF | Standard |

---

## 6. BOM summary

See [`components.xlsx`](../projects/wanos-board/components.xlsx) for designators, LCSC numbers, and mount types.

| Function | Part | Notes |
|---|---|---|
| HDMI / e-ink | Molex 208658-1052 | J1 |
| Field inputs | JST XH | J2–J7 (connector counts **R1** review) |
| SSR outputs | JST XH 6-pin RA | J8 |
| 12 V input | KF301 screw terminals | J9, J10 |
| I/O expanders | PCA9554PW × 2 | U1, U2 |
| Diff I²C | PCA9615DP | U3 |
| SSR drivers | PN2222A × 4 | Q1–Q4 |
| 12 V monitor | PC817 SMD | U4 |
| Pi header | 2×20 2.54 mm | J40 |
| Optional Pi power | USB-C | J41 |

**External (not assembled):** LCD modules, SHT31 sensor boards, external DIN SSRs.

Use Konnect to validate JLCPCB stock before **J1** order.
