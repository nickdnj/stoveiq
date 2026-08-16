#!/usr/bin/env python3
"""
StoveIQ web UI screenshot harness.

Serves the *real* UI extracted verbatim from firmware/src/web_server.c and feeds
it synthetic thermal data over a WebSocket that speaks the exact wire protocol
the firmware speaks:

  binary : 4-byte LE timestamp + 768 x int16 LE, temperature = value / 10.0 C
  text   : {"type":"status","ambient":..,"maxTemp":..,"burners":[..],"alerts":[..]}

Frame geometry is 32 columns x 24 rows (MLX90640), row-major.
This exists only to produce documentation screenshots. It is not part of the
firmware and never runs on the device.
"""

import asyncio
import json
import math
import random
import struct
import time
from pathlib import Path

from aiohttp import web, WSMsgType

HERE = Path(__file__).parent
FIRMWARE = HERE.resolve().parents[1] / "firmware"

COLS, ROWS = 32, 24
NPIX = COLS * ROWS
AMBIENT = 23.0

# Burner state enum from include/stoveiq_types.h
OFF, HEATING, STABLE, COOLING = 0, 1, 2, 3
# Alert type enum from include/stoveiq_types.h
ALERT_BOIL, ALERT_SMOKE, ALERT_PREHEAT, ALERT_FORGOTTEN, ALERT_FAULT = 0, 1, 2, 3, 4

# Set by --recipe on the command line; drives the coaching card.
SHOW_RECIPE = "--recipe" in __import__("sys").argv


class Burner:
    """One hot zone in the scene, and the burner record derived from it."""

    def __init__(self, bid, row, col, radius, temp, state, rate=0.0):
        self.id = bid
        self.row = row
        self.col = col
        self.radius = radius
        self.temp = temp
        self.state = state
        self.rate = rate
        self.on_since = time.time()

    def step(self, dt):
        """Advance this burner's temperature a little, so the UI looks live."""
        if self.state == HEATING:
            self.temp = min(self.temp + self.rate * dt, 235.0)
            if self.temp >= 232.0:
                self.state = STABLE
                self.rate = 0.0
        elif self.state == STABLE:
            self.temp += math.sin(time.time() * 0.7 + self.id) * 0.12
        elif self.state == COOLING:
            self.temp = max(self.temp - abs(self.rate) * dt, AMBIENT + 2)

    @property
    def pixel_count(self):
        return 0 if self.state == OFF else int(math.pi * self.radius ** 2)


def build_scene():
    """A four-burner cooktop mid-cook, seen from above."""
    return [
        # rear-left: stockpot at a rolling boil, pinned at water's boiling point
        Burner(0, row=7, col=9, radius=4.2, temp=99.6, state=STABLE),
        # rear-right: cast-iron skillet climbing toward searing temperature
        Burner(1, row=7, col=22, radius=3.6, temp=168.0, state=HEATING, rate=3.1),
        # front-left: empty, burner off
        Burner(2, row=17, col=9, radius=0.0, temp=AMBIENT + 1.4, state=OFF),
        # front-right: saucepan holding a simmer
        Burner(3, row=17, col=22, radius=3.0, temp=91.2, state=STABLE),
    ]


def render_frame(burners, t):
    """Rasterise the scene into 768 floats of degrees C."""
    px = [0.0] * NPIX

    for r in range(ROWS):
        for c in range(COLS):
            # Gentle background gradient — the cooktop surface is a touch warmer
            # in the middle than at the edges, and the sensor sees some of its
            # own housing at the corners.
            dx = (c - COLS / 2) / (COLS / 2)
            dy = (r - ROWS / 2) / (ROWS / 2)
            falloff = 1.0 - 0.25 * (dx * dx + dy * dy)
            px[r * COLS + c] = AMBIENT * falloff + random.gauss(0, 0.18)

    for b in burners:
        if b.state == OFF:
            # Residual warmth only
            peak = b.temp - AMBIENT
            radius = 2.2
        else:
            peak = b.temp - AMBIENT
            radius = b.radius

        if peak <= 0.5:
            continue

        for r in range(ROWS):
            for c in range(COLS):
                d2 = (r - b.row) ** 2 + (c - b.col) ** 2
                # Flat-topped Gaussian: cookware bottoms are close to isothermal
                # in the middle and fall off sharply at the rim.
                g = math.exp(-(d2 ** 1.35) / (2 * radius ** 2.7))
                if g > 0.002:
                    shimmer = 1.0 + 0.012 * math.sin(t * 2.2 + d2 * 0.35 + b.id)
                    px[r * COLS + c] += peak * g * shimmer

    return px


def pack_frame(px, ts_ms):
    buf = bytearray(struct.pack("<I", ts_ms & 0xFFFFFFFF))
    for v in px:
        buf += struct.pack("<h", max(-32768, min(32767, int(round(v * 10.0)))))
    return bytes(buf)


def status_json(burners, px):
    now = time.time()
    alerts = []
    for b in burners:
        if b.state != OFF and abs(b.temp - 100.0) < 2.5:
            alerts.append({"type": ALERT_BOIL, "burner": b.id,
                           "temp": round(b.temp, 1), "active": True})
        if b.temp > 200.0:
            alerts.append({"type": ALERT_SMOKE, "burner": b.id,
                           "temp": round(b.temp, 1), "active": True})

    # Recipe coaching state, mirroring "Seared Steak" step 4 from
    # s_recipes[] in src/cooking_engine.c (target 230 C, TRIGGER_TARGET).
    skillet = burners[1]
    recipe = None
    if SHOW_RECIPE:
        recipe = {
            "idx": 1, "name": "Seared Steak",
            "step": 3, "steps": 7,
            "desc": "Oil heating...", "coach": "PAN IS SCREAMING HOT!",
            "timer": 0, "burner": skillet.id,
            "temp": round(skillet.temp, 1),
            "target": 230.0, "trigger": 3,
        }

    return json.dumps({
        "type": "status",
        "ambient": round(AMBIENT, 1),
        "maxTemp": round(max(px), 1),
        "burners": [{
            "id": b.id,
            "state": b.state,
            "temp": round(b.temp, 1),
            "max": round(b.temp + (3.5 if b.state != OFF else 0.4), 1),
            "rate": round(b.rate if b.state == HEATING else
                          (-abs(b.rate) if b.state == COOLING else 0.0), 2),
            "row": b.row,
            "col": b.col,
            "px": b.pixel_count,
            "on": int((now - b.on_since) * 1000) if b.state != OFF else 0,
        } for b in burners],
        "alerts": alerts,
        **({"recipe": recipe} if recipe else {}),
    })


async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("[ws] client connected")

    burners = build_scene()
    t0 = time.time()
    last = t0
    tick = 0

    async def drain():
        # The UI sends calibration and silence_alert commands; consume them.
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                print(f"[ws] <- {msg.data[:120]}")
            elif msg.type in (WSMsgType.CLOSE, WSMsgType.ERROR):
                break

    reader = asyncio.create_task(drain())

    try:
        while not ws.closed:
            now = time.time()
            dt, last = now - last, now
            for b in burners:
                b.step(dt)

            px = render_frame(burners, now - t0)
            await ws.send_bytes(pack_frame(px, int((now - t0) * 1000)))

            # Status at half the frame rate, like the firmware's cadence
            if tick % 2 == 0:
                await ws.send_str(status_json(burners, px))

            tick += 1
            await asyncio.sleep(0.25)   # 4 Hz, matching the MLX90640
    except (ConnectionResetError, asyncio.CancelledError):
        pass
    finally:
        reader.cancel()
        print("[ws] client gone")

    return ws


async def index(request):
    return web.FileResponse(HERE / "index.html")


async def icon(request):
    p = FIRMWARE / "stoveiq-icon-1024.png"
    if p.exists():
        return web.FileResponse(p)
    raise web.HTTPNotFound()


async def manifest(request):
    return web.json_response({
        "name": "StoveIQ", "short_name": "StoveIQ",
        "start_url": "/", "display": "standalone",
        "background_color": "#111", "theme_color": "#111",
        "icons": [{"src": "/icon.png", "sizes": "1024x1024", "type": "image/png"}],
    })


async def sw(request):
    return web.Response(text="/* screenshot harness: no-op */",
                        content_type="application/javascript")


async def api_stub(request):
    return web.json_response({"ok": True})


def main():
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", ws_handler)
    app.router.add_get("/icon.png", icon)
    app.router.add_get("/manifest.json", manifest)
    app.router.add_get("/sw.js", sw)
    app.router.add_route("*", "/api/{tail:.*}", api_stub)
    web.run_app(app, host="127.0.0.1", port=8770, print=None)


if __name__ == "__main__":
    main()
