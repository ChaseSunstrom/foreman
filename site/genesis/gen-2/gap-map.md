# Genesis gap map — generation 2 (2026-11-02)

Drawn at: d2f4f18a

Redrawn against the code at d2f4f18a by targeted reads: each capability's built tasks (commit subjects tagged
"(Mission N, #K)" since gen 1's map at ae98159e, and gen 2's Mission tasks), their tests, and the measurements on
record (exam lines, outcomes, the gen-2 review). Every later idea is checked against this map: an idea that names
something under **Built** is a duplicate unless it extends it. Tiers: 3 capability, 4 paradigm.

Source limit: the held-out exam on the production model has not run (the user's testing-cadence steer keeps it for
the end of the run), so `fm exam scorecard` reads 0/13 and no capability below counts as passing. The signals Foreman
didn't author so far: the long-horizon tier (l001, l002; foreman 0/6 true done with 6 false dones, plain 1/6), the
gen-2 cross-cutting review on a stronger model (22 findings, 9 fixed, 4 sent here as gaps) and CI on main.

## Cross-cutting findings
- **Built, not yet measured.** Gen 1 closed most of gen 1's "advice, not action" holes with triggers and gates. What's
  missing now is proof that they work on held-out work: the production held-out exam (end of run) and outcomes past
  their 30-day window (T-2584 counts only those).
- **False completion.** The long-horizon tier's foreman arm claims done on 6 of 6 goals it fails. 17 of the 31 failed
  hidden checks demand interfaces the goal text never states (exam reach, reported, never rewritten), but 14 are real
  misses. T-2557 now checks each stated Done-when line; whether that moves the long tier is for the end-of-run exam.
- **Growth outruns measurement.** The gen-2 diff added 4,595 lines and removed 196; fmgenesis.py alone grew 729 lines
  with no exam kind of its own, and T-2503's lean check judges only the Missions' growth (review #6, #8).

## 1. Initiative
- Built: fm find with a detection ladder and ranked leads (T-2185); sessions must fix, report or refute every lead they
  were shown (T-2297); fm scout project probes; capability-miss and watcher triggers file work unasked (#5, #11).
- Measured: exam kinds bug, vuln, slow, docs, flaky, dep, none, rank exist; no graded held-out foreman line yet.
- Missing: proof on held-out repos that the leads Foreman ranks first are the ones worth fixing.
- Gaps: held-out initiative score (3).

## 2. Exhaustive thinking
- Built: the plan gate checks content by tier (T-2269, T-2335: 3+ approaches with a choice, readings, outcomes); blast
  radius in the plan (T-2277, T-2336); races at plan time chosen by evidence (T-2339); L plans race their design with
  throwaway spikes (T-2340); a cold rival reads the request (T-2341).
- Measured: exam kinds ambiguous, exists, race; no graded held-out line yet.
- Missing: evidence that a rival read or a race changed a choice for the better (dissents are resolved, never scored).
- Gaps: score adopted-vs-rejected dissents against outcomes (3).

## 3. Anticipation
- Built: Foreman predicts and scores its own active minutes (T-2290); a prediction book with muting (T-2406); the lane
  plan for the top prediction (T-2407); the user model reads only the user's own asks (T-2554); foresight flags CI red,
  setup changes and dead timers (T-2542).
- Measured: the walk-forward replay on 331 held-out asks: type 201 hits for the cleaned and the raw history (naive
  196); paths 0.118 against a naive 0.116. On s11-012 the path predictor scored below naive (review #2).
- Missing: a path predictor that beats naive; scored steer predictions (T-2505 seals them, nothing scores them,
  review #17).
- Gaps: path predictor past naive (3) · steer predictions scored (3).

## 4. Goal to finish
- Built: fm goal with items, a done-when that counts only if it fails on the item's start tree (T-2416), each stated
  Done-when line needing a check (T-2557); goals and mandates in every session note; the Stop drive and the forever
  loop (T-2569 keeps a re-read from closing a round).
- Measured: the long-horizon tier: foreman 0/6 true done, 6 false dones (l001, l002); plain 1/6.
- Missing: a done claim that survives hidden checks; the session's own checks don't cover what the goal implies.
- Gaps: false-done on long goals (4) — the next Seed's top gap (review #1).

## 5. Getting the tools it lacks
- Built: the capability-miss trigger (T-2270, T-2370), joined to the active task (T-2369); scaffolds for a missing
  tool (T-2278); fm which across every shelf (T-2371); built tools prove themselves (T-2372); the install-grant queue
  (T-2374); a long-horizon missing-binary fault (T-2377).
- Measured: exam kinds missing-tool, tool-build, tool-find, tool-grant with outside authors (T-2453); not graded.
- Missing: a graded held-out score (its four kinds are not graded yet); tools only the user can install wait for them
  (actionlint, T-2564).
- Gaps: unmeasured until the end-of-run exam grades missing-tool, tool-build, tool-find and tool-grant (3); inspection
  found no other.

## 6. Verifying anything
- Built: fm prove kinds --docs (T-2381), --infra (T-2385), --migration (T-2288, T-2386), --data, --release, measured
  perf proof (T-2284); the unproven rollup by domain (T-2273, T-2391); every result ends with "Does not prove:".
- Measured: exam kinds proof and beyond (T-2394); the rollup counts 1,042 unproven items here (594 docs, 568 meaning).
- Missing: intent proof beyond an LLM lens ("meaning" is the largest unproven class).
- Gaps: intent proof (4).

## 7. Self-repair and self-improvement
- Built: Foreman's own failures and fixes that didn't hold enter the signal-to-fix loop (T-2349); a user-steer rule
  whose check fails becomes a fix, checked nightly (T-2350); self-fix trials with verdicts (T-2351, T-2365); failure
  signatures name the failing check (T-2567).
- Measured: exam kinds recur, correction; not graded. Outcomes: 66 of 1,699 closes lost within 30 days (T-2584 now
  takes the rate over finished windows only).
- Missing: a graded held-out score (recur and correction are not graded yet).
- Gaps: unmeasured until the end-of-run exam grades recur and correction (3); inspection found no other.

## 8. Calibrated judgment
- Built: the calibration ledger of write-once bets (T-2337); confidence routes the next step (T-2338); stop only at an
  irreversible, ambiguous step (T-2342); ship bets (16 held in a row this run).
- Measured: exam kinds fork, door, unsure; FEATURE M plans held on first finish 96% while stating 65–85%
  (under-confident by the ledger).
- Missing: plan confidence that tracks the record (the ledger reports the gap, nothing adjusts it).
- Gaps: confidence calibrated from the ledger (3).

## 9. Orchestration
- Built: a history-based model router (T-2291) that probes down a tier (T-2353); lanes recover by cause (T-2354);
  fm run lanes; the model layer in shadow mode.
- Measured: the model-versus-rule exam has no model side: no night answers are booked (T-2582 says "not run").
- Missing: a configured model backend (LLM_API_KEY is the user's), so the model layer decides nothing yet; a graded
  held-out score for parts and lanes.
- Gaps: the model layer unmeasured, waiting on the user's key (3) · orchestration unmeasured until the end-of-run exam
  grades parts and lanes (3).

## 10. Beyond code
- Built: the incident ritual (T-2388); docs, infra, data and migration proof (#6); fm release for any repo (T-2390);
  release 1.2.51 shipped with highlights (T-2591, T-2595, T-2598).
- Measured: exam kinds docs, beyond, package; not graded.
- Missing: a graded held-out score (docs, beyond and package are not graded yet).
- Gaps: unmeasured until the end-of-run exam grades docs, beyond and package (3); inspection found no other.

## 11. Self-triggering
- Built: trigger routing that learns from outcomes (T-2276); watchers start work with no session on a zero-token tick
  (T-2356); installs staged for one yes (T-2357); timer liveness from systemd (T-2542); a skipped night is a success
  (T-2593).
- Measured: exam kinds trigger, watch; not graded. The night timer is installed; its runs skip while usage is high.
- Missing: a week of live ticks graded (needs the user's install of the tick timer; the gen-2 seed carries it); a
  graded held-out score for trigger and watch.
- Gaps: live ticks ungraded, waiting on the user's install (3) · unmeasured until the end-of-run exam grades trigger and
  watch (3).

## 12. Staying lean and safe
- Built: the lean ratchet on the always-on footprint (T-2281); lean measures substance (T-2503); the lean exam kind
  (T-2363); ablation captures subtraction candidates (T-2536); the session note fits one 1,500-character budget
  (T-2589); a failed matcher removed (T-2587).
- Measured: hook p95 within budget at every gate; the gen-2 diff's 23:1 add-to-cut ratio (review #8).
- Missing: the lean check over the tower's own growth, not only the Missions' (review #6).
- Gaps: lean check covers all growth (3).

## 13. Genesis as a feature
- Built: the tower orchestrator (fm genesis step through seed, Missions, critiques, select, drift, review, sweep);
  the multi-language exam with keys and holdout; selection and lineage that use train lines only (T-2566); drift
  against gen-0 and the user's steers; the cross-cutting review on a stronger model (T-2501); the live tower page.
- Measured: gen 2 selected as the baseline on s32-015 (3 train scenarios closed, Haiku: provisional); exam kinds
  line, none, sweep; not graded.
- Missing: a production-model confirm of the lineage (end of run); a run from no prompt on another project.
- Gaps: Genesis from no prompt, graded (3).

## Gen 3 ordering (largest gaps first)
1. #4 false completion on long goals (tier 4).
2. #6 intent proof (tier 4).
3. #12 lean check over all growth; #3 path predictor and scored steer predictions; #8 confidence from the ledger
   (tier 3).
4. #2 scored dissents; #1 held-out initiative score; #13 Genesis from no prompt (tier 3, measured by the end-of-run
   exam).
