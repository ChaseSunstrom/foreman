# Brainstorm — lens: approaches

- **Run a no-network lane smoke on a stub model** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: Pack says the user wants discipline to work for weak/small local models, yet nothing shows the scripted tour run against one; the user is AFK so regressions go unseen. Approach: a canned-response stub `claude` replays recorded turns through hooks, drive and close. Cheaper than a real small model, and deterministic.
  Done when: `fm smoke --stub` runs the tour end to end with the stub on PATH, exits 0, and fails if any stage rail step is skipped.

- **Add a verb-alias table fed by the unknown-command ledger** — FIX — value 4 — effort S — risk low — category: developer experience
  Why: "Builders and weak agents guess command names that don't exist (`fm task list`)"; the nearest-match message exists but the guess could just work. Approach: alias only guesses seen at least 3 times in logs, with a quiet "(ran `fm task ls`)" note; do less than a fuzzy matcher.
  Done when: a test seeding the unknown-command log with `task list` three times makes `fm task list` run `fm task ls` and print the note.

- **Make bare `fm` resolve to the lane's own checkout** — FIX — value 4 — effort S — risk med — category: lanes
  Why: "Builders in a lane can't run their own new `fm` flags: bare `fm` resolves to the main checkout's copy." Approach: put a lane-local shim dir first on PATH at lane creation, rather than teaching builders `python3 plugin/bin/fm`.
  Done when: in a lane worktree with a new flag added, `fm --newflag` runs the lane's code and `which fm` points inside the worktree.

- **Auto-record reviewer findings at reviewer stop** — FEATURE — value 5 — effort M — risk med — category: learning
  Why: "recording them is manual (`fm task finding`, one call per finding)… the feed starves." Approach options: parse structured output in SubagentStop (cheapest, deterministic) versus a Haiku extractor (more tolerant). Pick the parser with a Haiku fallback only on parse failure.
  Done when: a fixture reviewer result with three findings creates three finding records, and a malformed result creates one flagged "unparsed" record.

- **Put the refused command and replay verdict in the friction digest** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: "Grounding guard friction took a hand-written transcript miner… twice a premise turned out false only after mining." Approach: log the full command at refusal time instead of mining transcripts afterward; the digest then runs `fm guard try` on each.
  Done when: after two refusals, the digest lists both commands with their current verdicts and flags any that now allow.

- **Collapse the release ritual into one resumable `fm release`** — FEATURE — value 4 — effort M — risk med — category: release
  Why: "Releases are a manual 8-step ritual" and T-1173 is "Release 1.2.33" active. Approach: a checkpointed step list stored on disk, so a failure at gates resumes at that step, with push left behind the existing approval.
  Done when: a test with a fake failing gate stops at step 4, and a rerun after the fix resumes at step 4 and stops before push awaiting approval.

- **Let the autonomous drive invoke review and ideas as headless verbs** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: "/foreman:review and /foreman:ideas can only run when the user types them; the autonomous drive can't use them." Approach: the workflows become thin wrappers over `fm review` and `fm ideas`, which the drive calls under `fm contract` limits.
  Done when: a drive test with a stubbed child calls the review verb after a lane merge and records its findings with no user prompt.

- **Drop the guard's "it could be" guess unless the path exists** — FIX — value 2 — effort S — risk low — category: guard
  Why: the guess shows paths like /repo/cd/w.out. Do-less approach: stat the candidate and omit the line when absent, rather than a smarter resolver.
  Done when: a refusal on `cd w; cat > w.out` prints no guess line for a nonexistent /repo/cd/w.out.

- **Give deferred briefs a recheck trigger that expires them** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: 11 deferred briefs "still wait on external evidence or Claude Code features" and 37 accumulated before the triage. Approach: each carries a `recheck:` date or condition; `fm night` re-evaluates and drops or promotes it.
  Done when: a fixture brief with a past recheck date is listed as "due" by `fm next` and removed from the mission pack.

- **Measure builder self-review and defect-class feed against review rounds** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: "builder self-review (T-1147) and defect classes (T-1164) are new and unmeasured"; every branch needed 2–6 defects of review. Approach: record defects per lane before and after, shown in `fm lane list`.
  Done when: after two closed lanes with seeded findings, `fm stats lanes` prints mean review defects per lane split by whether the brief carried defect classes.

- **Wild: Replay every past confirmed review finding against each new lane diff** — FEATURE — value 4 — effort L — risk med — category: review
  Why: wild; assumption: findings are stored with enough shape (file pattern, defect class) to become cheap regex or AST checks, so the same hot-path-cost or lock-reentry bug cannot ship twice.
  Done when: a diff reintroducing a stored lock-reentry pattern is flagged by `fm lane merge` before review starts.

- **Wild: Mode where a skeptic child tries to break the last release overnight** — FEATURE — value 3 — effort L — risk med — category: autonomy
  Why: wild; the AFK user gets no adversary after the release ritual. Approach: `fm night` runs a read-only attacker over the new release's diff, capturing FIX briefs only for reproduced failures.
  Done when: a seeded bug in a fixture release is reproduced and captured as a FIX task by the night run.

- **Wild: A tick-box "what only you can do" page that executes the ticks** — FEATURE — value 4 — effort M — risk med — category: web UI
  Why: wild; extends `fm todo` and the pack's "final report" pillar. The web UI lists each user-only item with its command, and a tick queues it or marks it resolved.
  Done when: ticking an item in the page removes it from `fm todo` and runs or records the resolution once.
