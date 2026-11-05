# UI card examples: the first live run (T-3102)

`sampo playbooks small examples --grid ui --max-calls 12`, writer local (jarvis), 2026-11-05.

| | count |
|---|---|
| calls | 12 (jarvis-nothink 11, jarvis 1) |
| kept | 9 |
| rejected | 3 |

Why each rejected one failed, as recorded in the store's `examples.jsonl`:

- K-001901 overflow: 446 px wide, its widest box 364 px (bar ≤ 390 px)
- K-001903 contrast: 1.03:1 (bar 4.5:1 in both themes): its text vanished in one theme
- K-001906 height: 872 px tall (bar ≤ 800 px)

None was rejected for size or safety: given the frame's tokens and a kit demo of the same component, the local model
writes static, token-coloured markup. Kept examples read as real product UI: scan results, Lighthouse gates, test
runs, tab panels. One kept example (K-001897) scrolls its code block sideways inside its own box, which the overflow
gate allows, because the page itself stays 390 px wide.

A second run (`--max-calls 4`, the step's recorded evidence) kept 4 of 4, so the total is 13 kept and 3 rejected out of
16 calls (81%).

At 75 to 80% kept, the 3,137 UI cards need about 4,200 calls. Each card gets three tries (TRIES), so a card that keeps
failing falls back to its component's kit demo.
