@echo off
title MeoBoost - EXE Builder
chcp 65001 >nul

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                   MeoBoost - EXE Builder                     ║
echo ║           Windows Performance Optimization Tool              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

:: Check and install dependencies
echo [1/4] Checking and installing dependencies...
pip install pyinstaller rich --quiet

:: Clean previous builds
echo [2/4] Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

:: Build EXE
echo [3/4] Building MeoBoost.exe...
echo       (This may take 1-2 minutes)

pyinstaller --noconfirm --onefile --console --name "MeoBoost" ^
    --add-data "Files;Files" ^
    --hidden-import "rich" ^
    --hidden-import "rich.console" ^
    --hidden-import "rich.table" ^
    --hidden-import "rich.box" ^
    --hidden-import "tweaks" ^
    --hidden-import "tweaks.power" ^
    --hidden-import "tweaks.nvidia" ^
    --hidden-import "tweaks.amd" ^
    --hidden-import "tweaks.intel" ^
    --hidden-import "tweaks.gpu_common" ^
    --hidden-import "tweaks.network" ^
    --hidden-import "tweaks.memory" ^
    --hidden-import "tweaks.input" ^
    --hidden-import "tweaks.system" ^
    --hidden-import "tweaks.misc" ^
    --hidden-import "tweaks.privacy" ^
    --hidden-import "tweaks.fps" ^
    --hidden-import "utils" ^
    --hidden-import "utils.registry" ^
    --hidden-import "utils.system" ^
    --hidden-import "utils.backup" ^
    --hidden-import "utils.files" ^
    --hidden-import "utils.settings" ^
    --hidden-import "utils.benchmark" ^
    --hidden-import "ui" ^
    --hidden-import "ui.terminal" ^
    --collect-all "rich" ^
    --uac-admin ^
    main.py

:: Check result
echo.
if exist "dist\MeoBoost.exe" (
    echo [4/4] Build successful!
    echo.
    echo    Output:  dist\MeoBoost.exe
    echo    Size:    
    for %%A in ("dist\MeoBoost.exe") do echo             %%~zA bytes
    echo.
    echo You can copy MeoBoost.exe and run it directly.
    echo No additional files required.
) else (
    echo [ERROR] Build failed!
    echo Check the error messages above for details.
)

echo.
pause
