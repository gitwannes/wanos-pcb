<!-- --- file: docs/schematic-signoff.md -->

# Schematic sign-off checklist (Gate-S1)

Operator review of **`projects/wanos-board/`** hierarchical sheets before **L1** layout.

**How:** open each `.kicad_sch` in KiCad (or export PDF), check connectivity, refs, and nets vs [`field-wiring.md`](field-wiring.md) / [`board-spec.md`](board-spec.md). ERC: [`projects/wanos-board/wanos-board-erc.rpt`](../projects/wanos-board/wanos-board-erc.rpt).

| Done | Sheet file | What |
|:---:|---|---|
| [x] | [`pi_power.kicad_sch`](../projects/wanos-board/pi_power.kicad_sch) | **J17** + **J14** screw terminals; 5 V conditioning (**F1** / **Q6** / **D1**), **FB1**, **J40**; **D3** TVS; status **D23** / **D24**; 12 V monitor **U4** → Exp B P6 |
| [x] | [`ssr_drivers.kicad_sch`](../projects/wanos-board/ssr_drivers.kicad_sch) | **Q1–Q5**, **R14–R16**, **C8–C12**, **`SAFETY_BUS`** / **J13**; SSR activity **D19–D22** / **R25–R28** (see [`board-spec.md`](board-spec.md) § 4.1, § 5.3) |
| [x] | [`io_expanders.kicad_sch`](../projects/wanos-board/io_expanders.kicad_sch) | **U1**/**U2**, water **J4**, buttons **J8**; legacy door/kWh stubs pending retire |
| [x] | [`pulse_inputs.kicad_sch`](../projects/wanos-board/pulse_inputs.kicad_sch) | Greenfield **J2**/**J3** reed + **J6**/**J7** SDM72 front-ends |
| [x] | [`hdmi_spi.kicad_sch`](../projects/wanos-board/hdmi_spi.kicad_sch) | **J1** HDMI / e-ink SPI |
| [x] | [`i2c_plant.kicad_sch`](../projects/wanos-board/i2c_plant.kicad_sch) | **U5** TCA9548A, **C6**, **R11** RESET pull-up, **J9–J12**/**J18** SHT31, **J16** LCD (root bus) |
| [x] | [`wanos-board.kicad_sch`](../projects/wanos-board/wanos-board.kicad_sch) | Root hierarchy (no separate **Connectors** / **LEDs** sheets) |

**Signed off:** _date / Wannes_ — (fill when all rows checked)

Pipeline: [`docs/todo/phaseS-schematic.md`](todo/phaseS-schematic.md) § Gate-S1
