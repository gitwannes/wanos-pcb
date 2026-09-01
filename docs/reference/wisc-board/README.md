<!-- --- file: docs/reference/wisc-board/README.md -->

# WISC board reference summaries

Structured notes on **legacy WISC** KiCad projects under [`docs/wisc_boards/`](../../wisc_boards/). **Current WanOS** runs on WISC hardware in the field — mainly the **2.5.3 I/O carrier** plus the **2.6.4 HDMI board** on the Pi that drives **LCD screens** (see each summary).

**Read-only rule:** Do not edit KiCad sources under `docs/wisc_boards/` — see [`.cursor/rules/wisc-boards-readonly.mdc`](../../../.cursor/rules/wisc-boards-readonly.mdc). New design work lives in `projects/wanos-board/` (wanos-pcb-v1).

**Target spec for the new board:** [`board-spec.md`](../../board-spec.md) · **GPIO contracts:** [`gpio-interface.md`](../../gpio-interface.md)

---

## Reference boards

KiCad **sources** live under [`docs/wisc_boards/<board>/`](../../wisc_boards/). Fab exports, cache, history, backups, and lock files are in [`docs/wisc_boards/_donotcommit/`](../../wisc_boards/_donotcommit/) (gitignored — move off-machine when convenient).

| Summary | KiCad tree | Role |
|---|---|---|
| [**wisc-v5-2-5-3-production.md**](wisc-v5-2-5-3-production.md) | [`docs/wisc_boards/211201 wisc2-5-3/`](../../wisc_boards/211201%20wisc2-5-3/) | **Main I/O carrier** — SSR, doors, meters, SHT11 (production WanOS) |
| [**wisc-v2-6-4-hdmi.md**](wisc-v2-6-4-hdmi.md) | [`docs/wisc_boards/220313 wisc2-6-4-HDMI/`](../../wisc_boards/220313%20wisc2-6-4-HDMI/) | **In use today** — Pi + **LCD** node (85×56); powers Pi only; legacy e-ink **broken** |

---

## How to use these docs

1. **R1 / R2 kickoff** — confirm field wiring, connector counts, and GPIO subset against production reality.
2. **V1a bring-up** — preserve [`gpio-interface.md`](../../gpio-interface.md) BCM map when adapting wanos-pcb-v1 to current WanOS.
3. **S1 / L1 implement** — copy **patterns** (SSR drive, JST silk, debounce), not whole schematics, into `projects/wanos-board/`.

Migration narrative (future): [`cutover-wisc-to-wanos-pcb-v1.md`](../../cutover-wisc-to-wanos-pcb-v1.md) (planned at R2 close-out).
