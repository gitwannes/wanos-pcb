<!-- --- file: docs/reference/wisc-board/README.md -->

# WISC board reference

Structured notes and **read-only KiCad** projects for legacy **WISC** hardware. **Current WanOS** runs on WISC in the field — mainly the **2.5.3 I/O carrier** plus the **2.6.4 HDMI board** on the Pi that drives **LCD screens**.

**Read-only rule:** Do not edit KiCad sources here — see [`.cursor/rules/wisc-boards-readonly.mdc`](../../../.cursor/rules/wisc-boards-readonly.mdc). New design work lives in `projects/wanos-board/` (wanos-pcb-v1).

**Target spec:** [`board-spec.md`](../../board-spec.md) · **GPIO:** [`gpio-interface.md`](../../gpio-interface.md) · **Field wiring (wanos):** [`field-wiring.md`](../../field-wiring.md)

---

## Reference boards

| Summary | KiCad tree | Role |
|---|---|---|
| [**wisc-v5-2-5-3-production.md**](wisc-v5-2-5-3-production.md) | [`211201 wisc2-5-3/`](211201%20wisc2-5-3/) | **Main I/O carrier** — SSR, doors, meters, SHT11 |
| [**wisc-v2-6-4-hdmi.md**](wisc-v2-6-4-hdmi.md) | [`220313 wisc2-6-4-HDMI/`](220313%20wisc2-6-4-HDMI/) | **LCD Pi** node (85×56); **4-pin I²C J7** pinout reference for wanos |

Fab exports, cache, history, backups → [`_donotcommit/`](_donotcommit/) (gitignored).

---

## How to use

1. **R2 / V1a** — confirm harness parity vs [`field-wiring.md`](../../field-wiring.md).
2. **S1 / L1 implement** — copy **patterns** (SSR 5-pin, JST silk, debounce), not whole schematics, into `projects/wanos-board/`.
3. **4-pin I²C pinout** — use **2.6.4 J7** only (not 2.5.3 SHT11 DATA/CLOCK headers).

Silkscreen font (WISC + wanos) → [`../silkscreen/README.md`](../silkscreen/README.md).

Migration narrative (planned R2): `docs/cutover-wisc-to-wanos-pcb-v1.md`.
