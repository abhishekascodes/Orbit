# quick python ui mockup to test layout and ring animations for the 10.1" screen

import math
import sys
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageTk

WIDTH = 1024
HEIGHT = 640  # 16:10 ratio scaled down from 1920x1200

BG_COLOR = (12, 16, 24)
CARD_COLOR = (20, 26, 38)
BORDER_COLOR = (38, 48, 68)
TEXT_MAIN = (240, 244, 248)
TEXT_DIM = (130, 145, 168)

STATE_COLORS = {
    "IDLE": (64, 156, 255),
    "LISTENING": (46, 229, 174),
    "SPEAKING": (255, 168, 64),
}


def load_font(size, bold=False):
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    win_font = Path("C:/Windows/Fonts") / name
    if win_font.exists():
        return ImageFont.truetype(str(win_font), size)
    linux_font = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    if linux_font.exists():
        return ImageFont.truetype(str(linux_font), size)
    return ImageFont.load_default()


def render_frame(t, state, font_big, font_med, font_sm):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # top status bar
    draw.text((44, 34), "ORBIT", fill=TEXT_MAIN, font=font_med)
    draw.ellipse((142, 42, 152, 52), fill=STATE_COLORS[state])
    draw.text((164, 36), state.lower(), fill=TEXT_DIM, font=font_sm)

    status_right = "LAN: connected   |   mic: live"
    draw.text((WIDTH - 310, 36), status_right, fill=TEXT_DIM, font=font_sm)
    draw.line([(44, 84), (WIDTH - 44, 84)], fill=BORDER_COLOR, width=1)

    # left side clock and ambient stats
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%A, %b %d")

    draw.text((48, 130), time_str, fill=TEXT_MAIN, font=font_big)
    draw.text((54, 275), date_str, fill=TEXT_DIM, font=font_med)

    # room sensor placeholder cards (bme680 + hailo status)
    cards = [
        ("ROOM", "24.4 C"),
        ("HUMIDITY", "54 %"),
        ("AI NODE", "Local"),
    ]
    x = 48
    for label, val in cards:
        draw.rounded_rectangle([x, 380, x + 150, 480], radius=12, fill=CARD_COLOR, outline=BORDER_COLOR, width=1)
        draw.text((x + 16, 398), label, fill=TEXT_DIM, font=font_sm)
        draw.text((x + 16, 430), val, fill=TEXT_MAIN, font=font_med)
        x += 166

    # bottom prompt hint
    draw.text((48, HEIGHT - 52), "space: cycle voice state    |    esc: quit", fill=(90, 102, 124), font=font_sm)

    # right side animated orbit ring
    cx, cy = 760, 340
    speed = 2.0 if state == "IDLE" else (5.0 if state == "LISTENING" else 8.0)
    amp = 8 if state == "IDLE" else (18 if state == "LISTENING" else 26)
    pulse = math.sin(t * speed) * amp

    color = STATE_COLORS[state]
    outer_r = 128 + pulse
    inner_r = 96 - (pulse * 0.4)

    # soft glow rings
    for i in range(4, 0, -1):
        r = outer_r + i * 7
        fade = tuple(int(c * (0.28 / i)) for c in color)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fade, width=3)

    # main orbit circle and inner core
    draw.ellipse([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r], outline=color, width=5)
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], outline=(55, 70, 96), width=2)

    # small orbiting dot around the ring
    angle = t * (0.8 if state == "IDLE" else 2.4)
    dot_x = cx + math.cos(angle) * outer_r
    dot_y = cy + math.sin(angle) * outer_r
    draw.ellipse([dot_x - 8, dot_y - 8, dot_x + 8, dot_y + 8], fill=TEXT_MAIN)

    return img


def main():
    font_big = load_font(120, bold=True)
    font_med = load_font(26, bold=True)
    font_sm = load_font(18, bold=False)

    # save snapshot directly without launching window when --snap is passed
    if "--snap" in sys.argv:
        frame = render_frame(1.4, "LISTENING", font_big, font_med, font_sm)
        out_path = Path(__file__).resolve().parent.parent / "docs" / "ui_test.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        frame.save(out_path)
        print(f"Saved preview to {out_path}")
        return

    root = tk.Tk()
    root.title("Orbit UI Prototype (10.1 inch scale)")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.resizable(False, False)

    label = tk.Label(root, bd=0)
    label.pack()

    states = ["IDLE", "LISTENING", "SPEAKING"]
    state_idx = [0]
    start_time = time.time()

    def toggle_state(event=None):
        state_idx[0] = (state_idx[0] + 1) % len(states)

    root.bind("<space>", toggle_state)
    root.bind("<Escape>", lambda e: root.destroy())

    def tick():
        t = time.time() - start_time
        frame = render_frame(t, states[state_idx[0]], font_big, font_med, font_sm)
        tk_img = ImageTk.PhotoImage(frame)
        label.configure(image=tk_img)
        label.image = tk_img
        root.after(33, tick)  # ~30 fps

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
