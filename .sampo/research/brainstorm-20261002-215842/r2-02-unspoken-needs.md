# Brainstorm — lens: unspoken needs

- **Write a "decision log" that records every user yes/no and replays it as a standing rule** — FEATURE — value 5 — effort M — risk low — category: autonomy
  Why: The user wants full autonomy and no handed-off commands, yet every protected-core edit and plugin update still needs a yes, and the pack lists approvals as a known limitation. The need behind it is "stop asking me the same question." Log each approval with its scope (path glob, command shape, task type), propose a durable rule after the second identical yes, and let the user revoke from one list.
  Done when: after two approvals of the same protected-core edit class, the third occurrence proceeds without a prompt and `fm decisions` shows the rule with a revoke option.

- **Add a per-project "slow path" profile that tunes gates automatically** — PERFORMANCE — value 5 — effort M — risk med — category: speed
  Why: One project's `cargo test` takes a median of 8 minutes and runs about once per task, and gates account for 18.8 hours. Existing ideas cover caching and affected-test selection, but nothing learns the per-project cost and then picks a strategy (run in background, defer to queue end, or split by crate). The profile would be built from the ledger's own timings.
  Done when: on a project with gate median > 5 min, `fm check` defers the full suite to queue end by default, and the profile is visible in `fm ui --json`.

- **Turn pushback into a "you told me not to" tripwire** — FEATURE — value 4 — effort M — risk med — category: memory
  Why: The user's corrections are recurring and specific ("L, T, M mean nothing", "clean up your output", "no commands handed to me"). Today these live only in the session. Extract each correction as a testable rule, store it with its source quote, and warn before a plan or output step that would violate one. This differs from the "replay pushback as regression checks" wild idea because it acts at plan time, not after the fact.
  Done when: a plan that includes a bare tier letter in user-facing output is flagged at `fm task plan` with the quoted correction.

- **Add a "plan fits budget" check using historical time and token cost per task type** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: The user is usage-sensitive and complains about multi-hour tasks, and the pack has 287 tasks of measured data. The pack proposes budgets and receipts, but not the pre-commit step that says "this plan will take about 3 h and 40% of your weekly allowance, trim or proceed?"
  Done when: `fm task plan` prints an estimate range from similar past tasks, and a plan over the configured limit requires an explicit trim or override.

- **Make every Foreman message answer "what changed for me?" first** — FIX — value 4 — effort S — risk low — category: output
  Why: The user has asked for cleaner output twice and for plain words once (size words instead of S/M/L). Assumption: a lint pass over all user-visible strings is still missing. It would reject jargon (stage names, task IDs without titles, bare letters) and require the first line to state the outcome.
  Done when: a test scans the fm and mod string tables and fails on bare tier letters or ID-only references, and a sampled close-out starts with an outcome sentence.

- **Auto-draft the "why" for an inbox capture from the surrounding conversation** — FEATURE — value 3 — effort S — risk low — category: capture
  Why: Inbox items like T-0077 and T-0094 are one-liners that need re-derivation later, and the user wants Foreman to catch what they "can't say." On capture, attach the last few user turns and the active step as context so the later brief is not a cold start.
  Done when: a captured item shows its source turn and active step in `fm task show`.

- **Wild: Run a "second opinion" Haiku that argues the user's likely objection before every plan is shown** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: The user says brainstorming misses "things I want but don't know how to say" and also pushes back often. Build the objections from the correction history above ("too slow", "too noisy", "too many tokens"). Show only objections that match a past one. wild
  Done when: a plan that adds a long test run surfaces "you've objected to slow gates before" with the quote, and a plan with no match shows nothing.

- **Wild: Give each task an "exit ramp" that proposes stopping at the 80% result** — FEATURE — value 4 — effort M — risk med — category: speed
  Why: Tasks taking hours with 18 bookkeeping calls each suggests perfectionism by process. At each step, estimate remaining cost against remaining value and offer "ship now, capture the rest as a follow-up" with the leftover filed in the inbox automatically. wild
  Done when: after criteria are met and only polish remains, Foreman offers a one-key close that files the remainder as an inbox item.

- **Wild: Keep a "taste profile" built from what the user accepts and edits in the output** — FEATURE — value 3 — effort L — risk med — category: personalization
  Why: The user states preferences piecemeal (quiet output, size words, animated look). Mine accepted and rewritten outputs, plus approvals and rejections of brainstorm ideas, to produce a small profile that conditions brainstorms, formats and defaults. Assumption: enough signal exists in the ledger. wild
  Done when: `fm taste` lists at least five learned preferences with their evidence, and brainstorm packs include them.

- **Wild: Offer a "teach Foreman" mode where the user narrates a fix once and it becomes a playbook** — FEATURE — value 4 — effort L — risk med — category: playbooks
  Why: The user wants more playbooks without token burn, and the usual route is writing them by hand. Record a successful task's tool and step sequence, generalize it into a playbook draft with parameters, and run it with Haiku-level cost the next time a similar task arrives. wild
  Done when: after a finished task, `fm playbook from-task T-xxxx` produces a runnable playbook that reproduces the steps on a similar task.
