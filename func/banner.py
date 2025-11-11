import os
import sys
import time
import json
from pathlib import Path
import pyfiglet
from colorama import init, Style

init()

def rgb_escape(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def clear_lines(n):
    for _ in range(n):
        sys.stdout.write("\033[F\033[K")

def show_banner():
    base = Path(__file__).resolve().parent.parent
    data_path = base / "db" / "data.json"
    version = "v1.0"
    
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            version = data.get("version", version)
    except Exception:
        pass

    text = "QUANTUM ONLINER"
    fig = pyfiglet.Figlet(font="bloody")
    banner = fig.renderText(text)
    lines = banner.splitlines()
    line_count = len(lines) + 4

    blue_shades = [
        (0, 191, 255),
        (30, 144, 255),
        (65, 105, 225),
        (0, 0, 205),
        (25, 25, 112),
        (0, 0, 139)
    ]

    try:
        cols = os.get_terminal_size().columns
    except Exception:
        cols = 80

    cycles = 3
    delay = 0.1
    
    for cycle in range(cycles):
        r, g, b = blue_shades[cycle % len(blue_shades)]
        esc = rgb_escape(r, g, b)
        
        for shift in range(0, max(1, min(5, cols//30))):
            prefix = " " * shift
            
            for ln in lines:
                sys.stdout.write(esc + prefix + ln + Style.RESET_ALL + "\n")
            
            sys.stdout.write(esc + prefix + "─" * 50 + Style.RESET_ALL + "\n")
            sys.stdout.write(esc + prefix + f"    Quantum-Level Discord Token Online Tool" + Style.RESET_ALL + "\n")
            sys.stdout.write(esc + prefix + f"    Version: {version}" + Style.RESET_ALL + "\n")
            sys.stdout.flush()
            
            time.sleep(delay)
            clear_lines(line_count)

    final_esc = rgb_escape(0, 191, 255)
    for ln in lines:
        sys.stdout.write(final_esc + ln + Style.RESET_ALL + "\n")
    
    sys.stdout.write(final_esc + "─" * 50 + Style.RESET_ALL + "\n")
    sys.stdout.write(final_esc + f"    Quantum-Level Discord Token Online Tool" + Style.RESET_ALL + "\n")
    sys.stdout.write(final_esc + f"    Version: {version}" + Style.RESET_ALL + "\n")
    sys.stdout.flush()