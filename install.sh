#!/usr/bin/env bash
# Foreman bootstrap. Public repo:
#   curl -fsSL https://raw.githubusercontent.com/ChaseSunstrom/foreman/main/install.sh | bash
# Private repo (uses your gh login):
#   gh repo clone ChaseSunstrom/foreman ~/.claude/foreman && ~/.claude/foreman/install.sh
#
# Options:
#   --build          open Claude Code on the Foreman build (rebuild or resume from BUILD_PROMPT.md)
#   --no-plugins     skip setup-plugins.sh
#   --no-bypass      don't set bypassPermissions as the default permission mode
#   --no-wiring      don't wire Foreman into ~/.claude (statusLine wrapper, deny rules, CLAUDE.md block, rules symlink)
#   anything else    passed through to setup-plugins.sh (e.g. --security, --docs, --apply-conflicts)
# Environment:
#   FOREMAN_REPO     git URL to clone (default below)
#   FOREMAN_HOME     where to put it (default ~/.claude/foreman; BUILD_PROMPT.md assumes this path)
set -euo pipefail

FOREMAN_REPO="${FOREMAN_REPO:-https://github.com/ChaseSunstrom/foreman.git}"
FOREMAN_HOME="${FOREMAN_HOME:-$HOME/.claude/foreman}"

BUILD=0 PLUGINS=1 BYPASS=1 WIRING=1 PASS=()
for arg in "$@"; do
  case "$arg" in
    --build) BUILD=1 ;;
    --no-plugins) PLUGINS=0 ;;
    --no-bypass) BYPASS=0 ;;
    --no-wiring) WIRING=0 ;;
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
  placeholder="YOUR_GITHUB""_USER"   # split so configure-repo.sh doesn't rewrite this check
  case "$FOREMAN_REPO" in
    *"$placeholder"*) die "set FOREMAN_REPO=<git url>, or run ./configure-repo.sh <github-user> before pushing" ;;
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

# 4. Permission mode: bypass by default (Foreman's guard hook + deny rules are the brakes; see BUILD_PROMPT.md §4.7)
if [ "$BYPASS" = 1 ]; then
  settings="$HOME/.claude/settings.json"
  mkdir -p "$HOME/.claude"
  [ -f "$settings" ] && cp "$settings" "$FOREMAN_HOME/backups/settings.json.$(date +%Y%m%d-%H%M%S)"
  if command -v python3 >/dev/null 2>&1 && python3 - "$settings" "$FOREMAN_HOME/state/install-manifest.json" <<'PY'
import json, os, sys
path, manifest = sys.argv[1], sys.argv[2]
data = json.load(open(path)) if os.path.exists(path) and os.path.getsize(path) else {}
# Record the mode we found before the first change, so uninstall can restore it.
m = json.load(open(manifest)) if os.path.exists(manifest) else {}
if "defaultMode_original" not in m:
    m["defaultMode_original"] = (data.get("permissions") or {}).get("defaultMode")
    os.makedirs(os.path.dirname(manifest), exist_ok=True)
    with open(manifest + ".tmp", "w") as f:
        json.dump(m, f, indent=2, sort_keys=True)
    os.replace(manifest + ".tmp", manifest)
data.setdefault("permissions", {})["defaultMode"] = "bypassPermissions"
tmp = path + ".foreman-tmp"
with open(tmp, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
os.replace(tmp, path)
PY
  then
    say "Default permission mode: bypassPermissions (Claude Code asks you to confirm once on next launch)"
  else
    say "Couldn't update $settings; add  \"permissions\": {\"defaultMode\": \"bypassPermissions\"}  yourself"
  fi
fi

# 5. Foreman user wiring (reversible: plugin/uninstall.sh or `fm uninstall-user`)
if [ "$WIRING" = 1 ]; then
  say "Wiring Foreman into ~/.claude (statusLine wrapper, deny rules, CLAUDE.md block, rules symlink)"
  python3 "$FOREMAN_HOME/plugin/bin/fm" install-user || say "Wiring failed; run: $FOREMAN_HOME/plugin/bin/fm install-user --dry-run"
fi

say "Foreman is installed at $FOREMAN_HOME"
if [ "$BUILD" = 1 ] && [ -r /dev/tty ]; then
  say "Starting the build (it pauses once for plan approval unless BUILD_GATE is off)"
  cd "$FOREMAN_HOME"
  exec claude "Run the Foreman build: read $FOREMAN_HOME/BUILD_PROMPT.md in full and execute it. If $FOREMAN_HOME/local/PLAN.md exists, resume from it instead of starting over." </dev/tty
fi
printf '\nNext: start Claude Code in any repo and give it a request (e.g. FIX: ...).\n      /foreman:status shows where things stand; %s/MASTER.md explains everything.\n' "$FOREMAN_HOME"
