**Verdict:** approve with nits. I found no bypass of the guard lock, no guard rule change, and nothing dangerous or secret in the allow-corpus. The one real gap is that 'unable' stops at `drift()` and doesn't reach other consumers of `verdicts()`. I had no shell, so I ran no tests and could not recompute any hash.

## lens: adversary
- MEDIUM — plugin/lib/fmreplay.py:339-353 (`score`), :588 (`cmd_replay`), plugin/lib/fmfriction.py:68 — the 'unable' result only exists in `drift()`. Every other caller of `verdicts()` reads `error: X` as an ordinary verdict.
  - Scenario: `fm replay --candidate cand.py`, where the candidate's `check()` raises on every command. Each command comes back `error: …`, which `score` files under "tightened (new refusals)". `loosened` is empty, so it exits 0 with a clean report.
  - Plain `fm replay` calls an `allow` → `error:` flip "newly blocked (likely false positives)". `fmfriction` prints "still blocks".
  - The hook itself fails closed (fmhooks.py:1610), so this is a false clean rather than a bypass.
  - Fix: add a shared `unable(v)` helper and treat `error:` as its own bucket. In `score` it should exit 1, and the other two should report "unable".
  - Confidence: CONFIRMED by reading.
- LOW — plugin/lib/fmreplay.py:414 and :367 — `load_cases` returns `([], 0)` when the file is missing, so a deleted or emptied `guard_allow.jsonl` is silently skipped by the combined replay.
  - `record()` logs `cases >= 1`, and `safety_gate` (:499) only fails below 1. The ≥40 floor exists only in the unit test.
  - Fix: in default mode, count a missing or unreadable allow file as `broken`.
  - Confidence: high.
- LOW — plugin/lib/fmevolve.py:107, :110 and :137 — `git show HEAD:` and `git ls-tree HEAD` use symbolic HEAD, but the worktree is built from the earlier `head` SHA.
  - A commit landing in between could make the checked mode differ from the checked-out tree.
  - Fix: use `f"{head}:{target}"` and `ls-tree {head}`.
  - Confidence: medium.
- LOW — plugin/lib/fmevolve.py:31 — `GUARD` doesn't list the ratchet's own code (`fmreplay.py`, `fmevolve.py`, `fmbench.py`'s gate, `fmmutate.py`).
  - Redundant today, because the `TEXT` whitelist at :27 already rejects anything but md and routing.json.
  - Fix: add them, or comment that `TEXT` is the primary control.
  - Confidence: PLAUSIBLE.
- LOW — plugin/lib/fmreplay.py:406 — dedupe by id means that if the same id carries opposite labels in the two files, the second is silently dropped.

## Answers to the key questions
- **Path tricks:** `..`, `.` and `//` are handled by `normpath` plus the `..` check, and `re.I` covers case. A symlinked parent folder fails at `git show HEAD:path` ("isn't committed"). A hard link is a plain file in git, and the worktree is a fresh checkout, so nothing is shared. A different `--plugin-dir` can't reach guard files, because `GUARD` runs on the full target first and `TEXT` still applies.
- **Lock coverage:** `fmguard.py` has no `fm*` imports. `fmhooks.py`, `hooks/` (which includes the wrapper script and `hooks.json`), `test_guard*.py`, `guard_*` fixtures and `gen_evasions.py` are all covered. `fmcore`, `fmsettings` and `fmsetup` are unlocked but unreachable through `TEXT`.
- **Allow-corpus:** nothing should be refused. `tar -I zstd` and `NODE_OPTIONS=--max-old-space-size` are exact benign strings. I found no secrets and no `/home` or `chase` paths. Cwds are repo-relative.
- **'unable' propagation:** `drift()` is covered, so `report_cases`, `cmd_replay` (via `bad`), `record()` and the test suite all fail on it. The MEDIUM above lists where it isn't.
- **Guard rule changes:** none. The diff doesn't touch `fmguard.py`.

## Acceptance criteria
- Allow-corpus replays green: not verifiable without running it. The cases are plausible, and the test replays under both a temp home and this checkout.
- `fm evolve` refuses a guard path: met (fmevolve.py:99).
- An unrunnable check reports unable: met in `drift` and `report_cases`, partly elsewhere (see the MEDIUM).

## Implicit decisions
- The id-based dedupe across the two files; first file wins.
- Symlink mode is checked against git, not the filesystem.
- The allow-corpus is ignored whenever `FOREMAN_GUARD_CASES` is set.
- `error:` is treated as unable by string prefix.

## Not checked
- I ran no tests.
- Other writers of instruction files (`fminstr.py`).
- Whether every stored id equals `_key`.

**Noticed:**
- CHANGELOG.md has no T-1517 entry, though every neighbouring task has one.
- `guard_cases.jsonl:16` and `:33` (copied into the allow file) are the same command and cwd, `ssh host` in `.`, with different ids. At least one id isn't `_key(cmd, cwd)`, so the id-based contradiction check in `add_case` can miss it. Compare on (cmd, cwd) instead.
- No test covers a symlinked parent folder, a directory or a submodule as the evolve target.
