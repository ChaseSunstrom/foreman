# Brainstorm — lens: reliability

- **Cluster red gates into one incident by failure fingerprint** — FEATURE — value 4 — effort M — risk low — category: failure triage
  Why: CI goes red once per sha (T-1810 filed one FIX per red sha), so one broken import can fill the backlog with duplicates. Assumption: failing gate output is stable enough to hash into a fingerprint.
  Done when: three queued tasks failing with the same traceback produce one incident card and one needs-you item.

- **Reconcile backlog against journal at session start and list the drift** — FIX — value 4 — effort M — risk low — category: state integrity
  Why: T-1802's midnight defer came from a state that surfaces trusted without a cross-check. A hand-edited backlog row with no journal event is invisible today.
  Done when: adding a backlog row by hand with no matching journal event makes `fm status` list it as drift with the fix command.

- **Refuse to file a close receipt when the journal has a sequence gap** — FIX — value 4 — effort S — risk low — category: receipt honesty
  Why: a receipt is the proof surface. If a middle event is lost, the close claim can't be checked. Assumption: journal events carry no sequence numbers yet.
  Done when: deleting one interior journal line makes `fm done` refuse and name the gap's position.

- **Freeze writes with one key and keep reads live** — FEATURE — value 3 — effort S — risk low — category: incident control
  Why: the panic stop halts runs, but a wedged writer also blocks `fm status`, so the user loses sight of the cause. A read-only freeze keeps the view while work stops.
  Done when: with writes frozen, `fm status` answers in under 1 s and every `fm task` write refuses and prints the freeze reason.

- **Run a weekly restore drill of the newest backup into a scratch directory** — FEATURE — value 3 — effort S — risk low — category: recovery
  Why: backup exists, but an unrestored backup is only an assumption. Restore is the step that gets skipped.
  Done when: the drill restores into a temp directory and `fm doctor` passes against it, or fails naming the file that didn't restore.

- **Judge hung children by CPU and open descriptors, not only transcript growth** — FIX — value 3 — effort S — risk low — category: stall detection
  Why: a child blocked on a dead pipe shows no transcript growth and no CPU, but a model thinking quietly can also look idle. Assumption: procfs is readable on the target Linux hosts.
  Done when: a child blocked on a pipe read is flagged stalled within the configured window, and a child that is thinking is not.

- **Stamp each state file with a generation number that readers compare** — FIX — value 3 — effort S — risk low — category: torn reads
  Why: the surfaces read backlog and journal on their own clocks, so a torn or stale read can show old state as current.
  Done when: a reader that sees a generation older than the last one it showed reloads and says so in its output.

- **Truncated model replies resume from their last complete step** — FIX — value 3 — effort M — risk med — category: run recovery
  Why: a reply cut at the output limit is currently treated as a whole reply. Assumption: the runner exposes a stop reason the harness can read.
  Done when: a reply cut at the output limit resumes from its last complete step, and the receipt names the resume.

- **Wild: a failure museum that reruns old failures nightly and marks which still happen** — FEATURE — value 3 — effort M — risk low — category: regression memory
  Why: wild: closed failures are archived, but nothing asks whether they still reproduce, so fixes can quietly regress. Done when: each recorded failure is rerun and its row reads "reproduces" or "gone" in the morning list.

- **Wild: a forecast that warns before the queue fails, from the trend of retries and timeouts** — FEATURE — value 3 — effort M — risk med — category: early warning
  Why: wild: retries and timeouts usually climb for several runs before a queue dies, and a trend line can page earlier than a failure does. Assumption: retry and timeout counts are already in the journal.
  Done when: a synthetic rising series raises the warning at least two runs before the failure fixture goes red.

- **Wild: a shadow state twin that replays every write and halts the queue on divergence** — FEATURE — value 2 — effort L — risk med — category: state safety
  Why: wild: a second writer that applies the same events to a copy would catch a silent write bug the moment the two states disagree. Assumption: events are deterministic enough to replay.
  Done when: a deliberately corrupted write to the twin halts the queue within one event and names the field that diverged.
