---
id: T-2373
type: SECURITY
tier: M
status: blocked
priority: normal
scope: [plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/tests/test_guard.py, plugin/tests/test_guard_cases.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-31T14:02:01Z
updated: 2026-10-31T14:38:45Z
---
# Installs are the user's (Mission 6, #5): the guard sends every package install that adds something new, machine-wide or into the project, to a new user-only install category pinned to the exact package; restoring what the project already declares stays allowed
## Raw request
> Installs are the user's (Mission 6, #5): the guard sends machine-level package installs to a new user-only install category pinned to the exact package; project-local installs stay allowed
## Interpretation
gen-0 #5: install grants are queued for the user, never self-granted. On 2026-10-31, fm guard try in this repo allowed pip install --user, pipx install, uv tool install, npm install -g, cargo install, go install, gem install, brew install and sudo pacman -S; only claude plugin and claude mcp add changes need the user's plugin grant. A session can install anything machine-wide without asking.
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm guard try denies each listed machine-level install and each add of a package the project doesn't declare, with category install and the exact fm ask line (fm ask ID install --pin MANAGER:PACKAGE --why ...); every self-grant path from the adversary list (pip inside python -c, a Makefile target, a script written then run, PIP_USER=1, an unpinned npx, a lookalike name) is denied; restoring declared dependencies (npm ci, pip install -r, pip install -e ., uv sync, cargo build) is allowed; a granted pin covers that one install only and is spent on use; fm doctor's hook latency check still passes (worst p95 247.9 ms on 2026-10-31) — verify with `python3 plugin/tests/run.py test_guard test_guard_cases test_guard_evasions`
## Non-goals
## Approach (options → choice → why)
1) A user-only install category in fmguard (USER_ONLY). It covers acquiring anything new: package managers that write outside the project (pip, pip3 and python -m pip with --user, --break-system-packages, or a --target or --prefix outside the project, or with no project venv active; pipx install and inject; uv tool install and uv pip --system; npm, pnpm, yarn and bun global installs; cargo install; go install; gem install; brew; apt, apt-get, dnf, yum, zypper, apk, pacman -S, yay, paru, snap, flatpak, nix profile install), and adding a package the project's manifest or lockfile doesn't declare (npm, pnpm, yarn or bun add or install of a named package not in package.json; pip install of a name not in requirements*.txt or pyproject.toml; cargo add; poetry add; uv add; go get; bundle add); plus npx, uvx and pipx run of a package the project doesn't declare. Declared packages run install scripts too, but the project already chose them and its lockfile pins them; a new name is a choice the user hasn't made. Restoring what the project declares stays allowed (npm ci, npm install with no package, pip install -r requirements.txt, pip install -e ., uv sync, cargo build, bundle install): local and reversible in a lane. fm ask ID install --pin MANAGER:PACKAGE[@VERSION] grants exactly that one install, spent on use. 2) Reuse the plugin category: rejected, its pin is a marketplace plugin id checked against fmplugins.content_hash; a package needs its own pin and wording. 3) Block every package-manager call: rejected, restoring declared dependencies in a lane is local and reversible, and blocking it stalls ordinary work. Choice 1. fmguard.py is the guard file: trust mode is on (the user's /fm-trust), so Claude may edit it; this change only tightens the guard, is built and evaluated in a git worktree, and lands with adversarial test cases, never a weaker rule.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red tests first in test_guard, test_guard_cases and test_guard_evasions: each manager denied, each new-package add denied, each restore form allowed, the pin spent on use  <- CURRENT
2. [ ] fmguard: the install category, its detection and pin; fm ask pin validation for install (fmcli.cmd_ask, fmhooks._ask_prompt)
3. [ ] docs: MASTER.md guard table, CHANGELOG.md
4. [ ] adversarial cases: every self-grant path (pip inside python -c, a Makefile target, a script written then run, PIP_USER=1, an unpinned npx, a lookalike name) is denied in test_guard_evasions; the change only tightens the guard (trust mode lets Claude edit it), built and evaluated in a git worktree
5. [ ] queue fm ask T-2373 core for the end-of-run report: the guard file is protected core, so merging stays the user's call (gen-0's NEVER line); the existing guard suites pass unchanged (no deny becomes an allow)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-31T14:02:01Z created
- 2026-10-31T14:10:09Z set title=Installs are the user's (Mission 6, #5): the guard sends every package install that adds something new, machine-wide or into the project, to a new user-only install category pinned to the exact package; restoring what the project already declares stays allowed
- 2026-10-31T14:33:06Z step 4 text: leave the candidate on its lane branch and queue fm ask ID core for the end-of-run report (the guard file is the user's to merge) → adversarial cases: every self-grant path (pip inside python -c, a Makefile target, a script written then run, PIP_USER=1, an unpinned npx, a lookalike name) is denied in test_guard_evasions; the change only tightens the guard (trust mode lets Claude edit it), built and evaluated in a git worktree
- 2026-10-31T14:33:06Z step 1 text: red tests first in test_guard and test_guard_cases: each manager denied, each project-local form allowed, the pin spent on use → red tests first in test_guard, test_guard_cases and test_guard_evasions: each manager denied, each new-package add denied, each restore form allowed, the pin spent on use
- 2026-10-31T14:36:26Z blocked: held for the user: a user-only install category in fmguard needs adversarial cases that list install-command variants a session could use to slip past it, which is the activity the standing stop on enumerating guard-bypass forms rules out (T-1937, T-1928). The finding stands: on 2026-10-31 fm guard try allowed machine-wide installs (pip --user, pipx, uv tool, npm -g, cargo/go/gem install, brew, sudo pacman -S) with no grant. The user decides how to proceed; listed in the final report
## Follow-ups captured
