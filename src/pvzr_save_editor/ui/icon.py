"""Window icon loading (works from source and from a PyInstaller bundle)."""

import os
import sys
import tkinter as tk

from .theme import Theme


# Assets live inside the package, so __file__ resolves correctly both when
# running from source and inside a PyInstaller bundle (sys._MEIPASS).
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def _set_png_icon(root, path):
    img = tk.PhotoImage(file=path)
    root.iconphoto(True, img)
    root._icon_ref = img  # keep a reference so Tk doesn't garbage-collect it


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
            if report and sys.stderr:  # stderr is None in a --windowed EXE
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
