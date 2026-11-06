# Round 5 brainstorm catalogue (2026-10-15)

Probe: `fm ideas` with capability map + unspoken needs, 2 rounds, past every earlier ideas.md (brainstorm-20261015-101633): 54 new titles. Every one grounded by three fm-recon passes reading the code (verdict, evidence, value 1–5, effort).

## Build (round 5 slate, value-for-effort order)
1. Snapshot uncommitted work before a command discards it (deferred T-0868; `git reset --hard`, `checkout -- .`, `restore`, `clean -f`, `stash drop/clear`, `switch -f` run unasked on feature branches today; Claude Code's rewind doesn't cover Bash) — value 5, M
2. #48 Rank the review by risk with a "safe to skim" verdict (PARTIAL: fm tour orders files; nothing ranks risk) — value 5, M
3. #46 Audit the final message's claims against the tool log (PARTIAL: Stop gates only "done" claims; "tests pass" / "fixed" go unchecked) — value 4, M
4. #43 Count "keep going" prompts as stalls (PARTIAL: corrections are logged, a bare continue isn't) — value 3, S
5. #12 Nightly sentinel (PARTIAL: fm sentinel exists, fm night has no job for it) — value 3, S
6. #21 fm why quotes the user's own request (DONE but stops at commits/lessons) — value 3, S
7. #24 Rank "what next" across projects (PARTIAL: fm projects lists, nothing ranks) — value 3, S

## Later (premise holds, waits on evidence or cost)
- #3 coverage on changed lines (M, language-specific tooling) · #5 ratchet warnings vs start tree (M) · #7 stack trace → FIX brief with repro (M) · #8 PR review comments as steps (S, needs gh auth to verify) · #20 pasted log/URL → repro criterion (M) · #27 plan bigger than the request (M) · #31/#50 before/after UI shots + a11y at close (M) · #33 review a teammate's PR by running it (M) · #35 check newly added dependencies at close: existence, age, advisories (M, needs registry calls) · #37 predict lane conflicts at plan time (M) · #44 one ranked friction table (M) · #45 lint CLAUDE.md and other plugins' rules against Foreman's (M) · #47 a steer marks evidence stale (M)

## Done already
#1 evidence grade (Brief.grade) · #2 flaky reruns (fm check) · #4 fm task prove --hunks · #6 fm bisect / sentinel --bisect · #11 fm why · #15 fm suspects · #41 fm lane --spike

## Skip (with reason)
#9/#22 git hooks for human commits (guard protects .git/hooks; Foreman gates its own work) · #10 sharded migrations (L, no demand) · #13 screenshot → test (L, speculative) · #14/#19 cross-repo tasks (L) · #16 input shrinking (M, rare) · #17 test-assertion mutation (prove --hunks covers most) · #18 classifier learning from retypes (low value) · #23 branch + PR landing (outward; Foreman never pushes) · #25 rebuild from BUILD_PROMPT (value 1) · #26 blind re-derive (bench covers) · #28 pin behaviour (CLEAN lock exists) · #29 per-step commits (value 2) · #30 per-lane ports/DBs (value 2) · #32 API break gate (L) · #34 profile diff (value 2) · #36 migration reversibility (L) · #38 ADR export (value 2) · #39 OTel spans (value 2) · #40 non-code packs (L) · #42 watch human saves (ambient tests cover Claude's) · #49 doc claim checks (value 2) · #51 canary defects (name taken; bench) · #52 other-vendor second opinion (data leaves; value 2) · #53 fm teach (value 2) · #54 reviewer FAQ (noise)

Yield: 7 grounded builds (≥ 3), so not dry: after these, probe again.
