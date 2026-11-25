# Orbit

Hey, I'm Abhishek. Building my own desk assistant / smart display instead of buying an Echo Show.

Tired of commercial smart displays throwing ads on your desk and locking everything to the cloud, so I'm building one on a Pi 5 with actual speakers, a 10.1" screen, and local voice/AI stuff. Also planning to link it over LAN to my PC for heavier models when I'm at my desk.

Just getting started today - put together a rough parts list and hacked together a quick dark-mode UI test in Python to see how the clock and status ring look at 16:10.

Rough idea so far:
- Pi 5 (16GB) + Dual M.2 HAT (NVMe + AI module)
- 10.1" 1080p IPS touch display
- Two 40mm speakers + passive radiators on a 20V amp
- 6-mic circular array + physical switch to cut camera and mic power
- mmWave presence sensor + BME680 for room temp/VOC
- Rotary knob on top for volume + RGBW ring around the bezel

Files so far:
- `hardware/parts.md` - rough parts shortlist and power notes
- `firmware/screen_test.py` - basic dark mode UI layout test
