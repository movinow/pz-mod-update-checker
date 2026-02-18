@echo off
chcp 65001 >nul 2>&1
title PZ Mod Update Checker

echo.
echo   +====================================================+
echo   ^|  PZ Mod Update Checker                              ^|
echo   +====================================================+
echo.

REM --- Python check ---
REM Test if Python can actually execute code (not just exist on PATH).
REM This correctly handles both python.org and Microsoft Store installs,
REM and rejects the Windows Store alias stub (which can't run code).

py -c "import sys" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=py
    goto :found_python
)
python3 -c "import sys" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=python3
    goto :found_python
)
python -c "import sys" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=python
    goto :found_python
)

echo   [!] Python is not installed.
echo.
echo   This tool requires Python 3.7 or later.
echo.
echo   How to install (choose one):
echo.
echo     Option 1 - Microsoft Store (easiest):
echo       1. Open Microsoft Store
echo       2. Search for "Python 3"
echo       3. Click "Get" / "Install"
echo.
echo     Option 2 - Official site:
echo       1. Go to https://www.python.org/downloads/
echo       2. Download and run the installer
echo       3. IMPORTANT: Check "Add Python to PATH" before clicking Install
echo.
pause
exit /b 1

:found_python
for /f "tokens=*" %%v in ('%PYTHON_CMD% -c "import sys; print('Python', sys.version.split()[0])"') do (
    echo   [OK] %%v
)
echo.

REM --- If command-line arguments were passed, run directly ---
if not "%~1"=="" goto :run_direct

REM --- Interactive menu ---
:menu
echo   ----------------------------------------------------
echo   [1] Check for mod updates
echo   [2] List all mods (by update date)
echo   [3] Show recently updated mods (last 7 days)
echo   [4] Reset snapshot
echo   [0] Exit
echo   ----------------------------------------------------
echo.
set CHOICE=
set /p CHOICE=  Select [1-4, 0]:

if "%CHOICE%"=="1" goto :run_check
if "%CHOICE%"=="2" goto :run_list
if "%CHOICE%"=="3" goto :run_days
if "%CHOICE%"=="4" goto :run_reset
if "%CHOICE%"=="0" goto :quit
echo.
echo   [!] Invalid selection. Please enter 1-4 or 0.
echo.
goto :menu

:run_check
echo.
%PYTHON_CMD% "%~dp0pz_mod_update_checker.py"
goto :done

:run_list
echo.
%PYTHON_CMD% "%~dp0pz_mod_update_checker.py" --list
goto :done

:run_days
echo.
%PYTHON_CMD% "%~dp0pz_mod_update_checker.py" --days 7
goto :done

:run_reset
echo.
%PYTHON_CMD% "%~dp0pz_mod_update_checker.py" --reset
goto :done

:run_direct
%PYTHON_CMD% "%~dp0pz_mod_update_checker.py" %*
goto :done

:done
echo.
echo   --------------------------------------------------
echo   Press any key to close...
pause >nul
exit /b 0

:quit
exit /b 0
