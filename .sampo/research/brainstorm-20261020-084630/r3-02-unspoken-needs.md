# Brainstorm — lens: unspoken needs

- **Prove the guard fires inside forked and background subagents** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: the pack says fork subagents are now on by default in `claude -p`, and the safety claim (20 of 24 stopped) was measured on the main thread. Assumption: no existing test covers a dangerous Bash call made by a forked or background subagent.
  Done when: a roundtrip test has a forked subagent attempt one of the 24 corpus commands under bypass mode and the guard refuses it with the same verdict as on the main thread.

- **Silence Foreman's injections in read-only forked subagents** — PERFORMANCE — value 4 — effort S — risk low — category: cost
  Why: the long-session premium (~60%, $0.095 vs $0.059) comes from hook notes and bookkeeping that make context grow faster. Assumption: forks and scouts inherit those notes although they only read.
  Done when: a scout subagent that makes no edits receives zero Foreman hook-note bytes, and the long-session benchmark's per-run injected bytes drop with passes unchanged.

- **Alarm when Foreman's hook registration changes outside Foreman** — SECURITY — value 4 — effort S — risk low — category: tamper
  Why: the guard only protects while the hooks are registered, and bypass mode is how Foreman runs. Assumption: nothing currently notices another tool or a typo removing or reordering the entries in settings.
  Done when: deleting Foreman's PreToolUse entry from the settings file makes the next `fm` call or SessionStart print a one-line warning naming the missing hook, and a test covers it.

- **Make ceremony depend on the active model** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: the user wants it cheaper and "with latest claude code", and the Claude 5.5 family is newer than the Haiku/Sonnet runs the numbers come from. Assumption: stronger models need fewer reminders, and the hook payload exposes the model ID.
  Done when: a table keyed by model ID sets which notes are injected, and a duel on the strongest model shows lower Foreman overhead than the default with the same hidden-test pass rate.

- **Power-check a claim before spending on it** — FEATURE — value 3 — effort M — risk low — category: benchmarks
  Why: the long-session result is 6 of 6 vs 3 of 6, and the cost deltas are +10%/+14% on 3 runs. The user insists every claim is measured, and usage is scarce.
  Done when: `fm bench plan <case> --effect 10%` prints the runs needed given recorded variance and its dollar cost, and says "can't be shown at this budget" when that exceeds the cap.

- **Greet the first session on a new Claude Code version with a self-check** — FEATURE — value 3 — effort S — risk low — category: compatibility
  Why: Foreman was last adapted to 2.1.301 while 2.1.304 is out, and the changes in between touch compaction, Stop and `tool.check`. Assumption: users learn of drift only when something breaks.
  Done when: the first SessionStart under a version not in the verified list runs hook, pane-anchor and settings checks in under 3 seconds and prints one line saying what passed, and it stays silent afterwards.

- **Grey out site claims measured on an older Claude Code** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: the page's figures were measured on specific versions and models, and T-1246 notes the prose is hard-coded. A newer Claude Code makes them stale without anyone noticing.
  Done when: each figure on the Benchmarks page carries its Claude Code version, and the build marks it "measured on 2.1.301" in a muted style once a newer version is recorded.

- **Check the user's own CLAUDE.md and settings against Foreman's rules** — FEATURE — value 3 — effort S — risk low — category: doctor
  Why: assumption: users who already have a long global CLAUDE.md give instructions that conflict with plan-first or one-task-at-a-time, and the model resolves it unpredictably.
  Done when: `fm doctor` flags a line in user or project CLAUDE.md that contradicts a named Foreman rule (for example "never make a plan") and prints the file and line.

- **Lower reasoning effort on pure-bookkeeping turns** — PERFORMANCE — value 3 — effort M — risk med — category: cost
  Why: the pack attributes Foreman's premium to bookkeeping calls. Assumption: effort can be set per turn or per subagent, and these turns need little reasoning.
  Done when: bookkeeping-only turns run at a lower effort setting, output tokens per closed task fall by a measured amount, and the pass rate is unchanged on the spec suite.

- **Budget the repository's media weight** — CLEAN — value 2 — effort S — risk low — category: hygiene
  Why: the repo has 1,560 files and ships demo/live.svg and live.mp4, and every regenerated recording adds permanent history. Assumption: no size check exists.
  Done when: CI fails when tracked media exceeds a stated budget, and `fm doctor` prints the current total.

- **Wild: Paired-seed duel from a recorded shared prefix** — FEATURE — value 4 — effort L — risk med — category: benchmarks
  Why: wild. Both sides start each case from the same recorded first turns, so the point where they diverge is the only difference, which cuts run-to-run noise and the number of runs needed. Assumption: the prefix can be replayed deterministically through a cassette shim.
  Done when: running a case twice with the same prefix yields lower outcome variance than independent runs, and the report shows the turn where the two sides first differed.

- **Wild: Turn each marathon compaction into a diary entry** — FEATURE — value 3 — effort M — risk low — category: showcase
  Why: wild. The marathon found and fixed 3 things through 7 compactions, but the user can only see the end state. A short per-compaction entry (what was chosen, why, what was left) would make that story readable on the page.
  Done when: a marathon run writes one entry per forced compaction from the ledger with no extra model call, and the Benchmarks page renders them as a timeline.

- **Wild: A "break this claim" button on every benchmark row** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. The user wants every claim measured, so each row can invite attack: a link that opens a prefilled GitHub issue with the exact `fm bench` command, model, version and result hash to rerun.
  Done when: each row on the Benchmarks page has a link whose issue body contains a command that reproduces that row's configuration, and a test checks the link for every row.

- **Wild: Measure Foreman's idle footprint when no session is open** — PERFORMANCE — value 2 — effort S — risk low — category: footprint
  Why: wild-ish, and an assumption: the pane, web UI and watchers may keep polling after the session ends, which matters on a laptop and in a "without burning usage" project.
  Done when: a test starts and stops a session and asserts zero Foreman processes remain and CPU use over 30 seconds stays under a stated limit.
