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

printf '%s\n' 'Piste A KiCad verification passed.'
