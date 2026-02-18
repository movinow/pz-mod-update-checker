@echo off
chcp 65001 >nul 2>&1
title PZ Mod Update Checker

echo.
echo   +====================================================+
echo   ^|  PZ Mod Update Checker - Setup                      ^|
echo   +====================================================+
echo.

REM --- Python check ---
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=python
    goto :found_python
)
where python3 >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=python3
    goto :found_python
)
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=py
    goto :found_python
)

echo   [!] Python is not installed.
echo.
echo   This tool requires Python 3.7 or later.
echo.
echo   How to install:
echo     1. Open Microsoft Store
echo     2. Search for "Python 3"
echo     3. Click "Get" / "Install"
echo.
echo   Or download from: https://www.python.org/downloads/
echo   (Check "Add Python to PATH" during installation)
echo.
pause
exit /b 1

:found_python
echo   [OK] Python found: %PYTHON_CMD%

REM --- Version check ---
for /f "tokens=2 delims= " %%v in ('%PYTHON_CMD% --version 2^>^&1') do set PYVER=%%v
echo   [OK] Version: %PYVER%
echo.

REM --- Run script ---
%PYTHON_CMD% "%~dp0pz_mod_update_checker.py" %*

echo.
echo   --------------------------------------------------
echo   Press any key to close...
pause >nul
