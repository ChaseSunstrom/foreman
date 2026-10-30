# Critique — Mission 1, the exam (gen 1, #13 + #6)

Task: T-2079 (done; pushed to main at 1a78a3f on the user's push grant, a use the §8 report lists). Mission: gen-1/mission-exam.md.

## Exam scenarios: closed vs planned
| Planned | State |
|---|---|
| Generated repos build, visible tests pass (except flaky, dep) in python, js, ts, rust, ruby, c | closed — test_exam |
| Every hidden check fails planted, passes clean | closed — test_exam, all six languages |
| Oracle 100%, empty 0% | closed — test_exam; s0-001 empty row: 0/108 |
| Holdout never in `--split train` | closed — test_exam |
| ≥ 9 scenarios per kind, ≥ 3 held out | closed for Foreman's own generator only — `--per-kind 9` → 6 train + 3 held out per kind; these come from fmexam.py's templates, so the child-authored set the steer asks for is the next row, still open |
| Tool-less child author (standing rule 5) | built, not proven — `fm exam gen --author child`; its one real run kept 1 and the exam of the exam dropped 1, so its yield at ≥ 9 per capability is unmeasured (end-of-run exam) |
| Foreman vs plain session arms with cost | built, not yet measured — both arms run the same held-out scenarios, cost in `fm cost` under `exam-arm`, capped by `fm budget`; smoke so far: s0-001 (1 and 3 scenarios, below) and s31-006 (9 scenarios: foreman found 6/18, 7 false alarms, fixed 9/18; plain found 6/18, 6 false alarms, fixed 11/18); the deciding comparison is the end-of-run exam (gen-1/seed.md rule 6) |
| Finders baseline in exam.jsonl | closed — 0/108 (decision recorded 2026-10-28); revisited 2026-10-30 after fm find (T-2121): 90/108 found, 0 false alarms, held out 30/36, 0 fixed (finders find, never fix; T-2157) |

5 of the 8 rows are closed with their tests, and a sixth (≥ 9 per kind) only for Foreman's own generator; the child author and the arms comparison are built and smoke-tested, and both are decided at the end-of-run exam (gen-1/seed.md rule 6). None waits on the user.

## Outside signals
- **Session arms on s0-001 (smoke only, gen-1/seed.md rule 6).** exam.jsonl holds every graded line; the exam summary shows only
  the newest per run and agent. In order: (1) foreman and plain on 1 held-out scenario: both found 1/1, fixed 0/1
  (the work dir sat inside Foreman's state, see What failed 1); (2) the same pair after the temp-copy fix: both found
  1/1 and fixed 1/1, foreman at $0.34 and plain at $0.11 — the s0-001 (foreman) row the summary shows is this run,
  while its plain line was superseded by (3); (3) genesis and plain on 3 scenarios: the s0-001 (genesis) row, found
  3/3, 13 false alarms, fixed 0/3, and the s0-001 (plain) row, found 3/3, 9 false alarms, fixed 3/3. These are 1- and
  3-scenario samples, so no lean, cost or ranking change rests on them; the questions they raise for the end-of-run
  exam and the long-horizon tier are whether Foreman's extra cost buys anything on scenarios plain Claude misses
  (vague, none, missing-tool), and why the genesis arm fixed none. s31-006's 9-scenario smoke pair already leans the same way: plain fixed 11/18 to
  Foreman's 9/18 with one false alarm fewer.
- **Finders arm 0/108:** Foreman's deterministic finders (fmdocs.scan + fmsecrets) find none of the planted defects. Re-run 2026-10-30 (T-2157) with fm find in the arm: 90/108 found, 0 false alarms, held out 30/36 (zero tokens).
  At 0/108 the self-checks called those finders healthy (their own tests passed) while the exam said they found
  nothing; by standing rule 4 that made **#1 Initiative's finders a top gap** → Mission 3. After fm find they find
  90/108 but fix 0: finding is measured, fixing is still Mission 3's prove → fix gap.
- **fm outcomes (all time):** 1292 of 1337 finished tasks held (96.6%), 44 fixed later, 1 reverted. Close warnings on
  T-2079 itself: "suspiciously smooth: 16 runs passed the first time". Survival is good; first-try green is a sign the
  checks are too easy, not that the code is.
- **Cold reads:** this file, like every tower file, is filed only after `fm genesis put`'s cold Haiku read passes it
  (gen-1/seed.md rule 7, T-2166). The gen-level drift check (`fm genesis drift 1`, fm second over the whole generation) runs once
  gen 1's seed is filed.

## Coverage cells filled
coverage.md now exists (Mission 2). The cells this Mission's code fills there, both `F: plugin/lib/fmexam.py`:
Calibrated judgment's understand × CLI (the exam grades agents on held-out scenarios) and Genesis's build × CLI
(`fm exam gen` builds the exam). Its site section is Genesis page D; MCP, Desktop and pane cells are open (T-2172).

## Not-yet items
None added. Nothing here is a failed spike: the finders arm fixes 0 by design (finders find, T-2157), and the
genesis arm's 0/3 fixes on s0-001 is a #13 gap carried to Mission 2's critique and the end-of-run exam, not an idea
this Mission tried and dropped.

## What failed
1. First real session sample: the work dir sat under the project dir, so Foreman's own guard refused the agent's edits
   and both arms scored 0 fixed. Fixed by running sessions in a temp copy outside the project. Lesson: an exam arm
   must run where a user's repo would be, never inside Foreman's state.
2. A session that errored (rate limit, budget cap) was silently scored zero — a wrong "Foreman is weak" signal. Now
   counted as `errors` and shown as "N errored".
3. One planted bug per arm is too small a sample to rank anything. Cost per scenario ($0.11–0.34) makes a full
   held-out arm (33 scenarios) ~$4–11 per agent.

## What the next Seed should change
- ~~Every Mission's critique runs both session arms on ≥ 9 held-out scenarios~~ — superseded by the user's steer
  (2026-10-30): each generation runs the free deterministic arms on all scenarios plus at most a Haiku smoke run of
  foreman vs plain on ≤ 9 held-out ones (a smoke signal, never a verdict); the full arms and the long-horizon tier run
  once at the end on the production model.
- Add a **cost-per-verified-result** column to selection: a rewrite that ties on score at 3× the cost does not win.
- The child author should write the held-out third by default once it passes the exam of the exam reliably
  (currently 1 of 2 kept) — templates are memorisable by anything that reads fmexam.py.
- Mission 3 starts from the finders' 0/108 (90/108 found, 0 fixed after fm find): the find → prove → fix pipeline is graded on the exam's `none` and `bug`
  kinds, not on Foreman's own repo.
