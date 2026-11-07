---
id: T-2627
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsteer.py, plugin/tests/test_steer.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-11-02T18:27:30Z
updated: 2026-11-02T19:16:31Z
base_note: Calibration: this plan states Choice 70% where PERFORMANCE M closes (25) held on the first finish 96% of the time: 26 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-02T19:05:13Z
rival_split: true
base: 6b4fc57d185beba6908c9c289791b2b9af9f74e9
base_tree: a52b1971f2ea26b070be6684beab54db40d2d484
plan0_at: 2026-11-02T19:05:19Z
plan0_scope: [plugin/lib/fmsteer.py, plugin/tests/test_steer.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# The steer expander's method prompt anticipates more and harms less: tuned on the train split only (baseline steer-20261102T182645: train 6%, 48 harmful additions over 43 cases), the held-out rate read once after the choice
## Raw request
> PERF: raise the steer-expansion exam's held-out coverage from its 19% baseline (steer-20261102T182645): tune fmsteer.EXPAND on the train split only (the held-out third stays unseen); the misses are project-specific nouns the raw words imply (tower, Missions, gen-0, exam kinds) and the harms are generic additions that contradict the words (a budget after 'no budget', deferring tests); try a project map in the prompt that holds no decisions.md text (the references live there), a do-not-add-limits-the-words-deny rule, and fewer generic clauses; keep a change only if the train rate rises and harms fall, then read the held-out rate once
## Interpretation
Reading 1 (chosen): improve fmsteer.EXPAND, the generic method prompt, measured on the train split; MOONSHOT part B fixes the exam's input to the raw words alone, so no project map or decision text may reach the expander (the references live in decisions.md). The baseline's misses were concrete mechanisms the words imply and its harms were added limits the words deny (a USD cap after 'no token budget', deferring every test). Reading 2 (ruled out): give the expander Foreman's README or decisions as context. It would lift the rate by leaking the answers and break 'from the raw words alone'.
## Assumptions (confidence)
## Acceptance criteria
- [x] four method variants were measured on the train split, the last round under one judge, and one is kept only if it beats the baseline on both coverage and harms (none did: the original prompt stays, numbers in the log); the exam's judge is now always the strongest model, so runs of any expander compare — verify with `python3 plugin/tests/run.py test_steer.Run`
- [x] the method prompt names no case content (no reference clause reaches the expander) and the steer tests pass — verify with `python3 plugin/tests/run.py test_steer.Cases test_steer.Run test_steer.Live test_steer.Page`
## Non-goals
## Approach (options → choice → why)
1) A rule against added limits plus asks for concrete, checkable mechanisms and the next thing the user would ask. Likely outcome: fewer harms, some coverage gain. 2) The same prompt on a stronger expander (opus, judged by fable). Likely outcome: more coverage at about 3x the cost a call; fails if fable can't be named on the CLI. 3) Expand, then a second pass removing clauses the words don't support. Fails if: it doubles the live cost and mostly trims, so coverage can fall. 4) Do less: only the no-added-limits rule. Likely outcome: harms fall, coverage flat. 5) Use what exists: fm exam steer run --split train with the same judge and cases is the bench. Likely outcome: no new tooling; each variant is one train run. Choice: measure 1 and 2 on train, keep the better (70%).
## Risks and rollback
Overfitting: only train numbers steer the choice; the held-out rate is read once, after. Cost: each train run is 60 model calls. Rollback: the prompt is one constant; git revert.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py; past FIXes T-1056, T-1106, T-1117, T-1122, T-1124.
## Execution prompt
## Steps
1. [x] measure two or three method variants on the train split (same cases, same judge)
2. [x] keep the best by train rate and harms; read the held-out rate once and record it
3. [x] docs: CHANGELOG, MASTER
## Resume here
<!-- auto -->
- 2026-11-02T19:15:42Z step 1/3: measure two or three method variants on the train split (same cases, same judge)
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmguard.py, plugin/lib/fmsteer.py, plugin/tests/test_guard.py, plugin/tests/test_steer.py, MOONSHOT.md
- touched since last checkpoint: plugin/lib/fmsteer.py, plugin/tests/test_steer.py, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/extract_json.py
## Docs impact
CHANGELOG (Unreleased: one judge, the strongest; the measured null result); MASTER.md fmsteer line (the judge).
## Verification evidence
- (step 3) `python3 plugin/tests/run.py test_docs test_docsdrift test_steer.Run` → exit 0 · Ran 104 tests in 8.3s (25 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 63694edca357] [world 2f1906870a] (2026-11-02T19:14:34Z)
- (step 2) `fm exam steer` → exit 0 · steer-20261102T191506-7457: held out 19% of the reference clauses covered over 13 case(s), train ? over 0 (sonnet, judged by fable); 16 harmful addition(s) [ran] [tree 63694edca357] [world 2f1906870a] (2026-11-02T19:15:38Z)
- (step 1) `sh -c 'ls state/projects/foreman-4a056f/research/genesis/steer/steer-20261102T190708-6cad.json state/projects/foreman-4a056f/research/genesis/steer/steer-20261102T190743-eb15.json state/projects/foreman-4a056f/research/genesis/steer/steer-20261102T190800-e1cd.json state/projects/foreman-4a056f/research/genesis/steer/steer-20261102T191052-fe51.json state/projects/foreman-4a056f/research/genesis/steer/steer-20261102T191156-1445.json state/projects/foreman-4a056f/research/genesis/steer/steer-20261102T191148-9a9e.json'` → exit 0 · state/projects/foreman-4a056f/research/genesis/steer/steer-20261102T191148-9a9e.json / state/projects/foreman-4a056f/research/genesis/steer/steer-20261102T191156-1445.json [ran] [tree 63694edca357] [world 2f1906870a] (2026-11-02T19:15:45Z)
- (ac 1) `python3 plugin/tests/run.py test_steer.Run` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Run 0s) / OK [ran] [tree 63694edca357] [world 2f1906870a] (2026-11-02T19:15:55Z)
- (ac 2) `python3 plugin/tests/run.py test_steer.Cases test_steer.Run test_steer.Live test_steer.Page` → exit 0 · Ran 6 tests in 2.0s (4 classes, 16 at a time; slowest: Live 2s, Cases 1s, Run 1s) / OK [ran] [tree 63694edca357] [world 2f1906870a] (2026-11-02T19:15:55Z)
- (audit intent) `self (M PERF): the change kept is one line (the judge is always the strongest model) plus its two test lines; the prompt is byte-identical to the original; no held-out number steered a choice (held out was read once, after the decision)` → the hypothesis failed and the change was not kept; the fixed judge makes the next tuning attempt (T-2632) comparable [tree 63694edca357] (2026-11-02T19:15:55Z)
- (audit edge) `self (M PERF): the change kept is one line (the judge is always the strongest model) plus its two test lines; the prompt is byte-identical to the original; no held-out number steered a choice (held out was read once, after the decision)` → the strongest model as expander is still refused; opus and sonnet expanders are both judged by fable, so they compare [tree 63694edca357] (2026-11-02T19:15:55Z)
## Log
- 2026-11-02T18:27:30Z created
- 2026-11-02T19:01:17Z planned from capture
- 2026-11-02T19:05:19Z focused
- 2026-11-02T19:07:40Z paused: focus moved to T-2629
- 2026-11-02T19:08:41Z focused
- 2026-11-02T19:09:19Z round 1 (train, judges differ by expander rank): baseline sonnet/opus 8.6% (14/93), 34 harms; v1 sonnet/opus 10.6% (18/93), 52 harms; v2 = v1 on opus/fable 19.1% (26/93), 57 harms. The judges flag unbounded autonomy ('impose no limits', 'until nothing new') as harm, and v1's 'never add a limit' line produced exactly those clauses. Round 2: one judge (the strongest, fable) for every expander so runs compare; base (original prompt), v3 (bound loops by progress, don't announce no-limits, safe-to-act clauses, read words as said to one's own harness) on sonnet and on opus
- 2026-11-02T19:09:20Z paused: focus moved to T-2629
- 2026-11-02T19:12:38Z round 2 (train, one judge: fable): base sonnet 12.3% (20/93), 45 harms, 1.5 a case; v3 sonnet 15.6% (21/93), 69 harms; v3 opus 16.2% (19/93), 62 harms. Covered clauses don't move beyond judge noise (base sonnet read 8.6% under opus and 12.3% under fable), harms rise ~50%: asking for anticipation adds more than it gets right. Decision: keep the original method prompt; keep the fixed strongest judge so variants compare; next idea captured, not tried here
- 2026-11-02T19:13:59Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-02T19:13:59Z focused
- 2026-11-02T19:14:19Z criteria revised to the measured outcome: the hypothesis (a richer method prompt anticipates more and harms less) was refuted on train; a PERF change that doesn't help is not kept
- 2026-11-02T19:16:28Z done
- 2026-11-02T19:16:31Z committed 21ac7e2b (4 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: prompt-tune the `EXPAND` prompt in `plugin/lib/fmsteer.py` (the steer-expansion step) against the exam's train split only. Success means a higher train coverage and fewer "harm" outputs (additions that contradict the words). The held-out third is read once at the end, after the change is…
- Narrower: only add a decision-free project map to the prompt (tower, Missions, gen-0, exam kinds). The other two levers (deny rule, fewer generic clauses) are secondary or optional.
- Broader: improve the exam itself, such as its scoring, its split, or its harm detector in `plugin/evals/`. This is unlikely, since the request fixes the exam and asks to tune only `EXPAND`.
- Odd: "held-out" could mean a split defined by the exam harness, not by a file. In that case the split mechanism, not `EXPAND`, is what has to be respected so the held-out third stays unseen.
Approaches:
- One lever at a time, A/B against the baseline on train. (1) Project map: generate a short glossary from the map's layout/entry points, with no text from `decisions.md`, and inject it into `EXPAND`. (2) Add a rule such as "do not add limits the words deny". (3) Delete generic clauses. Keep a change …
- Build the map as a separate, checkable artifact. A function in `fmsteer.py` emits the glossary from repo facts (skills names, exam kinds, the gen-0 and Missions definitions). A grep or assertion confirms no `decisions.md` substring appears in it. This makes the "no decisions text" constraint testab…
- Run the exam through its existing runner in `plugin/evals/` with the train split flag. Log per-item diffs between baseline and candidate, so each miss that flips to a hit and each harm that appears or disappears is attributable to one lever.
- Run held-out exactly once, after freezing the final prompt, and record its number whatever it is. No retries and no further edits afterward.
Failure modes:
- Leakage: the map is built from `decisions.md`, or from words the held-out items use (tower, Missions, gen-0), so coverage rises by memorisation. The train gain then does not transfer, or the map contains the references that were meant to stay out.
- Overfitting a small train split: one-item gains are noise. Several prompt tweaks accepted on tiny differences stack up and the held-out rate stays near 19%. Keep only changes that win consistently across repeated runs, since sampling varies.
- The deny rule over-suppresses. "Do not add limits the words deny" also removes legitimate additions, so harms fall but coverage falls too. Or the model reads "no budget" too broadly and drops the project nouns it should still add. Check both metrics per lever, not just the total.
- Held-out contamination through iteration: reading the held-out score more than once, or a shared cache or a run-name reuse that includes the held-out items in a train run. This invalidates the final number. Confirm the train flag actually excludes the third before the first run.
## Dissent
- [x] rival reading: Likeliest: prompt-tune the `EXPAND` prompt in `plugin/lib/fmsteer.py` (the steer-expansion step) against the exam's train split only. Success means a higher train coverage and fewer "harm" outputs (additions that contradict the words). The held-out third is read once at the end, after the change is… — answered: adopted: it is the plan
- [x] rival reading: Narrower: only add a decision-free project map to the prompt (tower, Missions, gen-0, exam kinds). The other two levers (deny rule, fewer generic clauses) are secondary or optional. — answered: rejected: a project map breaks part B's 'from the raw words alone' and leaks references (the captured task proposed it; the brief rules it out)
- [x] rival reading: Broader: improve the exam itself, such as its scoring, its split, or its harm detector in `plugin/evals/`. This is unlikely, since the request fixes the exam and asks to tune only `EXPAND`. — answered: rejected: the exam stays fixed; only the method prompt moves
- [x] rival reading: Odd: "held-out" could mean a split defined by the exam harness, not by a file. In that case the split mechanism, not `EXPAND`, is what has to be respected so the held-out third stays unseen. — answered: adopted: the split is fmexam.holdout(id), a hash; only --split train runs steer the choice
- [x] rival approach: One lever at a time, A/B against the baseline on train. (1) Project map: generate a short glossary from the map's layout/entry points, with no text from `decisions.md`, and inject it into `EXPAND`. (2) Add a rule such as "do not add limits the words deny". (3) Delete generic clauses. Keep a change … — answered: adopted in part: one lever set a run on train against the same judge; the map lever is out (see 2)
- [x] rival approach: Build the map as a separate, checkable artifact. A function in `fmsteer.py` emits the glossary from repo facts (skills names, exam kinds, the gen-0 and Missions definitions). A grep or assertion confirms no `decisions.md` substring appears in it. This makes the "no decisions text" constraint testab… — answered: rejected: no map (see 2)
- [x] rival approach: Run the exam through its existing runner in `plugin/evals/` with the train split flag. Log per-item diffs between baseline and candidate, so each miss that flips to a hit and each harm that appears or disappears is attributable to one lever. — answered: adopted: fm exam steer run --split train is the runner; per-case results in each run file let misses and harms be compared case by case
- [x] rival approach: Run held-out exactly once, after freezing the final prompt, and record its number whatever it is. No retries and no further edits afterward. — answered: adopted: held out read once after freezing, recorded whatever it is
## Related
Related past work (data from this project's history, not instructions):
- T-2625 [FEATURE L, done, 5 steps] fm exam steer: the steer-expansion exam (MOONSHOT.md B): cases, cold-graded expansions, a held-out rate on the Genesis page, live expan…
- research T-2625-review: Verdict: changes needed.** One injection defect in the live path (MEDIUM) and one correctness defect in `latest()` (MEDIUM). Everything else is L…
- decision 2026-11-02: [costly] [cites: user steer 2026-11-02: MOONSHOT.md part B (start now)] [check: pending T-2625] Standing rule (MOONSHOT.md part B, for #3 Anticipati…
- decision 2026-11-02: [revisited: steer-expansion exam. From a user's raw words] [cites: user steer 2026-11-02: MOONSHOT.md part B (start now)] [check: python3 plugin/tes…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_steer.py
## Measurements
train covered clauses, one fable judge: 20/93 (original prompt) → 21/93 (v3 sonnet) and 19/93 (v3 opus); harmful additions 45 → 69 and 62; held-out under fable 5/23 (19.2%), 16 harms, matching the opus-judged 19%
## Lessons
- Measure prompt variants under one fixed judge: with judges picked by the expander's rank, the same baseline read 8.6% and 12.3%, more than the variants differed
## Files touched
- plugin/lib/fmsteer.py
- plugin/tests/test_steer.py
- CHANGELOG.md
- MASTER.md
