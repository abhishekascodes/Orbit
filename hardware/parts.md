# Parts List (Rough)

Still checking prices and deciding on exact speaker driver sizes before finalizing the BOM.

Main compute:
- Raspberry Pi 5 (16GB) + active cooler
- Dual M.2 PCIe HAT (needs an onboard PCIe switch like the Pineberry Dual or Waveshare so SSD and AI module both work on the single lane)
- 500GB NVMe M.2 2280 SSD
- Hailo-8 M.2 AI module (for local wake word, whisper, and hand gestures)

Screen & sensors:
- Waveshare 10.1" 1080p IPS touch display (going with DSI ribbon so I don't have stiff HDMI cables cramming the case)
- Pi Camera Module 3 Wide
- LD2410 24GHz mmWave sensor (UART) to wake the display when I walk up to the desk
- BME680 breakout for temp / humidity / VOC
- EC11 rotary encoder with a heavy metal knob on top
- SK6812 RGBW LED strip around the bezel (picked RGBW over normal RGB so white notifications actually look warm)
- Physical SPDT slide switch to cut power to camera and mics completely

Audio:
- ReSpeaker 6-mic circular array (planning to mount on soft rubber grommets so speaker bass doesn't rattle the mics)
- TPA3116D2 2x20W Class-D amp
- 2x 40mm 4ohm full-range drivers (looking at Dayton DMA45-4) + 2x 50mm passive radiators

Power notes so I don't fry anything later:
Can't run a 2x20W speaker amp on 5V or the Pi will brown out and reset whenever volume goes up. Planning to use a CH224K USB-C PD trigger requesting 20V from a 65W charger. 20V feeds the amp straight, and a 20V to 5V 5A buck converter steps down cleanly for the Pi and screen.

Also remembering to keep the BME680 tucked near a bottom cold-air intake slot so internal Pi CPU heat doesn't skew the room temperature numbers by 10 degrees.
