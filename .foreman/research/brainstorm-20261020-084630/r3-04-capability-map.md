# Brainstorm — lens: capability map

- **Pin repo-supplied commands behind a trust prompt** — SECURITY — value 5 — effort M — risk med — category: security
  Why: assumption: briefs, gates and `verify` commands are committed to git and run automatically in bypass mode. Ideas like drop-in gates, git-carried hints and `.foreman/known/` bundles widen this. A pulled change to a verify line is code execution. The pack covers untrusted hints but not untrusted commands.
  Done when: after a `git pull` changes a task's verify command, `fm task prove` refuses to run it until `fm trust` records its hash, and a test shows an unchanged command runs silently.

- **Harden the web UI's local server** — SECURITY — value 4 — effort S — risk low — category: security
  Why: assumption: the web UI listens on a local port and can approve asks and edit tasks. Local dev UIs are open to DNS rebinding and cross-origin POSTs. The pack has "survive restarts and version skew" but nothing on binding or auth.
  Done when: a request with a foreign `Host` or `Origin`, or a missing per-launch token, gets 403 on every mutating route, and the server binds to loopback only (checked by test).

- **Mutate the changed lines and require a test to notice** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: `fm task prove` already shows a test fails without the change. The "verification matters" spec suite shows the quality gap is weak tests. A proof that survives mutation of the touched lines is stronger.
  Done when: `fm task prove --mutate` flips operators and constants on the diff's added lines, reports surviving mutants as red, and a fixture with a test that never asserts is flagged.

- **Give each lane its own ports, database and temp dirs** — FEATURE — value 4 — effort M — risk med — category: lanes
  Why: parallel lanes run gates and dev servers at once. Load-sensitive criteria and flaky merge-train failures are in the pack; collisions on ports, SQLite files and `/tmp` paths are a likely cause. Assumption: the project under work uses fixed ports.
  Done when: two lanes started together each get distinct `PORT`, `TMPDIR` and DB-path env values, and a test that binds a fixed-offset port passes in both at once.

- **Declare triggers in one file** — FEATURE — value 4 — effort M — risk med — category: automation
  Why: the idea list scatters "turn CI red into a FIX lane", "issues into tasks", "dependency alerts", "nightly gardener" and "cloud routines" (T-0793). None share a mechanism. One `triggers` file with `on: ci-red | issue | schedule | push` and an action that enqueues a brief would cover them. The unattended contract and budget caps would apply to every trigger.
  Done when: a trigger `on: ci-red → capture FIX` creates exactly one deduped brief when a red run is simulated, and `fm triggers ls` shows its last fire.

- **Open a cross-project home screen** — FEATURE — value 4 — effort M — risk low — category: ui, devices
  Why: assumption: the user runs Foreman in several repos, and every view in the pack is per-repo. A single page lists each repo's active task, pending `fm ask`, blocked items and spend today.
  Done when: `fm home` and the web UI route list every repo Foreman has run in, with a pending-ask count, and clicking one opens that repo's view.

- **Refuse hand edits to generated files and name the generator** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: assumption: builders edit `dist/`, lockfiles and files headed "DO NOT EDIT". The edit succeeds and is silently overwritten on the next build. Edit-time fencing exists for dirty files but not for generated ones.
  Done when: an edit to a file with a generated header or a map-listed output path is refused with the generator command, and a `--because` override lets it through once.

- **Support GitLab, Gitea and Forgejo beside GitHub** — FEATURE — value 3 — effort M — risk low — category: integrations
  Why: the CI badge, `github-actions` card, ship-to-PR, issue import and review-thread ideas all assume GitHub. A small forge interface (`gh`, `glab`, `tea`) opens the product to other teams.
  Done when: the PR-open and CI-status calls run through a forge adapter, and a fake `glab` fixture passes the same ship test as the `gh` one.

- **Run to a deadline and cut scope to fit** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: the user's constraints are usage and time. "Bare continue as a priced contract" and the ETA ideas forecast, but nothing lets the user say "until 17:00". Assumption: tasks have recorded durations for the forecast.
  Done when: `fm drive --until 17:00` orders the queue by value per forecast minute, stops at the deadline with a receipt of what was left out, and a clock-stubbed test shows the cut.

- **Package Foreman for AUR, Homebrew and a Nix flake** — CLEAN — value 2 — effort S — risk low — category: distribution
  Why: assumption: the user is on Arch, per T-0325's `pacman` note. Install currently goes through the Claude plugin marketplace only. A packaged, pinned install also helps "pin the Foreman version per repo".
  Done when: a PKGBUILD and a flake build the CLI from a tagged release in a clean container and `fm doctor` passes.

- **Wild: Peek at a repo before opening it** — FEATURE — value 4 — effort M — risk low — category: security
  Why: wild. `fm peek <url|path>` shallow-clones into a throwaway directory and lists everything that would run on first open: `.claude/settings.json` hooks, `.mcp.json` servers, `CLAUDE.md` instructions, `.foreman` verify commands, package install scripts. It flags prompt-injection phrasing. This extends the trust prompt to repos the user hasn't opened yet.
  Done when: against a fixture repo with a malicious hook and a `.mcp.json`, `fm peek` prints both with file:line and writes nothing outside its temp dir.

- **Wild: Speak the user's language in the pane and refusals** — FEATURE — value 2 — effort M — risk low — category: ui
  Why: wild. Stable message codes (an idea above) allow a catalog per locale. Refusals and close lines would be translated while commands stay English. Assumption: some users do not read English first.
  Done when: with `FM_LANG=de`, a guard refusal and the close line print from the catalog, and a missing key falls back to English in a test.

- **Wild: Watch rivals' changelogs and file capability-gap briefs** — FEATURE — value 3 — effort S — risk low — category: roadmap
  Why: wild. The pack turns only Claude Code's notes into briefs. A weekly check of Codex, Aider, Cursor and Copilot release notes would show what "best-in-class" now means. It runs only when the user asks, since it needs network.
  Done when: given saved changelog fixtures, `fm radar` captures deduped briefs naming the source line, and a rerun on the same input creates none.
