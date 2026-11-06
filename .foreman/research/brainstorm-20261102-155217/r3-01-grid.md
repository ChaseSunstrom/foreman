# Brainstorm — lens: grid

Grid used: surfaces (CLI, hooks/SessionStart, foreman-ui pane, web UI, Genesis site, unattended drive/tick) × actors (user, agent, other lanes, unattended run) × failures (missing, wrong, slow, unsafe, unclear). Each idea names its cell.

- **Prove a prefetched verb is read-only** — SECURITY — value 4 — effort S — risk low — category: anticipation safety
  Why: cell hooks × unattended × unsafe. The pack lists "prefetch read-only verb output from verb-transition counts", but nothing proves a prefetched verb leaves state untouched.
  Done when: a test runs every prefetch-eligible verb and fails if the tree hash or any ledger line count changes; a planted writing verb makes it fail.

- **Tag each predicted next command with the guard's verdict** — FEATURE — value 4 — effort S — risk low — category: guard, anticipation
  Why: cell CLI × user × unsafe. A "you usually run X next" line could suggest something `fmguard.check` would block.
  Done when: a card line for a command the guard blocks shows "guard: would block" and is never offered as a one-key run.

- **Record whether the anticipation card reached the agent** — FIX — value 4 — effort M — risk low — category: delivery receipts
  Why: cell SessionStart × agent × missing. The burden fix (T-2667) shows SessionStart text can be dropped or miscounted. Assumption: the card is capped like other injections.
  Done when: each session ledger row has `anticipation_delivered` with a char count read from the transcript's hook_success record; a capped-out card is logged as dropped.

- **Hold a quota floor for the user's habitual first hour** — FEATURE — value 4 — effort M — risk med — category: unattended spend
  Why: cell unattended × user × slow. Overnight speculative drafts can burn the window so the user hits a limit at their first prompt. The pack has "spend idle usage" ideas but no floor.
  Done when: with a floor set to 30% and the user's median start time known, a simulated run stops speculating once the remaining window falls to 30%, and the receipt says so.

- **Stamp speculative drafts with their file-set hash** — FIX — value 3 — effort S — risk low — category: lanes
  Why: cell other lanes × agent × wrong. A pre-drafted answer goes stale once the user or another lane edits the same files.
  Done when: editing a file in a draft's set marks the draft "stale" in `fm next`, and it is not offered or merged.

- **Score the Genesis site's hit rate on user-authored asks only** — FIX — value 4 — effort S — risk low — category: measurement
  Why: cell site × user × wrong. The asks list is dominated by slate-origin items ("asked: FEATURE: … (c13…)"), so a published hit rate would be circular. T-2554 covers input authorship but not this publisher.
  Done when: `fm genesis live` output excludes slate-origin asks from the anticipation score and states the denominator.

- **Gauge card age at the user's first keystroke** — PERFORMANCE — value 3 — effort S — risk low — category: latency
  Why: cell pane × user × slow. A card computed at Stop is useless if it lands after the user types.
  Done when: a ledger field records the delay from card ready to first prompt, and `fm doctor` warns when its p90 is over a bar.

- **Name overnight drafts as drafted, landed or discarded on the morning card** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: cell unattended × user × unclear. This feeds the question about what the user sees after a silent failure. Assumption: drafts and landings are currently counted together.
  Done when: the card shows three counts that sum to the number of overnight items, and the totals reconcile with the ledger.

- **Reserve a "who was I predicting for" tag on lane hand-backs** — FEATURE — value 3 — effort M — risk low — category: lanes
  Why: cell other lanes × agent × missing. A lane that works ahead has no recorded link to the predicted ask that justified it, so waste can't be priced.
  Done when: every speculative lane carries a `for_prediction` id, and the receipt gives the waste rate per predictor.

- **Wild: let `fm ?` answer with the one thing Foreman expects you to ask** — FEATURE — value 3 — effort S — risk low — category: delight, anticipation
  Why: cell CLI × user × missing. Wild, assumption: the user would like to peek at the guess. Each use books a sealed prediction scored later.
  Done when: running `fm ?` prints one line with its evidence and writes a prediction row that gets settled by the next real ask.

- **Wild: have a cold child read only the morning card and say what happened overnight, then diff it against the ledger** — FEATURE — value 4 — effort M — risk low — category: legibility exam
  Why: cell unattended × user × unclear. A card a stranger misreads is unclear to the user too.
  Done when: an exam scores the child's account against ledger facts, and a score below the bar fails the card's wording.

- **Wild: write a "why I was wrong" line when a confident prediction misses** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: cell pane × user × wrong. Assumption: a miss on a high-confidence prediction is the richest data point. The line cites the ledger rows that misled the predictor.
  Done when: a miss above the confidence bar appends a cited cause, and the predictor's next table update reads it.

- **Test the anticipation card across ledger gaps and a clock jump** — FIX — value 3 — effort S — risk low — category: robustness
  Why: cell hooks × agent × wrong, tied to the earlier question about unattended paths running while the machine slept. T-2645 added `c.clock()` for windowed readers but not for the predictor.
  Done when: with FOREMAN_NOW set past a 3-day ledger gap, the card says "not enough recent data" instead of repeating old patterns.

Empty cells and why:
- **Web UI × any × slow:** an existing idea already covers a render budget at 10k tasks.
- **Site × agent:** agents don't read the Genesis site.
- **Other lanes × unsafe:** covered by the capability-token and file-intent ideas.
- **All "missing" cells for the user on the CLI:** covered by the honest "can't read you this week" idea.

Next question: which anticipation outputs would the user act on within a minute, and does any ledger field already record that reaction?
Next question: what do lanes and unattended runs do with a prediction the user later contradicts, and who cleans up work done for it?
