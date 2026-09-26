#!/usr/bin/env bash
# Foreman bootstrap. Public repo:
#   curl -fsSL https://raw.githubusercontent.com/YOUR_GITHUB_USER/foreman/main/install.sh | bash -s -- --build
# Private repo (uses your gh login):
#   gh repo clone YOUR_GITHUB_USER/foreman ~/.claude/foreman && ~/.claude/foreman/install.sh --build
#
# Options:
#   --build          start Claude Code and begin (or resume) the Foreman build when setup finishes
#   --no-plugins     skip setup-plugins.sh
#   anything else    passed through to setup-plugins.sh (e.g. --security, --docs, --apply-conflicts)
# Environment:
#   FOREMAN_REPO     git URL to clone (default below)
#   FOREMAN_HOME     where to put it (default ~/.claude/foreman; BUILD_PROMPT.md assumes this path)
set -euo pipefail

FOREMAN_REPO="${FOREMAN_REPO:-https://github.com/YOUR_GITHUB_USER/foreman.git}"
FOREMAN_HOME="${FOREMAN_HOME:-$HOME/.claude/foreman}"

BUILD=0 PLUGINS=1 PASS=()
for arg in "$@"; do
  case "$arg" in
    --build) BUILD=1 ;;
    --no-plugins) PLUGINS=0 ;;
    -h|--help) sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) PASS+=("$arg") ;;
  esac
done

say() { printf '\033[1m==>\033[0m %s\n' "$*"; }
die() { printf 'foreman: %s\n' "$*" >&2; exit 1; }
for bin in git claude; do command -v "$bin" >/dev/null 2>&1 || die "'$bin' is required but not on PATH"; done

# 1. Get or update the repo
if [ -d "$FOREMAN_HOME/.git" ]; then
  say "Updating $FOREMAN_HOME"
  if [ -z "$(git -C "$FOREMAN_HOME" status --porcelain --untracked-files=no)" ] &&
     [ "$(git -C "$FOREMAN_HOME" rev-parse --abbrev-ref HEAD)" = main ]; then
    git -C "$FOREMAN_HOME" pull --ff-only --quiet || say "Couldn't fast-forward; leaving the local copy as is"
  else
    say "Local changes or a non-main branch checked out (e.g. a Foreman build in progress); not pulling"
  fi
elif [ -e "$FOREMAN_HOME" ]; then
  die "$FOREMAN_HOME exists but isn't a git repo; move it aside first"
else
  case "$FOREMAN_REPO" in
    *YOUR_GITHUB_USER*) die "set FOREMAN_REPO=<git url>, or run ./configure-repo.sh <github-user> before pushing" ;;
  esac
  say "Cloning $FOREMAN_REPO -> $FOREMAN_HOME"
  mkdir -p "$(dirname "$FOREMAN_HOME")"
  git clone --quiet "$FOREMAN_REPO" "$FOREMAN_HOME"
fi
mkdir -p "$FOREMAN_HOME/state" "$FOREMAN_HOME/local" "$FOREMAN_HOME/backups"
chmod +x "$FOREMAN_HOME"/*.sh

# 2. Curated plugins
if [ "$PLUGINS" = 1 ]; then
  say "Setting up plugins"
  "$FOREMAN_HOME/setup-plugins.sh" --build-tools ${PASS[@]+"${PASS[@]}"}
fi

# 3. The Foreman plugin itself, from this repo as a local marketplace (loads in place: edits apply on /reload-plugins)
say "Installing the Foreman plugin"
claude plugin marketplace add "$FOREMAN_HOME" >/dev/null 2>&1 || true
claude plugin install foreman@foreman --scope user >/dev/null 2>&1 || die "couldn't install foreman@foreman (run: claude plugin validate $FOREMAN_HOME)"

say "Foreman is installed at $FOREMAN_HOME"
if [ "$BUILD" = 1 ] && [ -r /dev/tty ]; then
  say "Starting the build (it pauses once for plan approval unless BUILD_GATE is off)"
  cd "$FOREMAN_HOME"
  exec claude "Run the Foreman build: read $FOREMAN_HOME/BUILD_PROMPT.md in full and execute it. If $FOREMAN_HOME/local/PLAN.md exists, resume from it instead of starting over." </dev/tty
fi
printf '\nNext: start Claude Code anywhere and run  /foreman:build\n'
