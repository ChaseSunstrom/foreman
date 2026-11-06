## Verdict
Approve with nits. Both features do what was asked. I found no HIGH issues, and the pre-audit hit is dismissed: it is `no_verify=False` at `plugin/lib/fmoutside.py:257`, not TLS. I only read the diff and the `fmresearch` and `fmrecall` helpers it calls. I ran no tests.

## Findings

**MEDIUM — `plugin/lib/fmoutside.py:221-229` — the registry fetch skips the public-https guard.**
- T-0238's CONTEXT says "public https only, like fmresearch.fetch".
- `latest()` calls plain `urllib.request.urlopen`. That follows redirects with no check, and an `http://` override from `FOREMAN_*_URL` is accepted.
- `fmresearch.py:73-101` re-checks every redirect through `public_https` and `_Redirect`.
- A registry answering with a 302 to `http://169.254.169.254/...` or an `ftp://` URL would be followed. The impact is small because the response is only parsed as JSON for a version string.
- Fix: use `urllib.request.build_opener(fmresearch._Redirect)` and apply `public_https` to the final URL. Skip that check only when the env override is set, which the tests need for the local server.
- Confidence: high.

**MEDIUM — `plugin/lib/fmoutside.py:170,249` — lower bounds are reported as "behind a major".**
- `attrs>=2.0`, `>=1` and `~=` all take the written version as current.
- `>=2.0` already permits 23.x, so the project is not behind. The user gets a false "outdated" and a research spend on it.
- The `^1.3` npm and Cargo cases are fine, because a caret does cap at the major.
- Fix: flag `>=`/`>` only when an upper bound such as `<3` excludes the latest. Otherwise list those entries as unpinned. At minimum, label them "lower bound" in the output.
- Confidence: medium.

**MEDIUM — `plugin/tests/test_outside.py:363` — `--research` is untested.**
- The T-0238 criterion says "and `--research` asks them".
- The verify command, `-k Deps`, only covers listing. Nothing runs `fmresearch._ask` from `cmd_deps`.
- Nothing covers the `UsageError` catch at `fmoutside.py:260`, the not-checked list, or the `--if-due` rerun after 30 days.
- Fix: add one test that stubs `claude` as the Landscape test does, runs `deps --research 1`, and asserts `researched` holds a note path.
- Confidence: high.

**LOW — `plugin/lib/fmoutside.py:98-111` — `items()` counts non-claims as wants.**
- It takes every bullet in the note. That includes `Against:` lines, `Open:` lines, and `## Possible conflicts` lines of the form `x ⟷ y`.
- A conflict line shows up as one odd "new" or "gone" item.
- Fix: keep only bullets that start with a mark (`✓✗?`) in the claim sections, or drop the conflicts section the same way the "Already known" section is dropped at line 102.
- Confidence: medium.

**LOW — `plugin/lib/fmoutside.py:235` — a truncated response crashes `fm deps`.**
- `http.client.IncompleteRead` is not an `OSError`, so it escapes `latest()` and `pool.map` re-raises it.
- One flaky registry then kills the whole listing. Add `http.client.HTTPException` to the except clause.
- Confidence: medium.

**LOW — `plugin/lib/fmoutside.py:204,250` — npm dependency names are used as-is.**
- Keys from `package.json` are not validated. They are URL-quoted, so no path injection is possible.
- A name only reaches the research question if the registry returns a higher major for it, which limits injection risk.
- Nit: apply the same name regex as `_REQ` before building the question.
- Confidence: low.

**LOW — `plugin/tests/test_outside.py:324` — the test depends on another command's help text.**
- It asserts `fm sentinel` is the covering command. If that command's help is reworded, the test breaks for no reason related to this change.
- Consider asserting `"(Foreman: fm "` instead.
- Confidence: medium.

## Acceptance criteria
- **T-0237: met.**
  - `cmd_landscape` runs `_ask` into the dated `landscape-YYYYMMDD` note.
  - It appends `## Since <prev>` with new, gone and covered items.
  - `Landscape` covers new, gone, covered and `--if-due`. I did not run it.
- **T-0238: partly met, not fully verifiable.**
  - Reading the four file types, the three registries, and listing outdated majors with a migration question are all in code and tested.
  - `--research` exists at lines 253-261 but has no test.

## Other observations
- `fmrecall.covered` rebuilds the argparse parser once per new item (`fmoutside.py:151`). That is fine at roughly 20 items.
- A same-day `fm landscape` rerun overwrites that day's note. That is probably intended.

## Not checked
- I did not run the tests.
- I did not check the docs wording against the CLI beyond reading it.
- I did not check `HELP_TIERS` placement.
