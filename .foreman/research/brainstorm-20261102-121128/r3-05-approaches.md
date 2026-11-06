# Brainstorm — lens: approaches

Lens: approaches. The pack asks how to spend an idle account. Each idea below is a different way to turn idle usage into something measurable or built.

- **Run a public benchmark slice as the outside referee** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the steer says weakness-finding must use signals Foreman didn't author, yet every exam scenario is still in-house. A pinned slice of a public suite (SWE-bench Verified, Terminal-Bench) run through `fm code`, Claude, and plain gives a score nobody at Foreman wrote. It costs the most tokens, but that is what idle usage is for. Assumption: the suite's tasks run in a sandbox the host allows.
  Done when: `fm exam public --slice 20` prints foreman-vs-plain pass counts with the suite's own grader output linked.

- **Race three framings of an L task, keep the proven smallest** — FEATURE — value 5 — effort M — risk med — category: agents
  Why: T-1207, T-0034, and T-0035 are large, long-deferred tasks, and the standing rule says a failed spike gets 2+ different approaches. A tournament starts N worktree lanes with different briefs (reuse a tool, minimal, full rewrite). It keeps the one whose proof commands pass with the smallest diff. This differs from "same ask on two models": the models are the same and the framings differ. Trade-off: N× the tokens for one task.
  Done when: `fm try T-xxxx --ways 3` leaves one landed branch and a table of the losers' proof results and diff sizes.

- **Spike deferred tasks under a cap to learn their real effort** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: 30+ "Later from T-xxxx" tasks are marked M with no evidence behind the size. A capped, discarded spike per task (worktree, ~$0.50) records files touched, blockers hit, and whether the first test went green. Each task is then re-sized from observation, not guesswork. Assumption: the effort labels are guesses.
  Done when: after a spike run, each deferred task carries a `spike:` line with observed files, minutes, and a keep, split, or drop verdict.

- **Keep a warm hook daemon instead of cold Python starts** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: `bench_hooks.py` and a gate on median hook wall time exist, and T-0832 only plans a shell prefilter. A persistent process on a unix socket, with a shim that falls back to the cold path when it is down, removes interpreter startup from every tool call. The guard must still fail closed.
  Done when: `bench_hooks.py --runs 20` shows PreToolUse median at least 3× lower with the daemon, and killing the daemon changes no verdict.

- **Make doctor repair its own warnings** — FEATURE — value 3 — effort S — risk med — category: developer experience
  Why: `fm doctor` names many WARNs (timers, a missing steer check, stale install). A `--fix` that applies only each WARN's one safe, reversible repair, and prints the diff of state, turns diagnosis into action. Trade-off: each repair is code to maintain, so start with three.
  Done when: planting a missing steer check and a dead timer, then running `fm doctor --fix`, clears both, and a second run reports nothing to fix.

- **Generate shell completion and did-you-mean from the verb table** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: there are dozens of verbs and flags (`fm genesis`, `fm exam`, `fm night`), and the removed `--print-timer` flag shows people typing stale ones. One generated completion file for bash, zsh, and fish, plus a nearest-verb suggestion on unknown input, costs almost nothing. Assumption: no completion exists, since none appears in the pack.
  Done when: `fm completion zsh` installs and completes `fm exam r<TAB>` to `run`/`runs`, and `fm exm` prints "did you mean exam".

- **Replay the ledgers under other ceremony profiles with zero tokens** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: T-1266 wants a ceremony profile per task kind, chosen from duel data, and the recorded tasks already hold cost, steps, and held-or-reversed outcomes. Counterfactual replay estimates what a leaner profile would have cost and what it would have skipped, without a model call. Trade-off: it cannot show a task that would have failed.
  Done when: `fm profile whatif lean` prints, per task kind, the cost saved and the count of past proofs that profile would have dropped.

- **Add an adaptive-difficulty exam so plain stays near 50%** — FEATURE — value 4 — effort M — risk med — category: measurement
  Why: the steers note that exam items have no versioning and the BEYOND set can't change without breaking comparability. If plain passes almost everything, Foreman's delta is invisible. A tool-less child writes scenarios, a blind solver tries them, and a ladder keeps the plain arm's pass rate in a 35–65% band using stable versioned ids. Assumption: current plain pass rates are saturated, which the pack doesn't state.
  Done when: `fm exam ladder` reports each item's version and the plain-arm pass rate in the band, with old runs still comparable by id.

- **Measure cold-read agreement between Haiku and Sonnet** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: the rule is that Haiku reads first and Sonnet decides on any non-pass. If they agree 95% of the time on non-passes, the Haiku stage is only filtering. If they disagree often, Haiku is noise. The `fm outcomes` ledger already holds the paired verdicts.
  Done when: `fm outcomes --coldreads` prints agreement, Haiku false-pass count, and Sonnet-overturn count with a sample size.

- **Wild: A/B the user's own queue by randomizing ceremony per task** — FEATURE — value 4 — effort M — risk med — category: self-experiment — wild
  Why: synthetic duels measure the exam, not this user's work. Randomly giving each real task the full or lean profile (disclosed, never hidden) and recording held-rate, cost, and rework gives evidence from the user's own repos. Trade-off: some tasks get less ceremony on purpose.
  Done when: after 30 closed tasks, `fm profile ab` reports held-rate and cost per arm with a confidence note, and the user can turn it off with one command.

- **Wild: Adopt-an-issue, spending idle quota on local draft PRs** — FEATURE — value 3 — effort L — risk high — category: agents — wild
  Why: idle quota expires unused. Drafting fixes for small labelled issues in repos the user cares about, kept as local branches and never pushed, turns waste into a ready-to-review shelf. Needs a hard rule that nothing leaves the machine without the user. Assumption: the user wants this at all.
  Done when: `fm shelf` lists 3 local draft branches with proof receipts, and a network capture shows nothing was pushed.

- **Wild: Let the proof ask a stranger model to break it first** — FEATURE — value 4 — effort M — risk low — category: verification — wild
  Why: the steers want weakness-finding by a different model, but only cold reads exist at filing time. Before `fm task finish`, a different-vendor agent (Codex or Gemini through the adapters) gets only the diff and the proof command and writes one input that should make the proof fail. If it finds one, the finish is refused and the input becomes a regression test. Blocked in part by T-0336, which is unverified on live codex and gemini.
  Done when: finishing a task with a planted weak proof is refused with the breaking input, and a normal task finishes unchanged.

- **Wild: Run a nightly dream pass that re-derives one old fix cold** — FEATURE — value 3 — effort M — risk low — category: measurement — wild
  Why: a random closed task is re-attempted from its original ask on the current repo, blind to the old diff. The comparison shows whether the proof would still catch the same bug today and whether the codebase has drifted. A mismatch files a task.
  Done when: `fm night` logs one dream result per run with the old and new diff overlap and either "proof still holds" or a filed task id.

Next question: Which of Foreman's own scores would stay the same if the model were replaced by a random-answer stub, and what exam would expose that?
Next question: What is the smallest set of record classes that must survive a restore for the user to resume work, and has anyone ever tried the restore?
