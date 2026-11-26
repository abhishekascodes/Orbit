# Orbit

Hey, I'm Abhishek. Building my own desk assistant / smart display instead of buying an Echo Show.

Tired of commercial smart displays throwing ads on your desk and locking everything to the cloud, so I'm building one on a Pi 5 with actual speakers, a 10.1" screen, and local voice/AI stuff. Also planning to link it over LAN to my PC for heavier models when I'm at my desk.

Just getting started: put together a rough parts list, tested a clean light-mode UI mockup in Python, and modeled the front bezel and acoustic sub-box in CAD.

Rough idea so far:
- Pi 5 (16GB) + Dual M.2 HAT (NVMe + AI module)
- 10.1" 1080p IPS touch display tilted at 65 degrees
- Two 40mm speakers + passive radiators on a 20V amp (sealed 300cc box)
- 6-mic circular array + physical switch to cut camera and mic power
- mmWave presence sensor + BME680 for room temp/VOC
- Rotary knob on top for volume + RGBW ring around the bezel

Files so far:
- `hardware/parts.md` - parts shortlist and power notes
- `cad/screen_frame.md` - 10.1" bezel measurements and 65 deg tilt angle
- `cad/acoustic_chamber.md` - sizing the sealed 300cc speaker box
- `cad/orbit_front_bezel.blend` - 3D model in Blender
- `firmware/screen_test.py` - clean light mode UI layout test
