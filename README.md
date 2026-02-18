# PZ Mod Update Checker

**[日本語版 README はこちら (Japanese)](README.ja.md)**

Quickly find out **which mods were updated** when Steam downloads Workshop content for **Project Zomboid**.

![Windows](https://img.shields.io/badge/Windows-10%2F11-blue) ![macOS](https://img.shields.io/badge/macOS-supported-green) ![Linux](https://img.shields.io/badge/Linux-supported-orange) ![Python](https://img.shields.io/badge/Python-3.7+-yellow)

## The Problem

> You launch Steam and see "Project Zomboid - Workshop Content" downloading.
> It finishes, but... **which mod was updated??**

Steam only shows the download size — not which mods changed. To find out, you'd have to open the Workshop and check each mod manually.

**This tool gives you the answer instantly.** (Windows: double-click / macOS & Linux: terminal)

## Example Output

```
  * Updated mods (2)
  ======================================================================
    >> that DAMN Library 0.9848b
       2026-02-17 18:00 -> 2026-02-18 03:58
       Size: 33.9 MB  |  ID: 3171167894
       https://steamcommunity.com/sharedfiles/filedetails/?id=3171167894

    >> [Build 42] Unofficial Japanese Translation
       2026-02-16 12:00 -> 2026-02-17 21:13
       Size: 3.8 MB  |  ID: 1227676938
       https://steamcommunity.com/sharedfiles/filedetails/?id=1227676938
```

---

## Download

**[📦 Download Latest Release (zip)](https://github.com/movinow/pz-mod-update-checker/releases/latest)**

1. Download the `.zip` file from the link above
2. Extract it to any folder you like

> ⚠️ **Python is required** — see [Installation Guide](#installing-python) below if you don't have it yet

---

## Usage

### Windows (Menu Interface)

**Double-click `check_mod_updates.bat`** to see an interactive menu:

```
  +====================================================+
  |  PZ Mod Update Checker                              |
  +====================================================+

  [OK] Python 3.xx.x

  ----------------------------------------------------
  [1] Check for mod updates
  [2] List all mods (by update date)
  [3] Show recently updated mods
  [4] Reset snapshot
  [0] Exit
  ----------------------------------------------------

  Select [1-4, 0]:
```

Just type a number and press Enter.

| # | Function | Description |
|:-:|----------|-------------|
| **1** | Check updates | Shows which mods have been updated since your last check. On first run, records the current state and shows mods updated in the last 30 days |
| **2** | List all mods | Lists all subscribed mods sorted by update date (newest first) |
| **3** | Recent updates | Shows only mods updated in the last 7 days |
| **4** | Reset | Resets the snapshot. The next run will be treated as a first run |

### macOS / Linux

Run the Python script directly from a terminal:

```bash
python3 pz_mod_update_checker.py            # Check for updates
python3 pz_mod_update_checker.py --list     # List all mods
python3 pz_mod_update_checker.py --days 7   # Show mods updated in last 7 days
python3 pz_mod_update_checker.py --reset    # Reset snapshot
```

---

## Installing Python

This tool requires Python 3.7 or later. No additional libraries are needed.

### Windows

**Option 1: Microsoft Store (Recommended — easiest)**
1. Open Microsoft Store
2. Search for "Python"
3. Click "Get" on "Python 3.xx"

**Option 2: Official Website**
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.xx"
3. Run the installer
4. ⚠️ **Check "Add Python to PATH" before clicking Install**

### macOS

Python 3 is often pre-installed on macOS.
If not, open Terminal and run:

```
xcode-select --install
```

### Linux

Pre-installed on most distributions.
If not:

```bash
# Ubuntu / Debian
sudo apt install python3

# Fedora
sudo dnf install python3
```

---

## FAQ

### Q: Do I need to have the game or Steam running?

**No.** This tool reads files that Steam has previously saved to disk. It works completely offline — no need to launch the game or Steam.

### Q: Is it safe? Does it connect to anything?

**It runs entirely offline.** No network connections are made. It only reads Steam's local manifest files.

### Q: I get "Python is not installed"

This tool requires Python to run. The bat file will show this message:

```
  [!] Python is not installed.

  This tool requires Python 3.7 or later.
```

Install Python using one of the methods above, then try again.

> **Note for Windows users:** Windows 10/11 may appear to have a `python` command pre-installed, but this is actually an App Execution Alias that redirects to Microsoft Store — it's not real Python. You need to install Python using the methods described above.

### Q: I get "ACF file not found"

- Make sure Steam is installed on your computer
- Make sure you have at least one Workshop mod subscribed for Project Zomboid
- If you've never downloaded any mods, launch Steam and let it sync
- If Steam is installed in a non-standard location, use the `--acf` option:
  ```
  python pz_mod_update_checker.py --acf "D:\SteamLibrary\steamapps\workshop\appworkshop_108600.acf"
  ```

### Q: Mod name shows as "(ID: xxxxx)"

The mod's data may not have been downloaded correctly. Try verifying the game's file integrity through Steam.

### Q: Where is data stored?

A single snapshot file (`.pz_mod_snapshot.json`) is created **in the same folder as the tool**. No files are created anywhere else. No registry or system settings are modified.

### Q: How do I uninstall?

**Just delete the folder.** This tool makes no changes to your game data or Steam files, so deleting the folder removes everything cleanly.

---

## How It Works

1. Parses Steam's local manifest file (`appworkshop_108600.acf`) in Valve Data Format (VDF)
2. Reads each mod's update timestamp and resolves mod names from `mod.info` files
3. Compares the current state against the previous snapshot to detect changes
4. Saves the current state as a snapshot for next time

No Steam API or network communication is used. Everything is done through local file analysis.

---

## License

MIT License — free to use, modify, and redistribute.
