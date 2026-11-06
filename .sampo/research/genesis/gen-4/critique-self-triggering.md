# Critique — Mission 6, self-triggering (gen 4, #11)

Tasks: T-2916 (done). Mission: gen-4/mission-self-triggering.md.

## Closed vs planned
- Brief 1 (T-2916) is closed and merged, with a second commit from review. `night.jobs` lists a `moons grow` job (calls
  capped per night) and a `moons funnel` job at zero dollars. It lists them only when an own or loopback model answers,
  the project is not sensitive, and the store is under its 10,000 target. Both take `--local-only`: a call the local
  model cannot answer stops the run with its reason and never falls back to Haiku. Review made the funnel job list
  whenever rows wait to be funnelled, and made the local-only rule hold for every call, not only the first. It is the
  Mission's whole scope, as planned. No new verb, unit or hook.
- All three criteria are ticked. The third was `sampo night --dry-run` listing both jobs at $0.00. The task log
  records the reading at close. I could not re-read it today, for the reason below.

## Measures (first readings and due dates)
- Outcome measure: the catalogue's size after a real night, with the two Moons features costing $0 that night.
  First reading: none. No night has run since the jobs landed (the timer fires at 02:30, and the jobs closed at about
  10:38 UTC on 2026-11-04). The Mission's own done-when says "one real night has run both jobs". That is not met.
  Due: the first night after this critique, then a week.
- Live reading today: `sampo night --dry-run` plans 11 jobs, about $1.98 of $2.00. Eight are $0 chores (scout, dream,
  cold files, guard cases, steer checks, compost, consolidate, sentinel), plus a new "next request" job at $0. The
  paid ones are research debt (about $0.45) and court (about $1.53). The queue is skipped as over the limit. The two
  Moons jobs are not on the list.
- Why not: the candidates store is 10,007, over the 10,000 target. T-2865 closed this very session and grew the store
  by hand. So the gate did what it was built to do. That also means the first real night will probably run no Moons
  job at all. This is my reading of the gate, not a run. The measure as written cannot move until the target is raised
  or the funnel has rows waiting.
- Other shifts today: the 02:30 timer's last run is not in the ledger as a `night` event that I can see. `sampo triggers`
  shows the `night` trigger fired once in total. The schedule exists and little rides it.

## Outside signals
- None. The only new input is that the live page (T-2997 to T-3027) now steers sessions, but it does not start work
  by itself. It is steering from a user who is present, not a trigger.

## What failed
- The Mission solved yesterday's gap. When it was written the store stood at 4,879 of 10,000. By the time it closed,
  one interactive burst (T-2865) had reached 10,007, so the feature it shipped is switched off by its own gate. The
  feature is correct. It was sized to a number that moved under it, and nobody re-read the store between plan and close.
- The measure needs a night, so the exam cannot be run in the generation that builds it. This is the third Mission
  where the outcome waits on a clock (anticipation, gen 3, was the same). The Mission said "read after a night has
  run" and still ticked done-when in the plan. The critique can only say planned, not moved.
- The Mission left the paid half of the night alone. Court at $1.53 of a $2.00 limit still eats most of the money, and
  the queue is skipped every night for lack of it. That is the actual constraint on what starts without the user.

## What the next Seed should change
- Raise the target as part of the Mission, or write the gate as "rows waiting" so it does not turn off at a number. A
  store that stops growing should stop by evidence of diminishing novelty, not by a constant.
- Give the night a second kind of $0 work. Candidates that do not need a catalogue: T-2910's local brainstorm for the
  next Mission, the model bench rerun (T-2886), a graded morning card. The morning card is what lets the critique read
  what ran and why it stopped.
- A Mission that depends on a night reads its first real night in its own critique, or says plainly the critique is
  early. Gen 5's critique of this Mission should quote the ledger event for the first night, whichever jobs ran.
- Read `sampo triggers` for the `night` row each time. One firing in total is the number to move.
