# Foreman

A self-orchestration layer for Claude Code. Give it a terse request (`FIX: login times out on slow wifi`) and it plans, sequences, executes, verifies, and records the work in one central place. It stays focused on the current task, captures new requests instead of jumping to them, and resumes exactly where it left off after `/compact` or a new session.

This repo starts as a **bootstrap**: `BUILD_PROMPT.md` is the spec, and Claude Code builds the full system on your machine from it, dogfooding as it goes.

## Install (one line)

Public repo:

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_GITHUB_USER/foreman/main/install.sh | bash -s -- --build
```

Private repo (uses your `gh` login):

```bash
gh repo clone YOUR_GITHUB_USER/foreman ~/.claude/foreman && ~/.claude/foreman/install.sh --build
```

Leave off `--build` to set up without starting; later, run `/foreman:build` in any Claude Code session. Extra flags pass through to the plugin setup: `--security` (Trail of Bits security skills), `--docs` (Office/PDF skills), `--apply-conflicts` (disable plugins that compete with Foreman instead of just reporting them), `--no-plugins`.

## First-time publish

```bash
./configure-repo.sh <your-github-user>          # rewrites the placeholders above and commits
gh repo create foreman --private --source . --push
```

## What `install.sh` does

1. Clones this repo to `~/.claude/foreman` (or fast-forwards it if it's clean and on `main`).
2. Runs `setup-plugins.sh`: installs the curated plugins that are missing, installs language-server plugins only when the server is on your PATH, and reports conflicting or heavy plugins. It never uninstalls anything.
3. Registers this repo as a local plugin marketplace and installs `foreman@foreman`. Local marketplaces load in place, so edits under `plugin/` apply on `/reload-plugins`.
4. With `--build`, opens Claude Code and starts (or resumes) the build.

## What the build does

Recon and backup, then a plan that pauses once for your approval, then the build itself: the `fm` state CLI, hooks, skills, rules, read-only recon agents, memory hygiene, a self-check (`fm doctor`), and end-to-end tests. It commits to the `foreman/build` branch and never pushes. When it's done, `MASTER.md` explains every file and how the parts interact.

## Using it (after the build)

```
FIX: login times out after 30s on slow networks
FEATURE: export report as CSV @src/reports
CLEAN: collapse the three date helpers into one
```

Work runs in the order CLEAN → PERFORMANCE → SECURITY → FIX → FEATURE after a baseline check. Plain one-line requests get the same treatment. Mid-task ideas are captured and queued; `NOW:` switches tasks, `PAUSE` checkpoints, `/foreman:status` shows where things stand.

## Layout

```
BUILD_PROMPT.md       the spec Claude Code builds from
install.sh            one-liner bootstrap
setup-plugins.sh      curated plugin setup (safe to re-run; --dry-run to preview)
configure-repo.sh     one-time: point everything at your GitHub repo
.claude-plugin/       local marketplace "foreman"
plugin/               the Foreman plugin (bootstrap: /foreman:build)
local/ state/ backups/   machine-specific, gitignored
```

## Plugin choices

The reasoning, measured context costs, and conflicts are in `BUILD_PROMPT.md` (§4.6 and Appendix A). Preview what `setup-plugins.sh` would change with `./setup-plugins.sh --dry-run`.

## Updating and removing

- Update: rerun `~/.claude/foreman/install.sh`, or `git pull` in `~/.claude/foreman`.
- Remove the bootstrap: `claude plugin uninstall foreman@foreman && claude plugin marketplace remove foreman`. The full build adds an `uninstall.sh`.
