# Mission — the exam (gen 1, #13 + #6)

Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).

Scope: #13's exam (gen-0 §4) and #6 Verifying anything in the part the exam proves: a fix counts only when a
hidden check outside the repo passes, a reading only when it matches the key's readings ("does it do what the user
meant"), and a result that proves nothing is labelled (errored, smoke, provisional), never scored. #6's other proofs
(UI, data, infra and ops, the unproven rollup) are Mission 7's (mission-proof.md, seed row 7).

Self-contained for a fresh `fm run` in ~/.claude/foreman. Parent: gen-1/seed.md → gen-0.md §4.

## Charter (binds this Mission as written)
gen-0's lines, verbatim:
- MUST: full autonomy. Every decision through fm decide. Never ask me anything mid-run.
- MUST: no spend cap on building and proving. Tokens go into Foreman's code and its tests, not into sweeping the outside world. Waiting out a usage limit is fine.
- MUST: everything finishes completely. A capability is done only when it has its tests, its exam scenarios passing (§4), docs (MASTER.md, README where it belongs, CHANGELOG), a site page if it's user-facing, a pane/status surface if it has state, and it works on every surface it belongs on (Claude Code, fm code, other agents, Desktop).
- MUST: unprompted actions stay local and reversible (a lane, a branch, a spike, a throwaway folder). Anything that leaves the machine needs its grant, so it goes into the final report.
- NEVER: clone or sweep outside repos to brainstorm or to benchmark. Outside material is only allowed in the targeted form in §5.
- NEVER: grant yourself anything or lower your own guard. Protected core gets a built, evaluated candidate in a worktree plus `fm ask ID core` at the end. Merging Foreman changes stays my call.

Standing intent (plugin/templates/standing-intent.md), verbatim:
A harness that figures out and does everything itself. The user's only jobs are gen-0's goals and a yes to what leaves the machine or touches protected core. Every steer is a miss to learn from.

1. Anticipate: generalize the pattern behind each steer; before filing a tower doc, ask what the user would say if they read it now, and act on that first; more ambitious, complete, general and honest, with less hand-holding.
2. Act, don't advise: a capability counts only when real sessions use it by default; one a session doesn't call is a top gap.
3. Next-level, not polish: tier 3-4 first, one moonshot a generation, nothing killed for ambition; a failure goes to not-yet and is retried.
4. Complete, and the frame grows: a capability is done with its tests, exam, docs and every surface; new capabilities, rows, lenses and exam kinds are added with evidence.
5. General: ecosystem tools, structure-aware parsing and runtime signals over hand-written rules.
6. Truth over self-image: signals Foreman didn't author; a check that measures format instead of substance is a bug.
7. Spend where it decides something.
8. Every lesson becomes code: a rule plus an automatic check, in the same task.
9. Never trade safety for autonomy.

## Capability (gen-0 §4)
Locally generated throwaway repos in at least 6 languages with planted defects (bugs, vulns, missing tests, slow
paths, docs drift, a flaky test, a broken dep) plus vague goals, ambiguous requests, a task needing a missing tool and
"no request" scenarios, all with hidden answer keys. One third held out for grading only. Scores to
research/genesis/exam.jsonl: found vs key, false alarms, readings/approaches vs key, failing-test-first fixes, tokens
per verified result.

## Gaps this Mission targets (gap-map #13, cross-cutting "No exam exists"; tooling built in T-2079; each gap stays open until a scored, child-authored held-out run in the end-of-run exam shows it closed)
- Multi-language exam generator with hidden keys and holdout — tier 3.
- exam.jsonl scoring that every later Mission, critique and selection reads (found, false alarms and hidden-check
  fixes; tf-first counts toward closing a scenario) — tier 3.
- A free, deterministic agent arm (Foreman's own finders) so every task can re-run the exam without paid sessions — tier 3.
  It costs nothing; it doesn't score well (it finds and never fixes: 0 fixes on s0-001 and s7-004), and the exam says so.

## Toolchains here
python3, node 26 (runs .ts by type stripping), cargo/rustc, ruby (no minitest: plain asserts), gcc, bun. No javac,
no go. Six runnable languages: Python, JavaScript, TypeScript, Rust, Ruby, C, each re-proven per run by the exam of
the exam's check 1 (`fm exam check RUN` builds every rendered repo and runs its hidden checks; test_exam renders all six).

## Approaches
A. **Chosen** — one small app API described once (functions + cases), rendered per language; each defect kind is a
   variant of one function body or file; a seeded generator picks language × defects × names, writes the repo, keeps
   the key and the hidden checks outside it. Varied by seed, so no single scenario's text can be memorised, but the template set
   itself is learnable, which is why C's outside author writes the scored held-out third; keys are true by construction.
B. Hand-written fixture repos in bench/: fixed, memorisable, the held-out third leaks the moment anyone reads it.
C. **Also chosen (standing rule 5)** — a separate tool-less child (`fm exam gen --author child`) writes whole scenarios
   from the scenario format alone, never Foreman's code or the Missions; the harness keeps only those that pass the
   exam of the exam below. Outside-authored, so its held-out scores rank gaps; A stays the free fixture and reference
   author (`--author self`), and each result records its author.
D. Plant into the project's own code (fmbench's planted-bug): one language, no request-shape scenarios. Kept as is.

## Design
- `fm exam gen [--seed N] [--per-kind 9] [--lang L,..] [--kind K,..] [--split train|holdout|all] [--author self|child]` (default self: free and deterministic, the fixture the zero-token arms and
  tests run on, never a ranking score; a run that ranks gaps passes `--author child`, each result records its author,
  and a held-out kind the child can't author yet ranks nothing until it can; standing rule 5) (child: the tool-less outside author of C, which never sees Foreman's code or the Missions; self: the template reference) → `<p.dir>/exam/<run>/<scenario>/repo` (a git
  repo, one commit) and `.../key.json` + `.../hidden/` (outside the repo). With the 11 kinds above that is 99 scenarios, 33 held out (s0-001 is that run; its 108 keyed defects, 36 in the
  held-out third, count defects, not scenarios). Split by stable hash of the scenario id; per kind, candidates are drawn until each split's quota is full: held out = (n+2)//3 (9 → 3), train = the rest, so every capability exam has ≥ 9 scenarios and ≥ 3 held out.
- Scenario kinds: bug, vuln, untested, slow, docs, flaky, dep (one planted defect, request names the area or none),
  vague ("make this faster"/"make this great": key lists readings and approach keywords), ambiguous (two readings
  the key names both of), missing-tool (key: a capability miss recorded, no false done), none (3–4 defects, no request).
- Every scenario's key.json carries its own commands (suite build/run, each hidden check's file and command), so the
  grader reads only key.json + hidden/ and a child-authored scenario grades the same as a template one.
- `fm exam run RUN --agent oracle|empty|finders|foreman|plain [--split …]`: oracle/empty calibrate; finders =
  Foreman's deterministic finders, no session; foreman = one headless session per scenario with the plugin; plain =
  the same session without it (the head-to-head of rule 5, same held-out scenarios), each with its cost
  recorded beside its score (fmbench._session). foreman and plain are paid: they run in the end-of-run exam and for a
  regressing capability only (steer 1). `--budget` no longer defaults to $2 a session (T-2179: a
  dollar cap on proving is what gen-0's "no spend cap on building and proving" rules out); the timeout stays as the
  runaway stop.
- `fm exam grade RUN`: per scenario, findings (captured tasks in the scenario's Foreman state + the reply) matched to
  the key by file + symbol; false alarms; hidden checks run for fixes; a fix counts as failing-test-first when the
  agent's suite passes on its fix and fails with the planted file put back; the planted and clean files differ only at
  the defect, so a red there is the defect caught (limit, open: an arm that also changed other code in that file can
  go red for that and be credited; T-2203 puts back only the defect's lines and credits nothing when they no longer
  apply). Appends one line per run to research/genesis/exam.jsonl
  (split, agent, found/keyed, false alarms, readings hit, fixes, tf-first, cost, tokens per verified result).
- `fm exam` (status): last runs and scores, train vs holdout.
- `fm exam scorecard`: one row per capability from held-out, non-smoke lines; a capability whose free arm beats its
  session arm prints first as `top gap:` (steer 3, `fmgenesis.free_beats`). Open (T-2204): it counts template
  (`self`) held-out scenarios too, which the Design above says never rank; until T-2204 lands its rates are provisional. The next seed opens with the same check
  on train lines as `Top gap:` (T-2184): held-out lines only grade, so no seed ever reads them.
- Session paths: the Genesis line every session starts with names the next step (fmgenesis.step). Once a
  generation's Missions and critiques are in, that step is `fm genesis select N`, which refuses without a graded line
  and names `fm exam run RUN --agent A`, then `fm exam grade RUN --agent A`; `fm genesis check` and sweep's exam row
  say the same. So a session reaches the exam by following its next step: per generation the zero-token arms (steer 1), and the
  paid arms only in the end-of-run exam.

## Exam of the exam (its own held-out checks)
1. Every generated repo builds and its visible tests pass (the defect is hidden, not a broken build) — except flaky
   (passes most runs) and dep (fails to import by design).
2. Every hidden check fails on the planted repo and passes on the clean render of the same scenario.
3. A perfect oracle agent (the key itself as findings, the clean render as the fix) scores 100% found, 0 false alarms,
   and every fix passes its hidden check; an empty agent scores 0 found. tf-first isn't part of this calibration:
   it judges the arm's own tests, which an oracle doesn't write, so it's reported, never calibrated on.
4. Holdout ids never appear in a `--split train` generation.

## Done when
`fm exam gen/run/grade` work in all six languages; the four checks above are tests; the finders arm's baseline score
is in exam.jsonl; MASTER.md + CHANGELOG + site catalogue line; README names `fm exam` beside Genesis; MCP `exam_scorecard` and the Genesis line show it (T-2172; seen live 2026-10-30: session start printed "Genesis: gen 1 · exam 0/13 pass, 4 Haiku skipped");
`fm genesis` status shows the latest exam score; the end-of-run exam's session arms are scored with none cut off by a dollar cap (T-2179 removed the default cap; open until that exam runs).

```
FEATURE: fm exam — multi-language generated exam with hidden keys, holdout third, finders + claude arms, exam.jsonl scores
DONE-WHEN: generated repos build and hidden checks fail-planted/pass-clean in python, js, ts, rust, ruby, c
DONE-WHEN: an oracle agent scores 100% and an empty agent 0%; holdout never leaks into --split train
DONE-WHEN: every surface it belongs on shows the numbers `fm exam scorecard --json` computes from exam.jsonl (passing capabilities, smoke lines skipped): the CLI, the site's Genesis page (section D, from `fm genesis export`), MCP `exam_scorecard` for Desktop and other agents, the pane and fm code's status (the Genesis line, T-2172); a test seeds exam.jsonl and compares each surface's numbers to the scorecard's, not just that a line appears
DONE-WHEN: the end-of-run exam's exam.jsonl lines show every production-model session arm on a held-out scenario scored, none errored by a dollar cutoff, judged on those lines, not on a unit test
DONE-WHEN: #13's `fm genesis exam` fails a drafted gen-0 missing any whole standing-intent clause (steer 7; T-2191, test_genesis), and every steer's rule carries its automatic check (`fm decide --check`)
DONE-WHEN: `fm exam scorecard` prints first a capability whose free arm beats its session arm on held-out lines, and the next seed opens with the same check run on train lines, since held-out lines only grade (steer 3)
DONE-WHEN: a test follows fmgenesis.step past a generation's Missions to `fm genesis select N` and gets a refusal naming `fm exam run` and `fm exam grade`, so a session reaches the exam by its next step
DONE-WHEN: test-first credit comes only from the defect's own lines put back, never from an arm's other edits in that file (T-2203)
DONE-WHEN: the scorecard ranks only child-authored held-out scenarios, never template ones (T-2204)
DONE-WHEN: each exam.jsonl line reports recall per language and per defect kind (steer 4; T-2185), so a blind spot in one language can't hide in the total
DONE-WHEN: the end-of-run exam's scored held-out third is child-authored (`fm exam gen --author child`) for every kind in `fmexam.CHILD_KINDS`; a kind the child can't author yet ranks nothing until it can (its template scenarios are labelled `self` and never ranked)
```

The DONE-WHEN lines are this Mission's finish line, not claims that it is met.

Status 2026-10-30, by DONE-WHEN line above. "Built" means code plus a unit test, named; none is exam-proven until the
end-of-run exam (steer 1). Lines 1-2 are about the exam's own soundness, not any arm's score (arms' scores, such as
s0-001's 13 false alarms, are what the exam reports):
1. built: `fm exam check` on s0-001; test_exam renders all six languages.
2. built: test_exam (oracle 100% found, empty 0; a train generation never holds a holdout id).
3. open: each surface shows the line; no test yet compares its numbers to the scorecard's (test_genesis checks the
   line's shape, test_mcp only a capability name).
4. open: needs the end-of-run exam.
5. built, and only a presence check: test_genesis drops each whole clause and expects `_misses` to fail the draft.
   A draft that repeats the clauses and ignores them still passes it; whether a generation acts on them is judged by
   drift and the critiques, and by the end-of-run exam. Each steer rule names its check with `fm decide --check`.
6. built: test_genesis (`top gap:` on held-out lines, `Top gap:` in the seed from train lines).
7. open: select's refusal names both verbs in code (fmgenesis.select), untested.
8. open: T-2203.  9. open: T-2204.  10. open: T-2185.  11. open: needs the end-of-run exam's child-authored run.

Spend (standing intent 7, steer 1): each generation runs only the zero-token arms (oracle, empty, finders) plus at
most one Haiku smoke run on 9 or fewer held-out scenarios, which never decides; production-model session arms run in
the end-of-run exam and for a capability that regresses. Every result records its cost beside its score (cost and
tokens per verified result in exam.jsonl). Deferring the paid head-to-head is the user's steer 1, so until the end-of-run
exam every selection is provisional and lineage.md says so. Foreman sets no cap on proving (gen-0); a budget the user sets with
`fm budget` is the user's own.
