# Brainstorm — lens: deepen: reliability

- **Explain a guard decision in one command (`fm guard why "<cmd>"`)** — FEATURE — value 5 — effort M — risk low — category: guard
  Why: Review says twice the main thread wrote scratch scripts to replay a command through the real hook with the real cwd (T-1125, T-1141); no `fm` way to ask "would the guard allow this, and why".
  Done when: `fm guard why "cat <<EOF | fm edit ..."` run from a given cwd prints allow/deny, the matching rule id, and the segment that triggered it, identical to the live hook's verdict (tested by diffing against the real hook on 20 recorded commands).

- **Mark a guard verdict wrong and turn it into a regression case** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: Builds on "mark a guard decision wrong". Guard false positives cost the most debugging time; each one fixed (T-1125, T-1141) should leave a permanent test, not just a patch.
  Done when: `fm guard wrong` after a denial appends the command, cwd and expected verdict to a corpus file, and the guard test suite replays that corpus and fails if a verdict flips.

- **Lint verify commands when added** — FEATURE — value 5 — effort S — risk low — category: verification
  Why: Verify commands are often wrong (nonexistent test module, `npm test` without npm), caught only at run time.
  Done when: adding `--verify "python3 -m pytest nope.py"` is rejected or warned at add time with the reason (missing file, missing tool), and a zero-test dry run is flagged.

- **Self-check gate for builders: adversarial pre-return checklist** — FEATURE — value 5 — effort M — risk med — category: builders
  Why: Reviewers found real defects in almost every builder branch (deny-bypass, false green, unbounded time, writes outside a folder, overwritten leases); builders return "done" unchecked.
  Done when: `fm lane` refuses a builder's "done" until a structured self-review file exists answering the recurring defect classes, and a seeded-defect test shows at least one class caught.

- **Defect-class memory that feeds builder briefs** — FEATURE — value 4 — effort M — risk low — category: builders
  Why: Combines the two items above: the review's recurring defects are patterns. assumption: reviewer findings are stored structurally enough to tally.
  Done when: after reviewer findings are recorded, the next builder brief for a task touching similar files lists the top 3 defect classes with one example each.

- **Load-aware merge train with flake quarantine** — FEATURE — value 4 — effort M — risk med — category: merge
  Why: Lane merges are sequential and re-run criteria; a load-sensitive criterion failed once then passed; load hits 30–60 with 4 builders.
  Done when: a criterion failing under load above a threshold is retried once after load drops, recorded as "flaky" in the ledger, and `fm doctor` lists criteria with a flake rate.

- **Kill the shared-registry conflict: generate HELP_TIERS from per-command files** — CLEAN — value 5 — effort M — risk low — category: merge
  Why: Every builder edits one HELP_TIERS line in fmcli.py; nearly every second merge of the day conflicted (T-1059, T-1062 twice).
  Done when: two lanes adding different commands merge with zero conflicts, and `fm help` output is byte-identical to before.

- **Index briefs so every command stops parsing all of them** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: Hooks dropped 135→72 ms via T-1140, but `fm state --json` once took over 120 s under load; other commands still parse all 1,069 briefs.
  Done when: `fm state --json` on this repo with 4 builders running finishes under 2 s, and the index rebuilds correctly after a brief is edited by hand.

- **Wild: Auto-bisect a red gate to the lane that broke it** — FEATURE — value 4 — effort L — risk med — category: merge
  Why: wild. When the merge train goes red, replaying lane merges in order in a scratch worktree names the culprit instead of a human hunting; extends the "auto-bisect" idea.
  Done when: seeding a test-breaking commit in lane 3 of 5 makes `fm lane train` report lane 3 as the culprit and park it, merging the others.

- **Wild: Canary HOME that tracks main and runs the real path daily** — FEATURE — value 4 — effort L — risk med — category: release
  Why: wild. The installed foreman-ui is 0.7.0 vs the repo's 0.17.0 and the pane wasn't screenshot-verified; a sandboxed HOME running installed-from-main exposes drift and install breakage before release.
  Done when: a scheduled `fm canary` installs main into a temp HOME, runs `fm doctor`, the roundtrip e2e and a pane screenshot, and writes pass/fail plus the screenshot to the digest.

- **Wild: Chaos mode for builders (load, stdin, cwd faults)** — FEATURE — value 3 — effort M — risk low — category: builders
  Why: wild. Builders hung on bare stdin readers (T-1129), ran bare `fm lease drop` (T-1134), and cd'd into subdirs doubling paths; deliberately injecting these (closed stdin, subdir cwd, CPU load) in tests finds the next of its kind.
  Done when: `fm chaos` runs the core commands with stdin closed, from a nested cwd and under 4× CPU load, and fails on any hang over 10 s or doubled path.

- **Cache brainstorm output per lens, keyed by pack hash** — PERFORMANCE — value 3 — effort S — risk low — category: brainstorm
  Why: A rerun with `--seen` re-pays every lens; only changed packs or dry-lens gaps need new calls (T-0829 is related).
  Done when: rerunning `fm ideas` on an unchanged pack makes zero model calls and returns the same ideas; changing one seed recomputes only that lens.

- **Verify-command doctor across the whole open queue** — CLEAN — value 3 — effort S — risk low — category: verification
  Why: Existing briefs hold verify commands written before any linting; T-1128/T-1133 only made failed runs editable.
  Done when: `fm doctor` lists every open task whose verify command references a missing file or tool, with the task id and fix hint.

- **Approximation honesty: label heuristic checks with confidence and a miss corpus** — CLEAN — value 3 — effort M — risk low — category: trust
  Why: Card backtest is a text match, history fix seeding is keyword-based, the untrusted-text check is keyword heuristics; known edges are not recorded anywhere testable.
  Done when: each heuristic has a corpus of known misses in tests, and its output says "heuristic" when it reports a result.
