<!-- --- file: docs/todo/_archive/phaseS-schematic.md -->

# WanOS PCB Phase S — Schematic (+ KiCad project) — ARCHIVED

**Status:** **Done** **2026-09-21** (S1 **2026-09-01** + Gate-S1 operator close).

**Shipped:** [`projects/wanos-board/`](../../../projects/wanos-board/) hierarchical KiCad schematic for **wanos-pcb-v1**.

## Shipped summary

| Id | What | Closed |
|---|---|---|
| **S1** | Project + sheets + ERC **0 errors** | **2026-09-01** |
| **Gate-S1** | Operator schematic sign-off (Wannes) | **2026-09-21** |

**Sheets (as closed):** `Pi_Power`, `IO_Expanders`, `Pulse_Inputs`, `SSR_Drivers`, `HDMI_SPI`, `I2C_Plant` — checklist [`schematic-signoff.md`](../../schematic-signoff.md).

**Notable post-S1 schematic work retained in product docs:** TCA9548A + 5× SHT31; water on **J4** in `io_expanders`; greenfield door/kWh front-ends on `pulse_inputs` (retire legacy stubs on cutover); **C7** dropped; **R11** RESET pull-up.

## Product docs (canonical)

| Topic | Doc |
|---|---|
| Spec | [`board-spec.md`](../../board-spec.md) |
| Field / pulse | [`field-wiring.md`](../../field-wiring.md) |
| Expanders / I²C | [`io-expander-map.md`](../../io-expander-map.md) |
| Sign-off record | [`schematic-signoff.md`](../../schematic-signoff.md) |
| Parts | [`component-selection.md`](../../component-selection.md) |

**Next (main carrier):** **L1** layout — [`phaseL-layout.md`](../phaseL-layout.md).  
**Next (operator, near-term):** clean + check **wanos-remote** schematic — [`pipeline.md`](../pipeline.md) Sequence **Ops-Remote1**.

Pipeline: [`pipeline.md`](../pipeline.md).
