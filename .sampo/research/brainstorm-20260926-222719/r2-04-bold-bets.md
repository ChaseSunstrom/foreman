# Brainstorm — lens: bold bets

Most of the remaining space is marginal. I dropped an MCP tool layer for output compression (it adds per-session schema tokens, which cuts against the token goal), a resident file-watch daemon (hooks are already ~30 ms), and semantic conflict detection between queued tasks. These six are the ones I'd still build, best first:

- **Pre-grant permissions from the plan's own commands and scope** — FEATURE — value 4 — effort M — risk med
  Why: the user never runs commands and consent is yes/no only, so every permission prompt stalls an interactive turn or an unattended `fm run`. The brief already declares its verify commands and scope globs. Assumption: a PreToolUse `allow` decision is honored by the harness.
  Done when: in a test, the exact verify command and in-scope edits return allow. A command with an extra pipe, a different flag, or an out-of-scope path falls through to normal prompting, and the guard's deny rules still win.

- **Prove changed lines were executed by the evidence commands** — FEATURE — value 4 — effort M — risk med
  Why: the verification grade and `fm task prove` show tests can fail, but not that the edited lines ran under the recorded checks. Passing tests that never touch the diff still grade "ok". Assumption: Python can use stdlib `trace`; other stacks use a detected coverage tool or report "unknown".
  Done when: a task whose diff has an unexecuted hunk shows "uncovered: file:lines" at done and its grade drops. A fully covered diff is unchanged, and a missing tool degrades to "unknown" without blocking.

- **Warn about missing companion edits from git co-change history** — FEATURE — value 3 — effort M — risk low
  Why: "Docs impact" and scope drift catch known misses. They can't catch project-specific pairs such as a registry, snapshot, schema, migration, or changelog that historically changes with a file. Assumption: the repo has at least ~50 commits.
  Done when: on a fixture repo where A.py and registry.py changed together in 8 of 9 commits, editing only A.py makes `fm task done` list registry.py as a companion. A miss can be waived with a one-line reason.

- **Price a proposed rule or gate against past transcripts with `fm whatif`** — FEATURE — value 4 — effort M — risk low
  Why: about 200 ideas are now candidates, and the user's constraint is weekly tokens. Live A/B trials are slow and hook-trace replays test correctness, not spend. The `fm cost` transcript scanner already exists. Assumption: transcripts contain enough tool-call detail to simulate a guard.
  Done when: `fm whatif deny-unchanged-rereads` prints estimated tokens saved and turns affected over the last N sessions, with the example events. The numbers match a hand count on a fixture transcript.

- **Order `fm check` by failure likelihood and fail fast in the red loop** — PERFORMANCE — value 3 — effort S — risk low
  Why: the flake ledger and timings already exist, but selection (`--affected`) doesn't say which test to run first. During a FIX loop a red result is the signal that matters. Assumption: the runner accepts explicit test ids (pytest, unittest and similar).
  Done when: after a recorded failure, the next `fm check --loop` runs that test first and stops at the first failure. A full run is still required before done, and the timing on a fixture drops.

- **Recall abandoned and reverted approaches at plan time** — FEATURE — value 3 — effort S — risk low
  Why: "ruled out" lines and failures met are carried only within a task or handoff. Abandoned tasks and `git revert` commits are the cheapest source of "don't do this here", and recall doesn't index them. Assumption: abandoned briefs keep their reason.
  Done when: a new plan touching a file where an earlier task was abandoned or reverted gets one "previously abandoned: <reason>" line in the Related section at focus. Unrelated plans get none.
