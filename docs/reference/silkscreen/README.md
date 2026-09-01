<!-- --- file: docs/reference/silkscreen/README.md -->

# wanos-pcb-v1 — silkscreen reference

Silkscreen typography and artwork for **wanos-pcb-v1**, matching legacy **WISC** boards.

---

## PCB font (same as WISC)

Use **Printed Circuit Board 7** on silkscreen labels (connector names, revision text, short field hints).

| Resource | Link |
|---|---|
| **Font (FontSpace)** | [Printed Circuit Board 7](https://www.fontspace.com/printed-circuit-board-7-font-f15777) |
| Shortcut (Windows) | [`PCBfont.url`](PCBfont.url) |

Install the font on the KiCad workstation so PCB Editor can render the same face as WISC production boards.

**KiCad:** set default silkscreen font to this typeface where practical; minimum text height per [`board-spec.md`](../../board-spec.md) § 8.2 (**≥ 1.0 mm**).

---

## Logo / license artwork (WISC reference)

| File | Use |
|---|---|
| [`Wannes-PCB-logo.png`](Wannes-PCB-logo.png) | Board logo (from WISC library) |
| [`Cc-by-nc-sa_icon.svg.png`](Cc-by-nc-sa_icon.svg.png) | CC BY-NC-SA mark |
| `W annes illiams.jpg` / inverted variant | Author mark (optional) |

Footprint sources live under [`../wisc-board/211201 wisc2-5-3/Wannes-library.pretty/`](../wisc-board/211201%20wisc2-5-3/Wannes-library.pretty/) — copy into `projects/wanos-board/` at **L1 implement**, do not edit reference KiCad trees.

---

## Related

- [`board-spec.md`](../../board-spec.md) § 8 — fab + silk rules
- [`kicad-setup.md`](../../kicad-setup.md) — tooling
- WISC 2.5.3 production summary → [`../wisc-board/wisc-v5-2-5-3-production.md`](../wisc-board/wisc-v5-2-5-3-production.md)
