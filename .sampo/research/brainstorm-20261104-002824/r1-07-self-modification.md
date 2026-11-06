# Brainstorm — lens: self-modification

- **Mute self-filed detectors by their own drop rate** — FEATURE — value 5 — effort S — risk low — category: self-tuning
  Why: five recent drops (Breakage ahead, Source moved, Read the hot files, Missing tool shellcheck, MOONS_LOCAL) were all items Foreman filed itself and the user dismissed.
  Done when: `fm doctor` lists each filing detector with its filed and dropped counts, and a detector over 70% dropped across at least 10 filings is demoted to a digest line, with a test using a seeded ledger.

- **Mutable-surface manifest with bounds** — SECURITY — value 5 — effort M — risk med — category: self-change
  Why: assumption: anticipation will tune its own windows, prompts and thresholds, and nothing yet says what it may edit. A file lists the knobs, prose files and tables a self-change may touch, each with limits. The guard, the Ward and gen-0 are absent from it.
  Done when: a self-change lane that touches a path outside the manifest or a value outside its bounds is refused by `fm ship`, with a test for each case.

- **Self-repair prose and Exam references after a move** — FIX — value 4 — effort M — risk low — category: self-healing
  Why: T-2748 moved the `fm*.py` modules into `plugin/lib/sampo/` and left shims, and a cold-read list still named the old paths and was dropped as stale. After any rename or move, a zero-token pass finds the old names in skills, MASTER.md, Exam commands and `--json` key paths and drafts the fix as a task.
  Done when: renaming a module in a scratch repo yields one task per stale reference, and applying them turns `fm check` green.

- **Drive shadow-audits its own wait decisions** — FIX — value 5 — effort M — risk low — category: reliability
  Why: T-2873, T-2901 and the two related fixes each patched a different way the drive miscounts running subagents. The drive records "waiting on N agents (source)" at each tick and compares it with the engine's background list and its own event scan. Any mismatch is filed with the evidence attached.
  Done when: a fake host that omits a running subagent produces a mismatch record and a filed task naming both sources.

- **Champion/challenger for decision models** — FEATURE — value 4 — effort M — risk med — category: local models
  Why: the steers want d3, tev1 and kev scaffolded to frontier results, and the model bench has held-out closed tasks. A challenger profile (a new Ollama tag or prompt) runs in shadow beside the champion. It is promoted by pointer swap only if it beats the champion on that held-out set, and it is rolled back automatically if the live drop rate rises.
  Done when: a seeded better challenger is promoted and a seeded worse one is not, and the pointer swap is reversible with one command.

- **Rewrite skill descriptions from observed mis-triggers** — FEATURE — value 3 — effort M — risk med — category: skills
  Why: `plugin/skills/` has 1396 files and a cc-skill-descriptions card exists. Transcripts show when a skill fired and the user ignored it, or when a skill that fit did not fire. A proposed description rewrite is replayed against those transcripts before it is filed.
  Done when: a proposal reports hits and misses before and after on the same transcript set, and a proposal that trades more misses than it fixes is not filed.

- **Every missed prediction becomes a red test** — CLEAN — value 4 — effort S — risk low — category: anticipation
  Why: the anticipation model is new and has no regression corpus. When the user's first ask differs from the sealed prediction, the (ledger snapshot, ask) pair is saved as a fixture, and the predictor's test suite replays them all.
  Done when: adding a fixture where the predictor is wrong turns the suite red until a rule change or an explicit "unpredictable" tag is committed.

- **Cross-family second reader for self-changes** — SECURITY — value 4 — effort S — risk low — category: review
  Why: assumption: a model reviewing its own family's patch shares its blind spots. The standing cold reads run Haiku then Sonnet. Self-changes would add the local 27B as a third reader whose disagreement with the others is logged.
  Done when: a planted backdoor in a self-change patch is caught by at least one reader in a seeded test, and the agreement rate appears in `fm doctor`.

- **Prune MASTER.md and injected notes by whether they were read** — PERFORMANCE — value 3 — effort M — risk low — category: simplicity
  Why: the injected text and docs grow, and "ratchet injected tokens" caps size without saying what to cut. Count which anchors and notes are fetched or cited in sessions, then propose deleting sections with zero use in 30 days, each as a revertible commit.
  Done when: the report lists the unused sections with their token cost, and applying the top proposal drops session-start tokens by that amount with no failing doc test.

- **Wild: Self-surgery in a clone** — FEATURE — value 4 — effort L — risk med — category: self-upgrade
  Why: wild. Sampo installs its candidate self into a throwaway home, replays a recorded day of hook events and asks through it, and swaps the live install only if the outputs match the old one within stated tolerances.
  Done when: a candidate with a planted hook regression is blocked and a clean one is swapped, both from one command.

- **Wild: Parliament of sizes** — FEATURE — value 3 — effort M — risk med — category: governance
  Why: wild. A self-change needs votes from a 27B, a small Ollama model and a frontier model, each weighted by its past calibration on closed tasks. A vote that goes against a heavier voter is recorded as a dissent and settled later.
  Done when: `fm self vote <task>` prints each voter, its weight and its verdict, and a weight is recomputed from outcomes after each settled change.

- **Wild: Dream shift** — FEATURE — value 4 — effort L — risk med — category: overnight
  Why: wild. The user sleeps and wants major progress by morning. Overnight, Sampo drafts its own improvement on a branch that expires in 3 days. The change is one knob, rule or prose edit, with a sealed prediction such as "re-asks of X fall". The morning card shows the diff and its backtest result, and nothing merges without the user's key.
  Done when: a scratch run leaves one branch, one sealed prediction file and one morning-card entry, and the branch is deleted on expiry.

- **Wild: Self-description the user can strike through** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: wild. One file records what Sampo believes about this user's habits, windows and tolerances. Each line was learned by a named self-change, and a struck line stops being used.
  Done when: striking a line removes its effect on the next prediction, and the strike is logged with the line's origin.

Next question: Which of Sampo's own filings or self-edits has the user reverted or ignored within a day, and does that rate differ by the model that wrote them?
Next question: Can a self-change be proven harmless against the Ward without the change being able to read the Ward's rules?
