# --- file: projects/wanos-remote/_regen_schematic.py ---
"""Generate wanos-remote.kicad_sch from docs/remotepcb.md locks."""
from __future__ import annotations

import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "wanos-remote.kicad_sch"
LOCAL_SYM = ROOT / "wanos-remote.kicad_sym"
KICAD_SYM = Path(r"C:\Program Files\KiCad\10.0\share\kicad\symbols")
SHEET_UUID = "2ab6cac6-33d4-4a9a-8065-7c5b426b4bb1"
PROJ = "wanos-remote"

PIN = {
    "Conn_01x03": {1: (-5.08, 2.54), 2: (-5.08, 0.0), 3: (-5.08, -2.54)},
    "Conn_01x08": {
        1: (-5.08, 7.62),
        2: (-5.08, 5.08),
        3: (-5.08, 2.54),
        4: (-5.08, 0.0),
        5: (-5.08, -2.54),
        6: (-5.08, -5.08),
        7: (-5.08, -7.62),
        8: (-5.08, -10.16),
    },
    "R": {1: (0.0, 3.81), 2: (0.0, -3.81)},
    "C": {1: (0.0, 3.81), 2: (0.0, -3.81)},
    "LED": {1: (-3.81, 0.0), 2: (3.81, 0.0)},
    "D_TVS": {1: (-3.81, 0.0), 2: (3.81, 0.0)},
    "SW": {1: (-5.08, 0.0), 2: (5.08, 0.0)},
}


def uid() -> str:
    return str(uuid.uuid4())


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


def pin_xy(ax: float, ay: float, rot: int, kind: str, pin: int) -> tuple[float, float]:
    lx, ly = PIN[kind][pin]
    rx, ry = rot_local(lx, ly, rot)
    return ax + rx, ay - ry


def extract_symbol(text: str, name: str) -> str:
    needle = f'(symbol "{name}"'
    start = text.find(needle)
    if start < 0:
        raise RuntimeError(f"missing {name}")
    i = start + len(needle)
    depth = 1
    while i < len(text) and depth:
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
        i += 1
    return text[start:i]


def load_libs() -> str:
    texts = {
        "Connector_Generic": (KICAD_SYM / "Connector_Generic.kicad_sym").read_text(
            encoding="utf-8"
        ),
        "Device": (KICAD_SYM / "Device.kicad_sym").read_text(encoding="utf-8"),
        "power": (KICAD_SYM / "power.kicad_sym").read_text(encoding="utf-8"),
        "Switch": (KICAD_SYM / "Switch.kicad_sym").read_text(encoding="utf-8"),
        "Regulator_Linear": (KICAD_SYM / "Regulator_Linear.kicad_sym").read_text(
            encoding="utf-8"
        ),
        "Interface_Expansion": (KICAD_SYM / "Interface_Expansion.kicad_sym").read_text(
            encoding="utf-8"
        ),
        "local": LOCAL_SYM.read_text(encoding="utf-8"),
    }
    # (lib_key, bare_name_in_file, embedded_lib_id)
    specs = [
        ("Connector_Generic", "Conn_01x03", "Connector_Generic:Conn_01x03"),
        ("Connector_Generic", "Conn_01x08", "Connector_Generic:Conn_01x08"),
        ("Device", "R", "Device:R"),
        ("Device", "C", "Device:C"),
        ("Device", "LED", "Device:LED"),
        ("Device", "D_TVS", "Device:D_TVS"),
        ("Switch", "SW_Push", "Switch:SW_Push"),
        ("power", "+3V3", "power:+3V3"),
        ("power", "GND", "power:GND"),
        ("Regulator_Linear", "AP2204K-3.3", "Regulator_Linear:AP2204K-3.3"),
        ("Interface_Expansion", "MCP23017x-x-SO", "Interface_Expansion:MCP23017x-x-SO"),
        ("local", "DS2482-800", "DS2482-800"),
        ("local", "TLP281-4", "TLP281-4"),
    ]
    parts: list[str] = []
    for key, bare, lib_id in specs:
        sym = extract_symbol(texts[key], bare)
        if bare != lib_id:
            sym = sym.replace(f'(symbol "{bare}"', f'(symbol "{lib_id}"', 1)
        parts.append(sym)
    return "\n\t\t".join(parts)


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


def place(
    lib_id: str,
    ref: str,
    value: str,
    x: float,
    y: float,
    rot: int,
    footprint: str,
    pins: list[str],
    unit: int = 1,
) -> str:
    pin_blk = "\n".join(
        f"""\t\t(pin "{p}"
\t\t\t(uuid "{uid()}")
\t\t)"""
        for p in pins
    )
    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x:g} {y:g} {rot})
\t\t(unit {unit})
\t\t(body_style 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(in_pos_files yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
{prop("Reference", ref if unit == 1 else f"{ref}", x, y - 5.08)}
{prop("Value", value, x, y + 5.08)}
{prop("Footprint", footprint, x, y, hide=True)}
{prop("Datasheet", "", x, y, hide=True)}
{prop("Description", "", x, y, hide=True)}
{pin_blk}
\t\t(instances
\t\t\t(project "{PROJ}"
\t\t\t\t(path "/{SHEET_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit {unit})
\t\t\t\t)
\t\t\t)
\t\t)
\t)"""


def place_pwr(lib_id: str, value: str, ref: str, x: float, y: float) -> str:
    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x:g} {y:g} 0)
\t\t(unit 1)
\t\t(body_style 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(in_pos_files yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
{prop("Reference", ref, x, y + 3.81, hide=True)}
{prop("Value", value, x, y - 3.81)}
{prop("Footprint", "", x, y, hide=True)}
{prop("Datasheet", "", x, y, hide=True)}
{prop("Description", "", x, y, hide=True)}
\t\t(pin "1"
\t\t\t(uuid "{uid()}")
\t\t)
\t\t(instances
\t\t\t(project "{PROJ}"
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
\t\t(uuid "{uid()}")
\t)"""


def label(name: str, x: float, y: float, rot: int = 0) -> str:
    return f"""\t(global_label "{name}"
\t\t(shape input)
\t\t(at {x:g} {y:g} {rot})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify left)
\t\t)
\t\t(uuid "{uid()}")
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


def nc(x: float, y: float) -> str:
    return f"""\t(no_connect
\t\t(at {x:g} {y:g})
\t\t(uuid "{uid()}")
\t)"""


def note(body: str, x: float, y: float) -> str:
    esc = body.replace("\\", "\\\\").replace('"', '\\"')
    return f"""\t(text "{esc}"
\t\t(exclude_from_sim no)
\t\t(at {x:g} {y:g} 0)
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify left bottom)
\t\t)
\t\t(uuid "{uid()}")
\t)"""


def main() -> None:
    o: list[str] = []
    pn = 1

    def gnd(x: float, y: float) -> None:
        nonlocal pn
        o.append(place_pwr("power:GND", "GND", f"#PWR{pn}", x, y))
        pn += 1

    def v3(x: float, y: float) -> None:
        nonlocal pn
        o.append(place_pwr("power:+3V3", "+3V3", f"#PWR{pn}", x, y))
        pn += 1

    fp_r = "Resistor_SMD:R_0603_1608Metric"
    fp_c = "Capacitor_SMD:C_0805_2012Metric"
    fp_led = "LED_SMD:LED_0603_1608Metric"
    fp_tvs = "Diode_SMD:D_SMB"
    fp_esd = "Diode_SMD:D_SOD-323"
    fp_j3 = "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical"
    fp_rj = "Connector_RJ:RJ45_Amphenol_54602-x08_Horizontal"
    fp_sw = "Button_Switch_SMD:SW_SPST_PTS645"
    fp_mcp = "Package_SO:SOIC-28W_7.5x17.9mm_P1.27mm"
    fp_ds = "Package_SO:TSSOP-16_4.4x5mm_P0.65mm"
    fp_ldo = "Package_TO_SOT_SMD:SOT-23-5"
    fp_tlp = "Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"

    o.append(
        note(
            "wanos-remote v0.1 — docs/remotepcb.md\\n"
            "MCP 0x22 GPA0-3 pulses; DS2482 0x18 IO0-3; no INT; VIN SMBJ12A",
            25,
            195,
        )
    )

    # === J1 RJ45 ===
    # T568B: 1=SCL_J 2=GND 3=SDA_J 6=GND 5=VIN 4=GND 7=GND 8=GND
    jx, jy = 35, 160
    o.append(
        place(
            "Connector_Generic:Conn_01x08",
            "J1",
            "RJ45",
            jx,
            jy,
            0,
            fp_rj,
            [str(i) for i in range(1, 9)],
        )
    )
    jack = {
        1: "I2C_SCL_J",
        2: "GND",
        3: "I2C_SDA_J",
        4: "GND",
        5: "VIN",
        6: "GND",
        7: "GND",
        8: "GND",
    }
    for p, net in jack.items():
        px, py = pin_xy(jx, jy, 0, "Conn_01x08", p)
        lx = px - 15.24
        o.append(wire(px, py, lx, py))
        if net == "GND":
            gnd(lx, py)
        else:
            o.append(label(net, lx, py, 180))
    o.append(note("J1 T568B: 1 SCL 2 GND 3 SDA 6 GND | 5 VIN 4 GND | 7-8 GND", 20, 175))

    # D10 SMBJ12A VIN-GND
    o.append(place("Device:D_TVS", "D10", "SMBJ12A", 70, 175, 90, fp_tvs, ["1", "2"]))
    o.append(label("VIN", 70, 185, 90))
    gnd(70, 165)

    # R17 S0_RAIL
    o.append(place("Device:R", "R17", "10R", 85, 160, 0, fp_r, ["1", "2"]))
    o.append(label("VIN", 85, 168, 90))
    o.append(label("S0_RAIL", 85, 152, 270))
    o.append(place("Device:C", "C5", "10u", 95, 155, 0, fp_c, ["1", "2"]))
    o.append(label("S0_RAIL", 95, 163, 90))
    gnd(95, 147)
    o.append(place("Device:C", "C6", "100n", 105, 155, 0, fp_c, ["1", "2"]))
    o.append(label("S0_RAIL", 105, 163, 90))
    gnd(105, 147)

    # Power LED
    o.append(place("Device:R", "R18", "6k8", 120, 170, 0, fp_r, ["1", "2"]))
    o.append(label("S0_RAIL", 120, 178, 90))
    o.append(label("LED_PWR", 120, 162, 270))
    o.append(place("Device:LED", "D9", "PWR", 120, 150, 0, fp_led, ["1", "2"]))
    o.append(label("LED_PWR", 125, 150, 0))
    gnd(115, 150)

    # LDO U4
    o.append(
        place(
            "Regulator_Linear:AP2204K-3.3",
            "U4",
            "AP2204K-3.3",
            150,
            165,
            0,
            fp_ldo,
            ["1", "2", "3", "4", "5"],
        )
    )
    o.append(label("VIN", 138, 167.54, 180))
    o.append(label("VIN", 138, 165, 180))  # EN
    o.append(label("+3V3", 162, 167.54, 0))
    gnd(150, 155)
    o.append(nc(157, 165))
    o.append(place("Device:C", "C7", "100u", 135, 185, 0, fp_c, ["1", "2"]))
    o.append(label("VIN", 135, 193, 90))
    gnd(135, 177)
    o.append(place("Device:C", "C8", "100n", 145, 185, 0, fp_c, ["1", "2"]))
    o.append(label("VIN", 145, 193, 90))
    gnd(145, 177)
    o.append(place("Device:C", "C15", "2u2", 160, 185, 0, fp_c, ["1", "2"]))
    o.append(label("+3V3", 160, 193, 90))
    gnd(160, 177)
    o.append(place("Device:C", "C9", "47u", 170, 185, 0, fp_c, ["1", "2"]))
    o.append(label("+3V3", 170, 193, 90))
    gnd(170, 177)
    o.append(place("Device:C", "C13", "100n", 180, 185, 0, fp_c, ["1", "2"]))
    o.append(label("+3V3", 180, 193, 90))
    gnd(180, 177)
    v3(190, 190)

    # I2C series R19/R20: jack <-> chip
    o.append(place("Device:R", "R19", "22R", 70, 140, 90, fp_r, ["1", "2"]))
    o.append(label("I2C_SDA_J", 70, 150, 90))
    o.append(label("I2C_SDA", 70, 130, 270))
    o.append(place("Device:R", "R20", "22R", 85, 140, 90, fp_r, ["1", "2"]))
    o.append(label("I2C_SCL_J", 85, 150, 90))
    o.append(label("I2C_SCL", 85, 130, 270))

    # === 4 pulse channels ===
    tlp_pins = [
        ["1", "2", "9", "10"],
        ["3", "4", "11", "12"],
        ["5", "6", "13", "14"],
        ["7", "8", "15", "16"],
    ]
    for ch in range(1, 5):
        y = 115 - (ch - 1) * 30
        # JST J2-J5
        o.append(
            place(
                "Connector_Generic:Conn_01x03",
                f"J{ch + 1}",
                f"PULSE{ch}",
                30,
                y,
                0,
                fp_j3,
                ["1", "2", "3"],
            )
        )
        a = pin_xy(30, y, 0, "Conn_01x03", 1)
        s = pin_xy(30, y, 0, "Conn_01x03", 2)
        g_ = pin_xy(30, y, 0, "Conn_01x03", 3)
        o.append(wire(a[0], a[1], a[0] - 12.7, a[1]))
        o.append(label("S0_RAIL", a[0] - 12.7, a[1], 180))
        o.append(wire(s[0], s[1], s[0] - 12.7, s[1]))
        o.append(label(f"SIG{ch}", s[0] - 12.7, s[1], 180))
        o.append(wire(g_[0], g_[1], g_[0] - 7.62, g_[1]))
        gnd(g_[0] - 7.62, g_[1])

        o.append(place("Device:R", f"R{8 + ch}", "4k7", 55, y + 7.62, 0, fp_r, ["1", "2"]))
        o.append(label("S0_RAIL", 55, y + 15, 90))
        o.append(label(f"OPTO_A{ch}", 55, y, 270))

        o.append(
            place(
                "TLP281-4",
                "U1",
                "TLP281-4",
                75,
                y,
                0,
                fp_tlp,
                tlp_pins[ch - 1],
                unit=ch,
            )
        )
        # Labels for opto (positions approximate; ERC may need nudge in UI)
        o.append(label(f"OPTO_A{ch}", 62, y + 2.54, 0))
        o.append(label(f"SIG{ch}", 62, y - 2.54, 0))
        o.append(label(f"OPTO_C{ch}", 88, y + 2.54, 0))
        gnd(88, y - 2.54)

        o.append(place("Device:R", f"R{ch}", "470R", 105, y + 2.54, 90, fp_r, ["1", "2"]))
        o.append(label(f"OPTO_C{ch}", 105, y + 12, 90))
        o.append(label(f"PULSE_CH{ch}", 105, y - 6, 270))

        o.append(place("Device:R", f"R{4 + ch}", "10k", 120, y + 10, 0, fp_r, ["1", "2"]))
        o.append(label("+3V3", 120, y + 18, 90))
        o.append(label(f"PULSE_CH{ch}", 120, y + 4, 270))
        o.append(place("Device:C", f"C{ch}", "100n", 130, y + 4, 0, fp_c, ["1", "2"]))
        o.append(label(f"PULSE_CH{ch}", 130, y + 12, 90))
        gnd(130, y - 4)
        o.append(place("Device:D_TVS", f"D{ch}", "ESD5B5.0", 140, y + 4, 90, fp_esd, ["1", "2"]))
        o.append(label(f"PULSE_CH{ch}", 140, y + 12, 90))
        gnd(140, y - 4)

        o.append(place("Device:LED", f"D{4 + ch}", "ACT", 155, y + 10, 0, fp_led, ["1", "2"]))
        o.append(label("LED_ACT", 148, y + 10, 180))
        o.append(place("Device:R", f"R{12 + ch}", "1k0", 170, y + 10, 90, fp_r, ["1", "2"]))
        o.append(label(f"PULSE_CH{ch}", 170, y + 2, 270))
        # LED cathode path: LED K -> R -> PULSE (anode on LED_ACT)
        o.append(label(f"ACT_K{ch}", 160, y + 10, 0))
        o.append(label(f"ACT_K{ch}", 170, y + 18, 90))

    o.append(place("Switch:SW_Push", "SW1", "TEST", 190, 40, 0, fp_sw, ["1", "2"]))
    o.append(label("+3V3", 178, 40, 180))
    o.append(label("LED_ACT", 202, 40, 0))

    # === MCP U3 ===
    o.append(
        place(
            "Interface_Expansion:MCP23017x-x-SO",
            "U3",
            "MCP23017A",
            230,
            95,
            0,
            fp_mcp,
            [str(i) for i in range(1, 29)],
        )
    )
    o.append(
        note(
            "U3 MCP23017A 0x22\\nGPA0-3=PULSE_CH1-4\\nA0=GND A1=+3V3 A2=GND\\n"
            "~RESET=+3V3 INTA/INTB NC\\nunused GPIO NC (FW drive LOW)",
            210,
            130,
        )
    )
    o.append(label("I2C_SCL", 210, 115, 180))
    o.append(label("I2C_SDA", 210, 112, 180))
    o.append(label("+3V3", 210, 92, 180))  # RESET
    o.append(nc(212, 100))
    o.append(nc(212, 97))
    gnd(210, 80)  # A0
    o.append(label("+3V3", 210, 77, 180))  # A1
    gnd(210, 74)  # A2
    o.append(label("+3V3", 230, 125, 90))
    gnd(230, 65)
    o.append(label("PULSE_CH1", 250, 115, 0))
    o.append(label("PULSE_CH2", 250, 112, 0))
    o.append(label("PULSE_CH3", 250, 109, 0))
    o.append(label("PULSE_CH4", 250, 106, 0))
    for yy in range(60, 105, 3):
        o.append(nc(248, float(yy)))
    o.append(place("Device:C", "C12", "100n", 260, 125, 0, fp_c, ["1", "2"]))
    o.append(label("+3V3", 260, 133, 90))
    gnd(260, 117)
    o.append(place("Device:C", "C10", "10u", 270, 125, 0, fp_c, ["1", "2"]))
    o.append(label("+3V3", 270, 133, 90))
    gnd(270, 117)

    # === DS2482 U2 ===
    o.append(
        place(
            "DS2482-800",
            "U2",
            "DS2482-800",
            320,
            100,
            0,
            fp_ds,
            [str(i) for i in range(1, 17)],
        )
    )
    o.append(
        note(
            "U2 DS2482-800 0x18\\nIO0-3 temps IO4-7 NC\\nAD0-2=GND",
            300,
            130,
        )
    )
    o.append(label("I2C_SDA", 295, 108, 180))
    o.append(label("I2C_SCL", 295, 105, 180))
    o.append(label("+3V3", 320, 120, 90))
    gnd(320, 80)
    o.append(label("OW0", 345, 110, 0))
    o.append(label("OW1", 345, 107, 0))
    o.append(label("OW2", 345, 104, 0))
    o.append(label("OW3", 345, 101, 0))
    for yy in (95, 92, 89, 86):
        o.append(nc(343, float(yy)))
    gnd(295, 95)
    gnd(295, 92)
    gnd(295, 89)
    o.append(nc(295, 86))
    o.append(place("Device:C", "C11", "100n", 340, 125, 0, fp_c, ["1", "2"]))
    o.append(label("+3V3", 340, 133, 90))
    gnd(340, 117)
    o.append(place("Device:C", "C14", "100n", 350, 125, 0, fp_c, ["1", "2"]))
    o.append(label("+3V3", 350, 133, 90))
    gnd(350, 117)

    for i in range(4):
        y = 55 - i * 18
        o.append(place("Device:R", f"R{21 + i}", "2k2", 300, y, 0, fp_r, ["1", "2"]))
        o.append(label("+3V3", 300, y + 8, 90))
        o.append(label(f"OW{i}", 300, y - 8, 270))
        o.append(
            place(
                "Connector_Generic:Conn_01x03",
                f"J{6 + i}",
                f"TEMP{i + 1}",
                330,
                y,
                0,
                fp_j3,
                ["1", "2", "3"],
            )
        )
        t1 = pin_xy(330, y, 0, "Conn_01x03", 1)
        t2 = pin_xy(330, y, 0, "Conn_01x03", 2)
        t3 = pin_xy(330, y, 0, "Conn_01x03", 3)
        o.append(wire(t1[0], t1[1], t1[0] - 10, t1[1]))
        o.append(label("+3V3", t1[0] - 10, t1[1], 180))
        o.append(wire(t2[0], t2[1], t2[0] - 10, t2[1]))
        o.append(label(f"OW{i}", t2[0] - 10, t2[1], 180))
        o.append(wire(t3[0], t3[1], t3[0] - 7, t3[1]))
        gnd(t3[0] - 7, t3[1])

    sch = f"""(kicad_sch
\t(version 20250610)
\t(generator "wanos-remote-_regen_schematic")
\t(generator_version "1.0")
\t(uuid "{SHEET_UUID}")
\t(paper "A3")
\t(title_block
\t\t(title "wanos-remote")
\t\t(date "2026-09-21")
\t\t(rev "0.1")
\t\t(company "wanos")
\t\t(comment 1 "4x opto pulse + 4x DS18B20 / DS2482-800")
\t\t(comment 2 "docs/remotepcb.md")
\t)
\t(lib_symbols
\t\t{load_libs()}
\t)
{chr(10).join(o)}
\t(sheet_instances
\t\t(path "/"
\t\t\t(page "1")
\t\t)
\t)
\t(embedded_fonts no)
)
"""
    OUT.write_text(sch, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
