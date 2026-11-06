# Critique — Mission 3, Initiative (gen 1, #1)

Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
the exam forced: T-2202, T-2203, T-2204, T-2211, T-2217, T-2219, T-2222 (done), and the coverage refresh T-2223. Mission: gen-1/mission-initiative.md.

## Exam scenarios: built vs planned (nothing counts closed until the end-of-run exam)
| Planned | State |
|---|---|
| Exam contract repaired: README run command, edge contract, a proven unkeyed finding is an exam defect | built — T-2120, test_exam |
| Deterministic, language-agnostic finders, zero on every clean render | built — T-2121 (fm find); s31-006 closed its 3 clean scenarios (python, ruby, rust) with 0 false alarms; s0-001: 90/108 planted defects found, 0 false alarms |
| find → prove → fix: a finding counts only with a proof | built for untested, docs, dep and secret only — fm prove (T-2122, consent fixed in T-2202) and fm prove --capture plus /foreman:initiative (T-2123); bug, vuln, slow and flaky stay leads until a failing test shows them (T-2199, open) |
| Project scout: proven only, at most 3 a day, refutation ledger | built — T-2124 |
| Value ranking with per-finder precision | built — T-2125 |
| #1 held-out exam: I-none, I-rank, I-clean, child-authored | built, unmeasured — T-2126; every exam kind has had an outside author since T-2211 and T-2217, and only those results count (T-2204). No child-authored #1 run has been graded on the production model, so every row of #1 is open; recall per language and per bug type (the detection-ladder steer) waits on T-2185, and the long-horizon tier, the deciding score, runs only at the end |
| Long-horizon tier: the deciding end-of-run score | not run — it runs once, on the production model, as part of T-2077's end-of-run exam (gen-0 DONE-WHEN); its scenarios are the held-out long tasks |
| Detection ladder (the user's later steer): stack tools, tree-sitter rules, dynamic signals, hotspot review, every miss a rule | open — T-2185; recall per language and kind landed (T-2233) |
| Surfaces: fm code, MCP, AGENTS.md (other agents), site, pane, Desktop | partial, so #1 isn't done under gen-0's every-surface rule — built for fm code, MCP, AGENTS.md, site and pane (T-2127); Desktop not built (T-2232): it would reach #1 only through the MCP server |

Four rows (exam contract, finders, scout, ranking) are built with their tests; find → prove → fix covers four of its
eight kinds; the #1 exam is built but unmeasured; the surfaces row lacks Desktop. None is closed until #1's held-out
exam runs on the production model at the end of the run (gen-1/seed.md rule 6). The fm exam scorecard shows #1 as
"too few".

## Outside signals
- fm outcomes (survival, which Foreman doesn't author): T-2120 was fixed later (by T-2170), so it is lost; the other
  fourteen are held and settling, 30 days left in the window, which is survival so far, not proof.
- No review by a model outside Claude has run: no local model is installed, and sending the code to another provider
  is an outward step that waits on the user's grant (final report).

## Smoke signal (Haiku: shown, moves nothing)
- s31-006, 9 held-out I-none, I-rank and I-clean scenarios with 18 keyed defects, written by a tool-less child and by
  Foreman (author child+self, so not the outside-authored kind that counts, T-2204): oracle 18/18; finders 16/18
  found, 0 fixed, 0 false alarms; plain 6/18 found, 11 fixed, 6 false alarms; foreman 15/18 found, 17 fixed, 4 false
  alarms. It decides nothing. T-2184 then added the SessionStart leads note for the user's steer that every capability
  needs a real session path; no run has measured whether it changes these numbers.

## Inside signals (same model family: not outside evidence)
- A cold Haiku review of #1's code (a smaller model of the builder's family; research/haiku-review-initiative.md)
  found 6 issues. Two are confirmed in the code: fm find never scans tracked dot-directories (.github/workflows
  included), and `fm prove --capture` files leads with no daily or open-task cap. All are filed as T-2235.
- **s0-001:** the scorecard's top gap read "finders 30/36 where foreman found 1/36". That compared a 36-scenario
  line with a 1-scenario smoke line; T-2219 now compares arms only on the same scenarios. s0-001 has no same-scenario
  foreman run, so it now shows no gap either way.
- Reviews of the shipped code, not the exam, found the defects that mattered: forgeable run consent (T-2122's
  review, fixed by T-2202), test-first credit for a red caused by the grader's own damage (T-2203), template-written
  scenarios on the scorecard (T-2204), and a lane criterion that went green unrun (T-2123's review). Each review was
  one read-only foreman:fm-reviewer subagent of the same model family as the builder, so not an outside model; its
  findings were checked before fixing.

## Coverage cells filled
coverage.md was re-filed through its cold read and one code-reading review (T-2223). Initiative has 8 of its 64
cells filled, each naming its file in coverage.md: find × CLI (fmfind.py), find × MCP (fmmcp.py), verify × CLI
(fmprove.py), build × CLI (fmdraft.py), build × Claude Code (fmfind.py), plan × Claude Code (the brainstorm skill),
operate × CLI (fmorders.py) and operate × Claude Code (fmscout.py). The other 56 are open; the next Seed fills the
find cells first: Claude Code, fm code, other agents, Desktop, site and headless/server (the leads note's cell:
T-2230; Desktop: T-2232).

## Not-yet items
None: nothing for #1 has failed two approaches.

## Open work, each tracked
- Proofs for bug, vuln, slow and flaky findings: T-2199.
- Finder recall per language and per bug type: T-2185.
- A measured run of the SessionStart leads note: T-2230.
- The cold review's fixes, security first: T-2235.
- #1 on Desktop: not built; Desktop reaches fm find only through the MCP server, and no Desktop run or test exists
  (T-2232).

## What failed
1. The first fm prove trusted a tree whose last commit carried the user's email, so a cloned repo could forge
   consent to run its tests. Lesson: consent comes only from the user's own command; anything in the tree is a claim.
   Its rule and checks: `fm prove --yes-run` is user-only in the guard (test_guard's self-authorize rows) and
   test_find's test_your_email_on_head_is_no_consent_only_your_yes_run_is_and_it_is_remembered.
2. Three scoring flaws reached main, and neither a failing test nor the exam caught them: over-credited test-first
   (T-2203), self-authored scenarios counted (T-2204), and a sample-size artefact read as a top gap (T-2219). Each
   was found by a review or by reading the output, not by a failing test. Lesson: every score change gets a test that
   feeds it the case it would get wrong; each fix landed with one. T-2222's `.fmproved` now refuses a change to the
   exam and scorecard code without a red→green proof (test_finish_proved). That proves each change has a test, not
   that the next scoring flaw gets caught.
3. Proofs exist only for four of the eight kinds #1 names; the other four are leads, so the pipeline can't yet
   close a bug end to end from a proof. Tracked as T-2199.
4. The coverage refresh couldn't be filed: the cold read deadlocked on its own earlier findings once a flagged
   line was edited or removed. Lesson: a reviewer's memory must follow the text it judges. Fixed with a test:
   findings follow an edited line and end with a removed one (T-2228).
5. #1's own exam shows where it falls short: the finders found 0 of s0-001's 18 planted bugs (T-2233's per-kind
   recall; every other kind was found in full), because fm find has no bug finder (T-2242), and on s31-006 they fixed
   nothing.

## What the next Seed should change
- It opens with #1's top gap: the free finders arm ahead of the session on s31-006 (16/18 vs 15/18 found). T-2184's
  leads note and T-2242's bug rung are the changes the end-of-run exam on the production model measures; a Haiku run
  decides no selection, so the gap stays open until then, and with this mission's outside signals weak, that exam
  decides it.
- It fills Initiative's open find cells first, as every Seed does.
- Mission work starts from T-2235's security fixes, then T-2199: a failing-test proof for bug, vuln, slow and flaky,
  so the find → prove → fix loop covers every kind #1 names. Each of those tasks closes with its red→green proof;
  #1 itself stays open until its held-out exam on the production model, at the end of the run.
