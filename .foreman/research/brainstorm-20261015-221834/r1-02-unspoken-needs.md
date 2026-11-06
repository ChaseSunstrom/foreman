# Brainstorm — lens: unspoken needs

- **Resume ledger for every long-running unit** — FEATURE — value 5 — effort M — risk low — category: resilience
  Why: the user asked for easy resume of stopped worktree builders (T-1028 planned) and T-0831 notes capped `claude -p` children lose partial work; brainstorms, audits and reviews have the same failure. Assumption: they don't share a record format today.
  Done when: killing any `fm` child (builder, brainstorm, audit) mid-run and running `fm resume` lists it with task, branch/worktree, last step and a one-command continue, and continuing it finishes without redoing completed steps.

- **Record obstacle→fix pairs with a "did it actually work" check** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: user's "why have you not improved" complaint; T-1032 offers known fixes, but nothing shows a fix was later confirmed or got stale. Assumption: hints have no outcome tracking.
  Done when: each hint carries applied/worked/failed counts, a hint that failed twice is demoted and flagged in `fm doctor`, and a test shows a hint with a recent success outranks an older one.

- **Ship a portable `.foreman/known/` bundle with import/export** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: the user steered that fixes must travel by git, with project fixes in the repo and machine-wide ones in Foreman state. Assumption: promotion between the two tiers is manual or absent.
  Done when: `fm known promote <id>` moves a machine-wide fix into the repo file and a fresh clone's session surfaces it with no setup.

- **Scrub secrets and paths from shared hints before commit** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: fixes now ride in git, and transcript-derived text can hold tokens, home paths or private URLs; T-0791 lists injection defenses but not leakage into committed hints. Assumption: no redaction pass exists yet.
  Done when: a hint seeded with a fake API key and `/home/user/...` is committed with both redacted, and a CI check fails on a committed hint matching a secret pattern.

- **Treat a hint pulled from git as untrusted input** — SECURITY — value 4 — effort M — risk med — category: trust
  Why: teammates' hints get injected into sessions, and the 18 injection ideas in T-0791 are deferred. A poisoned hint could say "run curl|sh".
  Done when: hints are data-only (symptom, match, suggested command) and any suggested command passes through the guard hook, with a test where a malicious hint's command is blocked.

- **Auto-detect recurrence and propose a permanent fix** — FEATURE — value 5 — effort M — risk low — category: self-improvement
  Why: the user asked for "detect an issue and automatically go that path in the future". Assumption: today a hint is only offered, never escalated. When the same obstacle recurs three times, Foreman drafts a task to remove the cause (a test, a guard, a doctor check) rather than just remembering the workaround.
  Done when: after three recorded recurrences, `fm next` shows a root-cause task citing the three occurrences, and it is not created again once closed.

- **Show a "what Foreman learned this week" digest** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: the user doubted that Foreman improves, and nothing visible says otherwise. Assumption: the ledger already has the data.
  Done when: `fm learned --since 7d` and a pane section list new hints, how often each fired, and the failures avoided.

- **Add a regression test for each learned fix, auto-drafted** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: the drops list repeats "catch it earlier: no test covered this" several times. A learned obstacle should leave a test that reproduces it.
  Done when: closing a task that recorded an obstacle prompts for or drafts a failing-first test linked to the hint, and the hint shows its test id.

- **Heartbeat checkpoints so a killed session leaves a resumable state** — FEATURE — value 4 — effort M — risk low — category: resilience
  Why: SIGKILL, a power loss or a terminal close skip Stop hooks, and T-0798 (transcript repair, blackstart) is deferred. Assumption: state is only written at hook boundaries.
  Done when: after `kill -9` mid-task, the next SessionStart reports "interrupted at step N of T-xxxx, worktree W" within one line and offers the resume.

- **Wild: Make the pane a time scrubber over a past session** — FEATURE — value 3 — effort L — risk med — category: observability
  Why: wild. The ledger and the Agents graph already hold event data. Scrubbing back shows what each agent did when, and where a session went wrong, and it doubles as the replay-against-new-rules idea.
  Done when: `fm ui --replay <session>` steps the Agents graph forward and back from the ledger alone.

- **Wild: Let sessions on one machine share learned fixes live across projects** — FEATURE — value 3 — effort M — risk med — category: fleet
  Why: wild. The user wants "any project", and `fm scout` already reads across projects. A fix learned in repo A shows up in repo B's session when the symptom matches, marked "from another project", opt-in per project.
  Done when: with the setting on, a symptom first solved in project A is offered in project B and labelled with its source; with it off, nothing crosses.

- **Wild: Hold a nightly "dojo" that replays recorded obstacles against the current Foreman** — FEATURE — value 3 — effort L — risk med — category: self-improvement
  Why: wild. Real failures captured by T-0035 become a regression suite, so a Foreman change that re-breaks a learned fix gets caught before release.
  Done when: `fm dojo` replays the stored obstacles headlessly and reports which hints still resolve them, and the release gate fails if one regressed.

- **Name the user's recurring corrections as standing rules** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the user repeats steers ("fill the panel", "no gaps", "any project", "fewer facts per line"). Assumption: these live only as one-off requests. Foreman should notice a repeated steer, propose it as a standing rule with a check, and apply it to future UI and design tasks without being asked.
  Done when: after the same steer appears three times, `fm next` proposes a rule and, once accepted, a later UI task is checked against it with the result shown in its close receipt.
