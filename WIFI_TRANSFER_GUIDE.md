# WiFi Transfer Guide - For Your Laptop (macOS)

This guide shows how to transfer G-code from PancakePainter to Raspberry Pi via WiFi.

## What You Can Do NOW (Before Getting the Pi)

### 1. Test PancakePainter Export

```bash
# Run the app
cd /Users/mohamedeid/Documents/GitHub/PancakePainter
npm start
```

1. Create a test design (draw something simple)
2. Go to: `File > Export for printing...`
3. Save as: `test_pancake.gcode` (remember the location!)
4. Verify the file was created

### 2. Install Transfer Software (Choose One)

**Option A: Use built-in macOS tools** (Recommended - No installation!)
```bash
# Test if SCP works
which scp
# Should show: /usr/bin/scp

# You're ready!
```

**Option B: Install FileZilla** (GUI - Easier for beginners)
```bash
brew install --cask filezilla
```

**Option C: Install Cyberduck** (Mac-native - Pretty UI)
```bash
brew install --cask cyberduck
```

### 3. Send Setup Guide to Your Friend

Share this file with your friend who has the Raspberry Pi:
```
RASPBERRY_PI_SETUP.md
```

They need to:
- Enable SSH
- Find the Pi's IP address
- Set up the G-code directory
- Connect the printer
- Share connection details with you

---

## What You Need from Your Friend

Ask them to send you:

```
📋 Raspberry Pi Info:
1. IP Address: _______________
2. Username: _______________
3. Password: _______________
4. G-code directory path: /home/pi/gcode
5. WiFi network name: _______________
6. Are we on the same WiFi? Yes/No
```

---

## Once You Have the Pi Info

### Method 1: Use the Transfer Script (Easiest!)

I've created a script for you: `transfer_gcode.sh`

**Step 1: Configure the script**
```bash
# Edit the script and update these lines:
nano transfer_gcode.sh

# Change these values:
PI_IP="192.168.1.100"        # ← Put your friend's Pi IP here
PI_USER="pi"                  # ← Usually 'pi'
PI_GCODE_DIR="/home/pi/gcode" # ← Ask your friend for this path
```

**Step 2: Use it!**
```bash
# Transfer any G-code file
./transfer_gcode.sh ~/Desktop/pancake_design.gcode

# Or drag and drop:
./transfer_gcode.sh /path/to/your/file.gcode
```

That's it! The script will:
- ✅ Test connection to Pi
- ✅ Transfer your G-code file
- ✅ Show you where it was saved
- ✅ List all files on the Pi

---

### Method 2: Manual SCP Command

If you prefer to do it manually:

```bash
# Basic syntax:
scp /path/to/local/file.gcode pi@<PI_IP>:/home/pi/gcode/

# Example:
scp ~/Desktop/pancake.gcode pi@192.168.1.100:/home/pi/gcode/

# It will ask for password, then transfer
```

---

### Method 3: Using FileZilla (GUI)

1. Open FileZilla
2. Enter connection details:
   - Host: `sftp://192.168.1.100` (your Pi's IP)
   - Username: `pi`
   - Password: (what your friend gave you)
   - Port: `22`
3. Click "Quickconnect"
4. Drag and drop G-code files from left (your Mac) to right (Pi)

---

### Method 4: Using Cyberduck (GUI)

1. Open Cyberduck
2. Click "Open Connection"
3. Select "SFTP (SSH File Transfer Protocol)"
4. Enter:
   - Server: `192.168.1.100` (your Pi's IP)
   - Username: `pi`
   - Password: (what your friend gave you)
5. Connect and drag/drop files

---

## Complete Workflow: Design → Print

```
1. PancakePainter (Your Laptop)
   ↓
   Create design → Export G-code → Save file

2. Transfer via WiFi
   ↓
   Run: ./transfer_gcode.sh pancake.gcode

3. Raspberry Pi
   ↓
   File arrives in /home/pi/gcode/

4. Print
   ↓
   Your friend runs: ./print_gcode.sh pancake.gcode
   OR uses OctoPrint web interface

5. Pancake! 🥞
```

---

## Testing Without the Pi (Practice Mode)

You can practice the workflow without the Pi by transferring to another Mac:

```bash
# Start SSH on your Mac (if not already running)
sudo systemsetup -setremotelogin on

# Get your Mac's IP
ifconfig | grep "inet " | grep -v 127.0.0.1

# Test transfer to yourself
scp ~/Desktop/test.gcode yourusername@your-mac-ip:~/Desktop/test_transferred.gcode

# Enter your Mac password
```

This lets you practice the commands!

---

## Troubleshooting

### "Connection refused"
- Pi is not reachable
- Check if you're on the same WiFi
- Ping test: `ping <PI_IP>`

### "Permission denied"
- Wrong username/password
- Ask your friend to verify credentials

### "No route to host"
- Not on the same network
- Ask your friend for WiFi name and connect to it

### "Host key verification failed"
- Run: `ssh-keygen -R <PI_IP>`
- Try again

---

## Quick Reference

```bash
# Test connection
ping 192.168.1.100

# Transfer file (replace with your details)
./transfer_gcode.sh ~/Desktop/pancake.gcode

# Or manually:
scp ~/Desktop/pancake.gcode pi@192.168.1.100:/home/pi/gcode/

# SSH into Pi to check files
ssh pi@192.168.1.100
ls /home/pi/gcode/
```

---

## For Tomorrow's Demo

**Checklist:**
- [ ] PancakePainter exports G-code successfully
- [ ] You have Pi's IP address from your friend
- [ ] You're on the same WiFi network
- [ ] Transfer script is configured with correct IP
- [ ] Test transfer works
- [ ] Your friend can print the received file

**Practice run:**
1. Export a simple test design
2. Transfer to Pi
3. Have your friend confirm it arrived
4. Have them print it

Good luck! 🥞
