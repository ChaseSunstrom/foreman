---
id: T-0359
type: FIX
tier: S
status: done
priority: normal
scope: [~/projects/foreman-desktop/src-tauri/tauri.conf.json]
depends_on: []
source: user
created: 2026-10-06T05:44:59Z
updated: 2026-10-06T05:46:05Z
base: 5c9d7164587175f56c017e23123e01d0e75b8702
base_tree: 80256f58c27430dd80cc91520fc6f8a0e21fd9e6
verified: strong
---
# Foreman Desktop: ad-hoc sign the macOS build so it runs on Apple Silicon
## Raw request
> Foreman Desktop: ad-hoc sign the macOS build so it runs on Apple Silicon
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] bundle.macOS.signingIdentity is '-' and the config still builds — verify with `cd ~/projects/foreman-desktop && python3 -c "import json; assert json.load(open('src-tauri/tauri.conf.json'))['bundle']['macOS']['signingIdentity'] == '-'" && cargo check -q --manifest-path src-tauri/Cargo.toml`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] set signingIdentity, cargo check
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd ~/projects/foreman-desktop && python3 -c "import json; assert json.load(open('src-tauri/tauri.conf.json'))['bundle']['macOS']['signingIdentity'] == '-'" && cargo check -q --manifest-path src-tauri/Cargo.toml` → exit 0 · (no output) [ran] [tree 80256f58c274] (2026-10-06T05:45:44Z)
- (step 1) `cd ~/projects/foreman-desktop && git show HEAD:src-tauri/tauri.conf.json | python3 -c "import json,sys; assert json.load(sys.stdin)['bundle'].get('macOS', {}).get('signingIdentity') == '-', 'the committed config is unsigned'"` → ✗ exit 1 · ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ / AssertionError: the committed config is unsigned [ran] [tree 80256f58c274] (2026-10-06T05:45:52Z)
- (step 1) `cd ~/projects/foreman-desktop && python3 -c "import json; assert json.load(open('src-tauri/tauri.conf.json'))['bundle']['macOS']['signingIdentity'] == '-'" && cargo check -q --manifest-path src-tauri/Cargo.toml` → exit 0 · (no output) [ran] [tree 80256f58c274] (2026-10-06T05:45:52Z)
- (ac 1) `cd ~/projects/foreman-desktop && python3 -c "import json; assert json.load(open('src-tauri/tauri.conf.json'))['bundle']['macOS']['signingIdentity'] == '-'" && cargo check -q --manifest-path src-tauri/Cargo.toml` → exit 0 · (no output) [ran] [tree 80256f58c274] (2026-10-06T05:45:58Z)
- (audit edge) `self: Tauri's macOS signing page (quote verified in the T-0313 research note) says ad-hoc signing ('-') is what Apple Silicon needs without a certificate; the Linux job ignores bundle.macOS` → no Apple certificate in CI, so '-' signs ad hoc; a curl download via install.sh carries no quarantine flag [tree 80256f58c274] (2026-10-06T05:45:58Z)
- (audit self) `self: Tauri's macOS signing page (quote verified in the T-0313 research note) says ad-hoc signing ('-') is what Apple Silicon needs without a certificate; the Linux job ignores bundle.macOS` → no findings [tree 80256f58c274] (2026-10-06T05:45:58Z)
- (audit edge) `self: Tauri's macOS signing page (quote verified in the T-0313 research note) says ad-hoc signing ('-') is what Apple Silicon needs without a certificate; the Linux job ignores bundle.macOS` → no Apple certificate in CI, so '-' signs ad hoc; a curl download via install.sh carries no quarantine flag [tree 80256f58c274] (2026-10-06T05:46:04Z)
- (audit self) `self: Tauri's macOS signing page (quote verified in the T-0313 research note) says ad-hoc signing ('-') is what Apple Silicon needs without a certificate; the Linux job ignores bundle.macOS` → no findings [tree 80256f58c274] (2026-10-06T05:46:04Z)
## Log
- 2026-10-06T05:44:59Z created
- 2026-10-06T05:45:01Z focused
- 2026-10-06T05:46:05Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research ask-for-a-tauri-2-app-built-with-bun-what-do-20261006-0037: Asked 2026-10-06 · 2 sub-question(s) · 16 claims: 5 quote found, 6 quote not found, 5 unchecked. ✓ m…
- T-0326 [FEATURE M, done, 3 steps] Publish Foreman Desktop and add install.sh --desktop — lesson: Ship the app as release assets, not as a build recipe: an installer that…
- T-0318 [FEATURE L, done, 6 steps] FEATURE: beautiful modern animated desktop app wrapping Foreman — supports every feature, — lesson: A remote command over ssh gets no h…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar past tasks were L: consider --tier L
## Regression test
none: a one-line config value; no macOS build runs here. The criterion's check failed on the committed config (recorded, exit 1) and passes on the change, with cargo check.
