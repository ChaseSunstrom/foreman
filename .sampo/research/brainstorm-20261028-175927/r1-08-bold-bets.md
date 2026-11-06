# Brainstorm — lens: bold bets

- **Replace the gate with a content-addressed proof cache shared across machines** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: the pack shows repeated gate-lock waits, a flaky hook bench, CI minutes capped at 20, and "stop gate-lock waits between projects". Many ideas ask for memoized checks, none make a proof portable. assumption: tree-hash keyed results are safe when the toolchain and environment are hashed in.
  Done when: running the same suite on a second checkout with an identical tree hash returns a verified cached verdict in under 1 s, and a one-byte change to a source file forces a real run.

- **Run Foreman's whole loop as one Claude Code slash command with zero child processes** — FEATURE — value 5 — effort L — risk high — category: architecture
  Why: the user's steers keep pointing at burn and complexity (usage burn, "cut Foreman's usage burn", plugin/CLI parity gaps, T-0794 slim Foreman). Child `claude -p` fan-outs multiply cost. assumption: native subagents and Stop-hook loops can carry queue, lanes and the gate.
  Done when: a queue of three tasks completes inside one interactive session with no `claude -p` spawned (verified by process log), and `fm cost` shows lower total tokens than the child-process path on the same fixture.

- **Teach the guard from a replay of the user's own shell history** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: round 5 review: 6 destructive blocks mostly from guard collisions ($VAR paths, rm on /tmp globs); "refusal text could name the literal-path rewrite". The pack has no way to measure false positives against real use. assumption: shell history is readable and stays local.
  Done when: `fm guard replay ~/.bash_history` prints a block/allow table, every false block shows a suggested rewrite, and a retry of the rewritten command passes first time in a test.

- **Make every refusal self-healing: the guard returns the one rewrite that would pass** — FIX — value 4 — effort M — risk med — category: guard
  Why: the same review notes the refusal text should name the literal-path rewrite so a retry succeeds first time. Ledger already has "explain a guard refusal in plain English", but not a machine-applied safe rewrite.
  Done when: for a corpus of 20 refused-then-rewritten commands, the guard's suggested rewrite is accepted by the guard in 100% of cases and never widens scope (checked by a test).

- **Triage entry point that picks the surface** — FEATURE — value 4 — effort S — risk low — category: backlog
  Why: the review finds four triage routes (first, swipe TTY, swipe --serve, app view I) with no single entry; serve has no undo and no cards-left count.
  Done when: `fm inbox triage` opens swipe in the browser when a display exists, otherwise the TTY, shows "n left", and `u` undoes the last verdict, covered by a test of each branch.

- **Ticket sync that updates instead of duplicating, and posts the commit back** — FEATURE — value 4 — effort M — risk med — category: integrations
  Why: T-1859 fetches Jira/Linear only; an upstream edit makes a second brief; no GitHub issues, no write-back on close. Outward posting needs an explicit opt-in setting.
  Done when: re-running `fm inbox ticket GH#12` after the issue changes updates the existing brief in place, and `fm done` with `post_back=true` comments the commit link (against a stub server in tests).

- **Report known-fix hit rate: offered, accepted, wrong** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: T-1865 made matching safer but nothing measures whether it helps.
  Done when: `fm stats fixes` prints per-fix offered/accepted/rejected counts from the journal.

- **Wild: Run a nightly "new user, old repo" rehearsal that files its own bugs** — FEATURE — value 4 — effort L — risk med — category: dogfood
  Why: assumption: the biggest remaining defects are first-hour friction (T-0862/0863 deferred for lack of evidence). A headless persona clones a fixture repo, follows only the README, and any stall becomes a captured task with the transcript. wild
  Done when: the nightly run produces a report, and a seeded README break (a wrong command) is caught and filed within one run.

- **Wild: Make the queue a git ref so any machine can pick up lanes** — FEATURE — value 4 — effort L — risk high — category: fleet
  Why: the user pushes foreman/build to main, runs three builder lanes, wants overnight work (T-0793). Putting the backlog on an orphan ref gives sync, history and merge for free. wild
  Done when: two clones add different tasks offline, `fm sync` merges them without conflict, and a lane on clone B claims a task atomically so clone A cannot double-run it.

- **Wild: Price every queued task in dollars before it runs and refuse what can't finish before the reset** — FEATURE — value 5 — effort M — risk low — category: usage
  Why: the user's complaint that Foreman should have noticed its own usage burn unprompted; defer-until-reset already exists, so a forecast closes the loop. wild
  Done when: `fm queue quote` shows estimated cost and finish time per task, and `fm run` refuses (with the reason) when the quote exceeds remaining weekly budget, tested with a faked ledger.

- **Serve one local index of every served page, with a shared style** — CLEAN — value 3 — effort S — risk low — category: web UI
  Why: review notes settings serve and swipe serve each duplicate a style block and need Ctrl-C and one-shot tokens with no index.
  Done when: `fm serve` lists all pages with a single stylesheet, and removing a page's inline style block leaves it visually identical in a screenshot diff.

- **Scene gallery with a render-under-1s test and a caption per scene** — FEATURE — value 3 — effort S — risk low — category: scenes
  Why: T-1846..1855 shipped many scenes, with no index, no "what am I looking at" caption, no timing test.
  Done when: `fm scene gallery` renders every scene with its caption, and the test fails if any scene exceeds 1 s.

- **Report unused design tokens in DESIGN.md against the CSS** — FEATURE — value 3 — effort S — risk low — category: design
  Why: review notes Figma import is one-way and nothing checks tokens are used.
  Done when: `fm design unused` lists tokens with zero references in the project's CSS, and a fixture with two planted unused tokens reports exactly those two.
