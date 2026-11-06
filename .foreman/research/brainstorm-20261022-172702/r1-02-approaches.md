# Brainstorm — lens: approaches

- **Add a trigger eval that fails doctor when a skill never fires** — FEATURE — value 5 — effort M — risk low — category: skills
  Why: usage shows 12 of 13 skills never used, and no one measured why. The cause list (hooks pre-empt, wrong trigger words, budget) is inferred, not tested.
  Done when: `fm skills eval` runs N scripted scenarios, including autonomous-run states with no user words, and prints a per-skill invocation rate. `fm doctor` warns on any skill at 0%.

- **Trigger playbooks from the file being edited** — FEATURE — value 5 — effort M — risk med — category: hooks
  Why: the playbooks that do get read (ui/motion, scene-3d, review/security) map to file types and actions. 65 of 82 are never read because they hide behind one skill.
  Done when: a PreToolUse or PostToolUse hook, on first edit of a `.css`/`.tsx`/`.html` file in a session, injects a ≤1.5 KB excerpt of the matching playbook once. A test confirms it is not repeated and stays under the 10 KB preview limit.

- **Make the "Next:" hook line name the skill** — FIX — value 4 — effort S — risk low — category: hooks
  Why: cause #1 is that the injected "Next: fm …" command replaces the skill that describes the step. Pointing at the skill where the step has real how-to turns the pre-emption into a route.
  Done when: hook output for steps with a matching skill reads "Next: fm X (steps: foreman:Y)". The trigger eval shows that skill's rate above 0.

- **Rewrite descriptions as "Use whenever you are about to…"** — FIX — value 4 — effort S — risk low — category: skills
  Why: the pack's own example from anthropics/skills triggers on tasks, while Foreman's descriptions trigger on user words ("status", "where were we"). Autonomous runs never contain those words.
  Done when: all 13 descriptions are task- and state-phrased ("about to close a task", "queue empty", "gate failed"), total ≤2,000 chars, and the eval rate rises on the autonomous scenarios.

- **Rebalance the skill portfolio from usage** — CLEAN — value 4 — effort M — risk med — category: skills
  Why: the 2,000-char cap (T-1508) fixes the count, and the slots are spent on skills nobody uses. The most-read playbooks are not skills at all.
  Done when: `fm skills rebalance` proposes swaps. Merging never-used skills into playbooks and promoting the top-read playbooks (code-reviewer, security, motion, scene-3d) to skills keeps the total ≤2,000 chars. It applies only on approval.

- **Free listing budget with user-only skills** — PERFORMANCE — value 3 — effort S — risk low — category: skills
  Why: capture and design-extract are already user-only. Assumption: `disable-model-invocation` skills cost no model-listing budget, which would let the user-triggered ones move to slash commands and free room for model-triggered ones. This needs checking against Claude Code.
  Done when: a measured test shows the listing size before and after marking status, tidy and library user-only, and the freed characters fund at least 2 new task-triggered skills.

- **Expose playbooks as a searchable tool, not a hidden skill** — FEATURE — value 4 — effort M — risk med — category: playbooks
  Why: playbooks sit behind the one `playbooks` skill, which is itself never used. A search call (`fm playbooks find "<task words>"`) hinted by hooks needs no listing budget.
  Done when: `fm playbooks find` returns the top 3 matches with one-line summaries, a hook hints at it on a stuck or new-domain signal, and the read-rate of the 65 unread playbooks is measured a week later.

- **Mint skill drafts from recurring lessons** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: T-0217 tracks lesson confidence, and the user wants "way more skills" but writing them by hand has not scaled. Skills should come from real repeated work.
  Done when: a lesson recalled at least 3 times with first-time passes produces a draft skill in `.foreman/skills-proposed/`. It stays inactive until `fm skills accept`, and the guard rules are unchanged.

- **Import vetted third-party skills through the guard** — FEATURE — value 3 — effort L — risk high — category: ecosystem
  Why: anthropics/skills shows the pattern and a ready library, and the constraint says third-party skills run nothing unguarded.
  Done when: `fm skills add <path>` copies a skill into a quarantine folder and lints it. Its scripts only run through the guard, and a test shows an unguarded script is refused.

- **Delete the dead skills and ship fewer, better ones** (doing less) — CLEAN — value 2 — effort S — risk low — category: skills
  Why: 12 of 13 are unused over 30 days. The honest minimal answer is that hooks already carry the discipline. It conflicts with the user's ask for more, so it is the fallback if the eval shows triggering can't be fixed.
  Done when: skills with 0% eval rate and 0 usage are folded into playbooks, and `fm doctor` reports the smaller listing with no loss in test coverage.

- **Turn playbook families into specialist subagents** — FEATURE — value 4 — effort L — risk med — category: agents — wild
  Why: assumption: subagent descriptions are listed separately from the skill budget. Roles like "motion-designer", "security-reviewer" and "scene-3d-builder" with their playbooks preloaded are delegated by name, and review/security and scene-3d are already the most-read.
  Done when: 6 role agents ship with their playbooks preloaded, and a run log shows the orchestrator delegating to at least 3 of them unprompted.

- **Evolve descriptions overnight against the trigger eval** — FEATURE — value 3 — effort M — risk med — category: skills — wild
  Why: with the eval in place, a lane can try description variants, keep only a measured winner, and commit with the before/after numbers. No one hand-tunes triggering again.
  Done when: a lane run produces a PR-style diff for one skill showing its eval rate rising from X% to Y% with all descriptions still ≤2,000 chars.

- **Show a "skill dividend" panel in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI — wild
  Why: users can't see what skills do for them. The panel scans transcripts for moments Claude did by hand what a skill covers (the same greps, status checks), then shows "a skill would have saved ~N tokens". That makes the gap visible and shows which skills to promote.
  Done when: the web UI has a Skills tab listing each skill's invocations, missed opportunities and estimated tokens, with empty and loading states, driven by `fm usage` data.

- **Let a skill declare the state that should wake it** — FEATURE — value 4 — effort M — risk med — category: skills — wild
  Why: descriptions can't express "gate failed twice" or "context at 70%". A `wake:` field in the skill's frontmatter, which Foreman's hooks read, turns state into the trigger, so no one depends on the model's guess.
  Done when: a skill with `wake: gate_failed>=2` is announced by the Stop hook at the second failure, and a test checks it doesn't fire at the first.
