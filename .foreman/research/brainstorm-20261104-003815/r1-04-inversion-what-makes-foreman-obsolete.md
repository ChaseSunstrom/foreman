# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Run a keystone matrix over pairs of capabilities** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the ideas so far ablate one capability at a time, but ecology says removal effects are interactions: a keystone's loss cascades, a passenger's loss doesn't. Pairwise runs on the free arms are cheap.
  Done when: `sampo louhi ablate --pairs` prints a capability-by-capability matrix from the zero-token arms, names at least one keystone (removal flips 2 or more other cells) and lists the passengers (flip nothing).

- **Ledger each funnel stage's unique kills** — PERFORMANCE — value 5 — effort S — risk low — category: moons funnel
  Why: the funnel is cheap-first over 10,000 candidates, but nothing shows which stage rejects what no later stage would have. Stages that never reject anything unique are overhead. Assumption: the funnel log already records per-stage verdicts.
  Done when: `sampo genesis moonshot funnel --uniques` lists, per stage, the candidates only that stage killed. A stage with zero over 1,000 candidates is flagged skippable, and the skip is logged.

- **Alarm when the candidate pool's diversity collapses** — FEATURE — value 4 — effort M — risk low — category: moons funnel
  Why: 10,000 bulk candidates from one local model (qwen3.8-27b is used first) tend to converge on the same few shapes. The user's complaint that the moons "aren't even that moon-y" is the felt symptom.
  Done when: each funnel run reports a Shannon diversity index over the families (embedding clusters). Below a set floor, it injects a far-domain lens seed and re-draws, and the log records the before and after index.

- **Dedupe candidates against a fossil record with wake predicates** — FEATURE — value 4 — effort S — risk low — category: moons funnel
  Why: not-yet.md holds failed spikes with blockers, but nothing stops 10,000 fresh candidates re-proposing them. The standing rule says retry only when a new capability unblocks, which needs a machine-checkable predicate.
  Done when: the funnel's first stage matches candidates to not-yet entries by embedding. A match is dropped unless the entry's blocker predicate now evaluates true, in which case it is promoted with a "retry" tag.

- **Retry not-yet moons on a new model ID** — FEATURE — value 4 — effort S — risk low — category: moons / models
  Why: the standing rule says every Seed retries items a new capability may unblock, but only the Ward exam re-runs when a stronger model appears. Many blockers read "model too weak", and Fable 5.1 and Opus 5.5 are already in the environment. Assumption: blockers carry a coarse "needs: model" tag.
  Done when: adding a new model ID to the profiles queues every not-yet entry tagged `needs: model` for one spike on it. Each result is written back as pass, or fail with a second approach recorded.

- **Alarm when an exam family saturates** — FEATURE — value 4 — effort M — risk low — category: exam integrity
  Why: if the plain arm reaches the same ceiling as the Sampo arm on a scenario family, that family can't show lift any more, so the exam can't tell "Sampo is obsolete" from "the exam is spent".
  Done when: `sampo exam scorecard` marks a family "saturated" once the plain arm is within a set margin of the ceiling over N runs. It then files a task for a tool-less child to author harder scenarios without seeing Sampo's code.

- **Plant a contamination canary in the public Genesis data** — SECURITY — value 4 — effort S — risk low — category: exam integrity
  Why: the site publishes Genesis data on every tower change, and future models may train on it. Held-out exam scenarios and steers that leak into training would make the plain arm look better.
  Done when: each held-out scenario carries a unique canary string that is never published. A check scans the site build and the repo's public files for any of them and fails the publish if found.

- **Test local models for staying power per resident minute** — FEATURE — value 3 — effort M — risk low — category: local models
  Why: a model switch costs about 3 minutes, and Sampo hosts several profiles. Without a verdict, a model that has been outclassed keeps its slot and its switch cost.
  Done when: `sampo louhi models` prints, per profile, accepted outputs on closed tasks per resident minute (switch cost included) next to the best alternative. A profile that loses for N weeks is moved to dormant with a wake predicate, never deleted.

- **Wake dormant capabilities on a quorum of signals** — FEATURE — value 3 — effort S — risk low — category: lean / quorum sensing
  Why: auto-dormant mode is proposed, but waking on one trigger would flap. Ecological quorum sensing wakes a capability only when independent signals agree.
  Done when: a dormant capability wakes only when at least 3 distinct signals land inside a window (for example a user correction, a failed proof, a host release note). The wake log names the 3.

- **Run fallow generations when novelty yield drops** — wild — FEATURE — value 3 — effort M — risk med — category: genesis cadence
  Why: assumption: later generations yield fewer accepted ideas per Mission. Crop rotation says to rest a field before it exhausts. A generation that only deletes, audits and re-measures keeps the tower advancing without growth.
  Done when: after yield falls under a configured knee for 2 generations, the next Seed is auto-marked fallow. It files only subtraction, exam and subtraction-audit tasks and reports the yield it saw.

- **Transfer a retired capability's lessons to its neighbours** — wild — FEATURE — value 4 — effort M — risk med — category: lean / mycorrhizal
  Why: retiring a capability today loses what it learned. In a mycorrhizal network a dying tree passes its carbon to the others. Small-model cards (T-2909) are a ready receiving store.
  Done when: retiring a capability moves its recurring lessons and failure shapes into the cards of the capabilities that call it. Each moved row is tagged `from: <retired>`, and a held-out check shows no card grew past its size cap.

- **Run a perfect-model arm to find what stays valuable** — wild — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: obsolescence comes as models improve, so test it ahead of time. Give the plain agent the scenario's answer key as a hint and see what Sampo still adds. What survives (intent capture, outward-action guards, the Ward, clause proof) is the climax community that models can't replace.
  Done when: `sampo exam run --arm oracle-hint` runs plain-with-hint beside Sampo on the held-out set. The scorecard lists the capabilities whose lift stays above zero, labelled "model-proof".

- **Burn one capability in a clone and watch what regrows** — wild — FEATURE — value 3 — effort M — risk med — category: lean / succession
  Why: static ablation shows what breaks, not what the host or other capabilities fill in over a week. A burnt plot shows who recolonises it.
  Done when: a weekly lane deletes one capability in a throwaway clone, runs a week of replayed sessions, and writes a report saying whether the gap was filled by another verb, by the host, or left open.

Next question: which of Sampo's published claims would still be true if the plain arm used the best model that exists in a year, and what in the repo records that bet?
Next question: whose job is it to notice the day a capability's lift crosses zero, and does that action need the user at all under the standing push grant?
