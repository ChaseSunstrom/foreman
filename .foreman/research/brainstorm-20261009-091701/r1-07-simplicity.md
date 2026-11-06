# Brainstorm — lens: simplicity

- **Run a deletion pass as a first-class CLEAN gate** — FEATURE — value 5 — effort M — risk med — category: cleanup
  Why: the user steered "cleanup requests (repo, docs, briefs, dead code, replaced functionality) never got done"; T-0166 and T-0418 are CLEAN tasks sitting deferred or blocked.
  Done when: `fm task done` on a CLEAN task refuses without a deletion ledger (files and lines removed, plus a grep showing zero remaining references to the removed names), and a fixture task with no deletions is refused.

- **Prune unused surface from usage data** — FEATURE — value 5 — effort M — risk med — category: pruning
  Why: `fm usage` already reports skills, playbooks and commands never used. There are about 65 commands and 72 skill files, and nothing acts on that report.
  Done when: `fm prune` lists commands, skills and hooks unused for N sessions, each with its callers. `--apply` makes one removal branch per item, and it is gated by the bench and the doctor check.

- **Ratchet complexity in the release gate** — FEATURE — value 4 — effort S — risk low — category: release
  Why: Releases 1.2.13 to 1.2.16 came in a steady run, and each grew the guard and command surface (T-0414, T-0421, T-0422). Nothing makes growth pay for itself.
  Done when: the release task fails if the net count of commands, skills or guard rules rose without a `fm decide` entry that justifies it. A fixture release that adds a command without one fails.

- **Make every refusal carry its fix** — FIX — value 4 — effort M — risk low — category: guard UX
  Why: three separate user requests were the same bug: the `fm focus ...; sed` refusal (T-0404), "no active task" naming the task to resume (T-0409), and the refused `rm` of a symlink. Each refusal said what was wrong, not what to run.
  Done when: a test enumerates every refusal string in the hooks, and each contains a runnable `fm ...` command or one concrete rewrite. The test fails on a new bare refusal.

- **Collapse the command tree to about 25 verbs** — CLEAN — value 4 — effort M — risk med — category: command surface
  Why: the help lists 65 commands with heavy overlap: state/status, ideas/mission/landscape, second/audit, cost/usage/budget/digest, and session/claude/projects.
  Done when: grouped subcommands (`fm cost usage|budget|digest`) replace the old top-level names, which stay as aliases that warn for one release. Top-level help shows ≤30 entries, and the e2e roundtrip still passes.

- **Replace guard heuristics with an OS sandbox for the unknown cases** — SECURITY — value 5 — effort L — risk high — category: guard
  Why: the guard keeps growing special cases: `bash -lc`/`zsh -ic` clusters, python -c heredocs, script files (T-0275), symlinks, and brace writes. Each fix invites the next bypass. Assumption: bubblewrap or landlock is available on the supported platforms.
  Done when: commands the parser cannot classify run confined, with writes limited to the task's paths and the network off. The 5000-command replay shows no new allows, and at least one parser special case is deleted.

- **Cap the instruction tokens injected per session** — PERFORMANCE — value 4 — effort M — risk med — category: context cost
  Why: SessionStart injects context and the plugin has 72 skill files. `fm bench` and `fm evolve --drop` already exist to test whether an instruction earns its tokens. Assumption: the injected total is large and nobody tracks it.
  Done when: `fm doctor` reports injected tokens per hook and per skill. A configured ceiling fails the doctor check when exceeded, and one bench-verified removal brings the total below it.

- **Resume the one plausible task instead of refusing** — FEATURE — value 3 — effort S — risk med — category: flow
  Why: JARVIS edited between closing a lane task and refocusing T-0278 and was refused, and `fm focus X; edit` was refused twice. The user earlier dropped loosening the brief gate (YAGNI), so this applies only when exactly one task is paused or just-closed in that lane.
  Done when: an edit with no active task and exactly one resumable task focuses it and logs the event. With two or more candidates, the refusal still names them.

- **Run a nightly subtraction job** — FEATURE — value 4 — effort M — risk med — category: autonomy — wild
  Why: assumption: `fm night`, `fm evolve --drop` and the bench combine into "try removing one thing". Foreman only ever grows because nothing proposes deletions.
  Done when: a night run picks one instruction line, skill or dead function and removes it on a branch. It keeps the branch only if gates and bench are no worse, and it records the verdict in the morning digest.

- **Show only the next action in the statusline** — FEATURE — value 3 — effort S — risk low — category: UI — wild
  Why: assumption: the band and pane show more than a person reads. `fm next` already derives the single required action.
  Done when: a `minimal` UI profile renders one line, the next action, and expands only on a key press. A smoke screenshot shows one line at phone width.

- **Compile all rules into a one-page contract and load the rest on demand** — FEATURE — value 4 — effort L — risk high — category: instructions — wild
  Why: the 72 skill files plus hook text approach a mini-manual. The MCP server already exists to serve Foreman state to other agents. Assumption: retrieval at trigger time beats always-loaded text.
  Done when: a session starts with a generated contract of ≤1 page, and skills are fetched by MCP or recall when a trigger fires. Bench pass rate stays level, and tokens at session start drop by a measured amount.

- **Fold briefs, STATE, ledger and decisions into one append-only log** — CLEAN — value 3 — effort L — risk high — category: data model
  Why: `checkpoint` flushes into both the brief and STATE, `sync` mirrors three stores, and several bugs were about views drifting (the UI's current step stuck on 1/5, T-0406). Assumption: the stores overlap more than their readers need.
  Done when: STATE, the queue and the resume point are generated views of one event log. A migration reproduces the existing state byte-for-byte on a fixture project, and `fm docs` reports no drift.

- **Delete redundant tests found by replay** — CLEAN — value 2 — effort M — risk low — category: tests
  Why: there are 88 test files, and the gates include a 20-run hook benchmark. Slow gates already trigger a friction signal (T-0424).
  Done when: `fm tests prune` lists tests that never failed across bench replays and add no unique coverage, and removing them leaves the gate time lower with the same mapped coverage.
