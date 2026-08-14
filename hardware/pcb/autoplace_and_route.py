#!/usr/bin/env python3
"""
StoveIQ PCB Auto-Place and Route
Uses KiCad's pcbnew Python API + Freerouting autorouter.

Pipeline:
1. Load board
2. Place all footprints with proper positioning
3. Add ground pour on B.Cu
4. Export Specctra DSN
5. Run Freerouting autorouter
6. Import routed SES back
7. Save board

Usage:
  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9 autoplace_and_route.py
"""

import os
import sys
import subprocess

# Add KiCad's Python packages
sys.path.insert(0, "/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
os.environ["DYLD_FRAMEWORK_PATH"] = "/Applications/KiCad/KiCad.app/Contents/Frameworks"

import pcbnew

# Board dimensions in mm
BOARD_W = 45.0
BOARD_H = 35.0
BOARD_ORIGIN_X = 100.0  # mm from sheet origin
BOARD_ORIGIN_Y = 80.0

# Convert mm to KiCad internal units (nanometers)
def mm(val):
    return pcbnew.FromMM(val)

def place_footprint(board, fp, x_mm, y_mm, angle_deg=0, layer="F.Cu"):
    """Place a footprint at given position."""
    fp.SetPosition(pcbnew.VECTOR2I(mm(x_mm), mm(y_mm)))
    if angle_deg != 0:
        fp.SetOrientationDegrees(angle_deg)
    if layer == "B.Cu":
        fp.Flip(fp.GetPosition(), False)
    print(f"  Placed {fp.GetReference():6s} ({fp.GetValue():20s}) at ({x_mm:.1f}, {y_mm:.1f}) {angle_deg}deg {'BACK' if layer == 'B.Cu' else ''}")

def main():
    pcb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stoveiq.kicad_pcb")
    dsn_path = pcb_path.replace(".kicad_pcb", ".dsn")
    ses_path = pcb_path.replace(".kicad_pcb", ".ses")
    freerouting_jar = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools", "freerouting.jar")

    print("=" * 60)
    print("StoveIQ PCB Auto-Place and Route")
    print("=" * 60)

    # Step 1: Load board
    print("\n[1/7] Loading board...")
    board = pcbnew.LoadBoard(pcb_path)
    print(f"  Loaded: {pcb_path}")
    print(f"  Nets: {board.GetNetCount()}")

    footprints = list(board.GetFootprints())
    print(f"  Footprints: {len(footprints)}")

    if len(footprints) == 0:
        print("\n  No footprints on board yet. Running netlist import first...")
        print("  NOTE: You need to do 'Update PCB from Schematic' (F8) in KiCad first")
        print("  to transfer components from schematic to PCB.")
        print("  Then re-run this script.")
        sys.exit(1)

    # Step 2: Place footprints
    print("\n[2/7] Placing footprints...")

    # Board area: 100,80 to 145,115 (45x35mm)
    # Layout strategy:
    #   - USB-C (J1): left edge, centered vertically
    #   - LDO (U1): left-center, BACK SIDE for heat spreading
    #   - Input caps (C1, C2): near LDO input
    #   - Output cap (C3): near LDO output
    #   - ESP32-S3 module: center of board (it's the biggest component ~18x25mm)
    #   - ESP32 decoupling (C4, C5, C6): right next to ESP32 VDD pins
    #   - MLX90640 (U3): right edge, on thermal standoff
    #   - I2C pull-ups (R5, R6): between ESP32 and MLX90640
    #   - CC resistors (R1, R2): near USB-C
    #   - TVS diode (D1): near USB-C
    #   - WS2812B LED (LED1): front edge, visible
    #   - Buzzer (BZ1): front edge
    #   - Buzzer driver (Q1, R7): near buzzer
    #   - Reset/Boot (SW1, SW2): accessible edge
    #   - Pull-ups (R3, R4): near switches
    #   - JST connector (J2): right side
    #   - UART header (J3): right side, debug access
    #   - Mounting holes: 4 corners

    # Component placement map (reference -> (x_mm, y_mm, angle, layer))
    # Coordinates are absolute on the PCB sheet
    placements = {
        # Power input section (left side)
        "J1":   (103.0, 97.5, 0, "F.Cu"),      # USB-C connector, left edge
        "R1":   (107.0, 88.0, 0, "F.Cu"),       # CC1 pull-down
        "R2":   (109.0, 88.0, 0, "F.Cu"),       # CC2 pull-down
        "D1":   (109.0, 93.0, 0, "F.Cu"),       # TVS diode
        "C1":   (111.0, 97.5, 0, "F.Cu"),       # Input bulk cap

        # Voltage regulator (left-center, back side)
        "U1":   (115.0, 97.5, 0, "B.Cu"),       # AMS1117 LDO on BACK
        "C2":   (112.0, 103.0, 0, "B.Cu"),      # LDO input cap (back)
        "C3":   (118.0, 103.0, 0, "B.Cu"),      # LDO output cap (back)

        # ESP32-S3 module (center - this is ~18x25mm, dominates the board)
        # Module center at board center, shifted slightly right
        # Antenna end faces TOP edge (away from wall, toward room)
        "C4":   (125.0, 87.0, 0, "F.Cu"),       # ESP32 decoupling 100nF
        "C5":   (127.5, 87.0, 0, "F.Cu"),       # ESP32 decoupling 100nF
        "C6":   (130.0, 87.0, 0, "F.Cu"),       # ESP32 decoupling 10uF

        # Reset/Boot buttons (bottom left, accessible)
        "SW1":  (106.0, 111.0, 0, "F.Cu"),      # Reset button
        "SW2":  (112.0, 111.0, 0, "F.Cu"),      # Boot button
        "R3":   (106.0, 107.0, 0, "F.Cu"),      # EN pull-up 10k
        "R4":   (112.0, 107.0, 0, "F.Cu"),      # GPIO0 pull-up 10k

        # MLX90640 IR sensor (right edge, on standoff)
        "U3":   (141.0, 97.5, 0, "F.Cu"),       # IR sensor at right edge
        "R5":   (136.0, 92.0, 0, "F.Cu"),       # I2C SDA pull-up
        "R6":   (136.0, 95.0, 0, "F.Cu"),       # I2C SCL pull-up
        "C7":   (138.0, 103.0, 0, "F.Cu"),      # MLX90640 decoupling

        # Status LED (front, visible through enclosure)
        "LED1": (122.0, 112.0, 0, "F.Cu"),      # WS2812B status LED
        "C8":   (126.0, 112.0, 0, "F.Cu"),      # LED decoupling

        # Buzzer + driver (front right)
        "BZ1":  (133.0, 111.0, 0, "F.Cu"),      # Piezo buzzer
        "Q1":   (130.0, 107.0, 0, "F.Cu"),      # NPN driver
        "R7":   (128.0, 107.0, 90, "F.Cu"),     # Base resistor

        # Connectors (right side)
        "J2":   (142.0, 88.0, 0, "F.Cu"),       # JST gas sensor expansion
        "J3":   (142.0, 107.0, 0, "F.Cu"),      # UART debug header
    }

    placed = 0
    not_found = []
    for fp in footprints:
        ref = fp.GetReference()
        if ref in placements:
            x, y, angle, layer = placements[ref]
            place_footprint(board, fp, x, y, angle, layer)
            placed += 1
        elif ref.startswith("MH"):
            # Mounting holes already positioned in PCB file
            pass
        else:
            not_found.append(ref)

    print(f"\n  Placed: {placed}/{len(placements)}")
    if not_found:
        print(f"  Not in placement map: {not_found}")

    # Step 3: Add ground pour on bottom copper layer
    print("\n[3/7] Adding ground pour on B.Cu...")
    try:
        zone = pcbnew.ZONE(board)
        zone.SetIsRuleArea(False)
        zone.SetDoNotAllowTracks(False)
        zone.SetDoNotAllowVias(False)
        zone.SetDoNotAllowPads(False)
        zone.SetDoNotAllowCopperPour(False)
        zone.SetLayer(pcbnew.B_Cu)

        # Find GND net
        gnd_net = None
        for net in board.GetNetsByName():
            if net == "GND":
                gnd_net = board.GetNetsByName()[net]
                break

        if gnd_net:
            zone.SetNet(gnd_net)
            print(f"  GND net found: {gnd_net.GetNetname()} (code {gnd_net.GetNetCode()})")
        else:
            print("  WARNING: GND net not found, zone will be unassigned")

        # Zone outline = board outline with 0.5mm inset
        inset = 0.5
        outline = zone.Outline()
        outline.NewOutline()
        outline.Append(mm(BOARD_ORIGIN_X + inset), mm(BOARD_ORIGIN_Y + inset))
        outline.Append(mm(BOARD_ORIGIN_X + BOARD_W - inset), mm(BOARD_ORIGIN_Y + inset))
        outline.Append(mm(BOARD_ORIGIN_X + BOARD_W - inset), mm(BOARD_ORIGIN_Y + BOARD_H - inset))
        outline.Append(mm(BOARD_ORIGIN_X + inset), mm(BOARD_ORIGIN_Y + BOARD_H - inset))

        zone.SetMinThickness(mm(0.25))
        zone.SetThermalReliefGap(mm(0.5))
        zone.SetThermalReliefSpokeWidth(mm(0.5))

        board.Add(zone)
        print("  Ground pour added on B.Cu")
    except Exception as e:
        print(f"  WARNING: Could not add ground pour: {e}")

    # Step 4: Save placed board
    print("\n[4/7] Saving placed board...")
    pcbnew.SaveBoard(pcb_path, board)
    print(f"  Saved: {pcb_path}")

    # Step 5: Export Specctra DSN
    print("\n[5/7] Exporting Specctra DSN...")
    try:
        pcbnew.ExportSpecctraDSN(board, dsn_path)
        print(f"  Exported: {dsn_path}")
    except Exception as e:
        print(f"  Export failed: {e}")
        print("  You may need to export DSN manually from KiCad: File > Export > Specctra DSN")
        sys.exit(1)

    # Step 6: Run Freerouting autorouter
    print("\n[6/7] Running Freerouting autorouter...")
    if not os.path.exists(freerouting_jar):
        print(f"  ERROR: Freerouting not found at {freerouting_jar}")
        print("  Download from: https://github.com/freerouting/freerouting/releases")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["java", "-jar", freerouting_jar,
             "-de", dsn_path,    # input DSN
             "-do", ses_path,    # output SES
             "-mp", "20"],       # max passes
            capture_output=True, text=True, timeout=300
        )
        print(f"  Freerouting stdout: {result.stdout[:500] if result.stdout else '(none)'}")
        if result.stderr:
            print(f"  Freerouting stderr: {result.stderr[:500]}")
        if result.returncode != 0:
            print(f"  WARNING: Freerouting exited with code {result.returncode}")
        else:
            print("  Autorouting complete!")
    except subprocess.TimeoutExpired:
        print("  WARNING: Freerouting timed out after 5 minutes")
    except Exception as e:
        print(f"  ERROR running Freerouting: {e}")
        sys.exit(1)

    # Step 7: Import routed SES back
    print("\n[7/7] Importing routed SES...")
    if os.path.exists(ses_path):
        try:
            # Reload board (Freerouting may have modified state)
            board = pcbnew.LoadBoard(pcb_path)
            pcbnew.ImportSpecctraSES(board, ses_path)
            pcbnew.SaveBoard(pcb_path, board)
            print(f"  Imported and saved: {pcb_path}")
        except Exception as e:
            print(f"  Import failed: {e}")
            print("  You can import manually: File > Import > Specctra Session")
    else:
        print(f"  SES file not found: {ses_path}")
        print("  Autorouting may have failed. Check Freerouting output above.")

    print("\n" + "=" * 60)
    print("DONE! Open in KiCad to review:")
    print(f"  open {pcb_path}")
    print("=" * 60)

    # Run DRC
    print("\nRunning DRC check...")
    os.system(f'/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc "{pcb_path}" 2>&1')


if __name__ == "__main__":
    main()
