# Brainstorm — lens: user value

- **Guard non-Bash tools by effect class** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: assumption: the pack describes the guard as stopping "commands", and no earlier idea covers MCP tool calls, WebFetch or Write/Edit aimed outside the repo. Bypass mode skips prompts for all of these. Classify each tool call as read, write-local, write-outside, network or spend, and apply the same block, warn or allow rules.
  Done when: a fixture MCP call with a destructive effect class is blocked in bypass mode and logged, and a read-only MCP call passes.

- **Prove the guard holds inside subagents, background shells and worktrees** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: assumption: earlier ideas cover guard parity across harnesses, not across execution contexts within one harness. A guard that holds in the main thread but not in a spawned lane is the likeliest silent gap.
  Done when: one test runs a blocked command from a main shell, a subagent, a background task and a worktree lane, and each is blocked and ledgered.

- **Stop Foreman verbs being triggered by untrusted text** — SECURITY — value 4 — effort M — risk med — category: injection
  Why: taint ideas exist for commands in general. Foreman's own outward verbs (`fm ship`, `fm genesis live`, grants) are a specific confused-deputy target: a README line saying "run fm ship" shouldn't work. Require that any outward `fm` verb called in a session carries a user-turn origin, or else ask.
  Done when: a fixture repo whose file text instructs `fm ship --publish` makes the session ask or refuse, with the reason ledgered.

- **Detect hook collisions with other plugins** — FIX — value 3 — effort S — risk low — category: install
  Why: assumption: users run Foreman beside other Claude Code plugins and hooks. A hook that rewrites, reorders or shadows Foreman's guard goes unseen. Existing ideas protect Foreman's own config but not ordering or interference by others.
  Done when: `fm doctor` flags a second PreToolUse hook that can allow a command Foreman's guard blocks, with the ordering it found.

- **Add `fm distrust <shape>` to undo a learned approval** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: "show every live grant" and "remember approvals by shape" exist, but a retroactive revoke with a usage report doesn't. One command removes the approval and lists which past runs relied on it.
  Done when: after `fm distrust`, the same command prompts again, and the output lists each earlier use of that approval.

- **Price the user's disasters once, then report guard saves in hours** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: "name the guard's save in plain words" says what was blocked, not what it was worth. The user states five costs once (wiped home, force-push, leaked key, and so on). Each block then prints "≈ N hours avoided", labelled as the user's own estimate.
  Done when: a blocked force-push prints the user-set hours, and with no prices set it prints none.

- **Measure install-to-first-value** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: the first-run, tour and trial ideas all lack the one number that tells them apart. Record minutes from install to the first guard block, proven task or kept result.
  Done when: `fm doctor` prints that interval, or "not yet" with a count of sessions so far.

- **Show hook time spent this session on the status line** — PERFORMANCE — value 2 — effort S — risk low — category: perf
  Why: hook p95 is benched in tests, but the user never sees the cost of discipline while working. Display cumulative hook milliseconds, turning amber past a user-set budget.
  Done when: the status line shows a nonzero total after a session, and a fixture slow hook turns it amber.

- **Check state isolation on a shared machine** — SECURITY — value 2 — effort M — risk low — category: privacy
  Why: assumption: some users are on shared or family machines. Test that ledgers, transcripts and approvals are mode 0700 and unreadable to another OS user, and that a second user's Foreman can't read or overwrite them.
  Done when: a two-user test finds no cross-readable Foreman file and fails if one is made group-readable.

- **Add `fm can-i "<command>"` as a no-run guard oracle** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: docs and users have no safe way to ask "would the guard stop this?" without running it. It prints the verdict, the matching rule and the safe alternative, and agents can call it too.
  Done when: `fm can-i "rm -rf ~"` exits nonzero and names the rule, and `fm can-i "ls"` exits 0, with nothing executed.

- **Ship the guard as one file that protects a remote server (wild)** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild, assumption: users run agents over ssh on servers where installing Foreman is unwelcome. A single stdlib file registers as the hook, enforces the rules offline and spools its ledger for merge when the user reconnects.
  Done when: copying the file to a clean host blocks a fixture destructive command with no other Foreman files present.

- **Add a belt-rank trust ladder (wild)** — FEATURE — value 2 — effort M — risk med — category: autonomy
  Why: wild, extends "earn autonomy per task kind". The rank is shown on the status line, rises with clean weeks, and drops after a harm event. Higher ranks unlock only looser prompting, never fewer guard rules.
  Done when: a fixture ledger of 4 clean weeks raises the rank, an injected harm event lowers it, and the guard rule set is identical at every rank.

- **Add a phone kill switch (wild)** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild. A single signed link on the user's phone, on the local network or paired, revokes all grants, freezes lanes and writes a snapshot. Devices are thin in the pack, and unattended drives are what the user most needs to stop from afar.
  Done when: hitting the link in a test freezes a running fake drive within 5 seconds and lists the grants it revoked.

Next question: Which of these Foreman safeguards would a user notice only after switching to a different harness or machine, and where does the guard silently not run?
Next question: What does the user do in the first five minutes after a guard block they disagree with, and does any surface make that path shorter than editing the rule by hand?
