## Verdict
Changes needed. The lint logic is sound and the AC-named test looks right. One MEDIUM finding is on the card-admission path. I had no shell, so I ran no tests and did not run `fm lib check`.

## lens: intent
- LOW — plugin/lib/fmlib.py:339 — `_npx_names(text)` scans the whole card (body, Test first, Review), but the changelog and the AC say "a card's Verify". A prose mention like "scaffold with `npx create-foo`" in another section now fails the lint, and the message never says the hit is outside Verify. — Pass `verify.group(1)` when Verify exists, or reword the changelog to "any backticked npx in a card". — 70%

## lens: adversary
- MEDIUM — plugin/lib/fmlib.py:282 — `admit_problems` (fmlib.py:244-251) lints a draft inside `tempfile.TemporaryDirectory()`. So `lint_card` sees `cards_root=/tmp/tmpXXXX`, and `_npx_known` reads `os.path.dirname(cards_root)/npx-known.txt`, which is `/tmp/npx-known.txt`. A world-writable directory can therefore replace the reviewed list. Because the first file found wins outright, there is no merge with the shipped list. Reproducer: `echo evil-pkg > /tmp/npx-known.txt`, then `fm lib admit` a staged card whose Verify runs `npx evil-pkg`. The card is admitted. An empty or stray file does the opposite and flags every npx name. The real destination (`--into`, fmlib.py:1265) never has its neighbouring list consulted. — Look beside the root only when `os.path.basename(cards_root) == "cards"` (the test fixture and shipped layout both satisfy this, the temp dir doesn't). Alternatively give `admit_problems` an explicit list root. — 85%
- LOW — plugin/lib/fmlib.py:284 — Only `OSError` is caught. A non-UTF-8 `npx-known.txt` raises `UnicodeDecodeError`, which crashes `fm lib check` and the write hook. — Catch `(OSError, ValueError)`. — 60%

## lens: edge
- LOW — plugin/lib/fmlib.py:296-306 — These forms produce a false "unknown name": `npx vitest;` (trailing punctuation), a backslash-continued `npx \` (name becomes `\`), and a value-taking flag such as `npx --registry URL pkg` (the URL becomes the name). They are rare, and a flag-form value is not consumed. — Strip `;|&\` from the name and skip words containing `://`, or accept the ceiling with a `ponytail:` comment. — 55%

## lens: operator
No new always-on cost. `functools.cache` bounds the list read to once per distinct root. Cost: about 300 cards × one small file read per lint, which is negligible.

## lens: maintainer
- LOW — plugin/tests/test_library.py:75 — The test covers `--yes`, `--package X`, `--package=X`, `@latest` and the beside-list override. It does not cover `-p NAME` or the admit-in-temp-dir path (the MEDIUM above), so nothing fails if the admit path reads `/tmp`. — Add an assertion that `admit_problems` ignores a `npx-known.txt` in the system tmp, with `TMPDIR` pointed at a scratch dir containing one. — 70%

## Acceptance criteria
- Unknown npx name is a card problem naming npx-known.txt: met by the code path (fmlib.py:339-340) and the new test. I did not run it.
- Every shipped card passes `fm lib check`: not verifiable from the code. I could not run it, and 852 npx occurrences across 329 cards are too many to cross-check by hand.

## Implicit decisions
- The list holds bin names alongside package names (`cap`, `biome`, `ng`, `lhci`). The header says "or a project's own bin". The lint therefore cannot catch a bin whose same-named npm package is unrelated.
- The list beside the cards replaces the shipped list rather than extending it.
- Only the first non-flag word after `npx` is checked, so `-p a -p b` checks only `a`.
- The scope is `npx` only. `pnpm dlx`, `bunx` and `npm exec` are not checked.
- Output is capped at 3 names per card.
- Files in the diff that no step names: CHANGELOG.md, fmlib.py and test_library.py. The plan's step list is missing them.

## Not checked
- Running the tests or `fm lib check`.
- Whether each list name exists on npm. The header says it was checked on 2026-10-29.

Noticed: none
