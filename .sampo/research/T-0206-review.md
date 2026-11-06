**Verdict: changes needed.** There is one MEDIUM robustness bug and two LOWs. I found no HIGH SSRF hole. I traced this by reading the code and did not run anything. The two LockError-style claims below rest on my knowledge of the Python stdlib, so I rate them medium confidence.

## Findings

1. **MEDIUM** — `plugin/lib/fmresearch.py:99` and `:113-114`. A hostile page can abort the whole run and discard the paid research.
   - `raw.decode(charset, "replace")` sits outside the `try`. `get_content_charset()` returns whatever the server sent, so `Content-Type: text/html; charset=bogus` raises `LookupError`.
   - `http.client.HTTPException` subclasses such as `BadStatusLine` and chunked `IncompleteRead` are not `OSError` or `ValueError`. They are not caught at `:97` either.
   - `pool.map` re-raises the exception in `verify`. `cmd_ask` then crashes before `write_atomic`, so every researcher child's output is lost.
   - The URLs come from model output that a fetched page can steer, so an attacker needs only one page they control.
   - Fix: decode inside the `try` and fall back to utf-8 on `LookupError`. Catch `http.client.HTTPException` in `fetch`. Also wrap `fetch` in `verify` with `except Exception` so it returns `(None, why)`.
   - Confidence: medium-high.

2. **LOW** — `plugin/lib/fmresearch.py:91-93`. The resource limit is weaker than the module docstring says. `timeout=15` applies per socket operation, not to the whole fetch. A server that sends one byte every 14 seconds can hold a worker for hours before reaching the 3 MB cap. `pool.map` has no overall deadline, so `fm research ask` can hang. Fix: track a deadline in a read loop of chunked reads, for example 30 seconds total, and stop when it passes.

3. **LOW** — `plugin/lib/fmresearch.py:116-122`. "Verified" is trivially satisfiable. Any non-empty quote counts, including `"a"`, `"the"` or `"-"`. After `_norm` these almost always occur in a page. A prompt-injected or lazy researcher can therefore turn any claim into ✓. Fix: require a minimum length after normalising, for example at least 4 words or 20 characters. Otherwise mark the claim "unchecked: quote too short". Add a test for it.

## Checked and OK
- Redirects: `_Redirect` re-validates every hop for https and for public resolved addresses.
- Address checks: `is_global` rejects loopback, RFC1918, link-local (including 169.254.169.254) and CGNAT. Decimal-IP spellings are caught because they go through `getaddrinfo`.
- DNS rebinding: the TOCTOU between `public_https` and urllib's own lookup is already acknowledged in the `ponytail:` comment at `:74`.
- Output handling: the note goes through `redact` and `defang`. Only lines starting `- CLAIM/AGAINST/OPEN` are kept, so injected prose is dropped.
- Note path: `name` is validated against a strict regex before the path is built.
- Child processes: they run in a scratch directory with `--setting-sources project,local` and MCP disabled. The planner gets no tools.

## Acceptance criteria
- **Claims marked verified / not found / unchecked, recall first:** met. `Verify.test_quotes_are_checked...` covers all three statuses. `test_plans_fans_out...` checks that the "Already known" entry (`speed-notes`) appears in the note. Real `fetch` is only reached with a stub, and the stub `claude` makes no web calls.
- **Private or non-https URL never fetched:** met for the direct URL. The test covers `http://`, localhost, 127.0.0.1, 10.0.0.1, `::1`, `file:`, the metadata IP and `ftp:`. The redirect handler `_Redirect` has no test, so that path is unverified.

## Intent
The four DONE-WHENs in the request (a plugin-skill line in `next_action`, `fm-recon.md` and `delegate.md` carrying the protocol, the agent file with read-only tools and doctor, ideas annotated with brief ids) are not in `fmresearch.py`. The diff touches `fm-recon.md` and `delegate.md`, but I did not confirm the other items. The task's own criteria cover only `fm research ask`, so they capture only part of the request. I could not check this from the diff.

## Not checked
- The full 471-line diff, including the `fmcli.py` wiring, `fmrecall.py`, `MASTER.md` and the docs.
- Whether Claude Code's own `WebFetch`, used by the researcher child, can reach private addresses. `public_https` does not apply to it.
- Whether `fmrecall.py` needs an edit. The pre-audit flagged it, and it is shown as modified.
- The edge, operator and maintainer lenses.
