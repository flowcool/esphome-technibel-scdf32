#!/bin/sh
set -eu

base_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
generated_dir="$base_dir/generated"

mkdir -p "$generated_dir"

kicad-cli sch erc \
  "$base_dir/piste-a-reference.kicad_sch" \
  --output "$generated_dir/erc.rpt" \
  --severity-all \
  --exit-code-violations

kicad-cli pcb drc \
  "$base_dir/piste-a-reference.kicad_pcb" \
  --output "$generated_dir/drc.rpt" \
  --schematic-parity \
  --severity-error \
  --exit-code-violations

grep -q '\*\* messages ERC: 0  Errors 0  Warnings 0' "$generated_dir/erc.rpt" || \
  grep -q '\*\* messages ERC: 0  Erreurs 0  Avertissements 0' "$generated_dir/erc.rpt"
grep -q '\*\* Found 0 DRC violations \*\*' "$generated_dir/drc.rpt"
grep -q '\*\* Found 0 unconnected pads \*\*' "$generated_dir/drc.rpt"
grep -q '\*\* Found 0 Footprint errors \*\*' "$generated_dir/drc.rpt"

# Guard against mirroring the top-view XIAO footprint. With USB-C toward row 1,
# the right-hand header must start with 5V, GND, 3V3 from top to bottom.
grep -Eq '\(pad "8" .*\(at 121\.35 58\.33\).*\(net 2 "\+5V"\)' "$base_dir/piste-a-reference.kicad_pcb"
grep -Eq '\(pad "9" .*\(at 121\.35 60\.87\).*\(net 4 "GND"\)' "$base_dir/piste-a-reference.kicad_pcb"
grep -Eq '\(pad "10" .*\(at 121\.35 63\.41\).*\(net 1 "\+3V3"\)' "$base_dir/piste-a-reference.kicad_pcb"

printf '%s\n' 'Piste A KiCad verification passed.'
