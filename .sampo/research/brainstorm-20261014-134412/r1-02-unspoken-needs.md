# Brainstorm — lens: unspoken needs

- **Fingerprint every drop and filter new ideas against it** — FEATURE — value 5 — effort S — risk low — category: ideation
  Why: the user dropped "if-scope the Read hook" and "delta reads", each with a measurement. The pile still holds "Scope every hook with native `if` filters", "Serve repeat reads as ranges or deltas" and "Narrow hooks natively…". Drops don't gate anything, so the same ideas return every round.
  Done when: a test feeds the dropped "if filter on Read" idea in new wording to `fm ideas`'s post-filter. It is flagged with the drop date and the measurement, and passes only with `--remeasure`.

- **Add a positive capability inventory to every brainstorm pack** — FEATURE — value 5 — effort S — risk low — category: ideation
  Why: round 2 yielded 3 grounded ideas out of 437 because most re-proposed existing commands. The pack carries a huge negative "ideas so far" list but no generated list of what Foreman can already do (verbs, settings, hooks, one line each). The inventory should replace the pile, not sit beside it.
  Done when: the pack contains an `fm help --all`-derived inventory under 3 KB, and a seeded duplicate of an existing verb is rejected in a replay test.

- **Canonicalise idea categories and cluster labels** — FIX — value 4 — effort S — risk low — category: ideation
  Why: the pile mixes "tokens 24", "tokens/speed", "performance: time and tokens per finished task: 22" and cluster headers sitting in the idea list. The "Thin so far" hint counts exact strings, so it misleads children.
  Done when: every category passes through one alias table, the headers are not counted as ideas, and a test shows `tokens` and `tokens/speed` merging into one count.

- **Record session kind once and make every hook read it** — FIX — value 4 — effort M — risk med — category: reliability
  Why: round 1 and 2 fixed one-off `claude -p` driving the queue, bench replays counted as one-offs, `record_pid` overlap, and children re-entering hooks. They are separate patches for one class: ambient session detection.
  Done when: SessionStart writes `session_kind` (interactive, headless child, bench, lane, remote) once. A parametrised test runs every hook across all five kinds, and `fm doctor` prints the kind.

- **Alarm when a Foreman metric looks too perfect** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user caught "the full suite never failed" and the catch-rate readers missing "✗ exit N". Both were silent zeros that looked like good news.
  Done when: any rate over N≥30 events showing 0 failures or 100% prints "implausible, check the reader" in `fm doctor`. A fixture with a seeded failure of the real stored format flips the number.

- **Add a host-reality probe for hardened and RAM-backed systems** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: assumption: this machine runs `linux-hardened` (Arch, per T-0325) with work under `/run/user`. Hardened kernels often disable unprivileged user namespaces, which breaks bubblewrap-style sandboxes. Spill files, heartbeats and monitor outputs on tmpfs vanish at logout.
  Done when: `fm doctor` reports userns availability and any Foreman store on tmpfs, each with the exact fix command.

- **Check public pushes for identity leaks before a release** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: assumption: the user uses an anonymised email and the repo is public. `fm page` already swaps the username for "user", but release pushes (1.2.27 to GitHub main) are not shown to check commit author/committer emails, hostnames or home paths.
  Done when: a pre-push check lists author emails, hostnames and `/home/<name>` strings in the range being pushed. A seeded commit with a real email blocks until acknowledged.

- **Wild: Recompute the track record with an independent reader** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: wild; a metric reader and its writer are written by the same hand, which is why the format mismatches keep slipping through. A cold child gets only the raw ledger and the docs and derives catch rate and give-up rate. A mismatch with `fm`'s numbers files a task.
  Done when: a seeded ledger with a known answer makes the cold child and `fm` agree, and a deliberately broken reader produces a filed mismatch task.

- **Wild: Run the bench in a hostile-host container** — FEATURE — value 3 — effort M — risk med — category: reliability
  Why: wild; round 1's bugs surfaced through environment quirks: closed stdout pipes, no stdin, missing `python3`, throttled CPU. One container profile (read-only home, tmpfs state, no userns, slow disk, no tty) could replay all of them on every release.
  Done when: `plugin/tests/e2e` has a hostile-host target that fails when a known-broken fixture (stdout closed, home read-only) is reintroduced.

- **Wild: Make every new idea cite the invariant it serves** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: wild; thousands of ideas must collapse onto a few laws (never idle, evidence before done, one writer per state, nothing sent without consent). An idea with no invariant is either a new law, which the user should see, or noise.
  Done when: `fm ideas` output requires an `Invariant:` line from a short list in MASTER.md. Ideas that cite none are listed separately as "proposes a new law".

- **Wild: Say what Foreman would refuse to do about its own idea pile** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; the user keeps asking for "etc." improvements with no end. A round-close line could name the one deferred cluster Foreman now thinks is not worth building, with the measurement behind it, so removing work feels like progress.
  Done when: `fm round` close prints one "I'd drop this" line citing a number from the ledger, and the user's yes records a drop with a fingerprint.
