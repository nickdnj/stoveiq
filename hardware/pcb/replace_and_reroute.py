#!/usr/bin/env python3
"""
StoveIQ PCB - Improved placement + re-route.
Deletes all tracks/vias, replaces components with tighter layout, re-runs Freerouting.
"""
import os, sys, subprocess

sys.path.insert(0, "/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
os.environ["DYLD_FRAMEWORK_PATH"] = "/Applications/KiCad/KiCad.app/Contents/Frameworks"

import pcbnew

def mm(val):
    return pcbnew.FromMM(val)

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    pcb_path = os.path.join(base, "stoveiq.kicad_pcb")
    dsn_path = os.path.join(base, "stoveiq.dsn")
    ses_path = os.path.join(base, "stoveiq.ses")
    jar_path = os.path.join(base, "..", "tools", "freerouting.jar")

    print("=" * 60)
    print("StoveIQ - Improved Placement + Autoroute")
    print("=" * 60)

    board = pcbnew.LoadBoard(pcb_path)
    print(f"Loaded: {len(list(board.GetFootprints()))} footprints, {len(list(board.GetTracks()))} tracks")

    # Step 1: Delete all tracks and vias
    print("\n[1] Deleting all tracks and vias...")
    tracks = list(board.GetTracks())
    for t in tracks:
        board.Remove(t)
    print(f"  Removed {len(tracks)} track segments")

    # Step 2: Improved placement
    # Board outline: (100,80) to (145,115) = 45x35mm
    # Strategy:
    #   LEFT column (x=102-113):  Power input section
    #   CENTER (x=114-132):       Main ICs, buttons, buzzer driver
    #   RIGHT column (x=133-143): Sensor, connectors, I2C pull-ups
    #
    # TOP row (y=82-92):     Decoupling caps, small passives
    # MIDDLE row (y=93-104): Main ICs, power
    # BOTTOM row (y=105-113): Buttons, buzzer, debug

    print("\n[2] Placing components...")

    placements = {
        # === POWER INPUT (left side) ===
        "J1":   (101.5, 97.0, 270, "F.Cu"),      # USB-C connector, left edge, rotated
        "D1":   (104.0, 93.5, 0, "F.Cu"),       # TVS diode near USB input
        "R1":   (104.0, 88.0, 0, "F.Cu"),        # CC1 pull-down
        "R2":   (106.5, 88.0, 0, "F.Cu"),        # CC2 pull-down
        "C1":   (108.0, 93.5, 0, "F.Cu"),        # Input bulk cap 10uF

        # === VOLTAGE REGULATOR (left-center) ===
        "U1":   (114.0, 97.0, 0, "B.Cu"),        # AMS1117 LDO (back side)
        "C2":   (110.0, 100.0, 0, "B.Cu"),       # LDO input cap (back)
        "C3":   (118.0, 100.0, 0, "B.Cu"),       # LDO output cap (back)

        # === ESP32 DECOUPLING (top center) ===
        # ESP32 module would go center ~(122, 95) — missing footprint
        "C4":   (120.0, 85.0, 0, "F.Cu"),        # 100nF decoupling
        "C5":   (123.0, 85.0, 0, "F.Cu"),        # 100nF decoupling
        "C6":   (126.0, 85.0, 0, "F.Cu"),        # 10uF bulk decoupling

        # === RESET / BOOT (bottom left) ===
        "R3":   (105.0, 106.0, 0, "F.Cu"),       # EN pull-up 10k
        "SW1":  (105.0, 111.0, 0, "F.Cu"),       # Reset button
        "R4":   (113.0, 106.0, 0, "F.Cu"),       # GPIO0 pull-up 10k
        "SW2":  (113.0, 111.0, 0, "F.Cu"),       # Boot button

        # === BUZZER DRIVER (bottom center) ===
        "R7":   (122.0, 107.0, 90, "F.Cu"),      # Base resistor 1k
        "Q1":   (125.0, 107.0, 0, "F.Cu"),       # NPN driver MMBT3904
        "BZ1":  (131.0, 109.0, 0, "F.Cu"),       # Piezo buzzer

        # === STATUS LED (bottom, near center) ===
        "LED1": (119.0, 111.0, 0, "F.Cu"),       # WS2812B status LED
        "C8":   (119.0, 114.0, 0, "F.Cu"),       # LED decoupling

        # === IR SENSOR SECTION (right side) ===
        "U3":   (141.0, 97.0, 0, "F.Cu"),        # MLX90640 IR sensor, right edge
        "R5":   (136.0, 93.0, 0, "F.Cu"),        # I2C SDA pull-up 4.7k
        "R6":   (136.0, 96.0, 0, "F.Cu"),        # I2C SCL pull-up 4.7k
        "C7":   (136.0, 99.0, 0, "F.Cu"),        # MLX90640 decoupling

        # === CONNECTORS (right side, inset for body clearance) ===
        "J2":   (137.0, 85.0, 0, "F.Cu"),        # JST gas sensor expansion (top right)
        "J3":   (137.0, 112.0, 0, "F.Cu"),       # UART debug header (bottom right)
    }

    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref in placements:
            x, y, angle, layer = placements[ref]
            # Reset to front if needed before flipping
            if fp.IsFlipped() and layer == "F.Cu":
                fp.Flip(fp.GetPosition(), False)
            elif not fp.IsFlipped() and layer == "B.Cu":
                fp.Flip(fp.GetPosition(), False)
            fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
            if angle != 0:
                fp.SetOrientationDegrees(angle)
            side = "BACK" if layer == "B.Cu" else "FRONT"
            print(f"  {ref:6s} -> ({x:.0f}, {y:.0f}) {side}")

    # Step 3: Save
    print("\n[3] Saving board...")
    pcbnew.SaveBoard(pcb_path, board)

    # Step 4: Export DSN
    print("\n[4] Exporting Specctra DSN...")
    pcbnew.ExportSpecctraDSN(board, dsn_path)

    # Step 5: Autoroute
    print("\n[5] Running Freerouting...")
    result = subprocess.run(
        ["java", "-jar", jar_path, "-de", dsn_path, "-do", ses_path, "-mp", "30"],
        capture_output=True, text=True, timeout=300
    )
    # Parse key info from output
    for line in (result.stdout + result.stderr).split("\n"):
        if any(k in line.lower() for k in ["pass", "complet", "score", "error", "fail", "unrouted"]):
            print(f"  {line.strip()}")
    if result.returncode != 0:
        print(f"  WARNING: exit code {result.returncode}")

    # Step 6: Import SES
    print("\n[6] Importing routed result...")
    if os.path.exists(ses_path):
        board = pcbnew.LoadBoard(pcb_path)
        pcbnew.ImportSpecctraSES(board, ses_path)
        pcbnew.SaveBoard(pcb_path, board)
        tracks_after = len(list(board.GetTracks()))
        print(f"  Done: {tracks_after} track segments")
    else:
        print("  ERROR: SES file not found")

    # Step 7: DRC
    print("\n[7] Running DRC...")
    os.system(f'/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc "{pcb_path}" 2>&1 | head -3')

    print("\n" + "=" * 60)
    print("DONE — reload in KiCad to review")
    print("=" * 60)

if __name__ == "__main__":
    main()
