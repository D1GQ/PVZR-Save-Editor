"""Dark ttk theme."""

import tkinter as tk
from tkinter import ttk


class Theme:
    BG          = "#1e1e1e"
    BG_ALT      = "#252526"
    BG_INPUT    = "#2d2d30"
    BG_HOVER    = "#37373d"
    FG          = "#e6e6e6"
    FG_DIM      = "#a0a0a0"
    FG_ACCENT   = "#4ec9b0"
    BORDER      = "#3f3f46"
    SEL_BG      = "#094771"
    SEL_FG      = "#ffffff"
    BTN_BG      = "#3a3d41"
    BTN_HOVER   = "#4a4d52"
    OK          = "#4ec9b0"
    WARN        = "#d7ba7d"
    ERR         = "#f48771"


def apply_dark_theme(root: tk.Tk):
    root.configure(bg=Theme.BG)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    cfg, smap = style.configure, style.map

    cfg(".", background=Theme.BG, foreground=Theme.FG,
        fieldbackground=Theme.BG_INPUT, bordercolor=Theme.BORDER,
        troughcolor=Theme.BG_ALT, selectbackground=Theme.SEL_BG,
        selectforeground=Theme.SEL_FG, insertcolor=Theme.FG)

    cfg("TFrame", background=Theme.BG)
    cfg("TLabel", background=Theme.BG, foreground=Theme.FG)
    for prefix, color in (("Dim", Theme.FG_DIM), ("Accent", Theme.FG_ACCENT),
                          ("Err", Theme.ERR), ("Warn", Theme.WARN)):
        cfg(f"{prefix}.TLabel", background=Theme.BG, foreground=color)

    cfg("TLabelframe", background=Theme.BG, foreground=Theme.FG,
        bordercolor=Theme.BORDER, lightcolor=Theme.BORDER,
        darkcolor=Theme.BORDER)
    cfg("TLabelframe.Label", background=Theme.BG, foreground=Theme.FG_ACCENT)

    cfg("TButton", background=Theme.BTN_BG, foreground=Theme.FG,
        bordercolor=Theme.BORDER, focuscolor=Theme.FG_ACCENT, padding=(8, 3))
    smap("TButton",
         background=[("pressed", Theme.BG_HOVER), ("active", Theme.BTN_HOVER)],
         foreground=[("disabled", Theme.FG_DIM)])

    cfg("TCheckbutton", background=Theme.BG, foreground=Theme.FG,
        indicatorbackground=Theme.BG_INPUT, indicatorforeground=Theme.FG)
    cfg("Disclosure.TCheckbutton", background=Theme.BG,
        foreground=Theme.FG_ACCENT, indicatorbackground=Theme.BG_INPUT,
        indicatorforeground=Theme.FG_ACCENT, padding=(2, 0))
    for name in ("TCheckbutton", "Disclosure.TCheckbutton"):
        smap(name,
             background=[("active", Theme.BG)],
             indicatorbackground=[("selected", Theme.FG_ACCENT),
                                  ("active", Theme.BG_HOVER)])

    cfg("TEntry", fieldbackground=Theme.BG_INPUT, foreground=Theme.FG,
        bordercolor=Theme.BORDER, insertcolor=Theme.FG)
    smap("TEntry",
         fieldbackground=[("readonly", Theme.BG_ALT)],
         bordercolor=[("focus", Theme.FG_ACCENT)])

    cfg("TCombobox", fieldbackground=Theme.BG_INPUT, background=Theme.BG_INPUT,
        foreground=Theme.FG, arrowcolor=Theme.FG, bordercolor=Theme.BORDER)
    smap("TCombobox",
         fieldbackground=[("readonly", Theme.BG_INPUT)],
         foreground=[("readonly", Theme.FG)],
         selectbackground=[("readonly", Theme.BG_INPUT)],
         selectforeground=[("readonly", Theme.FG)])

    cfg("TSpinbox", fieldbackground=Theme.BG_INPUT, foreground=Theme.FG,
        background=Theme.BG_INPUT, arrowcolor=Theme.FG,
        bordercolor=Theme.BORDER, insertcolor=Theme.FG)

    cfg("TNotebook", background=Theme.BG, bordercolor=Theme.BORDER)
    cfg("TNotebook.Tab", background=Theme.BG_ALT, foreground=Theme.FG_DIM,
        padding=(12, 6))
    smap("TNotebook.Tab",
         background=[("selected", Theme.BG)],
         foreground=[("selected", Theme.FG_ACCENT)])

    for orient in ("Vertical", "Horizontal"):
        cfg(f"{orient}.TScrollbar", background=Theme.BG_ALT,
            troughcolor=Theme.BG, bordercolor=Theme.BG,
            arrowcolor=Theme.FG_DIM)
    smap("Vertical.TScrollbar", background=[("active", Theme.BG_HOVER)])

    cfg("Treeview", background=Theme.BG_ALT, fieldbackground=Theme.BG_ALT,
        foreground=Theme.FG, bordercolor=Theme.BORDER, rowheight=22)
    cfg("Treeview.Heading", background=Theme.BG, foreground=Theme.FG_ACCENT,
        bordercolor=Theme.BORDER, relief="flat")
    smap("Treeview",
         background=[("selected", Theme.SEL_BG)],
         foreground=[("selected", Theme.SEL_FG)])
    smap("Treeview.Heading", background=[("active", Theme.BG_HOVER)])

    cfg("TPanedwindow", background=Theme.BG)
    cfg("Sash", sashthickness=6, background=Theme.BG)

    root.option_add("*TCombobox*Listbox.background", Theme.BG_INPUT)
    root.option_add("*TCombobox*Listbox.foreground", Theme.FG)
    root.option_add("*TCombobox*Listbox.selectBackground", Theme.SEL_BG)
    root.option_add("*TCombobox*Listbox.selectForeground", Theme.SEL_FG)
    root.option_add("*TCombobox*Listbox.font", "TkDefaultFont")
