# Brainstorm — lens: capability map

- **Probe the local model's real context window** — FIX — value 4 — effort M — risk low — category: local models
  Why: assumption: Ollama and LM Studio often load with a 2–8k context and silently truncate the prompt. The model then returns garbage or nothing, which looks like "it just isn't doing anything". The pack's runner work (T-1328) lists endpoints but doesn't check this.
  Done when: against a fake endpoint that truncates at 2k tokens, `fm code` prints "context 2048 < needed 6100 for this plan; set num_ctx or pick a model" before the first slot call.

- **Run every child non-interactive and name the prompt it hangs on** — FIX — value 4 — effort M — risk low — category: hangs
  Why: assumption: a worker's `git commit` waiting on a pinentry or credential helper, `npm init`, or `sudo` blocks forever with no output. That is the same symptom as the nixie run. Neither the watchdog idea nor the lean-profile idea covers it.
  Done when: a fake runner that runs `read x` or a signing commit is stopped within 10 s with "waiting for input: <the prompt text>", and `GIT_TERMINAL_PROMPT=0` plus a closed stdin are set for all children.

- **Serve the project's dependency docs from the installed versions** — FEATURE — value 4 — effort M — risk low — category: context
  Why: assumption: small and local models hallucinate APIs. A local index built from `site-packages` and `node_modules` docstrings, types and READMEs pins the exact version and sends nothing out. The repo-map idea covers the repo's own code, not its dependencies.
  Done when: a request that uses a function from a pinned fixture package gets that function's real signature in the plan prompt, and the same fixture at a different version gets the other signature.

- **Cap spend globally across projects and runners** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: the pack plans per-run caps and weekly per-project reports. The app now runs many projects and runners unattended, and nothing stops the sum.
  Done when: with a daily cap of $1 and a fake runner billing $0.40 per call, the third queued run across two projects refuses to start and the home screen shows "cap reached, resets 00:00".

- **Hand off a half-done task between runners with a packet** — FEATURE — value 4 — effort M — risk med — category: runners
  Why: fallback on classified failure and pausing at usage limits are planned. Neither says what the next runner knows. The packet would be the plan, the checks, the diff so far, and the red output.
  Done when: killing runner A mid-step makes runner B (fake) receive a packet containing the diff and last failing check output, and the task closes with commits from both.

- **Compile a pasted stack trace or bug report into a failing test first** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the harness already runs "checks fail first". The nixie-style "it's broken" requests arrive as pasted errors, and nothing turns those into the red check.
  Done when: a pasted Python traceback against a fixture repo yields a test that fails with the same exception type before any edit, and the run refuses to proceed if it can't reproduce.

- **Select only the tests the change touches during verify** — PERFORMANCE — value 3 — effort M — risk med — category: verify
  Why: assumption: step-level verify runs the full gate every time, which is slow with local models and wastes the worker's time budget. A selected run is used for steps and the full gate for the close.
  Done when: on a fixture with 50 test files, a one-file step runs only the mapped test, and the final close still runs the full gate (both asserted in the run log).

- **Honour proxy, custom CA and offline mirrors in the model client** — FEATURE — value 3 — effort S — risk low — category: setup
  Why: assumption: a stdlib client that ignores `HTTPS_PROXY`, `SSL_CERT_FILE` or a corporate CA fails with an opaque TLS or timeout error. `fm code doctor` should name the cause.
  Done when: with a fake proxy and a self-signed CA, a request succeeds when configured and fails with "TLS: unknown CA, set ca_file" when not.

- **Enforce an org policy file for allowed runners, endpoints and paths** — SECURITY — value 3 — effort M — risk med — category: policy
  Why: assumption: "manage any CLI" means a team will want to forbid some runners or cloud endpoints. The `--local-only` idea is a single switch, and this generalises it into a file that the guard's own safety rules can't be loosened by.
  Done when: a policy that denies `api.openai.com` makes a run configured with that endpoint refuse to start, naming the policy line, and a policy can only tighten, never loosen, the guard.

- **Turn the user's hand edits after a run into lessons** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: the lessons/confidence work (T-0217) learns only from recall and passes. A user fixing the result by hand is the strongest signal that the run was wrong, and it is currently thrown away.
  Done when: committing a change within 10 minutes of a closed run touching the same files creates a candidate lesson with the diff attached, shown on the next run's plan.

- **Wild: Expose the runner router as a local OpenAI-compatible endpoint** — FEATURE — value 3 — effort L — risk med — category: gateway
  Why: wild: any tool (editors, scripts, other agents) could point at `localhost:PORT` and get fm code's auto-default, fallback, quota and spend-cap logic. The MCP and ACP ideas expose the harness, not the model routing.
  Done when: `curl` to `/v1/chat/completions` returns a completion from a fake runner and falls back to a second one when the first returns 429.

- **Wild: Pre-mortem the plan with a second runner and turn its failure modes into checks** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: wild: a different runner lists how the plan could fail, and the harness converts the checkable ones into extra criteria. This sits between the "second opinion only when proof is thin" and "cross-examine the diff" ideas, but acts before any edit.
  Done when: on a fixture request, the pre-mortem adds at least one new failing-first check that the plain plan lacked, visible in the plan view.

- **Wild: Bisect a regression with the harness** — FEATURE — value 3 — effort L — risk med — category: debugging
  Why: wild: "this broke last week" becomes a request. The harness writes the failing check, runs `git bisect` with it in a throwaway worktree, and proposes the fix against the culprit commit.
  Done when: on a fixture repo with a planted regression 20 commits back, `fm code "login broke"` names the correct commit and leaves the user's worktree untouched.

- **Scope runs to a monorepo package with its own gates and runner** — FEATURE — value 3 — effort M — risk low — category: projects
  Why: assumption: "the project is the current directory" breaks in monorepos, where the gate and the right model differ per package.
  Done when: in a fixture with two packages having different test commands, a request inside `pkg-b` runs only `pkg-b`'s gate and records the package in the task.
