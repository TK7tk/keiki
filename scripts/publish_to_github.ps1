param(
  [Parameter(Mandatory = $true)]
  [string]$RepoUrl,

  [string]$Branch = "main",
  [string]$CommitMessage = "chore: sync"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Exec([string]$Cmd) {
  Write-Host ">> $Cmd"
  & $env:COMSPEC /c $Cmd
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed (exit=$LASTEXITCODE): $Cmd"
  }
}

Write-Host "cwd: $(Get-Location)"

# Init repo if needed
if (-not (Test-Path -LiteralPath ".git")) {
  Exec "git init"
}

# Ensure branch name
Exec "git branch -M $Branch"

# Ensure origin points to RepoUrl
$origin = (& git remote get-url origin 2>$null)
if (-not $origin) {
  Exec "git remote add origin $RepoUrl"
} else {
  Exec "git remote set-url origin $RepoUrl"
}

# Require git identity (avoid accidental placeholder commits)
$name = (& git config user.name)
$email = (& git config user.email)
if (-not $name -or -not $email) {
  Write-Host "git user.name / user.email が未設定です。先に設定してください:" -ForegroundColor Yellow
  Write-Host "  git config --global user.name \"<your name>\"" -ForegroundColor Yellow
  Write-Host "  git config --global user.email \"<your email>\"" -ForegroundColor Yellow
  exit 1
}

# Stage everything (respects .gitignore)
Exec "git add -A"

# Commit only if there are changes
$status = (& git status --porcelain)
if (-not $status) {
  Write-Host "No changes to commit."
  exit 0
}

Exec "git commit -m `"$CommitMessage`""

# Push
Exec "git push -u origin $Branch"

Write-Host "Done: pushed to $RepoUrl ($Branch)"

