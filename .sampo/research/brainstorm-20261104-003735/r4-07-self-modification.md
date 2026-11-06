# Brainstorm — lens: self-modification

- **Attribute every drive stop and failed tool call to the self-edits that preceded it** — FEATURE — value 5 — effort M — risk low — category: attribution
  Why: the top gaps (stops 0→0.1, failed tool calls up by half) arrived in the same window as T-2900, T-2901 and T-2873, which rewrote the drive's own counting. Nothing says whether Sampo's edits caused them. Assumption: each landed commit already carries a timestamp and a file list.
  Done when: `sampo why-stopped <stop-id>` prints the self-landed commits touching the drive or hooks in the prior 48h, and a replay of the last 10 stops names the right commit in at least 8.

- **Revert first when Sampo's own main goes red** — FEATURE — value 5 — effort M — risk med — category: self-repair
  Why: the standing push grant lets unattended work ship. A red `main` that gets investigated before it is reverted blocks every trigger-born lane overnight. Assumption: the red commit can be found by bisect.
  Done when: in a scratch repo with a planted bad self-landed commit, red CI triggers an automatic revert commit through `fm ship`, and the next night's lane starts from green.

- **Run one self-edit variable per night so outcomes can be attributed** — FEATURE — value 4 — effort S — risk low — category: experiment design
  Why: with many lanes landing edits, a change in the stops or failed-call rate can't be pinned to any one edit. The earlier "which gate was historically right" question has the same root. Assumption: edits are queued, not instant.
  Done when: the ledger shows at most one behaviour-affecting self-edit active per 24h window, and `sampo self log` marks each window's edit as the sole variable.

- **Learn least-privilege grants from trigger-born sessions** — SECURITY — value 4 — effort M — risk med — category: permissions
  Why: self-triggered sessions run unattended with the standing core yes. Assumption: the tool-use ledger records which tools each trigger kind actually used.
  Done when: after 10 runs of a trigger, `sampo trigger grants` proposes an allowlist equal to the tools used. Narrowing applies automatically, and widening is refused without the user's key.

- **Lint steer contradictions at the moment a steer is stored** — CLEAN — value 4 — effort M — risk low — category: steer integrity
  Why: the 80-odd standing steers already pull against each other, for example "never interrupt the user" against "say which cap only the user can raise once", or "tell the user" against "keep going". Self-added steers will multiply this. Assumption: steers are stored text with a check command.
  Done when: `fm decide --check` of a planted steer opposing an existing one prints both ids and refuses to store it without `--supersede`.

- **A/B trigger brief templates on alternating nights** — FEATURE — value 3 — effort M — risk low — category: self-tuning
  Why: a trigger starts work by handing a session a brief, and nothing measures which phrasing leads to closes that survive. Replaying old briefs doesn't catch live drift. Assumption: close survival at 14 days is the outcome signal.
  Done when: two templates for one trigger alternate nightly, and a ledger line per night shows survival rate per arm, with the loser retired after a preset sample.

- **Gate self-edit authority by the author model's tier** — SECURITY — value 4 — effort S — risk low — category: edit governance
  Why: the request asks for unlimited local-model volume, and a local 27B drafting edits to guard or drive files is a different risk from a frontier model doing so. Assumption: the author model is recorded on each lane.
  Done when: a local-model patch touching a protected path is refused without a frontier-model cold read, while one touching prose or data classes passes the normal gate.

- **Freeze self-edits when the host or model version changes** — FEATURE — value 3 — effort S — risk low — category: baseline drift
  Why: a host update shifts failed-call and stop baselines, so any edit judged against old baselines is mis-scored. Assumption: the host version is readable at session start.
  Done when: a faked host-version change holds self-edit landing for N nights and `sampo doctor` says why.

- **Classify the shape of self-edits that the user later reverted by hand** — FEATURE — value 3 — effort M — risk low — category: edit learning
  Why: the pack's earlier question asks what earlier self-edits that were hand-reverted share. Assumption: the hand-reverts are findable in git history.
  Done when: running the classifier over the last 200 commits lists the revert-prone shapes, and a new self-edit matching one is held for a morning yes.

- **Wild: shadow every frontier self-edit with a blind local patch** — FEATURE — value 3 — effort L — risk low — category: local models
  Why: it measures per edit class when the free lane could take over (assumption), so more self-repair can run without frontier spend. Wild.
  Done when: a report shows, per class, how often the local model's blind patch matches the landed one in replay, and classes above a set agreement are routed local-first.

- **Wild: make a different harness reproduce the symptom before a patch counts** — SECURITY — value 3 — effort L — risk med — category: cross-harness
  Why: the standing rule says Sampo isn't Claude-specific, and a fix verified only by the harness that wrote it is weak evidence. Wild.
  Done when: a self-fix for a stall closes only after a second harness (Codex, Gemini or opencode) is shown failing before the patch and passing after, or the close is marked single-witness.

- **Wild: hold a weekly self-edit sabbath to price self-modification** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: no data says whether self-edits improve outcomes on net, and the user wants overnight progress. Wild.
  Done when: on one night per week triggers run but no self-edit lands, and the morning card compares that night's yield and failure rate with the neighbouring nights.

- **Wild: let the legibility test be a small cold reader** — CLEAN — value 3 — effort M — risk low — category: edit review
  Why: a self-edit that a small tool-less model can't summarise correctly from its diff is probably too clever to trust. Assumption: a local model can do the summary. Wild.
  Done when: each landed edit has a stored one-line summary from the small reader, and a mismatch with the author's stated intent holds the edit for review.

Next question: Which of Sampo's own recent self-landed commits could already explain the new drive stops and failed calls, and could a replay prove it before we build more?
Next question: When a trigger-born session edits Sampo itself, who is allowed to undo it while the user is asleep?
