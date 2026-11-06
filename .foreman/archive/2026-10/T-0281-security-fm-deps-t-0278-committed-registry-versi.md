---
id: T-0281
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-04T08:07:16Z
updated: 2026-10-04T08:08:03Z
base: fccad6b1b49c118d253d22b4aefbe00f7aa24ea2
base_tree: d6156cdbd90ac3da825b23493344f0eab905718d
verified: strong
---
# SECURITY: fm deps (T-0278, committed) — registry version strings and manifest names reach
## Raw request
> SECURITY: fm deps (T-0278, committed) — registry version strings and manifest names reach the terminal and the research prompt unchecked; a FOREMAN_*_URL override skips the address check (background security review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] registry versions that aren't plain version strings, manifest names outside the ecosystems' name syntax, and control characters in reasons never reach the output or the research question; an overridden registry URL must be public https or loopback — verify with `python3 plugin/tests/run.py -p test_outside.py -k Untrusted`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test the untrusted inputs, then validate names, versions and override URLs in fmoutside.py
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_outside.py -k Untrusted` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Untrusted 0s) / FAILED (1 classes) [ran] [tree 8424b6369c91] (2026-10-04T08:07:31Z)
- (step 1) `python3 plugin/tests/run.py -p test_outside.py -k Untrusted` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Untrusted 0s) / OK [ran] [tree 45278555ab12] (2026-10-04T08:08:03Z)
- (ac 1) `python3 plugin/tests/run.py -p test_outside.py -k Untrusted` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Untrusted 0s) / OK [ran] [tree 45278555ab12] (2026-10-04T08:08:03Z)
- (audit adversary) `self: each of the three findings has a failing-first assertion (manifest names with control chars, injected registry versions, non-https/LAN/file overrides never opened); the T-0278 suite still passes` → names/versions constrained to ecosystem shapes before they reach output or the research prompt; override URLs https or loopback http only; reasons plain()ed [tree 45278555ab12] (2026-10-04T08:08:03Z)
- (audit self) `self: each of the three findings has a failing-first assertion (manifest names with control chars, injected registry versions, non-https/LAN/file overrides never opened); the T-0278 suite still passes` → no findings [tree 45278555ab12] (2026-10-04T08:08:03Z)
## Log
- 2026-10-04T08:07:16Z created
- 2026-10-04T08:07:23Z focused
- 2026-10-04T08:08:03Z done
- 2026-10-04T08:08:03Z committed b8bf5b2 (2 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0278-review-1: Approve with nits. Both features do what was asked. I found no HIGH issues, and the pre-audit hit is dismissed: it is `no_verify=False` at `plu…
- research T-0206-review: Verdict: changes needed.** There is one MEDIUM robustness bug and two LOWs. I found no HIGH SSRF hole. I traced this by reading the code and did …
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- research t0015-reaudit: T-0015 adversary re-audit of 1b175e1: HIGH the task id reaches the dialog unsanitized (bidi override in the id) → require a real task id. MED _HI…
## Regression test
plugin/tests/test_outside.py Untrusted
## Lessons
- Text from a registry or a cloned manifest is untrusted input: shape-check it before it reaches the terminal or a model prompt
## Files touched
- plugin/tests/test_outside.py
- plugin/lib/fmoutside.py
