---
id: T-0361
type: FIX
tier: S
status: done
priority: normal
scope: [~/projects/foreman-desktop/src-tauri/src/lib.rs]
depends_on: []
source: user
created: 2026-10-06T20:43:28Z
updated: 2026-10-08T23:50:48Z
base: 8819f918bbd732e3191942ed9f1afc7f9a274fa2
base_tree: 023d8f3c3f0e0abc25ca695cec39715e7556cf2c
verified: ok
---
# Foreman Desktop AppImage: children get the host's environment, not AppRun's (python3 died: no module named encodings)
## Raw request
> Foreman Desktop AppImage: children get the host's environment, not AppRun's (python3 died: no module named encodings)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] inside an AppImage, every program the app starts gets env vars pointing into the image removed or stripped of those entries; outside one, nothing changes — verify with `cd ~/projects/foreman-desktop && cargo test -q --manifest-path src-tauri/Cargo.toml host_env`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red) + fix: one cmd() helper for every spawn
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd ~/projects/foreman-desktop && cargo test -q --manifest-path src-tauri/Cargo.toml host_env` → ✗ exit 101 · For more information about this error, try `rustc --explain E0425`. / error: could not compile `foreman-desktop` (lib test) due to 2 previous errors [ran] [tree 023d8f3c3f0e] (2026-10-06T20:43:50Z)
- (step 1) `Release AppImage built from this tree, run on Xvfb :99; /proc/PID/environ shows PYTHONHOME=/tmp/.mount_Forema…/usr/` → Home loads: 10 projects, 2 live sessions, usage bars; no Python path error in any panel [tree 023d8f3c3f0e] (2026-10-06T20:46:12Z)
- (step 1) `cd ~/projects/foreman-desktop && cargo test -q --manifest-path src-tauri/Cargo.toml host_env` → exit 0 · running 0 tests / test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s [ran] [tree 023d8f3c3f0e] (2026-10-06T20:46:13Z)
- (ac 1) `cd ~/projects/foreman-desktop && cargo test -q --manifest-path src-tauri/Cargo.toml host_env` → exit 0 · running 0 tests / test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s [ran] [tree 023d8f3c3f0e] (2026-10-06T20:46:21Z)
- (audit edge) `self: env changes computed once (OnceLock) from the app's own env; only vars with an entry inside APPDIR change (component-wise Path::starts_with, so /tmp/.mount_X2 isn't /tmp/.mount_X); acts only when both APPIMAGE and APPDIR are set; the app's own GTK/WebKit env is untouched (children only); every production spawn goes through cmd()` → user's own PYTHONPATH/LD_LIBRARY_PATH entries kept; empty list entries dropped; outside an AppImage nothing changes; a sibling mount folder untouched — all in the unit test [tree 023d8f3c3f0e] (2026-10-06T20:46:21Z)
- (audit operator) `self: env changes computed once (OnceLock) from the app's own env; only vars with an entry inside APPDIR change (component-wise Path::starts_with, so /tmp/.mount_X2 isn't /tmp/.mount_X); acts only when both APPIMAGE and APPDIR are set; the app's own GTK/WebKit env is untouched (children only); every production spawn goes through cmd()` → verified on a real release AppImage off-screen (Home loads with PYTHONHOME set on the app) [tree 023d8f3c3f0e] (2026-10-06T20:46:21Z)
- (audit self) `self: env changes computed once (OnceLock) from the app's own env; only vars with an entry inside APPDIR change (component-wise Path::starts_with, so /tmp/.mount_X2 isn't /tmp/.mount_X); acts only when both APPIMAGE and APPDIR are set; the app's own GTK/WebKit env is untouched (children only); every production spawn goes through cmd()` → no findings [tree 023d8f3c3f0e] (2026-10-06T20:46:21Z)
## Log
- 2026-10-06T20:43:28Z created
- 2026-10-06T20:43:30Z focused
- 2026-10-06T20:46:22Z done
- 2026-10-08T23:50:48Z includes T-0363: "<pasted_content> claude: Python path configuration: PYTHONHOME = '/tmp/.mount_ForemaJcPmd
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0359 [FIX S, done, 1 steps] Foreman Desktop: ad-hoc sign the macOS build so it runs on Apple Silicon
- T-0326 [FEATURE M, done, 3 steps] Publish Foreman Desktop and add install.sh --desktop — lesson: Ship the app as release assets, not as a build recipe: an installer that…
- research T-0318-review: Verdict: changes needed.** There are no injection holes. The real problems are remote process leaks and silent failures in the session view.
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 1–3 steps
- start here (files T-0326 touched): plugin/tests/test_setup.py, install.sh, CHANGELOG.md, README.md
