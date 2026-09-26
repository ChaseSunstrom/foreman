#!/usr/bin/env bash
# One-time: point README, install.sh, and the manifests at your GitHub repo, then commit.
# Usage: ./configure-repo.sh <github-user> [repo-name]
set -euo pipefail
GH_USER="${1:?usage: ./configure-repo.sh <github-user> [repo-name]}"
REPO="${2:-foreman}"
cd "$(dirname "$0")"

FILES=(README.md install.sh .claude-plugin/marketplace.json plugin/.claude-plugin/plugin.json)
for f in "${FILES[@]}"; do
  sed -i.bak -e "s#YOUR_GITHUB_USER/foreman#$GH_USER/$REPO#g" -e "s#YOUR_GITHUB_USER#$GH_USER#g" "$f" && rm -f "$f.bak"
done
git add "${FILES[@]}"
git commit --quiet -m "chore: point install at github.com/$GH_USER/$REPO"

cat <<EOF
Configured for github.com/$GH_USER/$REPO. Push it with either:
  gh repo create $REPO --public --source . --push      # or --private
  git remote add origin git@github.com:$GH_USER/$REPO.git && git push -u origin main
EOF
