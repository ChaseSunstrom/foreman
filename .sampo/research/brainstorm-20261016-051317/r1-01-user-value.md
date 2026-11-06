# Brainstorm — lens: user value

- **Check a verify command when it is added** — FIX — value 5 — effort S — risk low — category: reliability of proofs
  Why: the review notes say verify commands are often wrong (nonexistent test module, `npm test` with no npm) and are caught only when they run; T-1128/T-1133 made runs editable but nothing validates at add time.
  Done when: `fm verify add` with a nonexistent module or missing binary is refused with the reason and a suggested command from `fm map` gates, and a test covers both cases.

- **Ask the guard "would this run here, and why"** — FEATURE — value 5 — effort S — risk low — category: guard debugging
  Why: the main thread twice wrote a scratch script to replay a command through the real hook with the real cwd (T-1125, T-1141); no `fm` verb does it.
  Done when: `fm guard explain '<cmd>' [--cwd DIR]` prints allow/deny, the matching rule and the safe alternative, using the same code path as the hook (a test asserts parity on 20 recorded commands).

- **Make registries append-only fragments so parallel builders never conflict** — CLEAN — value 5 — effort M — risk med — category: parallel lanes
  Why: every new command edits one HELP_TIERS line in fmcli.py; nearly every second merge conflicted (T-1059, T-1062 twice) and needed a re-merge builder.
  Done when: HELP_TIERS (and similar shared registries) are assembled from one-file-per-verb declarations, and two lanes adding different verbs merge with no conflict in a scripted test.

- **Make builders run an adversarial self-check before returning "done"** — FEATURE — value 5 — effort M — risk med — category: builder quality
  Why: reviewers found real defects in almost every builder branch (deny-bypass, false green, unbounded time, writes outside a folder, overwritten leases) while builders reported done.
  Done when: `fm lane` refuses a builder's "done" without a self-check receipt listing the diff's risky surfaces (deny paths, timeouts, path confinement, leases) each with a probe command it ran; a seeded-defect branch is rejected.

- **Normalise builder cwd and paths** — FIX — value 4 — effort S — risk low — category: builder hygiene
  Why: builders cd into subdirectories so relative paths double (lease paths `mods/foreman-ui/mods/foreman-ui/...`).
  Done when: lease, claim and edit verbs resolve against the worktree root regardless of cwd, and a test run from a subdirectory yields the same lease path as from the root.

- **Index briefs so no command parses all of them** — PERFORMANCE — value 4 — effort M — risk low — category: speed under load
  Why: hooks dropped 135→72 ms by skipping brief parsing (T-1140), but other commands still parse all 1,069 briefs; `fm state --json` once took over 120 s under load.
  Done when: `fm state --json` on this repo's state completes in under 2 s with load simulated by 4 busy processes, using a stat-keyed brief index that rebuilds itself when stale.

- **Merge lanes with criteria re-run only on what the merge touched** — PERFORMANCE — value 4 — effort M — risk med — category: merge train
  Why: lane merges are sequential and re-run every criterion; a load-sensitive criterion once failed a merge and then passed.
  Done when: a merge re-runs only criteria linked to the merged files plus a full run at train end, and a flaky criterion is retried once and logged as flaky rather than failing the merge.

- **Screenshot-gate the pane and flag the release lag** — FIX — value 4 — effort M — risk low — category: UI verification
  Why: the pane wasn't screenshot-verified this round, and the installed foreman-ui is 0.7.0 while the repo's is 0.17.0, so marketplace users lag.
  Done when: `fm doctor` reports the installed vs repo foreman-ui version with the update command, and a CI/gate step renders each pane state to a screenshot and fails on diff beyond a threshold.

- **Replace keyword heuristics with a measured accuracy report** — CLEAN — value 3 — effort M — risk low — category: honesty of approximations
  Why: card backtest is a text match, history fix seeding is keyword-based, the untrusted-text check is keyword heuristics; none have a known false-positive rate.
  Done when: each approximation has a labelled corpus from past ledger cases and `fm doctor --accuracy` prints precision/recall for each, with a ratchet test that fails if they drop.

- **Wild: Make a "why did the last merge conflict" auto-resolver for shared lists** — FEATURE — value 3 — effort M — risk med — category: parallel lanes
  Why: assumption: conflicts on sorted/registry lines are mechanical, so a merge driver can union them. Wild.
  Done when: a git merge driver registered by `fm init` resolves two-lane additions to a sorted list file with no human step in a scripted test.

- **Wild: Let the user say "keep going" once and get a signed overnight contract** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the user repeatedly says they are AFK and "I shouldn't need to ask"; each round restates permission. Wild.
  Done when: a single phrase creates a contract file (scope, budget, stop conditions, what is off-limits) that later rounds cite instead of re-asking, and `fm contract show` lists it with spend so far.

- **Wild: A "what did I miss" receipt written for the user after every AFK stretch** — FEATURE — value 4 — effort S — risk low — category: close-out legibility
  Why: the user goes AFK for long runs and only the final report carries what needs them; assumption: they'd rather skim one page ranked by "needs you".
  Done when: on first prompt after 30+ minutes idle, one screen lists shipped, failed, needs-you (with the command to resolve each) and spend, under 25 lines.

- **Wild: Pre-merge "conflict forecast" from lane touch-sets** — FEATURE — value 3 — effort S — risk low — category: parallel lanes
  Why: lanes collide on shared registry files; assumption: touch-sets predicted from similar tasks flag it before dispatch.
  Done when: `fm lane plan` warns when two queued tasks are predicted to touch the same file and serialises or splits them, verified on the HELP_TIERS case.
