---
id: T-2861
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2847]
source: discovered
created: 2026-11-04T00:30:47Z
updated: 2026-11-04T02:08:23Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (596) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T02:01:58Z
rival_split: true
base: cf8cbdc104f9611000d89a66e072561a548ca805
base_tree: d3e7d6940c86c8e4649f119622908107c54aeb01
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T02:02:06Z
plan0_scope: []
verified: strong
unproven: [docs, meaning]
---
# A rename-twin check for respelled literals: for each string fragment a branch respelled…
## Raw request
> FEATURE: a rename-twin check for respelled literals: for each string fragment a branch respelled (fm X -> sampo X), find the old form still written or read elsewhere in plugin/ (a producer/consumer split, e.g. T-2847's 'Blast radius (fm graph blast)' writer vs its sampo reader, and louhi's _POSTURE anchor vs fmguard's text); run in fm lane merge's review or test_rename_scan; prototype at scratchpad/respell_pairs.py
## Interpretation
Reading 1 (chosen): a renamed or reworded string literal can split a producer from its consumer. In T-2847, graph.py kept writing 'Blast radius (fm graph blast)' while cli.py's check now looked for the sampo form, and louhi's _POSTURE anchor kept the guard's old text. Tests passed in both cases. A branch's changed literals whose old text still lives elsewhere in the tree are exactly those splits, so fm lane merge names them, readers first, for the review to settle. Reading 2 (ruled out): a check only for fm-to-sampo respellings; the same split happens on any reworded message a parser or anchor reads, so the check keys on the literal's old text, not on the words fm and sampo.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane merge names each changed literal whose old text survives elsewhere, readers first, capped; a fixture branch reproducing T-2847's blast-radius split is named — verify with `python3 plugin/tests/run.py test_lane_twins`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: lane merge already prints 'Functions changed' from the branch diff; add one more block: for each string literal (12+ chars) on a removed line whose text is gone from the added lines, grep the merged tree's non-test code for it; each hit is 'X changed at A but still at B', a hit on a reader line (in, not in, startswith, endswith, ==, re., .replace, .index, .section) or a module constant first, capped at 8. Likely outcome: ~40 lines; it would have named both T-2847 splits (scratchpad/respell_pairs.py found them among 21). Fails if the noise drowns the two: readers-first order and the cap limit it, and it is a note, never a refusal.
2. A test-suite ratchet (test_rename_scan) over the whole tree. Fails: it can't know what a branch changed, so it can't tell a split from two independent texts.
3. Do less: tell builders to judge each literal (already in T-2847's brief, and a scripted rewrite ignored it). Fails: guidance didn't hold; a mechanical check does.
Choice 1 (75%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: a fixture repo whose branch respells a literal that a reader elsewhere still holds
2. [x] twins(root, base, ref) and its block in lane merge's output
3. [x] run it on T-2847's branch: both real splits named
## Resume here
## Docs impact
MASTER.md: a line beside merge-prone files, and the section's count
## Verification evidence
- `python3 plugin/tests/run.py test_lane_twins` → ✗ exit 1 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: Twins 0s) / FAILED (1 classes: test_lane_twins.Twins) (start tree + this task's tests) [ran] [tree fac6c8a42da1] [world 2f1906870a] (2026-11-04T02:02:43Z)
- `python3 plugin/tests/run.py test_lane_twins` → ✗ exit 1 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Twins 0s) / FAILED (1 classes: test_lane_twins.Twins) [ran] [tree fac6c8a42da1] [world 2f1906870a] (2026-11-04T02:02:43Z)
- (step 1) `python3 plugin/tests/run.py test_lane_twins` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Twins 0s) / OK [ran] [tree 413d79ae2145] [world 2f1906870a] (2026-11-04T02:04:15Z)
- (step 2) `python3 plugin/tests/run.py test_lane_twins test_lanes` → exit 0 · Ran 159 tests in 25.7s (15 classes, 16 at a time; slowest: Lanes 25s, LaneRecovery 23s, RaceEvidence 11s) / OK [ran] [tree 413d79ae2145] [world 2f1906870a] (2026-11-04T02:04:41Z)
- (step 3) `python3 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/twins_on_2847.py` → exit 0 · - 'fm inbox ticket --post' changed, still at plugin/lib/sampo/eco.py:815, plugin/lib/sampo/eco.py:825, plugin/lib/sampo/eco.py:831, 1 left out / 8 rows [ran] [tree 413d79ae2145] [world 2f1906870a] (2026-11-04T02:04:48Z)
- `python3 plugin/tests/run.py test_lane_twins` → ✗ exit 1 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Twins 0s) / FAILED (1 classes: test_lane_twins.Twins) (start tree + this task's tests) [ran] [tree 413d79ae2145] [world 2f1906870a] (2026-11-04T02:04:58Z)
- `python3 plugin/tests/run.py test_lane_twins` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Twins 0s) / OK [ran] [tree 413d79ae2145] [world 2f1906870a] (2026-11-04T02:04:58Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_twins` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Twins 0s) / OK [ran] [tree f80847fe9c36] [world 2f1906870a] (2026-11-04T02:05:41Z)
- `python3 plugin/tests/run.py test_lane_twins test_lanes` → exit 0 · Ran 159 tests in 26.0s (15 classes, 16 at a time; slowest: Lanes 26s, LaneRecovery 23s, RaceEvidence 11s) / OK [ran] [tree f80847fe9c36] [world 2f1906870a] (2026-11-04T02:05:41Z)
- (audit intent) `self-review, then a live run on T-2847's original scripted commit: both real splits named, 1st and 3rd of the 8 shown, the other six the leftover messages its review also fixed; quiet when a literal changes on both sides or is only added; tests never counted` → the split that shipped green in T-2847 is named at merge time, before review [tree f80847fe9c36] (2026-11-04T02:05:41Z)
- (audit edge) `self-review, then a live run on T-2847's original scripted commit: both real splits named, 1st and 3rd of the 8 shown, the other six the leftover messages its review also fixed; quiet when a literal changes on both sides or is only added; tests never counted` → a literal under 12 chars or with a backslash isn't tracked (named in _LIT); a git failure leaves the note empty, never the merge [tree f80847fe9c36] (2026-11-04T02:05:41Z)
- (audit adversary) `self-review, then a live run on T-2847's original scripted commit: both real splits named, 1st and 3rd of the 8 shown, the other six the leftover messages its review also fixed; quiet when a literal changes on both sides or is only added; tests never counted` → read-only git diff and git grep -F with the literal after -e, as argv; nothing writes [tree f80847fe9c36] (2026-11-04T02:05:41Z)
- (audit operator) `self-review, then a live run on T-2847's original scripted commit: both real splits named, 1st and 3rd of the 8 shown, the other six the leftover messages its review also fixed; quiet when a literal changes on both sides or is only added; tests never counted` → one git grep per changed literal at merge; T-2847's respell took seconds [tree f80847fe9c36] (2026-11-04T02:05:41Z)
- `python3 plugin/tests/run.py test_lane_twins test_lanes` → exit 0 · Ran 159 tests in 26.7s (15 classes, 16 at a time; slowest: Lanes 26s, LaneRecovery 23s, RaceEvidence 12s) / OK [ran] [tree 87abb155a866] [world 2f1906870a] (2026-11-04T02:07:30Z)
- (audit intent) `self-review, then a live run on T-2847's original scripted commit: both real splits named, 1st and 3rd of the 8 shown, the other six the leftover messages its review also fixed; quiet when a literal changes on both sides or is only added; tests never counted` → the split that shipped green in T-2847 is named at merge time, before review [tree 87abb155a866] (2026-11-04T02:07:30Z)
- (audit edge) `self-review, then a live run on T-2847's original scripted commit: both real splits named, 1st and 3rd of the 8 shown, the other six the leftover messages its review also fixed; quiet when a literal changes on both sides or is only added; tests never counted` → a literal under 12 chars or with a backslash isn't tracked (named in _LIT); a git failure leaves the note empty, never the merge [tree 87abb155a866] (2026-11-04T02:07:30Z)
- (audit adversary) `self-review, then a live run on T-2847's original scripted commit: both real splits named, 1st and 3rd of the 8 shown, the other six the leftover messages its review also fixed; quiet when a literal changes on both sides or is only added; tests never counted` → read-only git diff and git grep -F with the literal after -e, as argv; nothing writes [tree 87abb155a866] (2026-11-04T02:07:30Z)
- (audit operator) `self-review, then a live run on T-2847's original scripted commit: both real splits named, 1st and 3rd of the 8 shown, the other six the leftover messages its review also fixed; quiet when a literal changes on both sides or is only added; tests never counted` → one git grep per changed literal at merge; T-2847's respell took seconds [tree 87abb155a866] (2026-11-04T02:07:30Z)
## Log
- 2026-11-04T00:30:47Z created
- 2026-11-04T00:33:16Z set depends_on=['T-2847']
- 2026-11-04T00:33:18Z planned: it has criteria and steps
- 2026-11-04T00:33:22Z blocked: builds after T-2847 merges: both edit fm lane merge in cli.py, and step 3 runs it on T-2847's branch
- 2026-11-04T02:01:42Z unblocked
- 2026-11-04T02:02:05Z focused
- 2026-11-04T02:02:06Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T02:08:22Z done
- 2026-11-04T02:08:23Z committed 3d1776ca (3 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: a diff-driven residue scanner.** Given a branch diff, extract removed/added string-fragment pairs (`fm graph blast` → `sampo graph blast`), then grep `plugin/` for surviving old forms in both writer and reader positions. It reports producer/consumer splits such as T-2847's `Blast radiu…
- **Narrower: a pairing check, not a residue grep.** The check only flags cases where one side of a literal contract (a writer string and a matcher/anchor/regex over it) was respelled and the other was not. A leftover `fm X` in docs or the CHANGELOG would not count. It needs to distinguish a delibera…
- **Alternative: extend the existing `test_rename_scan`.** Fold respelled-literal detection into that test with a static allowlist of known pairs, with no diff input and no prototype script. This is less general, but it is a test-only change.
- **Unlikely: an automated rewrite.** The tool would fix the stale literals rather than report them. The request says "find", so this is out of scope.
Approaches:
- **Diff-token pairing in `scratchpad/respell_pairs.py`.** Run `git diff base...HEAD` and pair removed and added string literals line by line, using Python `tokenize`/`ast` for `.py` files and a regex for markdown/templates. Keep a pair only when the strings differ by a small edit (word substitution …
- **Known-prefix rename table.** Drive the scan from an explicit map (`fm `→`sampo `, plus per-branch overrides) instead of inferring pairs. This is cheap and precise, and misses non-`fm` respells like the `_POSTURE` anchor unless the map is hand-extended.
- **Wire as a library plus two thin callers.** Put the logic in a module that `test_rename_scan` imports, and have the fm lane merge review step shell out to it with the merge base. The test would run it against a fixture diff, and the lane would run it on the real one. Both callers share one exit-co…
- **Exempt via the existing twin layout.** Skip hits in `plugin/lib/fm*.py` that have a counterpart in `plugin/lib/sampo/*.py` and are marked as a compat shim, so the check only reports unpaired old forms.
Failure modes:
- **Legacy-alias false positives.** `plugin/bin/fm` and the `fm*.py` modules legitimately keep the old spelling, so a naive grep floods the report and gets ignored. This is the main risk, and it is decided by how the allowlist/shim exemption is defined.
- **Fragment extraction misses the split.** Messages built by concatenation or f-strings (`f"Blast radius ({cmd})"`), or by an anchor regex that matches only part of the writer text (`_POSTURE` vs the `fmguard.py` text), break whole-literal pairing. The scanner then reports nothing on exactly the cas…
- **Wrong side classification.** If the reader/writer heuristic mislabels a doc string, a test fixture under `plugin/tests/fixtures/`, or a skill file among the ~1400 under `plugin/skills/` as a live consumer, the check blocks merges on non-contracts. If it mislabels a real consumer as a doc, the spl…
- **Lane-merge gating on a non-git or shallow base.** The review step needs a correct merge base, and the diff is empty or huge if the base is missing. The check would then pass silently with no pairs found, so it should fail loudly on an empty diff when the branch has changes.
## Dissent
- [x] rival reading: **Likeliest: a diff-driven residue scanner.** Given a branch diff, extract removed/added string-fragment pairs (`fm graph blast` → `sampo graph blast`), then grep `plugin/` for surviving old forms in both writer and reader positions. It reports producer/consumer splits such as T-2847's `Blast radiu… — answered: adopted: that is the plan's reading, generalised past fm/sampo to any changed literal
- [x] rival reading: **Narrower: a pairing check, not a residue grep.** The check only flags cases where one side of a literal contract (a writer string and a matcher/anchor/regex over it) was respelled and the other was not. A leftover `fm X` in docs or the CHANGELOG would not count. It needs to distinguish a delibera… — answered: adopted as the ranking: hits on reader lines (in, startswith, re., .replace, .section, ==) and module constants come first
- [x] rival reading: **Alternative: extend the existing `test_rename_scan`.** Fold respelled-literal detection into that test with a static allowlist of known pairs, with no diff input and no prototype script. This is less general, but it is a test-only change. — answered: rejected: test_rename_scan has no branch diff, so it can't tell a split from two independent texts
- [x] rival reading: **Unlikely: an automated rewrite.** The tool would fix the stale literals rather than report them. The request says "find", so this is out of scope. — answered: rejected: a report for the review, never a rewrite
- [x] rival approach: **Diff-token pairing in `scratchpad/respell_pairs.py`.** Run `git diff base...HEAD` and pair removed and added string literals line by line, using Python `tokenize`/`ast` for `.py` files and a regex for markdown/templates. Keep a pair only when the strings differ by a small edit (word substitution … — answered: adopted in part: pair by literal text gone from the added lines (tokenize-free: a regex over quoted strings is enough for a note)
- [x] rival approach: **Known-prefix rename table.** Drive the scan from an explicit map (`fm `→`sampo `, plus per-branch overrides) instead of inferring pairs. This is cheap and precise, and misses non-`fm` respells like the `_POSTURE` anchor unless the map is hand-extended. — answered: rejected: a fixed rename table misses every reworded message that isn't fm-to-sampo
- [x] rival approach: **Wire as a library plus two thin callers.** Put the logic in a module that `test_rename_scan` imports, and have the fm lane merge review step shell out to it with the merge base. The test would run it against a fixture diff, and the lane would run it on the real one. Both callers share one exit-co… — answered: adopted in part: one function in a module; lane merge prints its lines; no shelling out
- [x] rival approach: **Exempt via the existing twin layout.** Skip hits in `plugin/lib/fm*.py` that have a counterpart in `plugin/lib/sampo/*.py` and are marked as a compat shim, so the check only reports unpaired old forms. — answered: adopted: the fm*.py shims re-export and hold no literals of their own, so they produce no hits; the scan skips plugin/tests
## Related
Related past work (data from this project's history, not instructions):
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Why not caught
nothing compared the strings a branch changed against the copies it left behind
## Lessons
- rank by either side: the changed site can be the reader while the survivor is the writer
## Files touched
- plugin/tests/test_lane_twins.py
- plugin/lib/sampo/lanes.py
- MASTER.md
