# Raspberry Pi Setup Guide for PancakePainter

This guide is for the person setting up the Raspberry Pi to receive G-code files from PancakePainter via WiFi.

## Prerequisites
- Raspberry Pi with Raspbian/Raspberry Pi OS installed
- WiFi configured and connected
- 3D Pancake Printer connected via USB

---

## Step 1: Enable SSH (if not already enabled)

```bash
# On the Raspberry Pi, open terminal and run:
sudo raspi-config
```

1. Navigate to: `Interfacing Options` → `SSH`
2. Select `Yes` to enable SSH server
3. Reboot if required

**OR enable via desktop:**
- Preferences → Raspberry Pi Configuration → Interfaces → SSH: Enable

---

## Step 2: Find Your IP Address

```bash
hostname -I
```

Example output: `192.168.1.100 2001:db8::1`
The first address (e.g., `192.168.1.100`) is your local IP address.

**Share this IP address with your teammate!**

---

## Step 3: Create G-code Directory

```bash
# Create a directory to store incoming G-code files
mkdir -p /home/pi/gcode
cd /home/pi/gcode
```

---

## Step 4: Identify Printer Connection

```bash
# Find which USB port the printer is connected to
ls /dev/tty*

# Common options:
# - /dev/ttyUSB0
# - /dev/ttyACM0
# - /dev/ttyUSB1

# Test printer connection
sudo chmod 666 /dev/ttyUSB0  # Replace with your actual port
echo "G28" > /dev/ttyUSB0    # Should home the printer (test)
```

---

## Step 5: Install OctoPrint (Recommended - Optional)

OctoPrint provides a web interface for printer control:

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install python3-pip python3-dev python3-setuptools python3-venv git libyaml-dev build-essential -y

# Install OctoPrint
cd ~
mkdir OctoPrint && cd OctoPrint
python3 -m venv venv
source venv/bin/activate
pip install pip --upgrade
pip install octoprint

# Run OctoPrint
~/OctoPrint/venv/bin/octoprint serve
```

**Access OctoPrint:**
- Open browser: `http://192.168.1.100:5000` (use your actual IP)
- Complete setup wizard
- Add printer profile for PancakeBot

**Auto-start OctoPrint on boot:**
```bash
# Download systemd service file
wget https://github.com/OctoPrint/OctoPrint/raw/master/scripts/octoprint.service
sudo mv octoprint.service /etc/systemd/system/
sudo systemctl enable octoprint.service
sudo systemctl start octoprint.service
```

---

## Step 6: Alternative - Install PrintRun (Lightweight)

If you don't want OctoPrint:

```bash
sudo apt-get install printrun -y

# Test print command
cd /home/pi/gcode
python3 -m printrun.printcore /dev/ttyUSB0 115200 test_file.gcode
```

---

## Step 7: Create Simple Print Script

```bash
nano /home/pi/print_gcode.sh
```

Add this content:

```bash
#!/bin/bash
# Simple script to print G-code file

GCODE_FILE="$1"
PRINTER_PORT="/dev/ttyUSB0"  # Change to your printer port
BAUD_RATE="115200"            # Change if your printer uses different baud rate

if [ -z "$GCODE_FILE" ]; then
    echo "Usage: ./print_gcode.sh <gcode-file>"
    exit 1
fi

if [ ! -f "$GCODE_FILE" ]; then
    echo "Error: File not found: $GCODE_FILE"
    exit 1
fi

echo "Printing: $GCODE_FILE"
echo "Port: $PRINTER_PORT"
echo "Baud: $BAUD_RATE"

# Method 1: Direct serial (simple but no feedback)
cat "$GCODE_FILE" > "$PRINTER_PORT"

# Method 2: Using printcore (better, with feedback)
# python3 -m printrun.printcore "$PRINTER_PORT" "$BAUD_RATE" "$GCODE_FILE"
```

Make it executable:
```bash
chmod +x /home/pi/print_gcode.sh
```

---

## Step 8: Test Connection from Laptop

Have your teammate test the connection:

```bash
# From their Mac, they should run:
ping <your-pi-ip-address>
ssh pi@<your-pi-ip-address>
```

Default credentials:
- Username: `pi`
- Password: `raspberry` (change this for security!)

---

## Step 9: Security (Optional but Recommended)

```bash
# Change default password
passwd

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install firewall (optional)
sudo apt-get install ufw -y
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 5000/tcp  # OctoPrint (if using)
sudo ufw enable
```

---

## Information to Share with Your Teammate

Send them this information:

```
Raspberry Pi Connection Info:
- IP Address: [Run: hostname -I]
- Username: pi
- Password: [your password]
- G-code Directory: /home/pi/gcode
- Printer Port: /dev/ttyUSB0 (or your actual port)
- OctoPrint URL: http://[your-ip]:5000 (if installed)
- WiFi Network: [your network name]
```

---

## Quick Test

Once your teammate transfers a file, test printing:

```bash
# Check if file arrived
ls -l /home/pi/gcode/

# Print it
cd /home/pi/gcode
./print_gcode.sh test_pancake.gcode

# OR if using OctoPrint:
# Just use the web interface at http://[your-ip]:5000
```

---

## Troubleshooting

**Problem: Cannot connect via SSH**
```bash
sudo systemctl status ssh
sudo systemctl start ssh
```

**Problem: Permission denied on printer port**
```bash
sudo usermod -a -G dialout pi
sudo chmod 666 /dev/ttyUSB0
```

**Problem: Printer not responding**
```bash
# Check if port is correct
ls -l /dev/tty*

# Test serial communication
sudo apt-get install minicom
minicom -b 115200 -D /dev/ttyUSB0
```

---

Good luck with your demo! 🥞
