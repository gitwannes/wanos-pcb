<!-- --- file: docs/gpio-interface.md -->

# wanos-pcb-v1 — GPIO and field interface

**R2 lock (2026-09-01):** full-board **BCM** map for **wanos-pcb-v1** schematic and future WanOS on this PCB.

Field connectors → [`field-wiring.md`](field-wiring.md) · Expander pins → [`io-expander-map.md`](io-expander-map.md) · E-ink HDMI pins → [`hdmi-spi-eink.md`](hdmi-spi-eink.md)

---

## Software strategy

| Phase | WanOS hardware | Notes |
|---|---|---|
| **Today** | **WISC** boards | [wanos `config_hardware.yaml`](https://github.com/gitwannes/wanos/blob/main/config_hardware.yaml) — direct GPIO / SHT11 |
| **Cutover** | **wanos-pcb-v1** | Operator updates **wanos** for expanders, SHT31, HDMI SPI — **all** board functions (**V1a** / main repo) |
| **No adapter** | — | No shim to preserve WISC GPIO map on this PCB |

Historical WISC pin map (reference only) → [§ WISC legacy](#wisc-legacy-reference-only).

---

## Pi BCM — wanos-pcb-v1 (locked)

### I²C bus (local)

| Signal | BCM | Device |
|---|---:|---|
| SDA | **2** | U1, U2, U5, **J16** LCD |
| SCL | **3** | |

**Addresses:** U1 **PCA9554** `0x20` · U2 **PCA9554** `0x21` · U5 **TCA9546A** `0x70`

### SSR outputs (Pi GPIO)

| Signal | BCM | Field / notes |
|---|---:|---|
| Master safety | **4** | On-board — **not** J13 |
| IR relay | **14** | J13 pin **5** |
| Sauna phase U | **15** | J13 pin **4** |
| Sauna phase V | **17** | J13 pin **3** |
| Sauna phase W | **18** | J13 pin **2** |

Software PWM ~1–5 Hz on sauna phases (same intent as WISC).

### E-ink — HDMI J1 → SPI

HDMI **physical pin** → signal per [`hdmi-spi-eink.md`](hdmi-spi-eink.md). **BCM:**

| SPI function | BCM | HDMI pin | Dir |
|---|---:|---:|---|
| DC | **7** | 4 | out |
| CS | **8** | 1 | out |
| MOSI | **10** | 7 | out |
| SCK | **11** | 10 | out |
| BUSY | **24** | 3 | in |
| RST | **25** | 6 | out |
| HPD | — | 19 | tied **GND** on PCB |

### Expander interrupts

**PCA9554 INT** (U1, U2): **NC** on v1 — poll I²C only.

---

## Logical I/O (not direct GPIO)

| Function | Implementation |
|---|---|
| Doors, water, 2× kWh | **PCA9554** U1 + **J2–J7** |
| Sauna LCD buttons | **PCA9554** U2 **P0–P2** + **J8** |
| 12 V presence / hard-lock | Opto **U4** → **U2 P6** |
| SHT31 × 4 | **TCA9546A** U5 + **J9–J12** (ch 0–3, sensor @ `0x44`) |
| LCD × 2 (paralleled) | **J16** I²C |

---

## WISC legacy (reference only)

Direct **BCM** on production **WISC** — for migration context, **not** wanos-pcb-v1 wiring.

### Pulse / digital inputs

| Signal | BCM | WanOS idx |
|---|---:|---:|
| kWh meter | 12 | 11001 |
| Cold water | 6 | 11002 |
| Hot water | 5 | 11003 |
| Sauna door | 27 | 10001 |
| Bathroom door | 22 | 10002 |

### SSR (WISC)

| Signal | BCM |
|---|---:|
| Master safety | 4 |
| IR relay | 14 |
| Sauna phase U | 15 |
| Sauna phase V | 17 |
| Sauna phase W | 18 |

### SHT11 (bit-banged on WISC)

| Location | idx | D | C |
|---|---:|---:|---:|
| Sauna high | 20001 | 11 | 25 |
| Sauna low | 20002 | 7 | 8 |
| Cinema | 20003 | 9 | 10 |
| Bathroom | 20004 | 24 | 23 |

---

## Related

- [`external-plant.md`](external-plant.md)
- [`board-spec.md`](board-spec.md)
- Delivery: [`todo/phaseV-verify.md`](todo/phaseV-verify.md) § V1a
