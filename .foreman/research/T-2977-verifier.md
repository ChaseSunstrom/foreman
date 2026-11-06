# T-2977: a close-holds verifier, first live numbers (2026-11-04)

## What it learns from
The training lake's outcome labels: held vs. fixed-later or reverted. Settling rows are dropped.

The features are text-free:
- distinct evidence commands;
- red-then-green proofs;
- tests run, passed and failed, parsed only from the output of commands Sampo ran;
- distinct lenses and audits;
- scope size;
- minutes active;
- tier and type.

There is no Claude-written text anywhere, per the recorded decision.

## Live run
`sampo exam models --verifier` over 590 labelled closes from this machine's projects, with each project held out in turn.

| Held-out project | Closes | AUC |
|---|---|---|
| largest (this repo) | 266 | 0.733 |
| second | 202 | 0.529 |
| third | 52 | 0.412 |
| two small ones | 4, 66 | too few of one class |
| **pooled** | **590** | **0.555** |

- At 10% false alarms it catches 22.8% of the closes that later needed a fix or a revert.
- The base rate of such closes is 15.6%.

## Reading
- **Weak signal overall.** It is real on the project with the most history (0.73) and absent elsewhere. Coarse counts don't transfer across projects well.
- **It stays in shadow.** `sampo task finish` logs a `close_score` only, and T-2976's floor would not adopt it (no project may regress).

## Next levers
- **Test-graded exam closes.** Louhi's exam closes add negatives graded by tests: a false-done is "closed and red", which is exactly what this verifier must catch, and exp 2 had 4 of gemma's 5 closes false-done.
- **Diff-size features.** Per-task diff size from git, once the lake carries it.
- **Re-measure each Rune generation** as the labels settle: 2,104 rows are still settling.
