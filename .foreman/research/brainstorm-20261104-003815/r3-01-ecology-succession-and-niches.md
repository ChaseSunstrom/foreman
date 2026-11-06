# Brainstorm — lens: ecology: succession and niches

- **Promote Ward rules through successional stages** — SECURITY — value 4 — effort M — risk low — category: Ward lifecycle
  Why: assumption: new Ward rules ship at full strength, and the pack shows the "retry-after-block" and rule-regret concerns without a lifecycle. A rule would start as a pioneer (warn-only, shadow-counted), become mature (blocking) and finally climax (compiled, frozen).
  Done when: `sampo ward rules --stage` lists each rule's stage, and a test shows a new rule cannot block until it has N shadow hits and zero hits on the user's accepted-command corpus.

- **Fuzz the ecotones between command classes** — SECURITY — value 4 — effort M — risk low — category: Ward fuzz
  Why: the bypass-hunting ideas so far are model-generated. Seams are where one grammar meets another, such as quoting into heredoc, `xargs`/`find -exec` into a shell, git aliases, env prefixes and `$(…)` inside refused verbs. A deterministic cross-product of seam pairs needs zero tokens.
  Done when: a generated seam corpus of at least 2,000 commands runs through the real hook path, and any case that passes where its plain form is refused fails the suite.

- **Make acquired Ward rules immune-safe (wild)** — SECURITY — value 4 — effort M — risk med — category: Ward learning
  Why: wild. In bacterial CRISPR a new spacer is acquired from an attacker and an autoimmunity check stops it hitting self. After a bypass attempt is caught, store a short, recency-ordered, size-capped signature, and reject any signature that would block a command in the user's accepted history. The array is tighten-only.
  Done when: a planted bypass produces a stored signature, a signature that would block a known-good command is refused with the command named, and the array never exceeds its cap.

- **Shield keystone files with read-only mounts in lanes** — SECURITY — value 4 — effort M — risk med — category: guard integrity
  Why: assumption: a few files (Ward rules, hook registration, settings) disable most defences if altered. Compute them from the import and hook graph, as in a removal experiment, then bind-mount them read-only into every lane worktree.
  Done when: a lane that tries to write a keystone file gets EROFS, and `sampo doctor` lists the computed keystone set.

- **Plant honey-token seeds in lane environments** — SECURITY — value 3 — effort S — risk low — category: egress
  Why: the pack has pack-egress and secret-scan ideas but no active tripwire. A unique fake secret in each lane's env gets swept for in packs, site data, git objects, transcripts and `fm-children`.
  Done when: seeding a token and running the sweep finds it in a planted leak path, and a clean run reports zero hits on every egress surface.

- **Probe for allelopathy between injected texts** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: assumption: tool results and repo files can emit text that suppresses Sampo's own rules (for example "Sampo is disabled", or a forged guard line). A fixed probe set of inhibitor strings goes through the hook path and checks that the Ward and the done-gate verdicts stay unchanged.
  Done when: 30 inhibitor fixtures leave every verdict identical to the baseline, and one deliberately weakened guard makes the test fail.

- **Keep a pioneer warm daemon for hooks** — PERFORMANCE — value 4 — effort L — risk med — category: hook latency
  Why: the pack shows a hook bench and a shim import tax. One resident process holds parsed rules and the map, and hooks become thin clients on a user-only unix socket with a peer-uid check. The cold path stays as a fallback.
  Done when: `bench_hooks.py` p95 drops measurably against the cold path, killing the daemon still gives the same verdicts, and a different-uid connection is refused.

- **Govern lane count with a carrying-capacity controller** — PERFORMANCE — value 4 — effort M — risk low — category: scheduling
  Why: lanes are parallel, local models cost about 3 minutes to switch, and there is no named ceiling. Logistic control grows lanes until hook p95, load or GPU queue crosses a threshold, then backs off.
  Done when: a synthetic load test shows the lane count settling below the threshold with no oscillation beyond one step.

- **Recompute the funnel only inside disturbed patches** — PERFORMANCE — value 4 — effort M — risk low — category: moons at scale
  Why: the 10,000-candidate funnel is append-only, and a changed embedder or threshold should not mean a full rerun. Key stages by candidate hash plus model fingerprint, and recompute only the LSH buckets a change touches.
  Done when: changing one threshold re-runs fewer than 20% of the candidates, and the final survivors equal a full rerun on a fixture.

- **Compile stable Ward rules into a climax automaton** — PERFORMANCE — value 3 — effort M — risk med — category: Ward speed
  Why: this works with the lifecycle above, since only climax-stage rules compile. One automaton is rebuilt on a rules-hash change, and a differential test against the slow path guards equivalence.
  Done when: 100k corpus commands give identical verdicts on both paths, and median Ward time falls.

- **Share one read cache across hooks on an event (competitive release)** — PERFORMANCE — value 3 — effort S — risk low — category: hook latency
  Why: assumption: several hooks on the same event reopen the same files (map, rules, ledgers). A per-event content-hash cache would remove the duplicate opens.
  Done when: an strace count of opens per event falls, and verdicts are unchanged.

- **Route lanes by reinforced conductance, like a slime mould (wild)** — PERFORMANCE — value 3 — effort M — risk low — category: routing
  Why: wild. Edges from task kind to model, endpoint or machine thicken with successes per second and decay otherwise, so routing follows measured flux without a hand-tuned table. The local-model bench could seed it.
  Done when: after 200 simulated tasks with a degraded endpoint, traffic to it falls below 10% without a config edit.

- **Attach as an epiphyte with zero host-config writes (wild)** — SECURITY — value 3 — effort M — risk med — category: host isolation
  Why: wild. An epiphyte lives on its host without harming it. Run Sampo's hooks through a wrapper or env-scoped config so the host's settings and files stay byte-identical, which makes uninstall and shim-doubling bugs cheap to reason about.
  Done when: a hash of the host config before and after a full session is identical, and removing the wrapper leaves no Sampo hook registered.

Next question: which of Sampo's defences already sit at climax stage, meaning unchanged and never missed for months, so they could be compiled and frozen while the pioneers get the testing effort?
Next question: when two lanes or two models compete for the same file or GPU, does the ledger record who lost, so a niche-overlap map could be drawn from data instead of guessed?
