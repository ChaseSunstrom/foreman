# Brainstorm — lens: simplicity

- **Give every guard block one rewrite hint** — FIX — value 5 — effort M — risk low — category: guard
  Why: most recent friction is guard false positives on Claude's own edit/probe commands, and each costs a rewrite. Today the block only says no. Have the guard reply with the one allowed form of the same action (for example "write via the Edit tool" or "use `fm --run`"), so the retry is one step, not a guess.
  Done when: a test feeds 10 known false-positive commands to the guard and each block message contains a concrete alternative command that the guard then allows.

- **Delete guard rules that have never fired for real** — CLEAN — value 4 — effort M — risk med — category: guard
  Why: the guard keeps gaining patterns (heredocs, backticks, `$'…'`, keywords, braces, versioned interpreters), and each new rule can produce false positives. Assumption: the ledger records which category blocked, and whether it was bypassed or retried.
  Done when: `fm guard stats` lists hits per category over the last N days, and a category with 0 true positives and at least 1 false positive is flagged for removal in the report.

- **Cut the always-on rules to what the gates can't enforce** — CLEAN — value 4 — effort S — risk low — category: rules
  Why: rules are about 5.7 KB loaded every turn, and the user is usage-sensitive. Every line that duplicates a gate or hook costs tokens in every session for no added safety.
  Done when: `plugin/rules/foreman.md` is under 3 KB, each remaining line is marked as not enforced by any hook, and `fm check` still passes 5/5.

- **Build the dashboard from one list of sections** — CLEAN — value 4 — effort M — risk low — category: mod UI
  Why: the user's complaints about mismatched AC/audits, unpanelled buttons, and a duplicate at the bottom of the chat all come from sections being drawn by separate code paths. Assumption: rows.tsx and register.tsx each build their own layout.
  Done when: the dashboard pane and the chat-bottom rendering come from the same section array, and a mod test fails if a section appears twice or has no panel border.

- **Replace the five audit lenses with a risk-picked pair** — FEATURE — value 3 — effort S — risk med — category: audits
  Why: parallel runs and subagent audits cost usage, and the user asked for no usage issues. A tier S task needs far less review than a security task. Assumption: audits currently run all lenses regardless of tier.
  Done when: an S-tier task runs at most 1 lens, an L-tier or SECURITY task runs 3 or more, and the audit log shows the chosen lenses and why.

- **Make `fm task finish` the only closing command** — CLEAN — value 3 — effort M — risk med — category: CLI
  Why: finish already commits, records evidence, and closes the task, but done/audit/commit steps still exist as separate commands the model must sequence. Fewer commands means fewer mis-sequenced calls.
  Done when: `fm help` lists `finish` as the single close path and the intermediate close commands are hidden or aliased to it, with the e2e roundtrip passing.

- **Merge the self-improvement trigger into task finish** — CLEAN — value 3 — effort S — risk low — category: self-improvement
  Why: the user wants recursive self-improvement, but it currently runs on two conditions (every 3 tasks and at least 2 h since the last pass). One rule reads better and is easier to debug. Assumption: the 2 h gap was added because passes started with nothing to read.
  Done when: one function decides "run a pass now" from friction volume alone, and a test shows no pass runs when the friction log is empty.

- **Wild: Add a "boring mode" that shows nothing unless blocked** — FEATURE — value 4 — effort M — risk low — category: UX
  Why: the user keeps asking for cleaner and quieter output, and many panels, bands, and hints compete. Boring mode would show only one line when Foreman needs something, and nothing otherwise. Assumption: panels remain for replies but dashboard, band, and hints go silent.
  Done when: with `fm mode boring`, a full task run prints no Foreman hints or bands, while a failed gate still produces exactly one visible line.

- **Wild: Run Foreman's own rules through a "would this line be missed" test** — CLEAN — value 3 — effort L — risk med — category: self-improvement
  Why: a subagent could replay recent sessions with each rule line removed and check whether the behaviour changed, so rules prove their value. Uses the RSI loop the user asked for, aimed at deleting things.
  Done when: a command outputs, per rule line, "changed behaviour in N of M replays", and lines scoring 0 are listed as candidates for deletion.

- **Wild: Add a "one-screen Foreman" that cannot grow past 20 lines** — FEATURE — value 3 — effort S — risk low — category: mod UI
  Why: the dashboard has header, task card, queue, inbox, gates, activity, subagents, and files, and it keeps growing alongside the user's complaints about looking weird. A hard line budget forces each section to compete for space.
  Done when: a mod test renders the dashboard with worst-case state and asserts at most 20 lines, with the least urgent sections collapsed first.
