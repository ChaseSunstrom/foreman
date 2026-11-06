# Brainstorm — lens: grid

- **Batch drafts by loaded model** — FEATURE — value 4 — effort M — risk low — category: scheduling
  Cell: CLI × other agents/lanes × slow. Why: the steer says a llama-swap model switch costs about 3 minutes and `/running` isn't relayed. Speculative drafts that alternate between qwen3.8-27b and the 35b would stall the user's own request. Draft work is queued per model, run in one window, and never switches while a user-typed request is pending. Assumption: the drive can see a pending user request.
  Done when: a test with two queued drafts on different models and one user request issues at most one switch, and none during the request.

- **Fill briefs from cited slots only** — FEATURE — value 5 — effort M — risk med — category: local models
  Cell: CLI × agent × wrong. Why: a 27B drafting a free-form brief invents scope. The draft is a typed template (title, Done-when, Exam, files), and each slot must carry a ledger row id or `unknown`. A validator rejects a slot with no source, and the frontier model only judges the filled form.
  Done when: a draft containing an uncited slot fails `fm` validation, and a fully cited one files.

- **Show a draft's three nearest past briefs** — FEATURE — value 3 — effort S — risk low — category: scaffolding
  Cell: CLI × agent × unclear. Why: the user's accepted briefs are the best style guide for a small model. The draft prompt includes the 3 nearest accepted briefs by embedding, falling back to char-shingle, and the draft names which ones it followed.
  Done when: the draft prompt contains 3 exemplars and the draft's header lists their task ids.

- **Settle predictions by text similarity** — FEATURE — value 4 — effort M — risk low — category: calibration
  Cell: unattended × user × wrong. Why: matching a draft to a later task by id misses asks the user phrased differently. Cosine similarity between the draft and the user's next typed ask (models.embed) gives a graded hit, so partial hits count.
  Done when: a fixture where the user asks the same thing in different words scores a hit above the threshold, and an unrelated ask scores a miss.

- **Preempt speculative file claims** — FEATURE — value 4 — effort M — risk med — category: lanes
  Cell: unattended × other agents × unsafe. Why: an overnight draft lane holds files a real lane then needs. Speculative lanes hold only advisory claims, and any real claim kills the draft lane and keeps its notes.
  Done when: a real lane claiming a file held by a draft lane starts without waiting, and the draft lane is recorded as preempted.

- **Edit a draft to teach the predictor** — FEATURE — value 4 — effort M — risk low — category: web UI
  Cell: web UI × user × wrong. Why: the user's edit to a draft's title or Done-when is the cleanest correction signal and currently has no capture path. The web card stores the edit diff as a correction row that the next pack reads as a do-not-repeat.
  Done when: editing a draft's Done-when in the web card writes a correction row, and the next pack includes it.

- **Gate drafts on the surface being in use** — FEATURE — value 3 — effort S — risk low — category: grounding
  Cell: web UI × agent × unclear (the carried grounding gap). Why: drafts get filed against surfaces nobody opens. Before drafting, count the real calls or opens of the surface over 30 days from local logs, and label zero-use drafts "surface unused".
  Done when: a draft touching a surface with zero recorded uses carries the label, and one with uses shows the count.

- **Probe the local endpoint's uptime by hour** — FEATURE — value 3 — effort S — risk low — category: machines
  Cell: unattended × machine × missing. Why: the request asks for a model of the machines, and the pack has none of the 27B server's availability. A cheap probe records reachability and loaded model per hour, and overnight drafting plans around the observed windows and flags a server that went dark.
  Done when: after a week of fixture probes, `fm` prints the best drafting window and warns when the last probe failed.

- **Test that an agent ignores a false prediction** — SECURITY — value 4 — effort S — risk low — category: injection
  Cell: hooks × agent × unsafe. Why: a note saying "the user will probably ask for X" can be read as an instruction. Plant a false prediction in a scratch home and run a fake agent over it.
  Done when: the test fails if the agent makes any edit toward the planted prediction, and a prediction with the "data, not instruction" fence passes.

- **Probe with a draft, keep only the problem** — FEATURE — value 5 — effort L — risk med — category: early warning
  Cell: unattended × user × missing (wild). Why: the request wants problems flagged before they happen, not finished work. Run the predicted task in a scratch worktree, then discard the code and keep only the first blocker (a failing test, a missing dependency, a conflicting steer) as a one-line flag.
  Done when: a fixture predicted task with a planted blocker yields the blocker line and leaves the user's tree untouched.

- **Slip in a decoy draft to measure over-trust** — FEATURE — value 3 — effort M — risk med — category: calibration
  Cell: web UI × user × unsafe (wild). Why: the memory and ledger can't tell whether the user reads drafts or stamps them. Now and then one plausible but wrong draft appears, and acceptance of it lowers the predictor's trust dial.
  Done when: accepting a decoy lowers the dial and writes a ledger row, and the decoy is labelled once the user acts.

- **Rerun last night's rejected drafts on the other model** — FEATURE — value 3 — effort M — risk low — category: local models
  Cell: unattended × agent × slow (wild). Why: the idle GPU at night is free. Replay rejected drafts on the second local model and keep a draft only if its Exam improves on the first.
  Done when: a fixture rejected draft is replayed once per night, and only an improved one reaches the morning card.

- **Forecast Arch updates that break the gates** — FEATURE — value 3 — effort M — risk med — category: machines
  Cell: CLI × machine × missing. Why: on a rolling-release host a pending python or git bump can break the plugin silently. Read `checkupdates` locally, and when a runtime we use is pending, run the gates in a scratch venv at the new version and flag before the user updates.
  Done when: a fixture pending python bump that breaks a test produces a flag naming the test, with nothing sent off the machine.

Empty cells, and why:
- Site × user × unsafe: the site publishes only generated data, and the existing embargo ideas cover it.
- Web UI × other agents × slow: view render budgets are already on the list.
- Unclear for lanes in general: attribution and hand-back fields are already covered.

Next question: which anticipation draft has the user actually edited rather than accepted or dropped, and what does the edit say about what the predictor missed?
Next question: when the 27B drafts at night and the user later asks something similar, how much of the draft survives into the real brief?
