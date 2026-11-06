Verdict: changes needed (2 MEDIUM intent/edge, 1 MEDIUM edge, 4 LOW); reviewer ran nothing (read-only).

## lens: intent
- MEDIUM — the exception "fail a line doing what an earlier read asked only on a gen-0/steer/intent breach" left out metric gaming, narrowing what the reader may fail. FIXED: "or games a metric" added.
- LOW — no writer's answer channel. Kept: the revised file is the answer (CHANGELOG says so); an --answer flag would be untrusted text for no gain.

## lens: adversary
- LOW — the data-not-instructions sentence didn't name the previous reads. FIXED.

## lens: edge
- MEDIUM — reads loaded before the 120 s read and written whole after: a concurrent put of another file lost its findings. FIXED: reloaded just before the write, merging only this file's entry.
- MEDIUM — stray findings (quotes the file doesn't hold) were carried with no line to re-check, working against convergence. FIXED: only held findings are kept; test asserts a stray isn't carried.
- LOW — no dedupe: one stubborn line filled the 40 slots. FIXED: one entry per line, newest why (tested).

## lens: operator
- ok: one small JSON per project, prompt bounded at 40 entries, no hook or loop.

## lens: maintainer
- LOW — test asserted a string constant. FIXED: dropped. Concurrency and corrupt-file fallbacks untested (reload and the except branch are one line each).

Noticed: nothing measures whether carried findings cut the rounds; the genesis_read ledger events per name already give the round count, so the next long filing (T-2182's mission-genesis.md) is the before/after.
