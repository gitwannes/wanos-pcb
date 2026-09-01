<!-- --- file: docs/reference/wisc-board/wisc-v5-2-5-3-production.md -->

# WISC v5 — rev 2.5.3 (production)

Summary of the **production WISC** board WanOS runs on today. KiCad sources are **read-only reference** in the repo.

| | |
|---|---|
| **Folder** | [`211201 wisc2-5-3/`](211201%20wisc2-5-3/) |
| **Project** | `wisc-v5.kicad_pro` |
| **Silk revision** | `wv5.0-pv3-d211201` |
| **Date in tree** | 2021-12-01 upload folder name; PCB title block 2012 (legacy) |
| **Status** | **Production** — current WanOS hardware |

**Related:** [`gpio-interface.md`](../../gpio-interface.md) (software pin map) · [`board-spec.md`](../../board-spec.md) (wanos-pcb-v1 target) · Index → [`README.md`](README.md)

---

## 1. Role

- Carrier for Raspberry Pi 4/5-style **40-pin header** (`P1`) — **main WanOS field-I/O** node (SSR, sensors, pulse inputs).
- **Direct Pi GPIO** for pulse inputs, SSR outputs, and **SHT11** bit-banged sensors — no I²C expanders, no SHT31 plant bus, no on-board 12 V opto monitor.
- **E-ink** via dedicated **Molex panel connector** (J3), not HDMI repurposing (see [§ 6 vs wanos-pcb-v1](#6-vs-wanos-pcb-v1)).

**Other Pi in production:** the [**2.6.4 HDMI WISC board**](wisc-v2-6-4-hdmi.md) sits on the **Pi where LCD screens are connected** — today it **only powers that Pi** (HDMI **disconnected**; e-ink **no longer works**). See that summary for deployed context.

Use this board to validate **what WanOS expects today** on the **I/O carrier** (V1a subset). Use [`wisc-v2-6-4-hdmi.md`](wisc-v2-6-4-hdmi.md) for **85×56 mm** outline and historical **HDMI→SPI** wiring.

---

## 2. Mechanical

| Item | Value |
|---|---|
| **Outline (approx.)** | **~74 × 105 mm** (from `Edge.Cuts` in `wisc-v5.kicad_pcb`) |
| **Thickness** | 1.6 mm |
| **Layers** | 2 (F.Cu / B.Cu) |
| **Pi mounting** | 2×20 vertical pin header — board sits as Pi carrier (not HAT stack) |

wanos-pcb-v1 targets **85 × 56 mm** — do **not** assume identical mechanicals.

---

## 3. Power

| Rail / block | Notes |
|---|---|
| **+5 V / +3.3 V** | Pi and logic |
| **+5VA** | Auxiliary 5 V domain (Pi power path) |
| **External 5 V** | J4 (`5V EXT`), 2-pin JST XH |
| **Fuses** | F1 2.5 A, F2 2 A (5×20 mm holders) |
| **Protection** | D3 `1N4002` |
| **Indicators** | Multiple `pwr_Raspi` and `5V_ext` LEDs |

**Not present:** isolated **12 V sauna rail monitor** / optocoupler hard-lock (wanos-pcb-v1 adds this).

---

## 4. Outputs — SSR (Pi GPIO → transistors)

Drive path matches wanos-pcb-v1 intent: **BCM → PN2222A / 2N7000 → external SSR opto inputs**.

| Channel | Schematic label | Driver | Activity LED |
|---|---|---|---|
| Safety | `SSR_safety` | PN2222A (Q7) | D4 |
| IR | `SSR_IR` | PN2222A | D5 |
| Sauna phase 1 | `SSR_S1` | PN2222A | D6 |
| Sauna phase 2 | `SSR_S2` | PN2222A | D7 |
| Sauna phase 3 | `SSR_S3` | PN2222A | D8 |

- Field header **J1** — 5-pin JST XH, silk **SSR**.
- Base resistors **2k2** to SSR nets; status LEDs with **220 Ω** class resistors.

**Software map:** [`gpio-interface.md`](../../gpio-interface.md) — BCM 4 (safety), 14 (IR), 15/17/18 (phases U/V/W).

---

## 5. Inputs and field connectors

### Digital / pulse (direct GPIO)

| JST | Silk / value | Pins | Function |
|---|---|---:|---|
| **J11** | `deur_sauna` | 2 | Sauna door reed |
| **J12** | `deur_badk` | 2 | Bathroom door reed |
| **J5** | `waterflow` | 4 | Bathroom cold + hot pulse meters |
| **J2** | `kWh` | 2 | Main kWh pulse |

- Pull-ups **10k**, debounce **100 nF** (`.1u`) on inputs.
- Pulse activity LEDs **220–330 Ω** (e.g. cold/hot/kWh indicators).

**Software map:** BCM 27/22 (doors), 6/5 (water), 12 (kWh) — [`gpio-interface.md`](../../gpio-interface.md).

**R1 note:** Two **separate** door connectors (J11/J12) — supports fixing wanos BOM vs single-door contradiction.

### SHT11 plant headers (4× 4-pin JST XH)

Bit-banged **SHT11**, not SHT31 / PCA9615.

| JST | Silk | WanOS location (idx) | Typical D/C BCM |
|---|---|---|---:|
| **J10** | `sens-sauna-high` | Sauna high 20001 | 11 / 25 |
| **J9** | `sens-sauna-mid` | Sauna low 20002 | 7 / 8 |
| **J8** | `sens-cinema` | Cinema 20003 | 9 / 10 |
| **J7** | `sens-badk` | Bathroom 20004 | 24 / 23 |

Each header: **4-pin XH** (data, clock, 3V3, GND style plant cable).

---

## 6. vs wanos-pcb-v1

| Feature | This board (2.5.3 prod) | wanos-pcb-v1 target |
|---|---|---|
| Digital inputs | Direct GPIO | **PCA9554** expander A + more channels |
| Doors | 2× 2-pin (J11/J12) | Same count, expander-backed |
| Water meters | 1× bathroom (J5) | **2× bathrooms** + extra pulses |
| kWh | 1× (J2) | **2×** kWh |
| Sauna LCD buttons | None | Expander B + 4-pin JST |
| Temperature | SHT11 × 4 | **SHT31 × 4** + **TCA9546A** mux (no PCA9615 v1) |
| 12 V monitor | None | **Optocoupler** → Expander B P6 |
| LCD | None | **2× I²C LCD** JST |
| E-ink | **J3** Molex `1746679-1` | **HDMI Type-A → SPI** ([`hdmi-spi-eink.md`](../../hdmi-spi-eink.md)) |
| USB | **J6** USB-A on board | Not in wanos spec |
| Outline | ~74×105 mm | **85×56 mm** |

---

## 7. Reuse for wanos-pcb-v1 design

**High value**

- BCM / WanOS GPIO map ([`gpio-interface.md`](../../gpio-interface.md)) — verified against schematic net labels.
- SSR transistor + LED indicator blocks and **J1** 5-pin SSR header pattern.
- JST XH field connector choices and **Dutch/short silk labels** (`deuren`, `water`, `kWh`, `sauna 3-2-1`).
- Input conditioning: **10k** pull-up, **100 nF** debounce, **220 Ω** activity LEDs.

**Copy assets (on implement)**

- [`Wannes-library.kicad_sym`](211201%20wisc2-5-3/Wannes-library.kicad_sym) — logos, custom symbols.
- [`Wannes-library.pretty/`](211201%20wisc2-5-3/Wannes-library.pretty/) — logos, **HCPL3700** footprint (unused here but relevant for 12 V monitor), Molex e-ink footprint.

**Use other reference**

- **HDMI e-ink + 85×56 mm** → [`wisc-v2-6-4-hdmi.md`](wisc-v2-6-4-hdmi.md)

---

## 8. Artifacts in repo tree

| Path | Purpose |
|---|---|
| `wisc-v5.kicad_sch` / `.kicad_pcb` / `.kicad_pro` | KiCad sources (read-only) |
| `Wannes-library*` | Custom symbols / footprints |
| `BOM 211206.xlsx`, schema PDF, PCB photos, `water-mosfet-circuit.png` | Supporting reference |
| `gerbers/`, cache, `.history/` | Moved to [`../_donotcommit/`](../_donotcommit/) (not in git) |

---

## 9. Konnect / Cursor

Safe **read-only** operations against this path: `get_project_info`, `open_project`, file-mode `get_board_info`. Do not edit KiCad sources here — see [`.cursor/rules/wisc-boards-readonly.mdc`](../../../.cursor/rules/wisc-boards-readonly.mdc).

Setup: [`kicad-setup.md`](../../kicad-setup.md).
