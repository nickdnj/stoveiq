#!/usr/bin/env bash
# Regenerate every hardware render in this repo from source.
#
# Everything here is produced by free and open-source tools:
#   kicad-cli     (KiCad 9/10)  — schematic plots, layer plots, raytraced 3D
#   openscad      (2021.01+)    — enclosure renders
#   rsvg-convert  (librsvg)     — SVG to PNG for GitHub rendering
#
#   macOS:  brew install kicad openscad librsvg
#   Debian: apt install kicad openscad librsvg2-bin
#
# Outputs land in pcb/renders/ and enclosure/renders/ and are committed, so a
# reader of the GitHub page never has to install anything. Re-run this after
# changing the schematic, the board, or either .scad file.
#
# SPDX-License-Identifier: MIT

set -euo pipefail
cd "$(dirname "$0")"

for tool in kicad-cli openscad rsvg-convert; do
    command -v "$tool" >/dev/null || { echo "missing: $tool (see header)" >&2; exit 1; }
done

# ---------------------------------------------------------------------------
# PCB — schematic, layer plots, and raytraced 3D views
# ---------------------------------------------------------------------------
echo "==> PCB"
mkdir -p pcb/renders
pushd pcb >/dev/null

kicad-cli sch export svg -o renders --no-background-color stoveiq.kicad_sch >/dev/null 2>&1
mv -f renders/stoveiq.svg renders/schematic.svg
kicad-cli sch export pdf -o renders/schematic.pdf stoveiq.kicad_sch >/dev/null 2>&1
rsvg-convert -w 3000 -b white renders/schematic.svg -o renders/schematic.png

# 2D layer plots. --fit-page-to-board keeps the page tight around the outline;
# it only does that if no stray footprint text sits off in the weeds.
kicad-cli pcb export svg --mode-single -o renders/layout-top.svg \
    -l 'F.Cu,F.Silkscreen,Edge.Cuts' \
    --exclude-drawing-sheet --fit-page-to-board --drill-shape-opt 2 stoveiq.kicad_pcb >/dev/null 2>&1
kicad-cli pcb export svg --mode-single -o renders/layout-bottom.svg \
    -l 'B.Cu,B.Silkscreen,Edge.Cuts' \
    --exclude-drawing-sheet --fit-page-to-board --mirror --drill-shape-opt 2 stoveiq.kicad_pcb >/dev/null 2>&1
kicad-cli pcb export svg --mode-single -o renders/assembly-drawing.svg \
    -l 'F.Fab,Edge.Cuts' \
    --exclude-drawing-sheet --fit-page-to-board --black-and-white stoveiq.kicad_pcb >/dev/null 2>&1
kicad-cli pcb export pdf -o renders/fab-drawing.pdf \
    -l 'F.Fab,F.Silkscreen,Edge.Cuts' stoveiq.kicad_pcb >/dev/null 2>&1

for f in layout-top layout-bottom assembly-drawing; do
    rsvg-convert -w 2400 -b white "renders/$f.svg" -o "renders/$f.png"
done

kicad-cli pcb render -o renders/board-iso.png    --width 2400 --height 1600 \
    --quality high --floor --perspective --rotate '-35,0,-30' --zoom 0.72 \
    --background opaque stoveiq.kicad_pcb >/dev/null 2>&1
kicad-cli pcb render -o renders/board-top.png    --width 2200 --height 1700 \
    --quality high --side top    --zoom 0.8 --background opaque stoveiq.kicad_pcb >/dev/null 2>&1
kicad-cli pcb render -o renders/board-bottom.png --width 2200 --height 1700 \
    --quality high --side bottom --zoom 0.8 --background opaque stoveiq.kicad_pcb >/dev/null 2>&1

popd >/dev/null

# ---------------------------------------------------------------------------
# Enclosure — PVC split-tube (the documented build) and the earlier wedge box
# ---------------------------------------------------------------------------
echo "==> Enclosure"
mkdir -p enclosure/renders
pushd enclosure >/dev/null

scad() {                        # scad <out> <file> <extra openscad args...>
    local out=$1 file=$2; shift 2
    openscad -o "renders/$out.png" --imgsize=2200,1500 \
        --colorscheme=Tomorrow --render "$@" "$file" >/dev/null 2>&1
}

PVC=stoveiq_pvc_enclosure.scad
scad assembly    "$PVC" -D SHOW_ASSEMBLY=true  -D SHOW_COMPONENTS=true \
                        --camera=340,-300,150,0,0,58
scad sensor-half "$PVC" -D SHOW_ASSEMBLY=false -D SHOW_SENSOR_HALF=true  -D SHOW_ESP32_HALF=false \
                        -D SHOW_COMPONENTS=true --autocenter --viewall --camera=0,0,0,55,0,215,0
scad esp32-half  "$PVC" -D SHOW_ASSEMBLY=false -D SHOW_SENSOR_HALF=false -D SHOW_ESP32_HALF=true \
                        -D SHOW_COMPONENTS=true --autocenter --viewall --camera=0,0,0,125,0,215,0
scad bracket     "$PVC" -D SHOW_ASSEMBLY=false -D SHOW_SENSOR_HALF=false -D SHOW_BRACKET=true \
                        --autocenter --viewall --camera=0,0,0,60,0,25,0
scad end-cap     "$PVC" -D SHOW_ASSEMBLY=false -D SHOW_SENSOR_HALF=false -D SHOW_END_CAP=true \
                        --autocenter --viewall --camera=0,0,0,60,0,25,0

WEDGE=stoveiq_enclosure.scad
scad wedge-iso       "$WEDGE" --autocenter --viewall --camera=0,0,0,58,0,35,0
scad wedge-side      "$WEDGE" --autocenter --viewall --camera=0,0,0,90,0,0,0
scad wedge-underside "$WEDGE" --autocenter --viewall --camera=0,0,0,125,0,30,0

popd >/dev/null

echo "==> done — see pcb/renders/ and enclosure/renders/"
