# Screenshots

The StoveIQ web interface, captured in Chrome at a 440 × 660 viewport.

**These are the real UI, driven by synthetic thermal data.** Every element is
served from the HTML embedded in `firmware/src/web_server.c` — nothing was
mocked up, redrawn, or retouched. The temperatures behind it come from
[`tools/ui-screenshots/`](../../tools/ui-screenshots/), which replays a
plausible four-burner cooktop over the firmware's own WebSocket protocol. The
cookware library and the cook session are seeded fixtures.

No photograph in this repository shows the physical device. The stills under
`video/assets/` are AI-generated illustrations from an unproduced video draft
and are not hardware documentation.

| File | Shows |
|---|---|
| `ui-dashboard.png` | Four burner cards with calibrated names, cookware, live temperatures and state |
| `ui-recipe.png` | Recipe coaching card — "Seared Steak" step 4, progress toward the 230 °C target |
| `ui-calibration.png` | The thermal heatmap with burner zones overlaid, as used to place them |
| `ui-session.png` | A completed cook replayed as an annotated temperature curve |
| `ui-cookware.png` | The cookware library, with emissivity class per item |
| `ui-settings.png` | Alert thresholds and sensor calibration |

## Regenerating

```bash
cd tools/ui-screenshots
python3 extract.py
python3 server.py --recipe
```

Then seed `localStorage` as described in that directory's README, size the
viewport to 440 × 660, and capture. See
[`tools/ui-screenshots/README.md`](../../tools/ui-screenshots/README.md).
