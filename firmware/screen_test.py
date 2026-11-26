# python ui layout test for the 10.1" screen
# using a clean, warm light mode like a braun / teenage engineering desk display

import math
import sys
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageTk

WIDTH = 1024
HEIGHT = 640  # 16:10 aspect ratio matching 1920x1200 panel

# Warm light mode palette
BG_COLOR = (244, 243, 239)        # warm off-white / paper
CARD_BG = (255, 255, 255)         # crisp white card
BORDER_COLOR = (218, 215, 208)    # tactile neutral border
TEXT_MAIN = (28, 32, 38)          # dark charcoal
TEXT_MUTED = (118, 124, 136)      # muted slate gray

STATE_COLORS = {
    "IDLE": (76, 92, 114),         # understated slate
    "LISTENING": (42, 128, 92),    # forest green
    "SPEAKING": (216, 96, 42),     # warm burnt orange
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


def render_frame(t, state, font_big, font_med, font_reg, font_sm):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Top header bar
    draw.text((48, 34), "ORBIT-10", fill=TEXT_MAIN, font=font_med)
    draw.ellipse((175, 42, 187, 54), fill=STATE_COLORS[state])
    draw.text((200, 37), state.lower(), fill=TEXT_MUTED, font=font_reg)

    draw.text((WIDTH - 290, 37), "wifi: 5ghz   |   mic: ready", fill=TEXT_MUTED, font=font_sm)
    draw.line([(48, 82), (WIDTH - 48, 82)], fill=BORDER_COLOR, width=1)

    # Big clock and day
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%A, %b %d")

    draw.text((48, 126), time_str, fill=TEXT_MAIN, font=font_big)
    draw.text((54, 275), date_str, fill=TEXT_MUTED, font=font_med)

    # Clean white telemetry cards (BME680 + AI status)
    cards = [
        ("DESK TEMP", "23.8 C"),
        ("HUMIDITY", "48 %"),
        ("VOICE CORE", "Local"),
    ]
    x = 48
    for label, val in cards:
        draw.rounded_rectangle([x, 380, x + 154, 482], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
        draw.text((x + 18, 400), label, fill=TEXT_MUTED, font=font_sm)
        draw.text((x + 18, 432), val, fill=TEXT_MAIN, font=font_med)
        x += 170

    draw.text((48, HEIGHT - 46), "space: toggle state   |   esc: exit", fill=TEXT_MUTED, font=font_sm)

    # Right side: clean geometric orbit dial (no blurry neon glow)
    cx, cy = 760, 340
    color = STATE_COLORS[state]
    pulse = math.sin(t * 4.0) * (14 if state == "SPEAKING" else 8)
    outer_r = 130 + pulse
    inner_r = 92

    # Clean geometric concentric rings with crisp line weights
    draw.ellipse([cx - outer_r - 18, cy - outer_r - 18, cx + outer_r + 18, cy + outer_r + 18], outline=(230, 228, 222), width=1)
    draw.ellipse([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r], outline=color, width=4)
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], outline=BORDER_COLOR, width=2)

    # Mechanical indicator dot orbiting the perimeter
    angle = t * (0.8 if state == "IDLE" else 2.2)
    dot_x = cx + math.cos(angle) * outer_r
    dot_y = cy + math.sin(angle) * outer_r
    draw.ellipse([dot_x - 7, dot_y - 7, dot_x + 7, dot_y + 7], fill=TEXT_MAIN)

    return img


def main():
    font_big = load_font(120, bold=True)
    font_med = load_font(24, bold=True)
    font_reg = load_font(18, bold=False)
    font_sm = load_font(14, bold=False)

    if "--snap" in sys.argv:
        frame = render_frame(1.4, "LISTENING", font_big, font_med, font_reg, font_sm)
        out_path = Path(__file__).resolve().parent.parent / "docs" / "ui_test.png"
        frame.save(out_path)
        print(f"Saved light mode preview to {out_path}")
        return

    root = tk.Tk()
    root.title("Orbit UI Layout (10.1 inch Light Mode)")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.configure(bg="#F4F3EF")
    root.resizable(False, False)

    label = tk.Label(root, bd=0, bg="#F4F3EF")
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
        frame = render_frame(t, states[state_idx[0]], font_big, font_med, font_reg, font_sm)
        tk_img = ImageTk.PhotoImage(frame)
        label.configure(image=tk_img)
        label.image = tk_img
        root.after(33, tick)

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
