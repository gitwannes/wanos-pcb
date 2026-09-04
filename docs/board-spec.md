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
- External **5 V** via **J17** screw terminal → input conditioning → **`+5VA`**
- **Pi** fed via **J40** header pins **2 & 4** (header injection; **J41** USB-C **DNP** v1)

#### 12 V (sauna SSR rail)

- Powers SSR opto-inputs
- Cut by external temperature safety
- Must be **monitored** by the PCB
- Loss of 12 V → Pi stays alive → WanOS logs critical event + stops sauna
- Sauna remains **hard-locked** until manual reset via UI/software

### 2.2 12 V monitoring (R1 lock)

Optocoupler (**U4**) on **`pi_power.kicad_sch`** → **Expander B P6** (`EXP_B_P6_12V_MON`).

- 12 V (**`+12V`** at **J14**) → **R32 1k5** → optocoupler LED
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

- **Sensor:** **YF-B6 / YF-B10** hall flow meter — OD pulse, supply **5–15 V** ([datasheet](reference/datasheets/external/YF-B6%20B10%20waterflow-sensor.pdf))
- **J4** — TE **5556416-1** RJ45 (LCSC **C86492**); **one Cat5 ~10 m** for all four meters — pinout / colours [`field-wiring.md`](field-wiring.md) § 2a
- **Front-end** on **`water_meters.kicad_sch`**: per channel **PESD5V0S1BA** TVS ([`pesd5v0s1ba.pdf`](reference/datasheets/pesd5v0s1ba.pdf)), **10 kΩ** pull-up to **`+3V3`**, **330 Ω** series, **100 nF** debounce, activity LED **1k0** — **no MOSFET**; **SMBJ5.0A** on **`+5VA`** at **J4**
- **Expander A** P2–P5 (`EXP_A_P2`…`P5`)
- **J5** unused v1

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

### 4.1 SSR channels (4× field + on-board safety gate)

**External:** 4× **Omron G3PJ-225B** DIN SSRs — coil **+** common **`+12V`**, coil **−** per channel via **J13** pins 2–5 ([`external-plant.md`](external-plant.md)). **No** fifth external SSR.

**On-board drivers** (`ssr_drivers.kicad_sch`):

| Ref | Role | BCM |
|---|---|---:|
| **Q5** | Safety gate — arms field drivers when on | **4** |
| **Q4** | IR coil return | **14** |
| **Q3** | Sauna phase U | **15** |
| **Q2** | Sauna phase V | **17** |
| **Q1** | Sauna phase W | **18** |

**Hardware safety interlock** (not a fifth SSR coil):

- **Q5** (**PN2222A**): emitter **GND**, collector **`SAFETY_BUS`** (shared with **Q1–Q4** emitters).
- **Q1–Q4**: emitters on **`SAFETY_BUS`**; collectors on **`SSR_*`** → **J13** pins 2–5.
- **BCM 4** high → **Q5** on → **`SAFETY_BUS`** pulled toward GND → field GPIOs can sink coil current.
- **BCM 4** low → **`SAFETY_BUS`** floats high via **R16** (10 kΩ to **`+5VA`**) → field drivers cannot energize coils even if GPIO 14/15/17/18 are high.
- **R14** 470 Ω (**GPIO_SSR_SAFETY** → **Q5** base), **R15** 10 kΩ base pulldown to **GND**.
- **No** on-board activity LED on the safety path (§ 5).

**Field channels:** **Pi GPIO** → **R1–R4** 470 Ω → **Q1–Q4** bases; **R5–R8** 10 kΩ base–emitter on each channel.

**J13** — **5-pin** JST vertical (**B5B-XH-A**); pin **1** = **GND** — [`field-wiring.md`](field-wiring.md) § 6.

**Decoupling:** **C8–C12** 100 nF collector–emitter per **Q1–Q5**.

**SSR activity LEDs:** **D19–D22** / **R25–R28** on this sheet (§ 5.3).

12 V SSR opto supply; software PWM ~1–5 Hz on sauna phases.

### 4.2 E-ink (HDMI → SPI)

See [`hdmi-spi-eink.md`](hdmi-spi-eink.md). Panel **+5 V** (HDMI pin **18**) via **F2** 500 mA polyfuse from **`+5VA`**.

### 4.3 LCD (2× modules, 1× header)

- **J16** — single **4-pin** I²C JST; both LCD tails wired in parallel (deployed practice)
- WISC **2.6.4 J7** pinout; distinct backpack I²C addresses required
- **No second LCD header on v1**

### 4.4 Pi power

- **J17** — **KF301-2P** screw terminal: external **5 V** in (+ / GND)
- Conditioning: **F1** 2 A polyfuse (SMD 1206, resettable), **Q6** `AO3401A` ideal diode (reverse block, ~mΩ drop), **D1** `BZT52C5V6` (overvoltage shunt), **C1** 100 µF bulk, **FB1** ferrite → **`+5VA`** / **`+5V-PI`** at **J40**
- **J40** 40-pin header — **`+5V-PI`** on pins **2 & 4** powers Pi (post-**FB1**); remaining pins = GPIO / I²C / SSR / e-ink
- **J41** USB-C — **DNP** v1 (not populated)

---

## 5. Indicator LEDs

**14** visible indicators (2 status + 12 activity). **No** activity LED on the **BCM 4** / **Q5** safety path. **Four** SSR activity LEDs (**IR** + phases **U/V/W**) on **J13** channels.

### 5.1 Status (dim)

On **`pi_power.kicad_sch`**. Resistors: **R29** = **2k0** (**+5VA**); **R30** = **6k8** (**+12V** — matched brightness).

| LED | Indicates |
|---|---|
| 5 V in | **`+5VA`** post-**F1** (PSU + polyfuse OK; self-resets after overcurrent) |
| 12 V | **`+12V`** at **J14** (external PSU input, after field temp safety) |

**D25** dropped — was a duplicate **`+5VA`** indicator (same rail as **D23**).

### 5.2 Field input activity

**Eight** LEDs total, resistors **1k0**, anode on **`+3V3`**, cathode on the logic/input net (lights when input is low).

| Group | Count | LEDs / R | Sheet | Signals |
|---|---:|---|---|---|
| Doors | 2 | D11–D12 / R17–R18 | `io_expanders.kicad_sch` | J2 sauna, J3 bathroom |
| Water B1 / B2 | 4 | D13–D16 / R19–R22 | `water_meters.kicad_sch` | **J4** RJ45 cold + hot ×2 |
| kWh | 2 | D17–D18 / R23–R24 | `io_expanders.kicad_sch` | J6 main, J7 aux |

### 5.3 SSR activity (`ssr_drivers.kicad_sch`)

**Four** LEDs (**D19–D22**), resistors **R25–R28** = **1k0** (target **2k0** when all indicators move to **`+5VA`** — see § 5.1), anode on **`+5VA`**, cathode on **`SSR_*`** (12 V coil-return domain).

| LED | R | Net | Driver |
|---|---|---|---|
| D22 | R28 | `SSR_IR` | **Q4** |
| D21 | R27 | `SSR_PHASE_U` | **Q3** |
| D20 | R26 | `SSR_PHASE_V` | **Q2** |
| D19 | R25 | `SSR_PHASE_W` | **Q1** |

When the driver is off, the LED can see **~7 V reverse** (12 V net vs 5 V rail). Typical 0805 indicators are specced under **5 V** reverse — field risk is **indicator failure only**, not SSR switching.

**Further revisions (optional):** add a **series reverse-blocking diode** (e.g. 1N4148 class, SOD-123) in each SSR activity string **only if** bring-up or field use shows LED degradation or failures. **Not required for v1.**

---

## 6. Electrical design rules

### 6.1 I²C

- **PCA9554PW × 2**, **TCA9546A**, **J16** LCD tap on **local bus**
- Pull-ups: **2k2** on **SCL** and **SDA** only (**R9**, **R10** on **`io_expanders.kicad_sch`**)
- VCC decoupling: **C3**/**C4** (PCA9554 **U1**/**U2**), **C6**/**C7** (**U5** mux) — [`io-expander-map.md`](io-expander-map.md) § 6
- **100 kHz**; keep I²C away from SSR/12 V zone

### 6.2 SSR area

- **C8–C12:** 100 nF across collector–emitter of each **Q1–Q5**
- **R16:** 10 kΩ **`+5VA`** → **`SAFETY_BUS`** (field-driver emitter rail)
- Ferrite on Pi 5 V; **SMBJ12A** on 12 V input

### 6.3 Safety

- EN 60335-2-53 context; no mains on PCB
- 12 V monitor fail-safe; hard-lock until manual reset

---

## 7. Functional placement (85 × 56 mm)

| Zone | Content |
|---|---|
| **Left** | Pi **J40**, HDMI **J1**, **J17** 5 V screw |
| **Top** | U1, U2, U5, I²C pull-ups, **J16**, **J9–J12**, decoupling |
| **Right** | **J2–J4**, **J6–J8** field inputs, activity LEDs |
| **Bottom** | **J14** 12 V (**pi_power**), **J13** SSR, **Q1–Q5**, SSR activity **D19–D22**, **U4** opto, **D3** TVS |
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
