# Brainstorm — lens: user value

- **Recall related history at intake** — FEATURE — value 5 — effort M — risk low
  Why: decisions.md, research/ and archived briefs are never surfaced; SessionStart carries only state lines.
  Done when: `fm recall` (a stdlib TF-IDF index over decisions, research, briefs and findings, rebuilt on `fm` writes, never in the hook) makes UserPromptSubmit add a ≤400-char "Related: D-7, T-0021, research/auth.md" note. A fixture test with a matching past decision shows it, and p50 hook latency stays under 30 ms.

- **Keep a per-project map current** — FEATURE — value 5 — effort M — risk med
  Why: every intake re-reads code from scratch, with no entry points, test commands, hot files or test-to-source links.
  Done when: `fm map` writes map.json (entry points, test commands, import/name-based test↔source links, hot files from git log). It refreshes on `fm task done` and the intake grounding step reads it. A fixture repo yields correct covering tests for a scope glob, and a stale map is flagged.

- **Verify what changed first, against a baseline** — FEATURE — value 5 — effort M — risk med
  Why: `fm check` is "exit 0" over all gates and can't tell pre-existing failures or flaky tests from regressions.
  Done when: `fm baseline` records gate results at focus time. `fm check --affected` runs covering tests first, reruns failures once to mark flaky ones, and labels each failure "new", "pre-existing" or "flaky". A task with an already-red test can reach done, and a new failure blocks it.

- **Reject regression tests that pass without the fix** — FEATURE — value 4 — effort M — risk med
  Why: weak tests are caught only by TDD instructions, not by code.
  Done when: `fm task evidence --proves-change` runs the new test on a copy of the tree with the change reverted (a temp worktree, no edits to the user's tree). FIX tasks need it to fail there and pass with the change. A test that passes either way is refused.

- **Match failures against earlier fixes** — FEATURE — value 4 — effort S — risk low
  Why: failure causes aren't collected, so the same bug can be re-diagnosed from scratch.
  Done when: PostToolUseFailure and blocked tasks store a normalized error signature plus files in failures.jsonl, with the resolution added at `task done`. A repeat signature makes the next-action note say "seen in T-xx, fixed by …". A test replays two tasks and gets the match.

- **Calibrate tier and effort from the ledger** — PERFORMANCE — value 3 — effort M — risk low
  Why: `guess_tier` is regex plus length and ignores how tasks actually turned out.
  Done when: nearest-neighbour over finished tasks (type, scope keywords → steps, attempts, files, duration) proposes the tier and shows "similar tasks took N steps". Falls back to the regex under ~10 samples. On replay of the existing ledger it beats the regex tier accuracy.

- **Auto-distill lessons and re-check decisions on overlap** — FEATURE — value 4 — effort M — risk med
  Why: lessons exist only if reflect is run by hand; autonomous decisions are never revisited; projects are siloed.
  Done when: `fm task done` requires 1–3 scoped lessons and decisions get a revisit trigger (globs). Later tasks touching those globs get "decision D-7 / lesson L-3 applies" in the brief. Lessons tagged as stack-generic go to an opt-in user-level file that other projects can recall. Assumption: uninstall removes that file.
