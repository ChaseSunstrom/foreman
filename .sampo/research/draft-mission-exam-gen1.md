# Mission — the exam (gen 1, #13 + #6)

Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).

Self-contained for a fresh `fm run` in ~/.claude/foreman. Parent: gen-1/seed.md → gen-0.md §4.

## Capability (gen-0 §4)
Locally generated throwaway repos in at least 6 languages with planted defects (bugs, vulns, missing tests, slow
paths, docs drift, a flaky test, a broken dep) plus vague goals, ambiguous requests, a task needing a missing tool and
"no request" scenarios, all with hidden answer keys. One third held out for grading only. Scores to
research/genesis/exam.jsonl: found vs key, false alarms, readings/approaches vs key, failing-test-first fixes, tokens
per verified result.

## Gaps this Mission targets (gap-map #13, cross-cutting "No exam exists"; built in T-2079, open until the end-of-run exam shows them closed)
- Multi-language exam generator with hidden keys and holdout — tier 3.
- exam.jsonl scoring that every later Mission, critique and selection reads (found, false alarms and hidden-check
  fixes; tf-first is shown but read by none of them until T-2170) — tier 3.
- A free, deterministic agent arm (Foreman's own finders) so every task can re-run the exam without paid sessions — tier 3.

## Toolchains here
python3, node 26 (runs .ts by type stripping), cargo/rustc, ruby (no minitest: plain asserts), gcc, bun. No javac,
no go. Six runnable languages: Python, JavaScript, TypeScript, Rust, Ruby, C.

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
  recorded beside its score (fmbench._session). Gap: `--budget` defaults to $2 a session, which is a dollar cap on
  proving that gen-0's "no spend cap on building and proving" rules out; T-2179 drops it for the exam arms (the
  timeout stays as the runaway stop).
- `fm exam grade RUN`: per scenario, findings (captured tasks in the scenario's Foreman state + the reply) matched to
  the key by file + symbol; false alarms; hidden checks run for fixes; a fix counts as failing-test-first when the
  agent's own tests fail on the original planted file (limit: any failing test counts, even one unrelated to the
  defect; T-2170 makes an outside check decide, so tf-first is smoke until then). Appends one line per run to research/genesis/exam.jsonl
  (split, agent, found/keyed, false alarms, readings hit, fixes, tf-first, cost, tokens per verified result).
- `fm exam` (status): last runs and scores, train vs holdout.

## Exam of the exam (its own held-out checks)
1. Every generated repo builds and its visible tests pass (the defect is hidden, not a broken build) — except flaky
   (passes most runs) and dep (fails to import by design).
2. Every hidden check fails on the planted repo and passes on the clean render of the same scenario.
3. A perfect oracle agent (the key itself as findings, the clean render as the fix) scores 100% found, 0 false alarms,
   and every fix passes its hidden check; an empty agent scores 0 found. tf-first isn't part of this calibration:
   until T-2170 it counts any failing test, so it's reported, never calibrated on.
4. Holdout ids never appear in a `--split train` generation.

## Done when
`fm exam gen/run/grade` work in all six languages; the four checks above are tests; the finders arm's baseline score
is in exam.jsonl; MASTER.md + CHANGELOG + site catalogue line; README names `fm exam` beside Genesis (open: T-2172);
`fm genesis` status shows the latest exam score; the exam arms run with no dollar cap (T-2179).

```
FEATURE: fm exam — multi-language generated exam with hidden keys, holdout third, finders + claude arms, exam.jsonl scores
DONE-WHEN: generated repos build and hidden checks fail-planted/pass-clean in python, js, ts, rust, ruby, c
DONE-WHEN: an oracle agent scores 100% and an empty agent 0%; holdout never leaks into --split train
DONE-WHEN: every surface it belongs on reads the scorecard: `fm exam scorecard` on the CLI, the site's Genesis page (section D), MCP for Desktop and other agents, and a pane line (the MCP tool and the pane line are T-2172)
DONE-WHEN: the exam arms run with no dollar cap (T-2179 removes `--budget`'s $2 default for them; the timeout stays as the runaway stop)
DONE-WHEN: `fm exam gen --author child` renders a tool-less child's plants for every kind it can author (`fmexam.CHILD_KINDS`), and those, not the template set, are the scored held-out third
```
