# Brainstorm — lens: blind spots

I read the eight unpredicted asks (T-2093 to T-2113) as one class: after a capability lands, the user has to ask for its **satellites**. These are check, step, bootstrap-from-nothing, select, drift, offer-itself, held-out exam and seal. The question a brainstorm should have asked is "what must exist around this capability before it can be trusted, resumed, offered, measured and sealed?" Asked of the whole project, it surfaces these ideas, all new to the list.

- **Grid every capability against its satellites** — CLEAN — value 5 — effort M — risk low — category: process
  Why: all eight missed asks were satellites of Genesis, each requested after the fact. Coverage.md already grids areas; nothing grids capabilities. Initiative (Mission 3) is about to repeat this.
  Done when: `fm genesis check` fails on an empty (capability, satellite) cell, and the grid lists Initiative with check, step, drift, offer, exam and seal each present or marked not-yet with a reason.

- **Write a lib card per exam stack** — FEATURE — value 4 — effort M — risk low — category: stacks
  Why: cards exist for python, tailwind and cc-* only, but the exam spans python, js, ts, ruby, rust and c, and Foreman found 0 of 108. Each card would give the single-test command, the assertion idiom, and the usual defect shapes for that language (C unchecked returns, Ruby nil, Rust unwrap/overflow).
  Done when: `fm lib show rust` (and the other five) prints a card, and a finder run on a never-seen rust repo cites it.

- **Score a crashed hunt as an error, never as a correct "none"** — FIX — value 5 — effort S — risk low — category: exam
  Why: T-2112 already made fallback drafts count as errors for Genesis. The same hole exists in Mission 3: the exam's `none` kind rewards silence, so a finder that times out looks perfect.
  Done when: a stub finder that exits 1 on a clean fixture repo scores `error` in exam.jsonl, not `pass`.

- **Write the proof test in the repo's own test idiom** — FEATURE — value 4 — effort M — risk med — category: proof quality
  Why: assumption: a landed failing test that ignores the project's framework, naming and fixtures is one the user deletes. Reading three neighbouring tests first would fix that.
  Done when: on a fixture with pytest-style and unittest-style repos, the generated test uses the repo's own framework and file naming, checked by a lint.

- **Turn an unresolvable oracle into a batched question** — FEATURE — value 3 — effort M — risk low — category: ambiguity
  Why: the exam has `ambiguous` and `vague` kinds, but the pipeline only has bug or none. When code could be a bug or deliberate, a question card is better than a guess.
  Done when: an ambiguous planted case yields one question line with both readings, and no lane opens.

- **Route every outward action through one coalescing outbox** — SECURITY — value 4 — effort M — risk med — category: outward actions
  Why: the user asked for a standing grant plus debounced pushes for the Genesis site, so a burst of puts becomes one push. Night-shift findings will multiply such actions (push, publish, notify), each with its own ad-hoc debounce.
  Done when: `fm outbox` lists pending pushes, publishes and notifications with their grant ids, and 20 events in a minute produce one push.

- **Add `fm miss` for bugs Foreman should have found** — FEATURE — value 4 — effort M — risk low — category: feedback
  Why: assumption: the only recall measure today is the synthetic exam. The user's own later fix commits are the cheapest real misses.
  Done when: `fm miss <commit>` checks out the parent, reruns the hunt, records hit or miss, and a miss files a probe-candidate task.

- **Randomize fixture commit hashes in the test suite** — FIX — value 3 — effort S — risk low — category: flakes
  Why: test_ship's `--check` test fails when a hash ends in "add", a substring match on "add a". That is a value-dependent flake no deterministic rerun reveals.
  Done when: the suite passes 50 runs with random hex hashes (including ones ending in `add`), and a finder kind "tests keyed on identifier content" flags the original.

- **Version the findings ledger and migrate it on read** — CLEAN — value 2 — effort S — risk low — category: durability
  Why: assumption: the findings ledger will change shape during Mission 3 (verdict types, fingerprints). Resumable `step` needs old ledgers to stay readable.
  Done when: a v1 ledger fixture loads under the current fm with a migration line, and an unknown future version refuses cleanly.

- **Wild: fan out an intake's siblings with one key** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: wild; assumption: when the user files a feature, the satellites follow within days. Intake would classify the ask, propose the check, step, exam and seal briefs, and queue them all on one key.
  Done when: filing "FEATURE: fm find" prints a sibling list drawn from the grid, and one key files them as linked tasks.

- **Wild: score how often the brainstorm predicted the user's next ask** — FEATURE — value 3 — effort M — risk low — category: meta
  Why: wild. A cold model sees the pack and writes the user's next three asks. A day later it is scored against the real ones, giving a blind-spot rate that is shown per round and on the Genesis page.
  Done when: the Genesis page shows a prediction-hit rate per round, computed from the intake log.

- **Wild: a tombstone page for unpredicted asks, grouped by class** — FEATURE — value 2 — effort S — risk low — category: site
  Why: wild. Each "what earlier brainstorms missed" entry becomes a labelled tombstone ("satellite: validation", "satellite: seal"). Classes with more than two tombstones trigger a standing question in every later brainstorm.
  Done when: the page renders the grouped entries from the brainstorm ledger, and a class with 3 entries adds a line to the next pack.

Next question: Which satellites would Initiative need that Genesis never had, such as consent per repo, a spend cap, or an owner check, because it acts on repos the user didn't ask about?
Next question: Does the exam grade a pipeline stage (find, prove, fix, rank) separately, so a regression can be blamed on the right stage?
