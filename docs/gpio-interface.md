<!-- --- file: docs/gpio-interface.md -->

# GPIO interface contract

Mirror of the WanOS software pin map. **Source of truth for runtime** remains [`config_hardware.yaml`](https://github.com/gitwannes/wanos/blob/main/config_hardware.yaml) in the main repo — update this file when that YAML changes or when **R1** locks connector pinouts.

All pins are **BCM** numbering on the Raspberry Pi GPIO header unless **R1** moves to a compute module carrier.

---

## Pulse / digital inputs

| Signal | BCM pin | WanOS idx | Type | Field name (NL) |
|---|---:|---:|---|---|
| kWh meter | 12 | 11001 | energy | kWh meter |
| Cold water | 6 | 11002 | fluid | koud water |
| Hot water | 5 | 11003 | fluid | warm water |
| Sauna door | 27 | 10001 | door | sauna deur |
| Bathroom door | 22 | 10002 | door | badkamer deur |

WanOS treats pulse inputs as GPIO edges; kWh resolution is **1000 pulses/kWh** (1 Wh per pulse). See main repo [`sauna-ir.md`](https://github.com/gitwannes/wanos/blob/main/docs/sauna-ir.md).

---

## SSR / GPIO outputs

| Signal | BCM pin | WanOS config key | Load notes (from software) |
|---|---:|---|---|
| Master safety | 4 | `safety_gpio` | Drives safety interlock; must default OFF at boot |
| IR relay | 14 | `ir_relais` | IR PWM channel |
| Sauna phase U | 15 | `sauna_relais_phase_U` | ~3500 W element, software PWM |
| Sauna phase V | 17 | `sauna_relais_phase_V` | ~3500 W element, software PWM |
| Sauna phase W | 18 | `sauna_relais_phase_W` | ~2000 W element, software PWM |

Sauna PWM frequency default: **5 Hz** (`config.yaml` / `sauna.pwm_freq`). Outputs use `lgpio` software-timed PWM, not hardware PWM blocks.

---

## SHT11 sensors (bit-banged)

Each sensor uses a **data** pin (D) and **clock** pin (C). WanOS reads via `pi_sht1x` / `RPi.GPIO` on a background thread separate from `lgpio` inputs.

| Location | WanOS idx | Name | D pin | C pin |
|---|---:|---|---:|---:|
| Sauna high | 20001 | sauna high | 11 | 25 |
| Sauna low | 20002 | sauna low | 7 | 8 |
| Cinema | 20003 | cinema | 9 | 10 |
| Bathroom 1e | 20004 | badk 1e | 24 | 23 |

Sensors expect **5 V** I/O behaviour per library init (`vdd='5V'`). Board must respect SHT11 wiring and cable length limits.

---

## Software domains (for isolation design)

| Domain | Library | Pins used |
|---|---|---|
| A — Pulse inputs + SSR outputs | `lgpio` | Inputs: 5, 6, 12, 22, 27 — Outputs: 4, 14, 15, 17, 18 |
| B — SHT11 polling | `RPi.GPIO` + `pi_sht1x` | 7, 8, 9, 10, 11, 23, 24, 25 |

**R1** must confirm whether both domains can share this carrier without pin conflicts (they do not overlap today).

---

## Open items (resolve at R1 kickoff)

- Pi model (4 vs 5) and mounting (HAT, DIN, panel)
- Connector types and pinout per field cable
- Opto-isolation / SSR part numbers and coil/logic voltages
- ESD and mains creepage for SSR switching nodes
- Whether I2C LCD wiring stays on a separate Pi (see WanOS **L2**) or lands on this board later
