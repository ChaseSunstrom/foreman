# Brainstorm — lens: bold bets

- **Run best-of-N Smith with the test suite as selector** — FEATURE — value 5 — effort M — risk low — category: agents
  Why: Smith's loops and false-done closes dominate (loops end 4 of 10 runs; gemma4:12b fixed 3/8). Selection at inference by real tests needs no training, and the winning runs feed the distillation set.
  Done when: on Louhi's train split, N=4 gemma4:12b in parallel worktrees, picked by tests, fixes strictly more scenarios than N=1, with the scorecard printed by `sampo exam`.

- **Constrain every typed decision to a grammar** — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: small deciders (4B) lose some of their 0.73 to malformed or off-schema output, and the reasoning-eats-budget failures show output control is shaky. JSON-schema or grammar decoding makes the parse-fail rate zero.
  Done when: a bench run reports parse failures as 0 for each `decide()` slot on the 200 held-out tasks, with accuracy no lower than before.

- **Measure each project's marginal value to each slot** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: 13 projects with very uneven sizes (1,767 briefs vs 59) and a per-project consent flag. Dropping each project in turn and re-benching tells the user what an exclusion costs and whether the big repos drown the small ones.
  Done when: a project × slot matrix of held-out accuracy deltas exists, and `sampo doctor` shows it next to each consent flag.

- **Mine disagreements between the 4B, 12B and 27B** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the models all run on this box. Cases where they split are the hard ones, so a small queue of those gets the user's or outcome labels where they matter most. Nothing beats majority on tier, and this finds why.
  Done when: a ranked "models disagree" list is produced from past briefs, and labelling the top 50 changes at least one slot's champion choice or is recorded as having changed none.

- **Plant canaries in the training lake and probe every artifact for them** — SECURITY — value 5 — effort M — risk low — category: privacy
  Why: a sensitive project's data must never leave the machine, and a stripped-name pass can't prove that. Unique synthetic strings in excluded projects, tested against each adapter before adoption, give a falsifiable leak check.
  Done when: an adoption card refuses any adapter whose generations reproduce a canary, and a test deliberately trains on a canary to prove the probe fails it.

- **Train a tool-output compressor from evidence runs** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: T-0828 (compact output rollout) is deferred, and 32k contexts on small models fill up with test logs. Evidence runs with exit codes show which lines the next action actually used.
  Done when: Smith with the compressor uses fewer prompt tokens on the train scenarios, with the fix rate no worse and every dropped span counted aloud.

- **Classify Smith failures into a taxonomy that steers the card grower** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: small-card growth is 0 so far, and 74 journals exist. A label for each ended run (loop, false-done, wrong file, reasoning overrun, context overflow) says which card to write next.
  Done when: all 74 journals carry a failure label, and the grower's next three cards each cite a label and its count.

- **Predict which tests a diff will break before running them** — PERFORMANCE — value 3 — effort L — risk med — category: speed
  Why: Sampo's suites are big (plugin/tests has 454 files) and the full suite gates every `fm ship`. Evidence runs pair diffs with exit codes. Assumption: enough failing runs exist for a usable signal.
  Done when: the predicted top-K tests catch at least 90% of real failures on held-out closed tasks, and the full suite still runs at ship time.

- **Publish Louhi-open, a leaderboard for small models on discipline** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: the exam already grades found, fixed, test-first and false alarms across 6 languages. A site page with the scenario generator and per-model rows turns an internal measure into the proof for "any model" on the landing page.
  Done when: the site page lists at least 3 models with a reproduction command, each row rebuilt from the exam output, not typed in.

- **Wild: Shadow-predict Claude Code's next tool call, evaluate only** — FEATURE — value 3 — effort M — risk med — category: observability
  Why: the Anthropic-output training restriction rules out learning from Claude's text, but comparing the local model's prediction to what happened needs no stored text. The hit rate is a free, continuous adoption signal for Smith.
  Done when: a session-path hook logs hit/miss counts per model with no Claude text persisted, and a test asserts that.

- **Wild: Keep an Elo ladder of models and scenarios together** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: Louhi has 18 runs on a few dozen scenarios, and a scenario every model passes or fails teaches nothing. Rating models and scenarios jointly retires the saturated ones and shows where to mint new ones, instead of a fixed set.
  Done when: each scenario has a difficulty rating, and a new Rune generation's exam adds the scenarios nearest the current champion's rating.

- **Wild: Give each adopted model a one-line voice in `sampo status`** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the web UI should show which slots use a model. A short plain-words line ("I'd have picked the second approach here; I'm 62% sure") per decision, saved with the brief, makes the models visible to the user and gives a free sample to correct.
  Done when: 20 consecutive decisions in a session each show a line, and the user's correction is stored as a labelled row.

- **Wild: Retrain the models on the previous generation's mistakes only** — PERFORMANCE — value 3 — effort M — risk med — category: training
  Why: every Rune generation retrains and re-benches, and full retrains compete with the moons funnel for one 16 GB GPU. Training on rows the last champion got wrong, with a replay sample, may cost a fraction of the time.
  Done when: an incremental run reaches within 1 point of a full retrain on the held-out projects in under a third of the GPU time.

Next question: which slot has the biggest gap between its best model and a human-labelled ceiling, so the first adoption goes there?
Next question: what does the model path do when the GPU is busy with the moons funnel, and is the fallback measured?
