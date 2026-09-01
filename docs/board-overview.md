<!-- --- file: docs/board-overview.md -->

# WanOS PCB — overview

**wanos-pcb-v1** is the first-generation WanOS Raspberry Pi carrier board designed in this repo (KiCad + JLCPCB).

| Hardware | Role |
|---|---|
| **WISC 2.5.3** | Main **field-I/O** carrier — SSR, doors, meters, SHT11 ([`reference/wisc-board/`](reference/wisc-board/)) |
| **WISC 2.6.4 HDMI** | **LCD Pi** node — **powers Pi only** today; legacy e-ink **broken** (HDMI not connected) |
| **wanos-pcb-v1** | **New** integrated carrier — replaces split WISC setup + failed HDMI/e-ink path |

Application logic stays in [gitwannes/wanos](https://github.com/gitwannes/wanos). Full **wanos-pcb-v1** capability (expanders, extra meters, SHT31 plant bus, on-board LCDs) targets a **later WanOS** release (version **not locked**). Until then, production WanOS stays on WISC; **V1a** proves the new board with a **WISC-equivalent subset**.

**Migration reference:** WISC summaries → [`reference/wisc-board/`](reference/wisc-board/) (KiCad trees under [`wisc_boards/`](wisc_boards/)). See pipeline Manual **Info — WISC board reference upload** and [`phaseR-requirements.md`](todo/phaseR-requirements.md) § Info — WISC migration.

---

## What wanos-pcb-v1 provides

- Digital inputs (doors, water meters, kWh meters, buttons)
- Differential I²C for SHT31 sensors (4×)
- SSR drives (3-phase sauna + IR) via Pi GPIO
- 12 V sauna rail monitoring (hard-lock safety)
- 2× I²C LCD headers
- WISC e-ink via HDMI→SPI — **legacy path failed in the field**; see [`hdmi-spi-eink.md`](hdmi-spi-eink.md) § Legacy WISC
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
| [`kicad-setup.md`](kicad-setup.md) | KiCad 10, Konnect, Cursor MCP, IPC checklist |
| [`reference/wisc-board/`](reference/wisc-board/) | WISC reference summaries (read-only KiCad under `wisc_boards/`) |
| [`todo/pipeline.md`](todo/pipeline.md) | Delivery pipeline (R1 → V1b, gates, Manual backlog) |

**Planned at R2 / V1a close-out:** `docs/external-plant.md`, `docs/field-wiring.md`, `docs/grounding.md`, `docs/installer-one-pager.md`, `docs/cutover-wisc-to-wanos-pcb-v1.md`. WISC summaries: [`reference/wisc-board/`](reference/wisc-board/) (2.5.3 production + 2.6.4 HDMI).

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
- WISC legacy PCB **edits** (reference trees are read-only; see [`.cursor/rules/wisc-boards-readonly.mdc`](../.cursor/rules/wisc-boards-readonly.mdc))
- Enclosure mechanical design (unless noted at **R2** kickoff)

---

## License

Source available — personal use OK, no redistribution. See [LICENSE](../LICENSE) and [wanos](https://github.com/gitwannes/wanos).
