# Brainstorm — lens: capability map

- **Resolve bare `fm` inside a lane to that lane's own copy** — FIX — value 4 — effort S — risk low — category: lanes
  Why: the round 4 review says builders can't run their own new `fm` flags because bare `fm` resolves to the main checkout, so they must type `python3 plugin/bin/fm`.
  Done when: a test runs `fm <newflag>` from a lane worktree that adds the flag, and it succeeds, while the same command from the main checkout uses main's copy.

- **Auto-record reviewer findings from review output** — FEATURE — value 4 — effort S — risk low — category: feedback loop
  Why: the defect-class feed to builder briefs (T-1164) starves because `fm task finding` is one manual call per finding.
  Done when: a test feeds a reviewer's structured result with 3 confirmed findings through the review verb, and `fm lane brief` then lists those 3 defect classes without any manual call.

- **Mine guard refusals into a digest that shows the commands** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: the review notes that the friction digest counts refusals but never shows them, and a hand-written transcript miner had to be built twice (it showed that "data-only cat writes" and "literal variables" were false premises).
  Done when: `fm guard mine --days 4` prints each refused full command (secrets redacted), its replayed verdict from `fm guard try`, and a per-reason count, and a test with 3 seeded refusals shows all three.

- **Learn verb aliases from the unknown-command ledger** — FEATURE — value 3 — effort S — risk low — category: DX
  Why: builders and weak agents guess names like `fm task list`, and the nearest-name hint only suggests the right one after the failure.
  Done when: a test records `task list` as an unknown command 3 times, after which `fm task list` runs the intended verb and notes the alias once.

- **Let the autonomous drive run review and ideas headlessly** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the pack says /foreman:review and /foreman:ideas only run when the user types them, and the user is AFK.
  Done when: a drive test with a fake child reaches the review step at close of an L task, runs `fm` review without a typed slash command, and logs the findings on the task.

- **Derive gates from CI and pre-commit config** — FEATURE — value 4 — effort M — risk med — category: gates
  Why: assumption: best-in-class tools (act, pre-commit, Danger) reuse the repo's own checks, while Foreman's gates are declared separately, so they can drift from CI.
  Done when: on a fixture with `.github/workflows/test.yml` and `.pre-commit-config.yaml`, `fm gates --import` proposes the matching commands, and `fm doctor` flags a gate that CI doesn't run.

- **Add inline diff comments in the web UI that become lane steers** — FEATURE — value 4 — effort L — risk med — category: web UI
  Why: assumption: Cursor, Copilot Workspace and GitHub review all let you comment on a hunk, and the web UI is the only surface found, yet it can't steer a running builder from a diff.
  Done when: a browser test comments on a line in a lane's diff, and the lane's next brief or inbox shows the comment quoted as untrusted data with file and line.

- **Add a command palette and deep links to the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: assumption: every task, lane and card id already appears in the UI, but ids aren't clickable or searchable from one place.
  Done when: a browser test presses `/`, types `T-1158`, and lands on a URL that reloads to the same task view, with the keyboard focus order passing an accessibility check.

- **Run fm children against a local OpenAI-compatible endpoint** — FEATURE — value 4 — effort L — risk med — category: local models
  Why: the standing asks include working for weak or small local models, and ideas/review/audit children are `claude -p` only. T-0335 and T-0336 show non-Claude paths are still unverified.
  Done when: with `FM_CHILD_ENDPOINT` set to a stub server, `fm ideas` completes one round against it with zero `claude` invocations and reports the model used.

- **Add `fm doctor --fix` for the safe findings** — FEATURE — value 3 — effort M — risk med — category: DX
  Why: assumption: doctor reports problems, as with the stale foreman-ui in T-0418, but each one is a manual follow-up, and the last-mile fix commands are known.
  Done when: a fixture with 2 fixable and 1 unfixable finding yields 2 applied fixes, each logged and undoable, and 1 reported with its manual command.

- **Show real paths in the guard's "it could be …" guess** — FIX — value 2 — effort S — risk low — category: guard
  Why: the review notes that it glues a command word into the path (e.g. `/repo/cd/w.out`), which misleads whoever is reading the refusal.
  Done when: a test with `cd w && cat > w.out` shows the guess as `<cwd>/w/w.out` or no guess at all, never a word-glued path.

- **Wild: Route all model traffic through a local proxy that Foreman owns** — FEATURE — value 4 — effort L — risk high — category: observability
  Why: wild; assumption: spend is estimated from the transcript today, while LiteLLM and Helicone give exact per-request cost, replay and failover. A local `ANTHROPIC_BASE_URL` proxy could attribute tokens per lane and fall back to a local model on rate-limit.
  Done when: with the proxy on, two lanes' requests are listed with exact token counts per lane, and a recorded request can be replayed from the ledger.

- **Wild: Offer GitButler-style virtual branches for the user's own dirty tree** — FEATURE — value 3 — effort L — risk high — category: git
  Why: wild; assumption: T-1169 now keeps the user's uncommitted work out of task commits, so the next step is letting that work be grouped into named, separately committable stacks, as GitButler does.
  Done when: a test with edits to 3 files assigned to 2 stacks produces 2 commits with the right files each, and the working tree is unchanged.

- **Wild: Show a repo map page with hotspot, ownership and task overlays** — FEATURE — value 3 — effort L — risk low — category: web UI
  Why: wild; `fm map` indexes 1524 files and the pack records conflict hot spots and hotspot scoring in the idea list, but the user can't see any of it as a picture. A treemap or code-city view could show lane scopes, conflict history and open tasks per directory.
  Done when: the page renders a treemap from `fm map` data, colours a seeded conflict-prone file, and clicking a directory lists its open tasks, with empty and loading states shown.
