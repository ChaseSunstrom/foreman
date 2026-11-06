# Brainstorm — lens: self-modification: finders that learn from which findings were kept, proven or reverted, and improve their own probes, measured and reversible

- **Log every finding's fate against the probe version that made it** — FEATURE — value 5 — effort M — risk low — category: learning ledger
  Why: the exam found 0/108 planted defects, and nothing in the pack shows a record joining probe → finding → kept/dropped/reverted/survived (`fm outcomes` has 30-day survival only per task). Without it, no self-edit can be judged. Assumption: findings get a stable fingerprint.
  Done when: after a scripted scout run with one kept, one dropped and one reverted finding, `fm find fates` prints three rows, each naming probe id and version.

- **Store probes as versioned declarative files with one-command revert** — FEATURE — value 5 — effort M — risk med — category: probe format
  Why: probes live in fmscout.py/fmdocs.py code, so a self-edit would be a code change to Foreman. A small data format (pattern, scope, question, severity) lets edits be diffed, bounded, and unable to execute code. Assumption: most deterministic probes can be expressed as data.
  Done when: `fm probe revert <id>` restores the prior file and a test shows the rerun output matches the pre-edit output byte for byte.

- **Gate every probe edit on the held-out exam plus a clean-repo silence check** — FEATURE — value 5 — effort M — risk low — category: edit gate
  Why: the user steered "weakness-finding by outside signals only"; `fm exam` already has holdout scoring and `none` kind. An edit that raises recall but breaks silence on clean repos must lose. Assumption: exam runtime is affordable per edit.
  Done when: a mutation that adds a noisy pattern is rejected with "none-kind precision fell from X to Y" and the probe file is unchanged.

- **Turn each missed exam defect into a candidate probe, then re-score** — FEATURE — value 5 — effort L — risk med — category: miss mining
  Why: 0 of 108 found; the key lists each planted defect's file and kind. A proposer reads misses from the training two-thirds only and drafts probes; the holdout third decides keep or discard. Assumption: the overfit guard below holds.
  Done when: one command drafts probes from training misses, and the printed report shows the holdout recall delta with the training delta beside it.

- **Alarm when a probe encodes an exam literal** — SECURITY — value 4 — effort S — risk low — category: overfit guard
  Why: a self-improving finder scored on a fixed exam will memorise it. Scan probe files for identifiers, paths and strings that appear in exam repos, and fail the edit on a match. Assumption: exam repos are generated, so literals are distinguishable.
  Done when: a probe containing a planted-repo function name fails `fm probe check` with the match.

- **Roll back an edit automatically when its live precision drops** — FEATURE — value 4 — effort M — risk med — category: auto-revert
  Why: reverts are the loudest outside signal. Track kept-rate per probe version with a sequential test, and restore the previous version when it is below the older one's rate with confidence, plus a journal line saying why. Assumption: enough findings accrue per probe to test.
  Done when: simulated ledger data with a worsening version triggers one revert and an audit entry, and a stable version triggers none.

- **Cap self-edits with a budget and require minimum evidence** — SECURITY — value 4 — effort S — risk low — category: change budget
  Why: an unbounded self-editing loop can drift. Allow at most N edits per week, and none from fewer than K fated findings. Assumption: a conservative default of 1 edit a week and K=10 fits.
  Done when: a second edit in the same week or an edit from 3 fated findings is refused with the reason printed.

- **Measure each probe's value by switching it off for a night** — PERFORMANCE — value 3 — effort M — risk low — category: ablation
  Why: a probe's yield is confounded with others that catch the same thing. A switch-off night reveals the findings only it produced. Assumption: shadow runs don't touch user trees.
  Done when: a report lists unique proven findings per probe over an ablation window, and a probe with zero is flagged.

- **Write down why a retired probe died** — CLEAN — value 3 — effort S — risk low — category: tombstones
  Why: without tombstones a later proposer rediscovers a noisy pattern and files it again. Store the reason, the evidence and the fate counts; the proposer reads tombstones before drafting.
  Done when: a proposed probe matching a tombstone is rejected with the tombstone cited.

- **Scrub learned patterns of project literals before they cross repos** — PRIVACY — value 4 — effort M — risk med — category: cross-repo learning
  Why: a probe learned from one user repo could leak names or secrets into another's probe set and the Genesis site. Keep shapes (AST kind, call pattern), drop identifiers. Assumption: a generalised pattern keeps enough signal.
  Done when: a probe mined from a fixture repo containing a secret-named function contains none of its identifiers.

- **Wild: Draw the probe family tree on the Genesis page** — FEATURE — value 3 — effort M — risk low — category: visibility
  Why: the Genesis site already graphs the tower; showing probe lineage with kept/reverted colours makes self-modification legible. wild
  Done when: the exported page lists each probe version as a node with parent, fate counts and exam delta.

- **Wild: Run a probe dojo against the failure museum overnight** — FEATURE — value 3 — effort L — risk med — category: replay
  Why: replaying old reverted fixes and past planted defects as sparring partners lets candidate probes train when no user project is available. Assumption: a corpus of past failures is kept. wild
  Done when: a nightly run scores candidates against stored cases and writes a ranked list without touching any live probe.

- **Wild: Make probes stake a budget on their own findings** — FEATURE — value 3 — effort M — risk med — category: economics
  Why: each probe gets a spend allowance that grows when its findings survive and shrinks on drops or reverts, so the budget allocation itself becomes the learning. Probes at zero are retired. wild
  Done when: after simulated fates, the allowance of a reverted-heavy probe falls below a kept-heavy one's and a zero-allowance probe is skipped.

- **Blame the right stage before touching a probe** — FIX — value 4 — effort M — risk low — category: attribution
  Why: a reverted finding may come from a bad fixer or a flaky proof, not from a bad probe. Classify the revert (probe false positive, weak proof, wrong fix) from the failing-test record, and edit only for the first.
  Done when: three fixture reverts with different causes produce three different stage labels, and only the probe-caused one lowers the probe's score.

Next question: Does the pipeline have enough fated findings per week in a single user's projects for any statistical self-edit to fire, or must learning pool across repos (and then what is allowed to leave a repo)?

Next question: Who audits the proposer: if a self-edit passes the exam yet a cold reader judges the probe unreasonable, which signal wins?
