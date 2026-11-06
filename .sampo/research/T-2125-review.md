**Verdict:** approve with nits. I found no HIGH issues. There are three MEDIUM design gaps worth fixing or capturing, plus some LOW nits. I did not run `python3 plugin/tests/run.py test_find`; everything below comes from reading the diff and the code it calls.

## lens: intent
- MEDIUM — plugin/lib/fmfind.py:116,184-190 — "Abstain below a threshold" is only half done. A muted or below-bar lead is still listed and counted in "N candidate(s)", and it still makes the exit status 1. Only `--capture` skips it. — With `--rank`, drop held leads from the exit status, or print them under a separate "held back" line. Alternatively, record in the CHANGELOG that abstain means "unfiled". — confidence 70%
- LOW — plugin/lib/fmfind.py:99,107 — The requested formula `severity x proof x reach / effort` has proof and effort fixed at 1. The `ponytail:` comment and MASTER.md say so. `"bug"` also has no producer among the finders, so the AC's "a bug" is only tested with a hand-made lead (test_find.py:217). — Fine as a stated ceiling; capture it as a follow-up. — confidence 85%
- LOW — plugin/lib/fmfind.py:145 — `--capture N` files the top N *new* leads, because already-seen keys are skipped before `len(made)` counts. A daily `--capture 3` therefore walks down the list. The help text says "top N". — Reword the help text, or count seen leads toward N. — confidence 75%

## lens: adversary
- MEDIUM — plugin/lib/fmfind.py:144 — The dedupe key is `finder:file:symbol`, with no line or message. `secrets` has an empty symbol, so every credential in one file shares one key. `sql` and `slow` leads share a key per function. Reproducer: file two leaks or two sql leads in one function, and only the first is captured. Because `seen` includes the archive, a regression after the first task is done is never filed either. — Add the line to the key, or add a hash of `says`. — confidence 85%
- Checked and fine: `what` goes through `c.plain`, so a tree-controlled newline cannot break out of the `> ` quote (fmfind.py:147,150). Trees outside the project, or a parent of it, get `confirm` and `confirm_why` (fmfind.py:152). `commonpath` over two realpaths is safe.

## lens: edge
- LOW — plugin/lib/fmfind.py:168-172 — `--capture 0` is falsy, so it silently does nothing and does not even rank. `--capture -1` prints "Filed 0 task(s): none new". — Reject `N < 1` with a `UsageError`. — confidence 90%
- LOW — plugin/lib/fmfind.py:175-178 — `precision(p)` runs inside the scan `try`. A corrupt brief or a `git log` failure prints "the scan failed under <root>" and exits 2, which blames the scan. — Move `precision` out of the try, or name it in the message. — confidence 60%

## lens: operator
- MEDIUM — plugin/lib/fmfind.py:116,134-160 — A mute is permanent. `capture` never files a muted finder's leads, and `precision` only counts closed tasks tagged with the finder. After 7 drops, `untested` sits at 0.294 with no way back. Nothing is filed, so nothing can be marked done, and there is no decay, unmute verb or probe lead. A dropped task also counts as a false alarm even when the user simply declined to look, for example a declined outside-tree confirm. — Let one lead from a muted finder through per run (an exploration slot), or weight old outcomes down. Document the ratchet. — confidence 80%
- LOW — plugin/lib/fmfind.py:124-126 — `fmoutcomes.outcomes(p)` loads every brief with the archive, then runs `git log -n200 --grep` and reads ledger events, on every `--rank`. This happens even when no task carries a `finder` tag. Cost per run is about 1 git call plus a full brief load. — Collect the tagged closed briefs first and call `outcomes` only if any is done. — confidence 70%
- LOW — plugin/lib/fmfind.py:112 — `rank` does findings × files set lookups and tokenises every file a second time. This is fine at normal size and could take seconds on a repo with thousands of untested leads. — Acceptable. Index word to file count once if it shows up in a measurement. — confidence 50%

## lens: maintainer
- LOW — plugin/tests/test_find.py:209-296 — There is no failure-path test for `--capture` outside a project (the `UsageError`), for `--capture 0` or a negative value, for a `reverted` fate lowering precision, or for two same-file secrets. — Add the first two and the dedupe case. — confidence 85%
- LOW — plugin/lib/fmfind.py:81,103 — The parameters named `precision` in `scan` and `rank` shadow the module function `precision(p)` defined below them. — Rename them to `prec` or `prior`. — confidence 80%
- LOW — plugin/lib/fmfind.py:137,148 — `capture` imports `fmcli` and calls its private `_create`. A past nit flagged a similar private call (`fmsecrets._tree`). — Fine for now; expose a public helper later.

## Acceptance criteria
- `fm find --rank` orders a vuln and a bug above slow and docs: met, per test_find.py:215-224 and 231-240. The vuln and bug placement is only synthetic for "bug".
- A finder under the floor is muted: met, per test_find.py:226-229 and 250-271.
- I did not run the test command, so a pass is not verified.

## Implicit decisions
- Prior 0.5 weighs as 10 cases, with FLOOR 0.3 and BAR 0.1.
- Severity table values, and reach capped at +0.5 over 10 files.
- Dropped means false alarm; done means real unless reverted.
- A rerun never refiles a closed lead (dedupe includes the archive).
- The exam arm ranks at the prior, not the project's learned precision.
- Held leads are listed last, not removed.
- `--capture` implies `--rank`.
- Discovered tasks are type SECURITY for vuln and secret, FIX otherwise, tier S.

## Not checked
- Whether `fm check` and the full test suite pass.
- The `site/` pages and README rendering.
- Hunks in `plugin/lib/fmcli.py`, `plugin/lib/fmexam.py` and `plugin/tests/test_find.py` are not named by step 3. They are the CLI flags, the exam arm and the tests, so they serve the task.

**Noticed:** none
