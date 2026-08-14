#!/usr/bin/env python3
"""Create a fresh StoveIQ PCB from scratch with all 26 components placed."""
import sys, os
sys.path.insert(0, "/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
os.environ["DYLD_FRAMEWORK_PATH"] = "/Applications/KiCad/KiCad.app/Contents/Frameworks"
import pcbnew

def mm(v): return pcbnew.FromMM(v)

FP_DIR = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
OX, OY, BW, BH = 100.0, 80.0, 45.0, 35.0

board = pcbnew.BOARD()
board.SetCopperLayerCount(2)

# Board outline
for s, e in [((OX,OY),(OX+BW,OY)),((OX+BW,OY),(OX+BW,OY+BH)),
             ((OX+BW,OY+BH),(OX,OY+BH)),((OX,OY+BH),(OX,OY))]:
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetStart(pcbnew.VECTOR2I(mm(s[0]), mm(s[1])))
    seg.SetEnd(pcbnew.VECTOR2I(mm(e[0]), mm(e[1])))
    seg.SetLayer(pcbnew.Edge_Cuts)
    seg.SetWidth(mm(0.15))
    board.Add(seg)
print("Board outline: 45x35mm")

# Nets
nets = ['', 'GND', '+3V3', '+5V', 'I2C0_SDA', 'I2C0_SCL', 'I2C1_SDA', 'I2C1_SCL',
        'GPIO_LED', 'GPIO_BUZZER', 'USB_DP', 'USB_DN', 'VBUS', 'CC1', 'CC2', 'EN', 'GPIO0',
        'UART_TX', 'UART_RX', 'BUZ_P', 'BUZ_BASE']
for i, n in enumerate(nets):
    board.Add(pcbnew.NETINFO_ITEM(board, n, i))
print(f"Created {len(nets)} nets")

# Components: (ref, lib, footprint, value, x, y, angle, side)
parts = [
    # POWER INPUT (left)
    ("J1",  "Connector_USB.pretty",                "USB_C_Receptacle_GCT_USB4110",              "USB-C",         103.0, 97.0,  90, "F"),
    ("D1",  "Diode_SMD.pretty",                    "D_SOD-523",                                 "PESD5V0U2BT",   108.0, 92.0,   0, "F"),
    ("R1",  "Resistor_SMD.pretty",                 "R_0402_1005Metric",                         "5.1k",          108.0, 87.0,   0, "F"),
    ("R2",  "Resistor_SMD.pretty",                 "R_0402_1005Metric",                         "5.1k",          110.5, 87.0,   0, "F"),
    ("C1",  "Capacitor_SMD.pretty",                "C_0805_2012Metric",                         "10uF",          111.0, 92.0,   0, "F"),
    # VOLTAGE REGULATOR (center-left)
    ("U1",  "Package_TO_SOT_SMD.pretty",           "SOT-223-3_TabPin2",                         "AMS1117-3.3",   116.0, 97.0,   0, "F"),
    ("C2",  "Capacitor_SMD.pretty",                "C_0805_2012Metric",                         "10uF",          112.0,101.0,   0, "F"),
    ("C3",  "Capacitor_SMD.pretty",                "C_0805_2012Metric",                         "22uF",          120.0,101.0,   0, "F"),
    # ESP32 DECOUPLING (top center)
    ("C4",  "Capacitor_SMD.pretty",                "C_0402_1005Metric",                         "100nF",         121.0, 84.0,   0, "F"),
    ("C5",  "Capacitor_SMD.pretty",                "C_0402_1005Metric",                         "100nF",         124.0, 84.0,   0, "F"),
    ("C6",  "Capacitor_SMD.pretty",                "C_0805_2012Metric",                         "10uF",          127.5, 84.0,   0, "F"),
    # RESET/BOOT (bottom left)
    ("R3",  "Resistor_SMD.pretty",                 "R_0402_1005Metric",                         "10k",           105.0,106.0,   0, "F"),
    ("SW1", "Button_Switch_SMD.pretty",            "SW_SPST_TL3342",                            "RESET",         105.0,111.0,   0, "F"),
    ("R4",  "Resistor_SMD.pretty",                 "R_0402_1005Metric",                         "10k",           112.0,106.0,   0, "F"),
    ("SW2", "Button_Switch_SMD.pretty",            "SW_SPST_TL3342",                            "BOOT",          112.0,111.0,   0, "F"),
    # STATUS LED (bottom center)
    ("LED1","LED_SMD.pretty",                      "LED_WS2812B-Mini_PLCC4_3.5x3.5mm",          "WS2812B",       120.0,111.0,   0, "F"),
    ("C8",  "Capacitor_SMD.pretty",                "C_0402_1005Metric",                         "100nF",         124.0,111.0,   0, "F"),
    # BUZZER DRIVER (bottom right)
    ("R7",  "Resistor_SMD.pretty",                 "R_0402_1005Metric",                         "1k",            127.0,108.0,  90, "F"),
    ("Q1",  "Package_TO_SOT_SMD.pretty",           "SOT-23",                                    "MMBT3904",      129.5,108.0,   0, "F"),
    ("BZ1", "Buzzer_Beeper.pretty",                "Buzzer_12x9.5RM7.6",                        "Buzzer",        135.0,109.0,   0, "F"),
    # IR SENSOR (right)
    ("U3",  "Package_TO_SOT_THT.pretty",           "TO-39-4_Window",                            "MLX90640",      140.0, 97.0,   0, "F"),
    ("R5",  "Resistor_SMD.pretty",                 "R_0402_1005Metric",                         "4.7k",          135.0, 92.0,   0, "F"),
    ("R6",  "Resistor_SMD.pretty",                 "R_0402_1005Metric",                         "4.7k",          135.0, 95.0,   0, "F"),
    ("C7",  "Capacitor_SMD.pretty",                "C_0402_1005Metric",                         "100nF",         135.0, 99.0,   0, "F"),
    # CONNECTORS (right)
    ("J2",  "Connector_JST.pretty",                "JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical",    "Gas Sensor",    134.0, 84.0,   0, "F"),
    ("J3",  "Connector_PinHeader_2.54mm.pretty",   "PinHeader_1x03_P2.54mm_Vertical",           "UART",          140.0,111.0,   0, "F"),
]

placed = 0
for ref, lib, fpname, value, x, y, angle, side in parts:
    try:
        fp = pcbnew.FootprintLoad(os.path.join(FP_DIR, lib), fpname)
        fp.SetReference(ref)
        fp.SetValue(value)
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        if angle != 0:
            fp.SetOrientationDegrees(angle)
        # Skip Flip() — causes segfault on new boards without full stackup
        # Back-side placement can be done interactively in KiCad
        board.Add(fp)
        placed += 1
        tag = "BACK" if side == "B" else ""
        print(f"  {ref:6s} {value:15s} ({x:.0f},{y:.0f}) {tag}")
    except Exception as e:
        print(f"  ERROR {ref}: {e}")

print(f"\nPlaced {placed}/{len(parts)}")
pcbnew.SaveBoard("stoveiq.kicad_pcb", board)
print("Saved: stoveiq.kicad_pcb")
