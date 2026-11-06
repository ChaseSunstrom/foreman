# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Rule-of-three before any plugin gets built** — FEATURE — value 4 — effort S — risk low — category: acquisition
  Why: the tree already holds 1,396 skills and the user's steers keep asking for leanness; a throwaway one-shot script is often enough, and every promoted tool adds context tax. Assumption: no promotion threshold exists today.
  Done when: `sampo plugins build` refuses to promote a script until the ledger shows three distinct tasks that used it, and prints the count.

- **Run a bare-host search before every `plugins find`** — FEATURE — value 4 — effort M — risk low — category: acquisition
  Why: the host keeps adding its own marketplace, MCP registry and skill search. Sampo's finder should first try the host's native search, and a log of the cases where the native one won shows when its own finder can retire.
  Done when: a find run records `native_hit` or `native_miss` per query, and `sampo doctor` shows the 30-day native hit rate.

- **Keep a counterfactual receipt for each acquired tool** — FEATURE — value 5 — effort M — risk med — category: outcomes
  Why: nothing in the pack shows whether an installed tool changed a task's outcome. Each tool should record the task it unblocked and whether a bare re-run (with no tool, in a lane) still passes.
  Done when: every tool row has `unblocked_task` and `bare_rerun: pass|fail`, and a tool whose bare re-run passes is flagged "not needed".

- **Retire a small-model card when the model passes bare** — FEATURE — value 5 — effort M — risk low — category: small models
  Why: the steer is thousands of cards for qwen 4B to 27B, but model weights improve and cards then become dead context. Assumption: Louhi's Smith-on-local-model exam (T-2908) can run an arm with and without a card.
  Done when: `sampo cards audit --model M` marks cards whose with/without delta is ≤0 over N scenarios as "retire candidate", and a retired card moves to a tombstone and is not injected.

- **Put a retire-when predicate in every built tool's manifest** — FEATURE — value 4 — effort S — risk low — category: lifecycle
  Why: the open question about the host adding features that overlap a verb applies to built tools too. A predicate such as "host has native X" or "bare 27B passes exam E" can be checked by doctor.
  Done when: building a tool without a `retire_when` field fails its test, and `sampo doctor` lists the tools whose predicate now holds.

- **Expire queued install grants whose need has gone** — FIX — value 3 — effort S — risk low — category: grants
  Why: the mission says install grants are queued, and queued asks go stale (the "Missing tool shellcheck" item was dropped because the premise changed). Stale grants make the user answer things that no longer matter.
  Done when: each queued grant re-checks its blocking task at pick time, and one whose task closed or whose need is met is auto-dropped with a one-line reason.

- **Prefer stdlib-only fallbacks for a missing tool** — FEATURE — value 4 — effort M — risk low — category: acquisition
  Why: the standing rule is "no software installs", and shellcheck was dropped for it. A tool a small stdlib script can replace should never need a grant.
  Done when: for a missing tool, the build path first tries a stdlib script plus test, and an install grant is queued only when that fails with a recorded reason.

- **Wild: let the small model impersonate the missing tool first** — FEATURE — value 3 — effort M — risk med — category: acquisition
  Why: assumption: if a local model can reproduce a linter's output on 20 sampled files with ≥90% agreement against the real one, the tool is not worth acquiring for that model's work.
  Done when: `sampo plugins emulate TOOL` prints an agreement score over sampled files, and the build or install decision cites it.

- **Wild: add "which existing tool does this replace?" to every acquisition** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the pack's `plugin/skills/` is already the largest directory. Acquisition that must name a removal makes the net tool count flat or falling.
  Done when: an acquisition record has `replaces: <tool>|none` with a reason for `none`, and the report shows the net count per generation.

- **Wild: run a monthly "host catch-up" scan of the acquired set** — FEATURE — value 3 — effort M — risk low — category: obsolescence
  Why: a cold child reads host release notes and the tool manifests and lists acquired tools the host now covers natively. The earlier ideas cover verbs; this covers the acquired tools, with a draft removal PR for each.
  Done when: the scan outputs a table of tool, host feature and confidence, and for a hit it files a removal task with the retire-when evidence.

- **Make acquired tools a harness-neutral spec with thin per-host adapters** — CLEAN — value 4 — effort L — risk med — category: portability
  Why: the pack says Sampo works on Codex, Gemini CLI and opencode, but plugin and MCP install code is host-specific and risks lock-in. A declarative tool spec (command, schema, test) keeps the tools alive if the main host changes.
  Done when: one built tool installs on two hosts from the same spec file, with each host's adapter under 50 lines.

- **Score tool acquisition as its own exam arm against "just write the script inline"** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the mission says the not-yet items wait on an exam arm against the path they replace, and #5 itself has no such arm.
  Done when: `sampo exam` has a scenario kind where the tool is missing and arms are acquire / inline script / give up, and the scorecard prints which arm wins.

- **Charge descriptions of acquired skills against a context budget** — PERFORMANCE — value 3 — effort S — risk low — category: lean
  Why: every acquired skill adds frontmatter text to the session, and the earlier ideas budget skill descriptions only generally. An acquisition that pushes the total past the budget must displace the least-used one.
  Done when: the acquisition step prints the character delta and fails when the skill-description total exceeds the budget file.

Next question: if a stranger's host already has a marketplace, MCP registry and a good model, what is the first acquisition Sampo would still do better than them, and is it measured?
Next question: which acquired tool has the user actually re-used after the task that caused it, and does the ledger show that?
