# --- file: helpers/find_duplicate_labels.py ---
"""Find net labels sharing the same coordinate in KiCad schematics."""

from __future__ import annotations

import re
import sys
from pathlib import Path

LABEL_RE = re.compile(
    r"\((?:global_label|label) \"([^\"]+)\"[\s\S]*?\(at ([-\d.]+) ([-\d.]+)",
    re.MULTILINE,
)


def scan(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    coords: dict[tuple[float, float], set[str]] = {}
    for match in LABEL_RE.finditer(text):
        net = match.group(1)
        x = round(float(match.group(2)), 2)
        y = round(float(match.group(3)), 2)
        coords.setdefault((x, y), set()).add(net)
    dups = {key: nets for key, nets in coords.items() if len(nets) > 1}
    if not dups:
        return
    print(path.name)
    for (x, y), nets in sorted(dups.items()):
        print(f"  ({x},{y}): {sorted(nets)}")


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path("projects/wanos-board")
    for sch in sorted(root.glob("*.kicad_sch")):
        scan(sch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
