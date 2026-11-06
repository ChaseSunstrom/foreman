---
id: T-0270
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-04T06:50:27Z
updated: 2026-10-04T07:00:40Z
base: 447785a7a935a936c00e7d4b0aab82092af84b43
base_tree: aecc8a89b46866964645f84ba73f434f67078f23
verified: strong
---
# Guard: git's remaining write and exec channels
## Raw request
> Guard: git's remaining write and exec channels — git config writing exec keys/aliases (and --file targets), file-writing env vars (GIT_TRACE*, GIT_INDEX_FILE), subcommand exec flags (rebase --exec, bisect run, submodule foreach, difftool -x, grep -O, --upload-pack/--receive-pack, filter-branch filters), config from files (include.path, GIT_CONFIG_GLOBAL/SYSTEM, HOME, XDG_CONFIG_HOME, --template), more write targets (archive -o, bundle create, worktree add, init, format-patch -o/--output-directory, --separate-git-dir, checkout-index --prefix, submodule add), exported exec vars in an earlier command (research T-0269-review-2)
## Interpretation
Close the git channels the T-0269 adversary pass found that predate it: ways a git command writes files or runs a command the guard never looks at.
## Assumptions (confidence)
## Acceptance criteria
- [x] every channel in research T-0269-review-2 (git config exec keys/aliases/--file, GIT_TRACE*/GIT_INDEX_FILE, subcommand exec flags, config from files, extra write targets, exported exec vars) is blocked or checked as typed, and ordinary git commands still pass — verify with `python3 plugin/tests/run.py -p "test_guard_git*"`
- [x] fm replay finds no newly allowed command and the guard suite passes — verify with `python3 plugin/tests/run.py -p "test_guard*"`
## Non-goals
## Approach (options → choice → why)
Options: (a) refuse every git command carrying -c/env config; (b) model each channel: a command value is re-checked as typed (check_bash), a file value is a write target, config loaded from a file is refused (system, user-grantable). Choice (b): (a) blocks everyday git (git -c user.name=…), while (b) keeps them and closes each channel at the place git reads it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_guard_git.py table of channel commands (blocked) and everyday git commands (allowed)
2. [x] Implement: assignment channels in check_bash, git config/subcommand exec flags/config-from-file in _git_code, write targets in _write_targets
3. [x] Docs: MASTER.md guard section, CHANGELOG.md
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_guard_git*"` → ✗ exit 1 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: GitChannels 0s) / FAILED (1 classes) [ran] [tree 6ddeb57e5a67] (2026-10-04T06:52:32Z)
- (step 1) `python3 plugin/tests/run.py -p "test_guard_git*"` → ✗ exit 1 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: GitChannels 0s) / FAILED (1 classes) [ran] [tree e728dc5c988d] (2026-10-04T06:52:54Z)
- (step 2) `python3 plugin/tests/run.py -p "test_guard*"` → exit 0 · Ran 59 tests in 1.2s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree c2fc1ea94d5b] (2026-10-04T06:55:03Z)
- (step 3) `grep -c 'T-0270' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree 6b490087f20a] (2026-10-04T06:55:19Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.8    33.6     150  [0] / SessionEnd                  28.6    29.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → e [ran] [tree 6b490087f20a] (2026-10-04T06:56:14Z)
- (step 2) `python3 plugin/tests/run.py -p "test_guard*"` → exit 0 · Ran 59 tests in 1.2s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree cf85614952d0] (2026-10-04T06:59:30Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    32.3     150  [0] / SessionEnd                  28.3    28.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → e [ran] [tree d77544e9a340] (2026-10-04T07:00:25Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_guard_git*"` → exit 0 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: GitChannels 0s) / OK [ran] [tree d77544e9a340] (2026-10-04T07:00:40Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_guard*"` → exit 0 · Ran 59 tests in 1.1s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, Core 0s) / OK [ran] [tree d77544e9a340] (2026-10-04T07:00:40Z)
- (audit intent) `fm-reviewer pass over all lenses, adversary-weighted (research T-0270-review-1); 1 HIGH regression + 4 MEDIUM + 2 LOW fixed with bypass-form tests; replay of 5,000 real commands: 0 newly blocked, 0 newly allowed` → every channel from T-0269-review-2 blocked or checked as typed; everyday git passes [tree d77544e9a340] (2026-10-04T07:00:40Z)
- (audit adversary) `fm-reviewer pass over all lenses, adversary-weighted (research T-0270-review-1); 1 HIGH regression + 4 MEDIUM + 2 LOW fixed with bypass-form tests; replay of 5,000 real commands: 0 newly blocked, 0 newly allowed` → fixed — assignments read behind wrappers/keywords (timeout, env -u, do, nice), NAME+= recognised (and no longer mistaken for the command by _strip_wrappers), clone -c/--config, init.templateDir, abbreviated long options, more command-valued keys, init --separate-git-dir X [tree d77544e9a340] (2026-10-04T07:00:40Z)
- (audit edge) `fm-reviewer pass over all lenses, adversary-weighted (research T-0270-review-1); 1 HIGH regression + 4 MEDIUM + 2 LOW fixed with bypass-form tests; replay of 5,000 real commands: 0 newly blocked, 0 newly allowed` → ok — no crash on empty git config, export without =, empty values, unicode; tests probe with a payload only a parse can catch (rm -rf ~/Documents), not a word scan [tree d77544e9a340] (2026-10-04T07:00:40Z)
- (audit operator) `fm-reviewer pass over all lenses, adversary-weighted (research T-0270-review-1); 1 HIGH regression + 4 MEDIUM + 2 LOW fixed with bypass-form tests; replay of 5,000 real commands: 0 newly blocked, 0 newly allowed` → ok — docs; 0 replay false positives [tree d77544e9a340] (2026-10-04T07:00:40Z)
- (audit maintainer) `fm-reviewer pass over all lenses, adversary-weighted (research T-0270-review-1); 1 HIGH regression + 4 MEDIUM + 2 LOW fixed with bypass-form tests; replay of 5,000 real commands: 0 newly blocked, 0 newly allowed` → ok — _git_writes and _git_pos are plain functions; one channel table per kind [tree d77544e9a340] (2026-10-04T07:00:40Z)
## Log
- 2026-10-04T06:50:27Z created
- 2026-10-04T06:52:12Z planned from capture
- 2026-10-04T06:52:15Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-04T06:52:15Z focused
- 2026-10-04T07:00:40Z done
- 2026-10-04T07:00:40Z committed 18ac1e4 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0269-review-2: Verdict:** changes needed. I read the code only and ran nothing, so each "not blocked" below comes from tracing the code and is unexecuted.
- research T-0269-review-1: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict [stale: plugin/lib/fmcore.py, plugin/lib/fmguard.py chang…
- research t0018-r1-maintainer: "fm: {e.args[0] if e.args else e}\"` — for a `KeyError('intent')` that prints exactly `fm: intent`, which reads like a value, not an error,…
- research t0018-r4-adversary: fSTe81D17ZxNHRCBuwq4","type":"message","role":"assistant","content":[{"type":"text","text":"## Verdict: changes needed\n\n## Findings\n\n**C…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Guard tests must use a payload only a real parse can catch: a core path inside quotes is caught by the word scan anyway, so such tests pass even when the channel isn't handled
## Files touched
- plugin/tests/test_guard_git.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
