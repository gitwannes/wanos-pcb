# --- file: helpers/cleanup_stale_labels.py ---
"""Remove orphaned net labels at old PCA9554 pin x-coordinates."""

from __future__ import annotations

import re
import sys
from pathlib import Path

STALE_X_COORDS = (34.37, 44.53, 119.38)
TOLERANCE = 0.01

LABEL_RE = re.compile(
    r"\t\((?:label|global_label) \"[^\"]+\"\n"
    r"\t\t(?:\(shape [^\)]+\)\n)?"
    r"\t\t\(at (?P<x>[-\d.]+) (?P<y>[-\d.]+)",
    re.MULTILINE,
)


def cleanup(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    removed = 0
    spans: list[tuple[int, int]] = []

    for match in LABEL_RE.finditer(text):
        x = float(match.group("x"))
        if any(abs(x - stale_x) <= TOLERANCE for stale_x in STALE_X_COORDS):
            start = match.start()
            end = text.find("\n\t)", match.end())
            if end == -1:
                continue
            end += len("\n\t)")
            spans.append((start, end))

    if not spans:
        return 0

    for start, end in reversed(spans):
        removed += 1
        text = text[:start] + text[end:]

    path.write_text(text, encoding="utf-8")
    return removed


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else Path("projects/wanos-board/io_expanders.kicad_sch")
    count = cleanup(target)
    print(f"Removed {count} stale labels from {target.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
