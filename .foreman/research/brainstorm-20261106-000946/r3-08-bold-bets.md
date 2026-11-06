# Brainstorm — lens: bold bets

- **Retire `sampo decide` when it stops earning, then re-earn it per slot** — FEATURE — 5 — L — risk med — governance
  Why: Steer "Sampo isn't specific to Claude Code" + "the tower advances itself" + "lean substance: growth with no measurement waits." A permanent zero-model kNN arm already exists in the ideas; the bet is to make the *model* the one that must prove it, not the default. No capability is killed without evidence, and the model's retirement is itself a ledger event the user sees.
  Done when: `sampo doctor` prints "decider arm: kNN (model retired 2026-12-01, re-earned threshold not met)" and a shadow model beat the oracle on 3 consecutive Rune benches before re-adopting.

- **Let the user veto an entire *class* of decisions, not one item** — FEATURE — 5 — S — risk low — user-surface
  Why: "Let the user veto a class of Sampo behaviour" already appears, but nobody wired it to the *trained* decider: the veto becomes a training negative for that slot's head, so one "never decide my closes" permanently reshapes the close-holds verifier without a retrain cycle. This is the "you told me once" receipt, but for the model's own confidence.
  Done when: `sampo decide veto close-holds` removes the head from the close path, files a standing-rule line, and the next `sampo decide train` excludes close-holds negatives from that head's loss.

- **Federate *regret*, never weights, across the user's own machines** — FEATURE — 5 — L — risk med — privacy
  Why: "Many sessions, one repo, many machines, no duplicates or drift" is the user's explicit ask; "keep data on the owner's hardware" is a standing rule. Each machine holds its own outcome lake; only the *regret labels* (which brief was undone, which close broke) travel, as a tiny gradient over a frozen embedding. No brief text, no repo names, no tool output ever leaves a box.
  Done when: `samo federate --peer box2` syncs only the regret vector; a diff of both boxes shows zero raw text in the sync dir, and the merged head beats each local head on the union holdout.

- **Make the decider the *next user*: it drafts the steer you'll give tomorrow** — FEATURE — 5 — M — risk med — anticipation
  Why: "We will want it to be a generic model… maybe brainstorm on features the model should have" + the user's standing intent to "manage all of that across sessions… even without direct access." The model reads the last 30 days of pushbacks and files a *draft* steer ("I think you'll want X next") that the user can accept, edit, or strike in one keystroke. A struck draft is a negative for the user-twin head.
  Done when: the morning card shows one drafted steer with its evidence (3 recent asks); accepting it files the steer with provenance "drafted by decider, accepted 2026-12-01"; striking it logs a negative and the model's confidence for that class drops.

- **A "Sampo is gone" morning: disable the whole model layer for one live session, every week** — FIX — 5 — S — risk low — blind-spot
  Why: "The only head-to-head on record is bench duel 2026-10-16" and "weakness-finding uses signals Foreman didn't author." The strongest signal that the decider earns its place is what the user *has to do by hand* when it's absent. This is the "no model" arm made human: a live, logged, reversible experiment that produces the real "I had to type this twice" shelf.
  Done when: `samo ghost --once` turns off every trained head for one session, logs every manual decision the user made, and the next morning card prints "you did N things by hand; the decider would have handled M of them."

- **Ship the decider as a *readable rulebook* the user edits, not a black box** — FEATURE — 5 — L — risk med — transparency
  Why: "The model is the next user, not a helper" + "no idea is killed for ambition." Compile every trained head's top-20 decision boundaries into a versioned `samo/rules/decider.md` with one rule per line ("if brief repeats same action 3× → escalate"). The user edits a line; the next retrain treats it as a hard constraint (a Lagrangian term, not a prompt). The model stays generic; the *rules* are the per-project taste.
  Done when: editing one line in `decider.md` and running `samo decide train` changes the head's output on that class without touching weights directly; the diff of the rulebook is the only "taste file" that ships.

- **Train the decider *only* on the user's undo, and nothing else** — FEATURE — 5 — M — risk low — labeling
  Why: "Use the user's own undo as the only label" + "the model's job is to predict it." Every close, every steer, every draft that the user later reverts, edits, or contradicts is a negative. The positive is "the user did not touch it for 14 days." No hand-labeling, no LLM-as-judge, no repo-text contamination. The training set is exactly the user's own behavior, generic across every Sampo project because undo is a universal signal.
  Done when: the outcome lake's schema has exactly two label sources: `user_undid` and `user_left_14d`; a `samo decide train --dry-run` prints "N rows eligible, 0 from tool output, 0 from repo text."

- **Make every model verdict a *git object* the user can diff and replay** — CLEAN — 5 — M — risk low — provenance
  Why: "The model is a git object, not a model file" + "make every model call a replayable, content-hashed ledger line." A verdict is stored as a small JSON blob in the repo's object store, referenced by hash from the task ledger. `samo decide replay T-3100` shows the exact brief, the model's one typed sentence, the abstain reason, and the outcome that followed. This makes the decider auditable by the cold Haiku read already required for every tower file.
  Done when: `git cat-file -p <verdict-hash>` returns the verdict JSON; `samo decide replay T-3100` prints it; a cold read can quote the verdict's line and name the gen-0 MUST it satisfies or breaks.

- **Let the decider *refuse the work* and be paid for saying "no"** — FEATURE — 4 — S — risk low — wild
  Why: "Let the model refuse the work, and pay it for saying 'no'" — the bet is that the most valuable decision is *not doing* something. The decider's abstain is not a failure; it's a first-class receipt with a confidence and a one-line reason. A correct abstain (user confirms "yeah, skip that") is a *positive* training signal. The metric becomes "abstain precision," not just accuracy.
  Done when: the morning card shows "decider abstained on 3 of 5 briefs; you confirmed 3/3 were correct" and the abstain precision is printed in `samo doctor` beside accuracy.

- **A "model autopsy" lane: replay every silent fallback from the last 7 days** — FEATURE — 4 — M — risk med — measurement
  Why: "Run the decider's mistakes overnight and file the regrets" + "name the fallback that fired, and why." A nightly lane replays every decision where the model fell back to rules (stall, timeout, low confidence) and asks: would the rules arm have done better? Disagreements are filed as regrets. This is the "measure the fallback" bench, made continuous, and it's the only way to find the slot that "has never left a ledger trace."
  Done when: `samo decide autopsy` prints "7-day fallback rate: 12%; 3 disagreements filed as regrets; slot close-holds had 0 traced abstains (gap)."

- **Cold-start a new project by *project fingerprint*, zero-shot, in minutes** — FEATURE — 4 — M — risk med — genericity
  Why: "Prove genericity with a canary project the user never built" + "seed a new project from its nearest siblings." A new repo is embedded once (bge-m3 over its file tree, not its text); the nearest 5 sibling projects' closed briefs are retrieved as few-shot priors. The decider answers with "I've seen 3 projects like this; here's what usually holds and what usually breaks." No training, no weights, pure retrieval over the user's own outcome lake.
  Done when: `samo decide init new-repo/` prints "fingerprint matched 3 siblings (sampo, my-weather-app, blog-engine); top predicted close-holds risk: 'guard path after migrate'" within 5 seconds, offline.

- **A "decider obituary": the model writes its own retirement when a slot stops earning** — CLEAN — 4 — S — risk low — wild
  Why: "Give each adopted model a one-line voice" + "growth whose capability has no measurement waits." When a slot's shadow score falls below the zero-model arm for 3 consecutive Rune generations, the model itself (the 0.6B, not the user) writes a one-line obituary: "close-holds verifier retired 2026-01-15: kNN beat it by 0.07 on holdout; 14-day undo rate was the real signal all along." The obituary is filed as a standing rule. This is the tower advancing itself, applied to the model's own existence.
  Done when: a retired slot's `samo decide status` prints the obituary; re-enabling it requires beating the kNN arm on the current holdout, not just a config flip.

- **Let the decider draft the user's *next bad week* and pre-stage the fix** — FEATURE — 4 — L — risk high — wild
  Why: "Bet on predicting the user's next bad week and pre-stage the fix" + "the model is the next user." The user-twin head doesn't just predict the next steer; it predicts the next *frustration* — the "I didn't ask for that" that comes 3 days from a specific class of close. It pre-stages a one-line patch or a "skip this" suggestion in the queue, flagged "pre-staged by decider, auto-reverts if you don't confirm within 48h." A pre-staged fix that the user confirms is a strong positive; one they ignore is a negative for the frustration head.
  Done when: the morning card shows "pre-staged: skip the weekly sync task (predicted annoyance from 3 similar closes); confirm or auto-revert in 48h"; confirming files the skip; ignoring logs a negative and the prediction's confidence decays.

- **Run the funnel as a *decision problem* the decider solves, not a ranker it feeds** — FEATURE — 4 — L — risk med — architecture
  Why: "Moons promote writes a lead's Domain as plain words" + "more and better ideas per hour." Instead of the decider scoring or ranking the 10,000-moon funnel, it *decides the stage transitions*: kill, tier, promote, merge — as typed verdicts with abstain. Each verdict is a git object. The funnel becomes an orchestrator with the decider as its judge, and the zero-model arm is "kill everything, promote nothing" (a hard floor). This is the "agents of agents" lens applied to the funnel itself: the decider is the specialist, the generator is the orchestrator.
  Done when: `samo funnel run --judge decider` produces stage verdicts as git objects; `samo funnel run --judge rules` (zero-model) produces the same stages with a different verdict distribution; the diff is the decider's marginal value, printed as "decider changed 12 of 400 stage decisions; 9 of 12 were confirmed correct by the outcome lake."

- **A "taste file" that is the *only* per-project state the decider holds** — CLEAN — 4 — M — risk low — privacy
  Why: "Show the user's own hand-edits as a 'taste file' Sampo reads before drafting" + "keep data on the owner's hardware." One small file per project: a few hundred lines of "user preferred X over Y in context Z," mined from the user's edits, undos, and steers. The generic base model is frozen and shared; the taste file is the *only* thing that differs per project. It's readable, diffable, and portable. "Federate regret, never text" becomes "federate the taste file's *deltas*, never its lines."
  Done when: `samo taste show` prints the file; a new project inherits the base model plus its own 20-line taste file; a diff between two projects' taste files shows no overlapping raw text, only delta vectors; the file is under 10 KB.
