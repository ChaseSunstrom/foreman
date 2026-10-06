#!/usr/bin/env bash
# Foreman bootstrap. Public repo:
#   curl -fsSL https://raw.githubusercontent.com/ChaseSunstrom/foreman/main/install.sh | bash
# Private repo (uses your gh login):
#   gh repo clone ChaseSunstrom/foreman ~/.claude/foreman && ~/.claude/foreman/install.sh
#
# Options:
#   --build          open Claude Code on the Foreman build (rebuild or resume from BUILD_PROMPT.md)
#   --desktop        also install Foreman Desktop from its newest release (Linux x86_64 AppImage, macOS app)
#   --no-plugins     skip setup-plugins.sh
#   --no-bypass      don't set bypassPermissions as the default permission mode
#   --no-mod         don't install the foreman-ui mod (band above the prompt, dashboard pane, toasts)
#   --no-wiring      don't wire Foreman into ~/.claude (statusLine wrapper, deny rules, CLAUDE.md block, rules symlink)
#   anything else    passed through to setup-plugins.sh (e.g. --security, --docs, --apply-conflicts)
# Environment:
#   FOREMAN_REPO     git URL to clone (default below)
#   FOREMAN_HOME     where to put it (default ~/.claude/foreman; BUILD_PROMPT.md assumes this path)
#   FOREMAN_DESKTOP_REPO  GitHub owner/repo the desktop app's releases come from (default below)
set -euo pipefail

FOREMAN_REPO="${FOREMAN_REPO:-https://github.com/ChaseSunstrom/foreman.git}"
FOREMAN_HOME="${FOREMAN_HOME:-$HOME/.claude/foreman}"
FOREMAN_DESKTOP_REPO="${FOREMAN_DESKTOP_REPO:-ChaseSunstrom/foreman-desktop}"

BUILD=0 PLUGINS=1 BYPASS=1 WIRING=1 MOD=1 DESKTOP=0 PASS=()
for arg in "$@"; do
  case "$arg" in
    --build) BUILD=1 ;;
    --desktop) DESKTOP=1 ;;
    --no-plugins) PLUGINS=0 ;;
    --no-bypass) BYPASS=0 ;;
    --no-mod) MOD=0 ;;
    --no-wiring) WIRING=0 ;;
    -h|--help) sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) PASS+=("$arg") ;;
  esac
done

say() { printf '\033[1m==>\033[0m %s\n' "$*"; }
die() { printf 'foreman: %s\n' "$*" >&2; exit 1; }
for bin in git claude; do command -v "$bin" >/dev/null 2>&1 || die "'$bin' is required but not on PATH"; done

# 0. Python: fm and every hook run on the python3 on PATH. Foreman needs 3.12.7+: older ones break `communicate()`
#    on a closed stdin, and argparse before 3.12.7 (and in 3.13.0) drops `fm task evidence ID --ac N CMD RESULT`.
py_ok() { python3 -c 'import sys; v = sys.version_info[:3]; sys.exit(not (v >= (3, 12, 7) and v != (3, 13, 0)))' >/dev/null 2>&1; }
if ! py_ok; then
  case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) die "Foreman needs Linux or macOS; on Windows, install it inside WSL" ;; esac
  have="$(python3 --version 2>&1)" || have="no python3"
  if [ "$(uname -s)" = Darwin ] && command -v brew >/dev/null 2>&1; then
    say "Installing Python with Homebrew (found: $have; Foreman needs 3.12.7+)"
    brew install python
  else
    if ! command -v uv >/dev/null 2>&1; then
      command -v curl >/dev/null 2>&1 || die "found $have; Foreman needs Python 3.12.7+ (install it, or curl so uv can)"
      say "Installing uv to install Python (no sudo needed)"
      curl -LsSf https://astral.sh/uv/install.sh | sh
      export PATH="$HOME/.local/bin:$PATH"
    fi
    say "Installing Python 3.13 with uv (found: $have; Foreman needs 3.12.7+)"
    uv python install 3.13 --default
    uv python update-shell   # later shells, and so the hooks, find it too
    export PATH="$(uv python dir --bin):$PATH"
  fi
  hash -r
  py_ok || die "python3 on PATH is still $(python3 --version 2>&1); put the new one's folder ahead of it on PATH and rerun"
fi

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
  [ "$BUILD" = 1 ] && PASS+=(--build-tools)   # plugin-dev: only needed while building Foreman itself
  "$FOREMAN_HOME/setup-plugins.sh" ${PASS[@]+"${PASS[@]}"}
fi

# 3. The Foreman plugin itself, from this repo as a local marketplace (loads in place: edits apply on /reload-plugins)
say "Installing the Foreman plugin"
claude plugin marketplace add "$FOREMAN_HOME" >/dev/null 2>&1 || true
claude plugin install foreman@foreman --scope user >/dev/null 2>&1 || die "couldn't install foreman@foreman (run: claude plugin validate $FOREMAN_HOME)"
# The UI mod (band, pane, toasts) is optional: builds without function-hook plugins keep the statusline and fm watch
if [ "$MOD" = 1 ]; then
  if claude plugin install foreman-ui@foreman --scope user >/dev/null 2>&1; then
    say "  installed foreman-ui (band, /fm pane, toasts; --no-mod skips it, claude plugin disable foreman-ui@foreman turns it off)"
  else
    say "  (foreman-ui not installed: this Claude Code build has no mods; the statusline and fm watch still work)"
  fi
fi

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
    # What existed before Foreman touched anything, so uninstall can remove what we created (fm install-user keeps these).
    m.setdefault("settings_created", not data)
    m.setdefault("permissions_created", "permissions" not in data)
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

# 6. Foreman Desktop (--desktop): the newest release's build for this machine, no Rust or bun needed here
if [ "$DESKTOP" = 1 ]; then
  asset() {  # the download URL of the newest release's asset whose name ends with $1
    curl -fsSL "https://api.github.com/repos/$FOREMAN_DESKTOP_REPO/releases/latest" | python3 -c '
import json, sys
print(next(a["browser_download_url"] for a in json.load(sys.stdin)["assets"] if a["name"].endswith(sys.argv[1])))' "$1" \
      || die "the newest Foreman Desktop release ($FOREMAN_DESKTOP_REPO) has no *$1"
  }
  case "$(uname -s)/$(uname -m)" in
    Linux/x86_64)
      url="$(asset _amd64.AppImage)"
      mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications"
      curl -fsSL "$url" -o "$HOME/.local/bin/foreman-desktop.part"
      chmod +x "$HOME/.local/bin/foreman-desktop.part"
      mv "$HOME/.local/bin/foreman-desktop.part" "$HOME/.local/bin/foreman-desktop"
      printf '[Desktop Entry]\nType=Application\nName=Foreman\nComment=Every project, session and agent on every device\nExec=%s\nTerminal=false\nCategories=Development;\n' \
        "$HOME/.local/bin/foreman-desktop" > "$HOME/.local/share/applications/foreman-desktop.desktop"
      say "Foreman Desktop installed: $HOME/.local/bin/foreman-desktop (and in your app menu)" ;;
    Darwin/*)
      url="$(asset .dmg)"
      dmg="$(mktemp -d)/foreman.dmg" mnt="$(mktemp -d)"
      curl -fsSL "$url" -o "$dmg"
      hdiutil attach -nobrowse -quiet -mountpoint "$mnt" "$dmg"
      mkdir -p "$HOME/Applications"
      rm -rf "$HOME/Applications/Foreman.app"
      cp -R "$mnt/Foreman.app" "$HOME/Applications/"
      hdiutil detach -quiet "$mnt"
      say "Foreman Desktop installed: $HOME/Applications/Foreman.app" ;;
    *) die "Foreman Desktop has builds for Linux x86_64 and macOS; build it from https://github.com/$FOREMAN_DESKTOP_REPO" ;;
  esac
fi

say "Foreman is installed at $FOREMAN_HOME"
if [ "$BUILD" = 1 ] && (: </dev/tty) 2>/dev/null; then   # a terminal we can actually open (not just a device node)
  say "Starting the build (it pauses once for plan approval unless BUILD_GATE is off)"
  cd "$FOREMAN_HOME"
  exec claude "Run the Foreman build: read $FOREMAN_HOME/BUILD_PROMPT.md in full and execute it. If $FOREMAN_HOME/local/PLAN.md exists, resume from it instead of starting over." </dev/tty
fi
printf '\nNext: start Claude Code in any repo and give it a request (e.g. FIX: ...).\n      /foreman:status shows where things stand; %s/MASTER.md explains everything.\n' "$FOREMAN_HOME"
