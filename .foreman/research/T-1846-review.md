**Verdict: changes needed.** The adversary question you asked has a clean answer. The resource-exhaustion and error-handling findings below are real, and I did not run any of them.

## lens: adversary

**Source text cannot reach the generated code, and the generated code cannot leave RUNTIME.**
- Tokens are ASCII-only (`re.ASCII`, `fmshade.py:17`). User names are mangled with fixed prefixes (`l_ u_ g_ a_ f_`, e.g. `:249`, `:279`, `:328`).
- Literals are re-emitted through `lit()` (`:54`) after `float()` or `int()`. Swizzle indices are int tuples. The only other text is fixed strings: `t[1].title()` on true/false, `_o_{base}_{OPN[op]}` and `_b_{fn}`.
- Comments, preprocessor lines and card markdown are dropped. Error messages echo only token text (ASCII ids, numbers, ops) or `repr()` of a character, so no escape sequences reach the terminal.
- The generated grammar has no attribute access, string literal or arbitrary subscript. `__builtins__` is `{}`. I found no escape.

- MEDIUM — `fmshade.py:264-267` — `precision`/`layout` skipping loops forever at end of input. `take()` advances `i` past the end while `peek()` stays clamped on the `end` token, so `eat(";")` or `eat(")")` never matches. Input: a file containing only `precision highp float` (no `;` after it), or `layout(location=0` with no `)` after it. This is a 100% CPU hang with no error. — Fix: `if self.peek()[0]=="end": self.fail(...)` inside both loops. — high
- MEDIUM — `fmshade.py:440,671-673` — only loops tick the budget, so user-function calls are free. `f1(x){return f0(x)+f0(x);} … f40` gives 2^40 calls per pixel with no loop and no `ShadeError`. — Fix: emit `_tick(line)` first in every non-entry function body. — high
- MEDIUM — `fmshade.py:12,826` — `LIMIT` is reset per pixel (`budget[0]=0`). Worst case is 100000 ticks × 512×512 pixels, doubled when a derivative adds a second pass. Nothing bounds the whole render. — Fix: a render-wide tick budget or a wall-clock deadline checked in `_tick`. — high
- MEDIUM — `fmshade.py:798-800,832` — `_d` stores one `vals[(site,n)]` entry per call, and `seen` keeps every pixel's dict. `for(int i=0;i<1000;i++) x+=dFdx(uv.x);` gives about 1.6e7 entries at the default 160x100 and about 2.6e8 at 512x512, so likely out of memory. — Fix: raise `ShadeError` past about 64 derivative calls per pixel, or refuse derivatives inside loops. — high
- LOW — `fmshade.py:13` — an unterminated `/*` is lexed as `/` then `*`, and each further `/*` rescans to end of input, so tokenizing is O(n²). Hostile input is a file of repeated `/* ` with no `*/`. — Fix: if `src.startswith("/*", pos)` after a failed match, raise `ShadeError("unterminated comment")`. — medium

## lens: edge

- MEDIUM — `fmscene.py:1538,1539` — `--out` is not checked against FILE, unlike `_write_out` (`:1463`). `fm scene shade card.md --out card.md` replaces the card with PNG bytes through `os.replace`. — Fix: add the same `samefile` guard. — high
- LOW — `fmscene.py:1539` — only OSError and ValueError are caught, so these crash with a traceback instead of a line message:
  - `((` repeated about 250 times raises `RecursionError` in the compiler.
  - `const float k = 1.0/0.0;` raises `ZeroDivisionError` at the global `exec` (`:817`).
  - 200 chained `+` raise `SyntaxError` ("too many nested parentheses") from `compile`.
  - `--set n=inf` on an int uniform raises `OverflowError` (`:758`).
  Fix: in `render`, convert `(SyntaxError, RecursionError, ArithmeticError, TypeError, MemoryError)` to `ShadeError`. — high
- LOW — `fmshade.py:181` — a line starting with `#` inside a `/* */` block raises "#word is outside the subset". Fix: strip comments before the preprocessor scan. — medium

## lens: maintainer

- LOW — `plugin/tests/test_shade.py` — no test covers the `LIMIT` loop abort, the sandbox, or any of the hangs above. Add one per fix.

## Acceptance criteria

- **PNG, uv gradient, iTime, swizzles, built-ins:** not verifiable here. The tests exist (`test_shade.py:25-69`), but I have no shell and did not run them.
- **Refuses what's outside the subset, naming the line:** met for the cases tested (`:89-105`). The hang and crash paths above are the exceptions.

## Implicit decisions

- Preview uniform values come from a hard-coded `PREVIEW` table.
- A pixel that divides by zero or overflows is drawn black and counted, where a GPU would give inf or NaN.
- `--size` is capped at 512×512 and defaults to 160x100.
- A card's first glsl block without `gl_Position` is the fragment shader.
- `exec` is used with an empty-builtins namespace as the sandbox.

## Not checked

Test execution, the rest of the diff (CHANGELOG, MASTER.md and the `fmcli` argparse beyond lines 6713-6745), and the intent and operator lenses beyond the cost lines above.

**Noticed:** none
