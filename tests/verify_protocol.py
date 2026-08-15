#!/usr/bin/env python3
"""Dependency-free regression checks for the Technibel IR protocol."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / "docs/captures/fan-campaign-2026-08-15.jsonl"
HEADER = ROOT / "esphome/libraries/technibel_ir.h"

FAN_NIBBLES = {
    "FAN_AUTO": 0x8,
    "FAN_1": 0xC,
    "FAN_2": 0xA,
    "FAN_3": 0xE,
    "FAN_4": 0x9,
    "FAN_5": 0xD,
    "FAN_6": 0xB,
}
LABELED_CAPTURES = {
    "AUTO": FAN_NIBBLES["FAN_AUTO"],
    "FAN 1": FAN_NIBBLES["FAN_1"],
    "FAN 2": FAN_NIBBLES["FAN_2"],
    "FAN 3": FAN_NIBBLES["FAN_3"],
    "FAN 4 repeat": FAN_NIBBLES["FAN_4"],
    "FAN 5 first attempt": FAN_NIBBLES["FAN_5"],
    "FAN 6": FAN_NIBBLES["FAN_6"],
}
FIXED_OFF = bytes.fromhex("D0 AC A8 08 03 A4")
KNOWN_COOL = bytes.fromhex("D0 6C 28 18 03 B4")


def reverse_bits(value: int) -> int:
    return int(f"{value:08b}"[::-1], 2)


def checksum(frame: bytes) -> int:
    total = sum(reverse_bits(frame[index]) for index in (1, 2, 3)) + 0xCB
    return reverse_bits(total & 0xFF)


def build_frame(mode: int, setpoint: int, fan: int, power: bool, ambient: int) -> bytes:
    if not power:
        return FIXED_OFF
    byte1 = ((reverse_bits(ambient - 4) >> 4) << 4) | mode
    byte2 = ((reverse_bits(setpoint - 4) >> 4) << 4) | fan
    frame = bytes((0xD0, byte1, byte2, 0x18, 0x03, 0x00))
    return frame[:5] + bytes((checksum(frame),))


def frame_to_raw(frame: bytes) -> list[int]:
    raw = [6500, -3300]
    for byte in frame:
        for shift in range(7, -1, -1):
            raw.extend((450, -2200 if byte & (1 << shift) else -900))
    raw.append(450)
    return raw


def decode_capture(raw: list[int], symbol_count: int) -> bytes:
    assert symbol_count == len(raw) == 99
    assert raw[0] < 0 and raw[-1] < 0
    pulses = raw[1:97:2]
    spaces = raw[2:97:2]
    assert len(pulses) == len(spaces) == 48
    assert all(pulse > 0 for pulse in pulses)
    bits = [int(abs(space) > 1500) for space in spaces]
    return bytes(
        sum(bits[offset + bit] << (7 - bit) for bit in range(8))
        for offset in range(0, 48, 8)
    )


def verify_header_contract(expected_fans: dict[str, int] = FAN_NIBBLES) -> None:
    source = HEADER.read_text()
    for name, value in expected_fans.items():
        match = re.search(rf"\b{name}\s*=\s*0x([0-9A-Fa-f]+)", source)
        assert match and int(match.group(1), 16) == value, name
    compact = re.sub(r"\s+", "", source)
    assert "if(!power)return{0xD0,0xAC,0xA8,0x08,0x03,0xA4};" in compact
    for term in ("technibel_reverse_bits(B1)", "technibel_reverse_bits(B2)",
                 "technibel_reverse_bits(B3)", "+0xCB"):
        assert term in compact, term


def verify_captures() -> int:
    records = [json.loads(line) for line in CAPTURES.read_text().splitlines()]
    canonical = [record for record in records if record.get("symbol_count") == 99]
    assert len(canonical) == 21

    decoded: dict[str, list[bytes]] = {}
    fan_nibbles = set()
    for record in canonical:
        frame = decode_capture(record["raw"], record["symbol_count"])
        assert frame[0] == 0xD0
        assert frame[3:5] == b"\x18\x03"
        assert frame[5] == checksum(frame), record["captured_at"]
        fan_nibbles.add(frame[2] & 0x0F)
        decoded.setdefault(record["operator_label"], []).append(frame)

    assert fan_nibbles == set(FAN_NIBBLES.values())
    for label, expected in LABELED_CAPTURES.items():
        assert any((frame[2] & 0x0F) == expected for frame in decoded[label]), label
    return len(canonical)


def verify_generator() -> None:
    assert build_frame(0xC, 24, FAN_NIBBLES["FAN_AUTO"], True, 26) == KNOWN_COOL
    assert build_frame(0xC, 30, FAN_NIBBLES["FAN_6"], False, 16) == FIXED_OFF
    assert len(frame_to_raw(KNOWN_COOL)) == 99

    altered = dict(FAN_NIBBLES)
    altered["FAN_6"] = 0x0
    try:
        verify_header_contract(altered)
    except AssertionError:
        pass
    else:
        raise AssertionError("negative control did not detect an altered FAN expectation")


def main() -> None:
    verify_header_contract()
    capture_count = verify_captures()
    verify_generator()
    print(f"Technibel protocol verification passed ({capture_count} canonical captures)")


if __name__ == "__main__":
    main()
