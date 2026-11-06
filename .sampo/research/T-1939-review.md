**Verdict: changes needed.** The fallback does what the acceptance criterion says, but it hides gh's error on a private repo or a rate-limited IP.

## lens: intent
- MEDIUM — plugin/lib/fmci.py:46-47 — `_api` turns every failure, including HTTP 404, 403 and 401, into `None`. For a private repo with gh logged out (the case the fallback exists for), `_latest` then returns no run on every poll. The watch runs silently to `max_polls` (default 120 × 30 s, about an hour) and ends with "gave up waiting: no new finished run". Before this change it failed at once with gh's "not logged in". The unauthenticated limit of 60 calls per hour is hit around poll 60 at the default interval, with the same silent outcome. — Catch `urllib.error.HTTPError` before the `OSError` clause and raise `gh_error` for 401, 403 and 404 (`fmforesight.ci_main` already maps 404 to "private"). Add a test with a 404. — confidence high.
- LOW — plugin/lib/fmci.py:79-84 — If the jobs or annotations call fails, or the failed jobs have no annotations, `tail` is empty. A FIX brief is still captured with an empty body. `capture_once` dedupes on the run URL and `seen` blocks a retry, so it stays empty. — When the text is empty, write "no annotations readable, see {url}", or raise `gh_error`. — confidence medium.
- LOW — plugin/lib/fmcli.py:6556 and MASTER.md:218 — Both still say "through gh". — Add "or GitHub's public API". — confidence high.

## lens: adversary
ok. I found nothing to break:
- The URL host is fixed.
- `repo` comes from the `github_repo` regex, and `sha` must be 40 hex characters.
- The run and job ids must be ints.
- No Authorization header is sent.
- `FOREMAN_NO_NET` and `sensitive` projects are honoured.
- Annotation text goes through `plain_lines`, `redact` and `defang` before it reaches the brief.

## lens: edge
- MEDIUM — the 404 and rate-limit failure above, reached on a private repo or after an hour of polling.
- LOW — plugin/lib/fmci.py:46 — `json.load` reads an unbounded response. The jobs list is not paginated (default 30), so a run with more than 30 jobs can miss failed ones. `[:20]` already caps the loop, so this is only worth a comment.
- No-network and no-origin cases: both re-raise gh's error, which is correct (tested).

## lens: operator
- LOW — see the stale docs above. Cost: one call per poll, up to 120 per watch, against the 60-per-hour unauthenticated limit shared with `ci_main`. That is the same root cause as the first finding.

## lens: maintainer
- LOW — plugin/tests/test_ci_watch.py:113-155 — The test covers a transient `OSError` and the no-origin case. It does not cover an HTTP 404 or 403, an empty annotation list, or `FOREMAN_NO_NET` and `sensitive`, which are the branches at fmci.py:42 and 46. Removing the `sensitive` check leaves it green. — Add small cases for them. — confidence high.
- The urlopen block is close to `fmforesight.ci_main`. It is similar but not identical, and sharing it would also fix the 404 handling.

## Acceptance criteria
- With gh failing, ci-watch finds the commit's run and briefs failed jobs' annotations as data: **met**. The test mocks `_gh` and `urlopen`, and asserts the run is found, only failed jobs are read, and the text is defanged. I did not run the suite.

## Implicit decisions
- Any gh `UsageError` triggers the fallback, including timeouts and non-auth failures.
- The API filters by `head_sha` and ignores the branch.
- Annotations are used only for failed jobs (`failure` or `timed_out`), at most 20 jobs.
- A 20 s timeout and no pagination.
- Failures return `None` and the watch carries on.

## Not checked
I did not run the tests. I did not read the CHANGELOG body beyond the diff.

**Noticed:** fm ci-watch has no message when the watch ends because polling saw no run at all. It could say whether gh or the API was used and the last error.
