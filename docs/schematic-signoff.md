<!-- --- file: docs/schematic-signoff.md -->

# Schematic sign-off checklist (Gate-S1)

Operator review of **`projects/wanos-board/`** hierarchical sheets before **L1** layout.

**How:** open each `.kicad_sch` in KiCad (or export PDF), check connectivity, refs, and nets vs [`field-wiring.md`](field-wiring.md) / [`board-spec.md`](board-spec.md). ERC: [`projects/wanos-board/wanos-board-erc.rpt`](../projects/wanos-board/wanos-board-erc.rpt).

| Done | Sheet file | What |
|:---:|---|---|
| [x] | [`pi_power.kicad_sch`](../projects/wanos-board/pi_power.kicad_sch) | 5 V in (**J17**), **F1** / **Q6** / **D1**, **FB1**, **J40** Pi power |
| [x] | [`safety_12v_mon.kicad_sch`](../projects/wanos-board/safety_12v_mon.kicad_sch) | 12 V monitor opto (**U4**), Exp B P6 |
| [ ] | [`ssr_drivers.kicad_sch`](../projects/wanos-board/ssr_drivers.kicad_sch) | SSR drivers **Q1–Q5**, **J13** |
| [ ] | [`io_expanders.kicad_sch`](../projects/wanos-board/io_expanders.kicad_sch) | **U1**, **U2** PCA9554 |
| [ ] | [`hdmi_spi.kicad_sch`](../projects/wanos-board/hdmi_spi.kicad_sch) | **J1** HDMI / e-ink SPI |
| [ ] | [`i2c_plant.kicad_sch`](../projects/wanos-board/i2c_plant.kicad_sch) | **U5** mux, **J9–J12** SHT31, **J16** LCD |
| [ ] | [`connectors.kicad_sch`](../projects/wanos-board/connectors.kicad_sch) | Field **J2–J14**, **J17** |
| [ ] | [`leds.kicad_sch`](../projects/wanos-board/leds.kicad_sch) | Activity + status LEDs |
| [ ] | [`wanos-board.kicad_sch`](../projects/wanos-board/wanos-board.kicad_sch) | Root hierarchy + sheet pins |

**Signed off:** _date / Wannes_ — (fill when all rows checked)

Pipeline: [`docs/todo/phaseS-schematic.md`](todo/phaseS-schematic.md) § Gate-S1
