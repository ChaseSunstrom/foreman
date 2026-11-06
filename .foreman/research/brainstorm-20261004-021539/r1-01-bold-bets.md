# Brainstorm — lens: bold bets

- **Lint the final message against the ledger** — FEATURE — value 5 — effort M — risk med — category: honesty
  Why: the rule "nothing is done without evidence fm ran itself" binds the ledger, not the prose the user reads. Reviews keep finding gaps between claims and proof. Assumption: the Stop hook can read the last assistant text.
  Done when: a final message saying "all tests pass" with no matching passing run in the ledger is flagged at Stop, and a message whose claims all match runs is not.

- **Trace every clause of the request to a criterion** — FEATURE — value 5 — effort M — risk low — category: intent
  Why: the dropped item "members' requests carried every item's criteria" and the user's repeated "not just small fixes" show clauses getting lost between request and brief. A clause matrix makes loss visible.
  Done when: `fm task new` on a three-clause request prints each clause mapped to a criterion or an explicit "dropped: reason", and close refuses while one is unmapped.

- **Require a runnable repro on every reviewer finding** — FEATURE — value 4 — effort M — risk low — category: review
  Why: review passes found 3–7 issues each time, and two HIGH issues in the proof tool. Prose findings are easy to argue away, while a failing command is not.
  Done when: a finding without a repro command is recorded as "unproven" and doesn't block, and a finding with a repro blocks until the repro passes.

- **Predict before running, and log the miss as a surprise** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: `fm surprise` exists but only works if someone remembers to call it. A one-line expected outcome recorded before each verify run makes surprises automatic.
  Done when: a run whose result differs from its recorded prediction creates a surprise entry without a manual call.

- **Check ledger invariants continuously** — SECURITY — value 4 — effort M — risk low — category: integrity
  Why: evidence-judging tools fail silently (a proof recorded with nothing proven, a crash leaving empty git objects that doctor missed). Invariants like "no done criterion without a run ID" or "no approval without a user turn" catch whole classes of bug. Assumption: ledger entries carry enough IDs to check these.
  Done when: a hand-corrupted fixture ledger (a done criterion with no run) makes `fm doctor` name the violated invariant, and a clean ledger passes.

- **Test state-schema migration against old fixtures** — FIX — value 4 — effort M — risk low — category: compat
  Why: the plugin changed daily, and users' state outlives versions. Truncated state JSON was already a failure. Assumption: state carries no schema version today.
  Done when: fixtures from the last N state shapes load under the current code with a recorded migration, and a deliberately unmigratable one fails with a named error.

- **Emit a versioned NDJSON event stream** — FEATURE — value 3 — effort M — risk low — category: interop
  Why: the UI, `fm serve`, and the planned MCP server each read state their own way. One schema'd stream, `fm events --follow`, would let any client (pane, MCP, other harness) consume Foreman.
  Done when: a conformance test replays a recorded session through the stream and the UI view model rebuilds identical cards from it.

- **Wild: Let Foreman dream — consolidate memory while idle** — FEATURE — value 4 — effort L — risk med — category: memory
  Why: assumption: lessons only grow. An idle-time pass merges duplicate lessons, drops those whose removal changes no bench result, and writes a diff the user can veto.
  Done when: a dream run on a fixture lesson set with planted duplicates cuts it by the planted count and leaves bench results unchanged.

- **Wild: Make the user's words a live contract** — FEATURE — value 5 — effort L — risk med — category: intent
  Why: the user's verbatim steers ("don't want small fixes", "not sacrificing quality") currently live only in a pack. Compile them into standing, testable assertions on every brief, such as "a brief tagged small-fix needs a stated reason" or "a speed-up must show a quality-neutral bench run".
  Done when: a brief that violates a compiled steer gets a pre-edit note that quotes the user's words.

- **Wild: Hold a pre-mortem court at brief time** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: pass 1 and 2 reviews found the same classes of bug (parser edge cases, export privacy, vacuous proof). A tool-less child writes the three likeliest ways this brief fails, and the top one becomes a criterion.
  Done when: `fm task new` on a parser task adds a criterion derived from a past finding class.

- **Wild: Run Foreman against a bare model as a blind A/B** — FEATURE — value 4 — effort L — risk med — category: proof
  Why: nothing yet shows Foreman earns its overhead. Replay a held-out bench case with and without it, then have a blinded judge compare the diffs.
  Done when: `fm bench ab CASE` prints a win/loss/tie verdict plus the cost delta, without revealing the arm to the judge.
