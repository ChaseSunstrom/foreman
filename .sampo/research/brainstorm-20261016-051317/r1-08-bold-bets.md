# Brainstorm — lens: bold bets

- **Make the registry edit-free: auto-collect verbs from files** — CLEAN — value 4 — effort M — risk low — category: dev experience
  Why: Review says parallel builders all edit one HELP_TIERS line in fmcli.py; nearly every second merge conflicted (T-1059, T-1062 twice) and needed a re-merge builder.
  Done when: adding a verb touches only its own file (a `# tier:` header is discovered at load), and two lanes that each add a verb merge with zero conflicts in a test.

- **Add `fm why-blocked "<command>"`: replay a command through the real guard** — FEATURE — value 5 — effort S — risk low — category: guard
  Why: Review says the main thread twice wrote scratch scripts to replay a command through the real hook with the real cwd (T-1125, T-1141); no `fm` way to ask.
  Done when: `fm why-blocked 'cmd'` prints allow/deny, the matching rule and the cwd used, and gives the same verdict as the live hook on a recorded corpus.

- **Lint verify commands when they are added** — FIX — value 4 — effort S — risk low — category: verification
  Why: Review says verify commands are often wrong (nonexistent test module, `npm test` without npm) and are caught only when run.
  Done when: adding a verify command that names a missing file or tool is refused with the reason, and a valid one passes; tested with both fixtures.

- **Require an adversarial self-check receipt before a builder says done** — FEATURE — value 5 — effort M — risk med — category: builders
  Why: Reviewers found real defects in almost every builder branch (deny-bypass, false green, unbounded time, writes outside a folder, overwritten leases).
  Done when: a builder's return is rejected unless it carries a receipt listing the attacks it tried (bypass, empty input, path escape, timeout), and a seeded flawed branch gets caught by that step.

- **Pin builders' cwd and normalise lease paths to the repo root** — FIX — value 3 — effort S — risk low — category: builders
  Why: Review shows builders cd into subdirectories so lease paths double (`mods/foreman-ui/mods/foreman-ui/...`).
  Done when: a lease taken from any subdirectory is stored repo-relative, and a test of `cd mods/x && fm lease` yields the single path.

- **Cache a brief index so no command parses all briefs** — PERFORMANCE — value 4 — effort M — risk low — category: performance
  Why: Review: `fm state --json` once took over 120 s under load, and other commands still parse every one of 1,069 briefs after hooks were fixed (T-1140).
  Done when: `fm state --json` on this repo runs under 2 s at load 30, with the index rebuilt automatically on a stale mtime and a test that corrupts it.

- **Make the merge train load-aware: retry load-sensitive criteria once, then flag them** — FIX — value 3 — effort S — risk low — category: reliability
  Why: Review says a load-sensitive criterion failed a merge once, then passed; lane merges are sequential and each re-runs criteria.
  Done when: a criterion failing only under load is retried once and marked "flaky-under-load" in the ledger, and a genuine failure still fails both runs.

- **Screenshot-gate the pane in the release path** — FEATURE — value 4 — effort M — risk med — category: UI
  Why: Review: the pane wasn't screenshot-verified this round; installed foreman-ui is 0.7.0 vs the repo's 0.17.0, so marketplace users lag.
  Done when: `fm release` fails if no pane screenshots from the current build exist, and `fm doctor` warns when the installed foreman-ui is more than one minor behind.

- **Replace the keyword heuristics with a measured accuracy report** — CLEAN — value 3 — effort M — risk low — category: honesty
  Why: Review lists card backtest (text match), history fix seeding (keywords) and the untrusted-text check as approximations with known edges.
  Done when: each heuristic has a labelled corpus and `fm doctor --accuracy` prints precision/recall, failing below a recorded floor.

- **Wild: Run Foreman against a "skeptic twin" that tries to make every builder branch fail before review** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: wild; assumption: the reviewer defect rate is high enough that a cheap pre-review attacker on the cheapest model saves more than it costs.
  Done when: on 5 past branches with known defects, the twin finds at least 4 of them in under 5 minutes each.

- **Wild: Give the guard a "what-if" playground in the pane** — FEATURE — value 3 — effort M — risk low — category: guard UI
  Why: wild; builds on the guard-debugging pain: type a command into the pane and watch the verdict and matched rule light up live.
  Done when: entering a command in the pane shows the same verdict as `fm why-blocked`, within 200 ms.

- **Wild: Make the final report a one-page "what only you can do" checklist with copy-paste commands** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: wild; the mission says in full autonomy ask nothing and put user-only actions (blocked T-0325 sudo pacman, T-0418 foreman-ui update, T-0352 publish) in the final report.
  Done when: the final report lists each blocked item with its exact command and a verify command, generated from the blocked queue.

- **Auto-split shared hot-spot files by a conflict-history report** — CLEAN — value 3 — effort M — risk low — category: dev experience
  Why: HELP_TIERS is one symptom; assumption: other shared files (register.tsx per T-0166, changelogs, test registries) conflict similarly.
  Done when: `fm hotspots` ranks files by merge conflicts from the ledger, and the top three are split or made append-only.

- **Wild: Auto-bisect a flaky or red gate to the lane that introduced it during the merge train** — FEATURE — value 3 — effort M — risk med — category: reliability
  Why: wild; the sequential merge train re-runs criteria per lane, so the culprit lane is already isolated by order.
  Done when: a seeded red criterion in lane 3 of 5 is attributed to lane 3 and only that lane is bounced.
