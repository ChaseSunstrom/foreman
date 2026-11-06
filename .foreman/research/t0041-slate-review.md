## Verdict: changes needed

## Findings

**HIGH — INTENT — slate item 9 (`brainstorm-20260926-smarter-slate.md:16`)** "Sensitive-path audits: a diff touching auth/crypto/secrets/exec/deserialization paths needs the adversary lens at any tier" is guard/audit hardening, not one of the six axes the user named (planning, recall, grounding, verification, decisions, learning). It's lifted from `research/brainstorm-20260926-195613/04-security-and-safety.md:15-17` ("Auto-escalate tier and audit lens on sensitive paths"). The pack explicitly says the last ten rounds "mostly hardened Foreman's own guard, state and audits" and the user wants the opposite emphasis (`pack-smarter.md:5`). Fix: drop it from this slate; let it compete in the normal SECURITY queue on its own merits rather than counting toward "wayyy smarter."

**MEDIUM — INTENT — slate items 1-2 (`slate.md:8-9`)** T-0042/T-0040 are plumbing bug fixes with no relation to smarter planning/recall/grounding/verification/decisions/learning. Fine to fix, but they shouldn't be presented as part of the "smarter" deliverable — only 7 of 9 items actually answer the ask.

**MEDIUM — MAINTAINER — slate item 4 (`slate.md:11`)** "test↔source links by name/import" bundles cheap filename-convention matching with import-graph parsing. Its source idea (`06-bold-bets.md:9`) spells out "import graph by regex/AST for Python and simple patterns for others" — per-language import parsing is disproportionate stdlib-only machinery for a codebase this repo's own playbooks (cpp/rust/python/typescript) show is polyglot. Fix: ship name-based matching only for v1 (stem/glob match, already stdlib-trivial), add import parsing later only if the miss rate warrants it.

**MEDIUM — MAINTAINER — slate item 4 (`slate.md:11`)** "refreshed when HEAD moves" doesn't say where HEAD-change detection and the churn/map regen run. Its source (`06-bold-bets.md:9`) proposed "refreshes incrementally on PostToolUse edits" — a hook path. A full churn/import scan run synchronously from a hook risks the ~30 ms p50 / 150 ms p95 budget (`pack-smarter.md:29`) on a large repo. Fix: pin the trigger to a CLI command off the hook path (`fm focus`/`fm task done`, as `05-simplicity.md:16` specifies), not a hook-driven HEAD watch.

**Other observations (out of lens):** item 4's ingestion of READMEs/code comments doesn't inherit item 3's injection-stripping treatment; `04-security-and-safety.md:19-21`'s matching idea was pushed to inbox instead of folded in — worth a security pass before build.

## Grounding claims — verified
Both spot-checked and true: redact runs on typed/`--run` evidence and `fm sync` (`plugin/lib/fmcore.py:218-228,730-731,750`, `plugin/lib/fmsync.py:120`); `bench_hooks.py --runs 20` is already a configured `fm check` gate for this project (`state/projects/foreman-4a056f/meta.json:7`), not merely a doctor routine. No inaccuracies found in the "still dumb" facts spot-checked (`guess_tier` at `fmcore.py:1155-1160`; no recall/decisions surfacing in `fmhooks.py`).

## Acceptance criteria
- Slate recognizable as "wayyy smarter": partially met — 7/9 items fit; item 9 is hardening in disguise (not met per user's own framing).
- Nothing more important left in inbox: met — inbox list (tier calibration, hint-compliance gates, model routing, etc.) is reasonably deferred, no obvious omission.
- Grounding claims correct: met (see above).
- Maintainer: simplest mechanism / no overlap / fits constraints: overlap — met (cross-lens duplicates already merged); simplest mechanism — not met for item 4; constraints — not verifiable from code (no implementation yet) but item 4's trigger/scope needs tightening before build.

## Not checked
`03-performance.md` (not read in full); feasibility/effort numbers themselves; `fmhooks.py`/`fmcli.py` beyond the cited excerpts; items 1, 2, 5, 6, 7, 8 were not independently re-derived from source code (no code exists yet to check against — plan-only).
