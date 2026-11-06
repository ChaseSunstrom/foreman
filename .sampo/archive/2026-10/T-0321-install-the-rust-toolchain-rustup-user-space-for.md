---
id: T-0321
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T01:08:55Z
updated: 2026-10-06T01:11:05Z
base: a980b28d118b8c40dc4df27815c0713764d41de6
base_tree: a5e3266426c59c61f3c6dba6a34811cb5c573b13
verified: strong
---
# Install the Rust toolchain (rustup, user space) for the Tauri app
## Raw request
> Install the Rust toolchain (rustup, user space) for the Tauri app
## Interpretation
T-0318's desktop app is Tauri (user's choice); Tauri needs Rust; none is installed. rustup in ~/.cargo, no sudo; rustup self uninstall undoes it.
## Assumptions (confidence)
## Acceptance criteria
- [x] cargo and rustc run from ~/.cargo/bin — verify with `~/.cargo/bin/cargo --version`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] rustup-init -y --profile minimal
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `~/.cargo/bin/cargo --version && ~/.cargo/bin/rustc --version` → exit 0 · cargo 1.99.0 (5f94df478 2026-08-27) / rustc 1.99.0 (b940084d7 2026-09-28) [ran] [tree a5e3266426c5] (2026-10-06T01:10:17Z)
- (step 1) `~/.cargo/bin/rustup show active-toolchain` → exit 0 · stable-x86_64-unknown-linux-gnu (default) [ran] [tree a5e3266426c5] (2026-10-06T01:11:05Z)
- (ac 1) `~/.cargo/bin/cargo --version` → exit 0 · cargo 1.99.0 (5f94df478 2026-08-27) [ran] [tree a5e3266426c5] (2026-10-06T01:11:05Z)
- (audit intent) `self: one command, verified by running the binaries` → rustc/cargo 1.99 in ~/.cargo/bin for the Tauri build; rustup added ~/.cargo/env to shell profiles; rustup self uninstall reverts [tree a5e3266426c5] (2026-10-06T01:11:05Z)
- (audit self) `self: one command, verified by running the binaries` → no findings [tree a5e3266426c5] (2026-10-06T01:11:05Z)
## Log
- 2026-10-06T01:08:55Z created
- 2026-10-06T01:08:55Z focused
- 2026-10-06T01:08:57Z guard authorization added: pipe-shell
- 2026-10-06T01:11:05Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Rust Testing Patterns (skills/playbooks/references/lang/rust-testing.md)
- research t0016-operator: xcept (OSError, ...)`, printed once) — the plugin is still installed, but the manifest is deleted anyway. Running `fm uninstall-user` again now …
- research t0016-maintainer: ds failures from removing tracked plugins/marketplaces only as a print statement (`err = ...; print(f\"Could not remove {what} {name}: {err}\"…
- T-0016 [FEATURE L, done, 4 steps] Approved plugin/marketplace installs on demand; conflict-free integration of plugins and skills
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
