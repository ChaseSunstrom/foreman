# Brainstorm — lens: sci-fi: the 2030 harness that weighs every reading and approach, races candidates in parallel lanes and decides by evidence, worked back to what Python and Foreman can do today

- **Speculate while the user reads the plan** — FEATURE — value 4 — effort M — risk low — category: latency
  Why: the pack asks what intake can do in the first ten seconds after a vague goal. Assumption: those seconds are idle today.
  Done when: opening a plan starts a throwaway lane that runs the baseline suite, `fm graph blast` and `fm find`, and a following `fm task focus` reads their cached results and runs none of them again (test counts subprocess calls).

- **Score races on a Pareto card, not pass/fail** — FEATURE — value 4 — effort M — risk med — category: decision
  Why: T-2271 races the runner-up, but the only signal is "green". Assumption: ties and near-ties are common.
  Done when: `fm lane race` writes a scorecard per candidate (criteria passed, diff lines, blast-neighbour files touched, `--bench` median) and picks the non-dominated winner. A fixture with two green candidates picks the smaller, faster diff and records why.

- **Kill losing lanes early by successive halving** — PERFORMANCE — value 3 — effort M — risk low — category: cost
  Why: parallel lanes multiply token spend. Assumption: the cheapest check (lint, one test file) already separates most losers.
  Done when: a race runs checks cheapest-first, stops any lane that fails a rung, and a 3-lane test fixture finishes with fewer total check executions than a full run.

- **Surface candidate disagreement as the question to ask** — FEATURE — value 5 — effort L — risk med — category: ambiguity
  Why: the lens says to decide by evidence, and the pack's "stops for me only when irreversible and ambiguous" needs an ambiguity detector that isn't opinion.
  Done when: two passing candidates get the same generated inputs (stdlib `random`, seeded). Any differing output becomes one `fm ask` line quoting both outputs. A fixture with an under-specified rule produces exactly one question.

- **Ablate hunks to find unproven code** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: Foreman's promise is "proves its work". A green suite doesn't show which of a diff's hunks the criteria depend on.
  Done when: `fm task prove --ablate` reverts each hunk in turn (`git apply -R`), reruns the verify command, and lists the hunks whose removal leaves it green. A fixture with one decorative hunk lists exactly that hunk.

- **Add a placebo arm to every race** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: a verify command that passes an empty or plausible-but-wrong change can't pick a winner. The pack's rule that signals must not be authored by Foreman supports an external control. Assumption: some done-when commands are non-discriminating.
  Done when: a race also runs an empty-diff candidate and a mutated copy of the winner. If either is green, the card prints "verify can't discriminate" and the win is marked typed-evidence.

- **Keep losers as ghost branches** — FEATURE — value 3 — effort S — risk low — category: recovery
  Why: assumption: when a chosen approach is reverted or re-fixed, the runner-up is the cheapest restart. Today lane diffs vanish at `fm lane rm`.
  Done when: `fm lane rm` saves each losing diff as a patch under `refs/fm/ghost/T-NNNN/` and `fm task reopen` lists them. Applying one to a fresh tree succeeds in a test.

- **Answer "why is this code like this?" with `fm why FILE:LINE`** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: Approach sections, race results and auto-decisions are recorded but scattered. Nothing maps a line back to the options rejected for it.
  Done when: `fm why plugin/lib/fmcore.py:120` finds the commit via blame, its task, and prints the chosen approach, the rejected options and the winning evidence. It prints "no recorded decision" otherwise.

- **Reconcile baton, ledger and repo by one rule** — FIX — value 4 — effort M — risk med — category: reliability
  Why: this answers the left question about disagreement after a kill. Assumption: the user never sees the disagreement today.
  Done when: `fm reconcile` ranks repo over ledger over baton and prints each mismatch (for example "baton says T-2301 open; commit abc closes it"). It repairs the lower-ranked source, and a killed-mid-close fixture ends consistent.

- **Audit every verb for a writer and judge with no user-owned check between** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: directly answers the first left question. The cold-read, exam and prediction verbs all have a model on both sides.
  Done when: `fm doctor` prints a table of verb → writer → judge → deterministic or user check between them. Any row with none is a named warning, and a test fails if a new verb is missing from the table.

- **Recompute shown numbers with an independent script** — SECURITY — value 4 — effort M — risk low — category: trust
  Why: answers the left question about numbers no other code has checked. The daily site stats refresh (T-2326) and the held-rate and prediction scores are quoted from the code that produced them.
  Done when: a separate stdlib script recomputes the site stats and the per-tier calibration straight from `events.jsonl`. `fm doctor` fails on any mismatch, and a corrupted-counter fixture trips it.

- **Wild: Read the captain's log aloud, locally** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Every auto-decision already gets a one-line receipt. Joined into a terse dated log for the day and spoken through a local TTS, it works as a hands-free "what happened overnight".
  Done when: `fm log --say` prints the day's decisions in order, and pipes them to `espeak-ng` or similar if present. It prints text only when absent.

- **Wild: Photo finish replay in the web UI** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: wild. A race is unattended and invisible afterwards. Lanes drawn as tracks with check ticks, a halving cut-off and the winner's scorecard turn "chosen by evidence" into something the user can show others.
  Done when: the web UI's task page replays a stored race from `events.jsonl`, with a play/pause control and a reduced-motion fallback of a static table.

- **Wild: Run lanes on reflink clones** — PERFORMANCE — value 3 — effort S — risk med — category: lanes
  Why: wild-leaning. Lanes at `fm lane max` 6 need six working trees. `cp --reflink=auto` makes a lane start in milliseconds and cost almost no disk on btrfs/xfs, with a git-worktree fallback elsewhere.
  Done when: lane creation uses reflink when the filesystem supports it. A benchmark shows creating 6 lanes of a 2000-file tree takes less than half the current time on that filesystem, and the fallback test passes on ext4.

- **Wild: Cache verify results by tree hash** — PERFORMANCE — value 3 — effort M — risk med — category: speed
  Why: racing lanes and the stuck ladder rerun identical commands on identical trees. Assumption: many repeats exist across candidates and hypothesis rows.
  Done when: a verify command's result is keyed by (tree hash, command, toolchain fingerprint) and replayed on a repeat. A test shows the second identical run spawns no subprocess, and a changed file invalidates it.

Next question: Which Foreman decisions are currently scored only by the model that made them, and what is the cheapest external signal for each?
Next question: When two lanes both pass, what does the user actually look at to trust the winner, and is the scorecard what they would reach for?
