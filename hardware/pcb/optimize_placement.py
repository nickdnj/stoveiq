#!/usr/bin/env python3
"""
StoveIQ PCB Placement Optimizer — Simulated Annealing

Optimizes component placement to minimize total wirelength while
respecting board constraints (keep-outs, edge placement, thermal isolation).

Usage:
  python3 optimize_placement.py [--iterations 5000] [--temp 100] [--cooling 0.995]
"""

import math
import random
import copy
import argparse
from kiutils.board import Board

# ============================================================
# BOARD GEOMETRY
# ============================================================
# Board outline in KiCad coords (mm)
BRD_X0, BRD_Y0 = 100.0, 80.0  # top-left
BRD_X1, BRD_Y1 = 145.0, 115.0  # bottom-right
BRD_W, BRD_H = 45.0, 35.0

# Antenna keep-out zone (no components)
ANT_X0, ANT_Y0 = 112.5, 80.0
ANT_X1, ANT_Y1 = 132.5, 90.0

# Component approximate sizes (width, height in mm) for overlap detection
COMP_SIZES = {
    'J1':   (12.0, 8.5),  # USB-C receptacle
    'U1':   (6.5, 7.0),   # SOT-223 LDO
    'U3':   (10.0, 10.0), # TO-39 can
    'BZ1':  (12.0, 12.0), # 12mm buzzer
    'J2':   (10.0, 6.0),  # JST 4-pin
    'J3':   (2.6, 7.7),   # Pin header 1x3
    'SW1':  (6.0, 6.0),   # Tactile switch
    'SW2':  (6.0, 6.0),
    'LED1': (3.5, 3.5),   # WS2812B
    'Q1':   (3.0, 3.0),   # SOT-23
    'D1':   (1.6, 1.0),   # SOD-523
}
# Default size for 0402/0805 passives
DEFAULT_SIZE = (1.5, 1.0)

# ============================================================
# NETLIST (from schematic — defines which components connect)
# Each net is a list of (ref, pad) tuples
# ============================================================
NETLIST = {
    '+5V': [('J1', 'VBUS'), ('D1', '1'), ('C1', '1')],
    'GND': [('J1', 'GND'), ('R1', '2'), ('R2', '2'), ('D1', '2'),
            ('C1', '2'), ('U1', '1'), ('C2', '2'), ('C3', '2'),
            ('C4', '2'), ('C5', '2'), ('C6', '2'), ('U3', 'VSS'),
            ('C7', '2'), ('LED1', 'VSS'), ('C8', '2'), ('Q1', 'E'),
            ('SW1', '2'), ('SW2', '2'), ('J2', '2'), ('J3', '3')],
    '+3V3': [('U1', 'VO'), ('C3', '1'), ('C4', '1'), ('C5', '1'),
             ('C6', '1'), ('U3', 'VDD'), ('C7', '1'), ('R5', '1'),
             ('R6', '1'), ('LED1', 'VDD'), ('C8', '1'), ('BZ1', '+'),
             ('R3', '1'), ('R4', '1'), ('J2', '1')],
    'VBUS_to_LDO': [('C1', '1'), ('C2', '1'), ('U1', 'VI'), ('D1', '1')],
    'CC1': [('J1', 'CC1'), ('R1', '1')],
    'CC2': [('J1', 'CC2'), ('R2', '1')],
    'I2C0_SDA': [('U3', 'SDA'), ('R5', '2')],
    'I2C0_SCL': [('U3', 'SCL'), ('R6', '2')],
    'I2C1_SDA': [('J2', '3')],
    'I2C1_SCL': [('J2', '4')],
    'GPIO_LED': [('LED1', 'DIN')],
    'GPIO_BUZZER': [('R7', '1')],
    'BUZ_BASE': [('R7', '2'), ('Q1', 'B')],
    'BUZ_DRIVE': [('Q1', 'C'), ('BZ1', '-')],
    'EN': [('R3', '2'), ('SW1', '1')],
    'GPIO0': [('R4', '2'), ('SW2', '1')],
    'UART_TX': [('J3', '1')],
    'UART_RX': [('J3', '2')],
}

# ============================================================
# PLACEMENT CONSTRAINTS
# ============================================================
# Fixed components (won't move during optimization)
FIXED = {'J1'}  # USB-C must be at left edge

# Soft constraints: preferred zones (ref -> (x_min, y_min, x_max, y_max))
ZONES = {
    'J1':   (BRD_X0, BRD_Y0 + 10, BRD_X0 + 8, BRD_Y1 - 10),   # Left edge
    'U3':   (BRD_X1 - 10, BRD_Y0 + 10, BRD_X1, BRD_Y1 - 10),   # Right edge
    'SW1':  (BRD_X0, BRD_Y1 - 8, BRD_X0 + 15, BRD_Y1),          # Bottom-left
    'SW2':  (BRD_X0 + 8, BRD_Y1 - 8, BRD_X0 + 20, BRD_Y1),     # Bottom-left
    'LED1': (BRD_X0 + 15, BRD_Y1 - 8, BRD_X1 - 15, BRD_Y1),    # Bottom center
    'BZ1':  (BRD_X0 + 20, BRD_Y1 - 15, BRD_X1, BRD_Y1),        # Bottom-right
    'J2':   (BRD_X1 - 12, BRD_Y0, BRD_X1, BRD_Y0 + 12),        # Top-right
    'J3':   (BRD_X1 - 10, BRD_Y1 - 12, BRD_X1, BRD_Y1),        # Bottom-right
}

# Thermal isolation: U3 (sensor) must be far from U1 (LDO) and ESP32 area
THERMAL_PAIRS = [('U3', 'U1', 15.0)]  # (ref_a, ref_b, min_distance_mm)


def get_size(ref):
    return COMP_SIZES.get(ref, DEFAULT_SIZE)


def load_board(path):
    """Load board and return dict of ref -> (x, y, angle)."""
    board = Board.from_file(path)
    components = {}
    for fp in board.footprints:
        ref = fp.properties.get('Reference', '?')
        x = fp.position.X if fp.position else 0
        y = fp.position.Y if fp.position else 0
        angle = fp.position.angle if fp.position and fp.position.angle else 0
        components[ref] = [x, y, angle]
    return components, board


def save_board(board, components, path):
    """Update board footprint positions from components dict and save."""
    for fp in board.footprints:
        ref = fp.properties.get('Reference', '?')
        if ref in components:
            x, y, angle = components[ref]
            fp.position.X = x
            fp.position.Y = y
            if fp.position.angle is not None:
                fp.position.angle = angle
    board.to_file(path)


def wirelength(components):
    """Calculate total Manhattan wirelength across all nets."""
    total = 0
    for net_name, pins in NETLIST.items():
        refs = [p[0] for p in pins if p[0] in components]
        if len(refs) < 2:
            continue
        # Half-perimeter wirelength (HPWL) — standard metric
        xs = [components[r][0] for r in refs]
        ys = [components[r][1] for r in refs]
        total += (max(xs) - min(xs)) + (max(ys) - min(ys))
    return total


def boundary_violations(components):
    """Count components outside board boundary."""
    violations = 0
    for ref, (x, y, _) in components.items():
        w, h = get_size(ref)
        hw, hh = w / 2, h / 2
        if x - hw < BRD_X0 or x + hw > BRD_X1 or y - hh < BRD_Y0 or y + hh > BRD_Y1:
            violations += 1
    return violations


def keepout_violations(components):
    """Count components in antenna keep-out zone."""
    violations = 0
    for ref, (x, y, _) in components.items():
        if ref in ('J1',):  # USB-C is far left, skip
            continue
        if ANT_X0 < x < ANT_X1 and ANT_Y0 < y < ANT_Y1:
            violations += 1
    return violations


def overlap_count(components):
    """Count overlapping component pairs."""
    refs = list(components.keys())
    overlaps = 0
    for i in range(len(refs)):
        for j in range(i + 1, len(refs)):
            r1, r2 = refs[i], refs[j]
            x1, y1, _ = components[r1]
            x2, y2, _ = components[r2]
            w1, h1 = get_size(r1)
            w2, h2 = get_size(r2)
            # Check bounding box overlap with 0.5mm clearance
            gap = 0.5
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            min_dx = (w1 + w2) / 2 + gap
            min_dy = (h1 + h2) / 2 + gap
            if dx < min_dx and dy < min_dy:
                overlaps += 1
    return overlaps


def zone_penalty(components):
    """Penalty for components outside their preferred zones."""
    penalty = 0
    for ref, (zx0, zy0, zx1, zy1) in ZONES.items():
        if ref not in components:
            continue
        x, y, _ = components[ref]
        # Distance from zone center
        cx = (zx0 + zx1) / 2
        cy = (zy0 + zy1) / 2
        dx = max(0, abs(x - cx) - (zx1 - zx0) / 2)
        dy = max(0, abs(y - cy) - (zy1 - zy0) / 2)
        penalty += dx + dy
    return penalty


def thermal_penalty(components):
    """Penalty for thermal-sensitive components too close together."""
    penalty = 0
    for ref_a, ref_b, min_dist in THERMAL_PAIRS:
        if ref_a not in components or ref_b not in components:
            continue
        xa, ya, _ = components[ref_a]
        xb, yb, _ = components[ref_b]
        dist = math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
        if dist < min_dist:
            penalty += (min_dist - dist) * 10
    return penalty


def total_cost(components):
    """Combined cost function."""
    wl = wirelength(components)
    bv = boundary_violations(components)
    kv = keepout_violations(components)
    ov = overlap_count(components)
    zp = zone_penalty(components)
    tp = thermal_penalty(components)
    return wl + 1000 * bv + 1000 * kv + 500 * ov + 5 * zp + tp


def anneal(components, iterations=5000, temp=100.0, cooling=0.995, seed=42):
    """Simulated annealing placement optimization."""
    random.seed(seed)
    best = copy.deepcopy(components)
    best_cost = total_cost(best)
    current = copy.deepcopy(components)
    current_cost = best_cost

    movable = [r for r in components if r not in FIXED]

    accepted = 0
    improved = 0

    print(f"\n{'Pass':>6} {'Temp':>8} {'Cost':>10} {'Best':>10} {'WL':>8} {'OL':>4} {'BV':>4} {'KV':>4}")
    print("-" * 65)

    for i in range(iterations):
        # Pick random component
        ref = random.choice(movable)
        old_x, old_y, old_a = current[ref]

        # Random perturbation (smaller as temp decreases)
        scale = max(1.0, temp / 20)
        dx = random.gauss(0, scale)
        dy = random.gauss(0, scale)

        # Apply move
        current[ref] = [old_x + dx, old_y + dy, old_a]

        # Evaluate
        new_cost = total_cost(current)
        delta = new_cost - current_cost

        # Accept or reject (Metropolis criterion)
        if delta < 0 or random.random() < math.exp(-delta / max(temp, 0.01)):
            current_cost = new_cost
            accepted += 1
            if new_cost < best_cost:
                best = copy.deepcopy(current)
                best_cost = new_cost
                improved += 1
        else:
            # Revert
            current[ref] = [old_x, old_y, old_a]

        # Cool down
        temp *= cooling

        # Progress report
        if (i + 1) % (iterations // 10) == 0:
            wl = wirelength(current)
            ov = overlap_count(current)
            bv = boundary_violations(current)
            kv = keepout_violations(current)
            print(f"{i+1:6d} {temp:8.2f} {current_cost:10.1f} {best_cost:10.1f} {wl:8.1f} {ov:4d} {bv:4d} {kv:4d}")

    return best, best_cost, accepted, improved


def main():
    parser = argparse.ArgumentParser(description='StoveIQ PCB Placement Optimizer')
    parser.add_argument('--iterations', type=int, default=5000, help='SA iterations')
    parser.add_argument('--temp', type=float, default=100.0, help='Initial temperature')
    parser.add_argument('--cooling', type=float, default=0.995, help='Cooling rate')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--input', default='stoveiq.kicad_pcb', help='Input PCB file')
    parser.add_argument('--output', default=None, help='Output PCB file (default: overwrite input)')
    args = parser.parse_args()

    output = args.output or args.input

    print("=" * 65)
    print("StoveIQ PCB Placement Optimizer")
    print("=" * 65)

    # Load board
    components, board = load_board(args.input)
    print(f"Loaded {len(components)} components from {args.input}")

    # Initial cost
    init_cost = total_cost(components)
    init_wl = wirelength(components)
    init_ov = overlap_count(components)
    print(f"\nInitial state:")
    print(f"  Wirelength:  {init_wl:.1f} mm")
    print(f"  Overlaps:    {init_ov}")
    print(f"  Boundary:    {boundary_violations(components)}")
    print(f"  Keep-out:    {keepout_violations(components)}")
    print(f"  Zone penalty:{zone_penalty(components):.1f}")
    print(f"  Thermal:     {thermal_penalty(components):.1f}")
    print(f"  Total cost:  {init_cost:.1f}")

    # Optimize
    print(f"\nRunning simulated annealing ({args.iterations} iterations)...")
    best, best_cost, accepted, improved = anneal(
        components,
        iterations=args.iterations,
        temp=args.temp,
        cooling=args.cooling,
        seed=args.seed
    )

    # Results
    final_wl = wirelength(best)
    final_ov = overlap_count(best)
    print(f"\nOptimized state:")
    print(f"  Wirelength:  {final_wl:.1f} mm ({final_wl - init_wl:+.1f} mm, {(final_wl/init_wl - 1)*100:+.1f}%)")
    print(f"  Overlaps:    {final_ov}")
    print(f"  Boundary:    {boundary_violations(best)}")
    print(f"  Keep-out:    {keepout_violations(best)}")
    print(f"  Zone penalty:{zone_penalty(best):.1f}")
    print(f"  Thermal:     {thermal_penalty(best):.1f}")
    print(f"  Total cost:  {best_cost:.1f} ({best_cost - init_cost:+.1f})")
    print(f"  Accepted:    {accepted}/{args.iterations} ({accepted/args.iterations*100:.1f}%)")
    print(f"  Improved:    {improved}")

    # Show placement changes
    print(f"\nPlacement changes:")
    for ref in sorted(best.keys()):
        ox, oy, _ = components[ref]
        nx, ny, _ = best[ref]
        if abs(ox - nx) > 0.1 or abs(oy - ny) > 0.1:
            print(f"  {ref:6s}: ({ox:.1f}, {oy:.1f}) -> ({nx:.1f}, {ny:.1f})  Δ=({nx-ox:+.1f}, {ny-oy:+.1f})")

    # Save
    save_board(board, best, output)
    print(f"\nSaved optimized board to {output}")


if __name__ == '__main__':
    main()
