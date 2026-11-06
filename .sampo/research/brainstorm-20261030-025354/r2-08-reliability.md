# Brainstorm — lens: reliability

- **Prove the harness before the bug** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: Mission 3 is graded on the `none` and `bug` kinds in repos Foreman has never seen. A test runner that silently fails to start looks the same as "no bug", so the `none` score would be luck. Assumption: single-test invocation differs per ecosystem and is guessed today.
  Done when: before any finding is proven, Foreman runs a sentinel test that must pass and one that must fail in the target repo, and a runner that can't pass both aborts the scan with a named reason (tested on python, js and rust fixtures).

- **Give every verdict a type** — FEATURE — value 5 — effort S — risk low — category: verdicts
  Why: the genesis exam change that counted fallback and error drafts as errors, plus the 0-of-108 outside signal, show that "found nothing" hides crashes. Assumption: the finders currently return an empty list for both clean and crashed.
  Done when: every scan ends in exactly one of `clean`, `findings`, `errored`, `env-blocked` or `unprovable`, a killed or malformed finder yields `errored` (never `clean`), and a test asserts each path.

- **Wrap every proof run in a hard envelope** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: proofs execute tests from repos Foreman has never seen. A hanging or looping test would stall a whole overnight shift, and a hostile one runs arbitrary code. Assumption: the lane runner has no per-proof limits today.
  Done when: a fixture test with an infinite loop and one that forks children are both killed as a process group at the timeout, output is capped, the network is off, and the finding is marked `errored` with the cause.

- **Seal each finding in a repro capsule** — FEATURE — value 4 — effort M — risk low — category: reproducibility
  Why: a finding that can't be replayed next month can't be audited against `fm outcomes` survival. Assumption: findings currently store prose and a test name only.
  Done when: each finding file records the commit, the tool and lockfile versions, the exact command, the seed and the environment hash, and `fm find replay <id>` reproduces the red result on a fresh checkout.

- **Expire a finding when its files change** — FIX — value 4 — effort S — risk low — category: staleness
  Why: the queue is deferred-heavy and nightly shifts run for days. A finding proven against an old tree could drive a lane against code that has moved. Assumption: no tree hash is stored with findings.
  Done when: a finding stores a hash of the files its proof touches, `fm find check` flags it `stale` after an edit to any of them, and the lane refuses to open on a stale finding.

- **Prove under the command CI uses** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: unseen repos have their own runners and flags, and a guessed `pytest` call can fail for reasons unrelated to the bug. Assumption: CI workflow files and manifests are readable for most target repos.
  Done when: for a fixture with a non-default test command in its workflow file, the proof runs that command narrowed to one test, and falls back to the guess only when no CI file exists (the receipt says which was used).

- **Trip a breaker after three straight dropped findings** — FEATURE — value 3 — effort S — risk low — category: circuit breaker
  Why: genesis already stops after 3 reverts. A finder that is wrong three times running is probably misconfigured for that repo, and it keeps spending. Assumption: the nightly shift has no such stop.
  Done when: three consecutive findings dropped as unprovable or refuted halt the shift, and the receipt reads "stopped: 3 drops in a row, finder likely mismatched".

- **Pin ranking as a pure function with a golden file** — CLEAN — value 3 — effort S — risk low — category: determinism
  Why: value ranking is new, and a ranking that reorders between two runs on the same ledger can't be tested or trusted. Assumption: ties and float scores have no fixed order.
  Done when: running the ranker twice on a frozen ledger gives byte-identical output, ties break by fingerprint, and a golden-file test fails on any change.

- **Bisect a red proof across history** — FEATURE — value 3 — effort M — risk med — category: evidence
  Why: a test that was green last week and red now is far stronger evidence of a bug than one that was always red, since the oracle may simply be wrong. Assumption: the repo has git history.
  Done when: `fm find` records "green at <sha>, red since <sha>" or "never green" per finding, and ranking weights the first above the second.

- **Wild: Race the finders against a null finder** — FEATURE — value 3 — effort M — risk low — category: baseline
  Why: assumption: a finder that only matches a random pick of file and line hasn't earned its cost. The pack shows deterministic finders scoring 0 of 108, and no lift is measured.
  Done when: the exam runs a random-pick arm beside each finder, and a finder whose precision is not above the null arm's gets muted with a note in the scorecard.

- **Wild: Metamorphic twin of the repo** — FEATURE — value 4 — effort L — risk med — category: consistency
  Why: assumption: finders that key on identifier names or formatting fail under harmless rewrites. Rename locals and reformat in a scratch copy, and the finding set should not change.
  Done when: on three fixture repos, a rename-and-reformat copy yields the same findings, and any finding that appears or disappears is listed as unstable and excluded from ranking.

- **Wild: Autopsy every reverted fix** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: assumption: a finding the user reverts or the 30-day survival check flags means the proof was fooled. Today nothing learns from that.
  Done when: a revert triggers a short note naming why the proof passed wrongly, the check goes into a fooled-by list, and the next scan applies it (tested with a hardcoded-literal fix).

- **Wild: A pocket zoo for toolchain smoke tests** — FEATURE — value 3 — effort M — risk low — category: preflight
  Why: assumption: the user's machine may lack node, cargo or ruby, and the first sign today would be a silent `clean`. Ship ten tiny buggy repos, one per exam language, with known answers.
  Done when: `fm find doctor` runs each zoo repo's proof and prints a per-language line, either "ok" or the exact missing tool and install command.

Next question: What is the measured precision and recall of each finder on a clean (`none`) repo versus a seeded one, and which verdict types are actually reachable today?
Next question: When a proof is `env-blocked`, who or what is allowed to fix the environment, and does that action need the user's consent?
