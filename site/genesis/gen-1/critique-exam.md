# Critique — Mission 1, the exam (gen 1, #13 + #6)

Task: T-2079 (done, shipped to main at 1a78a3f). Mission: gen-1/mission-exam.md.

## Exam scenarios: closed vs planned
| Planned | State |
|---|---|
| Generated repos build, visible tests pass (except flaky, dep) in python, js, ts, rust, ruby, c | closed — test_exam |
| Every hidden check fails planted, passes clean | closed — test_exam, all six languages |
| Oracle 100%, empty 0% | closed — test_exam; s0-001 empty row: 0/108 |
| Holdout never in `--split train` | closed — test_exam |
| ≥ 9 scenarios per kind, ≥ 3 held out | closed — `--per-kind 9` → 6 train + 3 held out per kind |
| Tool-less child author (standing rule 5) | closed — `fm exam gen --author child`; real run: 1 kept, 1 dropped by the exam of the exam |
| Foreman vs plain session arms with cost | closed — both arms run the same held-out scenarios; cost in `fm cost` under `exam-arm`, capped by `fm budget` |
| Finders baseline in exam.jsonl | closed — 0/108 (decision recorded 2026-10-28); revisited 2026-10-30 after fm find (T-2121): 90/108 found, 0 false alarms, held out 30/36, 0 fixed (finders find, never fix; T-2157) |

All 8 planned items closed; none waits on the user.

## Outside signals
- **Plain vs Foreman, held out (s0-001, 1 scenario each, two samples):** both found 1/1 and, after the temp-copy fix,
  both fixed 1/1 test-first. Foreman cost $0.34 against plain's $0.11 for the same score. One scenario is noise, not a
  ranking; but the only signal there is says **Foreman costs ~3× for no measured gain** on a single planted bug. That
  is a #12 Lean gap and a #6/#1 gap: Foreman's value has to show on scenarios plain Claude misses (vague, none,
  missing-tool), and nothing has measured those yet.
- **Finders arm 0/108:** Foreman's deterministic finders (fmdocs.scan + fmsecrets) find none of the planted defects. Re-run 2026-10-30 (T-2157) with fm find in the arm: 90/108 found, 0 false alarms, held out 30/36 (zero tokens).
  Self-checks call those finders healthy (their own tests pass); the outside signal says they find nothing. By standing
  rule 4 that makes **#1 Initiative's finders a top gap** → Mission 3.
- **fm outcomes (all time):** 1292 of 1337 finished tasks held (96.6%), 44 fixed later, 1 reverted. Close warnings on
  T-2079 itself: "suspiciously smooth: 16 runs passed the first time". Survival is good; first-try green is a sign the
  checks are too easy, not that the code is.
- **fm second:** not run this Mission (it is the gen-level drift check; scheduled for the end of gen 1).

## Coverage cells filled
coverage.md does not exist yet (Mission 2 builds it). Cells this Mission fills once the grid exists:
#13 × exam generator, #13 × scoring, #6 × held-out grading, all six languages × the 11 scenario kinds.

## Not-yet items
None added; none in this area to retry (not-yet.md does not exist yet — Mission 2 builds the ledger).

## What failed
1. First real session sample: the work dir sat under the project dir, so Foreman's own guard refused the agent's edits
   and both arms scored 0 fixed. Fixed by running sessions in a temp copy outside the project. Lesson: an exam arm
   must run where a user's repo would be, never inside Foreman's state.
2. A session that errored (rate limit, budget cap) was silently scored zero — a wrong "Foreman is weak" signal. Now
   counted as `errors` and shown as "N errored".
3. One planted bug per arm is too small a sample to rank anything. Cost per scenario ($0.11–0.34) makes a full
   held-out arm (33 scenarios) ~$4–11 per agent.

## What the next Seed should change
- Every Mission's critique runs **both session arms on ≥ 9 held-out scenarios of its own capability's kinds** (vague,
  ambiguous, none and missing-tool included), not one bug. Budget it; the spend cap is off for building and proving.
- Add a **cost-per-verified-result** column to selection: a rewrite that ties on score at 3× the cost does not win.
- The child author should write the held-out third by default once it passes the exam of the exam reliably
  (currently 1 of 2 kept) — templates are memorisable by anything that reads fmexam.py.
- Mission 3 starts from the finders' 0/108: the find → prove → fix pipeline is graded on the exam's `none` and `bug`
  kinds, not on Foreman's own repo.
