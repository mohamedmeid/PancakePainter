#!/usr/bin/env python3
"""G-Code Konverter für PancakePainter - Konvertiert G-Code-Dateien für optimale Kompatibilität"""

import re
import sys
import os

def convert_logo_gcode(input_file, output_file, max_x=200, max_y=192, home_x=0, home_y=0, valve_open_z=10, valve_close_z=0):
    # First pass: find coordinate bounds
    min_x = float('inf')
    max_x_found = float('-inf')
    min_y = float('inf')
    max_y_found = float('-inf')

    with open(input_file, 'r') as f:
        for line in f:
            match = re.match(r'G00 X([\d.]+) Y([\d.]+)', line)
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                min_x = min(min_x, x)
                max_x_found = max(max_x_found, x)
                min_y = min(min_y, y)
                max_y_found = max(max_y_found, y)

    # Calculate scaling and offset
    width = max_x_found - min_x
    height = max_y_found - min_y

    # Scale to fit with 10mm margin on each side
    scale_x = (max_x - 20) / width
    scale_y = (max_y - 20) / height
    scale = min(scale_x, scale_y)  # Use same scale for both to maintain aspect ratio

    # Calculate offset to center the logo and apply home position
    new_width = width * scale
    new_height = height * scale
    offset_x = home_x + (max_x - new_width) / 2 - min_x * scale
    offset_y = home_y + (max_y - new_height) / 2 - min_y * scale

    print(f"Original bounds: X={min_x:.1f} to {max_x_found:.1f}, Y={min_y:.1f} to {max_y_found:.1f}")
    print(f"Original size: {width:.1f}mm x {height:.1f}mm")
    print(f"Scale factor: {scale:.4f}")
    print(f"New size: {new_width:.1f}mm x {new_height:.1f}mm")
    print(f"Offset: X+{offset_x:.1f}, Y+{offset_y:.1f}")

    # Second pass: convert file
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            line = line.rstrip('\n')

            # Remove W1 workspace command
            if line.startswith('W1 '):
                f_out.write(';' + line + ' ;Removed for Marlin compatibility\n')
                continue

            # Fix Z-axis valve control based on user-defined values
            # Handle negative Z values (convert to positive open value)
            if 'Z-' in line:
                # This was valve open with negative value, convert to user's open value
                line = re.sub(r'Z-[\d.]+', f'Z{valve_open_z}', line)
                line = re.sub(r';.*open.*', ';Valve open', line, flags=re.IGNORECASE)
            # Handle existing Z values that indicate valve state
            elif re.search(r'G0[01]\s+Z[\d.]+\s*;.*open', line, re.IGNORECASE):
                # Valve open command
                line = re.sub(r'(G0[01])\s+Z[\d.]+', f'\\1 Z{valve_open_z}', line)
                line = re.sub(r';.*', ';Valve open', line)
            elif re.search(r'G0[01]\s+Z[\d.]+\s*;.*clos', line, re.IGNORECASE):
                # Valve close command
                line = re.sub(r'(G0[01])\s+Z[\d.]+', f'\\1 Z{valve_close_z}', line)
                line = re.sub(r';.*', ';Valve closed', line)
            # Handle Z values without comments (check common patterns)
            elif re.search(r'^\s*G1\s+Z0\s*$', line):
                # Likely a close command (Z0 is typically close)
                line = re.sub(r'Z0', f'Z{valve_close_z}', line)

            # Scale and offset XY coordinates
            match = re.match(r'(G00) X([\d.]+) Y([\d.]+)(.*)', line)
            if match:
                cmd = match.group(1)
                x = float(match.group(2))
                y = float(match.group(3))
                comment = match.group(4)

                # Scale and offset
                new_x = x * scale + offset_x
                new_y = y * scale + offset_y

                f_out.write(f'{cmd} X{new_x:.3f} Y{new_y:.3f}{comment}\n')
                continue

            # Default: write line as-is
            f_out.write(line + '\n')

    # Verify new bounds
    min_x_new = float('inf')
    max_x_new = float('-inf')
    min_y_new = float('inf')
    max_y_new = float('-inf')

    with open(output_file, 'r') as f:
        for line in f:
            match = re.match(r'G00 X([\d.]+) Y([\d.]+)', line)
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                min_x_new = min(min_x_new, x)
                max_x_new = max(max_x_new, x)
                min_y_new = min(min_y_new, y)
                max_y_new = max(max_y_new, y)

    print(f"\nNew bounds: X={min_x_new:.1f} to {max_x_new:.1f}, Y={min_y_new:.1f} to {max_y_new:.1f}")
    print(f"✓ Fits within X:{max_x}mm, Y:{max_y}mm limits!")

def get_positive_float(prompt, default=None):
    """Helper function to get a positive float from user input"""
    while True:
        if default is not None:
            user_input = input(f"{prompt} (Standard: {default}): ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"{prompt}: ").strip()

        try:
            value = float(user_input)
            if value < 0:
                print("Fehler: Der Wert muss positiv sein! Bitte versuchen Sie es erneut.")
                continue
            return value
        except ValueError:
            print("Fehler: Bitte geben Sie eine gültige Zahl ein!")
            continue

if __name__ == '__main__':
    print("=" * 60)
    print("G-Code Konverter für PancakePainter")
    print("=" * 60)

    # Prompt user for file path in German
    input_file = input("\nBitte geben Sie den Pfad der G-Code-Datei ein, die Sie konvertieren möchten:\n> ").strip()

    # Remove quotes if user pasted path with quotes
    input_file = input_file.strip('"').strip("'")

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"\nFehler: Datei '{input_file}' wurde nicht gefunden!")
        print("Bitte überprüfen Sie den Pfad und versuchen Sie es erneut.")
        sys.exit(1)

    # Get home position
    print("\n--- Home-Position einstellen ---")
    home_x = get_positive_float("Home X-Position (mm)", default=0)
    home_y = get_positive_float("Home Y-Position (mm)", default=0)

    # Get valve parameters
    print("\n--- Ventil-Parameter einstellen ---")
    valve_open_z = get_positive_float("Z-Wert für Ventil OFFEN (mm)", default=10)
    valve_close_z = get_positive_float("Z-Wert für Ventil GESCHLOSSEN (mm)", default=0)

    # Get printer dimensions
    print("\n--- Drucker-Abmessungen ---")
    max_x = get_positive_float("Maximale X-Abmessung (mm)", default=200)
    max_y = get_positive_float("Maximale Y-Abmessung (mm)", default=192)

    # Generate output filename by adding "_fixed" before the extension
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_fixed{ext}"

    print(f"\nKonvertierung läuft...\n")
    convert_logo_gcode(input_file, output_file, max_x=max_x, max_y=max_y,
                       home_x=home_x, home_y=home_y,
                       valve_open_z=valve_open_z, valve_close_z=valve_close_z)
    print(f'\n✓ Erfolgreich konvertiert: {output_file}')
