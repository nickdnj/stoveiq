# Video Outline: I Built a $50 Thermal Cooking Coach (and it actually works)

## Target: Build/Demo, ~9 minutes, Makers + Hobbyist Cooks + Hackaday/DIY Community
## Tone: Casual maker energy. "Look what I built." Authentic, not overproduced.
## Narration: Mix of voiceover [VO] and live on-camera [LIVE]

---

## Chapter 1: The Problem (0:00 - 1:00)
### Summary
Open with a provocative hook that frames the gap between existing cooking tech (dumb timers, single-point probes) and what should exist (a stove that can see). Build frustration, then pivot to "what if?"
### Key Points
- Every cooking app on the planet is a glorified countdown timer
- Probe thermometers measure one point, in one dish, at a time
- Nobody is watching the whole stove surface -- until now
- Hook: "What if your stove could actually SEE what you're cooking?"
### Scenes: 3
### Visual Approach
Split-screen comparison: timer app UI vs. StoveIQ thermal heatmap. Quick cuts between frustrated cooking moments and the thermal camera reveal.

---

## Chapter 2: The Idea (1:00 - 2:00)
### Summary
Introduce the two core components (MLX90640 thermal camera + ESP32-S3 microcontroller), explain the cost, and land the open-source value proposition. This is the "aha" moment where the audience realizes how accessible this is.
### Key Points
- MLX90640: 24x32 pixels of infrared thermal data, 110-degree field of view, 4Hz
- ESP32-S3: WiFi + BLE, runs the entire system -- sensor read, cooking engine, web server
- Total cost: $50-95 depending on where you source parts
- 100% local -- no cloud, no subscription, no app store. Just a browser.
- Open source: MIT software, CERN-OHL-S hardware
### Scenes: 3
### Visual Approach
Clean product shots of the two boards. Animated overlay showing what each component does. Cost breakdown graphic.

---

## Chapter 3: The Build (2:00 - 4:15)
### Summary
Walk through the physical build from unboxing to first thermal image. This is the core maker content -- show how easy it is to replicate. Breadboard wiring, firmware flash, BLE provisioning, and the "money shot" of seeing the stove in thermal vision for the first time.
### Key Points
- BOM: 2 boards + 4 jumper wires + USB cable
- Wiring: VIN to 3V3, GND to GND, SDA to GPIO 1, SCL to GPIO 2
- Firmware flash with PlatformIO (one command)
- BLE provisioning with ESP BLE Prov app (PoP: stoveiq-setup)
- First thermal image on the web dashboard -- the money shot
- PVC pipe enclosure: split pipe, drill sensor window, snap together
### Scenes: 6
### Visual Approach
Overhead workbench camera for wiring. Screen capture for PlatformIO terminal. Phone screen recording for BLE provisioning. Dashboard reveal is the hero moment -- hold on the heatmap.

---

## Chapter 4: The Cooking Coach (4:15 - 6:30)
### Summary
Live cooking demo showing the full coaching experience. Open the dashboard on a phone, show the heatmap with real burners, calibrate burner zones, and run a recipe with thermal-aware coaching. This is the "it actually works" proof.
### Key Points
- Open stoveiq.local on phone while at the stove
- Live heatmap showing real burner temperatures
- Burner calibration: draw circles over each burner zone on the heatmap
- Start a recipe (pasta): thermal triggers detect boil, prompt for actions, run timers
- "It knows my water is boiling before I do"
- Progress bars, coaching messages, confirmation buttons
- Multiple burners tracked simultaneously
### Scenes: 5
### Visual Approach
Split-screen: phone dashboard on left, actual stove on right. Close-ups of the phone showing coaching messages. Wide shot of cooking with the phone propped on the counter. Genuine reactions.

---

## Chapter 5: The Recipe System (6:30 - 8:00)
### Summary
Explain how recipes work under the hood -- JSON state machines with thermal triggers. Show the community recipe model (GitHub PRs) and simulation mode for testing without cooking. Make the audience want to contribute.
### Key Points
- Recipes are JSON files with steps, triggers, and coaching messages
- 8 trigger types: target temp, boil, simmer, food_drop, timer, confirm, manual, temp_below
- 6 built-in recipes: rice, steak, pasta, eggs, potatoes, caramelized onions
- Community contribution via GitHub pull requests
- Simulation mode: test recipes with virtual thermal data, no cooking required
- Show a recipe JSON side-by-side with the dashboard running it
### Scenes: 4
### Visual Approach
Code editor showing recipe JSON with callout annotations. Screen capture of simulation mode. GitHub repo page showing the recipes directory. Side-by-side: JSON steps mapping to dashboard UI states.

---

## Chapter 6: What's Next + CTA (8:00 - 9:00)
### Summary
Point viewers to all the resources, tease upcoming features (PCB, more recipes), and issue a clear call to action: build one, contribute a recipe, join the community.
### Key Points
- Hackaday.io project page (build log, discussion)
- GitHub repo: firmware, recipes, hardware files
- PCB design coming (KiCad, open source) -- no more breadboard
- "Build one. Contribute a recipe. Let's make cooking apps obsolete."
- Subscribe to the channel for build updates
- Star the repo on GitHub
### Scenes: 3
### Visual Approach
Quick montage of the project links with QR codes. Teaser render of the PCB (if available). End card with subscribe button and GitHub link.

---

## Estimated Runtime: 9 minutes
## Total Chapters: 6
## Total Scenes: 24
## Estimated Word Count (narration): ~1,350 words at 150 WPM
