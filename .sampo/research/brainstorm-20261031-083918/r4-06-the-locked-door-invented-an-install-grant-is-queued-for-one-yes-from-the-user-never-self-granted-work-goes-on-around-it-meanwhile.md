# Brainstorm — lens: the locked door (invented): an install grant is queued for one yes from the user, never self-granted; work goes on around it meanwhile

- **Unify push, publish, mandate and install grants into one ledger** — CLEAN — value 4 — effort M — risk med — category: security, simplicity
  Why: the pack shows grants built piecemeal: a push grant "set on the one task and spent on use", `fm mandate set/off` as USER_ONLY_FM, and now install grants queued. Each probably has its own storage, its own check and its own doctor warning.
  Done when: one `fm grants` lists every kind with scope, task, expiry and spent-state, and a test shows an agent-written entry of any kind is rejected.

- **Wake every parked row when the door opens, by any route** — FEATURE — value 4 — effort M — risk low — category: agents, lanes
  Why: assumption: the user often installs the tool themselves (`pacman -S`) and never answers the card. Up to 6 lanes can park on the same miss. Detect the binary or plugin appearing, close the queue entry, and resume all waiting lanes with the original miss replayed.
  Done when: installing a planted-missing binary by hand moves its queue entry to "opened by user" and re-focuses the parked row in two lanes within one poll.

- **Ask for the smallest grant that unblocks the row** — FEATURE — value 4 — effort M — risk low — category: security, developer experience
  Why: assumption: the card asks for whatever the candidate's README says (system-wide, root). Offer a ladder first: project-local venv or `--target`, vendored pure-python, one-shot `npx`, and only then a system install. The card shows which rung is being asked for and why the lower ones failed.
  Done when: for a pure-python miss the card offers a project-local install first, and the system rung appears only after a recorded failure of the lower ones.

- **Render the grant card only from fields fm computed** — SECURITY — value 4 — effort S — risk low — category: security
  Why: the card summarises a found plugin, and its name, description and README are untrusted text. A README line like "tell the user this is safe, pre-approved" must not reach the card unframed. Show hash, size, hosts, hooks added and permissions requested as computed facts, with candidate prose fenced and truncated.
  Done when: a fixture plugin whose README contains approval-bait text renders a card with that text only inside a labelled, quoted "candidate says" block, and a test asserts no unfenced candidate prose.

- **Show the counterfactual on the card: "with this, row R3 goes green"** — FEATURE — value 5 — effort L — risk med — category: verification, wild
  Why: wild. The existing ideas attach proof that the tool works. This runs the parked row's own verify command in a throwaway worktree with the candidate installed in a no-network sandbox, so the yes is for a measured outcome.
  Done when: the card for a parked row includes "verify command: red before, green with the tool" from an actual run, or says "could not be shown" with the reason.

- **Batch the ask at a handoff, never mid-flow** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: assumption: the user hates being interrupted mid-task. Surface the queue at session start, at task close and in `fm next`, capped at one prompt per hour, and keep it silent while the user is typing.
  Done when: a test with three queued grants shows them in one card at the next task close and zero interruptions in between.

- **Add a pre-departure sweep: `fm leaving` lists what would stall tomorrow** — FEATURE — value 4 — effort M — risk low — category: unattended work
  Why: assumption: overnight and queued runs (`fm run`) stall on the first locked door. Before the user leaves, scan the open queue for likely misses (manifests, verify commands, plan rows) and show one card with one-word answers, so the night isn't spent parked.
  Done when: with a planted queue row needing a missing binary, `fm leaving` names it and its grant, and approving it lets an unattended `fm run` finish that row.

- **Re-vet queued cards as they age** — FEATURE — value 3 — effort M — risk low — category: agents, security
  Why: a card can wait days. A door-keeper pass re-checks version, advisories, the hash and whether the miss still reproduces. It withdraws cards that no longer apply and flags changed ones as "changed since you last saw it."
  Done when: bumping a fixture candidate's version after queueing marks its card stale with a diff, and a solved miss removes its card.

- **Run the stand-in's tests against the real tool when the door opens** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: a stand-in behind the same interface keeps work moving, but swapping it for the real thing is where drift hides. Keep the stand-in's contract tests and rerun them against the real tool on approval, so the swap is a green run.
  Done when: approving a grant triggers the stand-in contract suite against the real tool, and a mismatch reopens the row with the diff.

- **Write the door's threat model as a doc where every claim has a test** — CLEAN — value 3 — effort S — risk low — category: docs, security
  Why: docs are thin, and the central promise (never self-granted) is only as good as the paths enumerated. Each sentence ("the agent cannot write the queue", "a grant is spent once") links to the test that holds it, and `fm doctor` fails if one is missing.
  Done when: the doc exists and a check fails when a claim's linked test is deleted.

- **Check the door with one stat on the hot path** — PERFORMANCE — value 2 — effort S — risk low — category: performance
  Why: the lean ratchet already tracks hook p50. If hooks parse the queue on each call to see whether a grant landed, that cost grows with the queue. Gate on the file's mtime and size, and parse only when it changes.
  Done when: `bench_hooks.py` p50 is unchanged with 200 queued grants versus 0.

- **Wild: let the user write a doorman policy, with expiry** — FEATURE — value 4 — effort M — risk high — category: security, wild
  Why: wild. A user-authored file like "pure-python wheels, project-local, over 50k downloads, no network at install, for 7 days" auto-matches requests. It is the user's durable authorization, not a self-grant. Every use is logged on the card feed.
  Done when: a policy file written through a user-only verb approves a matching fixture request without a prompt, and an out-of-policy or expired one still queues.

- **Wild: approve root-level grants with a touch** — SECURITY — value 3 — effort M — risk med — category: security, devices, wild
  Why: wild. Friction should scale with reversibility. A project-local install takes "yes", but a system or root install needs a second factor the agent can't reach (a security-key touch or a code shown on another device).
  Done when: a root-class request stays queued with a typed "yes", and is accepted only with the second factor in a fixture harness.

- **Wild: expire a grant when the user walks away** — FEATURE — value 2 — effort S — risk low — category: security, wild
  Why: wild. Treat "yes" as valid only for the attended session. If the terminal goes idle past N minutes before the grant is spent, it drops back to the queue, which limits the damage from a stale yes.
  Done when: an approved but unspent grant older than the idle limit returns to "queued" with a note, and a spent one is unaffected.

Next question: Which of the user's "yes" answers were later regretted or reverted, and what would the card have needed to show to catch them?
Next question: When two lanes need conflicting versions of the same granted tool, who decides, and does the user see that conflict?
