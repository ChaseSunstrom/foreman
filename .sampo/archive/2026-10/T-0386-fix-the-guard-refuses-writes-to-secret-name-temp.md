---
id: T-0386
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T01:35:35Z
updated: 2026-10-09T01:41:56Z
base: 9ad3ab6f88c06a30b05f616c890e4a58220e39fa
base_tree: ac0ab6984f1c133a062490c3d2e40f00c8898c79
verified: strong
---
# FIX: the guard refuses writes to secret-name templates (jarvis-core/config/secrets.yaml.ex
## Raw request
> FIX: the guard refuses writes to secret-name templates (jarvis-core/config/secrets.yaml.example, from JARVIS's builder); .example/.sample/.template/.dist copies hold placeholders — exempt them unless their content looks like a real secret
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] secret-name templates (.example .sample .template .dist .tmpl) are writable; the real files and key files stay credentials — verify with `python3 plugin/tests/run.py -k test_secret_templates_are_not_credentials`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the template exemption in _is_credential
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_secret_templates_are_not_credentials` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ScratchNames 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f453775e3ea3] (2026-10-09T01:40:16Z)
- `python3 plugin/tests/run.py -k test_secret_templates_are_not_credentials` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ScratchNames 0s) / OK [ran] [tree f453775e3ea3] (2026-10-09T01:40:16Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.0    34.7     150  [0] / SessionEnd                  29.5    31.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 910 tests in [ran] [tree eb3a917bf2b4] (2026-10-09T01:41:36Z)
- (ac 1) `python3 plugin/tests/run.py -k test_secret_templates_are_not_credentials` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ScratchNames 0s) / OK [ran] [tree eb3a917bf2b4] (2026-10-09T01:41:36Z)
- (audit adversary) `self: template suffix exempts only the name rule (secrets/credentials/tokens); key and .env rules run first; replay checked in the gate` → cp config/secrets.yaml config/secrets.yaml.example still reads the guarded source; id_ed25519.example and secrets.example.yaml stay credentials (test) [tree eb3a917bf2b4] (2026-10-09T01:41:36Z)
- (audit intent) `self: template suffix exempts only the name rule (secrets/credentials/tokens); key and .env rules run first; replay checked in the gate` → the JARVIS builder's secrets.yaml.example write passes (test) [tree eb3a917bf2b4] (2026-10-09T01:41:36Z)
- (audit self) `self: template suffix exempts only the name rule (secrets/credentials/tokens); key and .env rules run first; replay checked in the gate` → no findings [tree eb3a917bf2b4] (2026-10-09T01:41:36Z)
## Log
- 2026-10-09T01:35:35Z created
- 2026-10-09T01:39:59Z focused
- 2026-10-09T01:41:36Z done
- 2026-10-09T01:41:37Z committed c9c65ae (3 files)
- 2026-10-09T01:41:56Z correction to the adversary lens: cp/cat of config/secrets.yaml into a template is NOT blocked — the guard's credentials category covers writes to secret-named paths, not Bash reads (cat secrets.yaml > notes.txt passed before this task too). No new channel: the exemption only changes which names count as secret files to write; a real secret copied into any file is caught at commit by fm secrets (fm task finish --commit).
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0324-review: Verdict: changes needed.** One fail-open path and two config-clobber paths are verified. I read the code but ran nothing, so each failing input b…
- research T-0270-review-1: Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every…
- research mission-20261008-195201.pack: super improve foreman
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
