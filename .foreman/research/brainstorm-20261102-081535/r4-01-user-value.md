# Brainstorm — lens: user value

- **Boot with only the documented environment** — FEATURE — value 4 — effort M — risk low — category: docs/ops
  Why: assumption: "docs against code" checks flag names, but a project can still start only because the developer's shell holds undocumented variables, tools or files. Run the entry point in a scrubbed env, with `env -i` plus only the variables the README, `.env.example` and compose file list. Each failure names the undocumented dependency.
  Done when: a fixture app that reads an undocumented `FOO_TOKEN` fails the boot proof and names `FOO_TOKEN`; the same app passes once `FOO_TOKEN` is documented.

- **Flag thinner rigor than comparable past tasks** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: assumption: the user never asks "did you check less than last time?", but that's how a lazy FIX slips through. Compare this task's proof kinds, count and strength with the median of the last N closed tasks of the same kind in this repo. Print one line when it is clearly below.
  Done when: replaying a closed task with its proofs stripped prints "thinner than 8 of 9 similar tasks: no shot, no data check". An average task prints nothing.

- **Prove schedule claims with a next-fire table** — FEATURE — value 3 — effort S — risk low — category: ops
  Why: assumption: "runs nightly at 02:00" in a cron, systemd timer or CI workflow is a claim that unit tests never touch. Parse the schedule, print the next 5 fire times in the user's timezone, and flag DST gaps and overlaps, `@reboot` in containers, and CI cron's UTC-only rule.
  Done when: `0 2 * * *` under a spring-forward timezone is flagged for the skipped hour, and the table matches `systemd-analyze calendar` on a fixture.

- **Resolve every link, anchor and asset in docs and site** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the pack shows `site/` (64 files) and a README with in-page anchors like `#quick-start`, but only token-level docs-vs-code checks. Check local relative links, `#anchors` and image paths with no network. External URLs are checked only when a setting allows it, so nothing leaves the machine by default.
  Done when: a renamed heading breaks a fixture's `#how-it-works` link and the check names the file and line. With the default setting it makes zero network calls.

- **Add a "never opened" audit on claims about code** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: assumption: a finish that says "the parser handles X" is weaker if the session never read the parser. Map each file or symbol named in the final message to whether any tool call read, searched or ran it. Unread ones are tagged unproven by name.
  Done when: a transcript fixture whose final message mentions `parse.py` with no read of it yields "named, never opened: parse.py".

- **Prove file modes and leftovers after every prover run** — SECURITY — value 3 — effort S — risk low — category: security
  Why: existing ideas fail proofs that leave residue, but none checks what the run created. Diff the filesystem before and after a flow. Flag world-readable files that contain key-like strings, new symlinks leaving the tree, and `0777` modes.
  Done when: a fixture flow that writes `token.txt` as `0644` fails with the path and mode.

- **Check that a commit message is legible from its diff** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: assumption: the user's disbelief often starts when the summary doesn't match the change. A small local model, sent nothing external, restates the change from the diff alone. A cheap overlap check against the commit or PR text flags mismatches such as "refactor" versus a behaviour change.
  Done when: a commit titled "rename var" that also changes a default is flagged as "behaviour change not mentioned".

- **Add a disbelief button that spawns a different-method re-prove** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: assumption: the user's real verification is gut-level doubt about one proof, and no current idea captures it. `fm doubt PROOF` re-proves the claim by a different prover kind and records which method the user distrusts. Future proofs of that kind are tagged "user-doubted".
  Done when: doubting a unit-test-only proof of a UI claim launches `fm shot`, and the ledger shows doubted and re-proved with the outcome.

- **Render transactional email and notification text as proofs** — FEATURE — value 2 — effort M — risk low — category: UI
  Why: assumption: the "UI" surface in the pack is web, but products often ship emails, toasts and CLI errors that screenshots never see. Render templates to an image, check that the plain-text part exists and links resolve, and run a placeholder-leak scan for `{{name}}` and `None`.
  Done when: an email fixture with an unfilled `{{first_name}}` fails with the line number.

- **Gate a ship on proofs from the user's last bad week** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: the user steers hard on proof before presentation. Keep a short "scars" list of claims that were wrongly called done in the past. Re-run each scar's prover at `fm ship` and name the one that matters if it can't run.
  Done when: a scar from a false-done task re-runs at ship, and a deliberately re-broken change fails the gate with that scar's id.

- **Wild: write the user's first Monday-morning check** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: assumption: after a finished task, the user's real question the next day is "does it still work?" Generate a 60-second `monday.sh` of the three cheapest proofs from the task. Run it automatically on the next session start and print one pass/fail line.
  Done when: closing a task with proofs writes `monday.sh`. The next session start prints "yesterday's work: 3/3 still hold" or names the break.

- **Wild: rehearse the claim with a deliberately wrong build** — FEATURE — value 3 — effort M — risk med — category: trust — wild
  Why: assumption: proofs should be shown to bite. Before showing "proven", apply a one-line plausible mutation in a scratch copy and require the prover to go red, so the user sees red then green side by side.
  Done when: the finish receipt shows "red on mutant `x > 0` → `x >= 0`, green on real" for at least one proof, and a prover that stays green on the mutant is downgraded to weak.

- **Wild: let proofs have a visible half-life on the status line** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: assumption: proofs expire when covered files change, but the user can't see it. Show a small `proof: 5 fresh · 2 stale` counter that dims as covered files move, and expands to the stale claim names on request.
  Done when: editing a file covered by one proof changes the counter within one prompt and `fm status` names the claim.

Next question: Which of these checks would the user run by hand today, and where is the log (shell history, transcripts) that shows it, so the next brainstorm ranks by observed habit instead of by Foreman's guess?
Next question: What does "unproven" cost the user in practice (reopened tasks, a bad push, a missed bug), and is there a ledger of that cost to weight the proof-debt ranking?
