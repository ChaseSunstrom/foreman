# Brainstorm — lens: state-of-the-art agent harness gaps

- **Add `fm spec` executable-spec intake with EARS-style requirements** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: Kiro and Spec Kit (landscape research done) turn requests into numbered requirements that trace to tests; Foreman has criteria with verify commands but no requirement→design→task chain or traceability matrix. Assumption: criteria are free text today.
  Done when: `fm spec new` on a paragraph yields requirement IDs, each linked to a criterion, and `fm task done` fails if a requirement has no linked passing verify.

- **Expose Foreman as an MCP server of read-only state and recall tools** — FEATURE — value 4 — effort M — risk low — category: interop
  Why: Other agents/subagents and non-Claude-Code clients can't query `fm recall`, `fm why`, `fm map`, or task state. `fm-recon` and `claude -p` children are tool-less or limited; an MCP stdio server in stdlib Python gives them recall and map without file access. Assumption: no MCP server exists in fmserve.
  Done when: a `claude -p` child with the Foreman MCP configured answers "what lessons exist on fmguard?" through the `recall` tool, and the call is visible in the transcript.

- **Add session-trace distillation into reusable skills (`fm distill`)** — FEATURE — value 5 — effort L — risk med — category: self-improvement
  Why: Voyager/Claude "skills from trajectories" pattern; `fm repeats` finds repeated manual work but only suggests, and creating skills is guarded. Distill a successful bench-passing task transcript into a candidate playbook, then verify lift on `fm bench` before one yes/no install.
  Done when: `fm distill T-NNNN` writes a draft playbook to a staging dir and `fm bench run` reports pass-rate/cost with vs without it.

- **Add a continuous-learning instinct store with confidence decay** — FEATURE — value 4 — effort M — risk med — category: memory
  Why: ECC's "instincts" are small observed behaviours with confidence, reinforced or decayed by outcomes. Foreman has lessons and corrections but no confidence-weighted, auto-promoting layer. Assumption: lessons currently have no scores. Complements, doesn't duplicate, "hit counts."
  Done when: a repeated user correction raises an instinct's confidence across 3 sessions, and a contradicted one drops below the injection threshold and stops appearing in `fm next`.

- **Make long-horizon runs resumable via a plan-DAG with checkpoint commits (`fm goal`)** — FEATURE — value 4 — effort L — risk med — category: autonomy
  Why: The user wants "don't stop" recursive work; Task Master/Kiro decompose goals into dependency graphs. Foreman has queue and lanes but a goal like "make it the best plugin" has no tree, no stop rule, no spend ledger. Assumption: "Track multi-task goals" was proposed but not built.
  Done when: `fm goal add` decomposes into dependent briefs, a killed session resumes at the first unmet node, and the goal halts at a set token ceiling.

- **Add an LLM-as-judge rubric grader to `fm bench` for non-test tasks** — FEATURE — value 4 — effort M — risk med — category: evaluation
  Why: bench only handles fail-to-pass cases with hidden tests; most Foreman work (CLEAN, docs, UI, research) has none. A rubric derived from the task's criteria, graded by a separate-model `claude -p` child, lets those be A/B measured too.
  Done when: `fm bench run` scores a docs-only finished task using a rubric file and reports grader agreement with the original verdict on 5 labelled cases.

- **Wild: Run a competing-harness shootout inside `fm bench`** — FEATURE — value 4 — effort M — risk low — category: evaluation — wild
  Why: bench replays headless with a candidate plugin; run the same cases with plain Claude Code and with a disabled-Foreman baseline to show where Foreman helps or hurts and prune ceremony that never pays.
  Done when: `fm bench compare --baseline none` prints per-case pass, cost, turns for Foreman vs bare Claude Code.

- **Wild: Self-evolving prompts via bench-gated mutation (GEPA-style)** — FEATURE — value 5 — effort L — risk high — category: self-improvement — wild
  Why: `/foreman:improve` builds candidates by hand. Let a child propose mutations of a single skill or STAGE_REFERENCE text, evaluate on a held-out bench split, and keep a Pareto front of cost vs pass rate; applied only after one yes.
  Done when: `fm evolve SKILL` runs N mutations, outputs a front table, and the winner beats baseline on held-out cases.

- **Add an AST-aware context compressor for reads (`fm outline`/`fm slice`)** — PERFORMANCE — value 4 — effort M — risk low — category: context
  Why: Aider repo-map and token-sensitive user; Python `ast` can return signatures and a requested function body. Assumption: the existing outline-first idea was only a guard, not a slice tool with measured savings.
  Done when: `fm slice file.py:func` returns just that body plus imports, and a bench case shows lower read tokens at equal pass.

- **Wild: Add a "shadow reviewer" that critiques every plan with a different model before execution** — FEATURE — value 3 — effort S — risk low — category: review — wild
  Why: Multi-model cross-check is a known harness gap; plans currently get only the user's approval or Foreman's own audit. One `claude -p` child with a different model reads the brief and returns three objections.
  Done when: `fm task plan` on an L task attaches a ≤120-word objections block and bench shows whether it changes first-pass success.

- **Add cross-harness export of briefs and lessons as AGENTS.md** — FEATURE — value 3 — effort S — risk low — category: interop
  Why: AGENTS.md and Cursor/Codex rules are the de facto cross-tool standard; Foreman's lessons are Claude-Code-only. Generate a bounded AGENTS.md from lessons and project map behind one outward yes.
  Done when: `fm export agents` writes an AGENTS.md under 2 KB with top lessons and test commands, regenerated deterministically.
