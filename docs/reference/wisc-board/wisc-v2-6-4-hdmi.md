<!-- --- file: docs/reference/wisc-board/wisc-v2-6-4-hdmi.md -->

# WISC v2.6.4 — HDMI e-ink interface board

Summary of the **85 × 56 mm WISC HDMI / e-ink interface** KiCad project. Sources are **read-only reference** in the repo.

| | |
|---|---|
| **Folder** | [`docs/wisc_boards/220313 wisc2-6-4-HDMI/`](../../wisc_boards/220313%20wisc2-6-4-HDMI/) |
| **Project** | `wisc2-6-4.kicad_pro` |
| **Title block** | Wisc · rev **2.6.4** · 2022-03-13 · Hofmans |
| **Silk ID** | `220313_wisc2-6-4` |
| **Status** | **In production use** — Pi node with LCD screens (see [§ 1](#1-role-and-deployed-use-today)) |

**Related:** [`hdmi-spi-eink.md`](../../hdmi-spi-eink.md) (wanos-pcb-v1 target) · [`board-spec.md`](../../board-spec.md) · Index → [`README.md`](README.md)

**Verified open in KiCad (2026-09-01):** `open_project` → `ipc_available: true`, board `wisc2-6-4.kicad_pcb` loaded.

---

## 1. Role and deployed use today

### KiCad design role

This is a **compact Pi carrier / interface board** (~**85 × 56 mm**), **not** the full field-I/O WISC in [`wisc-v5-2-5-3-production.md`](wisc-v5-2-5-3-production.md).

It concentrates on:

- **Raspberry Pi 40-pin header** (`P1`)
- **E-ink display** interconnect using an **HDMI symbol** and **Molex `17466791` footprint** (HDMI pin names on pads — cable to WISC e-ink panel)
- **External power** (5 V / 12 V) and **temp-safety** interlock wiring
- **I²C** breakout (`J7`)
- **4-pin link to “board 2”** (`J4` `to-board2`) — power rails to a second board
- **USB-A** (`J6`)

There are **no** SSR drives, door/water/kWh field inputs, or SHT plant headers on this PCB.

### Deployed use (operator, 2026-09-01)

> This **2.6.4 HDMI** board **is used for WanOS today**, on the **Raspberry Pi where the LCD screens are connected**.
>
> The **HDMI cable is not connected** — in current operation this board **only powers the Pi**.
>
> **HDMI was connected in the past** and **e-ink worked**; it **does not work any more**. That failure is **one of the reasons** to replace the entire **HDMI / e-ink** approach on **wanos-pcb-v1**.

WanOS today therefore uses **two WISC hardware roles**:

| Board | Deployed role today |
|---|---|
| [**2.5.3 production**](wisc-v5-2-5-3-production.md) | Main field-I/O carrier (SSR, doors, meters, SHT11, …) |
| **This 2.6.4 HDMI board** | Pi + **LCD** node — **power only**; e-ink path **unused / broken** |

Use this KiCad tree for **85×56 mm mechanical**, historical **HDMI→SPI GPIO** wiring, and **power patterns** — not as proof that the legacy e-ink path still works in the field.

See also [`hdmi-spi-eink.md`](../../hdmi-spi-eink.md) § Legacy WISC / motivation to redesign.

---

## 2. Mechanical

| Item | Value |
|---|---|
| **Outline** | **85 × 56 mm** (Edge.Cuts: 78.548–163.548 mm × 60.820–116.820 mm) |
| **Thickness** | 1.6 mm |
| **Layers** | 2 (F.Cu / B.Cu), paste/mask on both sides |
| **Mounting** | Four mounting holes (`H1`–`H4`) |
| **Pi** | 2×20 vertical header (`P1`) |

Matches **wanos-pcb-v1** target size in [`board-spec.md`](../../board-spec.md).

---

## 3. Connectors

| Ref | Silk / value | JST / type | Function |
|---|---|---|---|
| **P1** | Raspi header | 2×20 pin | Pi 40-pin |
| **J5** | e-ink | `Wannes:17466791` (Molex-style, HDMI pin naming) | WISC e-ink panel (HDMI cable) |
| **J7** | I²C | 4-pin XH | GPIO2 (SDA) / GPIO3 (SCL) + power |
| **J4** | to-board2 | 4-pin XH | See [§ 4](#4-power-and-board2-link) |
| **J1** | 12V ext | 2-pin XH | External 12 V in (`+12VA`) |
| **J2** | temp-safety | 2-pin XH | Sauna temperature safety interlock |
| **J3** | 5V ext | 2-pin XH | External 5 V in |
| **J6** | USB_A | Molex horizontal | USB host port |

Schematic notes: **I²C** = GPIO2 data, GPIO3 clock. **Pi pwr connector** annotation: pins 1,3 = 3V3; 2,4 = 5V.

---

## 4. Power and board2 link

### Rails

| Rail | Notes |
|---|---|
| **+5VA** | Fused 5 V path (F1 **2 A**), `D2` `1N4001`, bulk/decoupling caps |
| **+12VA** | From **J1** `12V ext`; routed to **J4** and e-ink **+5V** pin (HDMI pin 18 → `+5VA` on PCB) |
| **+3V3** | Pi / logic |
| **D1** `BZX85C5V6` | Zener in 5 V input conditioning |

### J4 `to-board2` (4-pin XH)

| Pin | Net | Notes |
|---:|---|---|
| 1 | GND | |
| 2 | +5VA | |
| 3 | *(NC)* | Unconnected on this rev |
| 4 | +12VA | |

Likely **power feed** to a second WISC board (main I/O carrier), not a signal harness.

**J2 `temp-safety`:** 2-pin — external sauna over-temperature safety chain (cuts 12 V path off-board).

---

## 5. E-ink — HDMI footprint, SPI on Pi GPIO

Schematic uses symbol **`Connector:HDMI_A`** with footprint **`Wannes:17466791`** (same physical family as production J3 on 2.5.3, but pads are labeled with **HDMI net names**).

### BCM map (annotated on schematic — use for software)

| SPI function | BCM GPIO | HDMI pad function (on footprint) |
|---|---:|---|
| **CLK** | 11 | CK+ (pad 10) |
| **MOSI** | 10 | D2− (pad 3) |
| **CS** | 8 | D0+ (pad 7) |
| **BUSY** | 24 | D1+ (pad 4) |
| **RST** | 17 | CEC (pad 13) |
| **DC** | 25 | SDA (pad 16) |
| **Panel 5 V** | — | +5V (pad 18) → `+5VA` |

Most other HDMI pads/shields tie to **GND**. **HPD** (pad 19) → GND on this layout.

### vs [`hdmi-spi-eink.md`](../../hdmi-spi-eink.md)

The wanos-pcb-v1 doc maps **HDMI pin numbers → signal names** (TMDS-oriented). This WISC board implements a **concrete BCM assignment** on the Molex/HDMI footprint. Before **R2** lock:

- Reconcile wanos **Molex 208658-1052** target part vs **`17466791`** reference footprint.
- Confirm **CEC → RST** and **SDA → DC** match running WanOS e-ink driver expectations (wanos doc currently lists CEC/SDA as spare/future).
- Lock whether wanos-pcb-v1 follows **this BCM map** or the draft HDMI-pin table.

---

## 6. vs production WISC 2.5.3

| Topic | [2.5.3 production](wisc-v5-2-5-3-production.md) | This board (2.6.4 HDMI) |
|---|---|---|
| **Size** | ~74 × 105 mm | **85 × 56 mm** |
| **Production WanOS today** | Main I/O carrier | **Yes** — Pi with **LCDs**; **Pi power only** (HDMI **disconnected**; e-ink **no longer works**) |
| **SSR, doors, water, kWh, SHT11** | Full carrier | **None** |
| **E-ink** | Molex J3 (no HDMI symbol) | **HDMI symbol + same footprint family**, documented SPI GPIO |
| **12 V monitoring opto** | None | None (temp-safety **J2** only) |
| **I²C header** | None | **J7** |
| **Link to other board** | None | **J4** power to “board2” |

---

## 7. vs wanos-pcb-v1

| wanos-pcb-v1 target | This reference |
|---|---|
| 85 × 56 mm outline | **Match** — use for mechanical R2 |
| HDMI Type-A → SPI e-ink | **Closest WISC SPI wiring reference** — verify BCM + connector part |
| Full field I/O on one board | **Not here** — merge with 2.5.3 I/O patterns + expanders per spec |
| PCA9554 / SHT31 / LCDs | **Not on this PCB** |
| 12 V opto hard-lock | **Not on this PCB** (only temp-safety JST) |
| Single integrated carrier | wanos goal — this was a **split** (interface + board2) experiment |

---

## 8. Reuse for wanos-pcb-v1

**High value**

- **Board outline** and mounting hole placement (85×56).
- **E-ink SPI BCM map** (§ 5) and HDMI-pad → GND treatment on unused pairs.
- **J7** I²C header pattern (GPIO2/3) — relevant to on-board LCD headers in spec.
- **J1/J2/J3** external power + **temp-safety** silk (`to temp.safety`, `12V ext`, `5V ext in`).
- **J4** as evidence of **12 V / 5 V distribution** thinking (wanos integrates on one board).

**Low / do not copy blindly**

- **J4 to-board2** split-board architecture (wanos-pcb-v1 is one carrier).
- **J6 USB-A** (not in wanos spec).
- **`17466791`** footprint without confirming [`component-selection.md`](../../component-selection.md) **208658-1052** equivalence.

---

## 9. Artifacts in repo tree

| Path | Purpose |
|---|---|
| `wisc2-6-4.kicad_sch` / `.kicad_pcb` / `.kicad_pro` | KiCad sources (read-only) |
| `wisc2-6-4-schema.pdf` | Schematic PDF |
| `fp-lib-table` / `sym-lib-table` | Library pointers (`Wannes:` footprints — copy from 2.5.3 tree if needed) |
| `gerbers/`, backups, cache, `.history/` | Moved to [`../_donotcommit/`](../_donotcommit/) (not in git) |

---

## 10. Konnect / Cursor

Read-only inspection OK (`get_project_info`, `open_project`, file-mode reads). Do not edit under `docs/wisc_boards/`. Setup: [`kicad-setup.md`](../../kicad-setup.md).
