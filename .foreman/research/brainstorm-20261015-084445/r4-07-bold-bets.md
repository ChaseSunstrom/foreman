# Brainstorm — lens: bold bets

The pack's idea list is close to saturated, so most of these are bold bets that combine existing fragments into one shippable thing, plus a few real gaps (A2A, editor sidebar, merge-queue check). Where an idea overlaps an earlier one, I say which pieces it joins.

- **Ship Foreman Core 2.0 as a zero-wiring marketplace plugin with a ten-verb front door** — FEATURE — value 5 — effort L — risk med — category: distribution
  Why: Evidence B/A: every popular rival installs with one marketplace command and doesn't rewrite `~/.claude`, while Foreman's install sets bypass, deny rules and an output style, and `fm` isn't on PATH. Joins the earlier Seed, ten-verb help, safe-install and PATH ideas into one release.
  Done when: in a clean HOME, `/plugin install` plus `fm hello` works, `settings.json` is byte-identical before and after, and `fm help` lists at most 10 verbs.

- **Add `fm leave 8h`, one verb for the safe overnight queue** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: assumption: the user's "keep going… recursively" habit means they want to walk away. It joins the existing charter, canary, dead-man heartbeat, learned allowlist and return-card ideas behind a single entry point with a hard budget and stop rule.
  Done when: one command in a fixture repo prints a charter (scope, budget, allowed commands, push channel), runs two queued tasks, and ends with a single return card with receipts; killing the session mid-run produces a flagged "died at step N" card.

- **Ship a first-run wizard in the web UI** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the surface is the web UI, yet the newcomer walkthrough (A1–A10) happens entirely in a terminal full of jargon. `fm serve` opens a localhost page that previews each `~/.claude` change as a toggleable diff, runs the no-model demo, and shows `fm doctor` in plain words.
  Done when: declining one install toggle in the wizard leaves that setting untouched on disk, and the page works with no network.

- **Expose verify-as-a-service over A2A and MCP** — FEATURE — value 4 — effort M — risk med — category: interop
  Why: B shows superpowers (about 300k stars), claude-flow and BMAD orchestrate but don't verify. A `verify(brief, diff)` endpoint that returns a receipt makes Foreman the referee layer beneath them instead of a rival. Earlier ideas covered MCP state and gates, not an agent-protocol endpoint other orchestrators can call.
  Done when: a stub A2A client submits a brief and diff and gets back a pass/fail receipt with an evidence hash, and a deliberately vacuous verify command is rejected.

- **Add a thin editor sidebar for VS Code, Cursor and Windsurf** — FEATURE — value 4 — effort M — risk low — category: devices
  Why: B notes Task Master reaches Cursor and Windsurf users, and Foreman has no editor surface. The sidebar is a pure renderer of `fm state --json` (queue, step, open criteria) with click-to-open on `file:line`.
  Done when: the extension lists the active task and criteria from a fixture state, and clicking an evidence path opens that file in the editor.

- **Publish `foreman/evidence` as a GitHub required status check** — SECURITY — value 4 — effort M — risk med — category: trust
  Why: assumption: teams that adopt Foreman want branch protection to enforce it. The check passes only if the PR's proof pack hash matches the PR head's tree hash, so stale or forged "done" can't merge. This is distinct from the earlier PR-comment and Action ideas.
  Done when: a PR with a proof pack from an older tree shows the check red, and re-running on the new tree turns it green.

- **Rank every hot-path hook by cost against catches and show the table in `fm doctor`** — PERFORMANCE — value 3 — effort M — risk low — category: footprint
  Why: C/D show 108 verbs of which 46 are unused, 28k lines, rules loaded every session, and hook latency as a repeated worry. This joins the per-gate cost-per-catch and hook-time ledger ideas into one start-up table that names the cheapest deletions.
  Done when: `fm doctor --cost` prints each hook's median ms, injected bytes and decisions in the last 30 days, sorted by cost per decision.

- **Make `fm release-check` one command that runs every newcomer and fault gate** — CLEAN — value 4 — effort M — risk low — category: developer experience
  Why: A8 shows a fresh install fails its own doctor, and rounds 2–3 went dry because gates are scattered. It combines the clean-HOME walkthrough, seeded-bug fixture, hostile-repo drill and install/uninstall byte round trip into a single release gate.
  Done when: the command fails on a deliberately broken installer and passes on main, with one summary line per gate.

- **Wild: add Referee mode, a read-only live grader for any Claude Code session** — FEATURE — value 3 — effort L — risk med — category: observability — wild
  Why: assumption: the 0/3 bench cases and "no published evidence" mean Foreman has no outside comparison data. Referee tails a session transcript, with or without Foreman, and scores each "done" claim against git and test output. That yields the data for a rival comparison table.
  Done when: pointed at a recorded rival-plugin transcript, it prints claims checked, claims unsupported and an evidence-ratio line.

- **Wild: add a commute briefing with spoken return card and voice yes/no** — FEATURE — value 3 — effort M — risk med — category: devices — wild
  Why: assumption: a phone or car is where "needs you" moments land. A local text-to-speech read of the return card, plus a phone shortcut that answers a pending `fm ask` by voice, bound to the ask id.
  Done when: a pending ask with a default is answered through the shortcut and the task resumes, and a stale ask id is refused.

- **Wild: add `fm autopsy-me`, naming the user's three costliest habits from their own transcripts** — FEATURE — value 4 — effort M — risk low — category: user value — wild
  Why: A1 shows newcomers can't see what Foreman does for them. At install it reads the last 30 days of local transcripts, never sends them anywhere, and names three habits (such as re-running the whole suite, or re-reading unchanged files) with counted examples and the one setting that helps.
  Done when: on a fixture transcript set it prints three habits, each with a count and an example line, and makes no network call.
