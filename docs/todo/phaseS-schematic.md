<!-- --- file: docs/todo/phaseS-schematic.md -->

# WanOS PCB Phase S — Schematic (+ KiCad project)

KiCad schematic and project for **wanos-pcb-v1**. ERC clean before **Gate-S1** and **L1**.

**Status:** **S1** **Done** **2026-09-01** — ERC **0 errors**; **Gate-S1** next.

**Shipped:** [`projects/wanos-board/wanos-board.kicad_pro`](../../projects/wanos-board/wanos-board.kicad_pro) + 7 hierarchical sheets · ERC report [`wanos-board-erc.rpt`](../../projects/wanos-board/wanos-board-erc.rpt) · product docs updated (J17 power, J41 DNP, LED values, 12 V monitor on **Pi_Power**).

**Related:** [`board-spec.md`](../board-spec.md) · [`io-expander-map.md`](../io-expander-map.md) · [`hdmi-spi-eink.md`](../hdmi-spi-eink.md) · [`component-selection.md`](../component-selection.md) · [`projects/wanos-board/components.xlsx`](../../projects/wanos-board/components.xlsx) · [`kicad-setup.md`](../kicad-setup.md) · Sequence → [`pipeline.md`](pipeline.md).

**DoD convention:** Last DoD = audit & update ALL `docs/**/*.md` (and root README) against shipped artifacts.

---

## Subphases

| Id | What | Status |
|---|---|---|
| **S1** | KiCad project + schematic + ERC | **Done** **2026-09-01** |

---

## S1 — KiCad schematic wanos-pcb-v1

### Kickoff locks (2026-09-01)

**Power (locked 2026-09-01):**

| Item | Lock |
|---|---|
| **5 V in** | **KF301-2P** screw terminal (**J17**) — external PSU + / GND |
| **5 V to Pi** | **`+5VA`** → **FB1** → **`+5V-PI`** → **J40** pins **2 & 4** + GND (header injection — WISC 2.6.4) |
| **Conditioning** | **F1** **2 A** polyfuse, **Q6** `AO3401A` ideal diode, **D1** `BZT52C5V6` shunt, **C1** 100 µF → **`+5VA`** |
| **FB1** | **Populate** `BLM21PG331SN1` (after conditioning, before **J40** 5 V) |
| **J41** | **DNP v1** — no USB-C Pi power |

**LED resistors (locked 2026-09-01):**

| Refs | Value | Notes |
|---|---|---|
| **R17–R24** (field activity, **`io_expanders.kicad_sch`**) | **1k0** | ~1.3 mA @ 3.3 V |
| **R25–R28** (SSR activity, **`ssr_drivers.kicad_sch`**) | **1k0** | ~3 mA @ 5 V (**`+5VA`** → **`SSR_*`**) |
| **R29** (status, **+5VA**) | **2k0** | ~1.5 mA @ 5 V (Vf ~2 V) |
| **R30** (status, **+12V**) | **6k8** | ~1.5 mA @ 12 V — matched brightness to **2k0** @ 5 V |

**Status LED sense:**

| LED | Sense |
|---|---|
| **5 V in** | Post-**F1** / **`+5VA`** entry (PSU + polyfuse OK) |
| **12 V** | **`+12V`** at **J14** (external PSU input, after field temp safety) |

**D25** / **R31** dropped **2026-09-02** — duplicate **`+5VA`** indicator (same rail as **D23**).

**HDMI panel 5 V (locked 2026-09-01 — option 2):**

| Item | Lock |
|---|---|
| **J1 pin 18** | **`+5VA`** via **F2** **500 mA** polyfuse (on **`+5VA`** bus) |
| **V1a** | Cable/panel verification per [`hdmi-spi-eink.md`](../hdmi-spi-eink.md) before relying on e-ink |

**Other:**

| Item | Lock |
|---|---|
| Symbols | **A** — KiCad stock + Konnect/JLC greenfield; WISC = topology reference only |
| **bom-targets.yaml** | Sync from `components.xlsx` where MD matches; fix xlsx drift (see below) |
| Expander **B** P3–P5, P7 | **NC** v1 — no nets, no pull-ups; firmware output **LOW** at init |
| **R32** (opto LED) | **1k5** |

**Implement-time housekeeping (not kickoff blockers):** sync `bom-targets.yaml` + fix `components.xlsx` drift (drop **J15**, **J1** → **C6990958**, **J41** DNP, add **J17**, **F1**, **F2**, **D1/D2**); product docs (`board-spec`, `field-wiring`, …) at **S1 DoD**.

**Kickoff:** **closed** **2026-09-01** · **Implement:** **2026-09-01**

### Prereqs

- **R2** Done — [`gpio-interface.md`](../gpio-interface.md), [`grounding.md`](../grounding.md)
- **Ops1** Done — Konnect + KiCad 10 ([`kicad-setup.md`](../kicad-setup.md))
- Datasheet pack in [`reference/datasheets/`](../reference/datasheets/README.md) (pipeline Manual)

### KiCad deliverables (implement phase)

| Artifact | Action |
|---|---|
| `wanos-board.kicad_pro` | Create project; link to `design.yaml` revision **wanos-pcb-v1** |
| `wanos-board.kicad_sch` | Root + hierarchical sheets (see below) |
| Symbol libraries | JLC/LCSC symbols for U1–U2, U4–U5, Q1–Q4, J1, passives — validate footprints vs [`components.xlsx`](../../projects/wanos-board/components.xlsx) |
| `bom-targets.yaml` | Sync key parts from xlsx |

### Target schematic sheets

| Sheet | Source |
|---|---|
| `Pi_Power` | **J17** + **J14** screw terminals; 5 V conditioning (**F1**, **Q6**, **D1**), **FB1**, **J40**; **D3** TVS; status **D23** / **D24**; **U4** 12 V monitor → Exp B P6 (**R32**, **R33**, **C17**); **J41** DNP |
| `IO_Expanders` | [`io-expander-map.md`](../io-expander-map.md) — **U1**/**U2**, I²C pull-ups, door/kWh activity LEDs |
| `Water_Meters` | YF-B6/B10 front-end — OD pull-ups, series R, debounce, water LEDs ([`field-wiring.md`](../field-wiring.md) § 2a); nets `WM_*` ↔ `EXP_A_P2`…`P5` |
| `SSR_Drivers` | Pi GPIO → R/Q → **J13** (5-pin); **`+12V`** rail ref; SSR activity **D19–D22** / **R25–R28** |
| `HDMI_SPI` | J1 — [`hdmi-spi-eink.md`](../hdmi-spi-eink.md) |
| `I2C_Plant` | U5 TCA9546A; **J9–J12** SHT31; **J16** LCD |
| `Connectors` | Field JST **J2–J8** (incl. water **J4–J5**) per [`field-wiring.md`](../field-wiring.md) |

Status on **Pi_Power**; SSR activity on **SSR_Drivers**. Water conditioning on **Water_Meters**. Door/kWh activity LEDs on **IO_Expanders**.

Use Konnect schematic tools and/or manual KiCad; **ERC** via `kicad-cli` or Konnect.

### Pre-ERC checklist

- [x] Connector pin counts match [`field-wiring.md`](../field-wiring.md) (R1 Done)
- [x] 12 V opto on **Expander B P6** only
- [x] **R9/R10 = 2k2** I²C pull-ups; **R11–R13** DNP (no PCA9615); **R14–R16** on SSR sheet
- [x] TCA9546A @ **0x70**; four SHT31 channels **J9–J12**
- [x] Four SSR field strings + **Q5** safety gate + **R16** **`SAFETY_BUS`** pull-up; Pi GPIO net names match **R2** BCM table
- [x] PCA9554 A0–A2 tied; unique I²C addresses
- [x] HDMI nets named per hdmi-spi-eink doc

### S1 DoD

- [x] `wanos-board.kicad_sch` + `.kicad_pro` in repo
- [x] ERC pass or waivers recorded here
- [x] Ready for **Gate-S1** operator sign-off (pipeline Sequence **#2**)
- [x] Last DoD: all `docs/**/*.md` + README audited

### ERC (2026-09-01)

**Result:** **0 errors**, **89 warnings** — [`wanos-board-erc.rpt`](../../projects/wanos-board/wanos-board-erc.rpt)

**Accepted warnings:** `endpoint_off_grid`, `unconnected_wire_endpoint`, `isolated_pin_label` on global labels / cosmetic routing.

**Post-implement fix:** **J13 pin 1** restored to **GND** (was briefly tied to **+12V** during ERC pass — corrected per [`field-wiring.md`](../field-wiring.md) § 6).

**2026-09-02:** **`safety_12v_mon.kicad_sch`** merged into **`pi_power.kicad_sch`** (**U4**, **R32**–**R33**, **C17**); status LEDs **D23** / **D24** on **Pi_Power**; net name **`+12V`** (not **`+12VA`**) for external 12 V input; **J14** + **D3** TVS moved to **Pi_Power** (off **Connectors**).

**2026-09-04:** Water meters **YF-B6/B10** — sheet **`water_meters.kicad_sch`** (OD pull-up to **`+3V3`**, **330 Ω** series, **100 nF**, activity LEDs); **no MOSFET**. See [`field-wiring.md`](../field-wiring.md) § 2a.

**2026-09-02:** Re-run ERC + netlist after **`leds.kicad_sch`** removal and Exp B **NC** cleanup — [`wanos-board-erc.rpt`](../../projects/wanos-board/wanos-board-erc.rpt) on disk may still list the old **LEDs** sheet.

**2026-09-02:** **`leds.kicad_sch`** removed from root hierarchy (**`wanos-board.kicad_sch`** / **`wanos-board.kicad_pro`**); file deleted.

**2026-09-02:** Expander **B** P3–P5, P7 → **NC** (dropped **`UI_*`** nets and **R34**–**R36**).

**2026-09-02:** Field input activity LEDs **D11–D18** / **R17–R24** moved from **`leds.kicad_sch`** to **`io_expanders.kicad_sch`** (with **U1**/**U2**); **`leds.kicad_sch`** sheet dropped from hierarchy.

**2026-09-02:** SSR activity LEDs **D19–D22** / **R25–R28** moved from **`leds.kicad_sch`** to **`ssr_drivers.kicad_sch`** (cathodes on **`SSR_*`** nets).

**2026-09-02:** **`io_expanders.kicad_sch`** rework — PCA9554 address straps (**U1** `0x20`, **U2** `0x21`); **C3**/**C4** per-chip VCC decoupling; **C5** dropped (redundant). See [`io-expander-map.md`](../io-expander-map.md) § 1 / § 6.

**Footprint follow-up (L1 / Gate-S1):** **Q1–Q5** SSR drivers SOT-23; pi-power **Q6** ideal diode + **F1** polyfuse + **C1/D1** SMD (**2026-09-02**).

---

## Gate-S1 — Operator schematic sign-off

**Pipeline Sequence #2** (not a letter subphase). **Prereq:** S1 ERC clean.

**Checklist:** [`schematic-signoff.md`](../schematic-signoff.md) (per-sheet sign-off).

- [ ] Operator reviews schematic PDF (or KiCad) — connector orientation, SSR path, 12 V opto, net names
- [ ] Sign-off recorded (date + name) in this section before **L1** starts

---

## Out of scope

- PCB placement (**L1**)
- Gerber export (**J1**)
