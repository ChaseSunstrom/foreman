# Mission 7 — anticipation (gen 3, #3)

Task: T-2677 (the Mission's own grounding and filing).

Parent: gen-3/seed.md row 7 → gen-0.md #3 "Anticipation". gen-0's goal, MUSTs and NEVERs are quoted in the seed and
apply here unchanged.

## Capability
Foreman says what it foresees at the moment the user can use it. It already predicts the user's next request
(fmforesight.predict, booked and scored against a naive baseline, muted when it trails), but the guess is shown nowhere.
A session that ends with landed, unshipped work says nothing. The blocked pile gives a count but never the one action
that would free the most work. Each is a foreseen need that never reaches the user.

## Grounding
- Brainstorm: fm mission for #3, then fm ideas --rounds 4 --deepen 3 --falsify --crossbreed --seen-latest 6 with the
  grid lens (T-2672): 393 distinct ideas (research/brainstorm-20261102-155217). Three recon passes grounded them,
  recorded with fm research add as research/brainstorm-20261102-m7.md. 393 ideas in 64 clusters
  (34 built, 176 partial, 170 new, 13 false premise; 16 marked build). Mission 6's measures, from this catalogue: 169 of
  170 "new" verdicts carry a canary, and 27 of the 41 grid-cell ideas grounded as real gaps.
- Spot check, true: fmforesight.lines (fmforesight.py:197) returns a setup change and red CI only. The next-request
  row in predictions.jsonl (fmforesight.prediction_tick, fmforesight.py:311) has no reader that shows it. Two recon
  passes found this independently.
- Spot check, true: fmhooks.py holds no unshipped-work notice (grep "unshipped", "git cherry", "fm ship": none), and
  this session shipped 48 commits by hand after they sat local for hours.
- Spot check, true: fmforesight.pile_lines (fmforesight.py:184) prints the blocked count, the oldest item and
  "→ fm tidy", never which user action frees the most.
- Spot check, true: fmserve._notify (fmserve.py:741) runs the user's fm notify command but ignores its exit code and
  swallows every error, so a broken command fails silently on every warning it was meant to carry.

## Gaps this Mission targets (coverage: #3)
- learn × Claude Code: a prediction that beats its baseline is booked and scored but never seen.
- ship × Claude Code: landed work waits unshipped though the user granted pushes to main.
- operate × CLI: the blocked pile names no action ranked by what it frees.
- operate × headless/server: a foreseen warning sent through fm notify can fail every time without anyone knowing.
- Not in this Mission: the hook-error line at session start, draft-ahead staleness stamps, the capture-time closest-task
  line and conditional reminders. They are marked build in the catalogue and carried to the next seed.

## Ideas (from the brainstorm, grounded)
- "Do less: print one 'you usually ask X next' line" is partial (booked, never shown). That is brief 1.
- "Offer to ship when a session ends with landed, unshipped work" is new. Under the user's push grant it becomes an
  action rather than an offer. That is brief 2.
- "Mark each blocked task with the single user action that frees it, ranked by count freed" is partial. That is brief 3.
- "Prove every alert channel delivers, and fall back when it doesn't" is partial. That is brief 4.
- The rest stay in the catalogue with their marks; none is dropped silently.

## Exam
- Brief 1: on this project's history, the line appears only while fmforesight.prediction_kinds shows next-request
  beating its baseline and not muted. Each showing is booked, so the hit rate of shown guesses can be read apart from
  unshown ones. Outcome measure: after a week, the shown-guess hit rate against the baseline's, read with
  fm outcomes --predictions.
- Brief 2: with commits main lacks and the user's standing push grant on record, fm next names fm ship as the one
  required action once the queue's tasks are closed, so the drive ships without asking. Without the grant it prints one
  line naming the count and the command. Outcome measure: the hours landed work waits before a push, read from the
  ledger before and after.
- Brief 3: a pile with tasks blocked on two asks and one grant names the ask that frees the most, with its count.
  Outcome measure: the blocked count a week later against today's 44.
- Brief 4: a notify command that exits non-zero is recorded as failed, and fm doctor warns after three failures in a
  row, naming the command. Outcome measure: notify delivery failures surfaced instead of silent, counted from the
  record.

## Long-horizon goal (end of run)
What Foreman foresees reaches the user where they look (session start, session end, the blocked pile), and each line
carries the number that says whether it was right.

## Lean
Three lines on existing surfaces (fmforesight.lines, the Stop hook's end note, fmforesight.pile_lines) and one doctor row. No new verb, no
new state file; brief 1 adds a "shown" field to rows the book already writes.

## Tier share
All four are tier 2 to 3 (S): foreseen needs that are computed already and only need to reach the user.

## Done when
- Each brief closes with its own criterion command green on the closing tree.
- Mission 6's two use measures are reported from this Mission's catalogue (grid cells that yielded a grounded idea;
  "new" verdicts carrying a canary) in gen-3/critique-anticipation.md, and carried back to Mission 6.
- Each brief's outcome measure has its first reading, or the date it is due, in the critique.

## Briefs (fm intake)
```
FEATURE: fmforesight.lines shows the newest unscored next-request prediction (type and top paths) at session start only while prediction_kinds shows it beating its baseline and not muted, and the book records that it was shown
FEATURE: when commits on the work branch are missing from main and the queue is closed, fm next makes fm ship the required action under the user's standing push grant (a decision citing it), else one line names the count and the command; silent when nothing waits
FEATURE: fmforesight.pile_lines names the user action that frees the most blocked tasks (an fm ask answer, a grant, a dependency) with its count, ranked
FIX: fmserve._notify records each delivery's result (exit code included) and fm doctor warns after three failures in a row, naming the notify command
```
