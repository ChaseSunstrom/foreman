---
id: T-2397
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmresearch.py, plugin/lib/fmcore.py, plugin/tests/test_research.py, plugin/tests/test_proof.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T14:03:48Z
updated: 2026-11-01T23:58:16Z
group: Mission 7 proof inbox
base: d6c7f9eb2cff8874c3a9d4085ed52c357b2f8170
base_tree: 8eb16b4d8cfce3d8cc5304ae113531c49273971f
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-01T23:50:28Z
plan0_scope: [plugin/lib/fmresearch.py, plugin/lib/fmcore.py, plugin/tests/test_research.py, plugin/tests/test_proof.py, MASTER.md, CHANGELOG.md]
verified: ok
---
# Research claims say how they were learned (ran, read, recalled); fm prove labels a Decision resting only on recalled ones
## Raw request
> FEATURE: research claims say how they were learned (ran, read or recalled) and a Decision resting only on recalled claims is labelled in fm proof (Mission 7 inbox, tier 2)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] each claim line in a research note carries how it was learned: [read] (a cited http(s) page), [ran] (SOURCE run: or a backticked command), [recalled] (no source); the Already known (fm recall) lines are marked [recalled]; fm prove's research-uncited (which already flags a Decision with no verified claim) says it rests on recalled or unchecked claims only — verify with `python3 plugin/tests/run.py test_research test_proof`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] ground: how a task's Decision links to its research note (research/ path in the brief or evidence); pick the link fm prove can read without running anything
2. [x] red tests: parse_claims on three claim lines gives read, ran, recalled and _line shows it; fm prove lists a done task whose Decision cites a note of only recalled claims as 'recalled', and not one with a read claim
3. [x] Claim.how in parse_claims and _line; PROOF_KINDS 'recalled' row reading the cited note; MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_research.HowLearned` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: HowLearned 0s) / FAILED (1 classes: test_research.HowLearned) [ran] [tree 6e8ecc3f8c65] (2026-11-01T23:50:39Z)
- (step 1) `grep -n research-uncited plugin/lib/fmcore.py` → the Decision link is _need_research's: a RESEARCH task's Decision names a research/ note (by stem) holding a '- ✓ ' line; that kind already flags the recalled-only case [tree 9e074cb4bfbf] (2026-11-01T23:51:09Z)
- (step 2) `python3 plugin/tests/run.py test_research.HowLearned` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: HowLearned 0s) / OK [ran] [tree 9e074cb4bfbf] (2026-11-01T23:51:10Z)
- (step 3) `python3 plugin/tests/run.py test_research test_proof test_site` → exit 0 · Ran 103 tests in 19.1s (40 classes, 16 at a time; slowest: Proof 19s, Header 5s, Meaning 3s) / OK [ran] [tree 9e074cb4bfbf] (2026-11-01T23:51:30Z)
- (ac 1) `python3 plugin/tests/run.py test_research test_proof` → exit 0 · Ran 67 tests in 18.1s (20 classes, 16 at a time; slowest: Proof 18s, Stop 2s, Meaning 2s) / OK [ran] [tree dccdbbfa065d] (2026-11-01T23:57:51Z)
- (audit edge) `self-review: _how reads only the claim's SOURCE text (https/http → read, run:/backtick → ran, else recalled); the tag sits after the status mark, so research-uncited's '- ✓ ' prefix check is untouched; the Already known lines get [recalled]; research-uncited's why now names the recalled-or-unchecked case it already flagged` → an http (not https) source is read but verify() fetches https only, so it stays unchecked and its line says so; a SOURCE of 'run:' with nothing after it is still ran; an empty source is recalled [tree dccdbbfa065d] (2026-11-01T23:57:51Z)
- (audit self) `self-review: _how reads only the claim's SOURCE text (https/http → read, run:/backtick → ran, else recalled); the tag sits after the status mark, so research-uncited's '- ✓ ' prefix check is untouched; the Already known lines get [recalled]; research-uncited's why now names the recalled-or-unchecked case it already flagged` → no findings [tree dccdbbfa065d] (2026-11-01T23:57:51Z)
## Log
- 2026-10-31T14:03:48Z created
- 2026-11-01T23:31:14Z planned from capture
- 2026-11-01T23:50:27Z focused
- 2026-11-01T23:50:28Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-01T23:50:29Z criterion 1 text: each claim line in a research note carries how it was learned: read (a cited page), ran (SOURCE is a command: run: or backticks), recalled (no source, or the Already known section); fm prove lists a done task with a Decision section whose research note (research/, named in the task's evidence or Decision) has only recalled claims as kind 'recalled' → each claim line in a research note carries how it was learned: [read] (a cited http(s) page), [ran] (SOURCE run: or a backticked command), [recalled] (no source); the Already known (fm recall) lines are marked [recalled]; fm prove's research-uncited (which already flags a Decision with no verified claim) says it rests on recalled or unchecked claims only
- 2026-11-01T23:50:29Z scope: the fm prove half exists (research-uncited, T-2391, flags a Decision naming no note with a verified claim); this adds the per-claim label and names it in that kind's why
- 2026-11-01T23:51:38Z scope: MASTER.md and CHANGELOG.md entries
- 2026-11-01T23:58:14Z done
- 2026-11-01T23:58:16Z committed 112e6842 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2353 [FEATURE M, done, 3 steps] The router picks the cheapest model that holds: probing down a tier, and fm run uses it too (Mission 8, #9) — lesson: A confirmation st…
- T-0277 [FEATURE M, done, 4 steps] Research rigor: page cache and --file batches, cross-checks (single-source claims, contradictions, --quorum) — lesson: Heuristic labels…
- T-2398 [FEATURE S, planned, 2 steps] Each proof run records the world it leaned on; fm doctor names done tasks whose world moved since
- decision 2026-11-01: [revisited: defer the full foreman-vs-plain exam] [cites: user steer 2026-10-30: standing rules for the rest of the genesis run] [check: python3 plu…
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_research.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmcore.py, plugin/tests/test_proof.py; re-ground the plan against them before editing
## Lessons
- Before building a check, look for one that already covers it; often only its message needs to name the case
## Plan gaps
- failed first: step 2 red tests: parse_claims on three claim lines gives read, ran, recalled and _line shows it; fm prove…
## Files touched
- plugin/tests/test_research.py
- plugin/lib/fmcore.py
- plugin/lib/fmresearch.py
- MASTER.md
- CHANGELOG.md
