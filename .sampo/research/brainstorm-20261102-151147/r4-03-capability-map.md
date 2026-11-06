# Brainstorm — lens: capability map

- **Block test-weakening and suppression in every diff** — FEATURE — value 4 — effort S — risk low — category: proof integrity
  Why: assumption: `fm find` and the finish gate don't diff for the shortcuts agents take. Those are new `skip`/`xfail`, `# noqa`, `@ts-ignore`, `|| true`, `--no-verify`, a loosened assertion, a deleted test, and a broad `except`. Existing ideas cover vacuous proofs and detector weakening, not the user's own diff.
  Done when: a fixture diff that adds each marker makes `fm task finish` list it by file:line as "suppression added", and a clean diff lists none.

- **Apply thresholds to changed lines only** — FEATURE — value 4 — effort M — risk low — category: quality gate
  Why: SonarQube's "clean as you code" is the model. Standard linters and complexity tools found from manifests, as the #1 steer asks, could gate new and touched code without a legacy-debt wall. assumption: nothing in the pack gates the user's repo on diff-scoped complexity, lint or duplication.
  Done when: in a fixture repo with 50 old lint errors, a diff adding one new error fails the gate naming that line, and a diff adding none passes.

- **Surface co-change and hotspot hints from git history** — FEATURE — value 4 — effort M — risk low — category: code intelligence
  Why: CodeScene-style temporal coupling costs no tokens. The pack's churn map uses Foreman task history only, and LSP blast radius (T-0788) is deferred. assumption: no git-log coupling exists.
  Done when: after editing file A, a note says "B changed in 80% of the last 20 commits touching A" when that is true in a fixture history, and says nothing otherwise.

- **Add a backport lane for release branches** — FEATURE — value 3 — effort M — risk med — category: git workflow
  Why: assumption: porting exists for other repos, and none of the ideas cherry-picks a proven fix across maintenance branches. It would use `git cherry-pick -x`, run the proof on each branch, and report green or conflict per branch.
  Done when: `fm backport T-N release/1.2 release/1.3` produces one receipt row per branch, with the proof result on each branch's tree.

- **Add a hotfix mode with a proof-debt clock** — FEATURE — value 3 — effort M — risk med — category: ceremony
  Why: the "ceremony per task kind" (T-1266) is deferred and the steers always demand full ceremony. An outage needs a fast path that is honest. Reduced proof is allowed, but it books unproven items with a 24h due time that `fm next` and the drive then enforce.
  Done when: a hotfix task closes with only a smoke proof, `fm next` lists the debt with its deadline, and past the deadline the debt becomes the top item.

- **Scope steers to paths and stacks** — FEATURE — value 3 — effort S — risk low — category: steers
  Why: more than 40 steers are all global, and the pack complains about burden. Cursor's and Continue's glob-scoped rules suggest a `paths:` or `stack:` field. Pending-set relevance selection is already filed, but authored scoping is cheap and deterministic.
  Done when: a steer with `paths: plugin/templates/web/**` is injected only when a touched file matches, and `fm burden` shows the drop.

- **Shim agent commands to be non-interactive** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: commands that wait on stdin or a pager hang a session. The shim would set `CI=1`, `GIT_TERMINAL_PROMPT=0`, `PAGER=cat`, `DEBIAN_FRONTEND=noninteractive` and an `EDITOR` stub for Bash tool calls. Existing ideas time-box provers and reap children, but none prevents the hang.
  Done when: a Bash call to `git commit` with no `-m` fails fast with a message instead of blocking, in a test with a 5 s bar.

- **Teach the guard other shell dialects and task-runner indirection** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: `T-2668` hardened bash `$(` nesting, and the dialect work is bash-centred. assumption: fish, zsh-only syntax, PowerShell and nushell aren't parsed. `make clean`, `npm run x` and `just` can hide an `rm -rf` in a recipe the typed line never shows.
  Done when: a fixture where `make clean` expands to `rm -rf ~` is blocked, as are `Remove-Item -Recurse -Force $HOME` and fish `rm -rf ~`, and benign recipes pass.

- **Emit forge-side enforcement matching the local guard** — SECURITY — value 3 — effort M — risk med — category: out-of-session
  Why: the open question "which guarded surfaces does Foreman not control (IDE, cron, CI)". Generate GitHub rulesets, required checks and CODEOWNERS stubs, plus a pre-receive hook, that reproduce the no-force-push, protected-path and secret-scan rules where a rogue session can't skip them. Output is a reviewed file, applied only by the user.
  Done when: `fm guard --emit-forge` writes a ruleset JSON, and a test shows each local push-class rule has a forge counterpart or a listed "can't express".

- **Choose injected-note wording per model family by exam** — FEATURE — value 3 — effort M — risk med — category: multi-model
  Why: Foreman runs on Claude, Codex, Gemini and opencode through `fm code`, but the notes are one phrasing. assumption: wording is untuned per family. The steer-expansion exam shows wording changes measured outcomes, so run the free arms and the Haiku smoke across 2 variants per family.
  Done when: for one family, two phrasings are scored on the same held-out scenarios and the better one becomes that family's default, with the numbers in `fm exam`.

- **Harvest dated TODOs into the queue** — FEATURE — value 2 — effort S — risk low — category: debt
  Why: `TODO(2026-12-01)` or `TODO(T-id)` comments become tasks with wake dates, and the gate fails after the date. This is distinct from dated deferrals, which only cover Foreman's own tasks.
  Done when: a fixture with an expired `TODO(2026-01-01)` yields a queued task naming file:line, and a future date yields nothing.

- **(wild) Export closed tasks as SWE-bench-style instances** — FEATURE — value 4 — effort M — risk low — category: benchmark
  Why: the red-first proof already gives FAIL_TO_PASS tests, and the pass-before tests give PASS_TO_PASS. Exporting `repo@start`, the problem statement and those lists feeds the duel (T-1231) and the long-horizon tier with the user's own repos, which no outside scenario can match. wild.
  Done when: `fm export-bench T-N` writes an instance JSON whose FAIL_TO_PASS tests fail on the start tree and pass on the landed tree when replayed.

- **(wild) Prove the user's CI can go red** — FEATURE — value 3 — effort M — risk med — category: CI trust
  Why: "Check CI against local gates" assumes CI can fail. A throwaway-branch canary pushes a known-red commit and expects a red check within a bound. A CI that stays green on a planted failure is the worst silent gauge. Needs a push grant and `fm ship` rules. wild.
  Done when: on a scratch branch, the canary commit turns the check red inside the timeout and the branch is deleted; if the check stays green the verb exits nonzero and says so.

- **(wild) Record which diff hunks the user actually read** — FEATURE — value 3 — effort L — risk med — category: review
  Why: "reviewed" currently means a click or a quiet minute. An opt-in, local-only editor extension logs per-hunk dwell, so landed work shows "3 hunks never on screen". It extends the rubber-stamp detector and the unread-lines map. Data stays on the machine. wild.
  Done when: with the extension on, a landed diff's receipt lists hunks with under 2 s dwell, and with it off nothing is written.

Next question: of these, which are already built under another verb name, since the pack's own list shows most capability-map gaps are now filled? A grep-backed "already built" pass should precede filing.
Next question: which of these would the user feel in their first week, given that dropped ideas were mostly "already built" or value 2?
