<!-- --- file: docs/board-overview.md -->

# WanOS PCB — overview

**wanos-pcb-v1** is the first-generation WanOS Raspberry Pi carrier board designed in this repo (KiCad + JLCPCB).

| Hardware | Role |
|---|---|
| **WISC boards** | What **current WanOS** runs on today (previous generation; not in this repo). |
| **wanos-pcb-v1** | **New** board — replaces ad-hoc / WISC wiring with a structured carrier. |

Application logic stays in [gitwannes/wanos](https://github.com/gitwannes/wanos). Full **wanos-pcb-v1** capability (expanders, extra meters, SHT31 plant bus, on-board LCDs) targets a **later WanOS** release (version **not locked**). Until then, production WanOS stays on WISC; **V1a** proves the new board with a **WISC-equivalent subset**.

**Migration reference (pending):** Operator will upload the current **WISC** board layout later — see pipeline Manual **Info — WISC board reference upload** and [`phaseR-requirements.md`](todo/phaseR-requirements.md) § Info — WISC migration. Target path: `docs/reference/wisc-board/`.

---

## What wanos-pcb-v1 provides

- Digital inputs (doors, water meters, kWh meters, buttons)
- Differential I²C for SHT31 sensors (4×)
- SSR drives (3-phase sauna + IR) via Pi GPIO
- 12 V sauna rail monitoring (hard-lock safety)
- 2× I²C LCD headers
- WISC e-ink via HDMI→SPI
- Status and activity LEDs

Canonical electrical spec → [`board-spec.md`](board-spec.md).

---

## Documentation map

| Doc | Content |
|---|---|
| [`board-spec.md`](board-spec.md) | Full wanos-pcb-v1 electrical / mechanical spec |
| [`component-selection.md`](component-selection.md) | JLCPCB parts and footprints |
| [`hdmi-spi-eink.md`](hdmi-spi-eink.md) | WISC e-ink HDMI→SPI |
| [`io-expander-map.md`](io-expander-map.md) | PCA9554 / PCA9615 net map |
| [`gpio-interface.md`](gpio-interface.md) | WISC subset vs full-board GPIO |
| [`jlcpcb-ordering.md`](jlcpcb-ordering.md) | Fab export checklist |
| [`kicad-setup.md`](kicad-setup.md) | KiCad 10 + Konnect + Cursor |
| [`todo/pipeline.md`](todo/pipeline.md) | Delivery pipeline (R1 → V1b, gates, Manual backlog) |

**Planned at R2 / V1a close-out:** `docs/external-plant.md`, `docs/field-wiring.md`, `docs/grounding.md`, `docs/installer-one-pager.md`, `docs/cutover-wisc-to-wanos-pcb-v1.md`, `docs/reference/wisc-board/` (on upload).

---

| Artifact | Location |
|---|---|
| KiCad project | `projects/wanos-board/` |
| BOM seed | `projects/wanos-board/components.xlsx` |
| Fabrication outputs | `projects/wanos-board/fabrication/` |

---

## Out of scope (this repo)

- WanOS Python / YAML (main repo)
- Z-Wave, Hue, MQTT integrations
- WISC legacy PCB files
- Enclosure mechanical design (unless noted at **R2** kickoff)

---

## License

Source available — personal use OK, no redistribution. See [LICENSE](../LICENSE) and [wanos](https://github.com/gitwannes/wanos).
