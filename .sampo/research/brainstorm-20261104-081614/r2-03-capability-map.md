# Brainstorm — lens: capability map

- **Force every decider slot through a grammar** — FEATURE — value 5 — effort S — risk low — category: reliability
  Why: Small models die on format and budget (gemma4:12b ran out of tokens on 7 of 10 exam scenarios; loops end 4 of 10 runs). Outlines, llama.cpp GBNF and vLLM guided decoding make invalid output impossible. Assumption: the Ollama and remote endpoints accept a JSON schema.
  Done when: 200 held-out `decide()` calls on qwen3.5:4b return 0 unparseable outputs, and a schema-violation counter is in the ledger.

- **Compile slot prompts against the bench before training weights** — FEATURE — value 4 — effort M — risk low — category: prompt optimisation
  Why: DSPy/MIPRO-style search costs no GPU training. The best intake type is 0.73 against a 0.595 majority, so there is room for prompt gains. It shares the leave-one-project-out bench.
  Done when: an optimised prompt beats the hand-written one on whole-project holdout by a recorded margin, or `sampo` records "no gain" and keeps the old one.

- **Join every model call to its eventual outcome** — FEATURE — value 5 — effort M — risk low — category: observability
  Why: Langfuse-style tracing, but the label arrives at task close (done, held, reverted, later fixed). Drift and the adoption card then use live accuracy per slot and project, not only the offline bench. Assumption: calls can carry a task id.
  Done when: after a task closes, every model call made during it shows in the slot scoreboard with its outcome, and a test asserts the join.

- **Predict the files a brief will touch** — FEATURE — value 4 — effort M — risk low — category: retrieval
  Why: Pairs of brief text and changed files exist for 4,078 briefs in git. It feeds Smith's context pack and blast radius (T-0788), and works on any repo with history. Cursor and Copilot do the equivalent with next-edit models.
  Done when: recall@5 on a held-out project beats a BM25/grep baseline.

- **Score whether a criterion's verify command is vacuous** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: Many false-done closes come from commands that pass without the change. `sampo task prove` records fail-before results as free labels.
  Done when: a classifier on held-out projects reports AUC against prove outcomes, and `task` warns on high-vacuity criteria.

- **Audit label noise in the briefs** — CLEAN — value 3 — effort S — risk low — category: data quality
  Why: A Cleanlab-style pass matters because the false-done and survival heads train on "done", which includes closes that didn't hold.
  Done when: on a copy with 5% planted flipped outcomes, the top 10% of the ranked list recovers at least 70% of the flips.

- **Weak-label the 149k ledger lines** — FEATURE — value 4 — effort M — risk med — category: data
  Why: Refusals, reverts, answered asks and steers are labels hiding in the ledger. Snorkel-style labeling functions grow the training set well past 4,078 briefs. Assumption: the labeling functions' noise stays below the briefs'.
  Done when: label-model accuracy on 100 hand-checked rows is reported per function, and rows from the sensitive-project exclusion are provably absent.

- **Queue label requests for when the user returns** — FEATURE — value 4 — effort S — risk low — category: active learning
  Why: The user is away and nobody may ask questions, but the final report is read. A ranked list of uncertain cases as yes/no cards (Argilla-style) turns idle time into labels.
  Done when: the report holds at most 10 cards, answers are stored as labelled rows, and the next retrain consumes them.

- **Write a flip report between Rune generations** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: Scores hide what changed. Run generation N and N-1 on the same historical decisions and list the disagreements with the brief and the later outcome.
  Done when: each generation's report lists its top 20 flips, and the web UI shows them.

- **Choose quantisation and context per slot from the bench** — PERFORMANCE — value 3 — effort S — risk low — category: serving
  Why: One 16 GB card has to hold the Ollama models while the funnel runs. gemma4:12b already needed a 32k setting by hand.
  Done when: a table of quant × context × accuracy × tokens/s exists per slot, and slot config selects a Pareto point.

- **Train an output compactor on what was later cited** — FEATURE — value 4 — effort L — risk med — category: context
  Why: T-0828 (compact output rollout) tracks fetch-back. Lines that Smith or Claude later quoted or acted on are free labels for which output matters.
  Done when: at 4× compression, the fetch-back rate is below head/tail truncation on the same sessions.

- **Mint Louhi scenarios from lessons (wild)** — FEATURE — value 4 — effort M — risk med — category: evaluation
  Why: The lessons store records what went wrong. Turning each into a replayable scenario makes every lesson a regression test, and a lesson that doesn't change an outcome is shown to be dead weight (links to T-0217).
  Done when: for 20 lessons, the scenario fails without the lesson recalled and passes with it, or is flagged inert.

- **Train a draft model for Smith's tool-call dialect (wild)** — PERFORMANCE — value 3 — effort L — risk high — category: serving
  Why: The 27B has two sessions, and tool-call JSON is very predictable (74 journals). Speculative decoding is lossless. Assumption: the remote endpoint supports a draft model, which is unverified.
  Done when: tokens/s rises on a fixed Smith replay with byte-identical outputs.

- **Write close receipts with a local model, checked against evidence (wild)** — FEATURE — value 3 — effort M — risk med — category: legibility
  Why: T-0795 wants plain receipts. Each claim must trace to an evidence line, which makes a hallucinated receipt a failing test.
  Done when: every close prints a 2-line receipt, and a test confirms each claim matches a ledger evidence row.

Next question: Which slot's wrong answer is cheapest for the user to catch, so the first adopted model goes there?
Next question: Does any retrain input come from text a project's own files could have written, and is that channel tested?
