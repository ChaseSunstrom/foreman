# Brainstorm — lens: user value

- **Sweep near-miss inputs through every string and pattern match** — FEATURE — value 5 — effort M — risk low — category: bug finder
  Why: the user's first ask was test_ship's `--check` failing because a hash ending in "add" matched the substring "add a". Substring, regex and prefix heuristics are a bug class that exam repos in any language will have too.
  Done when: on a planted repo with 3 substring-vs-word matchers, the finder emits 3 failing tests, each red on the untouched tree, and emits none on the clean twin.

- **Hunt for time bombs and file them by deadline** — FEATURE — value 4 — effort M — risk low — category: scout probe
  Why: assumption: nobody asks for work whose deadline hasn't hit yet. Targets are hardcoded dates, skip-until markers, cert and token expiries, and runtimes near end-of-life in CI files and manifests. Today is 2026-10-30, so Python 3.10 reaches EOL this month.
  Done when: a fixture with an expired `skipUntil`, a CI pin on an EOL runtime and a date literal in the past yields three findings, each with its date and a ranking that puts the nearest deadline first.

- **Turn the user's repeated manual follow-ups into triggers** — FEATURE — value 5 — effort M — risk med — category: initiative
  Why: the asks show "re-ship", "re-record" and "re-match the site" recurring, and a leftover question asks which follow-ups have no trigger. Foreman can mine the intake history for verbs asked 3 or more times and propose an "after X, always Y" task.
  Done when: given a fixture history with "re-ship the site" asked 3 times, `fm find` proposes a hook task that cites those 3 asks. Declining it records a fingerprint so it never reappears.

- **Rank findings by closeness to what the user already cares about** — FEATURE — value 4 — effort M — risk low — category: ranking
  Why: unasked work is easier to accept next to the current mission, such as findings in files near open tasks or in surfaces the user keeps asking about (site, genesis). Ranking by value alone ignores that.
  Done when: two findings of equal value, one in an open task's neighbourhood by import graph, rank neighbour-first, and the shown formula includes a proximity term.

- **Stop at the first proven win and show it within minutes** — PERFORMANCE — value 4 — effort S — risk low — category: first run
  Why: the pack shows the finders spending money for 0 of 108 defects, and a new user judges Foreman on the first scan. Running probes cheapest-first and printing the first red-on-untouched-tree test immediately gives value before the full sweep finishes.
  Done when: on a fixture with one cheap-to-find proven bug, the first finding prints before the slowest probe starts, and the elapsed time is on its line.

- **Resurrect abandoned work: stashes, stale branches, half-finished lanes** — FEATURE — value 3 — effort M — risk low — category: scout probe
  Why: assumption: users leave unfinished work that is already designed and half-written, which is cheaper to finish than a new finding is to prove. Foreman already reaps lane branches but doesn't offer to finish them.
  Done when: a repo with a 2-week-old stash and an unmerged branch yields two "finish this" cards, each naming its last commit and what the gates say about it.

- **Pair findings in a weekly 5-question ranking quiz** — FEATURE — value 3 — effort M — risk low — category: value calibration
  Why: the value formula's weights are a guess until the user's taste feeds them. Pairwise "which would you rather have fixed?" answers are cheap to give and calibrate weights better than 30-day survival alone.
  Done when: five answered pairs change at least one weight in a stored file, and the next ranking of a fixture reflects that change and shows it.

- **Mine red CI history for recurring causes** — FEATURE — value 4 — effort M — risk med — category: flake / bug finder
  Why: `fm inbox gh` is manual and the flake finder only reruns locally. Failures that CI has already hit are evidence nobody has to guess at.
  Done when: given 20 recorded run logs where one test failed 4 times, the finder emits one finding whose proof reruns that test and cites the 4 run ids.

- **Audit commit messages against their diffs** — FEATURE — value 3 — effort M — risk low — category: bug finder
  Why: a commit that says "fix X" with no test touching X is a bug candidate, and git history is available in every never-seen repo.
  Done when: on a fixture with 3 "fix" commits, the one with no test or assertion change is flagged and the other two are not.

- **Wild: Draft upstream-ready bug reports for the user's dependencies** — FEATURE — value 3 — effort L — risk med — category: ecosystem
  Why: wild. Foreman already runs deps checks. A failing test against a pinned dependency at the version the user ships turns "unasked work" into something the user can hand upstream; nothing is sent without a "yes".
  Done when: a fixture with a known bug in a vendored lib yields a minimal stdlib-only repro and a draft issue file, and no network call is made.

- **Wild: Close the day with one change Foreman is proudest of** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. After ranking, the night shift picks its single best proven fix by the user's own survival data and writes two lines on why it chose that one. The user gets one thing to trust rather than a list.
  Done when: the morning card has one highlighted finding with a reason line that cites a ranking input.

- **Wild: Refuse to scan until a buy-in check passes on the user's own history** — SECURITY — value 3 — effort M — risk low — category: trust
  Why: wild. Before the first unasked scan in a project, replay the last 10 fixed bugs and check whether the finders would have found them. This reports a recall number the user sees before spending, and answers the leftover question of what an exam actually predicts.
  Done when: `fm find --rehearse` prints `recalled k/10` for a fixture history, and a scan proposal shows that figure beside its cost.

- **Say which finding classes Foreman cannot see in this repo** — FEATURE — value 4 — effort S — risk low — category: honest clean
  Why: a "clean" verdict on a stack with no runnable single-test command is misleading, and the exam's `none` kind rewards honest abstention. Listing blind classes next to "clean" makes the verdict worth trusting.
  Done when: a repo with no test runner returns "cannot prove here" with the reason, and a repo with a runner lists the probe kinds that ran and the ones skipped.

Next question: What does one proven finding cost end to end on each exam language, and at what cost does a user stop wanting the next one?
Next question: Which findings did the user accept but never merge, and what does that gap say about value that survival data can't?
