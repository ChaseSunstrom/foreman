# Brainstorm pass 6 (2026-10-04) — confirming probe: dry

Source: research/brainstorm-20261004-034835 (performance: time and tokens per finished task; unspoken needs × 2 rounds, past passes 2–5; 43 new titles).

## Grounded and kept
None that isn't built or already planned.

## Grounded and dropped
- Overlap the review with the next task / park the batch / fast and slow review lanes / pre-warm the next brief — the same need as passes 4 and 5: T-0234 (lanes) is where it lands; it goes first in the inbox.
- Cache verdicts by tree hash and command, memoize gates by file content — exists (fm check reuses a pass on the same tree).
- Run only the tests the diff reaches, impacted tests per step — exists (fm check --affected).
- Order child packs for prompt-cache reuse, prefix-stable packs — built in pass 1.
- Diff-scoped reviewer packet — exists (fm audit prep's brief and diff snapshot).
- Time and token cost per ceremony step, ceremony time per task — fm cost and the ledger cover it; no decision would change.
- Ship `fm guard check`, patterns in a data file — built in pass 5 (fm replay --cmd; doc files skipped).
- Stranger-test the README — T-0244. Export lessons as a skill pack — fm export agents.
- Re-review deltas, skip unchanged lenses — re-reviews are rare; nothing to save.
- Reviewer model by risk, cheap-to-strong escalation — trades review quality for tokens the budget already caps; the user asked for quality.
- Resident hook daemon — hook p95 is 33 ms.
- Research source track records, saturation stops, ranking the inbox by re-asks — small gains on features that already work.

## Yield
0 new grounded ideas: dry. With pass 5 (2), two consecutive probes agree. The loop stops (fm decide); the planned inbox is finished next, lanes first.
