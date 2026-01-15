## Workflow: GitHubへ一発でpush（ローカル→GitHub）

このリポジトリの内容を、指定したGitHubリポジトリへまとめてpushする手順です。

### 前提

- `git` がインストール済み
- GitHubにpushできる認証が済んでいる
  - 例: Git Credential Manager / ブラウザで認証 / PAT など

### 1発実行（推奨）

PowerShellで、リポジトリ直下で実行します。

```powershell
.\scripts\publish_to_github.ps1 -RepoUrl "https://github.com/TK7tk/keiki.git"
```

### よくある運用

- 既に `origin` がある場合は、`-RepoUrl` のURLに差し替えてpushします
- 追加したくないファイルが出てきたら、`.gitignore` に追記します（例: 大きい生成物、ローカル専用メモ等）

