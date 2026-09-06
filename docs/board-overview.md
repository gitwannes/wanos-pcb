<!-- --- file: docs/board-overview.md -->

# WanOS PCB — overview

**wanos-pcb-v1** is the first-generation WanOS Raspberry Pi carrier board designed in this repo (KiCad + JLCPCB).

| Hardware | Role |
|---|---|
| **WISC 2.5.3** | Main **field-I/O** carrier — SSR, doors, meters, SHT11 ([`reference/wisc-board/`](reference/wisc-board/)) |
| **WISC 2.6.4 HDMI** | **LCD Pi** node — **powers Pi only** today; legacy e-ink **broken** (HDMI not connected) |
| **wanos-pcb-v1** | **New** integrated carrier — replaces split WISC setup + failed HDMI/e-ink path |

Application logic stays in [gitwannes/wanos](https://github.com/gitwannes/wanos). Operator continues on **WISC** until **wanos** is updated for this board (**V1a**). **R1** + **R2** closed **2026-09-01**.

---

## What wanos-pcb-v1 provides

- Digital inputs (doors, water meters, 2× kWh, buttons) via **PCA9554** expanders
- **SHT31 × 5** via **TCA9548A** mux and Cat5 plant cables (~4–5 m); **J16** LCD on root I²C
- SSR drives (3-phase sauna + IR) via Pi GPIO
- **12 V** rail monitoring (optocoupler → Expander B P6)
- **1×** I²C LCD header (two displays paralleled on **J16**)
- WISC e-ink via HDMI→SPI — legacy path failed in the field; see [`hdmi-spi-eink.md`](hdmi-spi-eink.md)
- Status and activity LEDs

Canonical electrical spec → [`board-spec.md`](board-spec.md).

---

## Documentation map

| Doc | Content |
|---|---|
| [`board-spec.md`](board-spec.md) | Full wanos-pcb-v1 electrical / mechanical spec |
| [`field-wiring.md`](field-wiring.md) | JST pinouts, Cat5, mux channels (**R1**) |
| [`component-selection.md`](component-selection.md) | JLCPCB parts and footprints |
| [`hdmi-spi-eink.md`](hdmi-spi-eink.md) | WISC e-ink HDMI→SPI |
| [`io-expander-map.md`](io-expander-map.md) | PCA9554 + TCA9548 map |
| [`gpio-interface.md`](gpio-interface.md) | Pi BCM map + software strategy (**R2**) |
| [`external-plant.md`](external-plant.md) | Off-board SSR + 12 V plant |
| [`grounding.md`](grounding.md) | Ground / return scheme |
| [`reference/datasheets/README.md`](reference/datasheets/README.md) | Datasheet pack |
| [`reference/silkscreen/README.md`](reference/silkscreen/README.md) | Silkscreen font + artwork |
| [`reference/wisc-board/`](reference/wisc-board/) | WISC summaries + read-only KiCad |
| [`jlcpcb-ordering.md`](jlcpcb-ordering.md) | Fab export checklist |
| [`kicad-setup.md`](kicad-setup.md) | KiCad 10, Konnect, Cursor MCP |
| [`todo/pipeline.md`](todo/pipeline.md) | Delivery pipeline (S1 → V1b) |

**V1a close-out (planned):** `docs/installer-one-pager.md`, `docs/cutover-wisc-to-wanos-pcb-v1.md`.

---

| Artifact | Location |
|---|---|
| KiCad project | `projects/wanos-board/` |
| BOM seed | `projects/wanos-board/components.xlsx` |
| Fabrication outputs | `projects/wanos-board/fabrication/` |

---

## Out of scope (this repo)

- WanOS Python / YAML (main repo)
- WISC legacy PCB **edits** (read-only under [`reference/wisc-board/`](reference/wisc-board/); see [`.cursor/rules/wisc-boards-readonly.mdc`](../.cursor/rules/wisc-boards-readonly.mdc))
- Enclosure mechanical design (no constraint locked at R2)

---

## License

Source available — personal use OK, no redistribution. See [LICENSE](../LICENSE) and [wanos](https://github.com/gitwannes/wanos).
