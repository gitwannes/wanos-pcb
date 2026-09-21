<!-- --- file: docs/external-plant.md -->

# wanos-pcb-v1 — external plant (off-board)

Off-board wiring for sauna **12 V DC plant**, **DIN SSRs**, and independent **temperature safety**. Locked at **R2** (2026-09-01).

**On-board connectors:** [`field-wiring.md`](field-wiring.md) · **Ground returns:** [`grounding.md`](grounding.md) · **Board spec:** [`board-spec.md`](board-spec.md)

**Datasheets:** SSR → [`reference/datasheets/external/omron-g3pj.pdf`](reference/datasheets/external/omron-g3pj.pdf) · kWh meters → § 5a · pack index → [`reference/datasheets/README.md`](reference/datasheets/README.md)

---

## 1. Overview

| Item | Role |
|---|---|
| **12 V PSU** | Sauna SSR **coil** supply (not Pi logic) |
| **Temp safety** | Independent hardware — **cuts 12 V** on overtemperature; **not** controlled by WanOS |
| **wanos PCB** | Monitors 12 V (opto **U4**); drives **4×** SSR coil returns via **J13**; **BCM 4** on-board safety gate (**Q5**) |
| **4× DIN SSR** | Switch **mains** heater / IR loads — **not** on PCB |

---

## 2. External SSR modules

**Part (locked):** **Omron G3PJ-225B DC12-24** × **4** on DIN rail.

| wanos channel | J13 pin | Typical load |
|---|---:|---|
| Sauna phase **W** | 2 | Heater phase W |
| Sauna phase **V** | 3 | Heater phase V |
| Sauna phase **U** | 4 | Heater phase U |
| **IR** relay | 5 | IR / auxiliary heater |

**J13 pin 1** = **GND** (control return). Pinout → [`field-wiring.md`](field-wiring.md) § 6.

### Coil wiring (DC 12 V)

- **Coil +** (all four modules): common **`+12V`** from PCB (same rail as **J14** after field safety).
- **Coil −** (each module): individual return via **J13** pins 2–5 — PCB sinks current through **PN2222A** when the matching Pi GPIO is active.
- Coil rating **12–24 V DC** — site uses **12 V** plant.

### AC load

- Mains connections **only** at SSR **load** terminals — qualified installer; **no mains** on wanos PCB.

### On-board safety gate (BCM 4)

WanOS **arms** the four field SSR drivers by asserting **BCM 4** high. That turns **Q5** on and pulls the shared **`SAFETY_BUS`** (emitters of **Q1–Q4**) toward **GND**, so the field GPIOs can sink coil current when active.

- **R16** (10 kΩ **`+5VA`** → **`SAFETY_BUS`**) holds the bus high when **Q5** is off.
- There is **no** fifth G3PJ module and **no** safety coil net on **J13**.
- Independent **12 V** hard-lock: external temp safety + opto **U4** on **`pi_power`** (§ 3) — separate from **BCM 4** / **Q5**.

---

## 3. 12 V plant — J14

**J14** — **KF301-2P** screw terminal on **`pi_power.kicad_sch`** (with **D3** TVS at entry).

| Pin | Signal |
|----:|--------|
| **1** | **`+12V`** — 12 V **after** external temp safety |
| **2** | **GND** — 12 V return |

### Field wiring

```text
PSU (+) ---> [external temp safety - NC] ---> J14-1 (+12V)
PSU (-)  -----------------------------------> J14-2 (GND)
```

When safety opens, **`+12V`** at **J14** falls to **0 V** → opto **U4** on **`pi_power`** → **EXP_B_P6** → WanOS **hard-lock** (Pi / 5 V stay up).

---

## 4. Temperature safety (independent)

- **Not** implemented on wanos PCB.
- Site **over-temperature** device breaks the **12 V positive** path **before** **J14** (series insert).
- WanOS **does not** control this interlock; it only **detects** loss of 12 V.

---

## 5. Harness reuse (migration from WISC)

| Harness | Reuse |
|---|---|
| **SSR J1 → J13** | Reuse if 5-pin JST tail fits (same pinout) |
| **Doors, water, kWh** | Reuse where pinout matches; water is **YF-B6/B10** on **one Cat5** → **J4** RJ45 — [`field-wiring.md`](field-wiring.md) § 2a (not legacy dual 6-pin JST) |
| **SHT11 plant → SHT31** | Re-terminate or replace tails (**SDA/SCL** vs DATA/CLOCK) — [`field-wiring.md`](field-wiring.md) § 7 |
| **Two-Pi WISC** | **One Pi** on wanos-pcb-v1 (I/O + e-ink integrated) |

---

## 5a. kWh meters (plant inventory)

Site may have **more than two** energy meters. **Not all need a pulse run to wanos.** PCB has **two** pulse inputs (**J6** main, **J7** aux) — wiring and software map → [`field-wiring.md`](field-wiring.md) § 2b · [`board-spec.md`](board-spec.md) § 3.3.

This section is **plant reference** (which devices exist / how their S0 ports behave). It does **not** lock which meter is on which JST.

| Part | Role (typical) | Datasheet | Pulse / S0 (from datasheet) | Notes vs wanos **J6/J7** (`+5VA` pull-up) |
|---|---|---|---|---|
| **Eastron SDM72D-M** | 3-ph / multi-param DIN meter (also RS485 Modbus) | [`sdm72d-m.pdf`](reference/datasheets/external/sdm72d-m.pdf) | Configurable pulse; default **1000 imp/kWh**; passive opto needs external DC | **Design reference** for the drawn front-end (docs historically used **5–27 V**, ~**27 mA**, ~**35 ms**). Compatible with **`+5VA`** rail class. |
| **Sibratec DDS-1Y-18L** | 1-ph DIN, LCD, pulse for PLC | [`dds-1y-18l.pdf`](reference/datasheets/external/dds-1y-18l.pdf) | Specs: **2000 /kWh**, width **~90 ms**; PLC use **10–30 V DC**, **~27 mA** (limits also cite max **60 V DC** / **50 mA**); terminals **20/21**; ≤**20 m** without amp | **Do not assume** drop-in on **`+5VA`**: published operating band starts at **10 V**. Faceplate text shows **1000 imp/kWh** while body text says **2000** — confirm on the physical unit before software constants. |
| **Finder 7E.12.8.230.0002** | 1-ph 10(25) A, 2-module, SO open-collector (DIN **43864**) | [`finder-7e.12.8.230.0002.pdf`](reference/datasheets/external/finder-7e.12.8.230.0002.pdf) | External **5–30 V DC**, max **20 mA**; SO **2000 imp/kWh**, pulse **~100 ms** (7E.12 row); cable up to **1000 m** at 30 V / 20 mA | Voltage class **OK** with **`+5VA`**. Imp/kWh and pulse width differ from SDM72 defaults — software must match the wired meter. |

**wanos pulse class:** passive / SO open-collector, polarity-aware, idle open, pulse closes to return — same electrical story as § 2b. **Modbus** on the SDM72 is plant-side only on v1 (no RS485 on the carrier).

---

## 6. Safety assumptions (EN 60335-2-53 context)

Informal hardware assumptions only — **not** a compliance sign-off.

| Topic | Assumption |
|---|---|
| Heater power | External **DIN SSRs**; no mains on wanos PCB |
| Over-temperature | **Independent** device cuts **12 V** off-board |
| WanOS | Logic + monitoring; **hard-lock** when 12 V missing; manual reset via UI |
| Formal CE / product marking | **Operator responsibility** — out of scope for this repo |

---

## 7. Cabinet environment

PCB in **low-voltage control cabinet** (not in hot steam zone). **No** conformal coat on v1. External thermal cutoff remains off-board (§ 4).

---

## Related

- [`grounding.md`](grounding.md)
- [`gpio-interface.md`](gpio-interface.md)
- Legacy production reference → [`reference/wisc-board/`](reference/wisc-board/) (intent / migration only)
