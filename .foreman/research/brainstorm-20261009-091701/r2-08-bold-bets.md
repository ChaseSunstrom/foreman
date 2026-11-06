# Brainstorm — lens: bold bets

- **Capture contradictions at intake** — FEATURE — value 4 — effort M — risk low — category: intent
  Why: the pack shows decisions, vetoes, and a steer ("cleanup never got done") held in separate stores. Nothing checks a new request against them. Assumption: decisions.md and vetoes are structured enough to match against.
  Done when: capturing "add a fallback cache" after a decision "no caches, YAGNI" prints the conflicting decision id and asks keep, supersede, or drop before the brief is created.

- **Record a hypothesis ledger for FIX tasks** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: FIX is the most common type, but evidence is just "a command passed". Assumption: no per-hypothesis tracking exists today. The ledger would hold hypothesis, experiment, and result, with a reproduction artifact required before any edit and a note on why the winning hypothesis beat the others.
  Done when: `fm task done` on a FIX is refused without a reproduction that fails before the change and passes after. The brief lists at least one rejected hypothesis, or says explicitly "none".

- **Analyse escapes and propose the missing gate** — FEATURE — value 5 — effort M — risk med — category: learning
  Why: Foreman has gates and sentinels, but the pack shows no link from a later bug back to the earlier "done" task that should have caught it. JARVIS relays (step band stuck, lane merge refused, tool caches) are such escapes. Assumption: later briefs can be linked to earlier tasks through `fm why` and shared files.
  Done when: a FIX touching files from a closed task produces an escape record naming that task and the gate tier that missed it, plus a proposed gate. Accepting it adds the check to `fm gates` for that type.

- **Capture behaviour before and after each task** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: `fm smoke` checks the product after the fact, and "behaviour preservation for CLEAN" is a single-type idea. This generalises it. Before the first edit, Foreman records characterization output (CLI output, HTTP responses, screenshots, exit codes) for the touched surface. At done it diffs the recording and flags changes outside the brief's scope. Assumption: surfaces can be recorded generically.
  Done when: a task that silently changes a CLI's `--help` text outside its scope fails done with a unified behavioural diff, and an in-scope change passes.

- **Verify evidence in CI for any agent's PR** — FEATURE — value 4 — effort M — risk low — category: ecosystem
  Why: `fm pr` and `fm export` exist, but only inside Foreman. A GitHub Action could re-run the evidence commands in a clean checkout and comment pass or fail on PRs from any agent or human. Assumption: evidence records carry runnable commands plus an environment fingerprint.
  Done when: the Action runs on a sample PR and posts a table of criteria, commands, and reproduced results. A PR with fabricated evidence is flagged red.

- **Compile repeated procedures into tested playbook skills** — FEATURE — value 4 — effort L — risk med — category: self-extension
  Why: `fm repeats` only reports what a repeated procedure could become, and builders redo the same shell sequences (lane rm cleanup, release steps). Foreman could write the skill or MCP tool itself, with a test, in a lane, and retire the manual path. Assumption: repeats data identifies stable argument patterns.
  Done when: after N repeats of a sequence, a lane produces a skill plus a passing test, and `fm usage` shows later runs using it instead of raw commands.

- **Govern infrastructure and data changes with plan, apply, rollback** — FEATURE — value 4 — effort L — risk high — category: task types
  Why: the task types are FIX, FEATURE, CLEAN, and so on, all code-shaped. Real users also change terraform, migrations, and configs. A new task type would require a dry-run diff, an approval, an apply, and a proven rollback before done. Assumption: the user runs such work.
  Done when: a migration task can't reach done without a recorded plan output, an approval, and a rollback command whose run is in the evidence.

- **Onboard a legacy repo with a safety crawl** — FEATURE — value 4 — effort L — risk med — category: adoption
  Why: `fm init` registers a project but builds no safety net, and `fm map` is shallow. A crawl would generate characterization tests, a risk heatmap from churn and coverage, and a first-week queue of safe cleanups. Assumption: new projects with weak tests are a growth path.
  Done when: running it on an untested repo yields a passing characterization suite, a ranked risk list, and at least 5 queued briefs with gates.

- **Make Foreman's own evidence reproducible years later** — FEATURE — value 3 — effort M — risk low — category: evidence
  Why: evidence is recorded as output text, and gates drift as dependencies change. Pin toolchain versions and lockfile hashes in each evidence record, and re-run on demand ("does task X still hold at HEAD, or did the world change?"). `fm sentinel` is the nearest neighbour but doesn't separate code regressions from environment drift.
  Done when: `fm sentinel --explain` labels each failure as code-changed or environment-changed.

- **Wild: Earn autonomy licences per model and task type** — FEATURE — value 4 — effort L — risk med — category: autonomy
  Why: the pack has `fm autonomy` as a global standard/full switch, and `fm bench` can replay finished tasks. Every new model or Claude Code version would sit an exam from the bench, and the pass rate on each type would set what it may do unattended. Assumption: enough finished tasks exist to form meaningful exams. wild
  Done when: switching to an unlicensed model type drops `fm run` to ask-mode for that type, and a passing bench run lifts it with the score shown.

- **Wild: Run a constitution interview** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: the pack shows Foreman inferring taste from steers after the fact, as with "budget limits shouldn't block until 75%". A short upfront interview with concrete dilemmas ("slower and safer, or faster and riskier?") would write vetoes, autonomy defaults, and thresholds in one pass, and re-run quarterly as a diff against observed behaviour. wild
  Done when: the interview writes vetoes and settings, and a later `fm taste` shows stated versus revealed preferences side by side.

- **Wild: Keep a behaviour time machine** — FEATURE — value 3 — effort L — risk med — category: history
  Why: this extends the behaviour-capture idea above. Keep the per-task recordings in a content-addressed store, so the question "when did this screen or output change, and under which task?" becomes a bisect over recorded behaviour rather than over commits. Assumption: recordings are small after deduplication. wild
  Done when: `fm why --behaviour <surface>` names the first task whose recording differs, with before and after attached.

- **Hand a task to a human with a packet** — FEATURE — value 3 — effort M — risk low — category: collaboration
  Why: the pack covers fleets of machines and agents, but not teammates. A handoff would export the brief, the resume point, the evidence so far, the vetoes that apply, and the open questions as a single page or PR draft. Importing it on another person's Foreman would continue the task at the exact step. Assumption: users sometimes work with others.
  Done when: exporting a half-done task and importing it in a fresh project directory resumes at the same step with the evidence intact.
