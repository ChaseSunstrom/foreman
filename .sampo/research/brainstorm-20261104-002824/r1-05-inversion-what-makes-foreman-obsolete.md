# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Ablate each scaffold step per local model** — FEATURE — value 5 — effort M — risk low — category: local models
  Why: the standing steer is to scaffold local models (the 27B, Ollama models) up to frontier results, but nothing measures which scaffold steps still earn their keep. Each model upgrade can turn a step into dead weight. Assumption: the model bench can run with a step on and off.
  Done when: `sampo louhi` prints a per-step pass-rate delta for qwen3.8-27b on held-out closed tasks, and a step with delta ≤ 0 is skipped by default for that model.

- **Switch token-thrift machinery off for free local models** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: compact output (T-0828), ceremony tiers (T-1266) and pace degrade exist to save paid tokens. On a local endpoint those savings are worth zero, but the added complexity and information loss remain. Assumption: the profile records whether a backend is metered.
  Done when: a task run on a local profile shows no compaction or tier downgrade in its receipt, and a test fails if a metered profile loses them.

- **Replay the last 30 days with Foreman off** — FEATURE — value 5 — effort M — risk med — category: honesty
  Why: the idea list has necessity corpora and bare-model ablations, but no passive version over the user's own real ledger. Classify each block, nudge, gate failure and resume as "host alone would have done this" or "only Foreman did", using the host's permission rules and tool list. Assumption: ledgers hold enough detail for that classification.
  Done when: `fm uninstall --preview` lists unique saves and redundant interventions, each with its ledger row id, and a fixture ledger gives a known count.

- **Sweep the backlog for tasks whose premise is already met** — CLEAN — value 4 — effort S — risk low — category: queue hygiene
  Why: about 30 "Later from T-07xx/08xx" deferred items sit open, and the user's recent drops include "premise already met" and "stale". Resolve each task's claims against the repo, `--help` and host tool list with no model, then propose closing the ones that no longer hold.
  Done when: `fm tasks sweep` lists deferred tasks with at least one unresolved claim and the evidence line, and a planted obsolete task is caught.

- **Graduate nudges to shadow per user and model** — FEATURE — value 4 — effort M — risk med — category: stand-down
  Why: if the user already plans first or writes the test first, or a model never skips proofs, the matching nudge is noise. This is teaching to obsolescence. Assumption: each nudge has a measurable trigger condition.
  Done when: after N consecutive tasks where a nudge's trigger never held, it moves to shadow for that user and model, `fm doctor` names it, and it returns on the first lapse.

- **Make the drive runner-pluggable** — FEATURE — value 4 — effort L — risk med — category: portability
  Why: T-0793 (cloud routines) and the "user is asleep" steer point to unattended work moving off the local box. If the host ships good cloud runs, a local-only drive is obsolete. Define the drive's contract as queue in, receipts out, with the Ward and Exam applied at the edges.
  Done when: a fake remote runner completes a queued task through the same contract and the receipt passes the same gates as a local run.

- **Draw the discipline Pareto curve** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: nobody has measured how much of the held-rate comes from 0, 5, 20 or all rules. It would show which minimal config (poor man's Foreman) reaches 90% of the full result. A tripwire tells the user once when bare config catches up.
  Done when: the Models section of the site shows held-rate against rule count on at least 8 held-out scenarios, and the one-time "you may not need the rest" line fires on a fixture.

- **Test recall and map against just reading the repo** — PERFORMANCE — value 3 — effort M — risk low — category: context
  Why: as context windows grow, repo map and lesson recall may stop helping on frontier models, but the 27B still needs them. Find the crossover per model.
  Done when: for two models, an A/B on 10 tasks reports first-pass rate with and without map and recall, and injection is gated by the result.

- **Layer over host-native tasks instead of beside them** — FEATURE — value 3 — effort M — risk med — category: integration
  Why: hosts keep adding todo and plan features, so a parallel queue eventually becomes the redundant one. Mirror both ways so Foreman holds only what the host can't (dependencies, Exams, grants). Assumption: the host exposes a readable task store.
  Done when: a task created in the host's native list appears in `fm next` with its id, and closing one closes the other.

- **Draft the self-deleting migration when the host ships an equivalent** — FEATURE — value 4 — effort L — risk med — category: self-retirement (wild)
  Why: the idea list already says to watch release notes and mark verbs the host now does natively, but stops at flagging. Take the next step: generate the deletion patch plus the exam that proves nothing regressed.
  Done when: given a fixture release note matching a verb, a task is filed with a deletion diff and a green exam run.

- **Ask the model to fire Foreman line by line** — FEATURE — value 3 — effort S — risk low — category: self-report (wild)
  Why: it is cheaper to have a tool-less child mark which injected lines it would have followed anyway, then ablation-test only those. It turns model self-report into a shortlist of candidates for the necessity test.
  Done when: each new model ID gets a ranked "would skip" list, and the top 5 are ablation-tested with results recorded.

- **Run a frontier-optional week** — PERFORMANCE — value 5 — effort L — risk med — category: local models (wild)
  Why: the steer is local models scaffolded to frontier results. Run the queue with the local model doing the work and frontier only judging, then publish the share of tasks that pass the same Exam at what cost.
  Done when: the report gives the local-only pass share against a frontier-only baseline on the same briefs.

- **Spar nightly with a rival plugin's default config** — FEATURE — value 3 — effort M — risk low — category: benchmarking (wild)
  Why: T-0866 and T-0869 want bench cases and rival plugin imports. Running a rival's stock setup on Sampo's own held-out tasks shows where Foreman is already redundant or behind.
  Done when: a scorecard shows Foreman against one rival on at least 9 scenarios, with the first loss named.

Next question: which Foreman interventions has the user overridden or undone, and do those cluster in capabilities the bare model already covers?
Next question: what is the smallest signal that tells us the user has stopped reading Foreman's output, as distinct from trusting it?
