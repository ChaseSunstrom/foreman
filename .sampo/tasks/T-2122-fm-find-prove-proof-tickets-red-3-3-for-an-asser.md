---
id: T-2122
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T08:06:47Z
updated: 2026-10-30T19:27:00Z
base: 265c2417ec182eb34a706323c961ea1c96db694e
base_tree: 2668b8777b8578b94cd9f245ab41ad5383c1eb85
plan0_at: 2026-10-30T19:06:00Z
plan0_scope: []
verified: strong
---
# fm find prove: proof tickets, red 3/3 for an assertion and mutate-to-confirm; unproven candidates become leads (Mission 3 brief 3)
## Raw request
> fm find prove: proof tickets, red 3/3 for an assertion and mutate-to-confirm; unproven candidates become leads (Mission 3 brief 3)
## Interpretation
fm find reports candidates; `fm find prove [PATH]` turns each into a proof ticket or a lead. Proven = evidence a person can rerun: untested → stub the function to fail and the suite stays green; vuln/slow/flaky/bug → a test red 3/3 for an assertion (not import, syntax, setup or timeout) whose failure changes once the candidate is stubbed (it exercises that function); docs/dep/secret → their own check re-run cold on a fresh copy. Everything else goes to leads.jsonl, never the inbox.
## Assumptions (confidence)
- The failing-gates finder (fm adopt's gate run, rerun once: flaky vs fail) and each candidate's probe command land here, not in fm find, which stays read-only (decided on T-2121). (high)
## Acceptance criteria
- [x] a planted defect's candidate is proven and a candidate on clean code is a lead — verify with `python3 plugin/tests/run.py test_find`
## Non-goals
## Approach (options → choice → why)
A. Mutation for untested + model-written tests for the rest, all run on a throwaway copy with credentials stripped (chosen: no model call for untested/docs/dep/secret; the model only writes a test, a deterministic run judges it). B. Model judges each candidate by reading it (rejected: the session arms already lose on precision this way). C. Per-language analysers (Mission 6). D. Revert the line's last git change as the 'fix' (rejected for now: most candidates have no defect-introducing commit; mutate-to-confirm via stubbing is general). The repo's test command comes from fmmap._gates; --test CMD overrides. The failing-gates finder lands here (decided on T-2121): a gate red on the untouched copy, rerun once, red twice = proven fail, else flaky lead.
## Risks and rollback
Runs untrusted repo code: only on a temp copy (copytree, symlinks not followed), fmbench.CREDENTIALS stripped, a timeout per run; refused on a path outside the user's project unless --yes-run. A model test that fails for its own reason (wrong import) is classified non-assertion and stays a lead. Rollback: the verb is additive; fm find unchanged.
## Execution prompt
## Steps
1. [x] proof ticket: run 3x on an untouched copy, classify the failure
2. [x] mutate-to-confirm + leads.jsonl
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/README.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/plugin/rules/foreman.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_find.FindProve test_hooks` → ✗ exit 1 · Ran 218 tests in 82.0s (29 classes, 16 at a time; slowest: Stop 81s, NoTaskGate 54s, PreToolUse 50s) / FAILED (2 classes) [ran] [tree b5c924605dc7] (2026-10-30T19:09:03Z)
- (step 1) `python3 plugin/tests/run.py test_find test_hooks test_context_tax test_docsdrift test_export test_audit test_playbook_evals` → exit 0 · Ran 324 tests in 41.1s (70 classes, 16 at a time; slowest: Stop 41s, NoTaskGate 30s, PreToolUse 25s) / OK [ran] [tree ee8b7cdff3e3] (2026-10-30T19:12:11Z)
- (step 2) `python3 plugin/tests/run.py test_find.FindProve` → ✗ exit 1 · Ran 6 tests in 1.1s (1 classes, 16 at a time; slowest: FindProve 1s) / FAILED (1 classes) [ran] [tree 0e6ea4010ab3] (2026-10-30T19:13:42Z)
- (step 2) `python3 plugin/tests/run.py test_find test_hooks test_context_tax test_docsdrift test_export test_audit test_playbook_evals test_cli` → exit 0 · Ran 457 tests in 45.8s (104 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 35s, PreToolUse 30s) / OK [ran] [tree e502fb4722ea] (2026-10-30T19:14:46Z)
- (step 2) `python3 plugin/tests/run.py test_find.FindProve test_guard test_guard_exec_vectors` → ✗ exit 1 · Ran 309 tests in 9.9s (89 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 6s, Trust 5s) / FAILED (3 classes) [ran] [tree fc32b9eadc32] (2026-10-30T19:22:18Z)
- (step 2) `python3 plugin/tests/run.py test_find test_hooks test_guard test_guard_exec_vectors test_context_tax test_docsdrift test_export test_audit test_playbook_evals test_cli` → exit 0 · Ran 758 tests in 48.0s (190 classes, 16 at a time; slowest: Stop 48s, NoTaskGate 36s, PreToolUse 32s) / OK [ran] [tree bbf3d1a8340b] (2026-10-30T19:24:08Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 38 tests in 6.1s (15 classes, 16 at a time; slowest: FindCli 6s, FindRenders 3s, FindProve 2s) / OK [ran] [tree bbf3d1a8340b] (2026-10-30T19:25:54Z)
- `python3 plugin/tests/run.py test_find test_hooks test_guard test_guard_exec_vectors` → exit 0 · Ran 552 tests in 43.5s (130 classes, 16 at a time; slowest: Stop 43s, NoTaskGate 33s, PreToolUse 28s) / OK [ran] [tree bbf3d1a8340b] (2026-10-30T19:25:54Z)
- (audit intent) `one foreman:fm-reviewer pass over every lens with the adversary weighted (research T-2122-review): 1 HIGH + 9 MEDIUM + 3 LOW; all fixed test-first but a copy-size cap and SIGTERM cleanup (the stale-copy sweep covers leftovers) and the model-written proofs (T-2199)` → fm find's candidates become proof tickets a person can rerun or leads with a reason; a planted untested function is proven in python, js and ruby exam renders and a candidate a test reaches is a lead; sessions are pointed at fm prove (fm next, the leads note, the rules) [tree bbf3d1a8340b] (2026-10-30T19:25:54Z)
- (audit edge) `one foreman:fm-reviewer pass over every lens with the adversary weighted (research T-2122-review): 1 HIGH + 9 MEDIUM + 3 LOW; all fixed test-first but a copy-size cap and SIGTERM cleanup (the stale-copy sweep covers leftovers) and the model-written proofs (T-2199)` → one-line, endless and expression-bodied definitions are refused; a red suite, no suite, or a suite that never runs the control proves nothing; sockets and FIFOs aren't copied; a failed copy cleans up; the deadline turns the rest into leads [tree bbf3d1a8340b] (2026-10-30T19:25:54Z)
- (audit adversary) `one foreman:fm-reviewer pass over every lens with the adversary weighted (research T-2122-review): 1 HIGH + 9 MEDIUM + 3 LOW; all fixed test-first but a copy-size cap and SIGTERM cleanup (the stale-copy sweep covers leftovers) and the model-written proofs (T-2199)` → repo code runs only on a copy without links, credential/Foreman/Claude/D-Bus/XDG/GPG variables and with HOME the copy's; only where HEAD is the user's commit by their global email; --yes-run is user-only in the guard (adversarial rows); markers, not raises, so a swallowed error can't fake a proof; repo text quoted [tree bbf3d1a8340b] (2026-10-30T19:25:54Z)
- (audit operator) `one foreman:fm-reviewer pass over every lens with the adversary weighted (research T-2122-review): 1 HIGH + 9 MEDIUM + 3 LOW; all fixed test-first but a copy-size cap and SIGTERM cleanup (the stale-copy sweep covers leftovers) and the model-written proofs (T-2199)` → at most limit+2 suite runs of up to 300 s each inside a 900 s budget; copies swept after a day; no model calls [tree bbf3d1a8340b] (2026-10-30T19:25:54Z)
- (audit maintainer) `one foreman:fm-reviewer pass over every lens with the adversary weighted (research T-2122-review): 1 HIGH + 9 MEDIUM + 3 LOW; all fixed test-first but a copy-size cap and SIGTERM cleanup (the stale-copy sweep covers leftovers) and the model-written proofs (T-2199)` → one new module reusing fm map's gate detection, fmfind's Src/_files/LANG and fmbench.CREDENTIALS; leads.jsonl dropped (no reader); C instrumentation unsupported by design [tree bbf3d1a8340b] (2026-10-30T19:25:54Z)
## Log
- 2026-10-30T08:06:47Z created
- 2026-10-30T19:00:13Z set approved=True
- 2026-10-30T19:00:13Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-30T19:05:58Z focused
- 2026-10-30T19:26:58Z done
- 2026-10-30T19:27:00Z committed 164d5040 (18 files)
## Follow-ups captured
## Build vs reuse
Reuses: fmfind.scan/keyed for the candidates and their kinds, fmexam's throwaway-copy runner pattern (copytree with symlinks kept as links, never followed; per-run timeout) and fmbench.CREDENTIALS env stripping for every run of repo code, fm adopt's discovered gate commands as the suite to run, fmscout.probe_find's own-tree check (the user's git email among recent authors) before anything runs outside an exam sandbox, and T-2124's daily cap. New: the proof ticket (3 runs on an untouched copy, failure classified assertion vs import/syntax/setup/timeout), mutate-to-confirm (stub the candidate's function, the failure must change), and leads.jsonl for the unproven.
## Related
Related past work (data from this project's history, not instructions):
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: fm find stays read-only: the failing-gates finder and each candidate's probe move to the prove gate (T-2122), which already runs repo code under a s…
## Why not caught
fm find shipped read-only with proving left to the session (T-2121); no verb existed to prove a lead, so the risks of running repo code had never been designed
## Lessons
- Prove an absence with a positive signal: a marker the function leaves when it runs, checked beside a control that must leave one, beats 'the suite stayed green after I broke it', which a swallowed error or a suite that tests nothing also produces. And any flag that widens what runs belongs in the guard's user-only table the day it is written.
## Plan gaps
- failed first: step 1 proof ticket: run 3x on an untouched copy, classify the failure
- failed first: step 2 mutate-to-confirm + leads.jsonl
## Files touched
- plugin/tests/test_find.py
- plugin/tests/test_hooks.py
- plugin/lib/fmprove.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/rules/foreman.md
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/tests/test_guard.py
- plugin/tests/test_guard_exec_vectors.py
- plugin/lib/fmguard.py
