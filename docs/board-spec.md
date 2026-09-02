<!-- --- file: docs/board-spec.md -->

# WanOS PCB — board specification

**Revision:** **wanos-pcb-v1** (first-generation WanOS carrier; replaces ad-hoc / **WISC**-era wiring on a new board — not a spin of the old WISC PCB).

Structured specification for KiCad 10 + Konnect, manufactured via JLCPCB. **Target:** **Raspberry Pi 4** on **85 × 56 mm** outline (WISC 2.6.4 mechanical reference).

**Related:** Overview → [`board-overview.md`](board-overview.md) · Components → [`component-selection.md`](component-selection.md) · Field wiring → [`field-wiring.md`](field-wiring.md) · HDMI→SPI → [`hdmi-spi-eink.md`](hdmi-spi-eink.md) · I/O map → [`io-expander-map.md`](io-expander-map.md) · GPIO contracts → [`gpio-interface.md`](gpio-interface.md) · Silkscreen → [`reference/silkscreen/README.md`](reference/silkscreen/README.md)

**R1 locks:** 2026-09-01 · **R2 locks:** 2026-09-01 — [`todo/_archive/phaseR-requirements.md`](todo/_archive/phaseR-requirements.md) § R2 shipped summary.

---

## 1. System overview

WanOS is a Raspberry-Pi-based home-automation controller for sauna, bathroom, cinema, and water systems.

**wanos-pcb-v1** provides:

- Digital inputs (doors, water meters, kWh meters, buttons) via **PCA9554** expanders
- **SHT31** temperature/humidity (4×) via **TCA9546A** mux + Cat5 plant cables
- SSR control outputs (3-phase sauna + IR)
- **12 V** sauna rail monitoring (optocoupler hard-lock)
- **1×** I²C LCD header (two displays paralleled)
- E-ink display via repurposed HDMI connector (WISC SPI)
- Status and activity LEDs

**Board size:** **85 × 56 mm** (Pi-compatible outline; **not** a HAT stack).

**Software note:** Operator continues **WanOS on WISC** until **wanos** is updated for this board. **One Pi** replaces the former two-Pi WISC split. GPIO / I²C map → [`gpio-interface.md`](gpio-interface.md).

---

## 2. Power architecture

### 2.1 Rails

#### 5 V (stable, independent)

- Powers Raspberry Pi
- Powers logic (PCA9554PW, TCA9546A, LEDs, I²C sensors on local bus)
- Must **remain powered** when sauna safety triggers
- External **5 V** via **J17** screw terminal → WISC-style conditioning → **`+5VA`**
- **Pi** fed via **J40** header pins **2 & 4** (header injection; **J41** USB-C **DNP** v1)

#### 12 V (sauna SSR rail)

- Powers SSR opto-inputs
- Cut by external temperature safety
- Must be **monitored** by the PCB
- Loss of 12 V → Pi stays alive → WanOS logs critical event + stops sauna
- Sauna remains **hard-locked** until manual reset via UI/software

### 2.2 12 V monitoring (R1 lock)

Optocoupler (**U4**) → **Expander B P6** (`EXP_B_P6_12V_MON`).

- 12 V → **R32 1k5** → optocoupler LED
- Transistor → pull-up to 3.3 V → **Expander B pin P6**
- Optional RC: 10 kΩ + 100 nF
- Part: **PC817A** class (see [`reference/datasheets/pc817a.pdf`](reference/datasheets/pc817a.pdf))

**Logic:** LOW = 12 V present; HIGH = 12 V missing → hard-lock.

---

## 3. Inputs

### 3.1 Door sensors

- **2×** 2-pin JST (**J2** sauna, **J3** bathroom) — pin 1 GND, pin 2 signal
- Reed switches, 100 nF debounce, **Expander A** P1/P0

### 3.2 Water meters — bathroom 1 and 2

- **J4**, **J5** — 6-pin JST each (cold + hot)
- **Expander A** P2–P5; activity LEDs **1k0** (R17–R28)

### 3.3 kWh counters (main + aux)

- **J6**, **J7** — 2× 2-pin JST
- **Expander A** P6 (main), P7 (aux); activity LEDs

### 3.4 Buttons (sauna LCD)

- **J8** — 4-pin JST (3 buttons + GND); Cat5 UTP harness
- **Expander B** P0–P2; pinout → [`field-wiring.md`](field-wiring.md) § 5

### 3.5 SHT31 sensors (4×)

- Bathroom, cinema, sauna mid, sauna high
- **TCA9546A** (**U5**) @ **`0x70`** — one mux channel per sensor
- **J9–J12** — 4× 4-pin JST, WISC **2.6.4 J7** I²C pinout
- **~4–5 m Cat5** per sensor; all modules at I²C **`0x44`**
- **100 kHz** Standard mode; **no PCA9615** on v1
- Detail → [`field-wiring.md`](field-wiring.md) § 7

---

## 4. Outputs

### 4.1 SSR channels (4×)

- 3 sauna phases + 1 IR
- **Pi GPIO** → 470 Ω → **PN2222A** (**Q1–Q4** field, **Q5** master safety BCM4) → external SSR
- **J13** — **5-pin** JST vertical (**WISC J1** parity); pin **1** = **GND**
- 12 V SSR opto supply; software PWM ~1–5 Hz on sauna phases

### 4.2 E-ink (HDMI → SPI)

See [`hdmi-spi-eink.md`](hdmi-spi-eink.md). Panel **+5 V** (HDMI pin **18**) via **F2** 500 mA polyfuse from **`+5VA`**.

### 4.3 LCD (2× modules, 1× header)

- **J16** — single **4-pin** I²C JST; both LCD tails wired in parallel (deployed practice)
- WISC **2.6.4 J7** pinout; distinct backpack I²C addresses required
- **No second LCD header on v1**

### 4.4 Pi power

- **J17** — **KF301-2P** screw terminal: external **5 V** in (+ / GND)
- Conditioning (WISC 2.6.4): **F1** 2 A, **D2** `1N4001`, **D1** `BZX85C5V6`, **FB1** ferrite → **`+5VA`**
- **J40** 40-pin header — **+5VA** on pins **2 & 4** powers Pi; remaining pins = GPIO / I²C / SSR / e-ink
- **J41** USB-C — **DNP** v1 (not populated)

---

## 5. Indicator LEDs

**15** visible indicators (3 status + 12 activity). **No** activity LED on **master safety** SSR (BCM 4). **Four** SSR activity LEDs (**IR** + phases **U/V/W**) on **J13** channels.

### 5.1 Status (dim)

Resistors: **R29**, **R31** = **2k0** (5 V rails); **R30** = **6k8** (12 V — matched brightness).

| LED | Indicates |
|---|---|
| 5 V in | **`+5VA`** post-**F1** (PSU + fuse OK) |
| 12 V | **+12VA** at **J14** |
| 5 V Pi | **`+5VA`** at **J40** pin **2** |

### 5.2 Activity

Resistors **R17–R28** = **1k0**.

| Group | Count | Signals |
|---|---:|---|
| Doors | 2 | J2 sauna, J3 bathroom |
| Water B1 / B2 | 4 | J4–J5 cold + hot |
| kWh | 2 | J6 main, J7 aux |
| SSR (J13) | 4 | IR, phase U, V, W |

---

## 6. Electrical design rules

### 6.1 I²C

- **PCA9554PW × 2**, **TCA9546A**, **J16** LCD tap on **local bus**
- Pull-ups: **2k2** on **SCL** and **SDA** only (**R9**, **R10**)
- **100 kHz**; keep I²C away from SSR/12 V zone

### 6.2 SSR area

- 100 nF near each PN2222A; ferrite on Pi 5 V; **SMBJ12A** on 12 V input

### 6.3 Safety

- EN 60335-2-53 context; no mains on PCB
- 12 V monitor fail-safe; hard-lock until manual reset

---

## 7. Functional placement (85 × 56 mm)

| Zone | Content |
|---|---|
| **Left** | Pi **J40**, HDMI **J1**, **J17** 5 V screw |
| **Top** | U1, U2, U5, I²C pull-ups, **J16**, **J9–J12**, decoupling |
| **Right** | **J2–J8** field inputs, activity LEDs |
| **Bottom** | **J14** 12 V, **J13** SSR, Q1–Q4, U4 opto, TVS |
| **Center** | Routing keep-out; lock HDMI before Freerouting |

Silkscreen font → [`reference/silkscreen/README.md`](reference/silkscreen/README.md).

---

## 8. Manufacturing (JLCPCB)

| Parameter | Value |
|---|---|
| Layers | 2 |
| Size | 85 × 56 mm |
| Thickness | 1.6 mm |
| Finish | ENIG |
| Soldermask | Green |
| Silkscreen | White; **`wanos-pcb-v1.0`** + Wannes logos — [`reference/silkscreen/README.md`](reference/silkscreen/README.md) |
| Min text height | ≥ 1.0 mm |

DRC → [`projects/wanos-board/constraints.md`](../projects/wanos-board/constraints.md).

**JLCPCB assembly (R2):** full **PCBA** — SMD + through-hole (**J40**, JST, **J14**, HDMI **J1**) unless revised at **Ops2/J1**.

---

## 9. Summary

| Doc | Content |
|---|---|
| [`field-wiring.md`](field-wiring.md) | JST pinouts, Cat5, mux channels |
| [`component-selection.md`](component-selection.md) | Parts and footprints |
| [`external-plant.md`](external-plant.md) | Off-board SSR + 12 V plant |
| [`grounding.md`](grounding.md) | Ground / return scheme |
| [`gpio-interface.md`](gpio-interface.md) | Pi BCM + software strategy |
| [`io-expander-map.md`](io-expander-map.md) | Expander + mux map |
| [`components.xlsx`](../projects/wanos-board/components.xlsx) | BOM seed |

Konnect + KiCad 10 for schematic, layout, DRC, and fab export.
