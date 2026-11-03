"""Notebook tabs: fields, plants, store, achievements."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from ..binary import (POTTED_PLANT_FIELDS, PROFILE_FIELDS, PROFILE_KIND,
                      PottedPlant, UserProfile)
from ..metadata import (ARRAY_FIELD_ENUMS, FIELD_GROUPS,
                        FIELDS_OWNED_BY_OTHER_TABS, POTTED_PLANT_ENUM_FIELDS,
                        PROFILE_ENUM_FIELDS, STORE_TOGGLE_ITEMS, enum_for,
                        label_for)
from .theme import Theme
from .widgets import (ArrayFieldEditor, IntFieldEditor, TimeFieldEditor,
                      column_header, make_scrollable, show_enum_missing)


class FieldsTab(ttk.Frame):
    """Main editor: every profile field not owned by another tab, by group."""

    def __init__(self, parent, profile: UserProfile):
        super().__init__(parent)
        self.profile = profile
        self.vars = {}  # field name -> (widget or tk var, kind)
        self._build()

    def _build(self):
        inner = make_scrollable(self)

        groups = list(FIELD_GROUPS)
        grouped = {name for _, names in groups for name in names}
        ungrouped = [
            n for n, _ in PROFILE_FIELDS
            if n not in grouped and n not in FIELDS_OWNED_BY_OTHER_TABS
        ]
        if ungrouped:
            groups.append(("Other", ungrouped))

        for title, names in groups:
            present = [
                n for n in names
                if n in PROFILE_KIND and n not in FIELDS_OWNED_BY_OTHER_TABS
            ]
            if not present:
                continue
            frame = ttk.LabelFrame(inner, text=title, padding=10)
            frame.pack(fill="x", expand=False, padx=8, pady=6)
            frame.columnconfigure(1, weight=1)
            self._build_group(frame, present)

    def _build_group(self, parent, names):
        for row, name in enumerate(names):
            kind = PROFILE_KIND[name]
            cur = getattr(self.profile, name)

            if kind in ("i32arr", "boolarr"):
                enum_name = ARRAY_FIELD_ENUMS.get(name)
                table = enum_for(enum_name) if enum_name else {}
                widget = ArrayFieldEditor(parent, name, cur, kind, table)
                widget.grid(row=row, column=0, columnspan=2,
                            sticky="we", pady=(6, 2))
                self.vars[name] = (widget, kind)
                continue

            ttk.Label(parent, text=label_for(name)).grid(
                row=row, column=0, sticky="w", padx=(0, 12), pady=3)

            if kind in ("bool", "booltoi32"):
                var = tk.BooleanVar(value=bool(cur))
                ttk.Checkbutton(parent, variable=var).grid(
                    row=row, column=1, sticky="w", pady=3)
                self.vars[name] = (var, kind)

            elif kind == "i64time":
                widget = TimeFieldEditor(parent, name, int(cur or 0))
                widget.grid(row=row, column=1, sticky="we", pady=3)
                self.vars[name] = (widget, kind)

            elif kind in ("i32", "i64", "u64"):
                widget = IntFieldEditor(
                    parent, name, int(cur or 0),
                    enum_name=PROFILE_ENUM_FIELDS.get(name))
                widget.grid(row=row, column=1, sticky="we", pady=3)
                self.vars[name] = (widget, kind)

            elif kind == "str":
                var = tk.StringVar(value=cur or "")
                ttk.Entry(parent, textvariable=var).grid(
                    row=row, column=1, sticky="we", pady=3)
                self.vars[name] = (var, kind)

    def commit(self):
        for name, (w, kind) in self.vars.items():
            if kind == "bool":
                value = bool(w.get())
            elif kind == "booltoi32":
                value = 1 if w.get() else 0
            elif kind == "str":
                value = w.get().strip() or None
            else:  # i32 / i64 / u64 / i64time / i32arr / boolarr
                value = w.commit()
            setattr(self.profile, name, value)


class PlantsTab(ttk.Frame):
    """Zen Garden: table of potted plants with add / remove / edit."""

    def __init__(self, parent):
        super().__init__(parent)
        self.current_profile = None
        self._build()

    def _build(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=8, pady=8)
        ttk.Button(bar, text="Add plant", command=self._add_plant).pack(side="left")
        ttk.Button(bar, text="Remove selected", command=self._remove_selected).pack(side="left", padx=6)
        ttk.Button(bar, text="Edit selected", command=self._edit_selected).pack(side="left")

        table = ttk.Frame(self)
        table.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        cols = ("#", "Plant type", "Garden", "X", "Y", "Age", "Fed", "Need")
        self.tree = ttk.Treeview(table, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140 if c == "Plant type" else 80,
                             anchor="w" if c == "Plant type" else "center")
        vsb = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        table.rowconfigure(0, weight=1)
        table.columnconfigure(0, weight=1)
        self.tree.bind("<Double-1>", lambda e: self._edit_selected())

    def set_profile(self, profile):
        self.current_profile = profile
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        if self.current_profile is None:
            return
        seeds = enum_for("ZEN_SEED_TYPE")
        gardens = enum_for("GARDEN_TYPE")
        ages = enum_for("POTTED_PLANT_AGE")
        needs = enum_for("POTTED_PLANT_NEED")
        for i, p in enumerate(self.current_profile.mPottedPlant):
            self.tree.insert("", "end", values=(
                i,
                seeds.get(p.mSeedType, f"Unknown({p.mSeedType})"),
                gardens.get(p.mWhichZenGarden, str(p.mWhichZenGarden)),
                p.mX, p.mY,
                ages.get(p.mPlantAge, str(p.mPlantAge)),
                p.mTimesFed,
                needs.get(p.mPlantNeed, str(p.mPlantNeed))))

    def _selected_index(self):
        sel = self.tree.selection()
        return self.tree.index(sel[0]) if sel else None

    def _add_plant(self):
        if self.current_profile is None:
            return
        self.current_profile.mPottedPlant.append(PottedPlant())
        self.refresh()
        kids = self.tree.get_children()
        if kids:
            self.tree.selection_set(kids[-1])

    def _remove_selected(self):
        i = self._selected_index()
        if i is None or self.current_profile is None:
            return
        del self.current_profile.mPottedPlant[i]
        self.refresh()

    def _edit_selected(self):
        i = self._selected_index()
        if i is None or self.current_profile is None:
            return
        PlantEditor(self, self.current_profile.mPottedPlant[i], on_ok=self.refresh)


class PlantEditor(tk.Toplevel):
    def __init__(self, master, plant: PottedPlant, on_ok):
        super().__init__(master)
        self.title("Edit potted plant")
        self.geometry("560x640")
        self.configure(bg=Theme.BG)
        self.plant = plant
        self.on_ok = on_ok
        self.vars = {}  # field name -> (widget or StringVar, kind)
        self._build()

    def _build(self):
        inner = make_scrollable(self)
        for name, kind in POTTED_PLANT_FIELDS:
            cur = getattr(self.plant, name)
            row = ttk.Frame(inner)
            row.pack(fill="x", padx=10, pady=4)
            ttk.Label(row, text=label_for(name), width=22, anchor="w").pack(side="left")

            enum_name = POTTED_PLANT_ENUM_FIELDS.get(name)
            if kind in ("i32", "i64") and enum_name:
                widget = IntFieldEditor(row, name, int(cur), enum_name=enum_name)
                widget.pack(side="left", fill="x", expand=True)
                self.vars[name] = (widget, kind)
            elif kind == "i64time":
                widget = TimeFieldEditor(row, name, int(cur))
                widget.pack(side="left", fill="x", expand=True)
                self.vars[name] = (widget, kind)
            else:
                # i32arr is edited as comma-separated ints, e.g. "1, 2, 3".
                text = ", ".join(str(x) for x in cur) if kind == "i32arr" else str(cur)
                var = tk.StringVar(value=text)
                ttk.Entry(row, textvariable=var).pack(side="left", fill="x", expand=True)
                self.vars[name] = (var, kind)

        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=10, pady=10)
        ttk.Button(bar, text="OK", command=self._ok).pack(side="right", padx=4)
        ttk.Button(bar, text="Cancel", command=self.destroy).pack(side="right")

    @staticmethod
    def _read_field(widget, kind):
        if hasattr(widget, "commit"):
            return widget.commit()
        if kind == "i32arr":
            tokens = [t.strip() for t in widget.get().split(",") if t.strip()]
            return [int(t, 0) for t in tokens]
        return int(widget.get().strip(), 0)

    def _ok(self):
        try:
            for name, _kind in POTTED_PLANT_FIELDS:
                widget, kind = self.vars[name]
                setattr(self.plant, name, self._read_field(widget, kind))
        except ValueError as e:
            messagebox.showerror("Invalid value", str(e), parent=self)
            return
        self.on_ok()
        self.destroy()


class StoreTab(ttk.Frame):
    """Store purchases: checkbox for toggle items, quantity spinbox otherwise."""

    def __init__(self, parent):
        super().__init__(parent)
        self.profile = None
        # item id -> BooleanVar (toggle items) or StringVar (quantity items)
        self.vars = {}
        self._build()

    def _build(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=8, pady=8)
        ttk.Label(bar, text="Owned quantities / unlocks", style="Accent.TLabel").pack(side="left")
        ttk.Button(bar, text="Clear all", command=self._clear_all).pack(side="right", padx=4)
        ttk.Button(bar, text="Check all toggles",
                   command=self._check_all_toggles).pack(side="right")

        inner = make_scrollable(self)
        items = sorted((v, n) for v, n in enum_for("STORE_ITEM").items() if v >= 0)
        if not items:
            show_enum_missing(inner, "STORE_ITEM")
            return

        column_header(inner, [("ID", 5), ("Item", 26), ("Value", 10)], padx=12)

        for value, name in items:
            row = ttk.Frame(inner)
            row.pack(fill="x", padx=12, pady=1)
            ttk.Label(row, text=str(value), width=5).pack(side="left")
            ttk.Label(row, text=name, width=26).pack(side="left")

            if value in STORE_TOGGLE_ITEMS:
                var = tk.BooleanVar(value=False)
                ttk.Checkbutton(row, variable=var).pack(side="left")
            else:
                var = tk.StringVar(value="0")
                ttk.Spinbox(row, from_=0, to=9999, increment=1,
                            textvariable=var, width=8).pack(side="left")
            self.vars[value] = var

    def _clear_all(self):
        for var in self.vars.values():
            var.set(False if isinstance(var, tk.BooleanVar) else "0")

    def _check_all_toggles(self):
        for var in self.vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(True)

    def set_profile(self, profile):
        self.profile = profile
        self.refresh()

    def refresh(self):
        purchases = list(self.profile.mPurchases) if self.profile else []
        for value, var in self.vars.items():
            qty = purchases[value] if value < len(purchases) else 0
            if isinstance(var, tk.BooleanVar):
                var.set(bool(qty))
            else:
                var.set(str(qty))

    def commit(self):
        if self.profile is None:
            return
        old = list(self.profile.mPurchases or [])

        # Keep existing entries; pad so every listed item has a slot.
        highest = max(self.vars, default=-1)
        new = old + [0] * (highest + 1 - len(old))

        for value, var in self.vars.items():
            if isinstance(var, tk.BooleanVar):
                qty = 1 if var.get() else 0
            else:
                try:
                    qty = int(var.get().strip() or "0")
                except ValueError:
                    name = enum_for("STORE_ITEM").get(value, "?")
                    raise ValueError(
                        f"Store item {value} ({name}): non-integer quantity")
                if qty < 0:
                    raise ValueError(f"Store item {value}: negative quantity")
            new[value] = qty

        self.profile.mPurchases = new


class AchievementsTab(ttk.Frame):
    """Earned / shown checkboxes for each achievement."""

    def __init__(self, parent):
        super().__init__(parent)
        self.profile = None
        self.earned_vars = {}
        self.shown_vars = {}
        self._build()

    def _build(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=8, pady=8)
        ttk.Label(bar, text="Achievements", style="Accent.TLabel").pack(side="left")
        ttk.Button(bar, text="Check all earned",
                   command=lambda: self._bulk(self.earned_vars, True)).pack(side="right", padx=4)
        ttk.Button(bar, text="Uncheck all earned",
                   command=lambda: self._bulk(self.earned_vars, False)).pack(side="right")
        ttk.Button(bar, text="Check all shown",
                   command=lambda: self._bulk(self.shown_vars, True)).pack(side="right", padx=4)

        inner = make_scrollable(self)
        achievements = enum_for("ACHIEVEMENT_TYPE")
        if not achievements:
            show_enum_missing(inner, "ACHIEVEMENT_TYPE")
            return

        column_header(inner, [("ID", 5), ("Name", 26), ("Earned", 10), ("Shown", 10)], padx=10)

        for value in sorted(achievements):
            row = ttk.Frame(inner)
            row.pack(fill="x", padx=10, pady=1)
            ttk.Label(row, text=str(value), width=5).pack(side="left")
            ttk.Label(row, text=achievements[value], width=26).pack(side="left")

            earned = tk.BooleanVar(value=False)
            ttk.Checkbutton(row, variable=earned).pack(side="left", padx=(0, 20))
            self.earned_vars[value] = earned

            shown = tk.BooleanVar(value=False)
            ttk.Checkbutton(row, variable=shown).pack(side="left")
            self.shown_vars[value] = shown

    @staticmethod
    def _bulk(mapping, value):
        for var in mapping.values():
            var.set(value)

    def set_profile(self, profile):
        self.profile = profile
        self.refresh()

    def refresh(self):
        earned, shown = set(), set()
        if self.profile is not None:
            earned = {i for i, b in enumerate(self.profile.mBEarnedAchievements or []) if b}
            shown = {i for i, b in enumerate(self.profile.mBShownAchievements or []) if b}
        for value, var in self.earned_vars.items():
            var.set(value in earned)
        for value, var in self.shown_vars.items():
            var.set(value in shown)

    @staticmethod
    def _collect(mapping, template):
        """Template list (padded as needed) with the checkboxes applied on top."""
        size = max(max(mapping, default=-1) + 1, len(template))
        out = list(template) + [False] * (size - len(template))
        for value, var in mapping.items():
            out[value] = bool(var.get())
        return out

    def commit(self):
        if self.profile is None:
            return
        self.profile.mBEarnedAchievements = self._collect(
            self.earned_vars, self.profile.mBEarnedAchievements or [])
        self.profile.mBShownAchievements = self._collect(
            self.shown_vars, self.profile.mBShownAchievements or [])
