# Brainstorm — lens: grid

Grid used: surfaces are the web UI, CLI (`sampo`/`fm`), hooks and skills, the site and README, and commit/ship output. Actors are the user, the agent, other agents and an unattended run. Failure modes are missing, wrong, slow, unsafe and unclear. These ideas avoid the lists above; two are second-order on them and say so.

- **Lint commit messages, tags and PR bodies for role words** — SECURITY — value 4 — effort S — risk low — category: public surfaces
  Why: cell commit/ship × unattended × unsafe. The vocabulary lint covers site text, but `fm ship` pushes commit messages and tags that stay public after a rewrite. Assumption: nothing lints them now.
  Done when: a commit message naming a machine, endpoint or vendor orchestrator is refused at `fm ship`, and a planted one is caught in a test.

- **Lint plugin manifest and skill frontmatter for host and vendor names** — SECURITY — value 3 — effort S — risk low — category: public surfaces
  Why: cell hooks/skills × other agents × unclear. The 1,396 skill files and marketplace listings render in strangers' harnesses. Assumption: descriptions still name Claude as the orchestrator in places.
  Done when: the ship gate fails on a `plugin.json` or SKILL description containing a banned orchestrator name, outside an allowlisted compatibility section.

- **Make doctor and receipt output paste-safe** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: cell CLI × user × unsafe. Users paste `fm doctor` output into issues, and paths like `~` and endpoint names leak the machine. The user's own steer was never to show "the user's machine".
  Done when: `fm doctor --paste` replaces home paths, hostnames and profile names with role tokens, and a golden test shows none survive.

- **Refuse drive edits to a doc number unless the same tick ran its probe** — SECURITY — value 3 — effort M — risk med — category: unattended docs
  Why: cell docs × unattended × wrong. The 421 flagged claims will be bulk-edited. Computed placeholders help, but only if the drive actually ran the probe. Second-order on "Make numbers in docs computed".
  Done when: an unattended edit that changes a numeric claim with no matching probe receipt is blocked and listed on the unproven shelf.

- **Show "meaning changed" separately from "wording changed" when the ask is edited** — FEATURE — value 4 — effort M — risk med — category: meaning proof
  Why: cell CLI × user × unclear. Meaning is the biggest unproven class (599), and re-planning after a user edit silently reuses old criteria. Assumption: re-plan keeps old criteria by default.
  Done when: editing the ask prints which criteria were kept, retired or flagged "re-read me", and a test covers a rename-only edit versus a semantic edit.

- **Reuse compiled criteria by example shape** — PERFORMANCE — value 3 — effort M — risk low — category: criteria compiler
  Why: cell CLI × agent × slow. Spec examples recur as shapes ("prints X when Y", "exits N on Z"), so compiling each one with a model is wasteful. Assumption: the shapes cluster heavily in closed Done-whens.
  Done when: the second task containing the same shape compiles its criterion with zero model tokens and passes the same stub-first check.

- **Give lanes a read-only proof lens of the parent's criteria** — FEATURE — value 3 — effort M — risk med — category: multi-agent
  Why: cell hooks × other agents × missing. A lane can close its part without knowing the parent's criteria cover its files. Assumption: criteria currently attach to the task id, not to file sets.
  Done when: a lane touching a file named by a parent criterion gets that criterion in its start note, and its hand-back must list its status.

- **Render web UI verdicts only from the stored row** — FIX — value 3 — effort S — risk low — category: web UI
  Why: cell web UI × user × wrong. The UI is the surface users trust most, so a recomputed verdict could disagree with the CLI. Assumption: some views recompute.
  Done when: a test that mutates the stored verdict shows the UI and `--json` always agree, with no recomputation path.

- **Bound each criterion's wall time by its past runs, with a "slow, not wrong" verdict** — PERFORMANCE — value 3 — effort S — risk low — category: unattended verification
  Why: cell CLI × unattended × slow. Timeouts already map to unproven, but a criterion that is merely slow tonight differs from one that hangs.
  Done when: a criterion over 3× its median is labelled "slow" with the run's elapsed time, not folded into "timed out".

- **Wild: let the site and README rotate which orchestrator they show per page load** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. The user said to show any orchestrator, never Claude. Cell site × user × unclear: if the name changes visibly, readers learn it is a slot.
  Done when: two loads of the scene show different generic orchestrator names, and no-JS shows the neutral "the orchestrator".

- **Wild: make a "wrong-but-green" court that proves a criterion can lose** — FEATURE — value 4 — effort L — risk med — category: meaning proof
  Why: wild. Cell CLI × agent × wrong. A cold small-model child writes the cheapest plausible wrong implementation per plan, and the plan only files if the criteria reject it. Overlaps "Run each criterion against a wrong implementation first", so this makes it a standing plan-time court with a published reject rate.
  Done when: a plan whose criteria accept the child's wrong implementation is held, with the accepted diff shown.

- **Wild: ship a "proof of absence" stamp for each public surface** — SECURITY — value 3 — effort M — risk low — category: public surfaces
  Why: wild. Cell site × unattended × unsafe. Each publish carries a hash plus the list of banned-term scans it passed (source, SVG text, alt text, commit messages), so a reader can see what was and wasn't scanned.
  Done when: the site footer links a scan list, and removing one scanner changes the stamp.

- **Wild: put criteria in a phone-sized "yes, that's what I meant" deck** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: wild. Cell web UI × user × missing. Meaning can't be proven mechanically, so each spec example becomes one swipeable card (given, gets, "that's right or wrong") and each answer is recorded as a human-witnessed proof.
  Done when: answering all cards for a task flips its meaning verdict to proven by witness, and a wrong swipe files a spec dispute.

**Cells left empty:**
- Web UI × unattended × unsafe: the UI is read-only by the existing stale-tab and action rules.
- CLI × other agents × slow: the earlier ideas on batching, memoising and warm pools cover it.
- Hooks × user × unclear: injected notes are already covered by the role-table and per-host rendering ideas.

Next question: which of the 599 unproven meaning claims has a user-supplied example in its own ask that nothing compiled, and how many would become runnable criteria with no model call?
Next question: do commit messages, tags and issue bodies Sampo writes appear in any current public-surface lint, and if not, how many past ones name a banned term?
