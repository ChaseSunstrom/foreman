# Brainstorm — lens: inversion: how verification fails: green unit tests on the wrong behaviour, docs that lie about the code, a UI never looked at, infra changed blind, perf claimed unmeasured, research uncited, an unproven claim reported as done

- **Fail a green whose test count dropped** — FIX — value 5 — effort S — risk low — category: test proof
  Why: assumption: a verify command can go green by collecting fewer tests (a deleted test, a new `-k` filter, a skip marker, an emptied glob). Evidence rows record exit code, not how much ran.
  Done when: a task whose verify command collects 12 tests at focus and 9 at close is refused with "collected 12 → 9", and the same count passes.

- **Lint verify commands for exit-code laundering** — FIX — value 4 — effort S — risk low — category: verify commands
  Why: assumption: `cmd | tee`, `|| true`, `grep` without `-q`, `pytest` with no path and a `;` chain all exit 0 while proving nothing. `fm task new` already notes missing test modules (T-1208), which is the same class of check.
  Done when: `fm task new` flags each of those five shapes in a fixture, and a clean command raises no note.

- **Reject degenerate screenshots** — FEATURE — value 4 — effort M — risk low — category: UI proof
  Why: `fm shot` and `fm flow` can capture a blank page, a spinner, a 404 or a stack trace and still count as "visual check done". Also reject a shot pixel-identical to the pre-change shot when the diff claims a visible change.
  Done when: fixtures (all-white, spinner frame, error page, unchanged page) are each refused with a named reason, and a real changed screen passes.

- **Refuse circular sources** — FEATURE — value 4 — effort M — risk med — category: research proof
  Why: assumption: research and docs claims can cite Foreman's own notes, the Genesis site or model-written summaries, so the "source" is just the claim's producer. This answers the earlier question about numbers never checked by anyone other than their producer.
  Done when: a claim whose only citation is a file Foreman generated is labelled unproven with "source is self-derived", and a claim citing an external fetched page with a verbatim quote that is present passes.

- **Check that the timed code is the changed code** — PERFORMANCE — value 4 — effort M — risk med — category: perf proof
  Why: T-2284 and T-2303 time a command before and after, but a speedup can come from a warm cache, a smaller input or a path the change never touches. Record the input size and cache state, and require a sampled profile or trace showing the changed function on the timed path.
  Done when: a bench where the changed function never appears in the trace is recorded as "measured, not attributed", and one where it does is recorded as attributed.

- **Flag evidence that ran impossibly fast** — SECURITY — value 3 — effort S — risk low — category: evidence integrity
  Why: assumption: typed evidence can be dressed up as run output. A row claiming a 40-second suite finished in 0.2s is detectable against the command's own history.
  Done when: a row whose duration is under 10% of that command's recorded p50 is labelled "implausible timing, treated as typed".

- **Read infra back from live state, with a blast ceiling** — FEATURE — value 4 — effort M — risk med — category: infra proof
  Why: an infra proof kind is already proposed (plan, scratch apply, re-plan), but a config diff can be clean while the live system differs. Add a read-only probe of the real state, plus a plan-time cap on resources touched that fails the proof if the diff exceeds it.
  Done when: on a fixture target, a change that touches 5 resources against a declared ceiling of 3 fails, and a probe reporting live state different from config is shown as drift.

- **Use a blind test author** — FEATURE — value 4 — effort M — risk med — category: wrong-behaviour green
  Why: the same session reads the ask, writes the red test and writes the fix, so a misreading is baked into both and the test goes green on the wrong behaviour. A separate tool-less child sees only the user's sentence and writes the acceptance test.
  Done when: for a seeded task with an ambiguous ask, the blind test and the builder's test disagree on at least one case and the disagreement is shown at close.

- **Print a judge map** — CLEAN — value 3 — effort S — risk low — category: judge independence
  Why: this answers the earlier question about verbs with a model on both sides. Cold reads, exam scenario authoring and scoring, and the evidence judges all appear to be Claude-family children grading Claude-family work. No pack evidence shows a user-owned check on those paths.
  Done when: one command lists every verb that has a model writer and a model judge, marks which have a user-owned check, and `fm doctor` warns on the rest.

- **Show the hunks no proof witnessed** — FEATURE — value 3 — effort L — risk med — category: coverage of claims
  Why: assumption: a task diff has hunks that no test, shot, bench or doc check touched. Map each hunk to the evidence rows that exercised it, using coverage and the trace.
  Done when: at close, a diff with one hunk outside every evidence row lists it as "unwitnessed: path:line" in the unproven rollup.

- **Wild: Plant a canary lie weekly** — SECURITY — value 4 — effort M — risk low — category: pipeline honesty
  Why: wild. Nothing tells us the gates still catch a false claim today. A sandbox task is seeded each week with a known-false "proven" claim (a typed result, a stale shot, an uncited fact), and an alarm fires if the pipeline closes it.
  Done when: a deliberately weakened gate in a test makes the canary close and `fm doctor` names the gate that let it through.

- **Wild: Test whether the acceptance check reacts to the ask** — FEATURE — value 3 — effort M — risk med — category: meant-it proof
  Why: wild. Negate or swap a noun in the user's sentence, regenerate the acceptance check, and see whether the old test still passes. If it does, the test isn't tied to the ask.
  Done when: for a fixture ask, the mutated-ask run fails the original test, and a test that ignores the ask's nouns is flagged as insensitive.

- **Wild: Generate "what does not prove" from a stranger's doubts** — FEATURE — value 3 — effort S — risk low — category: receipts
  Why: wild. Give the receipt, with no repo access, to a cold child and ask "what would you check to doubt this?". Its unanswered doubts become the receipt's "does not prove" lines instead of boilerplate.
  Done when: a receipt for a task with only unit-test evidence lists at least one task-specific unproven doubt that the evidence rows don't answer.

Next question: When a verification step itself errors or times out, which verbs record that as "unproven" and which silently skip it?
Next question: Which proof kinds have never been shown to fail on a planted fault, so their catch rate is a guess?
