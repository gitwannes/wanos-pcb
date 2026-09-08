# --- file: projects/wanos-board/_regen_pulse_inputs.py ---
"""Generate pulse_inputs.kicad_sch: greenfield door (reed) + kWh (SDM72) front-ends."""

from __future__ import annotations

import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "pulse_inputs.kicad_sch"
IO = ROOT / "io_expanders.kicad_sch"
PI = ROOT / "pi_power.kicad_sch"
SHEET_UUID = "a7c3e91f-2b4d-4f8a-9e1c-6d5b8a0f3c27"

# Local pin coords from embedded KiCad symbols (unit _1_1)
PIN = {
    "Conn_01x02": {1: (-5.08, 0.0), 2: (-5.08, -2.54)},
    "R": {1: (0.0, 3.81), 2: (0.0, -3.81)},
    "C": {1: (0.0, 3.81), 2: (0.0, -3.81)},
    "LED": {1: (-3.81, 0.0), 2: (3.81, 0.0)},  # 1=K, 2=A
    "D_TVS": {1: (-3.81, 0.0), 2: (3.81, 0.0)},
    "PWR": {1: (0.0, 0.0)},
}


def new_uuid() -> str:
    return str(uuid.uuid4())


def extract_symbol(text: str, name: str) -> str:
    needle = f'(symbol "{name}"'
    start = text.find(needle)
    if start < 0:
        raise RuntimeError(f"missing lib symbol {name}")
    i = start + len(needle)
    depth = 1
    while i < len(text) and depth:
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
        i += 1
    return text[start:i]


def extract_lib_symbols() -> str:
    io = IO.read_text(encoding="utf-8")
    pi = PI.read_text(encoding="utf-8")
    names_io = [
        "Connector_Generic:Conn_01x02",
        "Device:C",
        "Device:D_TVS",
        "Device:LED",
        "Device:R",
        "power:+3V3",
        "power:GND",
    ]
    parts = [extract_symbol(io, n) for n in names_io]
    parts.append(extract_symbol(pi, "power:+5VA"))
    return "\n\t\t".join(parts)


def rot_local(x: float, y: float, rot: int) -> tuple[float, float]:
    r = rot % 360
    if r == 0:
        return x, y
    if r == 90:
        return -y, x
    if r == 180:
        return -x, -y
    if r == 270:
        return y, -x
    raise ValueError(rot)


def pin_xy(at_x: float, at_y: float, at_rot: int, kind: str, pin: int) -> tuple[float, float]:
    """Map library pin local -> schematic world.

    KiCad schematic Y is flipped vs symbol local Y for placed instances
    (verified via ERC pin coordinates on Conn_01x02).
    """
    lx, ly = PIN[kind][pin]
    rx, ry = rot_local(lx, ly, at_rot)
    return at_x + rx, at_y - ry


def g(n: float) -> float:
    """Snap to 1.27 mm grid."""
    return round(n / 1.27) * 1.27


def prop(name: str, value: str, x: float, y: float, hide: bool = False) -> str:
    hid = "\n\t\t\t(hide yes)" if hide else ""
    return f"""\t\t(property "{name}" "{value}"
\t\t\t(at {x:g} {y:g} 0)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no){hid}
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)"""


def place_symbol(
    lib_id: str,
    ref: str,
    value: str,
    x: float,
    y: float,
    rot: int,
    footprint: str,
    pin_count: int,
) -> str:
    pins = "\n".join(
        f"""\t\t(pin "{i}"
\t\t\t(uuid "{new_uuid()}")
\t\t)"""
        for i in range(1, pin_count + 1)
    )
    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x:g} {y:g} {rot})
\t\t(unit 1)
\t\t(body_style 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(in_pos_files yes)
\t\t(dnp no)
\t\t(uuid "{new_uuid()}")
{prop("Reference", ref, x, y - 5.08)}
{prop("Value", value, x, y + 5.08)}
{prop("Footprint", footprint, x, y, hide=True)}
{prop("Datasheet", "", x, y, hide=True)}
{prop("Description", "", x, y, hide=True)}
{pins}
\t\t(instances
\t\t\t(project "wanos-board"
\t\t\t\t(path "/b64fe9be-4bba-4a4c-aa66-7fa6f4bbb662/{SHEET_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t\t(project "pulse_inputs"
\t\t\t\t(path "/{SHEET_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)"""


def place_pwr(lib_id: str, value: str, ref: str, x: float, y: float, rot: int = 0) -> str:
    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x:g} {y:g} {rot})
\t\t(unit 1)
\t\t(body_style 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(in_pos_files yes)
\t\t(dnp no)
\t\t(uuid "{new_uuid()}")
{prop("Reference", ref, x, y + 3.81, hide=True)}
{prop("Value", value, x, y - 3.81)}
{prop("Footprint", "", x, y, hide=True)}
{prop("Datasheet", "", x, y, hide=True)}
{prop("Description", "", x, y, hide=True)}
\t\t(pin "1"
\t\t\t(uuid "{new_uuid()}")
\t\t)
\t\t(instances
\t\t\t(project "wanos-board"
\t\t\t\t(path "/b64fe9be-4bba-4a4c-aa66-7fa6f4bbb662/{SHEET_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t\t(project "pulse_inputs"
\t\t\t\t(path "/{SHEET_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)"""


def wire(x1: float, y1: float, x2: float, y2: float) -> str:
    return f"""\t(wire
\t\t(pts
\t\t\t(xy {x1:g} {y1:g})
\t\t\t(xy {x2:g} {y2:g})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{new_uuid()}")
\t)"""


def junction(x: float, y: float) -> str:
    return f"""\t(junction
\t\t(at {x:g} {y:g})
\t\t(diameter 0)
\t\t(color 0 0 0 0)
\t\t(uuid "{new_uuid()}")
\t)"""


def global_label(name: str, x: float, y: float, rot: int = 0) -> str:
    return f"""\t(global_label "{name}"
\t\t(shape input)
\t\t(at {x:g} {y:g} {rot})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify left)
\t\t)
\t\t(uuid "{new_uuid()}")
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"
\t\t\t(at {x:g} {y:g} 0)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t)"""


def text_note(body: str, x: float, y: float) -> str:
    return f"""\t(text "{body}"
\t\t(exclude_from_sim no)
\t\t(at {x:g} {y:g} 0)
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify left bottom)
\t\t)
\t\t(uuid "{new_uuid()}")
\t)"""


def channel(
    *,
    ox: float,
    oy: float,
    j_ref: str,
    j_val: str,
    rpu: str,
    rs: str,
    rled: str,
    c_ref: str,
    tvs: str,
    led: str,
    exp_net: str,
    rail: str,
    pwr_base: int,
    title: str,
) -> tuple[list[str], int]:
    """One channel: J pin1=GND, pin2=SIG -> TVS, Rpu, LED, Rs, Cd -> EXP label."""
    out: list[str] = []
    rail_lib = "power:+5VA" if rail == "+5VA" else "power:+3V3"
    fp_r = "Resistor_SMD:R_0805_2012Metric"
    fp_c = "Capacitor_SMD:C_0805_2012Metric"
    fp_j = "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical"

    # --- Connector ---
    jx, jy, jrot = ox, oy, 0
    out.append(place_symbol("Connector_Generic:Conn_01x02", j_ref, j_val, jx, jy, jrot, fp_j, 2))
    p1 = pin_xy(jx, jy, jrot, "Conn_01x02", 1)
    p2 = pin_xy(jx, jy, jrot, "Conn_01x02", 2)

    # GND on pin1: place power symbol ON the pin
    out.append(place_pwr("power:GND", "GND", f"#PWR{pwr_base}", p1[0], p1[1], 0))
    pwr_base += 1

    # SIG rail to the left of pin2
    sig_y = p2[1]
    # Column X positions (1.27 grid)
    x_sig = p2[0]
    x_tvs = x_sig - 10.16
    x_pu = x_sig - 17.78
    x_led = x_sig - 25.4
    x_rs = x_sig - 38.1
    x_exp = x_sig - 50.8

    out.append(wire(p2[0], p2[1], x_tvs, sig_y))
    out.append(junction(x_tvs, sig_y))
    out.append(wire(x_tvs, sig_y, x_pu, sig_y))
    out.append(junction(x_pu, sig_y))
    out.append(wire(x_pu, sig_y, x_led, sig_y))
    out.append(junction(x_led, sig_y))
    out.append(wire(x_led, sig_y, x_rs + 3.81, sig_y))

    # --- TVS across SIG-GND (rot 270: pins vertical) ---
    # pin2 at SIG, pin1 toward +Y (down) to GND
    tvs_rot = 270
    tvs_at = (x_tvs, sig_y)
    out.append(
        place_symbol("Device:D_TVS", tvs, "PESD5V0S1BA", tvs_at[0], tvs_at[1], tvs_rot, "Diode_SMD:D_SOD-323", 2)
    )
    tp1 = pin_xy(tvs_at[0], tvs_at[1], tvs_rot, "D_TVS", 1)
    tp2 = pin_xy(tvs_at[0], tvs_at[1], tvs_rot, "D_TVS", 2)
    sig_pt = (x_tvs, sig_y)
    def _d2(a, b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2
    if _d2(tp1, sig_pt) <= _d2(tp2, sig_pt):
        sp, gp = tp1, tp2
    else:
        sp, gp = tp2, tp1
    out.append(wire(sp[0], sp[1], x_tvs, sig_y))
    out.append(place_pwr("power:GND", "GND", f"#PWR{pwr_base}", gp[0], gp[1], 0))
    pwr_base += 1

    # --- Pull-up R (vertical): pin1 on SIG, pin2 above to rail ---
    # pin1 world y = at_y - 3.81 = sig_y => at_y = sig_y + 3.81
    pu_at = (x_pu, sig_y + 3.81)
    out.append(place_symbol("Device:R", rpu, "10k", pu_at[0], pu_at[1], 0, fp_r, 2))
    pu1 = pin_xy(pu_at[0], pu_at[1], 0, "R", 1)
    pu2 = pin_xy(pu_at[0], pu_at[1], 0, "R", 2)
    out.append(wire(pu1[0], pu1[1], x_pu, sig_y))
    out.append(place_pwr(rail_lib, rail, f"#PWR{pwr_base}", pu2[0], pu2[1], 0))
    pwr_base += 1

    # --- Activity LED: rail -- Rled -- A -> K -- SIG (lights when SIG low) ---
    # LED rot 270 + Y-flip: place so K hits SIG
    led_at = (x_led, sig_y + 3.81)
    led_rot = 270
    out.append(
        place_symbol("Device:LED", led, "LED", led_at[0], led_at[1], led_rot, "LED_SMD:LED_0805_2012Metric", 2)
    )
    lk = pin_xy(led_at[0], led_at[1], led_rot, "LED", 1)  # K
    la = pin_xy(led_at[0], led_at[1], led_rot, "LED", 2)  # A
    out.append(wire(lk[0], lk[1], x_led, sig_y))

    # Rled: pin1 on anode (Y-flip: at_y - 3.81 = la_y => at_y = la_y + 3.81)
    rled_at = (x_led, la[1] + 3.81)
    out.append(place_symbol("Device:R", rled, "1k0", rled_at[0], rled_at[1], 0, fp_r, 2))
    rl1 = pin_xy(rled_at[0], rled_at[1], 0, "R", 1)
    rl2 = pin_xy(rled_at[0], rled_at[1], 0, "R", 2)
    out.append(wire(rl1[0], rl1[1], la[0], la[1]))
    out.append(place_pwr(rail_lib, rail, f"#PWR{pwr_base}", rl2[0], rl2[1], 0))
    pwr_base += 1

    # --- Series R (horizontal, rot 90): pin1 right toward SIG, pin2 left toward exp ---
    # rot90: pin1 -> (-3.81,0) relative = left; pin2 -> (3.81,0) = right
    # Want right pin on SIG side at x_rs+3.81... place at so pin2 (right) at (x_led already wired to x_rs+3.81)
    rs_at = (x_rs, sig_y)
    rs_rot = 90
    out.append(place_symbol("Device:R", rs, "330", rs_at[0], rs_at[1], rs_rot, fp_r, 2))
    rs1 = pin_xy(rs_at[0], rs_at[1], rs_rot, "R", 1)
    rs2 = pin_xy(rs_at[0], rs_at[1], rs_rot, "R", 2)
    right, left = (rs1, rs2) if rs1[0] > rs2[0] else (rs2, rs1)
    out.append(wire(x_led, sig_y, right[0], right[1]))
    out.append(wire(left[0], left[1], x_exp, sig_y))
    out.append(junction(x_exp, sig_y))

    # --- Debounce C: pin1 on SIG (Y-flip), pin2 to GND ---
    c_at = (x_exp, sig_y + 3.81)
    out.append(place_symbol("Device:C", c_ref, "100n", c_at[0], c_at[1], 0, fp_c, 2))
    c1 = pin_xy(c_at[0], c_at[1], 0, "C", 1)
    c2 = pin_xy(c_at[0], c_at[1], 0, "C", 2)
    out.append(wire(c1[0], c1[1], x_exp, sig_y))
    out.append(place_pwr("power:GND", "GND", f"#PWR{pwr_base}", c2[0], c2[1], 0))
    pwr_base += 1

    # Expander global label on SIG node after series R
    out.append(global_label(exp_net, x_exp, sig_y, 180))
    out.append(text_note(title, ox - 55, oy - 12))

    return out, pwr_base


def main() -> None:
    libs = extract_lib_symbols()
    chunks: list[str] = []
    pwr = 500

    chans = [
        dict(
            ox=88.9,
            oy=45.72,
            j_ref="J2",
            j_val="DOOR_SAUNA",
            rpu="R45",
            rs="R46",
            rled="R47",
            c_ref="C22",
            tvs="D30",
            led="D31",
            exp_net="EXP_A_P1_DOOR_SAUNA",
            rail="+3V3",
            title="Door sauna - reed contact; Rpu to +3V3; TVS+RC; activity LED",
        ),
        dict(
            ox=215.9,
            oy=45.72,
            j_ref="J3",
            j_val="DOOR_BATH",
            rpu="R48",
            rs="R49",
            rled="R50",
            c_ref="C23",
            tvs="D32",
            led="D33",
            exp_net="EXP_A_P0_DOOR_BATH",
            rail="+3V3",
            title="Door bathroom - reed contact; same front-end as sauna",
        ),
        dict(
            ox=88.9,
            oy=121.92,
            j_ref="J6",
            j_val="KWH_MAIN",
            rpu="R51",
            rs="R52",
            rled="R53",
            c_ref="C24",
            tvs="D34",
            led="D35",
            exp_net="EXP_A_P6_KWH_MAIN",
            rail="+5VA",
            title="kWh main SDM72D-M - Rpu to +5VA (meter needs 5-27V); ~10m Cat5",
        ),
        dict(
            ox=215.9,
            oy=121.92,
            j_ref="J7",
            j_val="KWH_AUX",
            rpu="R54",
            rs="R55",
            rled="R56",
            c_ref="C25",
            tvs="D36",
            led="D37",
            exp_net="EXP_A_P7_KWH_AUX",
            rail="+5VA",
            title="kWh aux SDM72D-M - same as main",
        ),
    ]

    for ch in chans:
        parts, pwr = channel(pwr_base=pwr, **ch)
        chunks.extend(parts)

    header = f"""(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{SHEET_UUID}")
\t(paper "A3")
\t(title_block
\t\t(title "wanos-pcb-v1 Pulse Inputs")
\t\t(comment 1 "Doors J2/J3 reed + kWh J6/J7 SDM72; retire duplicate stubs on IO_Expanders")
\t)
\t(lib_symbols
\t\t{libs}
\t)
"""
    footer = """\t(sheet_instances
\t\t(path "/"
\t\t\t(page "1")
\t\t)
\t)
\t(embedded_fonts no)
)
"""
    note = text_note(
        "GREENFIELD - duplicate J2/J3/J6/J7 vs IO_Expanders until old stubs removed. "
        "EXP_A_P* global labels join U1 on IO_Expanders.",
        20,
        15,
    )
    OUT.write_text(header + "\n".join([note] + chunks) + "\n" + footer, encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
