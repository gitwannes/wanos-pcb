<!-- --- file: docs/reference/datasheets/README.md -->

# Datasheet pack — wanos-pcb-v1

Operator reference PDFs for board design, JLCPCB ordering, and external-plant documentation.

**Home:** `docs/reference/datasheets/` (not under `projects/` — PDFs are reference material, not KiCad project outputs).

**Git:** large PDF binaries may be local-only; keep this README as the checklist. Drop PDFs in this folder locally.

**Naming:** all PDF/JPG filenames **lowercase** (ASCII).

---

## Inventory

### On-board ICs and semiconductors

| Done | Part | Filename |
|:---:|---|---|
| [x] | NXP **PCA9554PW** (I/O expander) | `pca9554.pdf` |
| [x] | TI **TCA9548A** (I²C mux) | `tca9548a.pdf` |
| [x] | **PC817A** (12 V opto, U4) | `pc817a.pdf` |
| [x] | **PN2222A** (SSR driver) | `pn2222a.pdf` |
| [x] | **SMBJ12A** (12 V TVS, **D3**) | `smbj12a.pdf` |
| [x] | **PESD5V0S1BA** (water SIG TVS, **D25**–**D28**) | `pesd5v0s1ba.pdf` |
| [x] | **SMBJ5.0A** (water **`+5VA`** TVS, **D29**) | `smbj5.0a.pdf` |
| [x] | **BLM21PG331SN1** (Pi 5 V ferrite) | `blm21pg331sn1.pdf` |

### Connectors

| Done | Part | Filename |
|:---:|---|---|
| [x] | Molex **208658-1052** (HDMI J1, LCSC **C6990958**) | `molex-208658-1052.pdf` |
| [x] | JST **XH** series (B2B/B4B/B5B/B6B-XH-A, 2.50 mm) | `jst-xh-series.pdf` |
| [x] | **KF301** screw terminal (J14 2P) | `kf301.pdf` |
| [x] | 2×20 **40-pin** female header (J40) | `40-female-header.pdf` |
| [x] | Amphenol **54602** RJ45 (KiCad footprint class for **J4**) | `amphenol-54602.pdf` + `amphenol-54602-drawing.pdf` |
| — | TE **5556416-1** (orderable **J4** MPN) | **Not required** — BOM/LCSC is enough; Amphenol **54602** docs are the land-pattern authority for the KiCad fp |

### Field wiring aids

| Done | What | Filename |
|:---:|---|---|
| [x] | T568B colour reference (water Cat5 → **J4**) | `rj45-t568b-wiring-colors.jpg` |

### Plant and external (for `docs/external-plant.md`)

| Done | Part | Filename |
|:---:|---|---|
| [x] | Omron **G3PJ-225B DC12-24** (DIN SSR) | `external/omron-g3pj.pdf` |
| [x] | **SHT3x** (Sensirion — SHT31 plant sensor) | `external/sht3x.pdf` |
| [x] | **YF-B6 / YF-B10** water flow sensor | `external/YF-B6 B10 waterflow-sensor.pdf` |

### Pi power (R2 lock — J41 DNP v1)

| Done | Part | Filename |
|:---:|---|---|
| [x] | **BZX85C5V6** family / **BZT52C5V6** (5 V zener, **D1**) | `bzx85c.pdf` |
| [x] | **1N400x** family (legacy reference; reverse block replaced by **Q6** ideal diode on wanos v1) | `1n400x.pdf` |
| [ ] | USB-C receptacle **J41** (LCSC part from `components.xlsx`) | `usb-c-j41.pdf` — **deferred** (J41 DNP v1) |

---

## Relevance notes (water / J4)

| File | Relevant? | Role |
|---|---|---|
| `pesd5v0s1ba.pdf` | **Yes** | SIG TVS **D25**–**D28** on `water_meters.kicad_sch` |
| `smbj5.0a.pdf` | **Yes** | **`+5VA`** TVS **D29** at **J4** |
| `amphenol-54602.pdf` / `-drawing.pdf` | **Yes** | Land-pattern / outline for KiCad fp `Connector_RJ:RJ45_Amphenol_54602-x08_Horizontal` (proxy for TE **5556416-1**) |
| `rj45-t568b-wiring-colors.jpg` | **Yes** | Operator colour aid for [`field-wiring.md`](../../field-wiring.md) § 2a |
| TE **5556416-1** PDF | **Not needed** | Orderable MPN is locked in BOM/LCSC; Amphenol **54602** already covers the footprint you are using |

---

## Status

**On disk:** water TVS pair (**PESD** + **SMBJ5.0A**), Amphenol **54602** fp refs, and T568B colour jpg present. Deferred only: **`usb-c-j41.pdf`** (J41 DNP v1).

---

## Related

- BOM seed: [`projects/wanos-board/components.xlsx`](../../projects/wanos-board/components.xlsx)
- HDMI / e-ink: [`hdmi-spi-eink.md`](../../hdmi-spi-eink.md)
- Components: [`component-selection.md`](../../component-selection.md)
- R2 tracking: [`todo/_archive/phaseR-requirements.md`](../../todo/_archive/phaseR-requirements.md) § R2
