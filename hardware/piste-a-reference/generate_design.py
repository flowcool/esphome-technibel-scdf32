#!/usr/bin/env python3
"""Generate the checked KiCad schematic and perfboard layout for Piste A.

Run with a Python environment containing ``kicad-sch-api``. KiCad itself is
used afterwards for ERC, DRC, and printable exports.
"""

from pathlib import Path

import kicad_sch_api as ksa


ROOT = Path(__file__).resolve().parent
SCH = ROOT / "piste-a-reference.kicad_sch"
PCB = ROOT / "piste-a-reference.kicad_pcb"
WIRE_TABLE = ROOT / "wiring-table.md"

PITCH = 2.54
BOARD_X = 100.0
BOARD_Y = 50.0
BOARD_W = 30.0
BOARD_H = 70.0
GRID_X = BOARD_X + (BOARD_W - 9 * PITCH) / 2
GRID_Y = BOARD_Y + (BOARD_H - 23 * PITCH) / 2

NETS = {
    "+3V3": 1,
    "+5V": 2,
    "BASE": 3,
    "GND": 4,
    "GPIO3": 5,
    "IR_ANODE": 6,
    "IR_CATHODE": 7,
}


def xy(coord: str) -> tuple[float, float]:
    """Convert a perfboard coordinate such as H8 to KiCad millimetres."""
    col = ord(coord[0].upper()) - ord("A")
    row = int(coord[1:]) - 1
    if not 0 <= col < 10 or not 0 <= row < 24:
        raise ValueError(f"Invalid perfboard coordinate: {coord}")
    return GRID_X + col * PITCH, GRID_Y + row * PITCH


def fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def fp_text(kind: str, text: str, x: float, y: float, layer: str = "F.Fab", size: float = 0.9,
            hidden: bool = False) -> str:
    hidden_expr = " (hide yes)" if hidden else ""
    return (
        f'    (property "{kind}" "{text}" (at {fmt(x)} {fmt(y)}) (layer "{layer}") '
        f'(effects (font (size {size} {size}) (thickness 0.15))){hidden_expr})\n'
    )


def pad(number: str, coord: str, net: str | None, shape: str = "circle") -> str:
    x, y = xy(coord)
    net_expr = "" if net is None else f' (net {NETS[net]} "{net}")'
    return (
        f'    (pad "{number}" thru_hole {shape} (at {fmt(x)} {fmt(y)}) '
        f'(size 1.8 1.8) (drill 1) (layers "*.Cu" "*.Mask"){net_expr})\n'
    )


def footprint(reference: str, value: str, pads: list[tuple[str, str, str | None]],
              outline: tuple[str, str] | None = None, notes: list[str] | None = None) -> str:
    xs = [xy(coord)[0] for _, coord, _ in pads]
    ys = [xy(coord)[1] for _, coord, _ in pads]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    result = [f'  (footprint "{reference}" (layer "F.Cu")\n']
    result.append(fp_text("Reference", reference, cx, min(ys) - 1.8))
    result.append(fp_text("Value", value, cx, max(ys) + 1.8, "F.Fab", 0.8, hidden=True))
    if outline:
        x1, y1 = xy(outline[0])
        x2, y2 = xy(outline[1])
        result.append(
            f'    (fp_rect (start {fmt(x1 - 1)} {fmt(y1 - 1)}) '
            f'(end {fmt(x2 + 1)} {fmt(y2 + 1)}) '
            '(stroke (width 0.3) (type default)) (fill none) (layer "F.Fab"))\n'
        )
    for number, coord, net in pads:
        result.append(pad(number, coord, net, "rect" if number == "1" else "circle"))
    if notes:
        for index, note in enumerate(notes):
            result.append(
                f'    (fp_text user "{note}" (at {fmt(cx)} {fmt(max(ys) + 3.3 + index * 1.4)}) '
                '(layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))\n'
            )
    result.append("  )\n")
    return "".join(result)


WIRES = [
    ("W01", "GPIO3", "YELLOW", "B3", "A3"),
    ("W02", "GPIO3", "YELLOW", "A3", "A11"),
    ("W03", "GPIO3", "YELLOW", "A11", "B11"),
    ("W04", "BASE", "YELLOW", "E11", "E18"),
    ("W05", "BASE", "YELLOW", "E18", "E20"),
    ("W06", "+3V3", "YELLOW", "H4", "I4"),
    ("W07", "GND", "BLACK", "H3", "I3"),
    ("W08", "GND", "BLACK", "I3", "G3"),
    ("W09", "GND", "BLACK", "F18", "G18"),
    ("W10", "GND", "BLACK", "H20", "G20"),
    ("W11", "+5V", "RED", "H2", "J2"),
    ("W12", "+5V", "RED", "J2", "J21"),
    ("W13", "IR_ANODE", "YELLOW", "F21", "F23"),
    ("W14", "IR_CATHODE", "YELLOW", "D18", "C18"),
    ("W15", "IR_CATHODE", "YELLOW", "C18", "C24"),
    ("W16", "IR_CATHODE", "YELLOW", "C24", "G24"),
    ("W17", "IR_CATHODE", "YELLOW", "G24", "G23"),
    ("W18", "GND", "BLACK", "G3", "G18"),
    ("W19", "GND", "BLACK", "G18", "I18"),
    ("W20", "GND", "BLACK", "G18", "G20"),
    ("W21", "GND", "BLACK", "I17", "I18"),
    ("W22", "GND", "BLACK", "I18", "I19"),
]

TOP_SIDE_JUMPERS = {"W11"}


def build_pcb() -> None:
    lines = [
        '(kicad_pcb (version 20241229) (generator "pcbnew") (generator_version "9.0")\n',
        '  (general (thickness 1.6))\n',
        '  (paper "A4")\n',
        '  (layers\n',
        '    (0 "F.Cu" signal)\n',
        '    (2 "B.Cu" signal)\n',
        '    (5 "F.SilkS" user "F.Silkscreen")\n',
        '    (7 "B.SilkS" user "B.Silkscreen")\n',
        '    (1 "F.Mask" user)\n',
        '    (3 "B.Mask" user)\n',
        '    (17 "Dwgs.User" user "User.Drawings")\n',
        '    (25 "Edge.Cuts" user)\n',
        '    (31 "F.CrtYd" user "F.Courtyard")\n',
        '    (29 "B.CrtYd" user "B.Courtyard")\n',
        '    (35 "F.Fab" user)\n',
        '    (33 "B.Fab" user)\n',
        '  )\n',
        '  (setup (pad_to_mask_clearance 0))\n',
        '  (net 0 "")\n',
    ]
    for name, number in sorted(NETS.items(), key=lambda item: item[1]):
        lines.append(f'  (net {number} "{name}")\n')

    # XIAO: component-side view, USB connector toward row 1.
    u1_pads = [
        ("1", "B2", None), ("2", "B3", "GPIO3"), ("3", "B4", None),
        ("4", "B5", None), ("5", "B6", None), ("6", "B7", None), ("7", "B8", None),
        ("8", "H2", "+5V"), ("9", "H3", "GND"), ("10", "H4", "+3V3"),
        ("14", "H5", None), ("13", "H6", None), ("12", "H7", None), ("11", "H8", None),
    ]
    lines.append(footprint(
        "U1", "XIAO ESP32-C3", u1_pads, ("A1", "I9"),
        None,
    ))
    lines.append(footprint("R1", "470 ohm", [("2", "B11", "GPIO3"), ("1", "E11", "BASE")], ("B11", "E11")))
    lines.append(footprint("Q1", "BC33740BU C-B-E", [("1", "D18", "IR_CATHODE"), ("2", "E18", "BASE"), ("3", "F18", "GND")], ("D18", "F18")))
    lines.append(footprint("R2", "10 kohm", [("1", "E20", "BASE"), ("2", "H20", "GND")], ("E20", "H20")))
    lines.append(footprint("C1", "100 nF", [("2", "I3", "GND"), ("1", "I4", "+3V3")], ("I3", "I4")))
    lines.append(footprint("C2", "100 nF", [("2", "I17", "GND"), ("1", "J17", "+5V")], ("I17", "J17")))
    lines.append(footprint("C3", "100 uF", [("2", "I19", "GND"), ("1", "J19", "+5V")], ("I19", "J19")))
    lines.append(footprint("R3", "47 ohm / 0.6 W", [("1", "J21", "+5V"), ("2", "F21", "IR_ANODE")], ("F21", "J21")))
    lines.append(footprint("D1", "TSAL6400", [("2", "F23", "IR_ANODE"), ("1", "G23", "IR_CATHODE")], ("F23", "G23")))

    # Board edge and coordinate grid.
    x1, y1 = BOARD_X, BOARD_Y
    x2, y2 = BOARD_X + BOARD_W, BOARD_Y + BOARD_H
    for start, end in [((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))]:
        lines.append(
            f'  (gr_line (start {fmt(start[0])} {fmt(start[1])}) (end {fmt(end[0])} {fmt(end[1])}) '
            '(stroke (width 0.4) (type default)) (layer "Edge.Cuts"))\n'
        )
    for col in "ABCDEFGHIJ":
        x, _ = xy(f"{col}1")
        lines.append(f'  (gr_text "{col}" (at {fmt(x)} {fmt(BOARD_Y + 2)}) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n')
    for row in range(1, 25):
        _, y = xy(f"A{row}")
        lines.append(f'  (gr_text "{row}" (at {fmt(BOARD_X + 1.2)} {fmt(y)}) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))\n')
        for col in "ABCDEFGHIJ":
            x, _ = xy(f"{col}{row}")
            lines.append(
                f'  (gr_circle (center {fmt(x)} {fmt(y)}) (end {fmt(x + 0.65)} {fmt(y)}) '
                '(stroke (width 0.12) (type default)) (fill none) (layer "Dwgs.User"))\n'
            )

    # Insulated point-to-point wires are represented as B.Cu for deterministic DRC.
    for wire_id, net, _color, start, end in WIRES:
        sx, sy = xy(start)
        ex, ey = xy(end)
        layer = "F.Cu" if wire_id in TOP_SIDE_JUMPERS else "B.Cu"
        lines.append(
            f'  (segment (start {fmt(sx)} {fmt(sy)}) (end {fmt(ex)} {fmt(ey)}) '
            f'(width 0.55) (layer "{layer}") (net {NETS[net]}))\n'
        )
    # J2 is the soldered handoff between the component-side 5 V jumper W11
    # and the solder-side 5 V rail W12.
    j8x, j8y = xy("J2")
    lines.append(
        f'  (via (at {fmt(j8x)} {fmt(j8y)}) (size 1.8) (drill 1) '
        f'(layers "F.Cu" "B.Cu") (net {NETS["+5V"]}))\n'
    )
    lines.append(")\n")
    PCB.write_text("".join(lines), encoding="utf-8")


def build_wire_table() -> None:
    rows = [
        "# Piste A perfboard wiring table\n\n",
        "Coordinate convention: component-side view, USB-C toward row 1. The solder-side drawing is mirrored by KiCad.\n\n",
        "| Wire | Net | Color | Side | From | To | Straight length |\n",
        "|---|---|---|---|---|---|---:|\n",
    ]
    for wire_id, net, color, start, end in WIRES:
        sx, sy = xy(start)
        ex, ey = xy(end)
        length = abs(ex - sx) + abs(ey - sy)
        side = "component-side jumper" if wire_id in TOP_SIDE_JUMPERS else "solder side"
        rows.append(f"| {wire_id} | `{net}` | {color} | {side} | `{start}` | `{end}` | {length:.1f} mm |\n")
    rows.extend([
        "\n## Component coordinates\n\n",
        "| Ref | Value | Pin coordinates |\n",
        "|---|---|---|\n",
        "| U1 | XIAO ESP32-C3, 2x7 sockets | pin 2/D1/GPIO3=`B3`; pin 8/5V=`H2`; pin 9/GND=`H3`; pin 10/3V3=`H4`; all 14 pins represented |\n",
        "| R1 | 470 ohm | 2/GPIO3=`B11`; 1/BASE=`E11` |\n",
        "| Q1 | BC33740BU | 1/C=`D18`; 2/B=`E18`; 3/E=`F18` |\n",
        "| R2 | 10 kohm | 1/BASE=`E20`; 2/GND=`H20` |\n",
        "| C1 | 100 nF | 2/GND=`I3`; 1/3V3=`I4` |\n",
        "| C2 | 100 nF | 2/GND=`I17`; 1/5V=`J17` |\n",
        "| C3 | 100 uF | 2/GND=`I19`; 1/+5V=`J19` |\n",
        "| R3 | 47 ohm / 0.6 W | 1/5V=`J21`; 2/IR_ANODE=`F21` |\n",
        "| D1 | fresh TSAL6400 | 2/A=`F23`; 1/K=`G23` |\n",
    ])
    WIRE_TABLE.write_text("".join(rows), encoding="utf-8")


def build_schematic() -> None:
    sch = ksa.create_schematic("Technibel Piste A reference perfboard")
    sch.set_paper_size("A4")
    sch.set_title_block(
        title="Technibel Piste A reference perfboard",
        date="2026-08-16",
        rev="1",
        company="esphome-technibel-scdf32",
        comments={
            1: "BC33740BU: C-B-E with flat face toward viewer",
            2: "Fresh TSAL6400: verify A/K before soldering",
        },
    )

    add = sch.components.add
    add("Connector_Generic:Conn_02x07_Counter_Clockwise", "U1", "XIAO ESP32-C3", (35.56, 88.9))
    add("Device:R", "R1", "470 ohm", (63.5, 76.2), rotation=90)
    add("Transistor_BJT:Q_NPN_CBE", "Q1", "BC33740BU", (88.9, 88.9))
    add("Device:R", "R2", "10 kohm", (76.2, 104.14))
    add("Device:LED", "D1", "TSAL6400", (109.22, 76.2))
    add("Device:R", "R3", "47 ohm / 0.6 W", (132.08, 76.2), rotation=90)
    add("Device:C", "C2", "100 nF", (119.38, 101.6))
    add("Device:C_Polarized", "C3", "100 uF", (134.62, 101.6))
    add("Device:C", "C1", "100 nF", (55.88, 116.84))

    nets = {
        "GPIO3": [("U1", "2"), ("R1", "1")],
        "BASE": [("R1", "2"), ("Q1", "2"), ("R2", "1")],
        "GND": [
            ("U1", "9"),
            ("Q1", "3"),
            ("R2", "2"),
            ("C1", "2"),
            ("C2", "2"),
            ("C3", "2"),
        ],
        "IR_CATHODE": [("Q1", "1"), ("D1", "1")],
        "IR_ANODE": [("D1", "2"), ("R3", "1")],
        "+5V": [("U1", "8"), ("R3", "2"), ("C2", "1"), ("C3", "1")],
        "+3V3": [("U1", "10"), ("C1", "1")],
    }
    for net_name, pins in nets.items():
        for ref, pin in pins:
            sch.add_label(net_name, pin=(ref, pin), size=1.0)
    for pin in ("1", "3", "4", "5", "6", "7", "11", "12", "13", "14"):
        position = sch.get_component_pin_position("U1", pin)
        if position is None:
            raise RuntimeError(f"Could not locate unused U1 pin {pin}")
        sch.no_connects.add(position)

    sch.add_text(
        "Canonical circuit — physical routing is checked separately on the perfboard layout.",
        (25.4, 25.4),
        size=2.0,
        bold=True,
    )
    sch.add_text(
        "D1 pin 1 = K/cathode to Q1.C; D1 pin 2 = A/anode to R3. "
        "C2 and C3 are directly across 5V/GND before R3.",
        (25.4, 30.48),
        size=1.27,
    )
    sch.add_text(
        "Q1 BC33740BU pin 1=C, pin 2=B, pin 3=E. XIAO GPIOs are not 5 V tolerant.",
        (25.4, 33.02),
        size=1.27,
    )
    sch.add_text(
        "U1 pins: 1=D0, 2=D1/GPIO3, 3=D2, 4=D3, 5=D4, 6=D5, 7=D6; "
        "8=5V, 9=GND, 10=3V3, 11=D7, 12=D8, 13=D9, 14=D10.",
        (25.4, 35.56),
        size=1.27,
    )
    sch.save(SCH)


if __name__ == "__main__":
    build_schematic()
    build_pcb()
    build_wire_table()
