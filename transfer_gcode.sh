#!/bin/bash

# PancakePainter G-code Transfer Script
# This script transfers G-code files from your Mac to Raspberry Pi via WiFi

# ============================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================

# Raspberry Pi connection details (get from your friend)
PI_IP="192.168.1.100"           # Replace with actual Pi IP address
PI_USER="pi"                     # Usually 'pi'
PI_PASSWORD=""                   # Leave empty to prompt for password
PI_GCODE_DIR="/home/pi/gcode"    # Directory on Pi to store G-code files

# ============================================
# SCRIPT START
# ============================================

echo "🥞 PancakePainter G-code Transfer Tool"
echo "======================================"

# Check if file argument provided
if [ $# -eq 0 ]; then
    echo "❌ Error: No G-code file specified"
    echo ""
    echo "Usage: ./transfer_gcode.sh <path-to-gcode-file>"
    echo "Example: ./transfer_gcode.sh ~/Desktop/pancake.gcode"
    exit 1
fi

GCODE_FILE="$1"

# Check if file exists
if [ ! -f "$GCODE_FILE" ]; then
    echo "❌ Error: File not found: $GCODE_FILE"
    exit 1
fi

# Get filename
FILENAME=$(basename "$GCODE_FILE")

echo ""
echo "📁 File: $FILENAME"
echo "🎯 Target: $PI_USER@$PI_IP:$PI_GCODE_DIR/"
echo ""

# Test connection first
echo "🔍 Testing connection to Raspberry Pi..."
if ping -c 1 -W 2 "$PI_IP" > /dev/null 2>&1; then
    echo "✅ Raspberry Pi is reachable at $PI_IP"
else
    echo "❌ Cannot reach Raspberry Pi at $PI_IP"
    echo "   Check:"
    echo "   1. Is the Pi turned on?"
    echo "   2. Are you on the same WiFi network?"
    echo "   3. Is the IP address correct?"
    exit 1
fi

# Create directory on Pi if it doesn't exist
echo ""
echo "📂 Ensuring directory exists on Pi..."
ssh "$PI_USER@$PI_IP" "mkdir -p $PI_GCODE_DIR" 2>/dev/null

# Transfer file
echo ""
echo "🚀 Transferring G-code file..."
if scp "$GCODE_FILE" "$PI_USER@$PI_IP:$PI_GCODE_DIR/"; then
    echo ""
    echo "✅ SUCCESS! File transferred to Raspberry Pi"
    echo ""
    echo "📍 Location on Pi: $PI_GCODE_DIR/$FILENAME"
    echo ""
    echo "Next steps:"
    echo "1. SSH into Pi: ssh $PI_USER@$PI_IP"
    echo "2. Navigate to: cd $PI_GCODE_DIR"
    echo "3. Print the file (method depends on your printer setup)"
    echo ""
else
    echo ""
    echo "❌ Transfer failed"
    echo "   Check:"
    echo "   1. Is SSH enabled on the Pi?"
    echo "   2. Is the username/password correct?"
    echo "   3. Do you have permission to write to $PI_GCODE_DIR?"
    exit 1
fi

# Optional: List files on Pi
echo "📋 Files currently on Raspberry Pi:"
ssh "$PI_USER@$PI_IP" "ls -lh $PI_GCODE_DIR/" 2>/dev/null || echo "   (Could not list files)"
echo ""
