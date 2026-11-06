# Brainstorm — lens: reliability

- **Add `fm guard why "<cmd>"` that replays a command through the real hook** — FEATURE — value 5 — effort S — risk low — category: guard debuggability
  Why: the review says the main thread twice wrote a scratch script to replay a command through the real hook with the real cwd (T-1125, T-1141); there is no `fm` way to ask "would the guard allow this here, and why".
  Done when: `fm guard why 'cat <<EOF | fm edit ...'` prints allow/deny, the matching rule and the cwd it used, and its verdict equals the live hook's on a recorded corpus of 50 commands.

- **Lint a verify command the moment it is added** — FEATURE — value 5 — effort S — risk low — category: verify integrity
  Why: the review says verify commands are often wrong (a nonexistent test module, `npm test` with no npm) and are caught only when they run; T-1128/T-1133 only made such runs editable.
  Done when: adding `python3 -m pytest nosuch.py` or `npm test` in a repo with no package.json to a task is refused or warned at add time with the reason, and a valid command passes silently.

- **Make shared registries conflict-free by splitting HELP_TIERS into per-verb files** — CLEAN — value 4 — effort M — risk low — category: merge conflicts
  Why: every new command edits one HELP_TIERS line in fmcli.py, so nearly every second merge conflicted (T-1059, T-1062 twice) and needed a re-merge builder.
  Done when: two builders each adding a verb on separate branches merge with zero conflicts, and `fm help` output is byte-identical to before.

- **Require an adversarial self-check receipt before a builder may report done** — FEATURE — value 5 — effort M — risk med — category: builder quality
  Why: reviewers found real defects in almost every builder branch (deny-bypass, false green, unbounded time, writes outside a folder, overwritten leases) while builders returned "done" unchecked.
  Done when: a builder's done is rejected unless it attaches a receipt listing at least one attempted break per changed surface with the command it ran, and a test shows a builder with no receipt is refused.

- **Index briefs so every command stops parsing all of them** — PERFORMANCE — value 4 — effort M — risk med — category: load resilience
  Why: T-1140 took hooks from 135 to 72 ms by not parsing all 1,069 briefs, but `fm state --json` once took over 120 s under load and other commands still parse every brief.
  Done when: `fm state --json` with 1,000+ briefs and a simulated load of 4 CPU burners completes under 5 s, and the index rebuilds correctly after deleting it.

- **Normalise lease paths against the worktree root** — FIX — value 4 — effort S — risk low — category: lease correctness
  Why: builders cd into subdirectories so relative paths double (`mods/foreman-ui/mods/foreman-ui/...`), corrupting leases and claims.
  Done when: `fm lease` run from any subdirectory stores the same repo-relative path, and a regression test covering cwd = `mods/foreman-ui` passes.

- **Re-run only the load-sensitive criterion on a lane merge, with a load-aware retry** — FIX — value 3 — effort M — risk med — category: merge reliability
  Why: merges are sequential, each re-running criteria, and one load-sensitive criterion failed a merge then passed; the failure looked like a real red.
  Done when: a criterion that fails under injected load and passes when rerun alone is recorded as "flaky under load" with both runs shown, and a genuine failure still blocks the merge.

- **Check the installed foreman-ui against the repo release at doctor time** — FIX — value 3 — effort S — risk low — category: version drift
  Why: installed foreman-ui is 0.7.0 while the repo's is 0.17.0 (0.18.0 per the later release), and T-0418 sits blocked; marketplace users lag a release unnoticed.
  Done when: `fm doctor` reports "foreman-ui 0.7.0 installed, 0.18.0 available" with the update command, and goes green after the update.

- **Screenshot-gate the pane in the release path** — FEATURE — value 4 — effort M — risk low — category: UI verification
  Why: the pane wasn't screenshot-verified last round, and the mission's pillar 4 requires before/after screenshots of every screen.
  Done when: a release step renders the pane from a deterministic fixture at three terminal sizes, diffs against stored goldens and fails on an unapproved change.

- **Flag approximate heuristics with a measured false-positive rate** — FEATURE — value 3 — effort M — risk low — category: heuristic honesty
  Why: card backtest is a text match, history fix seeding is keyword-based, and the untrusted-text check is keyword heuristics; their error rates are unknown.
  Done when: each of the three has a labelled sample set in the tests and `fm doctor` prints its precision and recall, failing if either drops below a recorded floor.

- **Wild: Replay every guard denial from the ledger nightly against the current guard and report verdict drift** — FEATURE — value 4 — effort M — risk low — category: guard regression
  Why: wild; guard false positives were the costliest debugging (T-1125, T-1141), and guard fixes can silently flip older verdicts. Assumption: the ledger keeps the command text and cwd.
  Done when: a nightly run lists commands whose allow/deny differs from the recorded verdict, and a deliberately loosened rule shows up in the report.

- **Wild: Build a "stuck builder" detector that spots bare-stdin hangs and repeated cd loops from tool-call shape** — FEATURE — value 3 — effort M — risk med — category: builder watchdog
  Why: wild; builders hung on bare stdin readers (T-1129), ran `fm lease drop` bare (T-1134) and cd'd into subdirectories. Assumption: the tool-call stream is readable from the ledger.
  Done when: a recorded hung-builder trace triggers an alert within 60 s naming the likely cause, and a normal builder trace triggers none.

- **Wild: Give each builder a throwaway "load budget" so four builders can't push the machine past a set load average** — FEATURE — value 4 — effort M — risk med — category: load shedding
  Why: wild; load reached 30-60 with 4 builders, which caused the 120 s `fm state` and the flaky merge criterion.
  Done when: with the budget set to 8, launching a fifth builder while load exceeds 8 queues it with a visible reason, and it starts once load drops.
