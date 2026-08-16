# UI screenshot harness

Runs the StoveIQ web UI on your desktop, without an ESP32 and without a stove,
so the screenshots in [`docs/images/`](../../docs/images/) can be regenerated
whenever the UI changes.

**The UI is real. The thermal data is not.** Every pixel of interface comes
straight out of `firmware/src/web_server.c`; the temperatures behind it are
synthesised by `server.py`. Nothing here runs on the device or ships in the
firmware binary.

## Why this exists

The web UI is embedded in the firmware as a C string literal, and the native
emulator build (`pio run -e emulator`) deliberately excludes `web_server.c` —
so there is no way to see the interface without flashing hardware and standing
at a hot stove. This harness closes that gap.

## Use

```bash
cd tools/ui-screenshots
pip install aiohttp

python3 extract.py          # web_server.c  ->  index.html
python3 server.py           # serve on http://127.0.0.1:8770
python3 server.py --recipe  # ...with the recipe coaching card active
```

Open <http://127.0.0.1:8770> in a browser at a phone-sized viewport (the UI is
capped at 500 px wide). A 440 × 660 viewport is what the committed screenshots
use.

## How it works

`extract.py` walks the `FALLBACK_HTML[]` literal chain in `web_server.c`,
strips the C comments between the fragments, and un-escapes the string literals
back into a single `index.html`. Re-run it after any UI edit.

`server.py` serves that file and speaks the firmware's exact WebSocket protocol
on `/ws`:

| Message | Payload |
|---|---|
| Binary | 4-byte little-endian timestamp, then 768 × `int16` little-endian; temperature = value ÷ 10, in °C |
| Text | `{"type":"status","ambient":…,"maxTemp":…,"burners":[…],"alerts":[…],"recipe":{…}}` |

Frames go out at 4 Hz to match the MLX90640; status at 2 Hz. The scene is a
four-burner cooktop viewed from above — a stockpot pinned at boiling, a cast-iron
skillet climbing toward searing temperature, an empty burner, and a saucepan
holding a simmer. Burner states and alert types mirror the enums in
`firmware/include/stoveiq_types.h`.

## Seeding a configured kitchen

Burner names, the cookware library, calibration offsets, and past cook sessions
all live in `localStorage`, not on the device. A fresh browser profile shows an
unconfigured UI. To reproduce the committed screenshots, set these keys before
loading:

| Key | Contents |
|---|---|
| `siq_cal` | `[{r,c,rad,name}]` — burner zones in sensor coordinates |
| `siq_cookware` | `[{id,name,icon,material,notes,created}]` |
| `siq_burner_cookware` | `{burnerId: cookwareId}` |
| `siq_calib_offsets` | `{"<burnerId>_<cookwareId>": offsetC}` |
| `siq_sessions` | `[{id,burner_id,cookware_id,label,started_ms,ended,samples,events}]` |
| `siq_unit` | `"C"` or `"F"` |

`ended` must be consistent with `started_ms` — the session chart derives its time
axis from the difference, and an inconsistent pair renders as
"No samples in this window".
