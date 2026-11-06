# Brainstorm — lens: reliability

- **Add a no-model deliberation floor** — FEATURE — value 4 — effort M — risk low — category: resilience
  Why: assumption: every deliberation stage today (readings, race, rival, cold read) needs a child, and no earlier idea says what happens when none can run (usage limit, logged-out auth, offline). A deterministic checklist (readings from the request's verbs, `fm graph blast`, tier from the diff) would fire instead, labelled "floor depth" on the receipt.
  Done when: with children stubbed to fail, `fm plan` on an M task still emits a plan whose receipt says `depth=floor`, and the gate accepts it only up to tier S/M.

- **Version the plan, readings and race files** — FIX — value 4 — effort S — risk low — category: schema
  Why: assumption: plan and decision files outlive the library that wrote them, and a newer gate reading an older plan would misjudge it. A schema field plus an "unreadable → refuse and say why" rule avoids that; the trigger table got the same idea, the plan files didn't.
  Done when: a test feeds the gate a plan with `schema: 0` and a future `schema: 99`. Both are refused with the named reason, and neither is treated as a pass.

- **Normalise text before the distinct-options check** — FIX — value 3 — effort S — risk low — category: gate
  Why: the pack lists paraphrase and "one idea in three costumes" checks, but nothing about invisible differences. Zero-width characters, case, CRLF or homoglyphs can make two identical options pass as distinct. assumption: the check compares raw strings.
  Done when: a plan with options "Use cache" and "Use cache" (second with a zero-width space) fails the distinct-options gate.

- **Measure cold-read self-consistency per cell** — FEATURE — value 4 — effort M — risk low — category: cold reads
  Why: the rule is Haiku first, then Sonnet decides, but nothing measures whether the same reader gives the same verdict twice on the same cell. A flaky judge makes "counted" cells unstable. Run each read twice and record the disagreement rate. A split verdict counts as "unread", not pass.
  Done when: `fm genesis` coverage output shows a per-batch disagreement rate, and a cell with split verdicts is not counted.

- **Rehydrate the plan after compaction and hash-check it** — FIX — value 5 — effort M — risk med — category: continuity
  Why: assumption: a long L deliberation spans a context compaction, and readings, options and the chosen approach exist only in the summary. The files are the truth: after compaction, SessionStart re-injects the plan's hash and a delta, and a mismatch halts edits.
  Done when: a test simulates compaction mid-plan; the next tool call sees the plan hash, and an edited-since-hash plan blocks edits until re-accepted.

- **Run every cell probe hermetically and three times** — FEATURE — value 4 — effort M — risk low — category: probes
  Why: the earlier ideas include "fill each cell from a probe" and "rot detector", but not whether a probe is itself deterministic. Fixed locale, TZ, HOME, no network, and three runs. A probe that differs between runs is marked flaky and the cell stays uncounted.
  Done when: a planted probe that reads the clock is reported flaky and its cell is not counted.

- **Sweep orphaned deliberation children and their tmp dirs at session start** — CLEAN — value 3 — effort S — risk low — category: hygiene
  Why: the working dir is `/run/user/1000/fm-children-1000` (tmpfs), and children killed by the OS, logout or a usage limit leave directories and processes behind. A start-of-session reap by pid-file and age, listing what it removed in one line, handles them.
  Done when: a fake child dir with a dead pid is removed at the next session start and logged, and a live one is left alone.

- **Record a provenance stamp for every deliberation stage** — FEATURE — value 3 — effort S — risk low — category: replay
  Why: assumption: the existing model-mismatch idea checks one run, but no record exists to replay a stage later. Store model id, prompt hash and input hash per stage, so "this plan can't be reproduced because the prompt changed" is detectable.
  Done when: `fm plan show --prov` prints a hash per stage, and changing a prompt template flags old plans as "prompt drifted".

- **Wild: Hold a power-cut hour for deliberation** — FEATURE — value 3 — effort M — risk low — category: chaos — wild
  Why: assumption: crashes at write boundaries were covered, but not their combination. Once an hour in the idle window, a scratch copy runs a full plan with a random mix of SIGKILL, ENOSPC and a frozen clock. It then asserts that resume yields either the same plan or a clean refusal.
  Done when: the night tick logs a pass/fail line for the drill, and an injected non-atomic write makes it fail.

- **Wild: Add a canary plan with a known-wrong obvious answer** — FEATURE — value 4 — effort M — risk low — category: liveness — wild
  Why: the "weekly planted forbidden command" idea proves the guard is alive. The same holds for deliberation: a fixed trap task whose first-instinct fix is wrong, run weekly. If the pipeline returns the trap answer, deliberation has silently degraded.
  Done when: a doctor row shows the canary's last result, and stubbing the race to always pick candidate A turns it red.

- **Wild: Compare two kill-switch outcomes on the same plan** — FEATURE — value 2 — effort L — risk med — category: determinism — wild
  Why: assumption: run the plan gate twice with a different seed or order of options; if the verdict changes, the gate is order-dependent. Do this as a nightly metamorphic pair on the last 10 closed plans.
  Done when: swapping option order on a stored plan leaves the verdict unchanged, and a planted order-dependent check is caught.

- **Give a stalled child a heartbeat deadline, not only a wall clock** — PERFORMANCE — value 3 — effort S — risk low — category: timeouts
  Why: assumption: a hung brainstorm or cold-read child blocks a stage until the wall limit. If no stdout byte arrives in N seconds, kill it, record "stalled", and retry once on the next tier.
  Done when: a stub child that sleeps silently is killed within the heartbeat window and the retry is logged.

- **Make a failed stage visible in the finish receipt** — FIX — value 4 — effort S — risk low — category: honesty
  Why: assumption: with fallbacks (floor depth, skipped rival, stalled child) a plan can look complete. The receipt should say "ran 3 of 5 stages; skipped: rival (stalled)", so a thin deliberation never reads as a full one.
  Done when: `fm task finish` output lists skipped or degraded stages, and a run with a killed rival shows it by name.

Next question: Which deliberation stages can succeed with an empty or truncated child output and still be recorded as "done"?
Next question: When two sessions deliberate on neighbouring tasks, which shared files (decisions.md, coverage.md, the idea catalog) do they both write, and what does the loser see?
