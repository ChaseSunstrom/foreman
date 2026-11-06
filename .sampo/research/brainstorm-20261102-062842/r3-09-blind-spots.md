# Brainstorm — lens: blind spots

**Answers first, from the blind-spot lens.**
- *What does the user lose when the guard errs toward blocking?* Nothing in the pack tracks it. The only guard numbers are the 124 labelled cases, which measure accuracy, not prompts lost per session.
- *Which output does the user act on unchecked?* The "Foreman 1.2.51 / Genesis: tower update" status lines and the auto-published `site/genesis` data. Nothing outside Foreman checks either one.

**The class behind the missed asks:** Foreman builds to the *letter and shape* of an ask. The asks it missed were about invented details (a flag spelling, a 7-vs-8 character threshold), inputs that were partly Foreman's own, and checks that pass while proving nothing. Ideas below are in that class and not already in the catalog.

- **Itemise invented details at task finish** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: steers fixed `--by harness` vs `--by-harness` and "8+ characters" vs a 7-character example. In each case Foreman chose a detail the user never wrote. The existing "literal tokens" check only goes request→surface, not surface→request.
  Done when: `fm task finish` prints "Choices I made that your words didn't state", listing each new flag, threshold, default and name absent from the request. A test fixture with one invented flag lists exactly that flag.

- **Test a criterion against its own examples** — FIX — value 4 — effort S — risk low — category: intake
  Why: T-2583's rule and its own example ('4% lost') contradicted each other, and the user caught it.
  Done when: capture extracts quoted examples from a DONE-WHEN and runs them through the stated rule. A criterion saying "8+ characters" next to a 7-character example is refused with both quoted.

- **Make the self-change gate say "inconclusive" under noise** — PERFORMANCE — value 4 — effort M — risk low — category: gates
  Why: T-2605 moved the gate to median wall time on a loaded bench after a flake. Nothing records the bench's own variance.
  Done when: each gate run stores its noise band. A delta inside the band reports "inconclusive, rerun" and never passes or fails. A test with an injected CPU hog gets no verdict.

- **Bench hooks cold, as the user lives them** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: `bench_hooks.py --runs 20` is warm by construction. The first hook after login, with a cold bytecode and file cache, is what the user feels, and no gate covers it.
  Done when: `fm doctor` shows first-run and steady-state p95 separately. A test clears `__pycache__` and gates the first-run figure.

- **Scrub everything `fm genesis live` publishes** — SECURITY — value 4 — effort S — risk low — category: publishing
  Why: a standing rule auto-publishes `site/genesis` to main with no human read. Tower data quotes steers and paths, and assumption: nothing scans them for home paths, emails, hostnames or tokens.
  Done when: publish refuses if a scan of the staged data finds any of those. A planted `/home/<user>` string blocks the publish with the file and line.

- **Audit each use of a durable grant against its words** — SECURITY — value 3 — effort M — risk med — category: grants
  Why: the push grant ("feel free to push to main at any time") is standing. Each use is set per task and spent, but nothing shows the user a drift view.
  Done when: `fm doctor` lists each grant, its use count and the commands run under it. A use outside the grant's literal scope is flagged.

- **Census vacuous proofs across closed tasks** — FIX — value 3 — effort S — risk low — category: verification
  Why: T-2606 handled a criterion whose runs matched no test, but only for the case in front of it. Renames rot old `-k` selectors silently.
  Done when: a nightly pass re-collects every stored verify command and lists any that now match zero tests. A fixture with a renamed test shows up in the list.

- **Add `fm define TERM`** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the user's own text uses cell, arm, Seed, ratchet, steer, door and titer without definitions. The README and MASTER.md cover none of the tower vocabulary in plain words.
  Done when: `fm define ratchet` prints one sentence plus the file that implements it, for every term in a maintained glossary. A test fails if a term used in the status line has no entry.

- **Report a guard's cost in prompts** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: the open question about prompts lost per session has no tracked number. Accuracy over 124 cases says nothing about interruption.
  Done when: `fm doctor` shows blocks, user overrides and prompts-per-session for the last 30 sessions. It names the top rule by overrides.

- **Wild: have a blind child write the test from the DONE-WHEN alone** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: assumption: a tool-less child that never sees the builder's reading will expose ambiguity, such as the 7-vs-8 case. Divergence between its test and the builder's test is the signal.
  Done when: for M and L tasks, a child-written test runs against the builder's change. A mismatch files an "ambiguous criterion" question instead of closing the task.

- **Wild: drill capture with hostile briefs** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: the missed asks are all intake-shaped. Assumption: planted bad briefs (a wrong flag, a contradictory example, a feature that already exists) measure whether capture catches what the user catches.
  Done when: a fixture intake with 6 planted defects reports the catch rate per defect type. The result appears in `fm exam`.

- **Wild: diff a stranger's weekly status against the user's recall** — FEATURE — value 3 — effort S — risk low — category: awareness
  Why: the user acts on unattended work they don't check. A tool-less child reads only one week of git log and `fm outcomes` and writes a status. The user marks what surprised them.
  Done when: `fm week` prints the status plus a "did you know?" list of items with no matching user-side ask. Each surprise is recorded.

Next question: which Foreman-chosen numbers or names (flag spellings, thresholds, cell wording) has the user corrected, and does a test pin each correction as a standing rule?
Next question: for the self-triggering grade, what is the simplest observation the user could make by hand in one minute that would contradict Foreman's own claim that a tick ran?
