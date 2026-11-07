---
id: T-2987
type: FEATURE
tier: S
status: blocked
priority: normal
scope: []
depends_on: [T-2978]
source: discovered
created: 2026-11-04T15:14:16Z
updated: 2026-11-05T02:02:29Z
base_note: Calibration: this plan states Choice 75% where FEATURE S closes (253) held on the first finish 100% of the time: 25 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
base: 2b6c237a3d332aef55de66319465a61751ee94c6
base_tree: acd42603cc518c914c7b02818e897ce4b95a093a
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T15:24:37Z
plan0_scope: []
paused_tree: 4f710662165a4cf005040060ffa7c73de272b76d
---
# Mint in projects with installed deps: git archive leaves out .venv and node_modules, so…
## Raw request
> Mint in projects with installed deps: git archive leaves out .venv and node_modules, so trader (Python, uv) and jarvis-code (JS) read red at HEAD and mint nothing. Link the source's dependency dirs into the throwaway copy, run Python through the linked venv's interpreter (never uv run, which would re-sync and repoint the real venv's editable install at the copy), and put the copy's src and root first on PYTHONPATH (minting and grading both) so the mutant shadows an editable install; prove it on trader and jarvis-code
## Interpretation
Reading 1 (chosen): real Sampo projects keep their deps untracked, so a git-archive copy can't run its tests. Mint links the source's dependency dirs (.venv, venv, node_modules) into the throwaway copy as symlinks, never writes through them, runs Python tests through the linked venv's own interpreter (a detected 'uv run X' becomes '.venv/bin/python -m X' so uv never re-syncs the real venv), puts the copy's src and root first on PYTHONPATH (key env, used by grading too) so a mutant shadows an editable install, and gives Rust one shared CARGO_TARGET_DIR per mint run. Reading 2 (ruled out): install deps into each copy; slow, and it installs software.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a fixture repo whose tests need an untracked .venv (a fake module only there) and an editable-style .pth pointing at the source mints a caught mutant; uv run becomes the venv's interpreter; the source's venv and files are untouched — verify with `python3 plugin/tests/run.py test_mint`
- [ ] a live mint keeps scenarios in two of this machine's projects in different languages — verify with `sampo exam runs --json`
## Non-goals
## Approach (options → choice → why)
1) Link, don't install. Symlink the source's .venv, venv and node_modules into the clean copy (copytree keeps the links in every mutant and scenario copy). Rewrite a detected `uv run X` or `poetry run X` to `<link>/bin/python -m X`. Set the key's env PYTHONPATH to "src:." (relative, so it resolves in whichever copy runs), and give Rust CARGO_TARGET_DIR=<mint tmp>/target. Grading passes the key's env through louhi._run. Likely outcome: trader and jarvis-code mint. Fails if: a test writes into node_modules or the venv. Tests that do are rare; the link is the user's own deps, and the mint never runs an installer.
2) Copy the deps (cp -a). Likely outcome: the same, but gigabytes per mutant. Fails if: volt-sized trees, at 40 copies per run.
3) Do less: mint only stdlib-only repos. Likely outcome: almost nothing on this machine. Fails if: the generic model needs real projects.
Choice 1 (75%): no installs, no copies; the shared cargo target turns minutes into seconds.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: untracked-venv fixture, editable .pth, uv run rewrite, source untouched
2. [x] dep links, interpreter rewrite, PYTHONPATH in key env and louhi _run, shared cargo target
3. [ ] live mint on trader plus one of jarvis-code or volt-gate; numbers in T-2978's research  <- CURRENT
## Resume here
<!-- auto -->
- 2026-11-04T16:02:57Z step 3/3: live mint on trader plus one of jarvis-code or volt-gate; numbers in T-2978's research
- git: foreman/build; 4 uncommitted: plugin/lib/sampo/cli.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/mint.py, plugin/tests/test_mint.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/testcmd-edit.json, plugin/lib/sampo/cli.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/mint.py, plugin/tests/test_mint.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_mint` → ✗ exit 1 · Ran 14 tests in 3.1s (2 classes, 16 at a time; slowest: MintFromRepo 3s, MintWithUntrackedDeps 2s) / FAILED (1 classes: test_mint.MintWithUntrackedDeps) [ran] [tree 3f0a7760d814] [world 2f1906870a] (2026-11-04T15:25:27Z)
- (step 2) `python3 plugin/tests/run.py test_mint test_exam` → exit 0 · Ran 123 tests in 107.3s (29 classes, 16 at a time; slowest: LeanKind 107s, ExamAuthors 81s, JudgmentKinds 76s) / OK [ran] [tree 70a53290b493] [world 2f1906870a] (2026-11-04T15:30:48Z)
- (step 2) `python3 plugin/tests/run.py test_mint test_exam` → exit 0 · Ran 124 tests in 145.4s (29 classes, 16 at a time; slowest: LeanKind 145s, ExamAuthors 87s, JudgmentKinds 78s) / OK [ran] [tree 67e2f72f46b1] [world 2f1906870a] (2026-11-04T16:01:35Z)
- (step 2) `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_exam test_left_out test_louhi_models test_mint test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.32s] [ran] [tree 555f9e1aa5f1] [world 2f1906870a] (2026-11-04T16:13:23Z)
- (step 2) `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_exam test_left_out test_louhi_models test_mint test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.43s] [ran] [tree 2026f70735c9] [world 2f1906870a] (2026-11-04T16:19:33Z)
- (step 2) `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_hardening test_code_worker test_core test_ctx_variant test_exam test_left_out test_louhi_models test_mint test_models test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.76s] [ran] [tree d0a36ff882d6] [world 2f1906870a] (2026-11-04T16:37:36Z)
- (step 3) `sampo exam check s4-018 && sampo exam check s2-017` → ✗ exit 1 · s2-017: 4 scenarios checked, 1 problems: / s2-017-m01: clean suite failed on run 2 of 3: exec exit 1: npm notice run tsc -p . && node --test --test-concurrency=1 dist/test/ [ran] [tree d0a36ff882d6] [world 2f1906870a] (2026-11-04T16:46:44Z)
- (step 3) `sampo exam check s4-018 && sampo exam check s2-017` → ✗ exit 124 (timed out after 762.14s) · s4-018: 4 scenarios checked, all sound / timed out after 762.14s [ran] [tree ef783de8d095] [world 2f1906870a] (2026-11-04T17:18:22Z)
- (step 3) `sampo exam check s2-017` → ✗ exit 1 · s2-017: 4 scenarios checked, 1 problems: / s2-017-m01: clean suite failed on run 1 of 3: exec exit 1: npm notice run tsc -p . && node --test --test-concurrency=1 dist/test/ [ran] [tree 7cd5c1976a08] [world 2f1906870a] (2026-11-04T17:27:43Z)
## Log
- 2026-11-04T15:14:16Z created
- 2026-11-04T15:14:45Z steer: also Rust: one CARGO_TARGET_DIR per mint run shared by the green runs and every mutant, so only the mutated crate recompiles (volt's target is 6.6 GB; a fresh build per mutant would blow the cap); this task carries T-2978's live step: mint on trader (Python) and jarvis-code (JS) or volt-gate (Rust)
- 2026-11-04T15:14:45Z planned: it has criteria and steps
- 2026-11-04T15:14:46Z set depends_on=['T-2978'], approved=True
- 2026-11-04T15:24:37Z focused
- 2026-11-04T15:24:37Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T15:31:39Z paused: focus moved to T-2988
- 2026-11-04T15:33:29Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T15:33:29Z focused
- 2026-11-04T15:34:50Z paused: focus moved to T-2950
- 2026-11-04T15:55:07Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T15:55:07Z focused
- 2026-11-04T15:55:09Z steer: trader's suite takes over 15 minutes in a copy (timed: killed at 900 s), so --test-cmd lets a slow repo mint against a fast subset; the detected gate stays the default
- 2026-11-04T16:03:00Z paused: focus moved to T-2951
- 2026-11-04T16:14:16Z scope: --only GLOB on exam gen --from-repo limits mutated files: no fast runnable Python suite exists among this machine's other projects (trader's subset >10 min, others need missing deps or hit live services), so the Python leg mints from one Sampo module with its own tests
- 2026-11-04T16:14:25Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T16:14:25Z focused
- 2026-11-04T16:49:32Z paused: focus moved to T-2977
- 2026-11-04T17:05:38Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T17:05:38Z focused
- 2026-11-04T17:22:09Z paused: focus moved to T-2970
- 2026-11-05T02:02:29Z blocked: step 3's live mint runs trader's and jarvis-code's test suites in throwaway copies, loading the machine the merge chain's gate benches on; runs right after the chain clears, with T-2878's measurement
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2978 [FEATURE M, planned, 3 steps] Scenario minting in real repos: plant one defect by mutation in a Sampo project's real…
- decision 2026-11-04: Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline d…
- similar past tasks were L: consider --tier L
