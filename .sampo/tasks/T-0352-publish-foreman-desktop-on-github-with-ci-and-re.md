---
id: T-0352
type: FEATURE
tier: M
status: blocked
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T04:38:42Z
updated: 2026-10-08T23:50:48Z
base: d1fdbc0758b37e1833248944fc24a0f31ec75b36
base_tree: 023d8f3c3f0e0abc25ca695cec39715e7556cf2c
paused_tree: 023d8f3c3f0e0abc25ca695cec39715e7556cf2c
---
# Publish Foreman Desktop on GitHub with CI and release pipelines
## Raw request
> Publish Foreman Desktop on GitHub with CI and release pipelines
## Interpretation
The user said yes to publishing the app on GitHub, with build pipelines. Foreman's repo is public, so this one is too. No gh or token exists here: install gh to ~/.local/bin; the login is the user's.
## Assumptions (confidence)
## Acceptance criteria
- [ ] github.com/ChaseSunstrom/foreman-desktop exists (public, like Foreman) with main pushed — verify with `git -C ~/projects/foreman-desktop ls-remote origin main`
- [ ] CI (type-check, Rust tests) runs on every push and a v* tag builds Linux and macOS bundles into a public release (no Windows: fm decide) — verify with `python3 -c "import json, urllib.request as u; g = lambda p: json.load(u.urlopen('https://api.github.com/repos/ChaseSunstrom/foreman-desktop/' + p)); runs = g('actions/runs?per_page=30')['workflow_runs']; ci = next(r for r in runs if r['name'] == 'CI' and r['status'] == 'completed'); rel = next(r for r in runs if r['name'] == 'Release' and r['head_branch'] == 'v0.1.0'); assets = [a['name'] for a in g('releases/tags/v0.1.0')['assets']]; assert (ci['conclusion'], rel['conclusion']) == ('success', 'success'), (ci['conclusion'], rel['conclusion']); assert any(a.endswith('.AppImage') for a in assets) and any(a.endswith('.dmg') for a in assets), assets; print('ok', assets)"`
## Non-goals
## Approach (options → choice → why)
(A) gh repo create + git push over the working ssh key; ci.yml (bun check, cargo test on ubuntu) on push/PR; release.yml on v* tags with tauri-apps/tauri-action building Linux (AppImage, deb, rpm), Windows (msi, nsis) and macOS (dmg, universal) into a draft-free GitHub release. (B) Build releases locally and upload — only Linux, and not repeatable. Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] repo hygiene: license, README, ignore list  <- CURRENT
2. [ ] workflows: ci.yml and release.yml (tauri-action)
3. [ ] create the repo, push, tag v0.1.0, watch the runs
## Resume here
<!-- auto -->
- 2026-10-08T22:50:15Z step 1/3: repo hygiene: license, README, ignore list
- git: foreman/build; 0 uncommitted
- failures met: json.decoder.jsondecodeerror: expecting value: line 0 column 0 (char 0)
## Docs impact
## Verification evidence
- (step 1) `bash -c 'cd ~/projects/foreman-desktop && test -f LICENSE && grep -q MIT src-tauri/Cargo.toml && bun install --frozen-lockfile'` → exit 0 · $ svelte-kit sync || echo '' / Checked 66 installs across 99 packages (no changes) [373.00ms] [ran] [tree 4848aa4d9c28] (2026-10-06T04:40:12Z)
- (step 2) `bash -c 'cd ~/projects/foreman-desktop && bun x --bun js-yaml .github/workflows/ci.yml >/dev/null && bun x --bun js-yaml .github/workflows/release.yml >/dev/null'` → exit 0 · (no output) [ran] [tree 4848aa4d9c28] (2026-10-06T04:40:20Z)
- (step 1) `cd ~/projects/foreman-desktop && grep -q 'MIT License' LICENSE && grep -q Releases README.md && grep -q node_modules .gitignore` → exit 0 · (no output) [ran] [tree 023d8f3c3f0e] (2026-10-06T20:47:12Z)
- (step 2) `cd ~/projects/foreman-desktop && python3 -c "import re; [print(f, 'unpinned') or exit(1) for f in ('.github/workflows/ci.yml', '.github/workflows/release.yml') for u in re.findall(r'uses: (\S+)', open(f).read()) if not re.search(r'@[0-9a-f]{40}$', u)]"` → exit 0 · (no output) [ran] [tree 023d8f3c3f0e] (2026-10-06T20:47:12Z)
## Log
- 2026-10-06T04:38:42Z created
- 2026-10-06T04:39:01Z focused
- 2026-10-06T04:40:20Z waiting: the user's gh auth login (gh installed to ~/.local/bin/gh v2.102.0, checksum verified)
- 2026-10-06T04:40:20Z paused: focus moved to T-0351
- 2026-10-06T04:47:19Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-06T04:47:19Z focused
- 2026-10-06T04:48:27Z paused: focus moved to T-0326
- 2026-10-06T04:51:28Z blocked: waits for the user's GitHub login: ~/.local/bin/gh auth login -h github.com -p ssh -w (repo, workflows, LICENSE and README are committed locally, ready to push)
- 2026-10-06T20:46:38Z unblocked: the repo exists and main is pushed over ssh (CI green on c9f54f6); gh isn't needed to tag, and runs are readable through the public API
- 2026-10-06T20:46:38Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-06T20:46:38Z focused
- 2026-10-06T20:47:07Z criterion 2 verify: `bash -c 'gh run list -R ChaseSunstrom/foreman-desktop -L 5 --json conclusion,name | grep -q success'` → `python3 -c "import json, urllib.request as u; g = lambda p: json.load(u.urlopen('https://api.github.com/repos/ChaseSunstrom/foreman-desktop/' + p)); runs = g('actions/runs?per_page=30')['workflow_runs']; ci = next(r for r in runs if r['name'] == 'CI' and r['status'] == 'completed'); rel = next(r for r in runs if r['name'] == 'Release' and r['head_branch'] == 'v0.1.0'); assets = [a['name'] for a in g('releases/tags/v0.1.0')['assets']]; assert (ci['conclusion'], rel['conclusion']) == ('success', 'success'), (ci['conclusion'], rel['conclusion']); assert any(a.endswith('.AppImage') for a in assets) and any(a.endswith('.dmg') for a in assets), assets; print('ok', assets)"`
- 2026-10-06T20:47:07Z criterion 2 text: CI (type-check, Rust tests) runs on every push and a v* tag builds Linux, Windows and macOS bundles into a release → CI (type-check, Rust tests) runs on every push and a v* tag builds Linux and macOS bundles into a public release (no Windows: fm decide)
- 2026-10-08T22:55:18Z paused: focus moved to T-0364
- 2026-10-08T23:50:48Z blocked: step 3 needs a GitHub repo created: gh isn't logged in on this machine (git over SSH works, the API doesn't); needs the user's gh auth login
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0326 [FEATURE M, blocked, 1 steps] Publish Foreman Desktop and add install.sh --desktop
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- T-0351 [FEATURE M, planned, 3 steps] Desktop UI cleanup: conversations without tool-call spam, and a tidier UI
- playbook Release and changelog (skills/playbooks/references/release/release-and-changelog.md)
