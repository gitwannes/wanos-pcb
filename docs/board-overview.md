<!-- --- file: docs/board-overview.md -->

# WanOS electronics board — overview

Product reference for the custom PCB that sits between the **WanOS Raspberry Pi** and site field wiring (pulse meters, door contacts, SHT11 probes, sauna/IR SSR drives).

Software behaviour is documented in the main WanOS repo ([`sauna-ir.md`](https://github.com/gitwannes/wanos/blob/main/docs/sauna-ir.md), [`config_hardware.yaml`](https://github.com/gitwannes/wanos/blob/main/config_hardware.yaml)). This repo owns **physical implementation** only.

---

## Role

The WanOS Pi runs Python control logic (`lgpio` outputs, pulse inputs, bit-banged SHT11 reads). Today those signals are likely wired ad hoc to headers or modules. This board should:

1. **Break out** all GPIO listed in [`gpio-interface.md`](gpio-interface.md) to robust connectors.
2. **Condition** inputs (pulse meters, doors) for 3.3 V BCM GPIO — isolation/TVS/filters as locked at **R1** kickoff.
3. **Drive** external SSR or relay coils for IR and sauna phases U/V/W plus the master safety interlock line.
4. **Route** four SHT11 sensor pairs (data + clock) to pluggable headers or terminal blocks.
5. **Stay compatible** with WanOS boot safety: all SSR lines must power-up **OFF** / LOW until software arms outputs.

---

## Functional blocks (design intent)

| Block | WanOS domain | Notes |
|---|---|---|
| **Pi interface** | — | 40-pin header or equivalent; Pi model locked at **R1** |
| **Pulse inputs** | kWh meter (pin 12), cold water (6), hot water (5) | Debounce/filter; see [`sauna-ir.md`](https://github.com/gitwannes/wanos/blob/main/docs/sauna-ir.md) § energy meter |
| **Door inputs** | Sauna (27), bathroom (22) | Dry contact or opto — locked at **R1** |
| **SSR outputs** | IR (14), U (15), V (17), W (18), safety (4) | Software PWM on sauna phases; safety is master enable |
| **SHT11 buses** | Four sensors (see gpio-interface) | 5 V tolerant bit-bang; keep cable length in mind |
| **Power** | — | Pi fed separately unless **R1** adds local regulation |

Detailed net names and connector pinouts are **not locked** until **R1** kickoff closes.

---

## Out of scope (this repo)

- WanOS Python / YAML application code
- Z-Wave, Hue, MQTT, LCD Pi, or other network integrations
- Enclosure mechanical design (may be noted in **R1** as operator follow-up)

---

## Delivery artifacts

| Artifact | Location |
|---|---|
| KiCad project | `projects/wanos-board/` |
| Fabrication outputs | `projects/wanos-board/fabrication/` |
| Order checklist | [`jlcpcb-ordering.md`](jlcpcb-ordering.md) |
| Pipeline / phases | [`todo/pipeline.md`](todo/pipeline.md) |
