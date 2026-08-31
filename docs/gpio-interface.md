<!-- --- file: docs/gpio-interface.md -->

# wanos-pcb-v1 — GPIO and field interface

Two views of the same board:

1. **WISC-equivalent subset** — what **current WanOS** expects today (direct Pi GPIO on WISC hardware). Used for **V1a** bring-up adapter planning.
2. **Full wanos-pcb-v1** — target mapping once expanders and plant I²C are supported in a **later WanOS**.

Runtime source of truth for **today’s software** → [wanos `config_hardware.yaml`](https://github.com/gitwannes/wanos/blob/main/config_hardware.yaml).

---

## WISC-equivalent subset (current WanOS)

Direct **BCM** pins on the Pi 40-pin header — matches WISC / current production wiring.

### Pulse / digital inputs

| Signal | BCM | WanOS idx | Type |
|---|---:|---:|---|
| kWh meter | 12 | 11001 | energy |
| Cold water | 6 | 11002 | fluid |
| Hot water | 5 | 11003 | fluid |
| Sauna door | 27 | 10001 | door |
| Bathroom door | 22 | 10002 | door |

kWh resolution: **1000 pulses/kWh** (1 Wh per pulse).

### SSR / GPIO outputs (Pi GPIO — software PWM ~5 Hz on sauna phases)

| Signal | BCM | Config key |
|---|---:|---|
| Master safety | 4 | `safety_gpio` |
| IR relay | 14 | `ir_relais` |
| Sauna phase U | 15 | `sauna_relais_phase_U` |
| Sauna phase V | 17 | `sauna_relais_phase_V` |
| Sauna phase W | 18 | `sauna_relais_phase_W` |

### SHT11 sensors (bit-banged — current WanOS, not SHT31)

| Location | idx | D pin | C pin |
|---|---:|---:|---:|
| Sauna high | 20001 | 11 | 25 |
| Sauna low | 20002 | 7 | 8 |
| Cinema | 20003 | 9 | 10 |
| Bathroom 1e | 20004 | 24 | 23 |

**V1a note:** wanos-pcb-v1 may route these functions through expanders on the PCB; **adapter firmware or wiring** must preserve this logical map until future WanOS adopts the full board map.

---

## Full wanos-pcb-v1 (future WanOS)

See [`io-expander-map.md`](io-expander-map.md) and [`board-spec.md`](board-spec.md).

| Function | Implementation |
|---|---|
| Doors, meters, kWh (incl. bathroom 2, 2× kWh) | **PCA9554** Expander A + JST field connectors |
| Sauna LCD buttons | **PCA9554** Expander B |
| 12 V presence / hard-lock | Optocoupler → expander pin (**R1** lock) |
| SHT31 × 4 | **PCA9615** differential I²C + plant JST |
| 2× LCD | I²C on Pi bus + JST headers |
| WISC e-ink | HDMI→SPI ([`hdmi-spi-eink.md`](hdmi-spi-eink.md)) |
| SSR × 4 | **Pi GPIO** → PN2222A → external SSR (unchanged drive path) |

SSR channels remain on **Pi BCM** (not expander PWM). Pi GPIO allocation for SSR + I²C + SPI → lock at **R2** in [`phaseR-requirements.md`](todo/phaseR-requirements.md).

---

## Software domains (WISC era)

| Domain | Library | Pins |
|---|---|---|
| Pulse inputs + SSR | `lgpio` | In: 5, 6, 12, 22, 27 — Out: 4, 14, 15, 17, 18 |
| SHT11 | `RPi.GPIO` + `pi_sht1x` | 7, 8, 9, 10, 11, 23, 24, 25 |

Future WanOS on wanos-pcb-v1 will move inputs/sensors to I²C expander / SHT31 drivers — tracked in the main wanos repo, not here.
