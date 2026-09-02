<!-- --- file: docs/todo/phaseS-schematic.md -->

# WanOS PCB Phase S — Schematic (+ KiCad project)

KiCad schematic and project for **wanos-pcb-v1**. ERC clean before **Gate-S1** and **L1**.

**Status:** **S1** **Done** **2026-09-01** — ERC **0 errors**; **Gate-S1** next.

**Shipped:** [`projects/wanos-board/wanos-board.kicad_pro`](../../projects/wanos-board/wanos-board.kicad_pro) + 8 hierarchical sheets · ERC report [`wanos-board-erc.rpt`](../../projects/wanos-board/wanos-board-erc.rpt) · product docs updated (J17 power, J41 DNP, LED values).

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
| **R17–R28** (activity) | **1k0** | ~1.3 mA @ 3.3 V |
| **R29**, **R31** (status, 5 V rails) | **2k0** | ~1.5 mA @ 5 V (Vf ~2 V) |
| **R30** (status, 12 V) | **6k8** | ~1.5 mA @ 12 V — matched brightness to **2k0** @ 5 V |

**Status LED sense:**

| LED | Sense |
|---|---|
| **5 V in** | Post-**F1** / **`+5VA`** entry (PSU + polyfuse OK) |
| **5 V Pi** | **`+5V-PI`** at **J40** pin **2** feed (post-**FB1**) |
| **12 V** | **`+12VA`** at **J14** |

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
| Expander **B** P3–P5 | **10k** pull-up to 3.3 V, **no** field wire, silk **SPARE/DNP** |
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
| `Pi_Power` | **J17** 5 V screw in, input conditioning (**F1**, **Q6**, **D1**), **FB1**, **J40** 5 V to Pi; **J41** DNP |
| `IO_Expanders` | [`io-expander-map.md`](../io-expander-map.md) |
| `SSR_Drivers` | Pi GPIO → R/Q → **J13** (5-pin); 12 V rail ref |
| `Safety_12V_Mon` | U4 opto → Exp B P6; R32, R33, C17 |
| `HDMI_SPI` | J1 — [`hdmi-spi-eink.md`](../hdmi-spi-eink.md) |
| `I2C_Plant` | U5 TCA9546A; **J9–J12** SHT31; **J16** LCD |
| `Connectors` | **J2–J16** field JST per [`field-wiring.md`](../field-wiring.md) |
| `LEDs` | Activity + status |

Use Konnect schematic tools and/or manual KiCad; **ERC** via `kicad-cli` or Konnect.

### Pre-ERC checklist

- [x] Connector pin counts match [`field-wiring.md`](../field-wiring.md) (R1 Done)
- [x] 12 V opto on **Expander B P6** only
- [x] **R9/R10 = 2k2** I²C pull-ups; no R11–R16
- [x] TCA9546A @ **0x70**; four SHT31 channels **J9–J12**
- [x] Four SSR field strings + **Q5** master safety + Pi GPIO net names match **R2** BCM table
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

**Post-implement fix:** **J13 pin 1** restored to **GND** (was briefly tied to **+12VA** during ERC pass — corrected per [`field-wiring.md`](../field-wiring.md) § 6).

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
