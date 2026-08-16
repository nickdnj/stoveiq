# StoveIQ Hardware

Everything mechanical and electrical, designed end-to-end in free and
open-source tools. No licence, no seat, no cloud account — clone the repo and
open the files.

| Directory | What | Tool | Status |
|---|---|---|---|
| [`pcb/`](pcb/) | Custom ESP32-S3 + MLX90640 board, 45 × 35 mm | KiCad 10 | **Placement study** — no MCU, unrouted, 58 DRC violations |
| [`enclosure/`](enclosure/) | PVC split-tube housing + cabinet bracket | OpenSCAD | **Built** — this is what is mounted over the stove |
| [`enclosure/`](enclosure/) | Wedge box for the custom board | OpenSCAD | Modelled only |

The honest summary: **the enclosure is real and the board is not.** The device
in daily use is an ESP32-S3 devkit and an MLX90640 breakout wired together and
zip-tied inside a length of PVC pipe. The custom PCB was drawn to replace them
and never finished.

---

## The toolchain

| Tool | Licence | Used for |
|---|---|---|
| [KiCad](https://www.kicad.org/) 10 | GPL-3.0 | Schematic capture, PCB layout, 3D raytracing, DRC, fab output |
| [OpenSCAD](https://openscad.org/) 2021.01 | GPL-2.0 | Parametric enclosure modelling and rendering |
| [FreeCAD](https://www.freecad.org/) | LGPL-2.1 | Alternative enclosure macro (see `enclosure/`) |
| [Freerouting](https://freerouting.org/) | AGPL-3.0 | Autorouting attempt (`pcb/stoveiq.dsn` / `.ses`) |
| [librsvg](https://gitlab.gnome.org/GNOME/librsvg) | LGPL-2.1 | SVG → PNG for the images on GitHub |
| [PlatformIO](https://platformio.org/) + [ESP-IDF](https://github.com/espressif/esp-idf) | Apache-2.0 | Firmware build (see `../firmware/`) |

Every image in this repository is generated from source by
[`render.sh`](render.sh) — no screenshots taken by hand, nothing drawn in a
proprietary tool.

```bash
# macOS
brew install kicad openscad librsvg

# Debian / Ubuntu
apt install kicad openscad librsvg2-bin

# Then, from the repo root
hardware/render.sh
```

Outputs land in `pcb/renders/` and `enclosure/renders/` and are committed, so
reading the GitHub page never requires installing anything.

---

## Where to start

- **Building one?** You want the devkit parts list in the
  [root README](../README.md#build-your-own) and the
  [enclosure build guide](../docs/enclosure-build.md).
- **Looking at the board?** [`pcb/README.md`](pcb/README.md) — full BOM,
  schematic, layout plots, and a frank list of what is wrong with it.
- **Printing a housing?** [`enclosure/README.md`](enclosure/README.md) —
  dimensions, print settings, STL export commands.

## Licence

Hardware is [CERN-OHL-S-2.0](../LICENSE-HARDWARE). Firmware is
[MIT](../LICENSE-SOFTWARE).
