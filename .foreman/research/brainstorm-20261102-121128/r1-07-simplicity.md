# Brainstorm — lens: simplicity

**Simplicity lens.** Each idea below removes, merges or hides something. Foreman's growth is the evidence: 1388 skill files, about 30 standing rules and 30+ deferred "Later from" items. T-0794 (Slim Foreman) and T-2503 (lean substance) already point this way.

- **Ship Lite mode: guard, plan, prove only** — FEATURE — value 5 — effort M — risk low — category: slimming
  Why: T-0794 is deferred, and the guard-only exam arm (T-2534) already exists to measure what the rest adds. Install.sh and `fm doctor` also must work with no claude on PATH.
  Done when: `fm install --lite` loads only the guard, the plan gate and `fm task prove`, and the hook p95 and injected chars are both lower than the full install in `bench_hooks.py`.

- **Turn ablation results into removal tasks** — CLEAN — value 5 — effort M — risk med — category: subtraction
  Why: T-2536 captures one candidate per feature whose "off" arm changed no pass and cost no more, and T-2503 holds back growth that has no measurement. Nothing yet deletes a feature once the evidence is in.
  Done when: a feature with a no-delta ablation gets a removal task, and closing it lowers the lean ratchet's rule, description and SKILL-size counts.

- **Fold the 30+ deferred "Later from" tasks into a few catalog files** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: T-0788 through T-0869 are deferred, each aggregating dozens of ideas. The "no idea killed" steer forbids deleting them, but it allows moving them to not-yet.md with the blocker recorded.
  Done when: `fm next` and the open-work list show at most 10 deferred items, and each moved idea keeps its blocker line in not-yet.md.

- **Collapse the steers into a superseding rule set** — CLEAN — value 4 — effort M — risk med — category: rules
  Why: the cold-read rule, the testing cadence, the exam-deferral rule and the long-horizon pause overlap and refine each other. Every steer must also carry an automatic check (`fm decide --check`), so overlaps multiply the checks.
  Done when: `fm decide --supersede OLD NEW` exists, the active rule list shows no two rules covering the same check, and `fm doctor` names any that do.

- **Give every receipt exactly three states: proven, unproven, overridden** — FIX — value 4 — effort S — risk low — category: receipts
  Why: this answers two earlier questions. A UI check that can't run (no display, no browser) must not read as a pass, and a hand override must not read as proof.
  Done when: a finish with a skipped UI check prints "unproven: no display", and an override prints "overridden by user, not proof" and counts as neither a pass nor a fail in `fm outcomes`.

- **Cap Foreman-filed inbox items at 5 in `fm next`** — CLEAN — value 3 — effort S — risk low — category: inbox
  Why: ci, self and discovered items are held back by the round-first rule. When released they could flood the queue. The T-2624 note about pasted credentials and settled asks shows noise already reaches the inbox.
  Done when: with 20 filed items, `fm next` shows 5 ranked by need and one "+15 more" line.

- **Hide verbs the user hasn't used in 30 days from `fm help`** — CLEAN — value 3 — effort S — risk low — category: help
  Why: assumption: the verb count is large, and the lean ratchet already tracks it. The user removed `--print-timer` on purpose, which suggests they prefer small surfaces.
  Done when: `fm help` lists at most 15 verbs by recent local use, and `fm help --all` lists the rest.

- **Close or tier the long-blocked adapter tasks (T-0335, T-0336, T-0337)** — CLEAN — value 3 — effort S — risk low — category: adapters
  Why: these are blocked on live verification of Codex, Gemini and opencode. The steer that Foreman isn't Claude-specific stays in force, so the tiers must be stated, not dropped.
  Done when: each adapter is marked "verified" or "best-effort" in `fm doctor`, and the blocked tasks move to not-yet.md with their blocker.

- **Merge Foreman's ledgers into one append-only record with a class field** — CLEAN — value 3 — effort L — risk high — category: ledgers
  Why: bets, outcomes, friction and decisions each have their own reader. The earlier question about a reader returning a wrong answer when a record class is missing is easier to check against one file.
  Done when: one reader verifies every record class is present, and removing a class makes `fm doctor` fail rather than return quiet zeros.

- **Wild: `fm eject` leaves a standalone guard and removes Foreman** — FEATURE — value 3 — effort M — risk low — category: exit
  Why: wild. T-0794 mentions "eject". A tool that can leave cleanly earns trust, and the guard is the part users value most in bypass mode.
  Done when: `fm eject` writes one dependency-free hook script plus a test table, uninstalls Foreman, and the guard still blocks the same commands.

- **Wild: a 100-line guard a person can audit in five minutes** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: wild. The guard stops commands the user would never want in bypass mode. A guard small enough to read is easier to trust than one buried among 131 lib files.
  Done when: the guard is a single file of 100 lines or fewer, and the existing guard tests pass unchanged against it.

- **Wild: a weekly "diet" digest with a negative-growth goal** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: wild. The lean ratchet detects growth but nobody celebrates removal. The digest would show lines, rules and verbs removed against added, plus hook p95.
  Done when: the nightly digest prints net change for the week, and a week with net removal is marked as met.

- **Wild: a one-command home screen where plain `fm` shows only what to do now** — FEATURE — value 4 — effort M — risk low — category: entry
  Why: wild. `fm next`, `fm doctor` and the Watch lines each answer part of "what now". Bare `fm` could print one line of state and one suggested action.
  Done when: bare `fm` prints at most 6 lines and names exactly one next action.

Answer to an earlier question: the user checks Foreman's verdicts by hand with `fm doctor`, `fm task prove` and `fm night`. These can be logged from inside Foreman as verb calls, without reading shell history.

Next question: which shipped feature has had no session path call it in the last 60 days, and what would deleting it break?
Next question: when the user steers "keep it simple", which of the standing rules would they themselves drop first?
