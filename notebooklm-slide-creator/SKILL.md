---
name: notebooklm-slide-creator
description: NotebookLMを使ってMarkdownファイルからスライドを自動生成するスキル。Playwrightでブラウザを自動操作し、.mdファイルをNotebookLMにアップロードしてスライド資料を作成する。「NotebookLMでスライド作成」「.mdからプレゼン資料を生成」「NotebookLM自動化」などのリクエストで使用。
---

# NotebookLM スライド自動作成スキル
## 概要

Playwrightを使ってGoogle NotebookLMのブラウザ操作を自動化し、Markdownファイルからスライド資料を生成する。

## 前提条件

- Python 3.8以上
- Playwright (`pip install playwright && playwright install chromium`)
- Googleアカウント

## セットアップ

### 1. Playwrightインストール

```bash
pip install playwright
playwright install chromium
```

### 2. 初回ログイン（セッション保存）

```bash
python scripts/login.py
```

ブラウザが開くので、Googleアカウントでログイン。完了後Enterキーを押すとセッションが保存される。

## 使い方

### 基本コマンド

```bash
# .mdファイルからスライド生成
python scripts/create_slide.py /path/to/content.md

# スライド説明ファイルを指定
python scripts/create_slide.py /path/to/content.md --prompt /path/to/prompt.md

# スライド説明をテキストで直接指定
python scripts/create_slide.py /path/to/content.md --prompt-text "3枚構成で要点をまとめて"

# 利用可能なプロンプトファイル一覧
python scripts/create_slide.py --list-prompts
```

### オプション

| オプション | 説明 |
|-----------|------|
| `--prompt`, `-p` | スライド説明用の.mdファイルパス |
| `--prompt-text`, `-t` | スライド説明テキスト（直接指定） |
| `--headless` | ヘッドレスモードで実行 |
| `--list-prompts`, `-l` | 調整フォルダの.md一覧表示 |

### ディレクトリ構成

```
C:\Users\西田貴彦\Documents\Cursor\西田個別作業\人事\
├── 02OUTPUT\          # ソースとなる.mdファイル
└── 調整\              # スライド説明用プロンプト.mdファイル
```

## ワークフロー

1. `login.py`でGoogleログイン（初回のみ）
2. `create_slide.py`でコンテンツ.mdファイルを指定
3. 必要に応じてスライド説明を指定
4. NotebookLMが自動でスライド生成

## トラブルシューティング

### セッション切れ

再度`login.py`を実行してログインし直す。

### UI変更によるエラー
NotebookLMのUIが更新された場合、セレクタの調整が必要。`create_slide.py`内のlocator部分を修正。
### タイムアウト

ネットワーク遅延時は`time.sleep()`の値を増やす。
