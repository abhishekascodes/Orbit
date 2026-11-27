"""
quick audio verification script for orbit-10
tests the respeaker mic array input levels and plays a test tone
through the tpa3116d2 amp to check for distortion and rattles
"""

import sys
import time
import math
import struct
import wave
import argparse

try:
    import sounddevice as sd
    import numpy as np
    HAVE_SOUNDDEVICE = True
except ImportError:
    HAVE_SOUNDDEVICE = False

def list_devices():
    print("=== audio devices detected ===")
    if not HAVE_SOUNDDEVICE:
        print("sounddevice not installed. run: pip install sounddevice numpy")
        return
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        in_ch = dev['max_input_channels']
        out_ch = dev['max_output_channels']
        print(f"[{i:2d}] {dev['name']} (in: {in_ch}, out: {out_ch}, rate: {dev['default_samplerate']:.0f}Hz)")
    print()

def generate_sine_sweep(duration=2.0, sample_rate=44100, f_start=150.0, f_end=3500.0):
    # frequency sweep from 150hz to 3.5khz to check speaker rattle
    n_samples = int(duration * sample_rate)
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        # linear sweep
        freq = f_start + (f_end - f_start) * (t / duration)
        val = 0.5 * math.sin(2.0 * math.pi * freq * t)
        samples.append(val)
    return samples

def test_speaker(device_id=None):
    print("running speaker sweep (150hz -> 3.5khz)...")
    if not HAVE_SOUNDDEVICE:
        print("error: sounddevice required for live playback")
        return

    sample_rate = 44100
    sweep = generate_sine_sweep(duration=2.5, sample_rate=sample_rate)
    audio_data = np.array(sweep, dtype=np.float32)

    try:
        sd.play(audio_data, samplerate=sample_rate, device=device_id)
        sd.wait()
        print("speaker sweep finished. listen for any plastic enclosure rattles.")
    except Exception as e:
        print(f"speaker test failed: {e}")

def test_mic(device_id=None, duration=3.0):
    print(f"recording {duration:.1f}s from mic array to check noise floor and clipping...")
    if not HAVE_SOUNDDEVICE:
        print("error: sounddevice required for mic capture")
        return

    sample_rate = 16000
    try:
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, device=device_id, dtype='float32')
        sd.wait()

        # calculate rms and peak
        rms = np.sqrt(np.mean(recording**2))
        peak = np.max(np.abs(recording))
        db_rms = 20 * math.log10(rms + 1e-9)
        db_peak = 20 * math.log10(peak + 1e-9)

        print(f"capture complete: peak = {db_peak:.1f} dBFS, rms = {db_rms:.1f} dBFS")
        if db_peak > -1.0:
            print("warning: signal clipped! lower preamp gain in alsamixer")
        elif db_rms < -50.0:
            print("signal very low. check if mic mute switch is on or mic array is selected")
        else:
            print("audio levels healthy, mic picked up clean room signal")
    except Exception as e:
        print(f"mic test failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="orbit audio bench test")
    parser.add_argument("--list", action="store_true", help="list audio devices")
    parser.add_argument("--speaker", action="store_true", help="run speaker sweep")
    parser.add_argument("--mic", action="store_true", help="record test sample from mic")
    parser.add_argument("--device", type=int, default=None, help="specific device index")
    args = parser.parse_args()

    if args.list:
        list_devices()
    elif args.speaker:
        test_speaker(args.device)
    elif args.mic:
        test_mic(args.device)
    else:
        list_devices()
        print("usage: python audio_test.py --speaker OR --mic")
