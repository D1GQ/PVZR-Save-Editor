"""Shared UI helpers and per-field editors."""

from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from ..metadata import enum_for, label_for
from .theme import Theme


def make_scrollable(parent):
    """Pack a vertically scrollable area into `parent`; return its inner frame."""
    outer = ttk.Frame(parent)
    outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer, highlightthickness=0, borderwidth=0,
                       background=Theme.BG)
    vbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)

    inner = ttk.Frame(canvas)
    window_id = canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=vbar.set)

    pending = None  # id of the scheduled scrollregion update

    def recompute_scrollregion():
        nonlocal pending
        pending = None
        bbox = canvas.bbox("all")
        if bbox is not None:
            canvas.configure(scrollregion=bbox)

    def on_inner_configure(_e):
        nonlocal pending
        if pending is not None:
            canvas.after_cancel(pending)
        pending = canvas.after_idle(recompute_scrollregion)

    def on_canvas_configure(e):
        canvas.itemconfigure(window_id, width=e.width)

    inner.bind("<Configure>", on_inner_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    canvas.grid(row=0, column=0, sticky="nsew")
    vbar.grid(row=0, column=1, sticky="ns")
    outer.rowconfigure(0, weight=1)
    outer.columnconfigure(0, weight=1)

    def wheel(e):
        if e.delta:
            canvas.yview_scroll(int(-e.delta / 120), "units")
        return "break"

    def wheel_x11(e):
        if e.num == 4:
            canvas.yview_scroll(-1, "units")
        elif e.num == 5:
            canvas.yview_scroll(1, "units")
        return "break"

    def bind_wheel(_):
        canvas.bind_all("<MouseWheel>", wheel)
        canvas.bind_all("<Button-4>", wheel_x11)
        canvas.bind_all("<Button-5>", wheel_x11)

    def unbind_wheel(_):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", bind_wheel)
    canvas.bind("<Leave>", unbind_wheel)
    return inner


def column_header(parent, columns, padx):
    """Dim header row; `columns` is a list of (text, width) pairs."""
    header = ttk.Frame(parent)
    header.pack(fill="x", padx=padx, pady=(4, 2))
    for text, width in columns:
        ttk.Label(header, text=text, width=width, style="Dim.TLabel").pack(side="left")


def show_enum_missing(parent, enum_name):
    ttk.Label(parent, text=f"{enum_name} enum not loaded.",
              style="Dim.TLabel").pack(anchor="w", padx=10, pady=10)


# ==========================================================================
# 6. Field editors
# ==========================================================================

class IntFieldEditor(ttk.Frame):
    """Integer entry, or a read-only dropdown when an enum table is given."""

    def __init__(self, parent, field_name: str, current_value: int, enum_name: str = None):
        super().__init__(parent)
        self.field_name = field_name
        self.enum = enum_for(enum_name)

        if self.enum:
            self.var = tk.StringVar(value=self._format(current_value))
            self.combo = ttk.Combobox(
                self, textvariable=self.var, state="readonly",
                values=[self._format(v) for v in sorted(self.enum)],
                width=32)
            self.combo.grid(row=0, column=0, sticky="we")
        else:
            self.var = tk.StringVar(value=str(current_value))
            self.entry = ttk.Entry(self, textvariable=self.var, width=22)
            self.entry.grid(row=0, column=0, sticky="we")
        self.columnconfigure(0, weight=1)

    def _format(self, v):
        if not self.enum:
            return str(v)
        name = self.enum.get(v)
        if name is None:
            return f"{v} (unknown)"
        return f"{v} — {name}"

    def commit(self) -> int:
        s = self.var.get().strip()
        if self.enum:
            try:
                return int(s.split(" ", 1)[0])
            except ValueError:
                raise ValueError(f"{self.field_name}: could not parse {s!r}")
        if s == "":
            raise ValueError(f"{self.field_name}: empty integer field")
        try:
            return int(s, 0)
        except ValueError:
            raise ValueError(f"{self.field_name}: '{s}' is not an integer")


_TIME_DISPLAY_FORMAT = "%Y-%m-%d %I:%M:%S %p"
_TIME_PARSE_FORMATS = (
    "%Y-%m-%d %I:%M:%S %p",
    "%Y-%m-%d %I:%M %p",
    "%Y-%m-%d %I:%M:%S%p",
    "%Y-%m-%d %I:%M%p",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)


class TimeFieldEditor(ttk.Frame):
    """Unix-timestamp field shown (and editable) as a 12-hour local datetime."""

    def __init__(self, parent, field_name: str, current_value: int):
        super().__init__(parent)
        self.field_name = field_name
        self.var = tk.StringVar(value=self._format(current_value))
        ttk.Entry(self, textvariable=self.var, width=24).grid(row=0, column=0, sticky="we")
        self.columnconfigure(0, weight=1)

    @staticmethod
    def _format(v: int) -> str:
        try:
            v = int(v)
        except (TypeError, ValueError):
            return str(v)
        if v <= 0:
            return "0 (never)"
        try:
            return datetime.fromtimestamp(v).strftime(_TIME_DISPLAY_FORMAT)
        except (OverflowError, OSError, ValueError):
            return f"{v} (out of range)"

    def commit(self) -> int:
        s = self.var.get().strip()
        if not s:
            return 0
        # Try the full text as a datetime first, so the time of day survives.
        for fmt in _TIME_PARSE_FORMATS:
            try:
                return int(datetime.strptime(s, fmt).timestamp())
            except ValueError:
                continue
        # Otherwise a raw timestamp, optionally followed by a note such as
        # "0 (never)" or "123 (out of range)".
        try:
            return int(s.split(" ", 1)[0], 0)
        except ValueError:
            raise ValueError(
                f"{self.field_name}: '{self.var.get()}' is not a "
                f"timestamp or a 12-hour datetime like 'YYYY-MM-DD 03:45:12 PM'"
            ) from None


class ArrayFieldEditor(ttk.Frame):
    """Collapsible editor for an int[] ("i32arr") or bool[] ("boolarr") field."""

    def __init__(self, parent, field_name: str, values, kind: str, enum_table):
        super().__init__(parent)
        self.field_name = field_name
        self.kind = kind
        self.enum_table = enum_table or {}
        self.values = list(values or [])
        self.rows = {}
        self._expanded = tk.BooleanVar(value=False)
        self._body_built = False
        self._body = None
        self._build()

    def _build(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 2))

        self._toggle = ttk.Checkbutton(
            header, variable=self._expanded, command=self._on_toggle,
            style="Disclosure.TCheckbutton")
        self._toggle.pack(side="left")

        ttk.Label(header, text=label_for(self.field_name),
                  style="Accent.TLabel").pack(side="left", padx=(4, 0))
        ttk.Label(header, text=f"({len(self.values)} entries)",
                  style="Dim.TLabel").pack(side="left", padx=(8, 0))
        ttk.Label(header, text=self._summarize(),
                  style="Dim.TLabel").pack(side="left", padx=(12, 0))

        if not self.values:
            ttk.Label(self, text="(empty)", style="Dim.TLabel").pack(
                anchor="w", padx=(20, 0), pady=(0, 2))

    def _summarize(self):
        if not self.values:
            return ""
        n = sum(1 for v in self.values if v)
        suffix = "set" if self.kind == "boolarr" else "non-zero"
        return f"{n} / {len(self.values)} {suffix}"

    def _on_toggle(self):
        if self._expanded.get():
            self._build_body()
            self._body.pack(fill="x", padx=(20, 0))
        elif self._body is not None:
            self._body.pack_forget()

    def _entry_label(self, i):
        return self.enum_table.get(i, f"index {i}")

    def _build_body(self):
        if self._body_built:
            return
        self._body_built = True
        self._body = ttk.Frame(self)

        grid = ttk.Frame(self._body)
        grid.pack(fill="x")
        grid.columnconfigure(2, weight=1)

        for i, cur in enumerate(self.values):
            ttk.Label(grid, text=str(i), width=4,
                      style="Dim.TLabel").grid(row=i, column=0, sticky="w")
            ttk.Label(grid, text=self._entry_label(i), width=32).grid(
                row=i, column=1, sticky="w", padx=(4, 8))

            if self.kind == "boolarr":
                var = tk.BooleanVar(value=bool(cur))
                ttk.Checkbutton(grid, variable=var).grid(
                    row=i, column=2, sticky="w")
            else:
                var = tk.StringVar(value=str(cur))
                ttk.Spinbox(grid, from_=0, to=2_147_483_647, increment=1,
                            textvariable=var, width=10).grid(
                    row=i, column=2, sticky="w")
            self.rows[i] = var

    def commit(self):
        if not self._body_built:  # never expanded: nothing was edited
            return list(self.values)
        out = []
        for i in range(len(self.values)):
            var = self.rows[i]
            if self.kind == "boolarr":
                out.append(bool(var.get()))
                continue
            s = var.get().strip() or "0"
            try:
                out.append(int(s, 0))
            except ValueError:
                raise ValueError(
                    f"{self.field_name}[{i}] ({self._entry_label(i)}): "
                    f"'{s}' is not an integer")
        return out
