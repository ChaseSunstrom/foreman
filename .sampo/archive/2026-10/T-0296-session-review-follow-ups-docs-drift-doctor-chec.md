---
id: T-0296
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-04T09:02:30Z
updated: 2026-10-04T09:28:33Z
batch: [T-0292, T-0293, T-0294]
base: f856062a2f227bb2dab5e088738eba1b9fabe92c
base_tree: 9abb72b0d5efe30ea0449422473d66b907925d8f
verified: strong
---
# Session-review follow-ups: docs drift, doctor checks routing and scopes integrity, ignored flags refused, duel rivals m…
## Raw request
> T-0292: FIX: docs drift after the passes — MASTER's T-0271 line still says hunks revert with git apply -R (replaced in T-0286), the prove --hunks ponytail comment predates per-definition splitting, the MASTER CLI line and fmbench file map miss landscape/deps/replay --cmd/bench duel|versions|court|soak
> T-0293: FIX: operator gaps from the session review — fm doctor never runs routing_problem (a broken routing.json silently empties hints and --split groups); fm replay --cwd without --cmd and fm second debate --model are accepted and ignored; fm doctor's integrity check fails every project's gate for one damaged unrelated repo (other projects should warn)
> T-0294: fm bench duel loads the rival plugin into a bypass-mode replay without any check: document that rivals must be trusted, or accept only installed plugin ids
## Interpretation
Follow-ups the whole-session review graded LOW: docs drift, operator gaps (silent routing breakage, flags accepted and ignored, one damaged project failing everyone's doctor gate), and duel rivals loaded into bypass-mode replays unchecked.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0292: MASTER no longer says hunks revert with git apply; its CLI line names landscape, deps, replay --cmd and bench duel/versions/court/soak; the fmbench file-map entry names them too — verify with `python3 plugin/tests/run.py -p test_followups.py -k Docs`
- [x] T-0293: fm doctor fails on a routing.json routing_problem rejects; fm replay --cwd without --cmd and fm second debate --model are refused; integrity damage in another project's repo or state warns, while damage in Foreman's own repo or the current project still fails — verify with `python3 plugin/tests/run.py -p test_followups.py -k Operator`
- [x] T-0294: fm bench duel takes only an installed plugin (an id, or the folder of one); any other folder is refused before a session starts — verify with `python3 plugin/tests/run.py -p test_followups.py -k Rival`
## Non-goals
## Approach (options → choice → why)
Docs: edit the drifted lines. Doctor: check_routing(path) via c.routing_problem; check_integrity tags each finding with its root/project and fails only for Foreman's home and the current project, warning otherwise. Flags: refuse rather than document. Rival: installed plugins are already trusted to run in the user's own sessions; arbitrary folders aren't, so a duel takes only installed ones (no new trust surface).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0292: FIX: docs drift after the passes — MASTER's T-0271 line still says hunks revert with git a
2. [x] T-0293: FIX: operator gaps from the session review — fm doctor never runs routing_problem (a broke
3. [x] T-0294: Fm bench duel loads the rival plugin into a bypass-mode replay without any check: document
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_followups.py` → ✗ exit 1 · Ran 5 tests in 7.4s (3 classes, 16 at a time; slowest: Operator 7s, Rival 0s, Docs 0s) / FAILED (3 classes) [ran] [tree 9abb72b0d5ef] (2026-10-04T09:15:08Z)
- (step 1) `python3 plugin/tests/run.py -p test_followups.py -k Docs` → exit 0 · Ran 1 tests in 0.0s (1 classes, 16 at a time; slowest: Docs 0s) / OK [ran] [tree 060675bad457] (2026-10-04T09:16:27Z)
- (step 2) `python3 plugin/tests/run.py -p test_followups.py -k Operator` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Operator 0s) / OK [ran] [tree 060675bad457] (2026-10-04T09:16:27Z)
- (step 3) `python3 plugin/tests/run.py -p test_followups.py -k Rival` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Rival 0s) / OK [ran] [tree 060675bad457] (2026-10-04T09:16:27Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 796 tests in 31.4s (190 classes, 16 at a time; slowest: Stop 22s, TaskLifecycle 19s, Parallel 18s) / FAILED (1 classes) [ran] [tree 060675bad457] (2026-10-04T09:17:51Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.0    30.3     150  [0] / SessionEnd                  28.6    31.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 796 tests in [ran] [tree 7a8c91eb6631] (2026-10-04T09:20:37Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_followups.py && python3 plugin/tests/run.py -p "test_integrity*" && python3 plugin/tests/run.py -p "test_bench_family*" -k Duel` → 9/17 hunks proven; unproven: plugin/lib/fmbench.py @@ -512 +512,3 @@ def _contender(spec):; plugin/lib/fmbench.py @@ -574,2 +575,2 @@ def _contest(p, args):; plugin/lib/fmcli.py @@ -617,2 +617,2 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmcli.py @@ -2269 +2269 @@ def build_parser():; plugin/lib/fmdoctor.py @@ -585,0 +588 @@ def check_integrity(roots, projects):; plugin/lib/fmdoctor.py @@ -655 +673,2 @@ def run_all(full=False):; plugin/lib/fmsecond.py @@ -197 +197 @@ def cmd_second(args):; plugin/lib/fmsecond.py @@ -207 +209 @@ def cmd_second(args): [inconclusive] [ran] [tree 7a8c91eb6631] (2026-10-04T09:21:45Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_followups.py && python3 plugin/tests/run.py -p "test_integrity*" && python3 plugin/tests/run.py -p "test_bench_family*" -k Duel` → 9/17 hunks proven; unproven: plugin/lib/fmbench.py @@ -512 +512,3 @@ def _contender(spec):; plugin/lib/fmbench.py @@ -574,2 +575,2 @@ def _contest(p, args):; plugin/lib/fmcli.py @@ -617,2 +617,2 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmcli.py @@ -2269 +2269 @@ def build_parser():; plugin/lib/fmdoctor.py @@ -585,0 +588 @@ def check_integrity(roots, projects):; plugin/lib/fmdoctor.py @@ -655 +673,2 @@ def run_all(full=False):; plugin/lib/fmsecond.py @@ -197 +197 @@ def cmd_second(args):; plugin/lib/fmsecond.py @@ -207 +209 @@ def cmd_second(args): [inconclusive] [ran] [tree 7a8c91eb6631] (2026-10-04T09:22:54Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_followups.py && python3 plugin/tests/run.py -p "test_integrity*" && python3 plugin/tests/run.py -p "test_second*" && python3 plugin/tests/run.py -p "test_bench_family*" -k Duel` → 13/17 hunks proven; unproven: plugin/lib/fmbench.py @@ -512 +512,3 @@ def _contender(spec):; plugin/lib/fmbench.py @@ -574,2 +575,2 @@ def _contest(p, args):; plugin/lib/fmcli.py @@ -617,2 +617,2 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmdoctor.py @@ -655 +673,2 @@ def run_all(full=False): [inconclusive] [ran] [tree 521011f0bbd9] (2026-10-04T09:24:18Z)
- (step 1) `python3 plugin/tests/run.py -p test_followups.py -k Docs` → exit 0 · Ran 1 tests in 0.0s (1 classes, 16 at a time; slowest: Docs 0s) / OK [ran] [tree b4780854e6dc] (2026-10-04T09:26:08Z)
- (step 2) `python3 plugin/tests/run.py -p test_followups.py -k Operator` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Operator 0s) / OK [ran] [tree b4780854e6dc] (2026-10-04T09:26:09Z)
- (step 3) `python3 plugin/tests/run.py -p test_followups.py -k Rival` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Rival 0s) / OK [ran] [tree b4780854e6dc] (2026-10-04T09:26:09Z)
- (step 3) `python3 plugin/tests/run.py -p test_followups.py -k Lfs` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Lfs 0s) / OK [ran] [tree b4780854e6dc] (2026-10-04T09:26:09Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.2    33.1     150  [0] / SessionEnd                  28.3    30.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 797 tests in [ran] [tree b4780854e6dc] (2026-10-04T09:27:04Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_followups.py && python3 plugin/tests/run.py -p "test_integrity*" && python3 plugin/tests/run.py -p "test_second*" && python3 plugin/tests/run.py -p "test_bench_family*" -k Duel` → 15/20 hunks proven; unproven: plugin/lib/fmbench.py @@ -35,10 +38,6 @@ def _git(root, *args, timeout=120):; plugin/lib/fmbench.py @@ -512 +512,3 @@ def _contender(spec):; plugin/lib/fmbench.py @@ -574,2 +575,2 @@ def _contest(p, args):; plugin/lib/fmcli.py @@ -617,2 +617,2 @@ def task_prove_hunks(p, b, args):; plugin/lib/fmdoctor.py @@ -655 +675,2 @@ def run_all(full=False): [inconclusive] [ran] [tree b4780854e6dc] (2026-10-04T09:28:21Z)
- (ac 1) `python3 plugin/tests/run.py -p test_followups.py -k Docs` → exit 0 · Ran 1 tests in 0.0s (1 classes, 16 at a time; slowest: Docs 0s) / OK [ran] [tree b4780854e6dc] (2026-10-04T09:28:32Z)
- (ac 2) `python3 plugin/tests/run.py -p test_followups.py -k Operator` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Operator 0s) / OK [ran] [tree b4780854e6dc] (2026-10-04T09:28:32Z)
- (ac 3) `python3 plugin/tests/run.py -p test_followups.py -k Rival` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Rival 0s) / OK [ran] [tree b4780854e6dc] (2026-10-04T09:28:32Z)
- (audit intent) `one fm-reviewer pass, intent + edge (T-0296-review-1): approve with 2 LOW edge findings — a lane's own repo damage only warned, and a doctor run from no project failed every project — both fixed test-first (a lane counts as its main checkout; current=False makes only Foreman's own repo fail). The background security review then found the lfs prefix bypass in T-0291's code (T-0299, logged as an escape): lfs now always runs git-lfs's fixed commands — test planted 'git-lfs smudge -- %f; touch' and saw it stop running. Hunks 15/20 (rest: docstring, message, comment, doctor wiring, and the old discovery code whose revert the proven canonical override still covers)` → three member criteria met with tests (Docs, Operator, Rival) plus the lfs escape [tree b4780854e6dc] (2026-10-04T09:28:32Z)
- (audit edge) `one fm-reviewer pass, intent + edge (T-0296-review-1): approve with 2 LOW edge findings — a lane's own repo damage only warned, and a doctor run from no project failed every project — both fixed test-first (a lane counts as its main checkout; current=False makes only Foreman's own repo fail). The background security review then found the lfs prefix bypass in T-0291's code (T-0299, logged as an escape): lfs now always runs git-lfs's fixed commands — test planted 'git-lfs smudge -- %f; touch' and saw it stop running. Hunks 15/20 (rest: docstring, message, comment, doctor wiring, and the old discovery code whose revert the proven canonical override still covers)` → lane worktrees, no-project doctor runs, old git, LFS repos [tree b4780854e6dc] (2026-10-04T09:28:32Z)
## Log
- 2026-10-04T09:02:30Z created
- 2026-10-04T09:15:01Z focused
- 2026-10-04T09:26:02Z scope: T-0299 (lfs prefix bypass in T-0291's bench filter code, found by the background security review) fixed here — this task already touches fmbench.py
- 2026-10-04T09:26:02Z includes T-0299: SECURITY: the bench's git-lfs exemption (T-0291) trusts any lfs driver value starting 'git
- 2026-10-04T09:28:32Z done
- 2026-10-04T09:28:33Z committed e96aade (9 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0258-review-1: Verdict:** changes needed. I found one HIGH cross-feature issue, two MEDIUM, and the rest are LOW doc or maintainer drift. I read the whole dif…
- research T-0280-review-1: Changes needed. No CRITICAL or HIGH findings, but I found three MEDIUM issues on the guard and untrusted-text paths you flagged. [stale: plugin…
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- research T-0212-review: Verdict: changes needed.** There are no CRITICAL or HIGH findings. Two MEDIUM issues are worth fixing before relying on `compare`. I read the cod…
## Lessons
- Never allowlist a shell command by prefix; replace it with the known command instead
## Files touched
- MASTER.md
- plugin/lib/fmcli.py
- plugin/tests/test_followups.py
- plugin/lib/fmsecond.py
- plugin/lib/fmreplay.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmbench.py
- plugin/tests/test_bench_family.py
- CHANGELOG.md
