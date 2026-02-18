#!/bin/bash
# PZ Mod Update Checker - macOS launcher
# Double-click this file to run

cd "$(dirname "$0")"

echo ""
echo "  +===================================================="
echo "  |  PZ Mod Update Checker - Setup"
echo "  +===================================================="
echo ""

# --- Python check ---
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "  [!] Python is not installed."
    echo ""
    echo "  macOS usually includes Python 3. If not, install it:"
    echo ""
    echo "    Option 1: Open Terminal and run:"
    echo "      xcode-select --install"
    echo ""
    echo "    Option 2: Download from:"
    echo "      https://www.python.org/downloads/"
    echo ""
    read -p "  Press Enter to close..."
    exit 1
fi

echo "  [OK] Python found: $PYTHON_CMD ($($PYTHON_CMD --version 2>&1))"
echo ""

# --- Run script ---
$PYTHON_CMD "$(dirname "$0")/pz_mod_update_checker.py" "$@"

echo ""
echo "  --------------------------------------------------"
read -p "  Press Enter to close..."
