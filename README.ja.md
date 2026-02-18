# PZ Mod Update Checker

**[English README](README.md)**

**Project Zomboid（プロジェクトゾンボイド）** のSteam Workshop Modが更新されたとき、**どのModが更新されたか**をすぐに確認できるツールです。

![Windows](https://img.shields.io/badge/Windows-10%2F11-blue) ![macOS](https://img.shields.io/badge/macOS-supported-green) ![Linux](https://img.shields.io/badge/Linux-supported-orange) ![Python](https://img.shields.io/badge/Python-3.7+-yellow)

## こんな経験ありませんか？

> Steamを起動したら「Project Zomboid - Workshop コンテンツ」のダウンロードが始まった。
> 終わったけど...  **一体どのModが更新されたの？？**

Steamはダウンロードサイズしか教えてくれません。どのModが更新されたか知るには、ワークショップを開いて一つ一つ確認する必要があります。

**このツールを使えば、すぐに答えがわかります。**（Windows: ダブルクリック / macOS・Linux: ターミナル）

## 出力例

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

## ダウンロード

**[📦 最新版をダウンロード（zip）](https://github.com/movinow/pz-mod-update-checker/releases/latest)**

1. 上のリンクから `.zip` ファイルをダウンロード
2. 好きな場所に展開（解凍）

> ⚠️ **Pythonが必要です**（まだの方は[下のガイド](#pythonのインストール)を参照）

---

## 使い方

### Windows（メニュー形式）

**`check_mod_updates.bat`** をダブルクリックすると、以下のメニューが表示されます：

```
  +====================================================+
  |  PZ Mod Update Checker                              |
  +====================================================+

  [OK] Python 3.xx.x

  ----------------------------------------------------
  [1] Check for mod updates         ... 更新されたModを表示
  [2] List all mods (by update date) ... 全Modを更新日時順に一覧
  [3] Show recently updated mods     ... 直近7日間に更新されたMod
  [4] Reset snapshot                 ... 記録をリセット
  [0] Exit                           ... 終了
  ----------------------------------------------------

  Select [1-4, 0]:
```

番号を入力してEnterを押すだけで実行できます。

| 番号 | 機能 | 説明 |
|:----:|------|------|
| **1** | 更新チェック | 前回の実行からどのModが更新されたかを表示します。初回は現在の状態を記録して、直近30日間の更新を一覧表示します |
| **2** | 全Mod一覧 | サブスクライブしている全Modを更新日時の新しい順に一覧表示します |
| **3** | 直近の更新 | 直近7日間に更新されたModだけを表示します |
| **4** | リセット | 記録をリセットします。次回の実行時に「初回」として扱われます |

### macOS / Linux

ターミナルからPythonスクリプトを直接実行します：

```bash
python3 pz_mod_update_checker.py            # 更新チェック
python3 pz_mod_update_checker.py --list     # 全Mod一覧
python3 pz_mod_update_checker.py --days 7   # 直近7日間の更新
python3 pz_mod_update_checker.py --reset    # 記録のリセット
```

---

## Pythonのインストール

このツールの実行にはPython（バージョン3.7以上）が必要です。追加ライブラリは不要です。

### Windows

**方法1: Microsoft Store（おすすめ・簡単）**
1. Microsoft Storeを開く
2. 「Python」で検索
3. 「Python 3.xx」の「入手」をクリック

**方法2: 公式サイト**
1. https://www.python.org/downloads/ にアクセス
2. 「Download Python 3.xx」をクリック
3. インストーラーを実行
4. ⚠️ **「Add Python to PATH」にチェックを入れてからインストール**

### macOS

macOSにはPython 3がプリインストールされていることが多いです。
もし入っていない場合は、ターミナルを開いて以下を実行：

```
xcode-select --install
```

### Linux

ほとんどのディストリビューションにプリインストール済みです。
もし入っていない場合：

```bash
# Ubuntu / Debian
sudo apt install python3

# Fedora
sudo dnf install python3
```

---

## よくある質問

### Q: ゲームやSteamを起動する必要がありますか？

**いいえ。** ゲームもSteamも起動していなくても使えます。Steamが過去にディスクに保存したファイルを読み取るだけなので、オフラインでも動作します。

### Q: 安全ですか？何かに接続しますか？

**完全にオフラインで動作します。** ネットワーク通信は一切行いません。Steamがローカルに保存しているファイルを読み取るだけです。

### Q: 「Python is not installed」と出ます

Pythonがインストールされていない場合、以下のような画面が表示されます：

```
  +====================================================+
  |  PZ Mod Update Checker                              |
  +====================================================+

  [!] Python is not installed.

  This tool requires Python 3.7 or later.
```

このツールの実行にはPythonが必要です。以下のどちらかの方法でインストールしてください：

**方法1: Microsoft Store（おすすめ・最も簡単）**
1. Windowsキーを押して「**store**」と入力 → Microsoft Storeを開く
2. 「**Python 3**」で検索
3. 「**Python 3.xx**」（数字が一番大きいもの）の「**入手**」をクリック
4. インストール完了後、もう一度 `check_mod_updates.bat` をダブルクリック

**方法2: 公式サイトからインストール**
1. https://www.python.org/downloads/ にアクセス
2. 「**Download Python 3.xx**」ボタンをクリック
3. ダウンロードしたインストーラーを実行
4. ⚠️ 最初の画面で **「Add Python to PATH」に必ずチェックを入れてから** 「Install Now」をクリック
5. インストール完了後、もう一度 `check_mod_updates.bat` をダブルクリック

> **注意:** Windows 10/11には `python` コマンドが最初から存在しているように見えることがありますが、これはMicrosoft Storeへの誘導用のショートカット（App Execution Alias）であり、実際のPythonではありません。上記の方法で本物のPythonをインストールする必要があります。

### Q: 「ACFファイルが見つかりません」と出ます

- Steamがインストールされているか確認してください
- Project ZomboidのWorkshop Modを1つ以上サブスクライブしていることを確認してください
- 一度もModをダウンロードしていない場合、Steamを起動してModを同期させてください
- Steamを非標準の場所にインストールしている場合は `--acf` オプションで手動指定できます：
  ```
  python pz_mod_update_checker.py --acf "D:\SteamLibrary\steamapps\workshop\appworkshop_108600.acf"
  ```

### Q: Mod名が「(ID: xxxxx)」と表示されます

そのModのデータが正しくダウンロードされていない可能性があります。Steamでゲームの「ローカルファイルの整合性を確認」を実行してみてください。

### Q: データはどこに保存されますか？

スナップショット（`.pz_mod_snapshot.json`）が **このツールと同じフォルダ内** に1つだけ作成されます。それ以外の場所にはファイルを作成しません。レジストリやシステム設定も変更しません。

### Q: アンインストールするには？

**展開したフォルダをそのまま削除するだけです。** ゲームデータやSteamのファイルには一切変更を加えていないので、フォルダを消せば何も残りません。

---

## 仕組み（技術的な説明）

1. Steamのローカルマニフェストファイル（`appworkshop_108600.acf`）を解析
2. 各Modの更新タイムスタンプとMod名を読み取り、初回時はスナップショットを作成
3. 前回のスナップショットと比較して差分を表示
4. 現在の状態を次回のためにスナップショットとして保存

Steam APIやネットワーク通信は使用しません。すべてローカルファイルの解析で完結します。

---

## ライセンス

MIT License - 自由に使用・改変・再配布できます。
