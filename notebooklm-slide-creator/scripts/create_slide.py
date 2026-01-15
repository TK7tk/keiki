#!/usr/bin/env python3
"""
NotebookLM スライド自動作成スクリプト
.mdファイルからNotebookLMでスライドを生成する
"""

import argparse
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# パス設定
SCRIPT_DIR = Path(__file__).parent
SESSION_DIR = SCRIPT_DIR.parent / "session"
STORAGE_STATE_PATH = SESSION_DIR / "storage_state.json"

# デフォルトの調整フォルダ（Windows用）
DEFAULT_PROMPT_DIR = Path(r"C:\Users\西田貴彦\Documents\Cursor\西田個別作業\人事\調整")

def read_markdown_file(file_path: Path) -> str:
    """Markdownファイルを読み込む"""
    if not file_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
    if file_path.suffix.lower() != ".md":
        raise ValueError(f"Markdownファイル(.md)を指定してください: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def check_session():
    """セッションファイルの存在確認"""
    if not STORAGE_STATE_PATH.exists():
        print("エラー: セッションファイルが見つかりません。")
        print("先に login.py を実行してログインしてください。")
        print()
        print(f"  python {SCRIPT_DIR / 'login.py'}")
        sys.exit(1)

def create_slide(content_file: Path, prompt_file: Path = None, prompt_text: str = None, headless: bool = False):
    """
    NotebookLMでスライドを作成

    Args:
        content_file: ソースとなる.mdファイルのパス
        prompt_file: スライド説明用の.mdファイルのパス（任意）
        prompt_text: スライド説明用のテキスト（任意、prompt_fileより優先）
        headless: ヘッドレスモードで実行するか
    """
    check_session()

    # コンテンツ読み込み
    print(f"コンテンツファイル読み込み: {content_file}")
    content = read_markdown_file(content_file)

    # プロンプト読み込み
    slide_prompt = ""
    if prompt_text:
        slide_prompt = prompt_text
        print(f"スライド説明（テキスト指定）: {slide_prompt[:50]}...")
    elif prompt_file:
        print(f"スライド説明ファイル読み込み: {prompt_file}")
        slide_prompt = read_markdown_file(prompt_file)

    print()
    print("=" * 50)
    print("NotebookLM スライド作成開始")
    print("=" * 50)

    with sync_playwright() as p:
        # ブラウザ起動（保存済みセッション使用）
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            storage_state=str(STORAGE_STATE_PATH),
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()

        try:
            # ① NotebookLMにアクセス
            print("NotebookLMにアクセス中...")
            page.goto("https://notebooklm.google.com/", wait_until="networkidle")
            time.sleep(2)

            # ② 新規作成ボタンをクリック
            print("新規ノートブック作成中...")
            # 「新規作成」または「Create new」ボタンを探す
            create_button = page.locator('button:has-text("新規"), button:has-text("Create"), button:has-text("新しいノートブック"), [aria-label*="Create"], [aria-label*="新規"]').first
            create_button.click(timeout=10000)
            time.sleep(2)

            # ③ テキストをコピー/ペースト
            print("コンテンツを入力中...")
            # 「コピーしたテキスト」または「Copied text」オプションを探す
            text_option = page.locator('text="コピーしたテキスト", text="Copied text", text="テキスト", text="Text"').first
            text_option.click(timeout=10000)
            time.sleep(1)

            # テキストエリアにコンテンツを入力
            textarea = page.locator('textarea, [contenteditable="true"], input[type="text"]').first
            textarea.fill(content)
            time.sleep(1)

            # 挿入/追加ボタン
            insert_button = page.locator('button:has-text("挿入"), button:has-text("Insert"), button:has-text("追加"), button:has-text("Add")').first
            insert_button.click(timeout=10000)
            time.sleep(3)

            # ④ Studioのスライド資料セクションへ
            print("スライド生成セクションへ移動中...")
            # Studioタブまたはスライドオプションを探す
            studio_tab = page.locator('text="Studio", text="スタジオ", [aria-label*="Studio"]').first
            studio_tab.click(timeout=10000)
            time.sleep(2)

            # スライドの✍マーク（編集/カスタマイズボタン）を探す
            slide_edit = page.locator('[aria-label*="スライド"], [aria-label*="Slide"], text="スライド", text="Slides"').first
            slide_edit.click(timeout=10000)
            time.sleep(1)

            # カスタマイズ/編集ボタン
            customize_button = page.locator('button:has-text("カスタマイズ"), button:has-text("Customize"), [aria-label*="edit"], [aria-label*="編集"]').first
            customize_button.click(timeout=10000)
            time.sleep(1)

            # スライド説明を入力
            if slide_prompt:
                print("スライド説明を入力中...")
                prompt_input = page.locator('textarea, input[type="text"], [contenteditable="true"]').last
                prompt_input.fill(slide_prompt)
                time.sleep(1)

            # ⑤ 生成ボタンをクリック
            print("スライド生成中...")
            generate_button = page.locator('button:has-text("生成"), button:has-text("Generate"), button:has-text("作成"), button:has-text("Create")').first
            generate_button.click(timeout=10000)

            # 生成完了を待つ
            print("生成完了を待機中（最大60秒）...")
            time.sleep(5)

            # 完了確認（ダウンロードボタンや完了表示を待つ）
            try:
                page.wait_for_selector('button:has-text("ダウンロード"), button:has-text("Download"), text="完了", text="Complete"', timeout=60000)
                print()
                print("スライド生成が完了しました！")
            except PlaywrightTimeoutError:
                print()
                print("生成処理中です。ブラウザで確認してください。")

            # ブラウザを開いたまま待機（ユーザーが確認できるように）
            if not headless:
                print()
                input("確認後、Enterキーを押して終了してください: ")

            # セッション更新
            context.storage_state(path=str(STORAGE_STATE_PATH))

        except PlaywrightTimeoutError as e:
            print(f"タイムアウトエラー: {e}")
            print("NotebookLMのUIが変更された可能性があります。")
            print("手動で操作を完了してください。")
            if not headless:
                input("Enterキーを押して終了: ")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            if not headless:
                input("Enterキーを押して終了: ")
        finally:
            browser.close()

def list_prompt_files():
    """調整フォルダ内の.mdファイル一覧を表示"""
    if not DEFAULT_PROMPT_DIR.exists():
        print(f"調整フォルダが見つかりません: {DEFAULT_PROMPT_DIR}")
        return []

    md_files = list(DEFAULT_PROMPT_DIR.glob("*.md"))
    if md_files:
        print("利用可能なプロンプトファイル:")
        for i, f in enumerate(md_files, 1):
            print(f"  {i}. {f.name}")
    else:
        print("調整フォルダに.mdファイルがありません。")
    return md_files

def main():
    parser = argparse.ArgumentParser(
        description="NotebookLMでスライドを自動生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 基本的な使い方
  python create_slide.py /path/to/content.md

  # スライド説明ファイルを指定
  python create_slide.py /path/to/content.md --prompt /path/to/prompt.md

  # スライド説明をテキストで直接指定
  python create_slide.py /path/to/content.md --prompt-text "3枚構成で要点をまとめて"

  # 利用可能なプロンプトファイル一覧
  python create_slide.py --list-prompts
        """
    )

    parser.add_argument("content", nargs="?", help="ソースとなる.mdファイルのパス")
    parser.add_argument("--prompt", "-p", help="スライド説明用の.mdファイルのパス")
    parser.add_argument("--prompt-text", "-t", help="スライド説明用のテキスト（直接指定）")
    parser.add_argument("--headless", action="store_true", help="ヘッドレスモードで実行")
    parser.add_argument("--list-prompts", "-l", action="store_true", help="調整フォルダの.mdファイル一覧を表示")

    args = parser.parse_args()

    # プロンプトファイル一覧表示
    if args.list_prompts:
        list_prompt_files()
        return

    # コンテンツファイル必須チェック
    if not args.content:
        parser.print_help()
        print()
        print("エラー: コンテンツファイルを指定してください。")
        sys.exit(1)

    content_path = Path(args.content).resolve()
    prompt_path = Path(args.prompt).resolve() if args.prompt else None

    create_slide(
        content_file=content_path,
        prompt_file=prompt_path,
        prompt_text=args.prompt_text,
        headless=args.headless
    )

if __name__ == "__main__":
    main()
