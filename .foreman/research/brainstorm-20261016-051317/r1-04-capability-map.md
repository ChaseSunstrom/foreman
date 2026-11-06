# Brainstorm — lens: capability map

- **Add `fm guard why "<cmd>"` with the real cwd** — FEATURE — value 5 — effort S — risk low — category: guard DX
  Why: the review says the main thread twice wrote scratch scripts to replay a command through the hook (T-1125, T-1141), and no `fm` verb answers "would the guard allow this here, and why". "Explain why Foreman blocked something" is in the ideas list, but this is the dry-run, pre-emptive form.
  Done when: `fm guard why "cat <<EOF | fm edit ..." --cwd X` prints allow or deny, the rule matched and the span that matched; a test pins its verdict to the live hook's on 20 recorded commands.

- **Lint a verify command when it is added** — FIX — value 5 — effort S — risk low — category: verification
  Why: the review says verify commands are often wrong (a nonexistent test module, `npm test` with no npm) and are caught only on the run. T-1128 and T-1133 only made such runs editable.
  Done when: `fm verify add "python -m nosuch"` fails at add time and names the missing module or binary, and `--no-check` is the only way past it.

- **Generate the help and verb registry from per-verb files** — CLEAN — value 4 — effort M — risk med — category: dev workflow
  Why: every builder edits the single HELP_TIERS line in fmcli.py, and nearly every second merge conflicted (T-1059, T-1062). Each verb would own one metadata file and the registry would be built from them.
  Done when: two lanes that each add a verb merge without a conflict, and `fm --help` output is byte-identical to before.

- **Index brief frontmatter in a stat-keyed sidecar** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: T-1140 fixed only the hooks. The review says other commands still parse all 1,069 briefs, and `fm state --json` once took over 120 s under load.
  Done when: `fm state --json` on 1,000+ briefs takes under 1 s warm, and the index rebuilds correctly after a brief is edited, deleted or corrupted.

- **Throttle lanes by system load** — FEATURE — value 4 — effort M — risk med — category: lanes
  Why: load reached 30–60 with 4 builders, a load-sensitive criterion failed a merge once and then passed, and merges re-run criteria sequentially. Lane count should follow load, and the criteria timeouts should too.
  Done when: with a simulated load of 40, `fm lane` dispatch holds back new builders and says why, and a criterion that fails only under load is retried once and labelled "load-flaky".

- **Resolve builder paths against the worktree root** — FIX — value 4 — effort S — risk low — category: lanes
  Why: builders cd into subdirectories and relative paths double (`mods/foreman-ui/mods/foreman-ui/...` in lease paths).
  Done when: a lease or claim path that doubles a directory segment is normalised, or rejected with a hint, and a test reproduces the `mods/foreman-ui` case.

- **Add a Renovate-style dependency upgrade lane** — FEATURE — value 3 — effort M — risk med — category: maintenance
  Why: assumption: Renovate and Dependabot are the reference tools in this space. The pack shows dependency-trial and new-dependency checks but no routine bumps. A lane would bump one dependency, run the gates, and queue the merge or a FIX task.
  Done when: on a fixture repo with an outdated pin, `fm deps bump` makes one branch per bump and records pass or fail with the failing gate.

- **Add SAST and vulnerability scanners as pluggable gates** — SECURITY — value 3 — effort M — risk low — category: security gates
  Why: assumption: Semgrep, OSV-Scanner and gitleaks are table stakes. The pack covers secrets and injection but has no static-analysis or CVE gate, and `fm doctor` can only detect the scanners, not run them.
  Done when: if `semgrep` or `osv-scanner` is installed, the close gate runs it on the diff and lists new findings as tasks, and a missing scanner is shown as skipped, not green.

- **Gate close on diff coverage of changed lines** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: assumption: Codecov and diff-cover do this. Mutation proof and the edit-time sentinel exist, but nothing says "the lines you changed ran under a test".
  Done when: a close with an untested changed function lists its line ranges, and `--waive` records why.

- **Open the pane in a tmux or zellij split** — FEATURE — value 3 — effort S — risk low — category: surfaces
  Why: the pack shows a mod and a web UI, but the pane would also work from a multiplexer for users without the mod. Related: "Fall back to a one-line statusline" exists.
  Done when: `fm ui --tmux` opens or reuses a split running the pane, and `--close` removes it.

- **Wild: Add an interactive guard playground to the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. It extends `fm guard why` with live typing, the matched rule highlighted, and one-click "this was a false positive" capture that writes a regression case.
  Done when: typing a command in the page shows a verdict within 200 ms, and a marked false positive becomes a failing test fixture.

- **Wild: Turn Sentry or log alerts into overnight FIX lanes** — FEATURE — value 4 — effort L — risk high — category: integrations
  Why: wild; assumption: the user runs a service with an error tracker. The issue-intake and push-alert items exist but not error-tracker ingestion. A stack trace becomes a reproduce-first FIX task, with the diff waiting for review in the morning, never auto-shipped.
  Done when: a fixture Sentry JSON payload yields a FIX task whose first step reproduces the error, and nothing is pushed.

- **Wild: Write personalised release notes for each user** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: wild. The installed foreman-ui is 0.7.0 against the repo's 0.17.0, and marketplace users lag. Notes would list only the changes touching verbs and cards the user's own ledger shows them using, plus what is new to try.
  Done when: `fm whatsnew` between two versions prints only items that match the user's top-used verbs, with a "more" count for the rest.

- **Wild: Run Foreman as a CI action that comments on PRs** — FEATURE — value 3 — effort L — risk med — category: CI
  Why: wild. PR-review-thread resolution exists locally. A GitHub Action would run `fm doctor`, the guard linter and the brain diff on a teammate's PR, with no Claude session required.
  Done when: a workflow on a fixture PR posts one comment containing the doctor result and the brain diff, and exits non-zero on a red gate.
