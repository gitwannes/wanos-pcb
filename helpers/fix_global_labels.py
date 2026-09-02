# --- file: helpers/fix_global_labels.py ---
"""Convert local net labels to global labels for cross-sheet connectivity."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

# Nets that must be global across hierarchical sheets.
GLOBAL_NETS: frozenset[str] = frozenset(
    {
        "+3V3",
        "+5VA",
        "+12VA",
        "GND",
        "I2C_SCL",
        "I2C_SDA",
        "GPIO_SSR_SAFETY",
        "GPIO_SSR_IR",
        "GPIO_SSR_PHASE_U",
        "GPIO_SSR_PHASE_V",
        "GPIO_SSR_PHASE_W",
        "GPIO_EINK_BUSY",
        "GPIO_EINK_MOSI",
        "GPIO_EINK_RST",
        "GPIO_EINK_SCK",
        "GPIO_EINK_CS",
        "GPIO_EINK_DC",
        "SSR_SAFETY",
        "SSR_IR",
        "SSR_PHASE_U",
        "SSR_PHASE_V",
        "SSR_PHASE_W",
        "EXP_A_P0_DOOR_BATH",
        "EXP_A_P1_DOOR_SAUNA",
        "EXP_A_P2_WM_B1_COLD",
        "EXP_A_P3_WM_B1_HOT",
        "EXP_A_P4_WM_B2_COLD",
        "EXP_A_P5_WM_B2_HOT",
        "EXP_A_P6_KWH_MAIN",
        "EXP_A_P7_KWH_AUX",
        "EXP_B_P0_BTN1",
        "EXP_B_P1_BTN2",
        "EXP_B_P2_BTN3",
        "EXP_B_P3_UI_READY",
        "EXP_B_P4_UI_ERROR",
        "EXP_B_P5_UI_LED",
        "EXP_B_P6_12V_MON",
        "EXP_B_P7_SPARE",
    }
)

LABEL_BLOCK_RE = re.compile(
    r"\t\(label \"([^\"]+)\"(?P<body>.*?)(?=\n\t\))",
    re.DOTALL,
)


def _in_global_set(net_name: str) -> bool:
    return net_name in GLOBAL_NETS


def convert_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0

    def replacer(match: re.Match[str]) -> str:
        nonlocal changed
        net_name = match.group(1)
        if not _in_global_set(net_name):
            return match.group(0)
        body = match.group("body")
        changed += 1
        return f'\t(global_label "{net_name}"\n\t\t(shape bidirectional){body}'

    new_text = LABEL_BLOCK_RE.sub(replacer, text)
    if changed:
        path.write_text(new_text, encoding="utf-8")
    return changed


def main(argv: Iterable[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("projects/wanos-board")
    total = 0
    for sch in sorted(root.glob("*.kicad_sch")):
        count = convert_file(sch)
        if count:
            print(f"{sch.name}: converted {count} labels")
            total += count
    print(f"Total converted: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
