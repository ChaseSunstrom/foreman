# Brainstorm — lens: unspoken needs

- **Replace the 61-cell grid with a cell ledger that fills from probes** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: The user's steers demand real, non-templated cells, and the mission's 61 empty cells are the ask. The need behind it is that cells stop being prose someone can template. Assumption: a probe (a command whose output names a file or a recorded n/a with a reason) is the only unforgeable fill.
  Done when: `fm genesis sweep` reports 0 empty, 0 templated and 0 duplicated cells, and each cell row cites a probe command that re-runs and prints the same file or reason.

- **Show the lean cost of every capability on one line** — FEATURE — value 5 — effort M — risk low — category: lean
  Why: The pack shows hook p95 278 ms, 387k context per reply and a SessionStart note of ~2k chars × 89. The user never asked "what does Foreman cost me", but the lean ratchet exists because they care. A single `fm doctor` line, with the biggest contributor named, makes the cost visible.
  Done when: `fm doctor` prints one line with hook p95, context per reply, the top 3 injected sources by bytes, and the delta against the last generation.

- **Send the SessionStart note once, then only a hash and a delta** — PERFORMANCE — value 4 — effort S — risk low — category: context
  Why: ~2k chars repeated ×89 sessions is measured waste. Assumption: most sessions change nothing between starts.
  Done when: a second session start in an unchanged repo injects under 200 bytes, with a test comparing byte counts.

- **Fix the brief-guard path false positives and keep a corpus** — FIX — value 4 — effort S — risk low — category: guard
  Why: The pack says 2 brief-guard false positives read a dict key and a `.join(` call as written paths. Each false positive trains the user to bypass the guard, which is the unspoken risk.
  Done when: a corpus file holds both strings as allowed, with a red-first test, and the guard passes them while still blocking the paths it blocked before.

- **Make every guard block teach the safe command** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: `core:interpreter-code-driving-foreman` blocked 42× in 7 days. Repeated blocks mean the agent doesn't learn from the refusal. Assumption: each block class has one safe equivalent.
  Done when: each of the top 5 block classes returns its reason plus one runnable alternative, and the 7-day repeat count for those classes drops in `fm friction`.

- **Pay for each new verb with a deletion in the same task** — CLEAN — value 4 — effort M — risk med — category: lean
  Why: Gen-0 §6 says each generation must remove at least as much as it adds, and 28 "Later from T-07xx" bundles sit deferred. The user's unspoken need is that Foreman not become the thing it was built to restrain.
  Done when: `fm task finish` refuses a task that adds a verb with no retired verb, card or bundle named, and the refusal prints the three least-used candidates.

- **Move unused stack cards to a cold shelf** — CLEAN — value 3 — effort S — risk low — category: library
  Why: `fm lib stats` shows 5 of 1219 cards used, and the user already dropped card-writing for being unmeasured.
  Done when: cards unused for 90 days load from a cold index, a `fm lib show NAME` still finds them, and injected card bytes fall in `fm cost`.

- **Declare which surface is unguarded at session start** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: The grid spans Claude Code, Codex, Gemini, opencode, MCP, Desktop and headless, while T-0337 and T-0335 show hook gaps on some hosts. Assumption: a user running a hookless host believes the guard still applies.
  Done when: a session on a host without a deny hook prints "guard: advisory only, no hook on this host" in its first output, and a test covers each host in the parity matrix.

- **Scan the state directory for secrets and loose modes** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: Foreman stores logs, research packs and transcripts under `~/.claude/foreman/state`. Assumption: some contain pasted tokens, and the privacy-minded user would want to know without asking.
  Done when: `fm doctor` flags any state file with a secret-shaped string or a mode wider than 0600, with a fixture test for both.

- **Name the commit that made it heavier** — FEATURE — value 3 — effort M — risk low — category: lean
  Why: The lean ratchet reports growth only against the previous generation. When hook p95 or context grows, the user will ask "which change did this", and bisecting by hand is the unspoken chore.
  Done when: `fm lean --blame` prints the commit range and the commit where hook p95 or injected bytes first rose past the noise floor.

- **Wild: Run the exam with every optional hook off** — FEATURE — value 4 — effort L — risk med — category: lean
  Why: wild. The user wants to know what the weight earns. Assumption: a hooks-off arm on the same held-out scenarios isolates each hook's gain, so unearned ones can be cut with evidence.
  Done when: `fm exam scorecard` prints per-hook lift against the hooks-off arm, and names any hook with no measurable lift.

- **Wild: Prove "leaves no trace" with an install, eject and diff round trip** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. The user is cautious about bypass mode and a guard; a stranger on a fresh VPS will wonder what Foreman left behind. T-0794 already defers an eject.
  Done when: a test installs into a scratch home, ejects, and a recursive diff against the pristine copy shows no leftover file, hook or setting.

- **Wild: Plant a harmless forbidden command weekly to prove the guard is alive** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: wild. A guard that silently stopped firing after a host update looks the same as a guard that has nothing to block. Assumption: a canary can be run in a sandbox without side effects.
  Done when: a weekly job attempts a canary on each installed host, records block or pass, and `fm doctor` goes red naming the host where it was not blocked.

- **Wild: Show a weekly "what the guard stopped" note in plain words** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. The user trusts what they can see. The 42 blocks are invisible unless they read friction logs, so the value of the guard goes unfelt.
  Done when: a weekly note lists the top blocks, each in one sentence with the saved action, and it is readable from `fm digest` with no flags.

Next question: Which of the 61 empty cells would the user be unhappy to see marked n/a, and which would they accept with a recorded reason?
Next question: What does a hookless host (Codex, Gemini, opencode) actually cost the user in unguarded risk today, measured rather than assumed?
