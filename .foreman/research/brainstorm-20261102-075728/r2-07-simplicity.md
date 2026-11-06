# Brainstorm — lens: simplicity

- **Make the idle goal path import nothing** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: the pack's gates include `bench_hooks.py`, and the lean ratchet tracks hook p95. Assumption: goal code is loaded eagerly. A user with no active goal shouldn't pay for the goal engine.
  Done when: a bench test shows that with no goal active, no goal module is imported, and the hook p95 is no higher than on a build with the goal code removed.

- **Give goal rows no authority** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: goals get seeded from pasted tickets and PRDs, which are untrusted text. Assumption: nothing stops a row from carrying "push to main" or "set a grant". Rows would be data only, so grants, publishes and guard changes would come only from the user's steers.
  Done when: a goal whose rows say "grant push" or "disable the guard" leaves grants and guard state unchanged, and a planted-row test proves it.

- **Refuse secrets and absolute home paths in the goal file** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the goal file sits in or beside the repo and may be committed or handed off. Assumption: the existing redaction applies only to the handoff page, not at write time.
  Done when: `fm goal` refuses to store a row containing a token-shaped string or `/home/<user>`, and says which row.

- **Test that goal modules never touch the network** — PRIVACY — value 3 — effort S — risk low — category: local-first
  Why: the site claims things stay local. An import-and-call scan of the goal modules (no socket, urllib, subprocess to curl) is a cheap standing proof.
  Done when: a unit test fails if any goal module imports a network library, and passes on the current tree.

- **Hold goal modules to the standard library** — SECURITY — value 2 — effort S — risk low — category: supply chain
  Why: the pack's supply-chain cluster (T-0791) is deferred. A stdlib-only rule on the goal engine is the smallest version of that defence.
  Done when: a test parses the goal modules' imports and fails on any non-stdlib name.

- **Cap the live plan at 12 rows and spill the rest to `later.md`** — FEATURE — value 4 — effort M — risk med — category: plan size
  Why: the user steers against scope growth, and the idea list includes "check plan size against the ask". A hard cap forces ordering, and the spill file keeps best-in-class items from being lost.
  Done when: decomposing a vague goal yields at most 12 live rows, with every other item in `later.md` carrying its reason, and promoting one swaps it in.

- **Collapse the goal surface to three verbs** — CLEAN — value 3 — effort M — risk med — category: developer experience
  Why: the pack shows "later from T-0794 slim Foreman" and a verb-count ratchet, and every earlier idea added another verb. Assumption: the goal verbs already number five or more. Keep new, status and done, and make the rest flags.
  Done when: `fm goal help` lists three verbs, the old verbs still work as aliases for one release, and the verb count doesn't rise.

- **Add `fm goal status --plain` for 40-column, no-ANSI output** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: the pack names the phone, SSH, tmux and watch surfaces. Plain text pipes into all of them with no new UI.
  Done when: the output is at most 40 columns with no escape codes, and a test checks the width against a long goal.

- **Break plan ties by fewest new dependencies** — FEATURE — value 3 — effort S — risk low — category: decomposition
  Why: assumption: when a plan row has two viable approaches, nothing today prefers the simpler one. A boring default also lowers supply-chain exposure.
  Done when: for a planted two-approach row, the plan picks the one adding no dependency and records the reason in one line.

- **Compact closed rows so goal state stays small** — PERFORMANCE — value 3 — effort M — risk med — category: resume
  Why: the goal has to survive days, crashes and compactions, so the file grows with every row. Each closed row folds into one line (id, proof command, commit), with the full text kept in git.
  Done when: after 200 closed rows the goal file is under 8 KB and resume time is unchanged.

- **Wild: paste a 280-character goal token to resume in any harness** — FEATURE — value 3 — effort M — risk med — category: handoff
  Why: wild. The pack lists hookless harnesses and mid-flight switches. A short token (goal id, repo identity, next row, done-oracle hash) can be pasted into any chat and resolved from local files.
  Done when: pasting the token into a fresh Codex or Gemini session makes the harness print the correct "where we were" lines from files alone.

- **Wild: the sticky-note test** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: wild. If the finished version can't be stated in three lines, the goal is two goals. The planner proposes the split instead of building a 40-row monolith.
  Done when: a planted sprawling goal produces a split proposal naming two sub-goals, and a small goal passes without one.

- **Wild: delete the goal state at close and keep only a tombstone** — PRIVACY — value 3 — effort S — risk med — category: lifecycle
  Why: wild. Finished goals leave state files that nobody reads and that may hold sensitive wording. Closing writes the three-line receipt to the repo and removes the working state, which stays recoverable from git history.
  Done when: after `fm goal done`, the state dir holds no files for that goal, the receipt exists, and `fm goal show` can reconstruct it.

Next question: Which of the goal engine's current files and verbs has no session path that calls it, and could it be deleted without any user noticing?
Next question: What does the goal engine cost per session in time and injected characters when no goal is active, measured on the user's real machine rather than the bench?
