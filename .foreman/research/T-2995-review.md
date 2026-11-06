**Verdict: changes needed.** Two privacy gaps and one fail-open on the Claude rule need fixing. I could only read files in this session, so I did not run `run.py test_traces`.

**Scope:** I reviewed `plugin/lib/sampo/traces.py`, `plugin/tests/test_traces.py`, `_smith_arm` at `louhi.py:3698-3712`, and the `--traces` branch at `louhi.py:4254-4259` (the option is declared at `cli.py:7913`). I skipped the rest of the 4984-line diff: live, lake, mint, models, selfgate, moonscale and the other merged tasks.

## lens: adversary / privacy
- HIGH — `plugin/lib/sampo/traces.py:48-54` — `_find` walks all of `tmp`, including `tmp/repo`, which the model under test can write to — Walk only `tmp/foreman` (Smith's home), not the whole `tmp` — CONFIRMED
  - Trigger: the model creates `repo/code/T-0001.jsonl` holding fabricated `{"kind":"msg",...}` lines. `os.walk` order is arbitrary, so that file can be picked instead of the real journal.
  - Effect: model-written text becomes training data labelled green. A symlink named `T-*.jsonl` inside such a `code/` directory is followed too.
  - The test only covers the real location.
- MEDIUM — `traces.py:112` — A journal whose meta line is missing or corrupt gives `meta={}`, `is_claude()` is False, and it is exported with null provenance. That fails open on the Claude rule — Refuse a journal with no `model` in its meta — CONFIRMED
- MEDIUM — `traces.py:57-85` and `louhi.py:4254` — `keep` and `export` never check `sensitive` or `lake_optout`. `lake.py:136-147` excludes both — Skip `keep` when the project is sensitive or opted out, and skip minted-origin journals from `detect_sensitive` repos — PLAUSIBLE
  - Trigger: `exam gen --from-repo` on a sensitive repo, then `exam models --traces D`.
  - Effect: the repo's source ends up in `traces.jsonl`.
- MEDIUM — `traces.py:25-27` with `lake.py:25` — `lake.clean` strips every absolute path of two or more segments, not just home and tmp paths. It corrupts the code the model trains on — Strip only `/home/<user>`, `/Users/<user>` and the tmp roots — CONFIRMED
  - `app.get('/api/users')` becomes `app.get('<path>')`, and `#!/usr/bin/env python3` becomes `#!<path> python3`. The model learns to emit `<path>`.
  - Anything over 20000 characters is cut by `text[:cap]`, which leaves tool-call `arguments` as invalid JSON.

## lens: intent
- MEDIUM — `louhi.py:3697,3702` — `green` is True when there are zero verify events and the run closed. `fixed` is vacuously True for the guard-only checks `intact`, `unchanged` and `testfiles` (`louhi.py:1639-1649`). A do-nothing timeout or an unverified close is kept, and `traces.py:74` labels it "green" — Require a verify event, or `fixed` plus a non-timeout end, and store the outcome as `fixed` or `green` — CONFIRMED
- LOW — `louhi.py:3699` — `fixed` is computed even when `green` is already True. For a minted scenario that is a second full run of the repo's test suite before grading — Use `fixed = not green and ...` — CONFIRMED
- LOW — `louhi.py:3711` — `getpass.getuser()` raises `KeyError` on Python before 3.13 when the container has no passwd entry or `USER`. The `except` does not catch it, so the scenario fails, which breaks the "grade never depends on it" comment — Wrap `getuser` or catch `Exception` — PLAUSIBLE

## lens: maintainer
- MEDIUM — `plugin/tests/test_traces.py:56-65` — The test's `/home/zed` is removed by the path pattern, not by the user-name list. Nothing tests user-name stripping, tmp-root stripping, secret redaction, forge-owner stripping or the 20000-character cap. Nothing tests the `--traces` branch or a fabricated journal — Add each as an assertion — CONFIRMED
- LOW — `test_traces.py:86` — The cap assertion allows 20000 bytes of slack; the real bound is `CAP + 1` — Assert `<= traces.CAP + 1` — CONFIRMED
- LOW — `traces.py:81` — The oversized-run tail is dropped, so a green trace can end mid-tool-call — Drop back to the last assistant turn.

## Acceptance criteria
- **AC1 (green run keeps a capped, stripped journal; red keeps none):** partly met.
  - Green keeps and red keeps none, covered by the test at `test_traces.py:56`.
  - The size cap is tested only loosely.
  - Stripping of paths over-reaches, and stripping of names is untested.
  - Some non-green runs are also kept (see the intent lens).
- **AC2 (export as chat JSONL with provenance; Claude runs refused; duplicates dropped):** met for the tested shapes (`test_traces.py:104-116`). It fails open on corrupt meta.

## Implicit decisions
- Dedupe is an exact hash of the messages.
- Each phase becomes one conversation.
- Meta `outcome` is hardcoded to "green".
- A Claude slot is detected by name regex over the slots and the resolved profile fields. An alias that hides a Claude backend passes.
- Journal location is found by a directory walk.

## Not checked
- I did not run the tests.
- I did not check whether the scenario repos or text are themselves Claude-written.
- I did not check the CLI parser wiring beyond `cli.py:7913`.

**Noticed:** `--export` and `--traces` can be passed together, and `--traces` is then silently ignored (`louhi.py:4246-4254`).
