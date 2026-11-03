@echo off
setlocal
cd /d "%~dp0"

rem ---- EXE output folder (relative to this script) ----
set "OUT_DIR=%~dp0build\PvZReplantedSaveEditor"

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv || goto :fail
)
call .venv\Scripts\activate.bat || goto :fail
python -m pip install --quiet --upgrade pip pyinstaller || goto :fail

echo Building EXE...
pyinstaller --noconfirm --clean --onefile --windowed ^
    --name PvZReplantedSaveEditor ^
    --icon "%~dp0src\pvzr_save_editor\assets\icon.ico" ^
    --paths "%~dp0src" ^
    --add-data "%~dp0src\pvzr_save_editor\assets;pvzr_save_editor\assets" ^
    --distpath "%OUT_DIR%" ^
    --workpath "%TEMP%\pvzr_build" ^
    --specpath "%TEMP%\pvzr_build" ^
    "%~dp0launch.py" || goto :fail

echo.
echo Done: %OUT_DIR%\PvZReplantedSaveEditor.exe
exit /b 0

:fail
echo Build failed.
exit /b 1