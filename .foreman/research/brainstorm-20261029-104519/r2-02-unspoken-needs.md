# Brainstorm — lens: unspoken needs

- **Resolve a typed id or name to its target before any refusal** — FEATURE — value 4 — effort M — risk low — category: usability
  Why: Three recent asks (docs-impact path guess T-1995/2000, run.py `-k` that matched nothing, `-k core_integrity` vs class `CoreIntegrity`) are the same need: the user keeps hitting errors that know what they meant and don't say. Prior ideas cover "did you mean" as a helper; this one is a resolver applied at the entry point (task ids, test names, paths, lens names, lib cards) so the command proceeds with the confident match and prints what it assumed.
  Done when: `run.py test_doctor -k core_integrity` runs the CoreIntegrity tests and prints "matched -k core_integrity → CoreIntegrity"; an ambiguous input still refuses, listing candidates.

- **Make every "Ship Tn to main" precondition a pre-flight checklist** — FEATURE — value 4 — effort S — risk low — category: shipping
  Why: Five "Ship T-… to main" asks in one session, each followed by a fix about what ship tripped on (overlapping suites, ambient run, scope). The need behind it: ship should never surprise. Assumption: ship still discovers problems mid-run.
  Done when: `fm ship T-n --plan` lists every check it will run (dirty foreign files, running suites, scope, docs-impact) and flags the ones that would block, before running anything.

- **Attribute every dirty file to a task at the moment it's edited** — FIX — value 4 — effort M — risk med — category: scope
  Why: The `_theirs`/`_task_files` steers show the same bug class four times (doctor core-integrity, scope check at close, ambient run, first_touch). Each fix patched one consumer. The unspoken need is that "whose file is this?" be answered once, at edit time, and recorded.
  Done when: an edit hook writes owner=task-id per path; `fm doctor`, scope check, and close-out all read that one map, and a test with two tasks' dirty files passes on all consumers.

- **Warn at capture when a request is a sibling of one just closed** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: Asks come in pairs (T-1984/T-1989 fix, then a FEATURE telling the brief/blocker to say it; "one exact match already suggested, T-1995" then "up to three"). The user is doing the follow-up manually. assumption: pairs are common enough to detect via shared file paths.
  Done when: capturing an item that shares @paths with a task closed in the last day prints "follows T-n; fold in or keep separate?".

- **Say why a decision was dropped when the same idea resurfaces** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: Dropped entries carry carefully researched reasons (T-0401 never-idle, YAGNI on memoization). Brainstorms still risk re-proposing them; the user shouldn't have to re-argue.
  Done when: filing an item whose title overlaps a dropped one shows the dropped reason and requires `--again` to proceed.

- **Give each steer a durable test or rule** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: Steers read as corrections ("the note ignores edits outside the project", "ac 1's -k matched no test"). They're lessons, but T-0217 (lesson confidence) is deferred. Assumption: steers currently live only in session history.
  Done when: a steer recorded on a task creates a lesson linked to its test; recall of it appears in the next task touching the same file.

- **Verify DONE-WHEN commands actually discriminate, at capture** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: T-1994 showed an acceptance criterion (`-k core_integrity`) that matched nothing and would have passed vacuously. The unspoken need: a check that can't fail isn't proof.
  Done when: `fm task add` runs each DONE-WHEN against the pre-change tree and rejects any that already pass or match zero tests.

- **Auto-pick the focused task from the shipped id in the request** — FIX — value 2 — effort S — risk low — category: ergonomics
  Why: "Ship T-1996 to main" implies focus on T-1996. assumption: focus is currently manual.
  Done when: `fm ship` with an id switches focus and says so, with no "wrong task focused" refusal.

- **Wild: Let the user type the request once and have Foreman write the follow-up fix tasks it predicts** — FEATURE — value 3 — effort L — risk med — category: prediction
  Why: wild. History shows FIX → FEATURE pairs on the same file within hours; draft the likely second ask as a deferred item.
  Done when: after closing a FIX, a drafted sibling appears in the queue marked "predicted", dismissable in one key.

- **Wild: Dogfood-diff report: what Foreman did differently from plain Claude on this task** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. The user keeps tuning ceremony; showing the plan, proofs, and blocks that changed the outcome justifies (or prunes) each gate.
  Done when: closing a task prints "gates that changed the result: 2 (tests-fail-before, scope)" or "none".

- **Wild: A "quiet week" mode that only fixes what the user's last 20 asks implied** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: wild. The loop keeps generating ideas (many "Later from" deferrals) while the user asks for narrow fixes; mode ties the loop's scope to asked-history instead of fresh brainstorms.
  Done when: with the mode on, a loop round proposes only items sharing paths or error messages with the last 20 asks.

- **Show the cost of a refusal in tokens and retries** — FEATURE — value 2 — effort S — risk low — category: observability
  Why: Many fixes make refusals actionable; the user can't see which blockers cost the most turns. assumption: events are logged.
  Done when: `fm stats blockers` ranks refusals by retries-until-resolved.
