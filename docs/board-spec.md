<!-- --- file: docs/board-spec.md -->

# WanOS PCB — board specification

**Revision:** **wanos-pcb-v1** (first-generation WanOS carrier; replaces ad-hoc / **WISC**-era wiring on a new board — not a spin of the old WISC PCB).

Structured specification for KiCad 10 + Konnect, manufactured via JLCPCB, mechanically compatible with Raspberry Pi 4/5.

**Related:** Overview → [`board-overview.md`](board-overview.md) · Components → [`component-selection.md`](component-selection.md) · HDMI→SPI → [`hdmi-spi-eink.md`](hdmi-spi-eink.md) · I/O map → [`io-expander-map.md`](io-expander-map.md) · GPIO contracts → [`gpio-interface.md`](gpio-interface.md)

---

## 1. System overview

WanOS is a Raspberry-Pi-based home-automation controller for sauna, bathroom, cinema, and water systems.

**wanos-pcb-v1** provides:

- Digital inputs (doors, water meters, kWh meters, buttons)
- Differential I²C sensor interfaces (SHT31 plant bus)
- SSR control outputs (3-phase sauna + IR)
- Power monitoring (12 V sauna rail)
- LCD interfaces (2× I²C)
- E-ink display via repurposed HDMI connector (WISC SPI)
- Status and activity LEDs

**Board size:** **85 × 56 mm** (Pi-compatible outline; **not** a HAT stack).

**Software note:** Full board capability targets a **later WanOS** release. **Current WanOS** continues on **WISC** boards until **wanos-pcb-v1** is proven (**V1a**). See [`gpio-interface.md`](gpio-interface.md) § WISC-equivalent subset.

---

## 2. Power architecture

### 2.1 Rails

#### 5 V (stable, independent)

- Powers Raspberry Pi
- Powers logic (PCA9554PW expanders, PCA9615, LEDs, sensors)
- Must **remain powered** when sauna safety triggers
- Provided by Pi or external regulated supply

#### 12 V (sauna SSR rail)

- Powers SSR opto-inputs
- Cut by external temperature safety
- Must be **monitored** by the PCB
- Loss of 12 V → Pi stays alive → WanOS logs critical event + stops sauna
- Sauna remains **hard-locked** until manual reset via UI/software

### 2.2 12 V monitoring

The design uses an **optocoupler** for robust, isolated 12 V presence detection.

- 12 V present → sauna control allowed
- 12 V missing → critical shutdown + lockout

#### Why optocoupler?

- Galvanic isolation between 12 V sauna safety rail and 3.3 V logic
- Protects Raspberry Pi and expanders from spikes or wiring faults
- Clean digital detection of “12 V present” vs “12 V missing”
- Supports required **hard-lock safety behaviour**

#### Recommended circuit

- 12 V → **1 kΩ – 2.2 kΩ resistor** → optocoupler LED
- Optocoupler transistor → **pull-up to 3.3 V** → digital input (I/O expander — pin **TBD at R1**; see [`io-expander-map.md`](io-expander-map.md))
- Optional RC filter (e.g. 10 kΩ + 100 nF) for noise immunity
- Suggested optocoupler: **PC817**, **LTV-817**, or equivalent phototransistor type

#### Logic interpretation

- LED ON → transistor pulls signal LOW → **12 V present**
- LED OFF → transistor floats HIGH → **12 V missing → trigger hard-lock**

---

## 3. Inputs

### 3.1 Door sensors (bathroom and sauna)

- Reed switches
- Debounce capacitors: **100 nF**
- Routed to **I/O Expander A**
- JST XH connectors

### 3.2 Water meters — bathroom 1 (cold and hot)

- Pulse counters
- Routed to **I/O Expander A**
- Activity LEDs: **220–330 Ω**
- JST XH connectors

### 3.3 Water meters — bathroom 2 (cold and hot)

- Additional pulse counters
- Routed to **I/O Expander A**
- Activity LEDs: **220–330 Ω**
- JST XH connectors

### 3.4 Energy kWh counter (main)

- Pulse input
- Routed to **I/O Expander A**
- Activity LED: **220–330 Ω**
- JST connector

### 3.5 Energy kWh counter (additional)

- Second kWh input
- Routed to **I/O Expander A**
- Activity LED: **220–330 Ω**
- JST connector

### 3.6 Buttons (sauna LCD)

- 3 digital inputs
- Routed to **I/O Expander B**
- JST connector (**4-pin**: 3 signals + GND — see **R1** checklist in [`phaseR-requirements.md`](todo/phaseR-requirements.md))
- Software debounce

### 3.7 SHT31 sensors (4×)

- Bathroom, cinema, sauna mid, sauna high
- Via **PCA9615** differential I²C
- Standard mode: **100 kHz**
- Each segment requires **4k7 pull-ups**
- JST connectors (addressing / segment plan **TBD at R1**)

---

## 4. Outputs

### 4.1 SSR channels (4×)

- 3 for sauna (3-phase heater)
- 1 for IR
- Software PWM: **1–5 Hz**
- **Pi GPIO** → **470 Ω** → PN2222A → SSR (not via I²C expander)
- PN2222A base pulldown: **10k**
- SSR opto input powered from **12 V**
- JST XH connectors for SSR outputs

Pi GPIO allocation → [`gpio-interface.md`](gpio-interface.md) § Full board.

### 4.2 E-ink display (HDMI Type A repurposed as SPI)

See [`hdmi-spi-eink.md`](hdmi-spi-eink.md).

### 4.3 LCD screens (2×)

- I²C bus
- Shared with I/O Expander B zone
- Standard 100 kHz
- JST connectors (**dedicated headers TBD at R1** — see phase **R1** checklist)

### 4.4 Pi power connector (optional)

- USB-A or USB-C
- 5k1 PD resistor if USB-C
- Only needed if powering Pi externally

---

## 5. Indicator LEDs

### 5.1 Status LEDs (dim)

- 5 V external power
- 12 V external power
- 5 V Pi power
- Resistors: **2k2–4k7**

### 5.2 Activity LEDs (bright)

- Doors (2×)
- Water meters (bathroom 1: 2×)
- Water meters (bathroom 2: 2×)
- kWh meters (2×)
- SSR channels (4×)
- Total activity LEDs: **12**
- Resistors: **220–330 Ω**

---

## 6. Electrical design rules

### 6.1 I²C

- Two × **PCA9554PW** expanders + LCDs + **PCA9615**
- Pull-ups: **4k7** per segment
- Keep I²C traces short and grouped
- Differential I²C isolated from SSR area

### 6.2 SSR area

- Keep SSR traces away from logic
- Add **100 nF** near each PN2222A
- Add **ferrite bead** on Pi 5 V rail
- Add **TVS diode** on 12 V input

### 6.3 Safety

- EN 60335-2-53 considerations
- No mains on PCB
- Clear separation between logic and SSR area
- 12 V monitoring must be fail-safe
- Sauna remains **hard-locked** until manual reset via UI/software

---

## 7. Functional placement plan (85 × 56 mm)

### 7.1 Left edge — Raspberry Pi interface zone

- 40-pin Pi header
- HDMI Type A (SPI for e-ink)
- Pi 5 V power connector (optional)
- Keep HDMI traces short
- Lock HDMI nets before Freerouting

### 7.2 Top edge — logic and I²C zone

- **PCA9554PW Expander A** (meters + doors + kWh)
- **PCA9554PW Expander B** (buttons + LCD)
- PCA9615
- I²C connectors (JST XH)
- Decoupling capacitors
- Pull-ups
- Test pads for I²C

### 7.3 Right edge — field inputs zone (JST XH)

- Door sensors
- Water meters bathroom 1 and 2
- kWh meters
- Buttons
- Activity LEDs

### 7.4 Bottom edge — power and SSR zone

- Screw terminals for **12 V input**
- TVS diode
- PN2222A transistors (4×)
- Base resistors (470 Ω + 10k pulldown)
- JST XH connectors for SSR outputs
- Ground pour for noise control
- Physical isolation from logic area

### 7.5 Center — routing and keep-out

- Keep center open for routing
- Maintain separation between HDMI/SPI, I²C, SSR, 12 V monitoring
- Freerouting only for non-HDMI nets

---

## 8. Manufacturing requirements (JLCPCB)

### 8.1 PCB specs

| Parameter | Value |
|---|---|
| Material | FR-4 |
| Layers | 2 |
| Size | 85 × 56 mm |
| Thickness | 1.6 mm |
| Surface finish | ENIG |
| Soldermask | Green |
| Silkscreen | White |
| Vias | Tented |
| Min drill | 0.3 mm |

### 8.2 DRC rules (Konnect)

| Rule | Value |
|---|---|
| Track width | 0.25 mm |
| Clearance | 0.2 mm |
| Via diameter | 0.6 mm |
| Via drill | 0.3 mm |
| Copper-to-edge | 0.25 mm |
| Text height | ≥ 1.0 mm |
| Mask clearance | 0.05 mm |

---

## 9. Summary

This document is the electrical, mechanical, and functional requirements for **wanos-pcb-v1**.

Detail supplements:

| Doc | Content |
|---|---|
| [`component-selection.md`](component-selection.md) | JLCPCB parts, footprints, BOM |
| [`hdmi-spi-eink.md`](hdmi-spi-eink.md) | WISC e-ink HDMI→SPI mapping |
| [`io-expander-map.md`](io-expander-map.md) | PCA9554 net map (pre-R1 locks) |
| [`projects/wanos-board/components.xlsx`](../projects/wanos-board/components.xlsx) | Assembly BOM seed |

Konnect + KiCad 10 provide automation for placement, routing, DRC, Freerouting, audits, and manufacturing export.
