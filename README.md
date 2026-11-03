# PvZ Replanted Save Editor

Tkinter save editor for Plants vs. Zombies: Replanted profiles.

## Develop (VS Code)

1. Open the folder, then `Python: Create Environment` (venv, `.venv`).
2. Press F5 and pick **PvZR Save Editor**.

Adding a new enum table: put an UPPER_CASE `{int: name}` dict in `enums.py`;
it is discovered automatically. Labels, groups and bindings live in `meta.py`.

## Build the EXE

Run `build_exe.bat` (or the VS Code build task, Ctrl+Shift+B). The result is
a single windowed file at `dist\PvZReplantedSaveEditor.exe`; it needs no
Python installed on the target machine. Build on Windows to get a Windows EXE.
