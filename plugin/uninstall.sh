#!/usr/bin/env bash
# Remove Foreman from this machine.
#   1. undo the ~/.claude wiring recorded in state/install-manifest.json (statusLine, deny rules, env,
#      CLAUDE.md block, rules symlink, permission mode)
#   2. uninstall the foreman@foreman plugin and the local "foreman" marketplace
#   3. keep state/ unless you confirm (it is archived to backups/ before it is removed)
# Usage: plugin/uninstall.sh [--dry-run] [--purge-state] [--yes]
# Plugins Foreman disabled are listed with the command to re-enable them; nothing else is touched.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
FOREMAN_HOME="${FOREMAN_HOME:-$(dirname "$HERE")}"
export FOREMAN_HOME
DRY=0 PURGE=0 YES=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --purge-state) PURGE=1 ;;
    --yes|-y) YES=1 ;;
    -h|--help) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "uninstall: unknown option '$arg'" >&2; exit 2 ;;
  esac
done
say() { printf '\033[1m==>\033[0m %s\n' "$*"; }
run() { if [ "$DRY" = 1 ]; then echo "    (dry-run) $*"; else "$@"; fi; }

manifest="$FOREMAN_HOME/state/install-manifest.json"
if [ -f "$manifest" ]; then
  disabled="$(python3 -c 'import json,sys; print(" ".join(json.load(open(sys.argv[1])).get("plugins_disabled", [])))' "$manifest" 2>/dev/null || true)"
else
  disabled=""
fi

say "Undoing the ~/.claude wiring"
if [ "$DRY" = 1 ]; then python3 "$HERE/bin/fm" uninstall-user --dry-run; else python3 "$HERE/bin/fm" uninstall-user; fi

say "Uninstalling the plugin and the local marketplace"
run claude plugin uninstall foreman@foreman --scope user >/dev/null 2>&1 || say "  (foreman@foreman was not installed)"
run claude plugin marketplace remove foreman >/dev/null 2>&1 || say "  (marketplace 'foreman' was not registered)"

if [ -d "$FOREMAN_HOME/state" ]; then
  if [ "$PURGE" = 1 ] && { [ "$YES" = 1 ] || { [ -r /dev/tty ] && read -r -p "Delete $FOREMAN_HOME/state (archived to backups/ first)? [y/N] " ans </dev/tty && [ "$ans" = y ]; }; }; then
    archive="$FOREMAN_HOME/backups/state-$(date +%Y%m%d-%H%M%S).tgz"
    run mkdir -p "$FOREMAN_HOME/backups"
    run tar -C "$FOREMAN_HOME" -czf "$archive" state
    run rm -r "$FOREMAN_HOME/state"
    say "State archived to $archive and removed"
  else
    say "Kept $FOREMAN_HOME/state (tasks, ledger, decisions). Remove it with --purge-state."
  fi
fi

if [ -n "$disabled" ]; then
  say "Foreman disabled these plugins; re-enable any you want:"
  for p in $disabled; do echo "    claude plugin enable $p"; done
fi
say "Done. The repo itself stays at $FOREMAN_HOME (delete it if you no longer want it)."
