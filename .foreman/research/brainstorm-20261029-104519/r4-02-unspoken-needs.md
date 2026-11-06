# Brainstorm — lens: unspoken needs

- **Keep a bypass-mode ledger** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the pitch is that Foreman guards bypass mode, but the pack shows no record of what bypass let through. assumption: the hook can tell which commands would have prompted in default mode.
  Done when: `fm bypass --since 1d` lists every command that ran unprompted, with risky ones flagged, and a test shows the guard's allow decisions land in it.

- **Capture a FIX from the last output** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: most asks start as an odd message the user saw, e.g. "no test matches test_doctor with -k core_integrity gives no way forward". Today they retype it. `fm oops` would take the last command and its output, and draft `FIX: <cmd> says … / DONE-WHEN: <cmd> now …`.
  Done when: after a command prints a dead-end message, `fm oops "no way forward"` creates a task whose DONE-WHEN reruns that exact command and whose body quotes its output.

- **Use the suite wait for read-only prep** — PERFORMANCE — value 3 — effort M — risk low — category: ship
  Why: the user insisted on never running two suites at once (T-1964, T-1984), so `fm ship` has real idle seconds. Writing the changelog line, the close-out receipt and the sibling-gap sweep needs no test run.
  Done when: during a live `fm ship` test run, the receipt and changelog draft exist before the suite exits, and no second test process starts.

- **Show before/after output for every message fix** — FEATURE — value 4 — effort S — risk low — category: receipts
  Why: recent asks are nearly all wording changes ("names the -k", "suggests up to three paths"). `fm task prove` already shows the test failing without the change, so the receipt could print the old and new text side by side.
  Done when: closing a FIX whose proof test asserts on a message prints "before: … / after: …" in the receipt, and `fm digest --week` lists those pairs.

- **Trace every commit claim to an assertion** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: subjects make claims ("names the -k", "up to three paths") and T-1994's `-k core_integrity` matched no test. Nothing checks that each claim has an assertion behind it. assumption: claims can be extracted as short noun-verb phrases with a model.
  Done when: `fm trace T-1996` maps each claim in the subject to a test id and flags unmapped ones, and a fixture with an unbacked claim is flagged.

- **Echo the generalised rule on every steer** — FEATURE — value 4 — effort S — risk low — category: steers
  Why: steers like "_task_files had the same gap" and "the note ignores edits outside the project" are rules the user states once. "Treat repeated steers as standing rules" waits for repeats. Foreman could restate the rule on first sight, and the user answers y/n.
  Done when: a steer produces "I'll treat this as: <rule>, applying to <scope>. Keep? y/n" and a "y" stores a rule that the next relevant brief quotes.

- **Warn when an ask contradicts an earlier ask** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: a dropped idea was rejected because it "conflicts with T-0401's never-idle design (the user: make sure it doesnt sit idle)". That check exists for ideas, but a new typed ask could collide the same way. assumption: past asks are searchable as short intent lines.
  Done when: an ask that reverses a stored intent prints "this conflicts with T-0401: <line>. Proceed?" before capture, tested with a seeded pair.

- **Tell the asker when the fix is live where they use it** — FEATURE — value 3 — effort S — risk low — category: dogfood
  Why: the user dogfoods through the installed plugin, and an unupdated install is a known gap (T-0418). Shipping to main does not mean the fix runs in their next session.
  Done when: after a ship, the next session start says "T-1996 is live in your installed copy" or "T-1996 is on main, install is 3 commits behind", from a drift check.

- **Re-inject a compaction-proof task brief** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: long dogfood runs get summarized mid-task, and the focused task's DONE-WHEN, scope and proof state are what Claude most needs afterwards. assumption: a hook fires after compaction.
  Done when: after a simulated compaction, the next turn context contains a brief of 200 tokens or fewer with the task id, scope, DONE-WHEN and proof status.

- **Wild: Add a late-night caution at ship** — FEATURE — value 2 — effort S — risk low — category: safety
  Why: assumption: the user works in long bursts and sometimes late. Past a configurable quiet hour with no break, `fm ship` re-runs the proof on a clean tree and prints the receipt before merging, the way a pilot reads a checklist.
  Done when: with the clock faked to 03:00, `fm ship` re-runs the proof and requires the receipt to print before it merges; at 14:00 it does not.

- **Wild: Share a read-only pane link with a teammate** — FEATURE — value 3 — effort L — risk med — category: devices
  Why: the web UI and pane already exist, but the pack shows no way for a second person to watch a run. This would be an opt-in, local-network, read-only stream of the work bar, lanes and receipts, with a token that expires.
  Done when: `fm share` prints a URL that shows live task state without edit controls, and stops working after the token expires or `fm share --stop`.

- **Wild: Keep a "what Foreman does now" page written from before/after pairs** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: assumption: with 2000 tasks, the user can't recall current behaviour. The before/after pairs from the receipts above, grouped by command, would make a living behaviour reference that is also a regression suite.
  Done when: `fm behaviour run` replays every stored pair against the current build and fails when any "after" text has drifted without a task.
