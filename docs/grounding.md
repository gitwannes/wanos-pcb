<!-- --- file: docs/grounding.md -->

# wanos-pcb-v1 — grounding and returns

Ground and return scheme for field install. Locked at **R2** (2026-09-01).

**Connectors:** [`field-wiring.md`](field-wiring.md) · **12 V / SSR plant:** [`external-plant.md`](external-plant.md)

---

## 1. Single PCB ground

All of the following tie to **one PCB ground plane** (common **GND**):

- Raspberry Pi **J40** ground pins
- Every field JST **pin 1 GND** (**J2–J3**, **J6–J8**, **J9–J12**, **J13** pin 1)
- Water **J4** RJ45 pins **2**, **5**, **6** (**GND**) + **SH** tabs
- **J14** pin 2 (12 V return)
- HDMI **J1** shields and repurposed GND pins per [`hdmi-spi-eink.md`](hdmi-spi-eink.md)
- **Q5** emitter (safety gate), opto **U4** return
- **Q1–Q4** emitters on **`SAFETY_BUS`** (not direct **GND** — see § 3)

There is **no** separate “signal ground” vs “power ground” on the PCB for v1.

---

## 2. 12 V DC return

- **J14-2** is the **12 V PSU negative** and PCB **GND**.
- **`+12V`** at **J14-1** is **after** the external temp-safety series insert ([`external-plant.md`](external-plant.md) § 3).
- SSR **coil +** common connects to **`+12V`** on-board; coil **−** returns per channel through **J13** to PCB drivers.

---

## 3. SSR control return

- **J13 pin 1** = **GND** for the 5-pin SSR field harness.
- **J13 pins 2–5** = coil **−** returns; each net is sunk by **Q1–Q4** collectors when the matching Pi GPIO is active **and** the safety gate is armed.
- **`+12V`** (common coil **+**) is on-board from **J14** / plant distribution — not on **J13**.

### Safety bus (`SAFETY_BUS`)

On **`ssr_drivers.kicad_sch`**:

| Node | Connection |
|---|---|
| **Q5** emitter | **GND** |
| **Q5** collector | **`SAFETY_BUS`** |
| **Q1–Q4** emitters | **`SAFETY_BUS`** |
| **R16** | **`+5VA`** → **`SAFETY_BUS`** (10 kΩ pull-up) |

**BCM 4** drives **Q5** (**R14** / **R15** on base). When **Q5** is off, **`SAFETY_BUS`** is high and field drivers cannot pull coil returns low. **BCM 4** is on-board only — not routed to **J13**.

Detail → [`board-spec.md`](board-spec.md) § 4.1 · [`external-plant.md`](external-plant.md) § 2.

---

## 4. Pi and 5 V logic

- Pi powered via **J17** external 5 V → on-board **`+5VA`** → **J40** header pins **2 & 4** (**J41** USB-C **DNP** v1).
- **5 V** and **3.3 V** logic return through Pi header **GND** to PCB plane.
- When **12 V** is cut by temp safety, **5 V** to Pi must **remain** (USB / board supply independent of **`+12V`**).

---

## 5. Field cables

| Cable | Ground practice |
|---|---|
| **JST** doors, kWh, buttons | Pin **1** = GND at PCB |
| **Cat5** water (**J4** RJ45) | GND on pins **2** / **5** / **6**; shield → **SH**/GND board end only |
| **Cat5** SHT31 / buttons | Use designated GND pair; do **not** float shield at both ends |
| **Cat5 shield** (if present) | Bond **board end only** to GND unless install standard says otherwise |

---

## 6. Mains and protective earth

- **AC mains** only at **G3PJ load** terminals — off PCB.
- If the **metal enclosure** is tied to **protective earth (PE)**, bond **PE to PCB GND at one point** near **J14** power entry (installer). WanOS does not sense PE.

---

## 7. Layout / noise

- Keep **J14 / J13 / SSR** zone away from **I²C** ([`board-spec.md`](board-spec.md) § 7).
- **FB1** ferrite on Pi **5 V** path ([`component-selection.md`](component-selection.md)).

---

## Related

- [`external-plant.md`](external-plant.md)
- [`board-spec.md`](board-spec.md) § 2
