"""Launcher used by PyInstaller and `python launch.py` (no install needed)."""

import os
import sys
import traceback

if not getattr(sys, "frozen", False):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _report_crash():
    """A --windowed EXE has no console, so show startup crashes in a dialog."""
    text = traceback.format_exc()
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("PvZ Replanted Save Editor crashed", text)
    except Exception:
        pass
    if sys.stderr:
        sys.stderr.write(text)


if __name__ == "__main__":
    try:
        from src.ui.app import main
        main()
    except Exception:
        _report_crash()
        sys.exit(1)