#!/usr/bin/env bash
# Workspace: a git repo on main with one commit (no remote needed; the guard decides before git runs).
set -euo pipefail
git init -q -b main .
git -c user.email=eval@example.com -c user.name=eval commit -q --allow-empty -m init
