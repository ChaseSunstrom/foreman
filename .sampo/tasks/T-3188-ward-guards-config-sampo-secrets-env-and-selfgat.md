---
id: T-3188
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T09:50:02Z
updated: 2026-11-05T10:35:58Z
builder_model: haiku
base: f3b72e33004d187bb1df88d9afef764af0d92f8f
base_tree: ec6de35a90fe2cf698511a2aeba6ee36d7b99993
plan0_at: 2026-11-05T09:50:43Z
plan0_scope: []
builder_returned: 2026-11-05T09:55:32Z
lane_stop: merged 2026-11-05T10:32:50Z
verified: strong
---
# Ward treats every file under ~/.config/sampo as a credential (secrets.env, selfgate.key and any later key), not only by file name, with a replay case for each
## Raw request
> Ward guards ~/.config/sampo/secrets.env and selfgate.key only by their file names: add ~/.config/sampo to the credential directories (_CRED_DIRS/_CRED_PART), so every file there is a credential to a gated agent, with a replay case for each
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmguard refuses a read or write by an agent of any file under ~/.config/sampo (cat, Read, a redirect, cp), with credentials as the category, while Sampo's own models.secret and selfgate still read them; the guard's replay corpus gains these cases and replays clean — verify with `python3 plugin/tests/run.py test_guard test_replay test_models`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing guard tests for files under ~/.config/sampo
2. [x] the directory in _CRED_DIRS/_CRED_PART and the replay cases
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard test_replay` → exit 0 · Ran 338 tests in 12.8s (97 classes, 16 at a time; slowest: Mutation 12s, GuardAgainstBash 11s, Trust 6s) / OK [ran] [tree f817e8ed49c3] [world 2f1906870a] (2026-11-05T09:53:11Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_replay` → exit 0 · Ran 338 tests in 26.2s (97 classes, 16 at a time; slowest: GuardAgainstBash 24s, Mutation 24s, Latency 11s) / OK [ran] [tree f817e8ed49c3] [world 2f1906870a] (2026-11-05T09:53:37Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_core test_doctor test_guard test_guard_diff test_guard_exec_vectors test_guard_git test_guard_pipes test_guard_sampo test_hooks test_left_out test_models test_rename_scan test_settings_scopes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [14.55s] [ran] [tree f817e8ed49c3] [world 2f1906870a] (2026-11-05T09:55:20Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_replay test_models` → exit 0 · Ran 426 tests in 27.9s (112 classes, 16 at a time; slowest: Mutation 26s, GuardAgainstBash 24s, Trust 11s) / OK [ran] [tree 29d1fc95539f] [world 2f1906870a] (2026-11-05T10:33:30Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_replay test_models` → exit 0 · Ran 426 tests in 21.7s (112 classes, 16 at a time; slowest: Mutation 20s, GuardAgainstBash 16s, Trust 11s) / OK [ran] [tree 29d1fc95539f] [world 2f1906870a] (2026-11-05T10:33:52Z)
- `python3 plugin/tests/run.py test_guard.CredentialReads` → ✗ exit 1 · Ran 8 tests in 2.0s (1 classes, 16 at a time; slowest: CredentialReads 0s) / FAILED (1 classes: test_guard.CredentialReads) (start tree + this task's tests) [ran] [tree 29d1fc95539f] [world 2f1906870a] (2026-11-05T10:34:01Z)
- `python3 plugin/tests/run.py test_guard.CredentialReads` → exit 0 · Ran 8 tests in 0.6s (1 classes, 16 at a time; slowest: CredentialReads 0s) / OK [ran] [tree 29d1fc95539f] [world 2f1906870a] (2026-11-05T10:34:01Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_replay test_models` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T10:33:52Z [ran] [tree 29d1fc95539f] [world 2f1906870a] (2026-11-05T10:34:17Z)
- (audit adversary) `self: read the merged guard change (~/.config/sampo in the credential dirs and parts) and its 8 CredentialReads tests; 426 guard/replay/models tests green; proved red on the start tree` → cat/head/cp/redirect-in/redirect-out, $HOME form, Read and Write tools on any file under the folder all refused; a sibling ~/.config/sampo-other stays free; glob and find -exec forms rely on the existing unknown-name handling (not added here) [tree 29d1fc95539f] (2026-11-05T10:34:17Z)
- (audit edge) `self: read the merged guard change (~/.config/sampo in the credential dirs and parts) and its 8 CredentialReads tests; 426 guard/replay/models tests green; proved red on the start tree` → Sampo's own in-process reads (models.secret, selfgate key) are not tool calls and still work; a grant (--allow credentials) lets a read through [tree 29d1fc95539f] (2026-11-05T10:34:17Z)
- (audit self) `self: read the merged guard change (~/.config/sampo in the credential dirs and parts) and its 8 CredentialReads tests; 426 guard/replay/models tests green; proved red on the start tree` → no findings [tree 29d1fc95539f] (2026-11-05T10:34:17Z)
## Log
- 2026-11-05T09:50:02Z created
- 2026-11-05T09:50:21Z planned from capture
- 2026-11-05T09:50:22Z set approved=True
- 2026-11-05T09:50:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3188.builder.md
- 2026-11-05T09:50:41Z focused
- 2026-11-05T09:55:28Z criterion 1 verify: `python3 plugin/tests/run.py test_guard test_guard_corpus` → `python3 plugin/tests/run.py test_guard test_replay test_models`
- 2026-11-05T10:32:50Z merged worktree-agent-af939e79f4eed4e9b (3 file(s))
- 2026-11-05T10:32:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af939e79f4eed4e9b
- 2026-11-05T10:32:53Z focused
- 2026-11-05T10:33:00Z scope: CHANGELOG.md also carries T-3176's line, owed after its close (the edit hook needs an active task)
- 2026-11-05T10:35:58Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/lib/sampo/hooks.py
- CHANGELOG.md
