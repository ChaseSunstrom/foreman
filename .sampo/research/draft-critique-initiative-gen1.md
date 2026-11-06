# Critique — Mission 3, Initiative (gen 1, #1)

Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
the exam forced: T-2202, T-2203, T-2204, T-2211, T-2217, T-2219 (done). Mission: gen-1/mission-initiative.md.

## Exam scenarios: built vs planned (nothing counts closed until the end-of-run exam)
| Planned | State |
|---|---|
| Exam contract repaired: README run command, edge contract, a proven unkeyed finding is an exam defect | built — T-2120, test_exam |
| Deterministic, language-agnostic finders, zero on every clean render | built — T-2121 (fm find); s0-001 finders arm 90/108 found, 0 false alarms; s7-004 20/24 |
| find → prove → fix: a finding counts only with a proof | built for untested, docs, dep and secret only — fm prove (T-2122, consent fixed in T-2202) and fm prove --capture plus /foreman:initiative (T-2123); bug, vuln, slow and flaky stay leads until a failing test shows them (T-2199, open) |
| Project scout: proven only, at most 3 a day, refutation ledger | built — T-2124 |
| Value ranking with per-finder precision | built — T-2125 |
| #1 held-out exam: I-none, I-rank, I-clean, child-authored | built — T-2126; since T-2211 and T-2217 every exam kind has an outside author, and since T-2204 only those results count. No child-authored #1 run has been graded on the production model, so every row of #1 is open. Recall per language and per bug type (steer 4) isn't reported yet: T-2185 (open) adds it, so the counts below are aggregates |
| Surfaces: fm code, MCP, AGENTS.md (other agents), site, pane, Desktop | built for fm code, MCP, AGENTS.md, site and pane — T-2127; Desktop unproven: it would reach #1 only through the MCP server, and no Desktop run or test exists; coverage.md lags (below) |

Seven of the seven rows are built with their tests; none is closed, because #1's held-out exam hasn't run on the
production model (gen-1/seed.md rule 6). The fm exam scorecard shows #1 as "too few".

## Outside signals
- **s31-006 (9 held-out I-none, I-rank and I-clean scenarios, 18 keyed defects, a Haiku smoke run that decides
  nothing):** the newest rows are oracle 18/18; finders 16/18 found, 0 fixed, 0 false alarms; plain 6/18 found,
  11 fixed, 6 false alarms; foreman 15/18 found, 17 fixed, 4 false alarms.
- **s0-001:** the scorecard's top gap read "finders 30/36 where foreman found 1/36". That compared a 36-scenario
  line with a 1-scenario smoke line; T-2219 now compares arms only on the same scenarios, and the gap is gone.

## Inside signals (same model family: not outside evidence)
- Reviews of the shipped code, not the exam, found the defects that mattered: forgeable run consent (T-2122's
  review, fixed by T-2202), test-first credit for a red caused by the grader's own damage (T-2203), template-written
  scenarios on the scorecard (T-2204), and a lane criterion that went green unrun (T-2123's review). Each review was
  one read-only foreman:fm-reviewer subagent of the same model family as the builder, so not an outside model; its
  findings were checked before fixing. No fix among them has been reverted (git log), which is survival so far, not
  proof.

## Coverage cells filled
coverage.md lists 5 Initiative cells filled (find × CLI, find × headless, plan × Claude Code, build × CLI,
operate × CLI) and 4 marked I. It lags the code: find × MCP and find × fm code were built by T-2127, and find ×
Claude Code by the session-start leads note (T-2184); `fm genesis check` still counts them empty.

## Not-yet items
None filed for #1.

## What failed
1. The first fm prove trusted a tree whose last commit carried the user's email, so a cloned repo could forge
   consent to run its tests. Lesson: consent comes only from the user's own command; anything in the tree is a claim.
   Its rule and checks: `fm prove --yes-run` is user-only in the guard (test_guard's self-authorize rows) and
   test_find's test_your_email_on_head_is_no_consent_only_your_yes_run_is_and_it_is_remembered.
2. Three scoring flaws reached main, and neither a failing test nor the exam caught them: over-credited test-first (T-2203), self-authored
   scenarios counted (T-2204), and a sample-size artefact read as a top gap (T-2219). Each was found by a review
   or by reading the output, not by a failing test. Lesson: every score change gets a test that feeds it the case
   it would get wrong. Its checks landed with each fix: test_exam's putback and load-error cases (T-2203),
   test_genesis's outside-author cases (T-2204) and the unequal-sample case (T-2219).
3. Proofs exist only for four of the eight kinds #1 names; the other four are leads, so the pipeline can't yet
   close a bug end to end from a proof. Tracked as T-2199.

## What the next Seed should change
- Mission work starts from T-2199: a failing-test proof for bug, vuln, slow and flaky, so the find → prove → fix
  loop covers every kind #1 names.
- Refresh coverage.md from the code before the next critique, so built cells stop reading empty.
- Open with the top gap steer 3 names: on s31-006's same 9 scenarios the free finders found 16/18 and the foreman
  session 15/18, so the session doesn't use all of fm find's output. It is a Haiku smoke signal, so it sets the next
  Seed's first work and decides no selection or lean change; the end-of-run exam on the production model measures it.
