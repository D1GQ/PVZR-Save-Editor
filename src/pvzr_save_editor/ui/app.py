"""Main application window."""

import os
import traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from ..constants import APP_TITLE, APP_VERSION, APP_CREDITS
from ..savefile import try_load
from .icon import apply_window_icon
from .tabs import AchievementsTab, FieldsTab, PlantsTab, StoreTab
from .theme import Theme, apply_dark_theme


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE + " " + APP_VERSION + ", by " + APP_CREDITS)
        self.geometry("1200x820")
        self.minsize(950, 620)
        apply_dark_theme(self)
        apply_window_icon(self)

        self.files = []
        self.current = None
        self.fields_tab = None

        self._build_shortcuts()
        self._build_toolbar()
        self._build_body()

    # ---- layout ----------------------------------------------------------

    def _build_shortcuts(self):
        self.bind_all("<Control-o>", lambda e: self.open_file())
        self.bind_all("<Control-O>", lambda e: self.open_folder())
        self.bind_all("<Control-s>", lambda e: self.save_current())
        self.bind_all("<Control-S>", lambda e: self.save_current_as())
        self.bind_all("<Control-r>", lambda e: self.reload_current())

    def _build_toolbar(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=10, pady=8)
        ttk.Button(bar, text="Open file…", command=self.open_file).pack(side="left")
        ttk.Button(bar, text="Open folder…", command=self.open_folder).pack(side="left", padx=6)
        ttk.Button(bar, text="Reload", command=self.reload_current).pack(side="left")
        ttk.Button(bar, text="Save", command=self.save_current).pack(side="left", padx=6)
        ttk.Button(bar, text="Save as…", command=self.save_current_as).pack(side="left")
        ttk.Button(bar, text="Quit", command=self.destroy).pack(side="left", padx=(18, 0))
        self.path_lbl = ttk.Label(bar, text="(no file)", style="Dim.TLabel")
        self.path_lbl.pack(side="left", padx=14)

    def _build_body(self):
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=10, pady=6)

        left = ttk.Frame(paned)
        paned.add(left, weight=1)
        ttk.Label(left, text="Loaded files", style="Accent.TLabel").pack(anchor="w")
        list_frame = ttk.Frame(left)
        list_frame.pack(fill="both", expand=True, pady=(4, 0))
        self.file_list = tk.Listbox(
            list_frame, exportselection=False,
            background=Theme.BG_ALT, foreground=Theme.FG,
            selectbackground=Theme.SEL_BG, selectforeground=Theme.SEL_FG,
            highlightthickness=0, borderwidth=0,
            activestyle="none")
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=vsb.set)
        self.file_list.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.file_list.bind("<<ListboxSelect>>", self._on_select)

        right = ttk.Frame(paned)
        paned.add(right, weight=5)
        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill="both", expand=True, padx=4, pady=4)

        self.tab_fields_container = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_fields_container, text="Main File Editor")

        self.plants_tab = PlantsTab(self.notebook)
        self.notebook.add(self.plants_tab, text="Zen Garden")

        self.store_tab = StoreTab(self.notebook)
        self.notebook.add(self.store_tab, text="Store")

        self.achievements_tab = AchievementsTab(self.notebook)
        self.notebook.add(self.achievements_tab, text="Achievements")

        self.notebook.bind("<<NotebookTabChanged>>",
                           lambda e: self._safe_commit_fields())

    # ---- opening / listing files ----------------------------------------

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Open PvZ Replanted save (.dat)",
            filetypes=[("PvZ save file", "*.dat"), ("All files", "*.*")])
        if not path:
            return
        pf, err = try_load(path)
        if pf is None:
            messagebox.showerror("Failed to load", f"{os.path.basename(path)}\n\n{err}")
            return
        self.files = [pf]
        self._refresh_file_list(select=0)
        self.path_lbl.configure(text=path)
        self._load_at(0)

    def open_folder(self):
        d = filedialog.askdirectory(title="Select folder containing .dat files")
        if not d:
            return
        self.files = []
        errors = []
        skipped = []
        for fn in sorted(os.listdir(d)):
            low = fn.lower()
            if not low.endswith(".dat"):
                continue
            if ".ig.dat" in low or low == "profile_data.dat":
                skipped.append(fn)
                continue
            pf, err = try_load(os.path.join(d, fn))
            if pf is None:
                errors.append(f"{fn}: {err}")
            else:
                self.files.append(pf)

        self._refresh_file_list(select=0 if self.files else None)
        self.path_lbl.configure(text=d)

        notes = []
        if skipped:
            notes.append(f"Skipped (not a profile): {', '.join(skipped)}")
        if errors:
            notes.append("Failed to parse:\n  " + "\n  ".join(errors))
        if notes:
            messagebox.showinfo("Folder loaded", "\n\n".join(notes))

        if self.files:
            self._load_at(0)
        else:
            self._clear_ui()

    def _refresh_file_list(self, select=None):
        self.file_list.delete(0, "end")
        for pf in self.files:
            self.file_list.insert(
                "end",
                f"{os.path.basename(pf.path)}  "
                f"[{pf.wrapper}]  "
                f"{pf.profile.mName or '(unnamed)'}")
        if select is not None and 0 <= select < self.file_list.size():
            self.file_list.selection_clear(0, "end")
            self.file_list.selection_set(select)
            self.file_list.activate(select)

    def reload_current(self):
        if self.current is None:
            self.open_file()
            return
        pf, err = try_load(self.current.path)
        if pf is None:
            messagebox.showerror("Reload failed", err)
            return
        try:
            idx = self.files.index(self.current)
            self.files[idx] = pf
        except ValueError:
            self.files = [pf]
            idx = 0
        self._refresh_file_list(select=idx)
        self._load_at(idx)

    def _on_select(self, _e):
        sel = self.file_list.curselection()
        if sel:
            self._load_at(sel[0])

    # ---- switching the active file --------------------------------------

    def _destroy_fields_tab(self):
        for w in self.tab_fields_container.winfo_children():
            w.destroy()

    def _load_at(self, idx):
        self._safe_commit_fields()
        self._destroy_fields_tab()
        self.current = self.files[idx]
        self.fields_tab = FieldsTab(self.tab_fields_container, self.current.profile)
        self.fields_tab.pack(fill="both", expand=True)
        for tab in (self.plants_tab, self.store_tab, self.achievements_tab):
            tab.set_profile(self.current.profile)
        self.path_lbl.configure(text=self.current.path)

    def _clear_ui(self):
        self._destroy_fields_tab()
        self.fields_tab = None
        for tab in (self.plants_tab, self.store_tab, self.achievements_tab):
            tab.set_profile(None)
        self.current = None

    def _safe_commit_fields(self):
        """Push UI edits into the profile; report bad input instead of raising."""
        if self.fields_tab is None:
            return
        try:
            self.fields_tab.commit()
            self.store_tab.commit()
            self.achievements_tab.commit()
        except ValueError as e:
            messagebox.showerror("Field error", str(e))

    # ---- saving ----------------------------------------------------------

    def _require_current(self):
        if self.current is None:
            messagebox.showinfo("No file", "Open a .dat file first.")
            return False
        return True

    @staticmethod
    def _show_save_error(e):
        messagebox.showerror("Save failed", f"{e}\n\n{traceback.format_exc()}")

    def save_current(self):
        if not self._require_current():
            return
        self._safe_commit_fields()
        try:
            self.current.save()
        except Exception as e:
            self._show_save_error(e)
            return
        messagebox.showinfo("Saved", f"Wrote {self.current.path}")

    def save_current_as(self):
        if not self._require_current():
            return
        out = filedialog.asksaveasfilename(
            title="Save as",
            defaultextension=".dat",
            filetypes=[("PvZ save file", "*.dat"), ("All files", "*.*")])
        if not out:
            return
        self._safe_commit_fields()
        try:
            self.current.save_as(out)
        except Exception as e:
            self._show_save_error(e)
            return
        messagebox.showinfo("Saved", f"Wrote {out}")


def main():
    try:
        app = App()
    except Exception:
        traceback.print_exc()
        raise
    app.mainloop()
