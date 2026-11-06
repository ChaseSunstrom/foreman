# Brainstorm — lens: user value

- **Run metric-climbing campaigns** — FEATURE — value 5 — effort L — risk med — category: autonomy
  Why: the pack shows task-shaped work only (fix, build, verify). Perf evidence exists, but nothing takes "get X under Y" and iterates. Assumption: the user has goals like latency, bundle size, flake rate or token cost.
  Done when: `fm climb "<cmd that prints a number>" --target N --budget 2h` runs lane attempts, keeps only changes where the gate stays green and the metric improves, and writes a ledger table of kept and rejected attempts.

- **Gate LLM-powered products with rubric evals** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: assumption: JARVIS is an LLM assistant, so `fm smoke` and unit gates can't catch a prompt or model regression. "Check the product the way its user uses it" stops at web UIs.
  Done when: golden conversations in `evals/` are sampled N times per run, scored by a rubric (code checks first, judge model second), and `fm check` fails when the pass rate drops below a recorded baseline.

- **Answer side questions from a read-only lane** — FEATURE — value 5 — effort M — risk low — category: focus
  Why: Foreman guards focus and captures new requests rather than chasing them. A question like "how does lane merge decide overlap?" should not become a task or derail the active step. Assumption: users currently wait or break focus to ask.
  Done when: `fm ask-repo "<question>"` or an `?`-prefixed prompt gets an answer with `file:line` citations from a forked read-only subagent. The active task, step and ledger are unchanged afterwards.

- **Route one message to the right lane** — FEATURE — value 4 — effort M — risk med — category: multi-lane
  Why: the JARVIS complaints (T-0278 against T-0280, a focus command mixed into a compound line) come from one human talking to several concurrent contexts. Assumption: users now type corrections into the main thread that concern a lane.
  Done when: a correction mentioning a lane's task or files is delivered to that lane's brief as a steer. An ambiguous message prompts a single-choice pick, and the ledger records where it went.

- **Ground FIX evidence in runtime traces** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: the pack's FIX flow records evidence, but a root cause is only the model's claim. Assumption: py-spy, strace, a debugger or tracing hooks exist on the host.
  Done when: a FIX brief can attach a captured trace (stack sample, syscall log, or watchpoint hit). The done-gate for a FIX requires either a trace line naming the cited cause or an explicit "not traceable" note.

- **Draft upstream bug reports from harness quirks** — FEATURE — value 4 — effort M — risk low — category: ecosystem
  Why: T-0337 (Gemini AfterAgent deny discards the answer), the bash -lc miss and the blocked adapter tasks are harness bugs. Foreman has an inbound pipe for Claude Code releases but none outbound.
  Done when: `fm upstream T-xxxx` writes a minimal standalone repro, versions, expected vs observed, and a redacted draft issue to a file. It sends nothing without an explicit user confirmation.

- **Carry the user's identity to any machine or project** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: vetoes, taste, standing yeses, autonomy and lessons are per-user value that a new machine or a new project (the JARVIS pattern) loses. Existing share and fleet ideas cover lessons and compute, not identity.
  Done when: `fm carry export` produces an encrypted bundle and `fm carry import` on a clean install restores vetoes, standing yeses, taste and settings. Secrets are excluded, and `fm doctor` confirms the result.

- **Show a demo transcript before building a FEATURE** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: the user rewrote requests repeatedly after the fact (focus-in-line, the band stuck on step 1/5). A scripted mock of the finished behavior is cheaper to correct than code.
  Done when: for FEATURE M/L, the plan includes a 10–30 line fake terminal or UI transcript. The builder lane starts only after approval, and the final smoke or journey output is diffed against that transcript.

- **Gate license and provenance on added code and deps** — SECURITY — value 3 — effort M — risk low — category: compliance
  Why: supply-chain signals are covered, but license compatibility and pasted-snippet origin are not. Assumption: the repos ship publicly (Foreman is on GitHub).
  Done when: the done-gate lists new dependencies with their licenses and flags copyleft or unknown ones against a project policy. It blocks on a violation with a named fix.

- **Wild: Incubate a whole project from one line overnight** — FEATURE — value 4 — effort L — risk med — category: greenfield
  Why: wild. Spike lanes are per-project, and nothing starts a project. The queue-idle complaints show spare capacity and appetite.
  Done when: `fm incubate "<idea>"` creates a throwaway repo, runs the full discipline through an MVP, and returns a demo clip, a cost summary and a keep/kill card. Kill leaves nothing behind.

- **Wild: Borrow usage from tomorrow's pace** — FEATURE — value 3 — effort M — risk med — category: budget
  Why: wild. The user said limits shouldn't block before 75% and subagents shouldn't be hard-capped. An explicit loan for an urgent task fits that stance and shows the cost honestly.
  Done when: past a pace line, `fm budget loan <task>` approves extra spend. The pace gauge shows the debt, and the next day's pace targets shrink accordingly in `fm digest`.

- **Wild: Suggest ghost edits while the user types by hand** — FEATURE — value 3 — effort L — risk high — category: editor
  Why: wild. Foreman covers agent work but not the user's own keystrokes. The brief, plan, vetoes and map are a richer context than a generic completion has.
  Done when: in the desktop app or an editor sidecar, saving a file shows a suggested next hunk citing the brief step and any veto that applies. Accepting it logs evidence for the step. Nothing is written unaccepted.

- **Turn the ledger into client-ready progress reports** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: assumption: the user works on projects for others. `fm digest` and `fm pr` already hold the facts but not a shareable, non-technical form.
  Done when: `fm report --since 7d --audience client` outputs plain-language markdown with work delivered, proof links and hours or cost. It excludes internal lessons, vetoes and paths.
