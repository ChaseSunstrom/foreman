# Mission — the exam (gen 1, #13 + #6)

Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).

Self-contained for a fresh `fm run` in ~/.claude/foreman. Parent: gen-1/seed.md → gen-0.md §4.

## Capability (gen-0 §4)
Locally generated throwaway repos in at least 6 languages with planted defects (bugs, vulns, missing tests, slow
paths, docs drift, a flaky test, a broken dep) plus vague goals, ambiguous requests, a task needing a missing tool and
"no request" scenarios, all with hidden answer keys. One third held out for grading only. Scores to
research/genesis/exam.jsonl: found vs key, false alarms, readings/approaches vs key, failing-test-first fixes, tokens
per verified result.

## Gaps closed (gap-map #13, cross-cutting "No exam exists")
- Multi-language exam generator with hidden keys and holdout — tier 3.
- exam.jsonl scoring that every later Mission, critique and selection reads — tier 3.
- A free, deterministic agent arm (Foreman's own finders) so every task can re-run the exam without paid sessions — tier 3.

## Toolchains here
python3, node 26 (runs .ts by type stripping), cargo/rustc, ruby (no minitest: plain asserts), gcc, bun. No javac,
no go. Six runnable languages: Python, JavaScript, TypeScript, Rust, Ruby, C.

## Approaches
A. **Chosen** — one small app API described once (functions + cases), rendered per language; each defect kind is a
   variant of one function body or file; a seeded generator picks language × defects × names, writes the repo, keeps
   the key and the hidden checks outside it. Varied by seed, so it can't be memorised; keys are true by construction.
B. Hand-written fixture repos in bench/: fixed, memorisable, the held-out third leaks the moment anyone reads it.
C. **Also chosen (standing rule 5)** — a separate tool-less child (`fm exam gen --author child`) writes whole scenarios
   from the scenario format alone, never Foreman's code or the Missions; the harness keeps only those that pass the
   exam of the exam below. Outside-authored, so its held-out scores rank gaps; A stays the free fixture and reference
   author (`--author self`), and each result records its author.
D. Plant into the project's own code (fmbench's planted-bug): one language, no request-shape scenarios. Kept as is.

## Design
- `fm exam gen [--seed N] [--per-kind 9] [--lang L,..] [--kind K,..] [--split train|holdout|all]` → `<p.dir>/exam/<run>/<scenario>/repo` (a git
  repo, one commit) and `.../key.json` + `.../hidden/` (outside the repo). Split by stable hash of the scenario id; per kind, candidates are drawn until each split's quota is full: held out = (n+2)//3 (9 → 3), train = the rest, so every capability exam has ≥ 9 scenarios and ≥ 3 held out.
- Scenario kinds: bug, vuln, untested, slow, docs, flaky, dep (one planted defect, request names the area or none),
  vague ("make this faster"/"make this great": key lists readings and approach keywords), ambiguous (two readings
  the key names both of), missing-tool (key: a capability miss recorded, no false done), none (3–4 defects, no request).
- Every scenario's key.json carries its own commands (suite build/run, each hidden check's file and command), so the
  grader reads only key.json + hidden/ and a child-authored scenario grades the same as a template one.
- `fm exam run RUN --agent oracle|empty|finders|foreman|plain [--split …]`: oracle/empty calibrate; finders =
  Foreman's deterministic finders, no session; foreman = one headless session per scenario with the plugin; plain =
  the same session without it (the head-to-head of rule 5, same held-out scenarios), budgeted (fmbench._session).
- `fm exam grade RUN`: per scenario, findings (captured tasks in the scenario's Foreman state + the reply) matched to
  the key by file + symbol; false alarms; hidden checks run for fixes; a fix counts as failing-test-first when the
  agent's own tests fail on the original planted file. Appends one line per run to research/genesis/exam.jsonl
  (split, agent, found/keyed, false alarms, readings hit, fixes, tf-first, cost, tokens per verified result).
- `fm exam` (status): last runs and scores, train vs holdout.

## Exam of the exam (its own held-out checks)
1. Every generated repo builds and its visible tests pass (the defect is hidden, not a broken build) — except flaky
   (passes most runs) and dep (fails to import by design).
2. Every hidden check fails on the planted repo and passes on the clean render of the same scenario.
3. A perfect oracle agent (the key itself as findings, the clean render as the fix) scores 100% found, 0 false alarms,
   all fixes failing-test-first; an empty agent scores 0 found.
4. Holdout ids never appear in a `--split train` generation.

## Done when
`fm exam gen/run/grade` work in all six languages; the four checks above are tests; the finders arm's baseline score
is in exam.jsonl; MASTER.md + CHANGELOG + site catalogue line; `fm genesis` status shows the latest exam score.

```
FEATURE: fm exam — multi-language generated exam with hidden keys, holdout third, finders + claude arms, exam.jsonl scores
DONE-WHEN: generated repos build and hidden checks fail-planted/pass-clean in python, js, ts, rust, ruby, c
DONE-WHEN: an oracle agent scores 100% and an empty agent 0%; holdout never leaks into --split train
```
