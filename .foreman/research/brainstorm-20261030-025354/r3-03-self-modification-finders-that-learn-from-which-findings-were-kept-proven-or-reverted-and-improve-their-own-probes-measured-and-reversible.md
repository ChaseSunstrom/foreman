# Brainstorm — lens: self-modification: finders that learn from which findings were kept, proven or reverted, and improve their own probes, measured and reversible

- **Replay every probe edit against the user's own finding history** — FEATURE — value 5 — effort M — risk low
  Why: the pack's exam gate is held-out and costs model runs, but the ledger of kept, reverted and dismissed findings already says what this user wants. Assumption: findings are stored with a repo snapshot or file hash.
  Done when: `fm probes try <edit>` prints "would re-file N reverted, would still catch M of K kept" without any model call, and a test shows an edit that re-files a reverted fixture is refused.

- **Pin every kept finding as a golden catch** — FEATURE — value 5 — effort M — risk low
  Why: Mission 3 is graded on `none` and `bug` in unseen repos, and a probe that learns to be quiet on `none` can silently stop catching bugs. Each kept finding's minimal vulnerable snippet becomes a permanent fixture, so edits can only add recall.
  Done when: a probe edit that stops catching any stored golden snippet fails `fm probes check`, naming the snippet.

- **Roll an edit back automatically when its precision drops (sequential test)** — SECURITY — value 4 — effort M — risk med
  Why: "measured and reversible" needs a trigger. Compare post-edit kept-rate against the pre-edit baseline with a sequential probability ratio test, so a bad edit is caught early without waiting for a fixed sample.
  Done when: in a simulated stream of 30 findings with a worse kept-rate, the edit is reverted by finding N or earlier, and the journal records the reversion with its statistic.

- **Blame the right stage before touching a probe** — FEATURE — value 4 — effort M — risk med
  Why: a reverted fix can be the finder's fault, the proof harness's (wrong failure reason), or the fixer's. Updating probes on every revert would teach them the wrong lesson. An autopsy step tags each revert with one of the three stages, and only finder-tagged ones feed probe learning.
  Done when: a fixture revert caused by a bad fix leaves probe weights unchanged, and a fixture revert caused by a false finding lowers its probe.

- **Require minimum evidence before any self-edit** — CLEAN — value 3 — effort S — risk low
  Why: with a handful of outcomes per probe, edits fit noise. Assumption: outcome counts per probe are small on a single user's repos. A power check sets the minimum number of outcomes before the proposer may run.
  Done when: `fm probes propose` on a probe with fewer than the threshold outcomes exits with "need N more outcomes" and spends zero tokens.

- **Measure a probe's value by switching it off for a night** — FEATURE — value 4 — effort M — risk low
  Why: yield-per-dollar from the ledger is correlational, because a probe may only duplicate another. A randomized ablation disables one probe per night and checks whether the morning card lost anything unique.
  Done when: after an ablation night the probe ledger shows "unique findings lost: 0" or a count, and probes with 0 over K nights are flagged for retirement.

- **Write down why a retired probe died** — FEATURE — value 3 — effort S — risk low
  Why: nothing in the pack stops the proposer from reinventing a probe that was already retired for noise. A short tombstone per retired probe records its pattern, reason and the ledger evidence, and the proposer reads the tombstones.
  Done when: a proposed edit whose pattern matches a tombstone is rejected with the tombstone's id and reason.

- **Express probes in a small declarative format so self-edits can't run code** — SECURITY — value 4 — effort L — risk med
  Why: the pack warns that finding prose is tainted and that Foreman's own probes can misfile. A self-editing system that writes executable code is a larger attack surface than one that edits pattern, scope and proof-template data checked by a schema.
  Done when: a probe file containing anything outside the schema fails validation, and the proposer's output is always a data diff.

- **Scrub learned patterns of project literals before they cross repos** — SECURITY — value 4 — effort M — risk low
  Why: a probe distilled from project A may embed identifiers, paths or secrets. Transfer to project B then leaks A's data into B's prompts and logs. Assumption: cross-project probe sharing is wanted, since users run Foreman on several repos.
  Done when: a probe mined from a fixture containing a fake API key and a private hostname carries neither string after export, and a test greps the exported file for them.

- **Interleave two rankings on the morning card and learn from the picks** — FEATURE — value 3 — effort M — risk low
  Why: calibrating rank weights offline is slow. Team-draft interleaving of the live ranking and a candidate ranking shows which one the user accepts more, using the one-key land-or-drop signal.
  Done when: after M card decisions, `fm find rank` reports a winner with a win count, and the losing ranking is discarded without a user prompt.

- **Wild: Draw the probe family tree on the Genesis page** — FEATURE — value 3 — effort M — risk low
  Why: wild. Genesis already exports a live tower graph to the site. A matching tree of probe ancestry shows each probe's parent, fitness and fate, so self-modification can be audited at a glance.
  Done when: the exported page has a probes view where clicking a node shows its edit diff and its before and after precision.

- **Wild: Run a probe dojo against the failure museum overnight** — FEATURE — value 3 — effort L — risk med
  Why: wild. Candidate probe mutations fight on a scratch copy seeded with past failures and planted canaries. Only winners surface as proposals, and the real repo is never touched.
  Done when: a morning note lists the mutations tried, their scores on the museum, and the one proposed edit, with the working tree unchanged.

- **Wild: Make probes stake a budget on their own findings** — FEATURE — value 2 — effort M — risk low
  Why: wild. Each probe carries a small credit balance that rises with kept findings and falls with reverts. A probe at zero credit goes to shadow mode, which gives self-modification a plain, legible currency.
  Done when: `fm probes` shows a balance column, and a probe reaching zero is shadow-run and stops filing to the card.

Next question: Does the user's keep, drop and revert behavior reflect finding quality, or just their mood and timing, and can the ledger tell the two apart?
Next question: What stops a self-edited probe set from slowly drifting away from the sealed charter and the genesis drift check?
