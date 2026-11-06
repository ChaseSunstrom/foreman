**Verdict:** approve with nits. The code is sound. The tests for the two acceptance criteria that matter most don't cover the real call path.

## lens: intent
- MEDIUM — `plugin/lib/sampo/models.py:912` — Acceptance criterion 2 says `models.complete` appends the row, but no test calls `complete()`. The tests in `test_live.py:71-94` call `note_call` directly, and `test_models.py` never mentions it. — Add one test that runs `complete()` on a profile with a stubbed `_post`, then asserts one row in `calls.jsonl`. — high
- LOW — `plugin/lib/sampo/models.py:905-908` — `cli` and `systemone` profiles return before `note_call`, and `embed` (about line 880) never calls it, so those calls get no lantern or spark. The request said "every model call". Claude shows up through `spend.jsonl`, so the gap is small. — Note the limit in the changelog or call `note_call` on the embed path. — medium

## lens: adversary
Ok. `_static` (`live.py:303`) only accepts a flat `[A-Za-z0-9_-][A-Za-z0-9._-]*` name and a known extension, so `/static/..%2FA-normal.woff2` gets a 404. The `SAMPO_CALLS` path comes from the user's own environment, and it only receives fixed-shape JSON rows made of a timestamp, a model name and a `[a-z-]` verb. I found no new sink.

## lens: edge
- LOW — `plugin/lib/sampo/cli.py:8659` — `main()` now calls `c.state_dir()` on every command-line run. That function can activate the state fallback and copy state (`core.py:237-251`), and it now runs before any command is parsed. I did not trace a failure; most commands call it anyway. — Compute the path lazily inside `note_call` and pass only a flag through the environment. — low

## lens: operator
Ok. Each `models.complete` call costs one small append of about 150 B. The file is capped at 4 MB with one `.1` rotation. Reads use `tail_jsonl(…, 400)`, which goes backwards from the end. Concurrent processes can race on `os.replace` and lose a few rows, and `note_call` swallows the error.

## lens: maintainer
- MEDIUM — `plugin/lib/sampo/cli.py:8658-8659` — Nothing tests that `main()` sets `SAMPO_CALLS`. Criterion 2's exam-under-a-temp-home path depends on this line alone, and deleting it fails no test. `test_live.py:80` covers only `note_call` reading the variable. — Test that `cli.main(None)` sets the variable, or that a subprocess under a temp `FOREMAN_STATE` writes to the inherited file. — high
- LOW — `CHANGELOG.md:40` — The entry doesn't mention the two other user-visible effects: fonts served as `font/woff2` and the ledger in words. The "plain words" checklist item is only partly met. — Add a clause for each. — medium

## Acceptance criteria
- Fonts served as `font/woff2` and 404 outside the folder: met. `live.py:39,303-311` and `test_live.py:200-208` cover it. I did not run the tests.
- `models.complete` appends one capped row and the snapshot includes it: partly met. The code path is in place (`models.py:912`, `live.py:175`), but the test covers `note_call` and not `complete()`. See the first intent finding.
- Ledger in words: not verifiable from this diff. The diff only touches `helpers.py`, `test_live.py`, `cli.py` and `models.py`, and the ticker change isn't in it.

## Files vs steps
`cli.py`, `helpers.py` and `test_live.py` serve step 2's env inheritance, though no step names them. `CHANGELOG.md` and `files-lib-2.md` are documentation. The `files-lib-2.md` fmlive entry was updated, so it needs no further edit.

## Implicit decisions
- The call log is `state/calls.jsonl`, the schema is `{ts, to, from}`, and the cap is 4 MB with one `.1` file.
- A loopback host logs the model name and any other host logs the profile name.
- The row is written before the request, so failed calls still spark.
- The `from` field is the first three `argv` words matching `[a-z][a-z-]*`.
- `SAMPO_CALLS` is set with `setdefault`, so the outermost process's file wins.
- Static files are read up to 4 MB and silently truncated past that.

## Not checked
I did not run any tests. I did not read the live-page front end, the `CALL_KINDS` mapping, or the ticker-in-words code, because it isn't in the diff.

**Noticed:** `plugin/lib/sampo/live.py:306` reads at most 4 MB of a static file and sends the truncated bytes with a 200 and no error.
