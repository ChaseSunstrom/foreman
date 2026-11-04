# Critique — Mission 2, anticipation (gen 4, #3)

Tasks: T-2912 (done, merged 2026-11-04 07:47Z, night job wired 11:21Z). T-2924 (captured, the live replay and note). Mission: gen-4/mission-anticipation.md.

## Closed vs planned
- Brief 1 (T-2912) is closed as code. The 27B reads the user's recent asks, the open queue and the standing steers, and predicts the next ask's type, paths and words. The guess is booked in the same next-request row as `pred_local`, scored like the other arms, and listed as its own kind. `replay_forecast` has a local arm that reports type hit, path overlap and word overlap beside the transition guess and the naive baseline. The session-start line and draft-ahead read whichever arm leads on 20 or more scored rows. A sensitive project asks loopback only. Criteria 1 and 2 are green on test_foresight.
- The night job was a late fix. At 07:46Z the first merge left `local_tick` with no caller. At 11:15Z the task widened its scope to night.py, cli.py and outcomes.py so that the night run calls it. This is the same failure the gen-3 critique named: code that passes its tests and has no caller on the live path. It was caught on the second focus, three and a half hours later.
- Criterion 3 was not met. It asked for the held-out replay on this project's own stream, filed as research next-request-local. At 07:46Z it moved to T-2924 because the endpoint was busy with moons growth. T-2924 is still captured. No research note by that name exists.

## Measures (first readings and due dates)
- Local arm vs the count on the held-out third. The rule: the local arm leads if its type hit beats the count's by 10 points or its path overlap by 0.10. First reading: none. The replay has not run. This is the Mission's one outcome measure.
- Live book. `sampo outcomes --predictions` today: "next-request-local: 0 scored, hit n/a vs baseline n/a". The arm has booked and scored nothing. The existing arm reads "next-request: 81 scored, hit 41% vs baseline 31%; shown at session start: 39 scored, hit 38%". Gen-3 left that line at 0 shown and scored; it is now 39 shown and scored. That is gen-3's measure moving, not this Mission's. Its hit rate of 38% is below the all-rows 41%, and the baseline for the shown rows is not printed, so I cannot say whether the shown line beats "same as last".
- Draft-ahead. "draft-ahead: 1 scored, hit 0%". The Mission's kill test said under 3 accepted drafts means the spend is waste. It is at 0 of 1, unchanged since before the Mission.
- The `genesis-anticipation` trigger row in `sampo triggers`: 23 fired, 0 done, 7 dropped, 16 open, precision 0.00. That is a Mission-adjacent signal. The anticipation work files tasks at low priority and none of them has closed. The pile line from gen-3 produces work nobody does.
- Night job: wired, not yet run to a reading. Nothing in the book proves a tick has booked a local row. Due: the first night after the endpoint frees.

## What failed
- The same pattern as Mission 1. Both live measures wait for the one remote endpoint. The Mission was seeded for the same night as moons growth and the GPU exam, and the endpoint is the single shared slot. So the criterion that actually tests the idea was cut at the first conflict, and two Missions in a row have a captured stub as their Exam.
- Zero scored local rows means the guess has never been checked against a real ask, so the Mission's own doubt, that the user's asks come from new ideas history cannot predict, is untouched.
- The Mission set up its Exam to avoid leakage (`reqs[:i]` only). The test for that is in the diff. I could not check from the live book that no row leaks, because there are no rows.

## What the next Seed should change
- Before a brief is filed with an Exam that needs a model host, check the host. `sampo` can say whether the endpoint has free slots and what holds them. If the host is busy, run the replay on the GPU profile, or schedule the Exam for a named night with the night job set to run it.
- Give T-2924 criteria with dates. It should read: replay on the held-out third, file the note, and state the type-hit gap against the count in points. Also decide in advance what happens to a tie.
- Read the shown-line baseline. `outcomes --predictions` should print the baseline for the shown rows next to the 38%, or the 38% cannot be judged.
- Stop filing `genesis-anticipation` tasks at 0% precision. Either the trigger earns its keep with a close, or it drops. Sixteen open at low priority is a pile with no owner.
- If the replay says the local arm leads: ghost-user night run and word-level drafts. If it does not: keep it in shadow and file the miss classes (wrong type, wrong area, new idea) with the small-model control step in T-2878.
