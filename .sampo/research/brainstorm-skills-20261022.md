## Brainstorm clustering and build slate: why Foreman's skills go unused

### 1. Answer
The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the exact `fm` command. The fix is to make the hooks name the skill (or playbook) at the right moment, then measure it. Adding more skills comes after that. The 2,000-character cap is Foreman's own rule (T-1253/T-1508), not Claude Code's. Restructure it (a user-only tier plus a hook-delivered router) instead of raising it. I did not check Claude Code's own limits.

### 2. Catalogue
Ideas are grouped by the short handles in `ideas.md`. About 149 ideas are covered. Every bullet falls in a cluster; the overlaps are noted.

| Cluster | Ideas (handles) | Grounding | Val | Eff | Risk | Mark |
|---|---|---|---|---|---|---|
| A. Hooks name the skill | Next lines name the skill (3 variants); turn-start hook chooses; retrieve in hook; path-triggered whispers; stage and file routing; state wakes a skill; load a playbook on demand; self-surfacing by path; before-edit and before-close pair; silence Next once followed | Partial. The hook already names `/foreman:brainstorm`, `/foreman:intake`, `/foreman:directions` (`fmhooks.py:1152,1176,1879`). `fmcore.py:2176-2180` `STAGE_REFERENCE` names `/foreman:playbooks` only for CLEAN, PERFORMANCE and SECURITY. FIX and FEATURE point at file paths. The `Next:` line (`fmhooks.py:1194`) is the bare `fm` text from `next_for`. | 5 | M | Context tax: `PROMPT_BUDGET` caps it, and T-1258 is a ratchet on injected bytes | **build** |
| B. Task-term descriptions | rewrite ×4; "Use whenever about to"; lint competing; A/B live; evolve overnight; sparring; description-optimizer; learn from manual invocations; misses rewrite; "why skills don't fire" page | Partial. Descriptions already start "Use when…", but they use Foreman nouns ("STATE", "STATUS", "RESUME"). Only `brainstorm` and `directions` use user words. | 4 | S | Low | **build** (hand rewrite and lint; skip the overnight and A/B machinery) |
| C. Router / index | foreman:index; `fm which`; zero-skills `fm help <moment>`; playbooks as a searchable tool; two-tier listing; one self-updating line; section-addressable; card/body split; thin bodies | Partial. `fm playbooks show` exists (`fmplaybooks.py:416`, `cmd_show`). The `playbooks` SKILL.md is a 98-line index. There is no `fm which`. | 4 | M | Low | **build** `fm which` (a router) and fold in the playbooks index; skip zero-skills |
| D. Playbooks to skills | promote proven; split by job; four or five families; a stub per playbook; `fm skills gen`; fold 13 into 4 or 5; merge status skills; specialist subagents; preload into subagents and lanes; forked context; compile mechanical playbooks into checks | Partial. The 82 playbooks live under one skill. `fm-reviewer` already reads review playbooks. Only a few are skills (`library`, `directions`). | 4 | M | Description budget (cluster H) | **build** two or three jobs; **skip** a stub per playbook and "fold 13 into 4" (churn) |
| E. New skills | design pack (3D, motion, looks); standalone design plugin; bundled scripts; personal-prefs skill; argue-my-side skill; per-project skill from `fm map`; draft from a recurring lesson (×3); autopilot; Claude writes the missing skill | Partial. The UI playbooks exist (`ui/scene-3d`, `motion`, `type-and-colour`, `design-direction`, `visual-qa`). So do the `fm design`, `fm scene` and `fm looks` verbs (`fmcli.py:6040,6063,6154`). The only design skills are `directions` and the user-only `design-extract`. `fm repeats` already drafts project skills (near T-1070). | 5 | M | Overlaps D | **build** the design pack; **skip** autopilot and personal-prefs (speculative) |
| F. Measure use | dead skills in `fm usage`; web UI panel, dividend, scorecard, chips, hit rate; extend the census; skill-miss detector; count inline use; why-not-loaded; replay or mine transcripts (×5); coverage matrix; close-out receipts; "consulted" field; gate close-out; gate FEATURE; rating; triage by usage | Partial. `fmcost.py:1102` `cmd_usage` counts `tool=="Skill"` events and playbook Reads or `show`. It prints "never used" at `:1158`. Gap: the hook-injected `/foreman:x` text and user-typed slash commands may not log a `Skill` event (inferred, low confidence). There is no miss detector. The ask-style "reach" lives in `fmplaybooks.reach`. | 5 | S/M | Metric validity | **build** |
| G. Evals and ratchets | `fm skills eval`; trigger eval fails doctor; firing ratchet; duels (×3); weekly ablation; cheap-model bench; smoke test; skill court | Missing for skills. Bench duels exist for plugins (near T-0280). | 3 | L | Needs a model run | **build** a static trigger-lint ratchet; **skip** live duels (cost, flaky) |
| H. Budget | user-only out of the budget; tiered descriptions; lift cap; per-project dynamic; list only relevant; slash-menu reorder; context rent in doctor | `test_docs.py:55-71` sums non-user-only skill and command descriptions plus workflow `description`s ≤ 2000. `USER_ONLY = {capture, design-extract}` (`:13`). | 3 | S | Context growth | **restructure**, don't raise (see §3) |
| I. Lifecycle | delete dead; merge or retire; retire after 90 days; review date; trial status; rebalance; prune; delete those a hook does | `fm usage --prune` exists for commands (`fmcost.py:1162`). It is not wired to skills. | 3 | S | Premature deletion | **build** as a report only (extend `--prune` to skills); **skip** auto-retirement |
| J. Authoring and ecosystem | `fm skill new` and lint; import via guard; sandbox; project overlay; `skills.toml`; one moment registry; export to other CLIs (×4); commons; cross-project recall | The overlay for playbooks exists (`.claude/playbooks/`, decision 2026-10-22). Guard and indexer hardening exists (near T-1396). `fm recall` exists. | 2 | M | Scope creep | **skip** (not the cause). Keep `fm skill lint` inside B. |
| K. Delight | karaoke; mascots; sidekick; gallery; skill of the day; rehearse unused; preview box; `/foreman:why`; what's new | Pane skill-use exists (near T-0939). | 2 | M | Noise | **skip**; `/foreman:why` joins F |

False premises:
- "Hooks never name a skill" is wrong. They name `/foreman:intake`, `brainstorm`, `directions`, `next`. But `Next:` itself is bare `fm` text, and the FIX and FEATURE stages point at file paths, not skills.
- "65 of 82 never read" counts only Reads and `fm playbooks show`. Subagent reads (`fm-reviewer`) may be undercounted (unverified).
- Much of the "near T-…" tagging in the index marks neighbours, not duplicates. Most ideas are not yet built.

### 3. Claude Code and the budget
- The 2,000-character cap is Foreman's own test (`test_docs.py:71`). It is set by T-1253: Claude Code 2.1.304 re-sends the listing after every compaction (`test_docs.py:56-57`). Decision T-1508 (`decisions.md:160`) kept the cap and rejected 2,100. Confidence: high. The platform's own limits I did not verify. The test only enforces a per-description maximum of 1024 (`:51`).
- Users can type `/foreman:x` regardless of the listing. Hook-named skills still need `Skill` invocation, which is fine because `disable-model-invocation` is set only on `capture` and `design-extract`.
- Restructure:
  - Move the rarely-model-triggered skills to user-only: `doctor`, `tidy`, `improve`, `reflect` (they are named by hooks, not by user words).
  - Spend the freed characters on task-term descriptions for the design, debugging and testing skills.
  - Keep the cap.

### 4. Build slate
All S or M. Run `python3 plugin/tests/run.py <module>` to verify.

1. **Hook names the skill on Next and on stage entry** (FEATURE, M; scope `plugin/lib/fmhooks.py`, `fmcore.py`, `plugin/tests/test_hooks.py`).
   - Acceptance: a replayed prompt for a design request injects `/foreman:ui-design` (or the new skill), and the injected total stays within `PROMPT_BUDGET`. Verify: `python3 plugin/tests/run.py test_hooks`.
   - Steps: add a `SKILL_FOR` map from stage and keyword to skill; append `(skill foreman:X)` to `next_for` and `STAGE_REFERENCE`; test the byte ratchet.
   - Claude Code: the `UserPromptSubmit` text makes the model call the `Skill` tool.
2. **Task-term descriptions and `fm skills lint`** (CLEAN, S; scope `plugin/skills/*/SKILL.md`, `fmdoctor.py`, `test_docs.py`).
   - Acceptance: no description contains `STATE`, `STATUS` or `RESUME` unquoted, and lint flags two descriptions that share more than 60% of their words. Verify: `python3 plugin/tests/run.py test_docs`.
   - Steps: rewrite 13 descriptions; add lint to doctor; keep the total ≤ 2000.
   - Claude Code: skill selection reads the new descriptions.
3. **Free the listing: user-only for the hook-named skills** (CLEAN, S; scope `test_docs.py` `USER_ONLY`, four `SKILL.md` files).
   - Acceptance: the listing total drops by at least 300 characters and the hooks still name them. Verify: `test_docs`.
   - Steps: add `disable-model-invocation: true` to `doctor`, `tidy`, `improve` and `reflect`; extend `USER_ONLY`; confirm the hooks use `/foreman:x`.
   - Claude Code: the user types the slash; the hook text offers it.
4. **`fm which <task>` router** (FEATURE, M; scope `fmcli.py`, new `plugin/lib/fmwhich.py`, `plugin/tests/test_which.py`).
   - Acceptance: `fm which "make a 3D hero with motion"` prints the skill and the playbooks `ui/scene-3d.md` and `ui/motion.md`. Verify: `python3 plugin/tests/run.py test_which`.
   - Steps: index skill descriptions and playbook headers with the existing `fmplaybooks` `_tokens`; rank; print a `fm playbooks show` line.
   - Claude Code: hook line "unsure? `fm which <task>`".
5. **Design pack: `ui-design` skill, M** (scope `plugin/skills/ui-design/`, `test_docs.py`).
   - Acceptance: SKILL.md routes 3D, motion, type, a non-generic look and QA to the UI playbooks plus `fm scene`, `fm design`, `fm looks`, and `directions`. Verify: `test_docs` (references exist).
   - Steps: write a task-shaped body of under 100 lines; link `scene-3d`, `motion`, `visual-qa`; add it to `SKILLS`.
   - Claude Code: `/foreman:ui-design` or a plain request.
6. **Three job skills from playbooks: `debug-test`, `release`, `research`** (FEATURE, M; scope `plugin/skills/{debug-test,release,research}/`).
   - Acceptance: each is under 60 lines, wraps existing playbooks and `fm` verbs, and fits the budget after #3. Verify: `test_docs`.
   - Steps: point to `intake/references/debugging.md`, `fix/flaky-tests.md`, `release/*`, `ground/search-first.md` and `fm research`.
   - Claude Code: each is model-invocable by task words.
7. **`fm usage` counts hook-named skills and slash commands, and shows misses** (FIX, M; scope `fmcost.py`, `fmhooks.py`, `test_cost.py`).
   - Acceptance: a fixture where the hook named `/foreman:X`, the model ran `fm` and did not load `X`, reports `missed: X`. Verify: `python3 plugin/tests/run.py test_cost`.
   - Steps: log a `skill_named` event; compare it with `Skill` events and `fm` Bash; print a "named, not loaded" line.
   - Claude Code: all in hook events.
8. **Unused-skill ratchet** (FEATURE, S; scope `fmdoctor.py`, `fmcost.py`).
   - Acceptance: `fm doctor` warns when a model-invocable skill had zero loads in 30 days and the hook named it more than N times. Verify: `test_doctor`.
   - Steps: reuse #7's data; warn only; no auto-deletion.
   - Claude Code: shows up in `/foreman:doctor`.
9. **Static trigger eval** (FEATURE, S; scope `plugin/tests/test_docs.py`, a new `trigger_cases.json`).
   - Acceptance: 3 or more phrased requests per skill match that skill's description above a threshold, with no tie. Verify: `test_docs`.
   - Steps: write a corpus mined from `fm recall`; use word overlap with ties failing.
   - Claude Code: guards #2.
10. **Skills in the TUI settings** (FEATURE, S, only if the user wants it; scope `fmsettings.py`).
   - Acceptance: a setting toggles model-invocation per skill. Skipped by default; it conflicts with the budget test.

### 5. Risks / surprises
- A hook that names a skill adds per-turn bytes. The T-1258 ratchet may fail, so measure first.
- Usage may undercount user-typed slash commands (inferred from `cmd_usage` reading only `tool=="Skill"`; low confidence). Check before judging skills as dead.
- The 13 skills include `library`, which `named cards` already triggers via hook. It may be "used" through `fm lib` and show 0 as a skill.
- `directions`' T-1508 note says Claude couldn't start it from plain words. Rewrites in #2 should be tested against that.

### 6. Not checked
- Claude Code's own skill-listing limits (no web check).
- The per-lens files.
- Web UI and pane code.
- `fm lib` card count. The glob for `skills/library/cards/*/` returned nothing. `fmlib.py` was not read.
- The `fmdoctor` skills checks.
- Event-log samples proving the 13/82 figures.

**Noticed:**
- `plugin/lib/fmlandlock.py` is untracked and `plugin/tests/test_guard_hardening.py` is modified. This work is outside the brief.
- The `ideas.md` "near T-…" tags are noisy: many point at unrelated tasks. A task-ID match on the word overlap is unreliable.
- `fm usage` hides subagent reads, so the "65 of 82" figure may be inflated. Worth its own check.
