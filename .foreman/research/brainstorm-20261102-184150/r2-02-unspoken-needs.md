# Brainstorm — lens: unspoken needs

- **Index every moonshot verdict in one generated table** — FEATURE — value 4 — effort S — risk low — category: docs
  Why: T-2720, T-2721 and T-2724 each added a rule about where a kill result and its Sample line live, so the user keeps repairing the place where results sit. Nothing lets them read all of M-01..M-20 at once.
  Done when: `fm genesis moonshot index` prints one row per M-id with script, sample line, result, date and verdict, and a test fails if a `bench/moonshot` script has no row.

- **Print the tower's position as the first line of bare `fm`** — FEATURE — value 4 — effort S — risk low — category: orientation
  Why: the user types "Genesis gen-3 Mission 7 (#3 anticipation)" and "Mission 1 (gen 4, #2 …)" from memory each time. T-2722 shows `fm next` had no tower awareness until they pointed at it. Assumption: this is the line they look for first.
  Done when: with a tower open, `fm` prints `gen 4 · Mission 1/8 (#2) · briefs 0/N filed · next: …` and prints nothing extra with no tower open.

- **Backfill dissent scores for the gen-3 briefs from existing close-survival data** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the carried gap says dissents are scored against outcomes. An earlier question asks how many gen-3 briefs have a computable measure and how many are vacuous. `fm outcomes` already tracks 14-day close survival.
  Done when: `fm outcomes --dissents --gen 3` lists each dissent with scored, unscored or vacuous, and the vacuous count is printed.

- **Blame the brief line that licensed a user correction** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: most asks here are corrections of small things Foreman wrote (T-2691, T-2693, T-2738, T-2729), and none of them says which sentence of the original brief allowed the miss. Assumption: a zero-token token-overlap match between the correction and the brief's lines gets right most of the time.
  Done when: filing a correction-shaped ask prints "closest licensing line: <brief>:<n>", and a planted case in the test suite resolves to the right line.

- **Show a "not yet verified by anyone but me" count on every tower file** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the user's standing rules require cold reads and signals Foreman didn't author, yet a Mission page doesn't say which of its claims got one. Assumption: the cold-read verdict is already stored per file.
  Done when: each tower file's header shows `cold-read: pass by sonnet (haiku: fail)`, or `unread` in the warning style, and `fm genesis check` fails on a filed file with no verdict.

- **Record the approach number on every re-run task** — FEATURE — value 3 — effort S — risk low — category: ledger
  Why: the steers say a failed spike gets 2 or more different approaches, and T-2702's replacement said "approach 2". The ledger shows nothing linking attempt 1's failure to attempt 2, so a reader can't tell a retry from a new idea.
  Done when: a task filed with `--retry-of T-N` shows `approach 2 of ≥2` plus what changed, and `fm task show` lists the chain.

- **Warn at filing when a Done-when bundles a clause the filer cannot edit after a failing run** — FIX — value 3 — effort M — risk low — category: briefs
  Why: T-2702's drop reason says criterion 3 bundled the user-held deletion and can't be edited after a failing run. The cost showed up only after the run.
  Done when: filing a brief with a clause naming a user-held action prints "split before running", and a planted two-clause Done-when triggers it in a test.

- **Log which Mission-page section the user opens first, locally** — FEATURE — value 3 — effort S — risk low — category: web UI
  Why: an earlier question asks which cell they open first and whether the grid order matches. Nothing records it. The log stays on this machine.
  Done when: the web UI keeps a local open-order file and `fm web --order` suggests a section order from it, with no network request in the test.

- **Wild: Open each generation with a "letter from the last user message"** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the gen-4 seed is written from the tower's files, not from the user's latest words. A two-line quote of the user's last three asks, placed above the seed, would anchor the generation to what they just did.
  Done when: each seed starts with the three most recent asks, quoted whole, and a test fails if one is truncated.

- **Wild: Ghost-merge the unspoken: a weekly list of things the user did by hand that Foreman could have done** — FEATURE — value 4 — effort M — risk med — category: initiative
  Why: the asks are almost all "ship", "kill test X", "file the first 20" — repeated manual steps. Assumption: commits made outside `fm ship` are visible from git and the ledger.
  Done when: `fm hands` lists commits and commands run outside Foreman verbs this week, each with the verb that would have covered it or "no verb".

- **Wild: A "silence is not consent" sweep for carried gaps** — FEATURE — value 3 — effort M — risk low — category: Genesis
  Why: Mission 1's request carries three gaps in prose. Assumption: if the next Mission page never mentions a carried gap, the user wouldn't notice until much later.
  Done when: at Mission close, each carried gap shows closed, still open or silently dropped, and "silently dropped" fails `fm genesis check`.

- **Wild: Make the tower speak in the user's compression** — FEATURE — value 2 — effort M — risk med — category: language
  Why: the user's asks are short and dense ("Ship 3 commit(s) to main"), while Foreman's outputs are long. Assumption: a length budget per surface learned from what they paste back would fit better than one fixed cap.
  Done when: a finish card for a closed Genesis brief fits in the user's median ask length times 4, and the full text is one flag away.

Next question: which standing rule or steer has the user restated in their own words more than twice, and does an automatic check already enforce it?
Next question: of the corrections the user made in the last 30 days, how many were about Foreman's printed output disagreeing with itself, and which printer produced them?
