# Brainstorm — lens: usage efficiency

- **Price output tokens at their real rate when planning fan-out** — FEATURE — value 3 — effort S — risk low — category: cost model
  Why: assumption: output tokens bill at a higher rate than input, so a 900-word child costs more than its input size suggests, and `fm cost` sums both into one figure. Fan-out is planned on the sum.
  Done when: `fm cost` reports input and output tokens separately, and the lens plan prices output at the configured rate and shows the total.

- **Pack the context to a token budget by value per token** — FEATURE — value 4 — effort M — risk low — category: context packing
  Why: the pack is all-or-nothing today. It repeats "The user's own words" and lists about 50 open-work rows verbatim, so the cheapest sections to cut are never the first cut.
  Done when: building a pack with budget B yields ≤ B tokens, drops the lowest value-per-token sections first, and logs each drop with its token count.

- **Skip the model call when the tree and failure are unchanged** — FEATURE — value 4 — effort S — risk low — category: retry cost
  Why: a retry after an identical failure re-sends the full pack and gets the same answer. The tree hash and the failure fingerprint are both already available.
  Done when: a second attempt with the same tree hash and fingerprint makes zero model calls and says why it stopped.

- **Step down through a brownout ladder before the spend cap** — FEATURE — value 4 — effort M — risk low — category: budget governance
  Why: assumption: the user wants the work to continue, not stop. Current behaviour is a hard pause at the cap. The ladder would cut lens count, then context size, then the hostile review, then pause.
  Done when: at 80%, 90% and 97% of budget each rung applies in order, and the glance line names the active rung.

- **Cap each child's output from its lens's measured p90 length** — PERFORMANCE — value 3 — effort S — risk med — category: output size
  Why: children are asked for up to 900 words, and their real length is in the journal. A fixed cap wastes output on the lenses that run short.
  Done when: a child cut off mid-table is detected by its missing end marker, only that lens reruns, and the cap for the next round tracks the observed p90.

- **Send session start only the backlog rows that changed** — PERFORMANCE — value 3 — effort S — risk low — category: session start
  Why: session start re-reads the whole open-work list each time, though most rows haven't moved since the last session. The journal already has the row hashes.
  Done when: a session start after no backlog change injects under 200 tokens of backlog text, and a changed row appears in the next start.

- **Compact an idle session on a timer so the next turn starts small** — PERFORMANCE — value 3 — effort M — risk med — category: context size
  Why: compaction currently fires mid-work at 200k. Compacting during idle time means the first resumed turn doesn't pay for the full window.
  Done when: a session idle past the timer resumes with its first turn under 20k input tokens and no lost acceptance criteria.

- **Wild: keep the prompt cache warm with a tiny timed ping** — FEATURE — value 3 — effort M — risk med — category: cache keepalive
  Why: wild; assumption: the cache TTL is short, so a long gap makes the next turn re-write a large prefix at full price. A small keepalive could cost less than one cold write, and `fm cost` would show the trade.
  Done when: the first turn after a 10-minute gap reads at least 90% of its prefix from cache, and the keepalive's own cost appears in `fm cost`.

- **Wild: trailer every commit with tokens spent per changed line** — FEATURE — value 2 — effort S — risk low — category: attribution
  Why: wild; efficiency is invisible in git history today, so a costly change looks the same as a cheap one. A trailer makes it searchable.
  Done when: each closed task's commit carries a `Foreman-Cost:` trailer, and `git log --grep` finds it.

- **Wild: run one week on a half-size pack as a context diet** — EXPERIMENT — value 2 — effort M — risk med — category: context experiment
  Why: wild; assumption: most of the pack is redundant, but nobody has measured by how much. One week at half size, with the held-rate compared against baseline, would give a number instead of a guess.
  Done when: the diet week's report shows the held-rate and spend beside the prior week, and the user decides from it whether to keep the smaller pack.
