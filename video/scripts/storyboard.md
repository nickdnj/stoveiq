# Storyboard: I Built a $100 Thermal Cooking Coach (and it actually works)

---

# Chapter 1: The Problem (0:00 - 1:00)
> Hook the viewer by exposing the gap between what cooking apps do (timers) and what they should do (see). Smash cut to the thermal heatmap reveal.

## Scene 1: Cold Open / Hook
- **Duration:** 15 seconds
- **Narration type:** [VO]
- **Image source:** Live footage + screen capture
- **Shot list:**
  1. Close-up of phone showing a generic timer app counting down (5s)
  2. Camera pulls back to reveal a pot on the stove, steam rising, nothing happening (5s)
  3. Quick cut to black (0.5s)
- **Image orientation:** landscape
- **Text overlay:** None
- **Motion:** static (phone screen), gentle pull-back (stove reveal)
- **Audio:** Narration + ambient kitchen sounds, no music yet
- **Transition out:** Hard cut

## Scene 2: The Frustration
- **Duration:** 20 seconds
- **Narration type:** [VO]
- **Image source:** Live footage (film) or stock
- **Shot list:**
  1. Probe thermometer stuck in a steak, single number on display (4s)
  2. Someone checking timer on phone while pot boils over behind them (5s)
  3. Hands juggling probe wire while flipping food (4s)
  4. Wide shot of messy stovetop, multiple burners, no tech helping (7s)
- **Image orientation:** landscape
- **Text overlay:** None
- **Motion:** quick cuts, handheld feel
- **Audio:** Narration, ambient kitchen, slight tension music sting at boilover
- **Transition out:** Smash cut to Scene 3

## Scene 3: The Reveal
- **Duration:** 25 seconds
- **Narration type:** [VO]
- **Image source:** Screen capture (dashboard heatmap) + AI-generated title card
- **Shot list:**
  1. Full-screen thermal heatmap of stove with two burners lit -- hold 3s
  2. Text overlay fades in: "What if your stove could actually SEE what you're cooking?" (4s)
  3. Dashboard UI fades in over heatmap: burner cards, recipe progress, "Rolling boil!" message (8s)
  4. Title card: "I Built a $100 Thermal Cooking Coach" (5s)
- **Image orientation:** landscape
- **Text overlay:** Hook question, then title
- **Motion:** static (heatmap hold), gentle-zoom (dashboard), static (title card)
- **Audio:** Narration. Music fades in on title card -- upbeat maker track
- **Transition out:** Crossfade 1s

---

# Chapter 2: The Idea (1:00 - 2:00)
> Introduce the two core components and land the cost + open-source value proposition. The audience should think: "I could build that."

## Scene 4: The Sensor
- **Duration:** 20 seconds
- **Narration type:** [VO]
- **Image source:** Live footage (product shot of MLX90640 breakout)
- **Shot list:**
  1. Clean close-up of MLX90640 breakout board on white/dark surface (8s)
  2. Slow zoom into the sensor window (gold square) (6s)
  3. Animated overlay: "24x32 IR pixels | 110deg FoV | 4Hz" (6s)
- **Image orientation:** landscape
- **Text overlay:** Sensor specs animated in
- **Motion:** slow zoom, then static for specs overlay
- **Audio:** Narration + background music at 12%
- **Transition out:** Cut

## Scene 5: The Brain
- **Duration:** 20 seconds
- **Narration type:** [VO]
- **Image source:** Live footage (product shot of ESP32-S3 DevKit)
- **Shot list:**
  1. Close-up of ESP32-S3 DevKit board (6s)
  2. Animated arrows pointing to WiFi antenna, USB-C, GPIO pins (8s)
  3. Text: "Sensor + Cooking Engine + Web Server = One Chip" (6s)
- **Image orientation:** landscape
- **Text overlay:** Feature callouts, then summary text
- **Motion:** gentle-zoom with animated overlays
- **Audio:** Narration + background music at 12%
- **Transition out:** Cut

## Scene 6: The Pitch
- **Duration:** 20 seconds
- **Narration type:** [VO]
- **Image source:** Live footage (both boards together) + graphic overlay
- **Shot list:**
  1. Both boards side by side on surface (5s)
  2. Animated price breakdown: "$75 sensor + $16 ESP32 + $4 wires = $95" (5s)
  3. Price slashes to "$50 with Chinese-source modules" (3s)
  4. License badges: "MIT Software | CERN-OHL-S Hardware | Zero Cloud" (7s)
- **Image orientation:** landscape
- **Text overlay:** Price breakdown, license badges
- **Motion:** static with animated overlays
- **Audio:** Narration + background music at 12%
- **Transition out:** Crossfade 1s

---

# Chapter 3: The Build (2:00 - 4:15)
> Core maker content. Show the full build from parts on the table to first thermal image. Emphasis on accessibility -- "if you can plug in a USB cable, you can build this."

## Scene 7: The BOM
- **Duration:** 15 seconds
- **Narration type:** [LIVE]
- **Image source:** Live footage (overhead workbench)
- **Shot list:**
  1. Overhead shot: all parts laid out on workbench (8s)
  2. Hands picking up each part briefly (7s)
- **Image orientation:** landscape
- **Text overlay:** Part names + Adafruit PIDs as items are picked up
- **Motion:** overhead static, handheld when picking up parts
- **Audio:** Live audio + background music at 10%
- **Transition out:** Cut

## Scene 8: Wiring
- **Duration:** 45 seconds
- **Narration type:** [LIVE]
- **Image source:** Live footage (overhead close-up of wiring)
- **Shot list:**
  1. Close-up of empty breadboard with both boards placed (5s)
  2. Connecting wire 1: VIN to 3V3 (8s)
  3. Connecting wire 2: GND to GND (6s)
  4. Connecting wire 3: SDA to GPIO 1 (8s)
  5. Connecting wire 4: SCL to GPIO 2 (8s)
  6. Pull back to show completed wiring -- hold for screenshot (10s)
- **Image orientation:** landscape
- **Text overlay:** Wiring diagram graphic overlay during connections
- **Motion:** overhead static, slow deliberate movements
- **Audio:** Live audio + background music at 10%
- **Transition out:** Cut

## Scene 9: Flash Firmware
- **Duration:** 25 seconds
- **Narration type:** [VO]
- **Image source:** Screen capture (terminal)
- **Shot list:**
  1. Terminal: `git clone` command (4s)
  2. Terminal: `cd firmware && pio run -t upload` (6s)
  3. Compile output scrolling (sped up 4x) (8s)
  4. Upload complete, device reboots (4s)
  5. Brief shot of serial monitor showing boot messages (3s)
- **Image orientation:** landscape
- **Text overlay:** Command text highlighted/enlarged
- **Motion:** static (screen capture)
- **Audio:** Narration + background music at 12%
- **Transition out:** Cut

## Scene 10: BLE Provisioning
- **Duration:** 25 seconds
- **Narration type:** [LIVE]
- **Image source:** Phone screen recording + live footage
- **Shot list:**
  1. Phone showing ESP BLE Prov app -- scanning (5s)
  2. Connecting to "StoveIQ" device (3s)
  3. Entering PoP: stoveiq-setup (5s)
  4. WiFi network selection (4s)
  5. "Connected!" confirmation (3s)
  6. Brief cut to phone browser opening stoveiq.local (5s)
- **Image orientation:** portrait (phone recording) -- will need pillarbox or picture-in-picture
- **Text overlay:** PoP code "stoveiq-setup" highlighted
- **Motion:** pillarbox for phone recording, or PIP over workbench shot
- **Audio:** Live audio + background music at 10%
- **Transition out:** Cut

## Scene 11: First Light -- The Money Shot
- **Duration:** 15 seconds
- **Narration type:** [LIVE]
- **Image source:** Live footage (phone/laptop showing dashboard + stove)
- **Shot list:**
  1. Dashboard loads -- heatmap appears showing room-temperature stove (3s)
  2. Hand reaches to stove, turns on a burner (3s)
  3. Heat bloom appears on the heatmap in real time (5s) -- HOLD THIS SHOT
  4. Reaction shot (4s)
- **Image orientation:** landscape
- **Text overlay:** None -- let the visual speak
- **Motion:** static/handheld
- **Audio:** Live audio, genuine reaction, music dips slightly for the reveal
- **Transition out:** Cut

## Scene 12: Enclosure
- **Duration:** 10 seconds
- **Narration type:** [LIVE]
- **Image source:** Live footage (quick build montage)
- **Shot list:**
  1. PVC pipe cut in half (2s)
  2. Hole drilled for sensor (2s)
  3. Boards placed inside (2s)
  4. Halves snapped together (2s)
  5. Mounted under cabinet pointing at stove (2s)
- **Image orientation:** landscape
- **Text overlay:** None
- **Motion:** quick cuts, montage pace
- **Audio:** Live audio + music slightly louder for montage energy
- **Transition out:** Crossfade 1s

---

# Chapter 4: The Cooking Coach (4:15 - 6:30)
> This is the proof. Live cooking demo showing the thermal-aware coaching system working in a real kitchen. Split attention between the phone dashboard and the actual stove.

## Scene 13: Dashboard Tour
- **Duration:** 30 seconds
- **Narration type:** [LIVE]
- **Image source:** Live footage (phone on counter + stove in background)
- **Shot list:**
  1. Wide shot: phone propped on counter, stove visible behind (5s)
  2. Close-up of phone: heatmap at top of dashboard (8s)
  3. Close-up of phone: burner cards below showing temps (8s)
  4. Tap settings gear: show C/F toggle, simulation mode (5s)
  5. Pull back to wide shot (4s)
- **Image orientation:** landscape (wide), portrait phone inserts via PIP
- **Text overlay:** UI element labels if needed for clarity
- **Motion:** mix of static wide and handheld close-ups
- **Audio:** Live audio + background music at 10%
- **Transition out:** Cut

## Scene 14: Burner Calibration
- **Duration:** 30 seconds
- **Narration type:** [LIVE]
- **Image source:** Phone screen recording + live footage
- **Shot list:**
  1. Tap gear icon, tap "Calibrate Burners" (3s)
  2. Heatmap in calibration mode -- tap to place first burner zone (5s)
  3. Drag circle to position over burner (4s)
  4. +/- buttons to resize (3s)
  5. Repeat quickly for remaining burners (8s)
  6. All four burners calibrated -- dashboard shows labeled burner cards (7s)
- **Image orientation:** portrait (phone recording) via PIP over kitchen wide shot
- **Text overlay:** "Calibrate once. Cook forever." at end
- **Motion:** pillarbox/PIP for phone, static for kitchen
- **Audio:** Live audio + background music at 10%
- **Transition out:** Cut

## Scene 15: Live Recipe Demo
- **Duration:** 55 seconds
- **Narration type:** [LIVE]
- **Image source:** Live footage (split view: phone dashboard + actual stove)
- **Shot list:**
  1. Tap Recipes on dashboard, tap Pasta (5s)
  2. Step 1 active: "Fill pot with water, set to high" -- water going into pot (8s)
  3. Dashboard: temperature climbing on burner card (6s)
  4. Step 2: "Waiting for rolling boil..." -- pot starting to bubble (8s)
  5. Dashboard: boil detected! Coaching message: "Rolling boil!" with chime (5s)
  6. Reaction: "It knew before I did. I was in the other room." (4s)
  7. Step 3: "Add pasta and stir" -- pasta going in, tap Confirm (6s)
  8. Step 4: Timer running, progress bar filling (5s)
  9. Timer complete: "Check -- al dente?" (4s)
  10. Drain and serve -- quick montage (4s)
- **Image orientation:** landscape (split screen or alternating)
- **Text overlay:** Recipe step name in corner during each step
- **Motion:** handheld, documentary feel, genuine cooking
- **Audio:** Live audio (sizzling, water, chime sounds), music at 8%
- **Transition out:** Cut

## Scene 16: Multiple Burners
- **Duration:** 10 seconds
- **Narration type:** [LIVE]
- **Image source:** Live footage (dashboard showing multiple active burners)
- **Shot list:**
  1. Dashboard showing 2-3 burners active with independent temps (5s)
  2. Quick pan across actual stove with multiple pots/pans (5s)
- **Image orientation:** landscape
- **Text overlay:** None
- **Motion:** static dashboard, handheld pan across stove
- **Audio:** Live audio + background music at 10%
- **Transition out:** Cut

## Scene 17: The Comparison
- **Duration:** 10 seconds
- **Narration type:** [VO]
- **Image source:** Screen capture (side-by-side comparison graphic)
- **Shot list:**
  1. Split screen: LEFT = generic timer "8:00" counting down. RIGHT = StoveIQ dashboard with heatmap, burner cards, recipe progress, "Rolling boil!" message (10s)
- **Image orientation:** landscape
- **Text overlay:** LEFT: "Timer App" / RIGHT: "StoveIQ"
- **Motion:** static
- **Audio:** Narration + background music at 12%
- **Transition out:** Crossfade 1s

---

# Chapter 5: The Recipe System (6:30 - 8:00)
> Pull back the curtain on how recipes work. Make the audience want to contribute their own.

## Scene 18: How Recipes Work
- **Duration:** 40 seconds
- **Narration type:** [VO]
- **Image source:** Screen capture (VS Code + animated diagram)
- **Shot list:**
  1. VS Code showing pasta.json with syntax highlighting (10s)
  2. Animated callouts highlighting: "desc", "trigger", "coach_msg" fields (10s)
  3. Animated flow diagram: Step 1 (target 50C) -> Step 2 (boil) -> Step 3 (confirm) -> Step 4 (timer 8min) (10s)
  4. Quick cut to seared-steak.json -- highlight "PAN IS SCREAMING HOT!" and "FLIP NOW!" coach messages (10s)
- **Image orientation:** landscape
- **Text overlay:** Field labels as callouts
- **Motion:** static code, animated overlays
- **Audio:** Narration + background music at 12%
- **Transition out:** Cut

## Scene 19: The Recipe Library
- **Duration:** 20 seconds
- **Narration type:** [VO]
- **Image source:** Screen capture (GitHub)
- **Shot list:**
  1. GitHub repo /recipes directory listing (5s)
  2. Click into /basics -- show 4 recipe files (4s)
  3. Click into /proteins -- show seared-steak.json (3s)
  4. PR template shown briefly (4s)
  5. Quick shot of /community folder (empty -- "yours goes here") (4s)
- **Image orientation:** landscape
- **Text overlay:** "Fork. Write JSON. Submit PR."
- **Motion:** static (screen capture with cursor movement)
- **Audio:** Narration + background music at 12%
- **Transition out:** Cut

## Scene 20: Simulation Mode
- **Duration:** 20 seconds
- **Narration type:** [LIVE]
- **Image source:** Phone screen recording + live footage
- **Shot list:**
  1. Dashboard settings: toggle Simulation Mode on (4s)
  2. Temperature slider appears -- drag it up (4s)
  3. Recipe steps advancing as virtual temp hits triggers (8s)
  4. "Boil detected!" in simulation -- no actual cooking (4s)
- **Image orientation:** landscape or PIP
- **Text overlay:** "Test recipes without cooking"
- **Motion:** static/screen capture
- **Audio:** Live audio explaining + background music at 10%
- **Transition out:** Cut

## Scene 21: Recipe JSON Close-Up
- **Duration:** 10 seconds
- **Narration type:** [VO]
- **Image source:** Screen capture (split screen)
- **Shot list:**
  1. LEFT: JSON recipe file. RIGHT: Dashboard running that recipe. As each step activates in the dashboard, the corresponding JSON step highlights on the left. (10s)
- **Image orientation:** landscape
- **Text overlay:** "Five fields. One recipe. Fork the repo."
- **Motion:** static with highlight animations
- **Audio:** Narration + background music at 12%
- **Transition out:** Crossfade 1s

---

# Chapter 6: What's Next + CTA (8:00 - 9:00)
> Point to resources, tease the roadmap, issue a direct call to action.

## Scene 22: Resources
- **Duration:** 25 seconds
- **Narration type:** [VO]
- **Image source:** Screen capture + AI-generated QR graphics
- **Shot list:**
  1. Hackaday.io project page (5s)
  2. GitHub repo main page with star count visible (5s)
  3. Recipes directory (3s)
  4. QR codes for both links overlaid (7s)
  5. Description text: "Links in the description" (5s)
- **Image orientation:** landscape
- **Text overlay:** URLs + QR codes
- **Motion:** static (screen captures)
- **Audio:** Narration + background music at 12%
- **Transition out:** Cut

## Scene 23: What's Coming
- **Duration:** 20 seconds
- **Narration type:** [VO]
- **Image source:** Screen capture (KiCad) + AI-generated PCB render
- **Shot list:**
  1. KiCad PCB layout or 3D render of the custom board (8s)
  2. Text: "No more breadboard." (3s)
  3. GitHub Issues page showing planned features (5s)
  4. Text: "100 community recipes by end of 2026" (4s)
- **Image orientation:** landscape
- **Text overlay:** Feature teasers
- **Motion:** gentle-zoom on PCB render, static for GitHub
- **Audio:** Narration + background music at 12%
- **Transition out:** Cut

## Scene 24: Call to Action / End Card
- **Duration:** 15 seconds
- **Narration type:** [LIVE]
- **Image source:** Live footage (on-camera, holding device)
- **Shot list:**
  1. Direct to camera, holding the assembled device (10s)
  2. End card with subscribe button, GitHub link, Hackaday link (5s)
- **Image orientation:** landscape
- **Text overlay:** End card elements -- subscribe, GitHub star, Hackaday.io
- **Motion:** static (on-camera), static (end card)
- **Audio:** Live audio, music fade out at 8:55
- **Transition out:** Fade to black

---

# Asset Summary

## By Source Type

| Source Type | Count | Notes |
|-------------|-------|-------|
| Live footage (film) | 14 scenes | Workbench, cooking demo, on-camera |
| Screen capture (record) | 5 scenes | Terminal, GitHub, VS Code, dashboard |
| AI-generated graphics | 4 assets | Title card, QR graphic, PCB render, comparison graphic |
| Title card | 1 asset | Video title at 0:50 |
| **Total unique scenes** | **24** | |

## Graphics/Overlays Needed

1. Wiring diagram overlay (Scene 8)
2. Price breakdown animation (Scene 6)
3. License badge graphic (Scene 6)
4. Sensor specs overlay (Scene 4)
5. ESP32 feature callout arrows (Scene 5)
6. Recipe flow diagram animation (Scene 18)
7. Side-by-side comparison graphic (Scene 17)
8. QR codes for GitHub + Hackaday (Scene 22)
9. End card template (Scene 24)

## Screen Captures Needed

1. Generic timer app (Scene 1)
2. PlatformIO terminal -- build + upload (Scene 9)
3. ESP BLE Prov app -- provisioning flow (Scene 10)
4. VS Code -- pasta.json and seared-steak.json (Scene 18)
5. GitHub -- /recipes directory, PR template (Scene 19)
6. Dashboard -- simulation mode (Scene 20)
7. Dashboard -- recipe running with JSON side-by-side (Scene 21)
8. Hackaday.io project page (Scene 22)
9. GitHub repo main page (Scene 22)
10. KiCad PCB layout or 3D render (Scene 23)

## Live Footage Shot List

1. Phone showing timer app + pot on stove (Scene 1)
2. Probe thermometer in steak (Scene 2)
3. Boilover moment (Scene 2)
4. Parts laid out on workbench (Scene 7)
5. Breadboard wiring -- 4 connections (Scene 8)
6. Phone BLE provisioning (Scene 10)
7. First thermal image + burner turn-on (Scene 11)
8. PVC pipe enclosure build montage (Scene 12)
9. Dashboard tour on phone (Scene 13)
10. Burner calibration on phone (Scene 14)
11. Full pasta cooking demo with dashboard visible (Scene 15)
12. Multiple burners active (Scene 16)
13. Simulation mode demo (Scene 20)
14. On-camera CTA, holding device (Scene 24)
