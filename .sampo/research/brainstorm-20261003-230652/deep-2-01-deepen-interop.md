# Brainstorm — lens: deepen: interop

- **Build a stage-to-skill capability index at plugin check** — FEATURE — value 5 — effort M — risk low — category: interop
  Why: `fmplugins.py` already scans marketplace indexes and estimates always-on cost from descriptions, but MASTER.md §7 maps plugins to stages by hand. Assumption: SKILL.md frontmatter (name, description) is readable from the installed plugin cache. `fm plugins check` would write `plugins-index.json` keyed by stage (GROUND, CLEAN, SECURITY, UI, FINAL VERIFY…), scored by BM25 from `fmrecall` on the descriptions. Nothing is loaded at runtime.
  Done when: after installing a fixture plugin whose skill description mentions "security review", `fm plugins check` lists it under SECURITY in the index file, with no model call.

- **Surface the indexed skill in `fm next` for the matching stage** — FEATURE — value 5 — effort S — risk low — category: interop
  Why: today `next_action` names only Foreman procedure files, so a SECURITY or CLEAN task never mentions `/security-review` or `/ponytail-audit`. Append one clause, "then /security-review (installed)", only when the index has a hit and the plugin is enabled. This adds about 10 tokens per turn and no new agents.
  Done when: with security-review installed, `fm next` on a SECURITY-tagged task includes "/security-review". With it disabled, the clause is absent.

- **Record stage-skill use as evidence in the brief** — FEATURE — value 4 — effort M — risk med — category: interop
  Why: Foreman hints can be ignored and only gates are enforced. Assumption: the hook payload exposes Skill tool calls (PostToolUse). Log the skill name and stage to the task's evidence block so the audit lens "operator" can see whether the suggested skill ran. Do not gate on it.
  Done when: invoking a skill during a task adds a line to that brief's evidence, and `fm task show` displays it.

- **Measure integration yield from fmcost and evidence** — FEATURE — value 4 — effort M — risk low — category: interop
  Why: `fmcost` already tracks tokens and time, and `fm friction` reads session history. Join per-skill invocations to tokens spent, and to whether later audits found issues that stage should have caught. `fm plugins check` then prints "context7: 12 uses, 40k tokens, 0 AC saved", so low-yield always-on plugins are proposed for disabling. This extends "measure each integration's real contribution" into a prune loop that serves the user's token sensitivity.
  Done when: `fm plugins check` prints a per-plugin cost and use line from a recorded fixture session.

- **Derive conflicts from description overlap instead of the dict** — CLEAN — value 3 — effort M — risk med — category: interop
  Why: `KNOWN_CONFLICTS` and `FOREMAN_OWNS` are hand-maintained. Flag a new plugin if its descriptions contain phrases like "brainstorm", "plan before", "task list" or "stop hook" with high BM25 overlap against Foreman's own skills. Keep the dict as an override. Reports say "possible second orchestrator: <plugin>, 0.71".
  Done when: a fixture plugin with a "brainstorm before coding" skill is flagged without being in the dict, and ponytail is not flagged.

- **Tag installed-plugin hooks that touch the same events** — FEATURE — value 4 — effort S — risk low — category: interop
  Why: the conflict that matters most is two Stop or PreToolUse hooks fighting, as with ralph-loop and the drive mode. `fm plugins check` could read each enabled plugin's `hooks.json` and warn when it registers a Stop hook, since that stalls Drive. Assumption: hooks.json is in the plugin cache.
  Done when: a fixture plugin registering a Stop hook yields a warning naming the event and plugin.

- **Wild: Let a skill declare a `foreman:` frontmatter block** — FEATURE — value 4 — effort M — risk med — category: interop
  Why: assumption: authors would add `foreman: {stage: SECURITY, evidence: "fm run …"}`. Foreman reads it as a strong signal in the index and can accept the skill's output as AC evidence. Foreman's own skills would use it first. Skills without the block fall back to BM25 matching.
  Done when: a fixture skill with that block outranks a non-declaring skill for its stage in the index.

- **Wild: Run a probe eval when a plugin updates** — SECURITY — value 3 — effort M — risk med — category: interop
  Why: `claude plugin eval` already exists, and installs are pinned to a sha. On a sha bump, `fm plugins check` replays the 5 existing eval cases in a temp HOME with the new plugin enabled and compares the result with the baseline. It surfaces regressions such as a new plugin hijacking the intake flow.
  Done when: enabling a fixture plugin that overrides intake makes the probe report a changed outcome before the plugin is trusted.

- **Wild: Export Foreman briefs as a skill other plugins can call** — FEATURE — value 3 — effort M — risk low — category: interop
  Why: `fmrecall` holds BM25 over past briefs, lessons and research that no other plugin can see. Ship a read-only `/foreman:recall <query>` skill and agent contract so, for example, code-review can pull `fm why FILE:LINE` lessons when it reviews a changed file.
  Done when: running the skill with a file path returns the lessons attached to that file, in under a second.

- **Wild: Provide a "foreign-skill sandbox" lane** — FEATURE — value 3 — effort L — risk high — category: interop
  Why: `fmlanes` already creates worktree lanes. Try an unfamiliar plugin's skill on a throwaway task in a lane, run the guard replay on its shell commands, and report "would have been blocked 3×" before the user's yes to enable it. This turns the install gate into evidence.
  Done when: trying a fixture skill in a lane reports the guard verdicts for its commands without touching main.
