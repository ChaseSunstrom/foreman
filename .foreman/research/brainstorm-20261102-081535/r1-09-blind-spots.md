# Brainstorm — lens: blind spots

- **Refuse A/B comparisons on unequal samples** — FIX — value 4 — effort S — risk low — category: measurement
  Why: T-2566 (select ignored held-out-only exam lines) and T-2610 (30-day windows must finish) are one class: two sides compared over different populations. Question missed: "what does each side of this comparison actually contain?"
  Done when: every select, duel, ablate and calibration compare prints `n_a / n_b / shared` scenario ids and exits "inconclusive" when shared is below a floor, shown by a test with disjoint arms.

- **Keep a verification-kind ledger** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: the request names six kinds of proof (UI, data, docs vs code, infra/ops, performance, intent). Nothing records which kind a closed task needed, which ran, and which were labelled unproven. Assumption: today only tests and `fm task prove` leave a trace.
  Done when: `fm task finish` writes `kinds: ui=ran data=n/a infra=unproven…` per task, and `fm doctor` WARNs on a kind with zero real runs in 30 days.

- **Add `fm prove data`: invariant and snapshot diff** — FEATURE — value 4 — effort M — risk med — category: data verification
  Why: the pack shows UI and perf instruments but no data verifier. Assumption: migrations and ledger rewrites (T-2610-style window changes) are today proven only by unit tests.
  Done when: running it before and after a change to a ledger or DB fixture prints row counts, key uniqueness, null rates and a checksum delta. A planted dropped row turns it red.

- **Find infra dry-run verifiers from manifests** — FEATURE — value 3 — effort M — risk low — category: ops verification
  Why: T-2542 (timers known alive) shows unit files can be installed but dead. Dry-run checks (`systemd-analyze verify`, `docker compose config`, `terraform validate`) can be found from the manifests Foreman already reads.
  Done when: a repo with a broken unit or compose file gets a red check line, and a missing tool is printed as "unproven: tool absent", never as green.

- **Generate a UI state matrix for `fm shot`** — FEATURE — value 3 — effort M — risk low — category: UI proof
  Why: `plugin/templates/web/index.html` is the surface, and empty, loading, error, long-text, RTL and narrow states are where UIs break. Assumption: `fm shot` is taken per page, not per state.
  Done when: one command shoots each page across at least 6 states, and a diff against the last green shot flags a changed state.

- **Run windowed logic across calendar boundaries** — FIX — value 3 — effort S — risk low — category: reliability
  Why: T-2610 and the 30-day bet windows, plus the T-2542 interval checks, all depend on dates. Question missed: "what happens on day 31, leap day or DST?"
  Done when: the suite runs the calibration, tick and window tests under injected clocks at day 29, 30, 31, Feb 29 and a DST shift, and a boundary off-by-one is caught by a planted case.

- **Ship a hand-computed known answer with every instrument** — FIX — value 4 — effort S — risk low — category: measurement
  Why: the missed asks (T-2534, T-2566, T-2610) were all instruments that were quietly wrong, not features. Brier, select, exam grade and the bench gate need a tiny fixture with an answer computed by hand.
  Done when: `fm doctor` runs each instrument on its fixture and goes red if the output differs from the stored hand answer.

- **Keep one aged register of unproven claims** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: the request says whatever can't be proven gets labelled unproven. Today that label lives in each task's text and is never summed up.
  Done when: `fm unproven` lists every open "unproven" label with its age and the cheapest named step to prove it, and the finish card links to it.

- **Fence two-device writes with a token** — FIX — value 3 — effort M — risk med — category: devices
  Why: this answers the pack's left-over question about a desk lease and a phone tap on the same row. Assumption: no fencing exists today.
  Done when: a stale writer's update is refused with "row moved on at HH:MM by <device>", and a two-process test shows exactly one winner and one notified loser.

- **Ask once before a private goal needs a remote model** — FEATURE — value 2 — effort S — risk low — category: privacy
  Why: this answers the pack's left-over privacy question. The safe default is fail closed, then one `fm ask`, with the answer stored as a costly decision and reused for that goal only.
  Done when: a goal labelled private that needs a remote-only capability stops with the ask, and a second run reuses the stored answer without asking again.

- **Wild: hold a falsifiability auction before building** — FEATURE — value 3 — effort M — risk med — category: proof
  Why: wild. The wished-for proof beyond unit tests is the cheapest observation that would show the feature wrong. Two tool-less children each propose one, and the cheaper becomes the task's first verify command.
  Done when: a task with an auction row has a verify command that fails on the parent commit.

- **Wild: verify as a tourist with no source** — FEATURE — value 3 — effort M — risk med — category: intent
  Why: wild. "Does it do what the user meant" is the weakest-proven kind. A child sees only `fm shot` and `fm flow` output and the user's verbatim ask, then says whether the demo satisfies it. Disagreement becomes "intent: unproven".
  Done when: a planted wrong-but-passing change is flagged by the tourist in an exam scenario.

- **Wild: turn each missed-ask question into an executable `.q` check** — FEATURE — value 4 — effort M — risk med — category: blind spots
  Why: wild. The pack's lens is "name the question that would have caught it". If each question is stored as a grep or AST pattern plus a probe, the next generation re-runs the whole library and files only new hits, so a missed-ask class cannot recur silently. Assumption: today the questions live in prose in brainstorm packs.
  Done when: `fm blindspots` runs at least the 8 known classes as checks, each with a planted violation it catches, and a new class is added by dropping one file.

Next question: which of Foreman's own instruments have a hand-computed expected answer in the repo, and which have only been checked against themselves?
Next question: for each of the six verification kinds, what is the last real (not fixture) run, and who would notice if it stopped working?
