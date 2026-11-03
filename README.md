# PvZ Replanted Save Editor

Tkinter save editor for Plants vs. Zombies: Replanted profiles.

## Layout

```
launch.py                     entry point for VS Code / PyInstaller
run.bat                       run from source on Windows
build_exe.bat                 build dist\PvZReplantedSaveEditor.exe
src/pvzr_save_editor/
    constants.py              app title, header size, profile version
    binary.py                 Reader/Writer, PottedPlant, UserProfile
    savefile.py               header, compression, load/save
    enums.py                  id -> name tables (data)
    meta.py                   labels, field groups, enum bindings (data)
    metadata.py               loads enums/meta, exposes enum_for()/label_for()
    ui/                       theme, icon, widgets, tabs, main window
    assets/                   icon.png / icon.ico
```

## Develop (VS Code)

1. Open the folder, then `Python: Create Environment` (venv, `.venv`).
2. Press F5 and pick **PvZR Save Editor**.

Adding a new enum table: put an UPPER_CASE `{int: name}` dict in `enums.py`;
it is discovered automatically. Labels, groups and bindings live in `meta.py`.

## Build the EXE

Run `build_exe.bat` (or the VS Code build task, Ctrl+Shift+B). The result is
a single windowed file at `dist\PvZReplantedSaveEditor.exe`; it needs no
Python installed on the target machine. Build on Windows to get a Windows EXE.
