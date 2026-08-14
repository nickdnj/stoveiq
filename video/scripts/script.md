# Video Script: I Built a $100 Thermal Cooking Coach (and it actually works)

**Channel:** Vistter
**Target Runtime:** ~9 minutes (~1,350 words at 150 WPM)
**Narration Style:** [VO] = pre-recorded voiceover, [LIVE] = on-camera with talking points

---

# Chapter 1: The Problem (0:00 - 1:00)

## [SCENE 1: Cold Open / Hook - 0:00-0:15] [VO]

[VISUAL: Close-up of a phone showing a generic cooking timer app counting down. Camera pulls back to show a pot on a stove, steam rising, nothing interesting happening.]

NARRATION:
"Every cooking app on the planet is just a dumb timer. You tap start, you wait, it beeps. That's it. That's the whole thing."

[TRANSITION: Hard cut]

---

## [SCENE 2: The Frustration - 0:15-0:35] [VO]

[VISUAL: Quick montage -- (A) probe thermometer stuck in a steak, showing one number. (B) Someone checking a timer on their phone while something boils over on the stove behind them. (C) Hands awkwardly juggling a probe wire while trying to flip food.]

NARRATION:
"Probe thermometers? Great -- you get one temperature, in one dish, at one point. Meanwhile your other burner is about to smoke because you forgot about it. There's nothing watching the whole stove. Nobody's built that. Until now."

[TRANSITION: Smash cut to thermal heatmap]

---

## [SCENE 3: The Reveal - 0:35-1:00] [VO]

[VISUAL: Full-screen thermal heatmap of a real stove with two burners lit. Bright heat zones glow against the cool background. Hold for two seconds, then overlay the text.]

[TEXT OVERLAY: "What if your stove could actually SEE what you're cooking?"]

NARRATION:
"What if your stove could actually see what you're cooking? Not a timer. Not a probe. A thermal camera that watches your entire cooktop and coaches you through every step."

[VISUAL: Dashboard UI fades in over the heatmap -- burner cards showing temperatures, a recipe progress bar, a coaching message that says "Rolling boil!"]

"I built one. It cost me a hundred bucks. And it actually works."

[TEXT OVERLAY: Title card -- "I Built a $100 Thermal Cooking Coach"]
[MUSIC: Upbeat maker-style track fades in]

[TRANSITION: Crossfade, 1s]

---

# Chapter 2: The Idea (1:00 - 2:00)

## [SCENE 4: The Sensor - 1:00-1:20] [VO]

[VISUAL: Close-up of the MLX90640 breakout board on a white surface. Slow zoom in on the sensor window.]

NARRATION:
"This is the MLX90640. It's a twenty-four by thirty-two pixel infrared thermal array with a hundred-and-ten-degree field of view. Seven hundred and sixty-eight pixels of heat data, four times per second. It sees temperature, not light."

[TRANSITION: Cut]

---

## [SCENE 5: The Brain - 1:20-1:40] [VO]

[VISUAL: Close-up of the ESP32-S3 DevKit board. Animated arrows pointing to key features: WiFi antenna, USB-C, GPIO pins.]

NARRATION:
"And this is the brain -- an ESP32-S3. WiFi, Bluetooth, dual-core processor. It reads the sensor, runs the cooking engine, and serves a full web dashboard. No phone app needed. No cloud. You just open a browser."

[TRANSITION: Cut]

---

## [SCENE 6: The Pitch - 1:40-2:00] [VO]

[VISUAL: Both boards side by side. Animated price tags appear: "$75" over the sensor, "$16" over the ESP32, "$4" for wires and cable. Total: "$95" -- then slashes to "$50" with text "Chinese source modules from $25"]

NARRATION:
"Two boards. Four wires. About a hundred bucks from Adafruit. You can get it cheaper if you source the sensor module directly from AliExpress, but I paid full price and it was worth every penny. Open source -- MIT for the software, CERN Open Hardware for the board files. No cloud, no subscription, no app store. Forever."

[TEXT OVERLAY: "MIT Software | CERN-OHL-S Hardware | Zero Cloud"]

[TRANSITION: Crossfade, 1s]

---

# Chapter 3: The Build (2:00 - 4:15)

## [SCENE 7: The BOM - 2:00-2:15] [LIVE]

[VISUAL: Overhead shot of parts laid out on workbench: ESP32-S3 DevKit, MLX90640 breakout, 4 jumper wires, USB-C cable.]

TALKING POINTS:
- "Here's everything you need. Two boards, four jumper wires, a USB cable. That's the whole BOM."
- Hold up each part briefly
- Mention Adafruit part numbers (PID 5312, PID 4469)

[TRANSITION: Cut]

---

## [SCENE 8: Wiring - 2:15-3:00] [LIVE]

[VISUAL: Close-up overhead of breadboard. Hands connecting the four wires one at a time.]

TALKING POINTS:
- "Four wires. That's it."
- Walk through each connection: "VIN to three-point-three volts. Ground to ground. SDA to GPIO one. SCL to GPIO two."
- Show the completed wiring -- clean shot, pause so viewers can screenshot
- "If you can plug in a USB cable, you can build this."

[TEXT OVERLAY: Wiring diagram graphic overlay during the connections:
  ESP32-S3 --> MLX90640
  3V3 --> VIN
  GND --> GND
  GPIO 1 --> SDA
  GPIO 2 --> SCL]

[TRANSITION: Cut]

---

## [SCENE 9: Flash Firmware - 3:00-3:25] [VO + Screen Capture]

[VISUAL: Terminal screen capture showing PlatformIO build and upload.]

NARRATION:
"Firmware is built on ESP-IDF five-point-five with FreeRTOS. You flash it with PlatformIO -- clone the repo, cd into firmware, pio run dash-t upload. It compiles, it flashes, done."

[VISUAL: Terminal shows successful upload, device reboots]

"The device boots into AP mode -- it creates its own WiFi network called StoveIQ. Connect to that and open one-nine-two dot one-six-eight dot four dot one."

[TRANSITION: Cut]

---

## [SCENE 10: BLE Provisioning - 3:25-3:50] [LIVE + Screen Capture]

[VISUAL: Phone screen recording of the ESP BLE Prov app. Show scanning, connecting, entering PoP, selecting WiFi network.]

TALKING POINTS:
- "To get it on your home WiFi, use the ESP BLE Provisioning app."
- "Scan, connect to StoveIQ, enter the proof-of-possession code: stoveiq dash setup."
- "Pick your WiFi network, enter the password, and it connects."
- Show the dashboard now accessible at stoveiq.local

[TRANSITION: Cut]

---

## [SCENE 11: First Light - The Money Shot - 3:50-4:05] [LIVE]

[VISUAL: Phone or laptop browser showing the StoveIQ dashboard for the first time. Thermal heatmap is live, showing the stove surface. User turns on a burner -- the heatmap blooms with color in real time.]

TALKING POINTS:
- This is the moment. Let it breathe.
- "There it is. Real-time thermal imaging of my stove. From two boards and four wires."
- Turn on a burner while the camera is rolling -- show the heat appear live
- Genuine reaction encouraged

[TRANSITION: Cut]

---

## [SCENE 12: Enclosure - 4:05-4:15] [LIVE]

[VISUAL: Quick montage of PVC pipe enclosure build: (A) pipe cut in half, (B) hole drilled for sensor, (C) boards placed inside, (D) halves snapped together, (E) mounted under cabinet angled at stove.]

TALKING POINTS:
- "Enclosure is a dollar fifty of PVC pipe. Split it, drill a window for the sensor, snap it together."
- "Mount it under the cabinet with adhesive. Angle it down at the stove."
- "There are 3D-printable STLs in the repo too, but honestly, PVC works great."

[TRANSITION: Crossfade, 1s]

---

# Chapter 4: The Cooking Coach (4:15 - 6:30)

## [SCENE 13: Dashboard Tour - 4:15-4:45] [LIVE]

[VISUAL: Phone propped on counter showing the dashboard. Camera alternates between the phone screen and the actual stove.]

TALKING POINTS:
- "Open stoveiq dot local on your phone. This is the cooking coach."
- Walk through the UI: heatmap at the top, burner cards below showing per-burner temps
- Show the settings gear icon -- C/F toggle, simulation mode
- "Everything runs on the ESP32. No server, no cloud, no internet required."

[TRANSITION: Cut]

---

## [SCENE 14: Burner Calibration - 4:45-5:15] [LIVE]

[VISUAL: Phone screen showing calibration mode. User taps on heatmap to place burner zones, drags to position, uses +/- buttons to resize circles.]

TALKING POINTS:
- "First thing you do is calibrate your burners. Tap the gear, tap Calibrate."
- "Tap on the heatmap where each burner is. Drag to position. Plus and minus to resize."
- "It saves to the device -- you only do this once."
- Show all four burners calibrated -- the dashboard now labels them Burner 1, 2, 3, 4

[TRANSITION: Cut]

---

## [SCENE 15: Live Recipe Demo - 5:15-6:10] [LIVE]

[VISUAL: Full cooking sequence with the dashboard visible. This is the centerpiece demo. Phone on counter, pot on stove, camera captures both.]

TALKING POINTS:
- "Let's cook pasta. Tap Recipes, tap Pasta."
- Show step 1: "Fill pot with water, set to high" -- coaching message says "Heating up..."
- Show the temperature climbing on the burner card in real time
- Step 2: "Waiting for rolling boil..." -- the thermal camera detects boil at ~100C
- Coaching message: "Rolling boil!" with an audio chime
- "It knew my water was boiling before I did. I was in the other room."
- Step 3: "Add pasta and stir" -- tap Confirm
- Step 4: Timer starts -- 8 minutes, progress bar filling
- Show coaching message: "Check -- al dente?"
- "That's it. Every step told me what was happening on the stove. Not a guess. Not a timer. The camera SAW the boil."

[TRANSITION: Cut]

---

## [SCENE 16: Multiple Burners - 6:10-6:20] [LIVE]

[VISUAL: Dashboard showing two or three active burners simultaneously, each with independent temperature tracking.]

TALKING POINTS:
- "And it tracks all four burners independently. Two pots going? No problem."
- "Each burner has its own temperature, state, and trend."

[TRANSITION: Cut]

---

## [SCENE 17: The Comparison - 6:20-6:30] [VO]

[VISUAL: Side-by-side split screen. Left: generic timer app showing "8:00" counting down. Right: StoveIQ dashboard showing thermal heatmap, burner cards with live temps, recipe progress bar, coaching message "Rolling boil!"]

NARRATION:
"This is what a timer app shows you. And this is what StoveIQ shows you. One is guessing. The other one is watching."

[TRANSITION: Crossfade, 1s]

---

# Chapter 5: The Recipe System (6:30 - 8:00)

## [SCENE 18: How Recipes Work - 6:30-7:10] [VO + Screen Capture]

[VISUAL: Code editor (VS Code) showing the pasta recipe JSON file. Animated callouts highlight key fields as they're mentioned.]

NARRATION:
"Recipes are JSON state machines. Each step has a description, a trigger, and a coaching message. The triggers are thermal -- boil means the camera detected a rolling boil at a hundred degrees. Target means the burner hit a specific temperature. Food-drop means a sudden temperature drop when you put cold food in a hot pan."

[VISUAL: Animated diagram showing the step flow: Step 1 (target 50C) --> Step 2 (boil) --> Step 3 (confirm) --> Step 4 (timer 8 min)]

"The seared steak recipe is my favorite. It watches the pan climb to two-thirty Celsius, tells you the pan is screaming hot, you drop the steak, and it starts a three-minute sear timer. Then it says -- and I quote -- FLIP NOW."

[TRANSITION: Cut]

---

## [SCENE 19: The Recipe Library - 7:10-7:30] [VO + Screen Capture]

[VISUAL: GitHub repo page showing the /recipes directory. Click into the category folders -- basics, proteins, vegetables, sauces.]

NARRATION:
"Six recipes built in: white rice, pasta, fried eggs, boiled potatoes, caramelized onions, seared steak. But the real play is the community. Recipes live in a GitHub repo. You fork it, write a JSON file, test it in simulation mode, and submit a pull request."

[VISUAL: Show the PR template briefly]

"Every recipe gets tuned with real thermal data. Gas heats differently than induction -- the recipes know that."

[TRANSITION: Cut]

---

## [SCENE 20: Simulation Mode - 7:30-7:50] [LIVE + Screen Capture]

[VISUAL: Dashboard in simulation mode. Temperature slider being dragged to simulate heating. Recipe steps advancing as virtual temperatures hit triggers.]

TALKING POINTS:
- "And if you don't want to actually cook to test a recipe, there's simulation mode."
- Show the simulation slider and preset buttons
- Drag temperature up -- show recipe steps advancing
- "You can develop and test recipes without turning on your stove."

[TRANSITION: Cut]

---

## [SCENE 21: Recipe JSON Close-Up - 7:50-8:00] [VO + Screen Capture]

[VISUAL: Split screen -- JSON on the left, dashboard running that recipe on the right. As each step activates in the dashboard, the corresponding JSON step highlights on the left.]

NARRATION:
"Five fields. That's a recipe. If you can write JSON, you can teach a stove to cook."

[TEXT OVERLAY: "Five fields. One recipe. Fork the repo."]

[TRANSITION: Crossfade, 1s]

---

# Chapter 6: What's Next + CTA (8:00 - 9:00)

## [SCENE 22: Resources - 8:00-8:25] [VO]

[VISUAL: Quick montage of project links with QR codes overlaid: (A) Hackaday.io project page, (B) GitHub repo main page, (C) Recipes directory]

NARRATION:
"Everything is on GitHub -- firmware, recipes, hardware files, enclosure models. The Hackaday dot io project page has the full build log. Links are in the description."

[TEXT OVERLAY: QR codes for GitHub repo and Hackaday.io page]

[TRANSITION: Cut]

---

## [SCENE 23: What's Coming - 8:25-8:45] [VO]

[VISUAL: Teaser images -- (A) KiCad PCB layout render (if available), (B) 3D enclosure render, (C) GitHub Issues page showing planned features]

NARRATION:
"Next up -- a proper PCB. No more breadboard. Open-source KiCad files so you can order boards from JLCPCB or PCBWay. And more recipes -- I want a hundred community-contributed recipes by the end of the year."

[TRANSITION: Cut]

---

## [SCENE 24: Call to Action / End Card - 8:45-9:00] [LIVE]

[VISUAL: On-camera, holding the device. Genuine, direct to camera.]

TALKING POINTS:
- "Build one. It's two boards and four wires."
- "Contribute a recipe. Fork the repo."
- "Let's make cooking apps obsolete."
- "Subscribe for the build series -- next video is a deep dive on the thermal imaging pipeline."
- "Star the repo on GitHub. Link in the description."

[TEXT OVERLAY: End card with subscribe button, GitHub link, Hackaday.io link]
[MUSIC: Fade out]

---

## Production Notes

### Word Count Summary
- Voiceover narration: ~1,050 words
- Estimated VO runtime at 150 WPM: ~7:00
- Live on-camera segments: ~2:00 of talking points (not scripted word-for-word)
- Total estimated runtime: ~9:00

### Music
- Upbeat, lo-fi maker/workshop vibe
- Fade in at title card (0:50), maintain under VO at ~12% volume
- Fade out at end card (8:55)

### B-Roll Needed
- Generic cooking timer app (stock or screen record)
- Probe thermometer in food (film or stock)
- Boiling pot (film)
- Workbench overhead shots (film)
- Terminal/PlatformIO screen capture (record)
- BLE provisioning phone recording (record)
- Full cooking demo footage with dashboard visible (film)
- GitHub repo screen capture (record)
