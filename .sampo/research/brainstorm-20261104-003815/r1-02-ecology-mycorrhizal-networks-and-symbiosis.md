# Brainstorm — lens: ecology: mycorrhizal networks and symbiosis

- **Inoculate a new repo from its nearest kin** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: assumption: first sessions in a new repo start cold. Forests seed seedlings with fungus from the parent soil. Sampo can find the user's most similar repo by stack card and gate set. It would copy over only the verified conventions, the gate commands and the not-yet traps, each marked "inherited, unconfirmed".
  Done when: in a fresh repo with a Python stack, the first `sampo` session lists at least 3 inherited items with their source repo, and each flips to "confirmed" or is dropped after one use.

- **Flow lessons along a gradient between repos** — FEATURE — value 4 — effort M — risk med — category: cross-repo
  Why: T-0217 gives lessons a confidence, and the pack shows no path for a lesson to reach another repo. Lessons move from repos rich in confirmed lessons to repos with few, but only where co-use edges (same stack, same failing gate) exist. Nothing moves along an edge with no evidence.
  Done when: a lesson confirmed in repo A appears in repo B's recall within one session, and a repo with no shared stack receives none.

- **Prime sibling lanes with a distress signal** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: assumption: parallel lanes (Missions 5-8) fail on shared causes one at a time. Plants under attack release signals that make neighbours raise defences before they are hit. When a lane hits a new failure class, such as a worktree state split, it writes a 200-character shape-only signal. Other live lanes pre-run the cheap check for that class at their next tool boundary.
  Done when: with two lanes running, a planted failure in lane 1 makes lane 2 run the matching check within one tool call, and no signal contains source text.

- **Rate each local model as a symbiont, with a cheater cut-off** — FEATURE — value 4 — effort M — risk low — category: local models
  Why: the model bench (T-2887/2894) measures accuracy but not the exchange. Each decision model gets a two-column record: what it saves (frontier calls avoided, minutes) and what it takes (hard-case relabels, GPU swap time, rerun failures). A model that takes more than it saves for N weeks is demoted to shadow. Plain give/take counts only, no money.
  Done when: `sampo louhi models` prints give and take per model, and a planted always-wrong model is demoted automatically.

- **Grow the 10,000-moon funnel by flux, not by rank** — FEATURE — value 5 — effort L — risk med — category: moonscale
  Why: the request is cheap-first funnel plus families. Physarum-style allocation fits it: each candidate starts as a thin tube. Every independent reinforcement, whether a lens that re-derives it, a different-family model that scores it wild ≥4, or a cold dedupe that finds no neighbour, thickens it. Spend goes to the thickest tubes, and tubes unreinforced for K rounds are pruned with the reason recorded. This keeps the standing rule that nothing is killed for ambition, because pruned means "not-yet" with a blocker.
  Done when: a 1,000-candidate synthetic run ends with spend concentrated in the top 10% of tubes, every pruned candidate carries a recorded reason, and a planted wild-5 candidate with one strong reinforcement survives.

- **Pair two weak models as a lichen** — FEATURE — value 4 — effort M — risk low — category: local models
  Why: the small-model uplift work (T-2908/2909) runs Smith on one local model at a time. A lichen is a fixed pair: one drafts, a second family verifies against the Exam. The pair is scored as one organism in the exam scorecard, beside each member alone and beside the frontier.
  Done when: `sampo exam run --agent smith --pair A,B` prints a single row, and the pair's pass rate is reported against both singles.

- **Set ceremony by repo succession stage** — FEATURE — value 3 — effort M — risk med — category: user value
  Why: T-1266 sets ceremony by task kind and model only. Young repos (few commits, no gates) are pioneer ground, so they get only Ward and prove. Mature repos with gates and CI get the full plan, prove and done-gate. Stage is derived from commit count, gate count and churn, and shown once.
  Done when: a new repo with no gates gets Lite ceremony, the same repo after 3 gates are found gets full ceremony, and `doctor` names the stage.

- **Census orphans in the ledger web** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: assumption: lessons, cards and not-yet items link to each other, but nothing checks the links. `sampo doctor` counts lessons never recalled, tasks with no lesson edge and cards no session read. It reports them as a single connectivity percentage.
  Done when: doctor prints orphan counts per ledger, and linking one orphan lowers the count by one.

- **Wild: show a soil view in the web UI** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Sessions and lanes appear as mushrooms above a line. Beneath it, the lesson, card and ledger edges between them glow when recalled and dim when idle. Reduced-motion users get a static, labelled graph.
  Done when: the page renders from real ledger data, a recall event brightens its edge within 1s, and the same view works in reduced-motion mode.

- **Wild: federate failure shapes between Sampo installs** — SECURITY — value 3 — effort L — risk high — category: privacy
  Why: wild, a wood-wide web between users. Off by default, each install can publish only salted hashes of false-done signatures and Ward-bypass shapes, never text or paths, and ingest others' hashes as read-only hints. The user sees the exact bytes before the first send.
  Done when: with the setting off, a packet capture shows zero egress. With it on, a planted signature hash is received by a second install, and the preview shows the exact payload.

- **Wild: let one dying lane leave nutrients** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: wild, a mother tree's dying nutrient release. When a lane is killed, usage-limited or crashed, a decomposer step first writes its "tried and failed" list, partial evidence and file touches to a handoff the next lane on the same task family reads first. Today partial work is only "kept by lane resume".
  Done when: a killed builder's next lane starts with the dead lane's tried-and-failed list, and its first action skips at least one recorded dead end.

- **Wild: gate moon families by quorum** — FEATURE — value 4 — effort M — risk med — category: moonscale
  Why: wild, quorum sensing. A family of moons (a cluster by embedding) is promoted to a full mission only when at least 3 independent lens models, from at least 2 model families, have each emitted a member. This turns "many cheap local guesses" into a signal that cheap rank alone can't give, and a lone idea stays in not-yet with its blocker.
  Done when: a synthetic family with votes from 2 families is held, one with 3 lenses across 2 families promotes, and the log shows each vote's source.

Next question: which of these exchanges are already visible in the ledgers, so a give/take record could start with zero new instrumentation?
Next question: what would the user see if two repos had a lesson that contradicted each other?
