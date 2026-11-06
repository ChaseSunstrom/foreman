## Verdict
Changes needed. One HIGH: a script that runs a second script drops the new finding before it reaches the caller.

## lens: adversary
- HIGH — plugin/lib/fmguard.py:4072-4077 — The new finding ("… nested too deep to read in full)") contains "too deep". When it comes back from a nested script to the outer `_check_script`, it hits the `elif "too deep" in f[1]` branch. With `len(_IN_SCRIPT) < 3` that branch sets `deep=True` and `continue`s, so the finding is dropped. The re-scan at 4087 covers only the outer chunk, which holds `bash b.sh` and no `rm`. — Pass findings that end in `nested too deep to read in full)` straight through, the way line 4070 passes "script nests too deep to read", before the `elif "too deep"` test. Then add a test for the chain. — confidence: high from reading the code. I had no shell, so I did not run it.
  - Path: the hook runs `bash a.sh`, and `_script_verdict(a)` pushes `_IN_SCRIPT`, which is now length 1. a.sh holds `bash b.sh`. `_script_verdict(b)` pushes it to length 2, so b's `_check_script` takes the `<3` branch and emits the new finding.
  - `_script_verdict` returns it unchanged (4462-4463, call site 3553). Back in a's `_check_script` the length is 1, so the finding is dropped.
  - Input: b.sh is `bash -c '…bash -c "rm -rf ~"…'`, nested 3 to 5 layers, and a.sh is `bash b.sh`. The result is no refusal.
  - A wrapper script defeats the acceptance criterion's guarantee. A two-script chain also needs fewer layers, because each script level uses up one depth.

- LOW — plugin/lib/fmguard.py:4086 — The re-scan covers literals only. It misses `rm -rf /abs/foreman/path`, core writes and `$VAR` targets. The ponytail comment says so, and the old code dropped these too, so this is not a regression. — Leave as is. — confidence: high

## lens: intent
- LOW — plugin/tests/test_guard_exec_vectors.py:458-459 — The criterion says "no grant lifts it". The test checks only that the message says "no grant lifts". It never runs `self.bash(..., allow=("system",))` or an `rm-outside` allow to show a grant fails to lift it. — Add `allow=("system", "rm-outside")` and assert it is still blocked. — confidence: medium

## lens: maintainer
- MEDIUM — plugin/tests/test_guard_exec_vectors.py:449-460 — Only a single-script case is tested. It cannot catch the HIGH above. — Add `a.sh` containing `bash b.sh`, with the deep `rm -rf ~` in b.sh, and assert a block. — confidence: high
- LOW — plugin/lib/fmguard.py:236-239, 192-193 — The "unreadable program" suffix list is now repeated in `_unread`, `_hint` and the producer at 4088. This is the same drift risk T-1932 noted. — Define one `_DEEP_TAIL` constant. — confidence: medium
- LOW — plugin/lib/fmguard.py:193 — The line is about 130 characters, against about 120 elsewhere. No lint config was found. — Wrap it. — confidence: low

## lens: edge
- Cost is a regex pass over one chunk (about 2 KB) and only when `deep` is set. It does not scale with calls or sessions.
- The cached verdict now carries the new finding string, so a cache hit behaves the same.
- Nothing else to report.

## lens: operator
- CHANGELOG.md line 4 already has the T-1931 entry. Nothing else to report.

## Acceptance criteria
- `rm -rf ~` under 5 `bash -c` or `eval` layers inside a script is refused as system and no grant lifts it: met for a single script. The code path is 4087-4089 → `_unread` at 238 → `unliftable`, and the test asserts it. Not met when the script is run from another script (the HIGH above).
- The same nesting around `date` passes: met. The test asserts `assertIsNone`. I did not run the suite, because I had no shell.

## Implicit decisions
- The new finding is category `system`, with a suffix string used to classify it, not a dedicated category. The same substring approach was already noted in T-1929.
- The scan covers the whole chunk, not only the over-deep part.
- `line[:80]` is used for the detail, matching the too-long path.

## Not checked
I did not run the tests or the timing. I did not check the interaction with `_UNREAD` or the cache invalidation.

**Noticed:** The `"too deep" in f[1]` substring test at 4072 and 4080 also matches `("rm-outside", "command nesting too deep to analyse…")`. That is the finding the new code replaces. Any future "too deep" wording will be swallowed the same way, so match the exact strings.
