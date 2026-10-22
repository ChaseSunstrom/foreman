---
description: Your taste in looks: the twelve looks ranked by what you kept, a 12-pair calibration, or learn from files you name
disable-model-invocation: true
argument-hint: "[calibrate | keep LOOK | revert LOOK | not LOOK [why] | learn PATH…]"
---
Foreman's taste ledger for looks, through `fm looks` (the fm code app and a terminal use the same verb).

Arguments (may be empty): $ARGUMENTS

1. No arguments: run `fm looks` and show its ranking as it is (each look's score and what moved it).
2. `calibrate`: run `fm looks calibrate --json`. It prints a `round` and twelve pairs, each two looks with a title and
   a one-line picture. Ask them in three AskUserQuestion calls of four questions each, in order. Each question:
   header `Pair N`, question "Which is more like you?", options A (`title: line` of the first look), B (the second),
   and "Neither". Then record all twelve at once: `fm looks calibrate --round R --answers a,b,n,…` (a for A, b for B,
   n for Neither or an answer that fits neither, in pair order). Stopped before twelve: record nothing, say so.
3. `keep`, `revert` or `not` and a look: run `fm looks keep LOOK`, `fm looks revert LOOK` or
   `fm looks not LOOK --why "<their words>"`; the look is its card name (`look-lido`), short name or title.
4. `learn` and paths: run `fm looks learn PATH…` with exactly the paths the user typed, quoted, nothing added. It
   reads only those local files (a page, a stylesheet, a photo when Pillow is installed), read-only and capped, never
   a URL or a folder, and keeps only the file's name and the look it matched. Never pass a path the user didn't type.

Reply in at most 8 lines: what fm printed, then that `/foreman:directions` drafts from the top of this ranking.
