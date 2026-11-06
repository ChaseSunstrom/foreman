# Brainstorm — lens: self-modification

- **Seal the verifier against the task it judges** — SECURITY — value 5 — effort M — risk low — category: self-judging
  Why: Mission 4 adds criteria compilers, probes and the unproven labeller, and the builder of a task could edit the code that grades it. Related ideas already listed (protect the core by path, bar the builder from closing its own Exam) cover paths, not the case where one diff changes both the claim and its checker.
  Done when: a test diff that touches both a doc claim and the probe or criterion file that checks it closes as "self-judged", never "proven", until a later task re-runs the claim on the unchanged checker.

- **Repair a drifted probe before calling its claim unproven** — FIX — value 4 — effort M — risk med — category: probe upkeep
  Why: the 421 flagged docs and the T-2748 module move (fm*.py to shims under plugin/lib/sampo/) mean many probes will break on a path, not on a false claim. Assumption: a large share of the first unproven labels will be broken paths.
  Done when: renaming a file cited by a probe makes Sampo follow the git rename, re-run the probe and record "probe repaired" with the old and new path. A probe that can't be repaired is labelled "probe broken", a different label from "claim unproven".

- **Grow the probe registry from unproven classes** — FEATURE — value 4 — effort M — risk med — category: self-extension
  Why: unproven claims are tallied by reason, but nothing turns a class with many members into a new checker. A class of 20 or more unproven claims with the same shape should file a task to build one probe type.
  Done when: `sampo unproven classes` lists classes by count, and the top class past a threshold has a filed task whose Done-when is a probe that catches a planted mutant of one member.

- **Keep the criterion-extractor rules as a data file that edits go through a held-out replay** — FEATURE — value 4 — effort M — risk med — category: extractor
  Why: turning spec examples into runnable criteria will start as hand-written patterns. Hard-coded patterns get patched by feel, and the standing rule says no per-language hand-written detection.
  Done when: patterns live in one data file, and a change to it is refused unless the replay over closed Done-whens (train/held-out split) shows no drop in extraction recall and no new tautologies.

- **Hand-label a gold set from closed Done-whens that really survived** — FEATURE — value 4 — effort S — risk low — category: ground truth
  Why: any self-tuned extractor or small-model verifier needs ground truth not authored by the extractor. Tasks that closed and survived 14 days (fm outcomes) supply it for free.
  Done when: a file of at least 40 (spec example, passing command) pairs exists, each linked to a task id and its outcome, and the extractor's score against it prints in `sampo doctor`.

- **Dogfood gate: close Mission 4 on Mission 4's own machinery** — CLEAN — value 4 — effort S — risk low — category: dogfooding
  Why: the Mission asks that anything unverifiable be labelled unproven, but nothing yet says Sampo's own repo must pass that standard before the Mission closes.
  Done when: the Mission's final receipt shows Sampo's own README, MASTER.md and site numbers run through the new lint and claim checks, with its unproven count by class printed and no unlabeled claim remaining.

- **Make self-edit wording honest: the edit says what was run** — FEATURE — value 3 — effort S — risk low — category: self-edit receipts
  Why: when Sampo rewrites its own docs or skills (genesis writes, doc downgrades), the commit message is free text. Assumption: nobody can later tell if an edit was checked.
  Done when: every self-authored docs or skill commit has a trailer `Checked: <command> -> <result>` or `Checked: none`, and the ship gate rejects a missing trailer.

- **Cold-read the diff of what Sampo tells the model, not the code** — SECURITY — value 3 — effort M — risk low — category: prompt drift
  Why: T-2768 reworded the genesis skill with no code change, and the review checked only the code. Injected notes and skills change behaviour, and the vocabulary lint covers only public surfaces.
  Done when: any commit touching skills or injected text gets a cold-read verdict on "does this change what the agent will do", and a wording-only claim is checked against a replayed scenario.

- **Wild: Mutation night on the verifier** — TEST? use FEATURE — value 4 — effort L — risk med — category: self-mutation
  Why: wild. The unproven count is only trustworthy if the checkers can fail. Each night, flip one comparison in the proof, criterion and lint code in a scratch copy and check that the test suite goes red. Survivors become labelled blind spots on the unproven shelf.
  Done when: a run in a scratch home reports a kill rate for the verifier modules, and a planted always-pass bug appears as a survivor.

- **Wild: A twin that reads only the new docs and predicts behaviour** — FEATURE — value 4 — effort M — risk low — category: doc truth
  Why: wild. After a self-edit, a tool-less child reads the old and new MASTER.md and predicts what changes for the user. Those predictions are run against scenarios. Differences show claims the docs make that the behaviour does not.
  Done when: one edited doc yields a list of predicted changes, each scored matched or unmatched by a run.

- **Wild: Let Sampo petition to retire its own checker** — FEATURE — value 3 — effort M — risk med — category: self-retirement
  Why: wild. Any check that has never failed in 90 days and agrees with the host's native result gets a retirement petition with the evidence. A reviewer lane must argue against it before the user sees it, which fits the lean stance.
  Done when: one check shows a filed petition with its pass count, last failure date and the reviewer's rebuttal.

- **Wild: Self-edit passport** — SECURITY — value 3 — effort L — risk med — category: provenance
  Why: wild. Every line of Sampo's own docs and skills carries, in a sidecar, who or what last changed it (user, builder, genesis, autofix) and which probe last passed it. A line only an agent has touched since the last human read shows as "agent-only".
  Done when: `sampo claim show <line>` prints the author class and last passing probe for one MASTER.md claim.

- **Pause self-extension while the unproven count rises** — CLEAN — value 3 — effort S — risk low — category: restraint
  Why: Sampo adds checkers, labels and lint rules faster than it can show they work (lean steer T-2503). Assumption: unproven growth is a usable signal.
  Done when: if the unproven count rose for two closes in a row, `sampo next` offers no new probe-building task until one existing probe is proven to fail on a mutant.

Next question: which self-edits did the user ever revert or hand-fix, and what shared the lines that Sampo changed?
Next question: when a checker and a claim disagree, who is wrong 'by default' in this repo's history, the claim or the checker?
