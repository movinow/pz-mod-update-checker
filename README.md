# PZ Mod Update Checker

**Project Zomboid** の Steam Workshop Mod がいつ更新されたかを素早く確認するコマンドラインツール。

Steamでダウンロードが走った後、どのModが更新されたのかワークショップを開かずに確認できます。

## 解決する問題

Steamのダウンロード画面ではファイルサイズは表示されますが、**どのModが更新されたかは表示されません**。
このツールはSteamのローカルデータを解析して、更新されたModを即座に特定します。

## 必要な環境

- **Python 3.7以上**（標準ライブラリのみ使用、追加インストール不要）
- **Steam** がインストールされていること
- **Project Zomboid** のWorkshop Modをサブスクライブしていること

### 対応OS

| OS | 対応状況 | Steamパスの自動検出 |
|---|---|---|
| Windows 10/11 | ✅ | デフォルトパス + レジストリ + ライブラリフォルダ |
| macOS | ✅ | デフォルトパス + ライブラリフォルダ |
| Linux | ✅ | 一般的な3パス + ライブラリフォルダ |

## インストール

```bash
# リポジトリをクローン（または pz_mod_update_checker.py をダウンロード）
git clone https://github.com/movinow/pz-mod-update-checker.git
cd pz-mod-update-checker
```

ファイルは `pz_mod_update_checker.py` の1つだけです。好きな場所に置いて実行できます。

## 使い方

### 基本：更新チェック

```bash
python pz_mod_update_checker.py
```

**初回実行**: 現在の全Modの状態をスナップショットとして保存し、直近30日間の更新を表示します。
**2回目以降**: 前回のスナップショットと比較し、更新・追加・削除されたModを表示します。

### 全Mod一覧

```bash
python pz_mod_update_checker.py --list
```

サブスクライブ中の全Modを更新日時の新しい順に一覧表示します。

### 直近N日間の更新

```bash
python pz_mod_update_checker.py --days 7
```

直近7日間に更新されたModだけを表示します。

### スナップショットのリセット

```bash
python pz_mod_update_checker.py --reset
```

スナップショットを現在の状態で上書きします。

### ヘルプ

```bash
python pz_mod_update_checker.py --help
```

## 出力例

### 更新が検出された場合

```
  +====================================================+
  |  PZ Mod Update Checker                              |
  |  Project Zomboid (App ID: 108600)                   |
  +====================================================+
  |  OS: Windows                                        |
  +====================================================+

  ACF last modified: 2026-02-18 10:26 (just now)
  Subscribed mods:  37

  Last check: 2026-02-17 22:00 (12h ago)

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

  Snapshot updated.
```

### --days 7 の場合

```
  Mods updated in the last 7 day(s) (4/37)
  ==========================================================================
  Updated               Ago        Size  Mod name
  --------------------------------------------------------------------------
  2026-02-18 03:58      6h ago     33.9 MB  that DAMN Library 0.9848b
  2026-02-17 21:13     13h ago      3.8 MB  [Build 42] Unofficial Japanese Translation
  2026-02-13 04:18     5d ago      16.5 MB  '89 Isuzu Trooper
  2026-02-11 11:20     6d ago       4.1 MB  Skill Recovery Journal
  ==========================================================================
  Total size: 58.3 MB
```

## 仕組み

1. Steamのローカルマニフェストファイル (`appworkshop_108600.acf`) を解析
2. 各Modの更新タイムスタンプとMod名（`mod.info` から取得）を読み取り
3. 前回のスナップショット（`.pz_mod_snapshot.json`）と比較して差分を表示
4. 現在の状態をスナップショットとして保存

すべてローカルファイルの解析のみで動作します。Steam APIやネットワーク通信は使用しません。

## 高度な使い方

### Steamが非標準の場所にインストールされている場合

```bash
python pz_mod_update_checker.py --acf "D:\SteamLibrary\steamapps\workshop\appworkshop_108600.acf"
```

### Modコンテンツフォルダを手動指定

```bash
python pz_mod_update_checker.py --content "D:\SteamLibrary\steamapps\workshop\content\108600"
```

## ファイル

| ファイル | 説明 |
|---------|------|
| `pz_mod_update_checker.py` | メインスクリプト（これだけで動作） |
| `.pz_mod_snapshot.json` | スナップショット（自動生成、`.gitignore` 推奨） |

## ライセンス

MIT License
