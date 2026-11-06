# Brainstorm — lens: deepen: tokens

- **Route every Agent call by price and measured pass rate** — FEATURE — value 5 — effort M — risk med — category: tokens
  Why: S-tier lanes hardcode "sonnet", scout is haiku, and T-0755 asks whether Foreman can spawn lower models. The Agent tool takes per-call `model` and `effort`. A router picks model and effort from task tier, step kind and the per-model lesion results already recorded (T-0752), and falls back upward when a model's pass rate on that step kind is low.
  Done when: `fm agents plan` on a read-only S step logs haiku/low, a root-cause step logs opus or higher at high effort, and a replay test shows the choice flips when the recorded pass rate drops below a threshold.

- **Lint the injected context for cache-busting bytes** — FIX — value 4 — effort S — risk low — category: tokens
  Why: assumption: timestamps, counters or reordered sections in the SessionStart/UserPromptSubmit preamble change the prefix each turn and defeat prompt caching. This builds on the hash-addressed delta idea by testing prefix stability directly.
  Done when: a test renders the preamble for two consecutive turns with only the clock changed and fails if any byte before the dynamic tail differs.

- **Schedule wakes and queue order by cache TTL** — FEATURE — value 4 — effort M — risk med — category: tokens
  Why: T-0758 ("doesn't sit idle") and the idle-cost meter and debounce ideas meet here. Foreman batches queue items that share a prefix inside the cache window. `ScheduleWakeup` then lands either under the TTL or well past it, never just after it, which is the worst case (a full miss for almost no wait).
  Done when: a simulated idle gap logs a wake delay chosen from the TTL rule, and a test shows two same-prefix tasks run back to back rather than interleaved with an unrelated one.

- **Compact on Foreman's terms at phase boundaries** — FEATURE — value 5 — effort M — risk med — category: tokens
  Why: Foreman already resumes at the exact step after `/compact` and hooks PreCompact. Compaction is cheapest when the cache is already cold and a phase has just closed. The idea is to compact proactively at those points and pass PreCompact a Foreman-written keep-list (current step, criteria, evidence refs) so the summary never has to rediscover state.
  Done when: a scripted session crossing a phase boundary compacts once, and a resume test confirms the same step and criteria with a capsule under a fixed token cap.

- **Phase manifests decide everything loaded** — FEATURE — value 4 — effort L — risk med — category: tokens
  Why: this merges the output-style-by-phase, tool-schema diet and skill-inlining ideas. A per-phase manifest (classify, plan, execute, verify, close) names the skills, subagent tools, output style and preamble blocks that phase loads. The repo has 73 skills, so always-loaded cost is plausible. Assumption: it is measurable from transcripts.
  Done when: `fm doctor` prints per-phase loaded-token counts, and the execute-phase count is at least 20% lower than today's all-in baseline on the fixture repo.

- **Stream gates through Monitor with a failure-only filter** — FEATURE — value 4 — effort M — risk low — category: tokens
  Why: the gates (`fm doctor`, `roundtrip.py`, `bench_hooks.py`) are long-running, and the agent currently reads or polls their output. Monitor streams a background command as notifications, so a filter can surface only the "✗ exit N" lines and the first failing assertion. The single result parser from T-0750 can do the filtering.
  Done when: a 3-minute fixture gate with one failure produces one notification carrying the failure, and zero tokens of passing output enter the context.

- **Make one content-addressed spill store with slice reads** — FEATURE — value 4 — effort M — risk low — category: tokens
  Why: cap-subagent-returns, big-output-to-evidence-file and the CLI output caps are the same mechanism built three times. A single `fm ref <hash> [--lines a:b|--grep]` lets any oversized output become a stub the model can slice later, and the evidence record can cite the same hash.
  Done when: a 50k-token subagent return reaches the parent as a stub under 300 tokens, and `fm ref` returns the exact requested slice with a matching hash.

- **Gate releases on tokens per verified task** — FEATURE — value 5 — effort M — risk med — category: tokens
  Why: Frontier 12 aims to measure Foreman's own burden, and the bench holdout and `release.py` already exist. Replaying a fixed task set per version and recording tokens per passing criterion turns every release milestone into a measured claim, and blocks a release that regresses it.
  Done when: `release.py` refuses a candidate whose replay tokens-per-pass exceeds the previous release's by more than a set margin, and prints the diff.

- **Retire any hook, skill or preamble line that doesn't pay for itself** — CLEAN — value 4 — effort M — risk med — category: tokens
  Why: delta reads were dropped after measurement showed they duplicated a built-in and added a hook process per Read. Make that audit routine: every component carries a measured token and latency cost and a measured saving or catch count (confidence from T-0217). Components that stay negative for N runs are proposed for removal.
  Done when: `fm audit cost` lists each component with cost, benefit and a verdict, and at least one fixture component with zero catches is flagged.

- **Wild: Quote each task in tokens before it starts and settle afterward** — FEATURE — value 3 — effort M — risk low — category: tokens — wild
  Why: it extends the priced plans in Frontier 13 and the budget-fit queue (T-0751). Foreman posts a token and dollar quote with an interval, then settles against actuals and trains its estimator on the error. A task that blows through its quote pauses and asks for a re-quote rather than silently continuing.
  Done when: finished tasks show quote versus actual, and the estimator's median error shrinks across a replayed history.

- **Wild: Put a token dashboard on an Artifact that the user can comment on** — FEATURE — value 3 — effort M — risk med — category: tokens — wild
  Why: Artifact offers a private page with shared data and comments sent to Claude, and Foreman uses none of it. A page lists spend per task and lane, and a comment like "too expensive" on a row becomes a standing cap for that task class. Assumption: ArtifactData can be written from the CLI side without a prompt.
  Done when: a comment on a row creates a recorded cap, and the next task of that class runs under it.

- **Wild: Hand idle-time grooming to a haiku-only cron janitor** — FEATURE — value 3 — effort M — risk med — category: tokens — wild
  Why: T-0757 asks to fold related requests into one milestone. T-0755 to T-0760 are six captures that overlap heavily, which is the evidence. A `CronCreate` job with a cold cache and no session history merges duplicates and reorders the queue using only task titles, so it costs far less than doing it in the main session.
  Done when: a fixture queue with six overlapping captures is reduced to one milestone with its sub-steps, with a recorded run cost below a set token cap.

- **Wild: Let a cheap model draft and a stronger model only edit the diff** — FEATURE — value 3 — effort L — risk high — category: tokens — wild
  Why: for mechanical steps (the Frontier 13 "one rule, not hundreds of edits" idea), a haiku builder drafts the change and the main model reviews a typed diff instead of regenerating it, paying output tokens only for the corrections. Assumption: output tokens dominate cost on these steps.
  Done when: on a fixture refactor, the strong model's output tokens fall by at least half and the verification suite still passes.
