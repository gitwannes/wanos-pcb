<!-- --- file: docs/field-wiring.md -->

# wanos-pcb-v1 — field wiring and JST pinouts

Locked **R1** (2026-09-01) + **R2** (2026-09-01). Canonical electrical behaviour → [`board-spec.md`](board-spec.md). Connector designators → [`projects/wanos-board/components.xlsx`](../projects/wanos-board/components.xlsx).

**WISC reference pinout for all 4-pin I²C JST:** WISC **2.6.4** board **J7** (not 2.5.3 SHT11 DATA/CLOCK headers).

**KiCad schematic sheets:** **J14** + **J17** + **J40** → **`pi_power.kicad_sch`**. Field JST **J2–J3**, **J6–J8** → **`connectors.kicad_sch`**. Water **J4** (RJ45) + YF front-end / TVS → **`water_meters.kicad_sch`**. **J13** → **`ssr_drivers.kicad_sch`**. **J9–J12**, **J16** → **`i2c_plant.kicad_sch`**. **J1** → **`hdmi_spi.kicad_sch`**. Door/kWh activity LEDs → **`io_expanders.kicad_sch`**; water activity LEDs → **`water_meters.kicad_sch`**.

---

## 1. Standard 4-pin I²C JST (XH)

Used on **J9–J12** (SHT31 plant) and **J16** (LCD).

| Pin | Signal | Notes |
|---:|---|---|
| **1** | **GND** | Common return |
| **2** | **SDA** | Pi I²C data (BCM2) on local bus |
| **3** | **SCL** | Pi I²C clock (BCM3) on local bus |
| **4** | **+3V3** | Sensor / LCD module supply |

Verified from WISC `wisc2-6-4.kicad_pcb` **J7** pad nets.

---

## 2. Standard 2-pin pulse / door JST

Used on **J2–J3** (doors), **J6–J7** (kWh). Matches WISC 2.5.3 production practice.

| Pin | Signal |
|---:|---|
| **1** | **GND** |
| **2** | **Pulse / reed signal** (to expander input, 10k pull-up on PCB) |

---

## 2a. Water meters — J4 (RJ45) + YF-B6/B10 over Cat5 (~10 m)

**Sensor:** YF-B6 / YF-B10 hall flow meter — datasheet [`reference/datasheets/external/YF-B6 B10 waterflow-sensor.pdf`](reference/datasheets/external/YF-B6%20B10%20waterflow-sensor.pdf).

| Spec | Value |
|---|---|
| Supply | **DC 5–15 V** (min **4.5 V**) → board **`+5VA`** |
| Output | **Open-drain** (requires pull-up) — yellow wire |
| Wires (sensor) | Red **VDD**, black **GND**, yellow **SIG** |
| Rate | \(F = 6.6 \times Q\) (L/min) → ~7–200 Hz |
| Field cable | **One Cat5/Cat5e UTP** (~**10 m**) → board **J4** RJ45 (8P8C) |

**No MOSFET / opto** on v1 — OD + pull-up to **`+3V3`** is level-safe into PCA9554.

**On-board front-end** (sheet **`water_meters.kicad_sch`**), per SIG channel:

| Element | Value | Role |
|---|---|---|
| **TVS** | **PESD5V0S1BA** (**D25**–**D28**) | ESD / surge clamp SIG → **GND** (long Cat5) — [`pesd5v0s1ba.pdf`](reference/datasheets/pesd5v0s1ba.pdf) |
| **Rpu** | **10 kΩ** → **`+3V3`** | Idle HIGH |
| **Rs** | **330 Ω** | Series field → expander |
| **Cd** | **100 nF** | Debounce / EMI (\(\tau \approx 1\,\text{ms}\)) |
| **Rled + D** | **1k0** + LED | Activity (lights on pulse / SIG low) |

Plus **D29** **SMBJ5.0A** across **`+5VA`** → **GND** at **J4** (sensor supply clamp) — [`smbj5.0a.pdf`](reference/datasheets/smbj5.0a.pdf).

**J4** — TE Connectivity **5556416-1** (LCSC **C86492**): RJ45 8P8C **TH**, **no LED**, **no magnetics**, unshielded. Schematic uses `Connector_Generic:Conn_01x08` + footprint **`Connector_RJ:RJ45_Amphenol_54602-x08_Horizontal`** (Amphenol **54602** land-pattern class — [`amphenol-54602.pdf`](reference/datasheets/amphenol-54602.pdf), [`amphenol-54602-drawing.pdf`](reference/datasheets/amphenol-54602-drawing.pdf)). JLC assembly: **wave soldering**.

Optional Cat5 foil/drain: bond at enclosure / PE (jack has no SH tabs) — [`grounding.md`](grounding.md).

### Cat5 wiring (T568B) — recommended

Colour cheat-sheet: [`reference/datasheets/rj45-t568b-wiring-colors.jpg`](reference/datasheets/rj45-t568b-wiring-colors.jpg).

| J4 pin | T568B wire | Pair | Net | Field / sensor |
|---:|---|---|---|---|
| **1** | White/Orange | 2 | `WM_B1_COLD` | Bath 1 cold yellow |
| **2** | Orange | 2 | **GND** | Bath 1 cold black (pair return) |
| **3** | White/Green | 3 | `WM_B1_HOT` | Bath 1 hot yellow |
| **6** | Green | 3 | **GND** | Bath 1 hot black (pair return) |
| **4** | Blue | 1 | **`+5VA`** | All reds (VDD) |
| **5** | White/Blue | 1 | **GND** | Extra / common black return |
| **7** | White/Brown | 4 | `WM_B2_COLD` | Bath 2 cold yellow |
| **8** | Brown | 4 | `WM_B2_HOT` | Bath 2 hot yellow |

**Bath 2 blacks:** splice to any **GND** conductor (pins **2** / **5** / **6**). **Bath 2** cold+hot share pair 4 (OK at ~7–200 Hz); do not leave unused pair conductors floating at the board end — they are already assigned.

**Shielded Cat5 (optional):** jack is **unshielded** — bond foil/drain to enclosure **PE** / chassis at **board end only** (not both ends).

| Net | Expander |
|---|---|
| `WM_B1_COLD` / `WM_B1_HOT` | **U1** P2 / P3 |
| `WM_B2_COLD` / `WM_B2_HOT` | **U1** P4 / P5 |

**J5** is **unused** on v1 (former second water JST — collapsed into **J4**).

---

## 3. Connector map (J designators)

| Ref | Pins | Function | Cable notes |
|---|---:|---|---|
| **J1** | HDMI | E-ink SPI | See [`hdmi-spi-eink.md`](hdmi-spi-eink.md) |
| **J2** | 2 | Door sauna | |
| **J3** | 2 | Door bathroom | |
| **J4** | 8 (RJ45) | Water meters B1+B2 | Cat5 ~10 m — § 2a |
| **J5** | — | **Unused v1** | Former water JST; collapsed into **J4** |
| **J6** | 2 | kWh main | |
| **J7** | 2 | kWh aux | Full-board feature |
| **J8** | 4 | Sauna LCD buttons | Cat5 UTP — § 5 |
| **J9** | 4 | SHT31 bathroom | Mux **ch 0**, Cat5 ~4–5 m |
| **J10** | 4 | SHT31 cinema | Mux **ch 1** |
| **J11** | 4 | SHT31 sauna mid | Mux **ch 2** |
| **J12** | 4 | SHT31 sauna high | Mux **ch 3** |
| **J13** | 5 | SSR field | § 6 |
| **J14** | 2 | 12 V in (KF301) — **`+12V`** + GND · schematic: **`pi_power`** | § 9 |
| **J16** | 4 | LCD I²C (both screens) | § 4 |
| **J17** | 2 | **5 V screw in** (KF301) — external PSU + / GND · schematic: **`pi_power`** | § 10 |
| **J40** | 40 | Pi header | |
| **J41** | — | USB-C | **DNP v1** |

---

## 4. LCD — one 4-pin header (J16)

Both LCD modules share **one** JST: tails are wired **in parallel** at the harness (same as deployed WISC/LCD practice).

- **Pinout:** § 1 (4-pin I²C).
- **Addresses:** each LCD backpack must use a **different I²C address** (typical jumper: `0x27` vs `0x3F`).
- **v1:** single **J16** only — no second LCD header.

---

## 5. Sauna buttons — Cat5 UTP to J8 (4-pin)

Board: expander inputs with pull-up; button shorts to **GND** when pressed.

**J8 (pin 1 = square pad):**

| J8 pin | Signal | Cat5 (T568B) | Button end |
|---:|---|---|---|
| **1** | **GND** | Brown + Brown/white (tie together) | Common return |
| **2** | **BTN1** | Orange/white | Switch to GND |
| **3** | **BTN2** | Green/white | Switch to GND |
| **4** | **BTN3** | Blue/white | Switch to GND |

Leave Orange, Green, Blue solids unconnected (or tie to GND at PCB end only).

---

## 6. SSR — J13 (5-pin field header)

**Connector:** **B5B-XH-A 1×05** vertical on **`ssr_drivers.kicad_sch`**.

| Pin | Signal | wanos channel |
|---:|---|---|
| **1** | **GND** | Control return |
| **2** | `SSR_PHASE_W` | Sauna phase W |
| **3** | `SSR_PHASE_V` | Sauna phase V |
| **4** | `SSR_PHASE_U` | Sauna phase U |
| **5** | `SSR_IR` | IR relay |

**Safety gate:** **BCM 4** → on-board **Q5** / **`SAFETY_BUS`** — **not** on this header. See [`board-spec.md`](board-spec.md) § 4.1.

**Harness reuse:** a legacy 5-pin SSR tail may plug in if its pinout matches this table ([`external-plant.md`](external-plant.md) § 5).

---

## 9. 12 V input — J14 (KF301-2P)

Schematic: **`pi_power.kicad_sch`** (with **D3** SMBJ12A TVS at entry).

| Pin | Signal |
|----:|--------|
| **1** | **`+12V`** — after external temp safety |
| **2** | **GND** |

Detail → [`external-plant.md`](external-plant.md) § 3.

---

## 10. 5 V input — J17 (KF301-2P)

Schematic: **`pi_power.kicad_sch`**.

| Pin | Signal |
|----:|--------|
| **1** | **+5V** — external PSU positive (before on-board conditioning) |
| **2** | **GND** |

On-board chain: **F1** 2 A polyfuse (resettable) → **Q6** ideal diode → **D1** overvoltage clamp → **`+5VA`** → **FB1** → **`+5V-PI`** → **J40** pins **2 & 4** (Pi header 5 V injection).

**J41** USB-C is **not populated** on v1.

---

## 7. SHT31 plant — Cat5 per sensor

- **4×** separate Cat5 runs (~**4–5 m** each), one **4-pin JST** per sensor (**J9–J12**).
- **TCA9546A** (U5) on PCB @ I²C **`0x70`** — select channel, then poll SHT31 at **`0x44`** (all modules use default address).
- **No PCA9615** on v1 — direct I²C through mux per channel.
- **Pull-ups:** **2k2** on main `I2C_SCL` / `I2C_SDA` only (**R9**, **R10**) — sized for ~5 m Cat5 @ 100 kHz.

**Migration from WISC SHT11:** old 4-pin plant headers used pin 2 = **CLOCK**, pin 3 = **DATA**. I²C uses pin 2 = **SDA**, pin 3 = **SCL** — re-pin at the board end or replace tails.

| Mux ch | JST | Location |
|---:|---|---|
| 0 | J9 | Bathroom |
| 1 | J10 | Cinema |
| 2 | J11 | Sauna mid |
| 3 | J12 | Sauna high |

---

## 8. I²C pull-ups (R1 lock)

| Ref | Value | Net |
|---|---|---|
| **R9** | **2k2** | `I2C_SCL` → 3.3 V |
| **R10** | **2k2** | `I2C_SDA` → 3.3 V |

Do not populate extra pull-up pairs on the same segment. Disable Pi internal I²C pull-ups when relying on board resistors.

---

## Related

- [`io-expander-map.md`](io-expander-map.md) — expander pin map
- [`gpio-interface.md`](gpio-interface.md) — software views
- WISC summaries → [`reference/wisc-board/`](reference/wisc-board/)
- External plant → [`external-plant.md`](external-plant.md) · Grounding → [`grounding.md`](grounding.md)
