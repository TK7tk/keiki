#!/usr/bin/env python3
"""
NotebookLM 初回ログイン用スクリプト
ブラウザを開いてGoogleログインを行い、セッションを保存する
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# セッション保存先ディレクトリ
SESSION_DIR = Path(__file__).parent.parent / "session"

def login():
    """NotebookLMにログインしてセッションを保存"""

    # セッションディレクトリ作成
    SESSION_DIR.mkdir(exist_ok=True)

    print("=" * 50)
    print("NotebookLM ログイン")
    print("=" * 50)
    print()
    print("ブラウザが開きます。Googleアカウントでログインしてください。")
    print("ログイン完了後、NotebookLMのホーム画面が表示されたら")
    print("このターミナルでEnterキーを押してください。")
    print()

    with sync_playwright() as p:
        # ブラウザ起動（セッション保存用のコンテキスト）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            storage_state=None,
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        # NotebookLMにアクセス
        page.goto("https://notebooklm.google.com/")

        print("ブラウザでログインを完了してください...")
        print()

        # ユーザーがログインするのを待つ
        input("ログイン完了後、Enterキーを押してください: ")

        # セッションを保存
        storage_state_path = SESSION_DIR / "storage_state.json"
        context.storage_state(path=str(storage_state_path))

        print()
        print(f"セッションを保存しました: {storage_state_path}")
        print("今後は create_slide.py を使ってスライドを作成できます。")

        browser.close()

if __name__ == "__main__":
    login()
