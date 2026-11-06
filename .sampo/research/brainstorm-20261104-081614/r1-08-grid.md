# Brainstorm — lens: grid

- **Ship a leave-one-project-out bench before any model is trained** — FEATURE — value 5 — effort M — risk low — category: measurement
  Cell: agent × wrong. Why: the pack's 0.73 intake score came from 200 held-out tasks drawn mostly from Sampo's own 1,767 briefs, so it says nothing about generality. The user wants a model that isn't Sampo-only.
  Done when: `sampo model bench` trains on 12 projects, scores the 13th, and prints per-project scores beside the majority baseline, with repo-specific names stripped. A model that doesn't beat majority on at least the held-out projects it was never trained on is not adopted.

- **Add a per-project training opt-out the collector enforces** — SECURITY — value 5 — effort S — risk low — category: privacy
  Cell: unattended × unsafe. Why: the pack says a sensitive project's data never leaves the machine and may be excluded from training. Nothing visible enforces that at collection time.
  Done when: a project marked `train: never` contributes zero rows to the dataset build, a test seeds a canary string in it, and the string is absent from every shard and every embedding index.

- **Train only on text the user or a tool wrote, never on repo or web content** — SECURITY — value 4 — effort M — risk med — category: poisoning
  Cell: unattended × unsafe. Why: this answers the left-over question about whether the Ward and the funnel's local models share a text channel. Ledgers and briefs quote file contents and tool output, so an injected line in a repo can reach a trained head.
  Done when: every training row carries a provenance tag (user, tool-verified, model, external). A planted "ignore the Ward" line in a fixture repo's README never appears in the built set. External-provenance rows are dropped or masked.

- **Label rows by outcome: done-and-held versus reverted or later-fixed** — FEATURE — value 5 — effort M — risk low — category: data
  Cell: agent × wrong. Why: briefs record done, blocked or reverted outcomes plus "later fixes", and Anthropic's terms make outcomes safer training data than Claude's own text. A decider trained on "closed" rather than "held" learns to copy false-done closes, which the 12B uplift run already shows.
  Done when: the dataset builder emits a `held` label (not reverted, no later-fix link within N tasks). A report shows the share of closed briefs that fail it, per project.

- **Give `decide()` a trained head that abstains, with the rules as fallback** — FEATURE — value 4 — effort M — risk low — category: decider
  Cell: agent × missing. Why: only intake type beats majority (0.73 vs 0.595); tier does not (0.58). A head should answer only where calibrated and say nothing otherwise, and the existing `decide()` path already calls it.
  Done when: for each slot, `decide()` uses the head only when its held-out accuracy at the chosen confidence exceeds the baseline. Tier stays on the current path. A log line records each abstain.

- **Keep a per-slot champion registry with shadow mode and rollback** — FEATURE — value 5 — effort M — risk med — category: adoption
  Cell: unattended × wrong. Why: the constraint is "adopted only where the bench shows it leads, retrained every Rune generation." That needs a place where champions live and a way to fall back.
  Done when: each Rune generation retrains, runs the candidate in shadow beside the champion for N decisions, and promotes only on a bench win. `sampo model rollback SLOT` restores the previous champion in one command.

- **Ship a retrieval-only baseline first: "briefs like this one", via bge-m3** — FEATURE — value 4 — effort S — risk low — category: zero-train
  Cell: agent × missing. Why: bge-m3 title-to-brief recall@1 is 0.85 already, so a kNN over closed briefs from all projects needs no training. Surfacing prior approaches, criteria and lessons at `fm next` and intake is the cheapest generic win, and it is a path a session already takes.
  Done when: intake and `fm next` show the top 3 similar closed briefs from any project with their outcomes. The test measures how often the chosen approach matches a held-out neighbour's.

- **Distil Smith's actor from verified runs, with loop runs kept as negatives** — FEATURE — value 4 — effort L — risk med — category: Smith
  Cell: other agents × wrong. Why: loops are the main end of runs (4 of 10), and the 74 journals hold every model message and tool call. Keeping only green-test, held-close runs as positives and loop-broken runs as explicit negatives teaches the avoidance the loop breaker currently forces from outside.
  Done when: on Louhi's held-out scenarios, the tuned 4B or 12B beats its untuned self on found and fixed counts and has fewer loop ends, with false-done closes no higher.

- **Schedule training in idle-GPU windows that yield to Ollama and resume** — PERFORMANCE — value 3 — effort M — risk med — category: training ops
  Cell: unattended × slow. Why: one 16 GB card also serves the exam and the decision models, and a 27B model switch costs about 3 minutes. A LoRA on a 0.6–4B model must not starve those.
  Done when: a training job pauses when an Ollama request arrives, resumes from checkpoint, and `sampo model status` shows progress. A test kills it mid-run and it finishes with the same final loss within tolerance.

- **Show each slot's model in the web UI with its bench and every abstain reason** — FEATURE — value 3 — effort M — risk low — category: transparency
  Cell: user × unclear. Why: web UI is the one listed surface, and the user is often away. They need to see which decisions a model made, its bench versus majority, and why it declined, without asking.
  Done when: the UI has a Models panel listing slot, champion, held-out score, baseline, shadow-win count and last 20 decisions with confidence. The panel renders with no model installed.

- **Wild: Predict the user's steer before they give it** — FEATURE — value 4 — effort L — risk med — category: foresight
  Cell: user × missing. Why: 150k ledger lines hold steers, asks and answers, and foresight already predicts the next request. A model trained on the user's accept and reject history across all 13 projects could pre-draft the answer to a recurring ask. Assumption: the user would accept pre-answered asks, with a visible trail.
  Done when: on held-out ask events, the prediction matches the user's real answer above the majority rate, and a wrong prediction never acts without the usual grant.

- **Wild: Train an adversary against the Ward and let the Ward learn from it** — SECURITY — value 4 — effort L — risk high — category: red team
  Cell: other agents × unsafe. Why: this takes up the question of what holds if a strong attacker reads Sampo's open rules. A local model proposes risky commands that dodge the rule text. Every one the Ward misses becomes a rule and a test.
  Done when: a nightly run produces N attempts, each miss is filed as a failing Ward test, and the rule count rises only when the new tests pass. The attacker model runs locally with no tools.

- **Wild: Transfer lessons between projects as embeddings, with no raw text shared** — FEATURE — value 4 — effort L — risk med — category: lessons
  Cell: agent × missing. Why: volt (773 briefs) and Sampo (1,767) learned things the git tool (143) and the game (59) never will. Lessons embedded and tagged by stack and kind could reach small projects without moving briefs between them.
  Done when: a small project's task retrieves a lesson from another project only when it is stack-matched and marked shareable, and the held-out outcome improves compared with no transfer.

- **Wild: Rank each Rune generation by how well it predicts the previous generations' decisions** — CLEAN — value 3 — effort M — risk low — category: forgetting
  Cell: unattended × wrong. Why: every generation retrains, so regressions on older projects are likely. A frozen "canary" set from each generation guards against forgetting.
  Done when: the retrain fails the gate if accuracy on any earlier generation's canary drops more than a set margin, and the failing slice is named.

**Cells left empty:** user × slow (nothing the user waits on) and user × unsafe (the Ward and the grants already stand there). Agent × slow is covered by the retrieval baseline. Other agents × missing is covered by Smith distillation, and unattended × unclear by the UI panel.

Next question: Which of the 13 projects has outcome labels (reverts, later fixes) reliable enough to train on, and does the held-out win survive after dropping the two biggest projects?
Next question: If a trained head and a Ward rule disagree on a command, which one wins, and does any ledger show a case that settles it?
