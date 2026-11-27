# Audio Subsystem Bench Notes

Bench test results for the audio input array and speaker amplifier.

## Hardware setup
- **Microphone Array**: ReSpeaker 6-Mic Circular Array connected via internal USB header.
- **Power Amplifier**: TPA3116D2 2x50W stereo Class-D board running off the 20V PD rail.
- **Transducers**: Two 40mm 4-ohm 5W full-range drivers mounted in the sealed 300cc PETG sub-enclosure, paired with a rear 70mm passive bass radiator.
- **Audio Output**: PCM5102A I2S DAC connected to Pi 5 GPIO header (Pins 12, 35, 40 for BCLK, LRCK, DIN).

## ALSA device mapping (Raspberry Pi OS)
Listing devices with `aplay -l` and `arecord -l`:
- Capture: `hw:CARD=Array,DEV=0` (6-channel 16-bit 16kHz PCM stream).
- Playback: `hw:CARD=sndrpihifiberry,DEV=0` (stereo 24-bit 44.1kHz / 48kHz I2S stream).

In `~/.asoundrc`, set default capture to use channels 1-2 downmixed for testing, or raw multi-channel for beamforming experiments.

## Frequency sweep test (150Hz to 3.5kHz)
Ran the sweep generator script (`firmware/audio_test.py --speaker`):
- **150Hz to 250Hz**: Passive radiator visibly oscillates. Bass is punchy and doesn't sound like a tin can thanks to the sealed 300cc chamber.
- **500Hz to 2kHz**: Clean vocal range clarity. No obvious distortion at normal conversational listening levels (about 65 dBA measured at 1 meter).
- **Enclosure resonance test**: Found a slight buzz around 380Hz where the front display bezel made contact with the main chassis. Adding a thin 1mm strip of adhesive closed-cell EVA foam along the mounting lip eliminated the rattle completely.

## Noise floor and ground hum check
- Before star grounding: Sharing the 5V logic ground return with the 20V amp ground produced an audible high-pitched squeal whenever the Pi 5 CPU jumped between idle and load states.
- After star grounding: Moving the amp power and ground directly to the CH224K 20V pads lowered the idle noise floor significantly. Mic capture test (`--mic`) reports an idle room noise floor around -48 dBFS with zero 50Hz mains hum or buck converter whine.

## Power rail stability under load
- Monitored the 20V rail with an oscilloscope during maximum volume bursts.
- Rail sag remained under 0.25V thanks to the 470uF low-ESR buffer capacitor placed right at the amp power terminals.
- MP2315 5V buck converter stayed cool to the touch and maintained a solid 5.12V output to the Pi 5 header with no thermal throttling or undervoltage warnings in `dmesg`.
