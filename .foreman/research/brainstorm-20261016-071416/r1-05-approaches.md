# Brainstorm — lens: approaches

- **Give each lane its own `fm` on PATH** — FIX — value 5 — effort S — risk low — category: builders
  Why: the review notes say bare `fm` in a lane resolves to the main checkout's copy, so builders can't run their own new flags. Alternatives are "tell briefs to use `python3 plugin/bin/fm`" (cheap, but relies on the agent obeying) or a worktree-local shim that execs that worktree's `plugin/bin/fm`. The shim is mechanical, in line with the user's "enforce mechanically" ask.
  Done when: a test creates a lane worktree whose `fm` has an extra flag, runs bare `fm --flag` there, and sees that flag work. The same flag fails in the main checkout.

- **Record reviewer findings from the reviewer's own output** — FEATURE — value 5 — effort M — risk med — category: review loop
  Why: findings feed builder briefs, but recording is one manual `fm task finding` per finding, so the feed starves. Options: a prompt reminder (weak), a required findings block parsed at SubagentStop (chosen), or a post-hoc transcript scan. Trade-off: a parser can misfire on prose, so it only accepts a fenced block with a fixed header.
  Done when: a fake reviewer result with two fenced findings creates two finding records without any manual call. Prose with no block creates none.

- **Show refused commands in the friction digest, replayed through the guard** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: the friction digest counts refusals but never shows the commands. Two premises were found false only after hand-mining (data-only cat writes, literal variables). Approach: store the full command per refusal and have the digest print each with its current `fm guard try` verdict, so false premises show up before a task is written.
  Done when: a test seeds two refusals and the digest prints both commands, each with a verdict. One refusal that now passes is marked "now allowed".

- **Let the common guessed verbs just work** — FEATURE — value 4 — effort S — risk low — category: CLI ergonomics
  Why: builders and weak agents guess `fm task list`, and the nearest-match suggestion only prints. Approach: an alias table seeded from the unknown-command ledger. A unique read-only match runs with a one-line "ran `fm tasks`" note. Mutating guesses still only suggest.
  Done when: `fm task list` prints the task list plus the note, and `fm task close-everything` runs nothing and prints suggestions.

- **Make the drive able to run review and ideas headless** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: /foreman:review and /foreman:ideas run only when the user types them, so the unattended drive can't use them. Options: let the drive spawn the existing `fm ideas` and a new `fm review` child (chosen), or wait for Claude Code to expose slash commands to hooks (blocked on external work). Trade-off: this adds spend, so it is bounded by `fm contract`.
  Done when: with a fake child, a drained queue under a contract triggers one review run and one ideas run, and both appear in the contract receipt.

- **Fix the guard's "it could be …" path guess** — FIX — value 3 — effort S — risk low — category: guard
  Why: the guess glues a command word onto the path (e.g. `/repo/cd/w.out`). Options: drop the guess when it isn't an existing path (least risk), or resolve it against the real cwd after `cd` (more helpful, more code).
  Done when: a test with `cd w && cat x > w.out` yields a suggestion that names no path containing `/cd/`.

- **Count review rounds per lane and show them** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: every builder branch needed 2–6 real defects fixed, and the new self-review (T-1147) and defect classes (T-1164) are "unmeasured". Approach: log defects found per merged lane with a flag for whether self-review ran, show the count in `fm lane list`, and compare averages with `fm lane stats`. This is cheaper than a full A/B.
  Done when: a test merges two lanes with 3 and 1 recorded defects and `fm lane stats` prints the average of 2 and splits it by self-review on and off.

- **Report which shipped verbs the unattended drive can reach** — CLEAN — value 3 — effort M — risk low — category: dead capability
  Why: the new workflows are user-typed only, and 11 deferred briefs wait on outside evidence. Approach: statically list every verb that no drive, hook or `fm next` path can invoke. Each one is either wired, labelled "human-only", or queued for deletion.
  Done when: the report on a fixture marks one verb with no autonomous caller as "human-only" and exits non-zero when one is unlabelled.

- **Write a three-line round retro that seeds the next pack** — FEATURE — value 3 — effort S — risk low — category: loop
  Why: round 4 had to rebuild context by hand ("review what shipped since round 2"). Approach: at round end, save kept, regretted and next lines (from closes, reverts and drops) and put them at the top of the next pack. The alternative is to rely on the ledger alone, which costs more tokens each round.
  Done when: finishing a round writes `retro.md`, and the next `fm ideas` pack begins with its three lines.

- **Wild: Pick the next lens by neglect, not by list** — FEATURE — value 2 — effort S — risk low — category: brainstorm
  Why: assumption: some lenses keep returning the same ideas while thin areas (devices, docs, privacy) stay thin. Roll weighted dice where weight rises with how long it's been since a lens produced a built idea. T-0829 handles dry lenses, but this also boosts neglected ones.
  Done when: with a seeded RNG and a history where one lens is long neglected, that lens is chosen at least 3 times in 10 draws.

- **Wild: Run the scripted tour on a small local model and map where it derails** — FEATURE — value 4 — effort L — risk med — category: weak-model support
  Why: the user wants Foreman to work for weak or small local models, yet nothing runs one. Approach: drive `fm demo` through a local Ollama model, log the first failed step per verb, and publish a "derail map" as tasks. Trade-off: slow and flaky, so it is a nightly job only. Assumption: a local runtime is installed.
  Done when: with a fake local model that fails on one step, the run emits a derail map naming that step and captures one task.

- **Wild: Publish a daily "what Foreman refused and why" page for the user to skim** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the user is AFK and wants no mid-run questions. Approach: render one static HTML page of the day's refusals, each with the command, reason and one-click "wrong, should allow" copy line (`fm guard wrong`). This turns the guard's labelled cases into a daily glance rather than a verb the user has to remember.
  Done when: a seeded ledger with three refusals produces a page listing three rows, each with a `fm guard wrong` command.

- **Do less: freeze round 4 to deletions and wiring only** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: three rounds added many verbs, and the user's "improve past everything shipped" may be best served by making what exists reachable and cheap. Trade-off: it produces fewer new capabilities, but each fix lands on something already shipped.
  Done when: the round's closed tasks have no net new verbs. The reachability report shows no unlabelled unreachable verbs.
