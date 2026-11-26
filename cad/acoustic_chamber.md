# Acoustic Sub-Enclosure and Speaker Baffle

Calculated the internal box volume and baffle cutouts for the bottom audio section so the speakers actually have bass.

## Why a separate sealed sub-enclosure?
Normal smart speakers sound like tin cans because they either use tiny 1-watt phone speakers or throw drivers into an open plastic shell with zero acoustic sealing.

With two passive radiators, the box has to be 100% airtight:
1. Passive radiators work like an acoustic mass-spring system driven by internal air pressure waves from the active drivers. If there is even a 1mm pinhole air leak, internal pressure drops, the passive radiators stop moving, and you lose all low-end.
2. An open cavity would blow pressurized air pulses straight into the Pi 5 heatsink and shake ribbon cables loose.
3. Air movement inside the chassis would vibrate the ReSpeaker microphones on the top deck and cause audio feedback loops.

## Box volume math (Vb target = ~300cc)
- Active drivers: 2x Dayton DMA45-4 (40mm full-range, 4 ohm, 20W peak, Fs = 130Hz)
- Passive radiators: 2x Dayton ND65-PR (50mm tuned disc radiators)

Internal cavity sizing:
- Internal width: 226.0mm
- Internal height: 34.0mm
- Internal depth: 42.0mm
- Gross internal volume: 226 * 34 * 42 = 322,728 mm3 (~322.7 cc)
- Subtracting driver magnet / frame displacement: ~11 cc per driver (~22 cc total)
- Net acoustic volume (Vb): ~300.7 cc

With 300cc net volume, the dual 50mm passive radiators tune the box down from the raw 130Hz driver resonance to around ~85Hz. That is low enough to give deep, clean vocal presence and solid kick drum punch without muddy distortion.

## Baffle layout & cutouts
- Front baffle: Two 40.5mm circular cutouts spaced 140mm apart for good stereo separation across the 250mm front width.
- Screw pattern: 4x M2.5 mounting screw holes on a 46mm bolt circle diameter per driver.
- Bottom plate: Two 52.0mm cutouts on the bottom face firing downward toward the desk surface for the passive radiators. The 15mm clearance feet on the base give the radiators plenty of breathing room.
- Perimeter seal: Added a 1.5mm tongue-and-groove channel along the mating edge to seat a soft TPU/silicone gasket so the box is completely airtight when screwed down.
