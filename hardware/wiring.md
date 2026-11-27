# Wiring Harness and Pinout Notes

Notes on how the power rails, audio lines, and sensor buses connect together inside the chassis.

## Power routing (20V PD and 5V Buck)
- **Main Input**: USB-C receptacle on the rear shell connects to the CH224K trigger board. Configured with a 6.8k resistor between CFG1 and GND to negotiate 20V @ 3.25A (65W) from my laptop GaN brick.
- **20V Audio Rail**: Heavy 18 AWG silicone wires run straight from the CH224K output pads to the TPA3116D2 Class-D amplifier power terminals. Added a 470uF 35V low-ESR electrolytic capacitor across the amp input pads to smooth out sudden bass transients.
- **5V Logic Rail**: A second pair of 18 AWG wires branches off the 20V pads into the MP2315 buck converter. The buck drops 20V down to a stable 5.1V (5A max).
- **Powering the Pi 5**: Output of the buck converter runs directly to GPIO Pin 2 (5V) and Pin 6 (GND) on the Pi 40-pin header. Running power through the header pins instead of using the USB-C port saves internal depth and lets me keep wiring tucked underneath the board.

## Grounding rules (avoiding ground loops)
- Running a single star ground point right at the negative output of the CH224K.
- The high-current speaker return currents go straight back to the 20V ground terminal. They do not share return wires with the sensitive microphone ground or I2C sensor lines, which keeps speaker buzz and switching whine out of the audio.

## 40-pin GPIO pinout map
- **BME680 (Air Quality / Temp)**:
  - VCC -> 3.3V (Pin 1)
  - GND -> GND (Pin 9)
  - SDA -> GPIO 2 (Pin 3)
  - SCL -> GPIO 3 (Pin 5)
  - Pulled up to 3.3V with internal resistors.

- **LD2410 (24GHz mmWave Radar)**:
  - VCC -> 5V (Pin 4)
  - GND -> GND (Pin 14)
  - TX -> GPIO 15 / RXD0 (Pin 10)
  - RX -> GPIO 14 / TXD0 (Pin 8)
  - Serial connection runs at 256,000 baud for fast presence detection.

- **EC11 Rotary Encoder (Volume & Navigation)**:
  - Channel A -> GPIO 17 (Pin 11)
  - Channel B -> GPIO 27 (Pin 13)
  - Push Switch -> GPIO 22 (Pin 15)
  - Common -> GND (Pin 20)
  - Using internal pull-ups in software.

- **Audio Amp Controls**:
  - MUTE -> GPIO 4 (Pin 7) - pulled low to mute during boot so there is no power-on pop through the speakers.
  - FAULT -> GPIO 24 (Pin 18) - reads high if the TPA3116 overheats or shorts.

- **Physical Privacy Switch**:
  - SPDT slider switch mounted on the top bezel.
  - One pole physically interrupts the 3.3V power lead to the Camera Module 3.
  - Second pole interrupts the 5V USB power lead to the ReSpeaker mic array.
  - Aux pin runs to GPIO 23 (Pin 16) as a status line so software knows when hardware privacy mode is engaged.
