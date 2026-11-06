# Brainstorm — lens: unspoken needs

- **Give every unbounded request a finish line** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: "super improve… etc. etc. etc." became T-0760 (RESEARCH M) with no end condition, so the run either never stops or stops arbitrarily. wild: the stopping rule is pre-registered, and a farewell report grades it.
  Done when: a superlative-only request ("make it better") gets a written metric target, a time/token budget and a stop rule at intake, and the close-out reports each against actuals.

- **Rebind project scope when the session changes directory** — FIX — value 3 — effort S — risk low — category: scope
  Why: the user works across Foreman, JARVIS and consumer repos, and "resolve which Foreman a request is about" is already listed. Nothing handles a mid-session `cd`. assumption: Claude Code exposes a CwdChanged hook event.
  Done when: after `cd` into another registered project, the next captured request lands in that project's queue and the band shows the new project name.

- **Check docs when a task finishes, not at `fm doctor`** — FIX — value 3 — effort S — risk low — category: docs
  Why: T-0686 shipped `fm bisect` without naming it in MASTER.md, and `fm doctor`'s self-docs check failed only afterwards.
  Done when: `fm task finish` on a task that adds a CLI verb or setting without a MASTER.md entry is refused with the missing name, and passes once the entry exists.

- **Make notifications work with zero configuration** — FEATURE — value 4 — effort M — risk low — category: notifications
  Why: `fm notify` only runs a user-supplied shell command, and the user never wants to be handed setup steps.
  Done when: on a fresh install with no notify setting, a needs-you event reaches the user through the first working channel (Desktop tray, terminal OSC, `notify-send`, then PushNotification), and `fm doctor` names the channel in use.

- **Publish only redacted classes to Artifacts** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: many earlier ideas publish the queue and ledger to claude.ai Artifacts, which is a cloud store. The user runs a hardened local setup and Foreman already has redaction code. assumption: briefs and diffs may contain private text.
  Done when: the default Artifact payload holds only task ids, titles, status and step counts. Brief bodies, paths and diffs appear only after a per-project opt-in, and a test seeds a secret into a brief and finds it absent from the payload.

- **Lint skills against the live Claude Code surface** — CLEAN — value 3 — effort S — risk low — category: dev experience
  Why: Foreman has 73 skills, and adopting more native features adds more tool names, hook events and flags that can silently go stale. The existing "diff the tool list" idea checks usage, not references.
  Done when: `fm doctor` fails and names the skill file and line for any referenced tool, hook event or `claude` flag missing from the installed Claude Code.

- **Stamp token and speed claims with a measurement** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: two features were built and then dropped or duplicated after measurement (delta reads, Frontier 02, ~109 tokens over 30 days). The measurement came after the build.
  Done when: a FEATURE brief claiming token or latency savings cannot leave `captured` without a transcript-derived baseline number, and one with no baseline is refused with the query to run.

- **Collect changelog fragments per task** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: the CHANGELOG.md:10 scan false positive, hand-assembled release lists ("T-0688 to T-0691") and lane merges all touch one file.
  Done when: each finished task writes a fragment file, and `release.py` builds the CHANGELOG section and the task-range title from fragments with no manual edits.

- **Pre-cut a release candidate each night** — FEATURE — value 3 — effort M — risk med — category: release
  Why: the user repeatedly asks for a release with a task range and a theme (1.2.17 to 1.2.27).
  Done when: after a green night run, an RC branch with generated notes exists, and a one-word "release" promotes it to GitHub main and JARVIS without re-running the gates.

- **Run hooks through a native HTTP transport to `fm serve`** — PERFORMANCE — value 3 — effort M — risk med — category: latency
  Why: hooks are latency-gated by `bench_hooks.py`. `fm serve` already exists. assumption: Claude Code supports HTTP-type hooks and the local server can answer within budget.
  Done when: PreToolUse p50 in `bench_hooks.py` drops below the Python-spawn baseline, and killing the server falls back to the command hook with the same verdicts.

- **Trigger the test sentinel from file-change events** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: T-0214 is deferred. Edit-time hooks miss Bash writes, formatters and the user's own edits. assumption: a FileChanged event exists.
  Done when: editing a file by `sed -i` or by hand runs its linked tests from the `fm map` test map and surfaces failures on the band within the latency budget.

- **Borrow from other plugins safely (`fm borrow <url>`)** — FEATURE — value 3 — effort M — risk med — category: capability
  Why: the installer already detects competing plugins, and the user wants "more capable". wild: it reads a third-party plugin in a quarantined directory and lists what Foreman lacks and where it would conflict with its 14 hooks.
  Done when: given a plugin repo, it writes a gap and conflict report without executing the plugin's code, and each gap becomes a captured task.

- **Run intake and gray-zone judgments on a local small model** — PERFORMANCE — value 3 — effort L — risk high — category: local-first
  Why: intake classification and gray-zone guard calls cost tokens and a network round-trip, and the pack's lens is local-first. wild: assumption: the user's hardware can host a small model, and an opt-in setting enables it.
  Done when: with the setting on, classification of the last 200 captured messages matches the hosted classifier at ≥95% with no outbound call, and with it off nothing changes.

- **Retire stale allowlisted secrets** — SECURITY — value 2 — effort S — risk low — category: hygiene
  Why: T-0671 marked a `.env` fixture as an allowlisted secret. Allowlist entries have no reason or expiry, so they can outlive being fake.
  Done when: each allowlist entry needs a reason and a review date, and the scan fails when an entry is expired or no longer matches a fixture file.
