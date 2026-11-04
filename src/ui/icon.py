import os
import sys
import tkinter as tk

from .theme import Theme


def _assets_dir():
    """Directory containing icon.png / icon.ico, both frozen and from source."""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "assets")


ASSETS_DIR = _assets_dir()


def _set_png_icon(root, path):
    img = tk.PhotoImage(file=path)
    root.iconphoto(True, img)
    root._icon_ref = img 


def _set_ico_icon(root, path):
    root.iconbitmap(path)


def apply_window_icon(root: tk.Tk):
    """Use the first icon that loads; otherwise draw a simple generated one."""
    is_windows = sys.platform.startswith("win")

    candidates = [(os.path.join(ASSETS_DIR, "icon.png"), _set_png_icon, True)]
    if is_windows:
        candidates.append((os.path.join(ASSETS_DIR, "icon.ico"), _set_ico_icon, True))

    for path, loader, report in candidates:
        if not os.path.isfile(path):
            continue
        try:
            loader(root, path)
            return
        except Exception as e:
            if report and sys.stderr:
                sys.stderr.write(f"Failed to load {path}: {e}\n")

    try:
        size = 32
        img = tk.PhotoImage(width=size, height=size)
        img.put(Theme.BG,        to=(0, 0, size, size))
        img.put(Theme.FG_ACCENT, to=(8, 8, size - 8, size - 8))
        img.put(Theme.BG,        to=(12, 12, size - 12, size - 12))
        img.put(Theme.FG_ACCENT, to=(14, 14, size - 14, size - 14))
        root.iconphoto(True, img)
        root._icon_ref = img
    except Exception:
        pass