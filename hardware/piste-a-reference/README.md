# Piste A reference perfboard

This directory is the construction authority for the fresh Phase 10 reference
board. The previous hand-drawn/SVG layout is obsolete and must not be used.

## Orientation and coordinates

- Board: isolated-pad FR4 perfboard, 30 × 70 mm, 10 columns × 24 rows.
- Component-side coordinates: columns `A`–`J` left to right, rows `1`–`24`
  top to bottom.
- The XIAO USB-C connector faces row 1.
- The solder-side PDF is already mirrored to match the board as held with the
  solder side facing the operator. Do not mirror it again.

## XIAO ESP32-C3 pin mapping

The schematic and PCB both represent the complete 2×7 XIAO socket:

| Left row, top to bottom | Function | Right row, top to bottom | Function |
|---:|---|---:|---|
| 1 | D0 | 8 | 5V / VBUS |
| 2 | D1 / GPIO3 | 9 | GND |
| 3 | D2 | 10 | 3V3 |
| 4 | D3 | 14 | D10 |
| 5 | D4 | 13 | D9 |
| 6 | D5 | 12 | D8 |
| 7 | D6 | 11 | D7 |

Only pins 2, 8, 9, and 10 are electrically used by this board. All other XIAO
pins remain available and unconnected.

## Mandatory polarity and pinout

- `Q1` is the Mouser onsemi `BC33740BU`. With the flat face toward the observer
  and leads down: pin 1 = Collector, pin 2 = Base, pin 3 = Emitter (`C-B-E`).
- `D1` must be a fresh Mouser Vishay `TSAL6400`: pin 2/anode/long lead at `F23`;
  pin 1/cathode/short lead/flat side at `G23`.
- `C3`: positive pin 1 at `J19`; negative pin 2/stripe at `I19`.
- `C2` and `C3` are directly across 5V and GND, before `R3`.

## Construction hold point

Before soldering, review these native and textual artifacts together:

1. `piste-a-reference.kicad_sch`
2. `piste-a-reference.kicad_pcb`
3. `wiring-table.md`

The current partially assembled board remains untouched as rollback/evidence.
Construction uses a new perfboard and fresh driver components.

## Verification

Install KiCad 9+ and run:

```bash
./verify-design.sh
```

The gate passes only when ERC reports zero errors/warnings and DRC reports zero
violations, zero unconnected pads, and zero schematic-parity problems.

The generator additionally requires `kicad-sch-api==0.5.6`:

```bash
python3 -m venv /tmp/piste-a-kicad-venv
/tmp/piste-a-kicad-venv/bin/pip install -r requirements.txt
/tmp/piste-a-kicad-venv/bin/python generate_design.py
```

Regeneration is deterministic for component placement, net assignments, and
wire coordinates. KiCad-generated UUIDs in the schematic may differ after a
full regeneration.
