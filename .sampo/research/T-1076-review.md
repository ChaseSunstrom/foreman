**Verdict: approve with nits.** The code is correct on the paths I traced. None of these findings is HIGH. I did not run the tests, and I could not check the seed issue numbers offline.

**Findings**

1. MEDIUM — `plugin/lib/fmdoctor.py:636-645` (`check_upstream`) — A user who has already updated Claude Code keeps getting a false WARN.
   - Scenario: a user on 2.1.40 hits `classifyHandoffIfNeeded is not defined` twice, then runs `claude update` to 2.1.50. The two old records stay in the 7-day window.
   - Doctor then reports "should be fixed in 2.1.45 yet recurs", which is wrong, because the errors predate the update.
   - The version is also cached for 24h (`fmhooks.py:2247`), so the other branch ("fixed in X: claude update") can fire for up to a day after updating.
   - Fix: count only errors newer than the mtime of `state/claude-version`, or at least reword the message to "seen N× in 7 days, possibly before updating". The test never covers this case.

2. MEDIUM, not verifiable — `plugin/lib/upstream-issues.json:3-13` — The brief required each issue number and `fixed_in` version to be confirmed against GitHub, but nothing in the diff or the repo shows that. Issues 25990, 21654, 22087 and 28334 appear nowhere else in the repo or the task state. A wrong `fixed_in` puts a false "claude update" or "yet recurs" message in front of the user. Fix: record the verification in the task log, or drop the entries you couldn't check.

3. LOW — `fmdoctor.py:617` — `failures.jsonl` records the output of failed Bash commands and failed `fm check` gates (`fmcli.py:3111`, `fmhooks.py:2020`). A failing test that echoes a pattern string, such as `test_upstream_issues` or a diff of `upstream-issues.json`, therefore counts as an upstream error. Two such runs while developing Foreman give a spurious WARN. Fix: skip records whose task scope includes `upstream-issues.json`, or accept this and note it.

4. LOW — `fmdoctor.py:617` — `note_failure` writes an extra record with `hinted: True` on the third repeat (`fmrecall.py:335`), so 3 failures show as "seen 4×". Fix: add `and not r.get("hinted")`.

5. LOW — `fmdoctor.py:47,53,617` — `run_all` has no try/except around `check_upstream`, so a bad data entry crashes the whole doctor run. Examples: a missing key (`KeyError`), a non-numeric `fixed_in` (`ValueError`), an invalid regex (`re.error`), or a non-dict JSONL line (`r.get` fails). The shipped file is schema-tested and Foreman is the only writer of `failures.jsonl`, so this is unlikely. Fix: wrap the per-issue body and turn the exception into a WARN, as `run_all` does for the bench at `fmdoctor.py:1151`.

6. LOW — `fmdoctor.py:644` — When the version is unknown (`()`), a match falls through to "fixed in X: claude update", which advises an update without knowing it is needed. Fix: add an "installed version unknown" branch.

**Checks that came out clean**
- **Regex backtracking:** the four seed patterns are literals, plus `\S*cwd-[0-9a-f]+` behind a literal prefix. That is linear per match, so there is no catastrophic backtracking. They are searched unanchored and case-insensitively, which is right for substring matching.
- **Latency:** each project costs at most about 1 MB of reading (`tail_jsonl`, 1000 records) plus 1000 `strptime` calls, which is small. The `claude --version` subprocess is cached for 24h, and `check_cc_features` already shares that cache. No before/after measurement was recorded.
- **`recent_hook_errors`:** `days=1` is the default, so the callers in `fmwatch.py:531,583`, `fmfriction.py:174` and `check_hook_errors` behave as before.

**Acceptance criteria**
- Repeated matches give WARN naming the issue and fix version; a single occurrence or no match gives PASS: **met**, per `test_upstream_issues` and the recorded green run.
- The shipped JSON parses and every entry has all five keys: **met**, per `test_the_shipped_upstream_list_is_well_formed`. That test also checks the regex compiles, the URL shape and the `fixed_in` format.

**Implicit decisions**
- The threshold is 2 or more matches, counted over the combined hook-log and failure-signature texts. A single error that appears in both sources counts twice.
- Patterns are searched as case-insensitive substrings. A `fixed_in` of `null` means "no fix yet".
- A missing data file gives WARN, not FAIL.
- The check reads every project's `failures.jsonl`, not only the current project's.
- The version comparison is by three-part tuple (pre-release suffixes are dropped by `_cc_version`).

**Not checked**
- Whether the GitHub issue numbers and fix versions are real.
- Whether any Claude Code error text ever reaches `hooks.log` or `failures.jsonl` outside the test fixtures.
- The tests were not run; I relied on the recorded evidence.

**Noticed:** `fmhooks._cc_version` caches for 24h, so doctor's version-dependent checks lag a `claude update` by up to a day. A small task could invalidate the cache on mtime or on `--version` mismatch.
