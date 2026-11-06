**Verdict:** changes needed. One MEDIUM finding breaks the acceptance criterion's "auth sent only to the configured host". I read the code only. No tests were run, and the diff is not applied against a live Jira or Linear.

Pre-audit: the "secret-looking" hits are the fake `FAKE` token and diff redaction markers, so dismissed. The large-file and hotspot notes are only size and churn.

## lens: adversary
- MEDIUM — plugin/lib/fmeco.py:589 — `urllib.request.urlopen` follows redirects and copies the `Authorization` header to the redirect target. A 3xx from the Jira host sends the token to another host, or over plain http. An SSO-fronted Jira Data Center answering a bad token with a 302 to the IdP is one such case. This breaks the AC's "auth sent only to the configured host". — Use an opener with a no-redirect handler, as `fmmodels._NoRedirect` and `_OPENER` do at plugin/lib/fmmodels.py:208-213. The 3xx then becomes an `HTTPError`, and the existing `HTTPError` branch reports it without the token. Add a test that a 302 to `https://evil.test` is never followed. The current test patches `urlopen`, so it must patch the opener instead. — high (CONFIRMED)
  - file: plugin/lib/fmeco.py, line 589
  - summary: Redirects from the Jira host carry the token to another host.
  - short_summary: token forwarded on cross-host redirect
  - failure_scenario: JIRA_URL=https://jira.corp, and it answers 302 Location: https://idp.other/login. urllib re-sends `Authorization: [REDACTED] …` there.
  - category: credential-exposure
- LOW — plugin/lib/fmeco.py:91-92 — the "isn't on JIRA_URL's host" error prints `c.plain(jira)`. A `JIRA_URL` of the form `https://user:[REDACTED]@host` would put those credentials in the error. — Print only `urlsplit(jira).hostname`. — medium

## lens: edge
- LOW — plugin/lib/fmeco.py:83 — `urlsplit` raises `ValueError` on a malformed bracket host. `fm inbox ticket 'http://[x'` gives a traceback. The `ticket_ref` call at :621 sits outside the `try`, and fmcli.py:7292 catches only `UsageError` and `KeyError`. Before this change the same input gave "can't read". — Wrap `urlsplit` in `try/except ValueError: return None`. — high (CONFIRMED by reading the code; not run)
- MEDIUM — plugin/lib/fmeco.py:652 — the dedupe key is only service and key, and `capture_once(key=…)` searches archived briefs too (fmeco.py:24). Once PROJ-12 has a brief, open or done, a later fetch of the edited or reopened ticket returns the old brief with "already in the inbox or done". The new text is never planned. — Add the body hash to the key, for example `ticket jira PROJ-12 <sha12>`. A refetch of an unchanged issue still dedupes, and a changed one gets a new brief. — medium (PLAUSIBLE)
- LOW — plugin/lib/fmeco.py:121 — if `JIRA_EMAIL` is set, auth is always Basic. A Jira Server/DC user who exports `JIRA_EMAIL` for another tool plus a personal access token gets a 401 "check the token". — Document it, or add a `JIRA_AUTH=bearer` override. — low

## lens: maintainer
- LOW — plugin/tests/test_inbox_more.py:241-243 — the evil-host case never asserts that no request was sent, which is the point of the check. — Capture `sent` from that call and assert it is empty. — medium
- LOW — plugin/tests/test_inbox_more.py:225-246 — no test covers a redirect (see the adversary finding), and the "no token in failure" check covers only the `UsageError` text, not stderr. — Add one redirect case. — medium

## lens: intent, operator
ok. A Jira key or URL and a Linear URL each become one brief. Failures are named, and the error text carries no token except the URL-credentials case above. The docs and `--help` match the code. The new HTTP call runs once per `fm inbox ticket` with a 20 s timeout, so there is no scale cost.

## Acceptance criteria
- **A Jira key or URL becomes one brief:** met. The tests `test_a_jira_key_or_its_url_is_fetched_once_and_made_one_brief` and `test_a_linear_url_is_asked_of_its_graphql_api` cover it.
- **A Linear URL becomes one brief:** met. The same Linear test covers it.
- **Auth goes only to the configured host:** not met when a redirect occurs (the MEDIUM finding). Met for the initial request, since the Jira target is built from `JIRA_URL` and the Linear target is hard-coded.
- **Each failure is said with no token in it:** met, apart from the URL-credentials case.

## Implicit decisions
- Jira REST v2 (the description is plain text or wiki markup, not ADF).
- Basic auth when `JIRA_EMAIL` is set, Bearer otherwise.
- A file that exists wins over a key of the same name.
- A bare key with both trackers configured is refused, not guessed.
- Lowercase keys are not recognised.
- A 1 MiB response cap and a 20 s timeout.
- `HTTPS_PROXY` is honoured.

## Not checked
Live Jira and Linear responses, and the test suite run. The fmcli.py help hunk serves no named plan step but is the feature's help text.

**Noticed:** none
