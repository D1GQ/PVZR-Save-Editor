@echo off
setlocal
cd /d "%~dp0"
set "OUT_DIR=%~dp0build\PvZReplantedSaveEditor"

if not exist .venv\Scripts\python.exe (
    rmdir /s /q .venv 2>nul
    python -m venv .venv || goto :fail
)

.venv\Scripts\python.exe -m pip install --quiet --upgrade pip pyinstaller || goto :fail

echo Building EXE...
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name PvZReplantedSaveEditor ^
    --icon "%~dp0src\assets\icon.ico" ^
    --paths "%~dp0." ^
    --add-data "%~dp0src\assets;assets" ^
    --distpath "%OUT_DIR%" ^
    --workpath "%TEMP%\pvzr_build" ^
    --specpath "%TEMP%\pvzr_build" ^
    "%~dp0launch.py" || goto :fail

echo Done: %OUT_DIR%\PvZReplantedSaveEditor.exe
exit /b 0

:fail
echo Build failed.
exit /b 1