# Brainstorm — lens: simplicity

- **Replace prefix allow-lists with six conserved danger classes** — FEATURE — value 5 — effort M — risk med — category: guard
  Why: users report 15+ approval prompts a session because allow rules match command prefixes. Immune receptors recognise a few conserved patterns, not each pathogen. The classes: write outside repo, egress, credential read, irreversible delete, privilege change, install.
  Done when: replaying the user's command history through the guard gives at least 50% fewer prompts, with zero new misses on the 124-case corpus.
  Prior art: Codex and Claude Code approve by prefix or rule. Better by: one approval covers a class plus target, not a string. Novelty: 3

- **Catch the rubber-stamping human** — FEATURE — value 4 — effort S — risk low — category: guard — wild
  Why: assumption: prompt fatigue works like high-dose tolerance, so approvals get faster and blinder. After 8 approvals each under 2 seconds, the next prompt becomes a typed one-line confirmation.
  Done when: a scripted burst of fast approvals triggers the typed confirmation, and a slow one does not.
  Prior art: none found. Better by: it guards the approver, not only the agent. Novelty: 5

- **Beat the dumbest guard** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: the guard has 124 cases but no floor to say what its complexity buys. The innate layer is a small set of germline receptors. A substring denylist of at most 30 lines is the equivalent.
  Done when: `fm replay` prints the denylist's score beside the guard's, and a rule is kept only if it flips at least one case.
  Prior art: none found. Better by: it gives every rule a measured reason to exist. Novelty: 3

- **Run an innate-only exam arm** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: a guard-only arm is already requested, but no arm freezes every learner (lessons, triggers, calibration). That arm shows what the adaptive layer earns.
  Done when: `fm exam run --agent innate` runs with learners read-only, and `fm doctor` shows the delta per kind.
  Prior art: ablation duels remove one feature at a time. Better by: it removes the whole class in one run. Novelty: 3

- **Shadow-retire before deleting any rule** — FIX — value 3 — effort S — risk low — category: guard
  Why: once an antibody exists, the antigen vanishes, so the rule looks unused and gets culled. Any retirement from non-firing data is therefore survivorship-biased.
  Done when: a retire candidate runs log-only for 30 days, and one would-block cancels the retirement.
  Prior art: none found. Better by: it separates "never needed" from "working". Novelty: 4

- **Allow one input per detector** — CLEAN — value 3 — effort S — risk low — category: learners
  Why: allelic exclusion means one lymphocyte carries one receptor. A detector that reads one declared signal has attributable precision, which the trigger auto-demotion already needs.
  Done when: a lint fails any detector that reads an undeclared input, and the registry lists one input per detector.
  Prior art: the Unix single-purpose rule. Better by: it is enforced, not a convention. Novelty: 2

- **Salt every fence around untrusted text** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: CI logs, issues and the SessionStart note carry untrusted text, and fixed delimiters can be forged. A per-session random id on each fence cannot be.
  Done when: a fixture containing a forged closing fence stays inside the data block.
  Prior art: this harness already ids its pasted blocks. Better by: it covers every Foreman-written fence. Novelty: 2

- **Fold all modes into one stance file** — CLEAN — value 3 — effort M — risk med — category: state
  Why: risk budget, fever, quarantine, away and privileged zones would each get their own state and reader. One line of `key=value ttl`, with one reader and one `fm doctor` row, replaces them.
  Done when: every mode reads and writes only the stance file, and the old state files are gone.
  Prior art: none found. Better by: one place shows why Foreman is acting cautious. Novelty: 3

- **Step autonomy down on three bits** — FEATURE — value 3 — effort S — risk low — category: autonomy
  Why: clinical triage uses three bedside yes/no bits, not a model. The bits are: touched files outside the plan, check turned red, over half the budget spent. Any two step autonomy down.
  Done when: a replay of past sessions shows the three-bit rule agrees with the risk budget on at least 90% of step-downs.
  Prior art: risk budget exists but is complex. Better by: you can read it in one glance. Novelty: 3

- **Type each repo with five bits** — FEATURE — value 3 — effort S — risk low — category: profile
  Why: assumption: a repo's traits (secrets present, deploys, network tests, monorepo, CI) set which danger classes matter. A first-visit scan picks the guard profile.
  Done when: `fm doctor` prints the five bits, and a docs-only repo gets the quiet profile.
  Prior art: none found. Better by: it adds no new rules, only a choice of which apply. Novelty: 3

- **Route risky tasks by model block rate** — FEATURE — value 3 — effort M — risk low — category: routing — wild
  Why: assumption: models differ in how often the guard blocks them. A per-model, per-task-kind block rate is cheap ground truth for routing, which the bet harness field already half-records.
  Done when: `fm outcomes --by model` shows blocks per 100 calls.
  Prior art: none found; rivals report cost only. Better by: it measures behaviour, not price. Novelty: 4

- **Shed derived caches on a fixed clock** — CLEAN — value 2 — effort S — risk low — category: state — wild
  Why: skin sheds on a schedule instead of tracking each damaged cell. Maps, packs and caches expire at 7 days and rebuild lazily, with no invalidation logic.
  Done when: no cache has an invalidation function, and the oldest derived file is under 8 days old.
  Prior art: the standard TTL cache. Better by: it deletes code instead of adding it. Novelty: 2

Next question: which of Foreman's defences does the user never see fire, and would they notice if it were deleted?
Next question: how often does the user approve a prompt without reading it, and has anything measured that?
