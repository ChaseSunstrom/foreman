# Brainstorm — lens: the recurring miss (invented): each failure, friction or user correction that recurs becomes a fix with a test, without being asked

- **Turn each "asked" line into a recurrence probe** — FEATURE — value 5 — effort M — risk low — category: self-repair
  Why: the pack's "what earlier brainstorms missed" list (T-2285, 2288, 2289, 2290, 2291, 2292, 2326, 2327) are corrections the user typed by hand; T-2272 only clusters failure signatures, not user words.
  Done when: `fm signals` lists user-asked lines with a shape key, and a shape seen 2+ times opens one FIX task whose first criterion is a failing test.

- **Make the gate learn its own blind spots from plan-gate misses** — FIX — value 4 — effort S — risk low — category: plan gate
  Why: T-2285 (option starting with a flag or code was not counted) shows the plan gate's parser fails on text shape. Same class likely exists in sibling parsers (steer parsing, criteria parsing).
  Done when: a fuzz test feeds each prose-parsed gate options starting with `-`, backticks, digits and parentheses, and every gate counts them identically.

- **Sweep the sibling code when a FIX closes** — FEATURE — value 4 — effort M — risk med — category: self-repair
  Why: T-2289 (lane rm vs .fm-scratch) followed the guard's script-cache exception; the same "throwaway folder" class probably lives in other verbs.
  Done when: closing a FIX runs `fm graph` for callers of the same helper, and the task records a list of siblings checked, each with a test or a stated n/a.

- **Score "did the miss stay gone" 30 days later** — FEATURE — value 4 — effort S — risk low — category: outcomes
  Why: T-2272 creates fixes but nothing shows whether the signature returned; the lean ratchet and prediction scoring (T-2281, T-2290) show the pattern for scoring after the fact.
  Done when: `fm doctor` prints per-fix "held / returned" with dates, and a returned signature reopens the original task.

- **Detect a user steer given twice and promote it to a check** — FEATURE — value 5 — effort M — risk low — category: steers
  Why: steers are stored but the same intent re-appears (e.g. "update the website" came as a fresh ask after the site rule existed). Assumption: the second occurrence is detectable by token overlap.
  Done when: a repeated steer triggers a message naming the earlier rule and its check, and, if no check exists, files one task.

- **Fence self-repairs from touching the guard and hooks** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: mission 8 #7 and #12 let Foreman change itself unasked; the guard must stay intact (§6), and T-2252 already shows the guard needing user-only verbs.
  Done when: a self-born FIX whose diff touches guard or hook files is refused at ship with a message naming the path, tested by a planted diff.

- **Quarantine a fix that needed a second fix** — CLEAN — value 3 — effort M — risk low — category: self-repair
  Why: T-2283 was fixed and then reappeared as a differently keyed baseline red (the dropped "same failure as T-2283" entry): dedupe by command text missed it.
  Done when: a FIX that has a follow-up referencing it within 14 days is flagged, and the dedupe key normalises interpreter paths (tested with the full-path case).

- **Count friction, not just failures** — FEATURE — value 4 — effort M — risk med — category: signals
  Why: only failure signatures feed T-2272; repeated retries, re-runs of the same command and manual `fm task set` repairs are friction the pack shows (the plan gap messages telling the session to fix by hand).
  Done when: a session with 3+ identical command reruns writes a friction signal, and the same signal across 3 tasks opens a FIX.

- **Require the failing test to fail on the old build** — FIX — value 4 — effort S — risk low — category: proof
  Why: `fm task prove` already shows the test fails without the change; self-born fixes should be mandatory-gated by it so a green-from-the-start test cannot close a miss.
  Done when: closing a signal-born FIX with a test that passes on the start tree is refused.

- **Wild: Replay a past correction against today's build nightly** — FEATURE — value 4 — effort L — risk med — category: regression
  Why: wild. Every user correction becomes a stored scenario; a cheap Haiku-free replay checks the old miss does not return.
  Done when: a nightly run replays all stored corrections and reports any that now reproduce.

- **Wild: A "repeat offender" board** — FEATURE — value 3 — effort S — risk low — category: dashboard
  Why: wild. A web UI panel ranks the five verbs generating most corrections, with trend arrows.
  Done when: the panel renders from real signals and the top verb matches a hand count.

- **Wild: Mutation night for the repairer** — FEATURE — value 4 — effort L — risk med — category: trust
  Why: wild. Plant a known recurring failure in a throwaway copy and check the loop opens, fixes and tests it unaided; otherwise the repairer itself is broken.
  Done when: the planted fault is fixed in a copy within a fixed budget, or the run is reported failed in `fm doctor`.

- **Let the user mark a reply "that again"** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: assumption: terse corrections are the cheapest signal the user can give, and currently they need free text.
  Done when: typing `that again` links the last assistant action to a signal and bumps its recurrence count.

Next question: Which self-born fixes were later reverted or corrected by the user, and what did they have in common?
Next question: Which recurring user words never reached a task at all, because no signature or steer parser saw them?
