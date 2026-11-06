# Brainstorm — lens: grid

**Cells covered**
- Surfaces: drive and hooks, CLI (`fm`/`sampo`), web UI, pane and status line, Smith TUI, phone push.
- Actors: user, agent, other agents, unattended run.
- Failure modes: missing, wrong, slow, unsafe, unclear.

**Cells left empty**
- Site × any actor: the site only displays Genesis data, so triggers don't touch it.
- Smith TUI × other agents: no evidence anyone drives Smith that way.
- Phone × slow: push latency is outside Sampo's control.

- **Re-verify an event's commit before a CI-red run starts** — FIX — value 4 — effort S — risk low — category: triggers
  Cell: unattended × wrong. Why: the request names CI watchers, and a red run on a commit that has since been fixed or force-pushed would start a pointless overnight session. Done when: a replayed fixture of a red SHA that is no longer the branch tip is dropped with the reason `superseded`, and no task is filed.

- **Scrub the environment of trigger-born sessions to the trigger's declared grants** — SECURITY — value 5 — effort M — risk med — category: security
  Cell: unattended × unsafe. Why: unattended runs inherit the user's full environment, including tokens, and the failed-call rise suggests nobody has audited what they hold. Done when: a trigger declaring only `repo:read` starts a session where `env` shows no other token variables, and a test asserts that.

- **Hold a sleep inhibitor for the duration of a triggered run** — FIX — value 4 — effort S — risk low — category: reliability
  Cell: unattended × missing. Why: assumption: laptop suspend is what makes "overnight progress" stop; the drive-stop gap is unexplained. Done when: a 10-minute triggered run on a machine set to suspend after 1 minute finishes without suspending, and the inhibitor is released at exit.

- **Show the next five fire times on save of any schedule** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Cell: user × unclear. Why: schedules are new, and a typo in a cron expression only shows itself a day late. Done when: `sampo trigger add` prints five local-time fire times, and a fixture crossing a DST change shows the correct offsets.

- **Claim each trigger event with an exclusive, TTL'd lock across harnesses** — FIX — value 4 — effort M — risk med — category: multi-agent
  Cell: other agents × wrong. Why: Claude, Codex and a Smith lane may all be armed on one repo, and two of them picking the same CI-red event would produce conflicting fixes. Done when: two processes racing on one event yield one run and one logged `claimed-by-other` line, and a killed claimant's lock expires.

- **Require a web-UI trigger edit to be same-origin, token-bound and shown as a diff** — SECURITY — value 4 — effort M — risk med — category: security
  Cell: web UI × unsafe. Why: a trigger is a command that runs unattended, so any page that can write one is an execution path, and the web UI is the new editing surface. Done when: a cross-origin POST to the trigger endpoint is refused, and a same-origin edit shows a before/after diff and needs a click.

- **Measure event-to-first-tool-call latency per trigger kind** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Cell: drive × slow. Why: a bench exists for hooks but not for "how long before triggered work starts", which is what the unattended user will feel. Done when: `sampo doctor` prints p50/p95 start latency for file, schedule and CI triggers from the trigger ledger.

- **Show next-fire and last-result as one status-line glyph** — FEATURE — value 3 — effort S — risk low — category: ui
  Cell: pane × unclear. Why: the user can't tell whether anything is armed without running a verb. Done when: the status line shows, for example, `⏲ 02:00 ✓` and turns hatched when the last run failed or the scheduler is not running.

- **Give each trigger kind a warm-start capsule so triggered sessions don't re-read the map** — PERFORMANCE — value 3 — effort M — risk med — category: performance
  Cell: agent × slow. Why: the pack's lean numbers (75,758 tokens at start, 2.4 GB of state) show cold starts are expensive, and a trigger fires the same few shapes repeatedly. Done when: a CI-red session's first prompt is at most 1,500 characters of capsule, and the run passes the same exam as a cold start.

- **Wild: Fire a task when a dated `TODO(2026-12-01)` comment expires** — FEATURE — value 3 — effort S — risk low — category: triggers
  Cell: unattended × missing. Why: wild: repos already hold promises to themselves that nothing watches, and this uses the file-trigger machinery for them. Done when: a fixture file with a past-dated TODO files exactly one task, once, citing `file:line`.

- **Wild: Treat the user's calendar file as the "don't touch the GPU now" signal** — FEATURE — value 3 — effort M — risk low — category: local-first
  Cell: user × wrong (the machine is busy when they need it). Why: wild: local models for unlimited background volume collide with the user's own use, and a local ICS file needs no network. Done when: with a busy event in the file, queued local-model triggers wait, and a log line names the event title.

- **Wild: Run a nightly synthetic end-to-end trigger that touches a scratch file, files a task, and closes it** — FEATURE — value 4 — effort M — risk low — category: reliability
  Cell: unattended × unclear. Why: wild: it proves the whole chain works before the user sleeps; the drive stops and failed calls suggest silent breakage. Done when: breaking any link (watcher, filing, drive pickup) makes the morning card say which link failed, within the same night.

- **Wild: Let a file untouched for 90 days with no test fire a "characterise this" task on the local model** — FEATURE — value 2 — effort M — risk med — category: local volume
  Cell: unattended × missing. Why: wild: the user wants unlimited local volume used on something useful, and untested old files are never anyone's priority. Done when: the task produces a characterisation test that passes on the unchanged file, in a scratch worktree, and is held for review.

- **Cap trigger-born output to a quote-only summary for the user's phone push** — FEATURE — value 2 — effort S — risk low — category: devices
  Cell: phone × unclear. Why: assumption: a push that contains model prose is unreadable and can leak repo text. Done when: the push is at most 140 characters, built from ledger fields only, and contains no model-written text.

Next question: Which trigger kinds does the user actually want to arm first, and what does each one do with a failure (retry, park, or page)?
Next question: When two armed triggers contradict (a schedule says run, a file watcher says the tree is dirty), which wins, and is that written anywhere a session can read?
