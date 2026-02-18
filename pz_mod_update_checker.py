#!/usr/bin/env python3
"""
Project Zomboid - Steam Workshop Mod 更新チェッカー

Steamのワークショップマニフェスト(ACF)ファイルを解析し、
どのModが更新されたかをスナップショット比較で検出する。

対応OS: macOS / Windows / Linux
依存: Python 3.7+ (標準ライブラリのみ)

使い方:
    python pz_mod_update_checker.py          # 更新チェック（スナップショット比較）
    python pz_mod_update_checker.py --list   # 全Mod一覧（更新日時順）
    python pz_mod_update_checker.py --reset  # スナップショットをリセット
    python pz_mod_update_checker.py --days 7 # 直近7日間の更新を表示
"""

import json
import os
import platform
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── 定数 ────────────────────────────────────────────────────────────

APP_ID = "108600"  # Project Zomboid
SNAPSHOT_FILENAME = ".pz_mod_snapshot.json"

# ローカルタイムゾーン（システム設定を使用）
LOCAL_TZ = datetime.now(timezone.utc).astimezone().tzinfo


# ─── Steamパス自動検出 ──────────────────────────────────────────────

def detect_steam_paths() -> tuple:
    """
    OSに応じたSteamワークショップのパスを自動検出する。
    Returns: (acf_path, content_dir) or (None, None)
    """
    system = platform.system()
    candidates = []

    if system == "Darwin":  # macOS
        candidates = [
            Path.home() / "Library/Application Support/Steam/steamapps/workshop",
        ]
    elif system == "Windows":
        # デフォルトパス
        candidates = [
            Path("C:/Program Files (x86)/Steam/steamapps/workshop"),
            Path("C:/Program Files/Steam/steamapps/workshop"),
        ]
        # カスタムインストール: レジストリから取得を試みる
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\WOW6432Node\Valve\Steam")
            steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
            winreg.CloseKey(key)
            candidates.insert(0, Path(steam_path) / "steamapps/workshop")
        except (OSError, ImportError):
            pass
    elif system == "Linux":
        candidates = [
            Path.home() / ".steam/steam/steamapps/workshop",
            Path.home() / ".local/share/Steam/steamapps/workshop",
            Path.home() / ".steam/debian-installation/steamapps/workshop",
        ]

    # Steamライブラリフォルダからも探索
    for base in list(candidates):
        steamapps = base.parent  # steamapps/
        libraryfolders_vdf = steamapps / "libraryfolders.vdf"
        if libraryfolders_vdf.exists():
            try:
                text = libraryfolders_vdf.read_text(encoding="utf-8", errors="replace")
                for match in re.finditer(r'"path"\s+"([^"]+)"', text):
                    lib_path = Path(match.group(1)) / "steamapps/workshop"
                    if lib_path not in candidates:
                        candidates.append(lib_path)
            except OSError:
                pass

    # 候補からACFファイルが存在するパスを探す
    for workshop_dir in candidates:
        acf = workshop_dir / f"appworkshop_{APP_ID}.acf"
        content = workshop_dir / "content" / APP_ID
        if acf.exists():
            return acf, content

    return None, None


# ─── VDF(Valve Data Format)パーサー ──────────────────────────────────

def parse_vdf(text: str) -> dict:
    """SteamのVDF形式テキストを辞書に変換する。"""
    result = {}
    stack = [result]
    key = None

    for token in _tokenize_vdf(text):
        if token == "{":
            new_dict = {}
            stack[-1][key] = new_dict
            stack.append(new_dict)
            key = None
        elif token == "}":
            stack.pop()
        elif key is None:
            key = token
        else:
            stack[-1][key] = token
            key = None

    return result


def _tokenize_vdf(text: str):
    """VDFテキストをトークンに分割する。"""
    i = 0
    length = len(text)
    while i < length:
        c = text[i]
        if c in (" ", "\t", "\r", "\n"):
            i += 1
        elif c == '"':
            j = i + 1
            while j < length and text[j] != '"':
                if text[j] == "\\":
                    j += 1
                j += 1
            yield text[i + 1 : j]
            i = j + 1
        elif c == "{":
            yield "{"
            i += 1
        elif c == "}":
            yield "}"
            i += 1
        elif c == "/" and i + 1 < length and text[i + 1] == "/":
            while i < length and text[i] != "\n":
                i += 1
        else:
            j = i
            while j < length and text[j] not in (" ", "\t", "\r", "\n", '"', "{", "}"):
                j += 1
            yield text[i:j]
            i = j


# ─── Mod情報取得 ─────────────────────────────────────────────────────

def get_mod_name(mod_id: str, content_dir: Path) -> str:
    """mod.infoファイルからMod名を取得する。"""
    mod_dir = content_dir / mod_id
    if not mod_dir.exists():
        return f"(ID: {mod_id})"

    # mod.infoを再帰的に探す（最大4階層）
    for depth in range(1, 5):
        pattern = "/".join(["*"] * depth) + "/mod.info"
        for mod_info_path in mod_dir.glob(pattern):
            try:
                text = mod_info_path.read_text(encoding="utf-8", errors="replace")
                match = re.search(r"^name=(.+)$", text, re.MULTILINE)
                if match:
                    return match.group(1).strip()
            except OSError:
                continue

    # mod.infoが見つからない場合、modsディレクトリ名をフォールバック
    mods_dir = mod_dir / "mods"
    if mods_dir.exists():
        subdirs = [d.name for d in mods_dir.iterdir() if d.is_dir()]
        if subdirs:
            return subdirs[0]

    return f"(ID: {mod_id})"


def format_size(size_bytes: int) -> str:
    """バイト数を読みやすい形式に変換する。"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def format_timestamp(ts: int) -> str:
    """Unixタイムスタンプをローカル日時文字列に変換する。"""
    dt = datetime.fromtimestamp(ts, tz=LOCAL_TZ)
    return dt.strftime("%Y-%m-%d %H:%M")


def days_ago_text(ts: int) -> str:
    """タイムスタンプが何日前かをテキストで返す。"""
    now = time.time()
    diff = now - ts
    days = int(diff / 86400)
    hours = int((diff % 86400) / 3600)
    if days == 0:
        if hours == 0:
            return "just now"
        return f"{hours}h ago"
    elif days == 1:
        return "yesterday"
    elif days < 30:
        return f"{days}d ago"
    elif days < 365:
        months = days // 30
        return f"~{months}mo ago"
    else:
        years = days // 365
        return f"~{years}y ago"


# ─── メイン処理 ──────────────────────────────────────────────────────

def load_acf_data(acf_path: Path) -> dict:
    """ACFファイルを読み込み、Mod情報を返す。"""
    text = acf_path.read_text(encoding="utf-8", errors="replace")
    data = parse_vdf(text)

    workshop = data.get("AppWorkshop", {})
    installed = workshop.get("WorkshopItemsInstalled", {})

    mods = {}
    for mod_id, info in installed.items():
        mods[mod_id] = {
            "size": int(info.get("size", 0)),
            "timeupdated": int(info.get("timeupdated", 0)),
            "manifest": info.get("manifest", ""),
        }

    return mods


def get_snapshot_path() -> Path:
    """スナップショットファイルのパスを返す（スクリプトと同じディレクトリ）。"""
    return Path(__file__).resolve().parent / SNAPSHOT_FILENAME


def load_snapshot(snapshot_path: Path) -> dict:
    """前回のスナップショットを読み込む。"""
    if snapshot_path.exists():
        try:
            return json.loads(snapshot_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_snapshot(snapshot_path: Path, mods: dict):
    """現在の状態をスナップショットとして保存する。"""
    snapshot = {
        "timestamp": int(time.time()),
        "mods": {
            mod_id: {
                "timeupdated": info["timeupdated"],
                "manifest": info["manifest"],
            }
            for mod_id, info in mods.items()
        },
    }
    snapshot_path.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def detect_changes(current: dict, snapshot: dict, content_dir: Path) -> dict:
    """前回のスナップショットと比較し、変更を検出する。"""
    prev_mods = snapshot.get("mods", {})
    prev_time = snapshot.get("timestamp", 0)

    updated = []
    added = []
    removed = []

    for mod_id, info in current.items():
        if mod_id not in prev_mods:
            added.append({
                "id": mod_id,
                "name": get_mod_name(mod_id, content_dir),
                "timeupdated": info["timeupdated"],
                "size": info["size"],
            })
        elif info["timeupdated"] != prev_mods[mod_id]["timeupdated"]:
            updated.append({
                "id": mod_id,
                "name": get_mod_name(mod_id, content_dir),
                "timeupdated": info["timeupdated"],
                "prev_timeupdated": prev_mods[mod_id]["timeupdated"],
                "size": info["size"],
            })

    for mod_id in prev_mods:
        if mod_id not in current:
            removed.append({
                "id": mod_id,
                "name": get_mod_name(mod_id, content_dir),
            })

    return {
        "prev_check": prev_time,
        "updated": sorted(updated, key=lambda x: x["timeupdated"], reverse=True),
        "added": sorted(added, key=lambda x: x["timeupdated"], reverse=True),
        "removed": removed,
    }


def print_changes(changes: dict):
    """変更内容を表示する。"""
    prev_time = changes["prev_check"]
    updated = changes["updated"]
    added = changes["added"]
    removed = changes["removed"]

    if prev_time:
        print(f"\n  Last check: {format_timestamp(prev_time)} ({days_ago_text(prev_time)})")
    print()

    if not updated and not added and not removed:
        print("  No changes since last check.")
        print()
        return

    if updated:
        print(f"  * Updated mods ({len(updated)})")
        print(f"  {'=' * 70}")
        for mod in updated:
            print(f"    >> {mod['name']}")
            print(f"       {format_timestamp(mod['prev_timeupdated'])} -> {format_timestamp(mod['timeupdated'])}")
            print(f"       Size: {format_size(mod['size'])}  |  ID: {mod['id']}")
            print(f"       https://steamcommunity.com/sharedfiles/filedetails/?id={mod['id']}")
            print()

    if added:
        print(f"  * Newly added mods ({len(added)})")
        print(f"  {'=' * 70}")
        for mod in added:
            print(f"    +  {mod['name']}")
            print(f"       Updated: {format_timestamp(mod['timeupdated'])}  |  Size: {format_size(mod['size'])}")
            print(f"       ID: {mod['id']}")
            print()

    if removed:
        print(f"  * Removed/unsubscribed mods ({len(removed)})")
        print(f"  {'=' * 70}")
        for mod in removed:
            print(f"    -  {mod['name']}  (ID: {mod['id']})")
        print()


def print_mod_list(mods: dict, content_dir: Path, days_filter: int = 0):
    """全Modを更新日時順に一覧表示する。"""
    mod_list = []
    for mod_id, info in mods.items():
        mod_list.append({
            "id": mod_id,
            "name": get_mod_name(mod_id, content_dir),
            "timeupdated": info["timeupdated"],
            "size": info["size"],
        })

    mod_list.sort(key=lambda x: x["timeupdated"], reverse=True)

    if days_filter > 0:
        cutoff = time.time() - (days_filter * 86400)
        filtered = [m for m in mod_list if m["timeupdated"] >= cutoff]
        print(f"\n  Mods updated in the last {days_filter} day(s) ({len(filtered)}/{len(mod_list)})")
        mod_list = filtered
    else:
        print(f"\n  All mods - sorted by update date ({len(mod_list)})")

    print(f"  {'=' * 74}")
    print(f"  {'Updated':<18} {'Ago':>10}  {'Size':>10}  Mod name")
    print(f"  {'-' * 74}")

    for mod in mod_list:
        ts_str = format_timestamp(mod["timeupdated"])
        ago = days_ago_text(mod["timeupdated"])
        size = format_size(mod["size"])
        print(f"  {ts_str:<18} {ago:>10}  {size:>10}  {mod['name']}")

    print(f"  {'=' * 74}")
    total_size = sum(m["size"] for m in mod_list)
    print(f"  Total size: {format_size(total_size)}")
    print()


def print_help():
    """ヘルプメッセージを表示する。"""
    print("""
  PZ Mod Update Checker - Detect which mods were updated

  Usage:
    python pz_mod_update_checker.py              Check for updates (snapshot comparison)
    python pz_mod_update_checker.py --list       List all mods sorted by update date
    python pz_mod_update_checker.py --days N     Show mods updated in the last N days
    python pz_mod_update_checker.py --reset      Reset the snapshot to current state
    python pz_mod_update_checker.py --help       Show this help message

  Options:
    --acf <path>       Override ACF file path (auto-detected by default)
    --content <path>   Override workshop content directory path

  The snapshot file (.pz_mod_snapshot.json) is saved next to this script.
  Add it to .gitignore if you don't want to track it.
""")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_help()
        return

    # パス検出
    acf_path, content_dir = detect_steam_paths()

    # コマンドライン引数によるオーバーライド
    for i, arg in enumerate(args):
        if arg == "--acf" and i + 1 < len(args):
            acf_path = Path(args[i + 1])
            # content_dirもACFから推定
            if content_dir is None:
                content_dir = acf_path.parent / "content" / APP_ID
        elif arg == "--content" and i + 1 < len(args):
            content_dir = Path(args[i + 1])

    # ACFファイル存在チェック
    if acf_path is None or not acf_path.exists():
        print()
        print("  ERROR: Could not find Steam workshop data for Project Zomboid.")
        print()
        if acf_path:
            print(f"  Checked: {acf_path}")
        else:
            print(f"  OS: {platform.system()}")
            print(f"  No Steam installation found in default locations.")
        print()
        print("  Please make sure:")
        print("    1. Steam is installed")
        print("    2. Project Zomboid is in your library")
        print("    3. You have subscribed to at least one workshop mod")
        print()
        print("  Or specify the path manually:")
        print(f"    python {Path(__file__).name} --acf <path to appworkshop_108600.acf>")
        print()
        sys.exit(1)

    snapshot_path = get_snapshot_path()

    print()
    print("  +====================================================+")
    print("  |  PZ Mod Update Checker                              |")
    print("  |  Project Zomboid (App ID: 108600)                   |")
    print("  +====================================================+")
    print(f"  |  OS: {platform.system():<47}|")
    print(f"  +====================================================+")

    # ACFファイルの最終更新日時を表示
    acf_mtime = os.path.getmtime(acf_path)
    print(f"\n  ACF last modified: {format_timestamp(int(acf_mtime))} ({days_ago_text(int(acf_mtime))})")

    # ACFデータ読み込み
    mods = load_acf_data(acf_path)
    print(f"  Subscribed mods:  {len(mods)}")

    # コマンド分岐
    if "--reset" in args:
        save_snapshot(snapshot_path, mods)
        print(f"\n  Snapshot has been reset.")
        print(f"  Changes will be detected from the next run.")
        print()
        return

    if "--list" in args:
        print_mod_list(mods, content_dir)
        return

    # --days オプション
    days_filter = 0
    for i, arg in enumerate(args):
        if arg == "--days" and i + 1 < len(args):
            try:
                days_filter = int(args[i + 1])
            except ValueError:
                pass

    if days_filter > 0:
        print_mod_list(mods, content_dir, days_filter)
        save_snapshot(snapshot_path, mods)
        return

    # デフォルト: スナップショット比較
    snapshot = load_snapshot(snapshot_path)

    if not snapshot:
        print(f"\n  First run - saving current state as snapshot.")
        save_snapshot(snapshot_path, mods)
        print(f"  Saved to: {snapshot_path}")
        print()
        print_mod_list(mods, content_dir, days_filter=30)
        return

    # 変更検出
    changes = detect_changes(mods, snapshot, content_dir)
    print_changes(changes)

    # スナップショット更新
    save_snapshot(snapshot_path, mods)
    print(f"  Snapshot updated.")
    print()


if __name__ == "__main__":
    main()
