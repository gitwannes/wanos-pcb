<!-- --- file: docs/reference/datasheets/README.md -->

# Datasheet pack — wanos-pcb-v1

Operator reference PDFs for board design, JLCPCB ordering, and external-plant documentation.

**Home:** `docs/reference/datasheets/` (not under `projects/` — PDFs are reference material, not KiCad project outputs).

**Git:** large PDF binaries are gitignored (`*.pdf` here). Keep this README as the checklist; drop PDFs in this folder locally.

**Naming:** all PDF filenames **lowercase** (ASCII).

---

## Inventory

### On-board ICs and semiconductors

| Done | Part | Filename |
|:---:|---|---|
| [x] | NXP **PCA9554PW** (I/O expander) | `pca9554.pdf` |
| [x] | TI **TCA9546A** (I²C mux) | `tca9546a.pdf` |
| [x] | **PC817A** (12 V opto, U4) | `pc817a.pdf` |
| [x] | **PN2222A** (SSR driver) | `pn2222a.pdf` |
| [x] | **SMBJ12A** (12 V TVS) | `smbj12a.pdf` |
| [x] | **BLM21PG331SN1** (Pi 5 V ferrite) | `blm21pg331sn1.pdf` |

### Connectors

| Done | Part | Filename |
|:---:|---|---|
| [x] | Molex **208658-1052** (HDMI J1, LCSC **C6990958**) | `molex-208658-1052.pdf` |
| [x] | JST **XH** series (B2B/B4B/B5B/B6B-XH-A, 2.50 mm) | `jst-xh-series.pdf` |
| [x] | **KF301** screw terminal (J14 2P) | `kf301.pdf` |
| [x] | 2×20 **40-pin** female header (J40) | `40-female-header.pdf` |

### Plant and external (for `docs/external-plant.md`)

| Done | Part | Filename |
|:---:|---|---|
| [x] | Omron **G3PJ-225B DC12-24** (DIN SSR) | `omron-g3pj.pdf` |
| [x] | **SHT3x** (Sensirion — SHT31 plant sensor) | `sht3x.pdf` |

### Pi power (R2 lock — J41 populated)

| Done | Part | Filename |
|:---:|---|---|
| [ ] | USB-C receptacle **J41** (LCSC part from `components.xlsx`) | `usb-c-j41.pdf` — **operator to add later** |

---

## Status

**12 / 13** PDFs on disk. **Deferred:** `usb-c-j41.pdf` (operator).

---

## Related

- BOM seed: [`projects/wanos-board/components.xlsx`](../../projects/wanos-board/components.xlsx)
- HDMI / e-ink: [`hdmi-spi-eink.md`](../../hdmi-spi-eink.md)
- Components: [`component-selection.md`](../../component-selection.md)
- R2 tracking: [`todo/phaseR-requirements.md`](../../todo/phaseR-requirements.md) § R2
