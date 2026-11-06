# Brainstorm — lens: unspoken needs

- **Measure the user's cost of being wrong, not accuracy** — FEATURE — value 5 — effort M — risk low — category: evaluation
  Why: the user's asks (T-2959..T-2973) are mostly rework after a "done" that wasn't (ship failures, shipped-site review, guard misses on real paths). Bench is accuracy vs majority (0.73 vs 0.595), which doesn't say what a wrong call cost. Label each decision by downstream cost: a later-fix task, a revert, a re-ask, minutes lost. Report each model's expected cost saved, not accuracy.
  Done when: the bench prints cost-weighted regret per slot, and a model with higher accuracy but worse regret is shown not adopted.

- **Predict "this change touches a published or live path" before the branch is cut** — FEATURE — value 4 — effort S — risk low — category: ship safety
  Why: T-2963 and T-2960 (ship conflicts on genesis.json the live tower keeps publishing; site tests failing in the scratch tree) were found only at ship time. A head or rule trained on the diffs of past ship failures flags the paths early.
  Done when: on the replayed T-2960/T-2963 briefs, the flag fires at brief time and names the file class.

- **Learn "same fix, other surface" siblings from fix pairs** — FEATURE — value 4 — effort M — risk low — category: completeness
  Why: T-2967 (guard compares literal paths in four places) and T-2964 (ten site issues in one review) show one bug has siblings. Train on briefs where a later fix touched the same pattern elsewhere; at close, list probable sibling sites.
  Done when: replayed on T-2967, the model names at least 3 of the 4 functions before the audit does.

- **Pre-rename and mass-change blast predictor** — FEATURE — value 3 — effort M — risk low — category: refactors
  Why: the Foreman→Sampo rename produced a long tail (shims, old-name tests, symlink real paths, ledger text). Generic projects will rename too. Predict the stale-name sites (shims, docs, tests, env vars, symlinks) from the repo, not from keyword search.
  Done when: on the rename commit range, recall of the later-fix files is measured and reported, with its false-alarm rate.

- **Tell the user what the model changed in plain words** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: the user is away often and returns to a pile of asks; steers say "never interrupt," "options on an artifact." A one-paragraph digest per Rune generation: which slot swapped, what it got right or wrong on their own history, with a one-word verdict.
  Done when: `sampo model digest` renders from the registry alone with no model call, and reads in under 150 words.

- **Treat the user's silence as a label** — FEATURE — value 4 — effort M — risk med — category: labels
  Why: dropped items ("stale", "not a breakage", "absorbed by") are decisions the user never typed. Mine accepts-by-not-reopening and dropped-as-noise as weak labels for the finder and intake slots.
  Done when: a weak-label set is exported with its source and a held-out check shows it agrees with typed decisions at a stated rate.

- **Flag a stale-premise brief before work starts** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: two dropped items were stale (the cold-read list named shim paths; the "breakage ahead" wasn't one). A head over brief text plus file-existence checks says "this premise has probably moved".
  Done when: on those dropped items, the flag fires and cites the changed path.

- **Cold-start a sibling-less project honestly** — FEATURE — value 4 — effort M — risk low — category: genericity
  Why: the request is a generic model, but 13 projects are lopsided (1,767 and 773 briefs against single digits). For a new project, say which slots are running on priors from other projects and which on its own data, and switch per slot as its closes accumulate.
  Done when: a new project's `sampo doctor` lists each slot as prior or own with its count.

- **Weight training by project so Sampo's own repo doesn't dominate** — FIX — value 4 — effort S — risk low — category: data balance
  Why: Sampo is 1,767 of 4,078 briefs, and its style (tower, moons, steers) is unlike a game or a git tool.
  Done when: the training build caps per-project share, and leave-one-project-out is reported with and without the cap.

- **Wild: Dream the user's next bad week** — FEATURE — value 3 — effort L — risk med — category: foresight (wild)
  Why: assumption: the late asks cluster around a few failure classes (shipping, path identity, rename tails). Replay the user's last month through the model with its wrong calls injected and show which would have turned into late asks.
  Done when: a report lists the injected failures and which late ask each maps to.

- **Wild: A model that reads the user's frustration** — FEATURE — value 3 — effort M — risk med — category: tone (wild)
  Why: corrections in the steers ("never interrupt," "wild moonshots," "don't block") are stored as rules but are really signals of mood. Train a head on message-to-steer pairs that raises a flag when a session is repeating a thing the user already corrected.
  Done when: on a replayed session that re-asked a question, the flag fires before the second ask.

- **Wild: Trade weights as a compact "taste file" between the user's machines** — FEATURE — value 2 — effort M — risk med — category: portability (wild)
  Why: assumption: the user uses a laptop and this box. A small signed adapter plus calibration table moves the trained taste without moving any briefs.
  Done when: a second machine loads the file and reproduces the bench numbers within noise, with no ledger text in it.

Next question: Which of the user's late asks would a perfect decider have prevented, and how many are about verification, not decisions at all?
Next question: Does a model trained on this user's history make the other projects' outcomes worse, and how would we notice?
