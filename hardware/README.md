# StoveIQ Hardware Design

## KiCad Project

**Location:** `pcb/stoveiq.kicad_pro`
**Tool:** KiCad 9 (Altium-importable)
**Board:** 2-layer FR4, 45x35mm

### Opening the Project

```bash
open /Applications/KiCad/KiCad.app pcb/stoveiq.kicad_pro
```

Or from KiCad: File → Open Project → select `pcb/stoveiq.kicad_pro`

### Schematic Components

| Ref | Part | Package | Purpose |
|-----|------|---------|---------|
| U1 | AMS1117-3.3 | SOT-223 | 5V→3.3V LDO regulator |
| U2 | ESP32-S3-WROOM-1-N8R8 | Module | WiFi+BLE MCU, 8MB Flash/PSRAM |
| U3 | MLX90640ESF-BAB | 4-pin | 32x24 IR thermal array, 110° FoV |
| J1 | USB4110-GF-A | SMD | USB-C power input |
| J2 | B4B-PH-K-S | JST-PH | Gas sensor expansion (I2C Bus 1) |
| J3 | Pin Header 1x3 | 2.54mm | UART debug (omit in production) |
| LED1 | WS2812B-Mini | PLCC4 | RGB status LED |
| BZ1 | PKLCS1212E4001 | 12mm | Piezo buzzer (85dB) |
| Q1 | MMBT3904 | SOT-23 | Buzzer NPN driver |
| D1 | PESD5V0U2BT | SOD-523 | USB ESD protection |
| SW1 | Tactile switch | 6mm | Reset |
| SW2 | Tactile switch | 6mm | Boot mode |
| R1-R2 | 5.1k | 0402 | USB-C CC pull-downs |
| R3-R4 | 10k | 0402 | EN/GPIO0 pull-ups |
| R5-R6 | 4.7k | 0402 | I2C pull-ups (Bus 0) |
| R7 | 1k | 0402 | Buzzer base resistor |
| C1-C2 | 10uF/10V | 0805 | Input + LDO input caps |
| C3 | 22uF/6.3V | 0805 | LDO output cap |
| C4-C5 | 100nF | 0402 | ESP32 decoupling |
| C6 | 10uF | 0805 | ESP32 bulk decoupling |
| C7-C8 | 100nF | 0402 | MLX90640 + LED decoupling |

### ESP32-S3 Pin Assignments

| GPIO | Function | Notes |
|------|----------|-------|
| 1 | I2C0 SDA | MLX90640 thermal sensor |
| 2 | I2C0 SCL | MLX90640 thermal sensor |
| 3 | I2C1 SDA | Gas sensor expansion (JST) |
| 4 | I2C1 SCL | Gas sensor expansion (JST) |
| 19 | USB D- | Native USB-JTAG |
| 20 | USB D+ | Native USB-JTAG |
| 38 | WS2812B DIN | Status LED data |
| 39 | Buzzer | Via Q1 NPN transistor |
| 43 | UART0 TX | Debug header |
| 44 | UART0 RX | Debug header |
| 0 | BOOT | Boot mode button |
| EN | RESET | Reset button |

### PCB Layout Guidelines

1. **Antenna keep-out:** 10mm clear zone around ESP32-S3 WROOM antenna (top edge)
2. **Thermal isolation:** MLX90640 at opposite edge from ESP32, on 2mm standoff
3. **LDO placement:** Back side of PCB with copper pour for heat spreading
4. **USB-C:** Board edge, accessible from enclosure opening
5. **I2C traces:** Keep under 10cm, no need for impedance matching at 400kHz
6. **Ground plane:** Solid on bottom layer, split only for antenna keep-out area

### Altium Import

This project is designed for KiCad→Altium transfer:
1. Open Altium Designer
2. File → Import → KiCad Design Files
3. Select `pcb/stoveiq.kicad_pro`
4. Altium imports schematic, PCB, and libraries

### BOM Cost Target

~$27 without gas module, ~$33 with BME688 gas sensor module.
