# Brainstorm — lens: performance

- **Read the git index directly to find changed files** — PERFORMANCE — value 4 — effort S — risk low — category: affected checks
  Why: assumption: `fm check --affected` shells out to `git status` on every run, and the pack notes that the affected and evidence paths still wait behind the machine-wide gate. Parsing `.git/index` stat data in Python (size, mtime, inode) finds the changed set with no subprocess.
  Done when: on a 5,000-file fixture, `fm check --affected` with no edits spawns zero `git` processes (checked with `strace -f -e execve`) and returns the same file list as `git status --porcelain`.

- **Single-flight identical checks across surfaces** — PERFORMANCE — value 4 — effort S — risk low — category: gate concurrency
  Why: the plugin, the CLI and the mod can each ask for the same `fm check` within seconds. The gate lock makes the second caller wait, then run the same work again. A keyed in-flight table lets concurrent callers with the same tree hash join the first run and get its result.
  Done when: three `fm check` calls launched within one second on an unchanged tree produce one gate run in the journal, and all three exit with its verdict.

- **Rebuild tests that touch only what a diff changed, from a coverage map** — PERFORMANCE — value 5 — effort M — risk med — category: test selection
  Why: "Select tests by co-change history" uses git history, which is noisy for new code. Recording each test's executed files once, then rerunning only tests whose traced files changed, matches what the diff actually touched (testmon-style). Assumption: the coverage map is stored in the repo's `.foreman` state and refreshed on each full run.
  Done when: after a one-line change in one module, `fm check --affected` runs only the tests whose recorded files include it, and a full run still passes with the same verdict.

- **Roll the journal up into per-day summaries for the charts** — PERFORMANCE — value 4 — effort M — risk low — category: History and Today
  Why: the Today and History charts re-read the whole journal to draw a week. A daily rollup file (counts, time, cost, gate verdicts) written once at each day's close lets both charts read a few kilobytes, and the rollup can be rebuilt from the raw journal if it is lost.
  Done when: rendering History for 90 days reads only the rollup files (verified by counting journal opens) and matches the numbers from a full journal scan.

- **Fail CI when a verb's startup import time exceeds its budget** — PERFORMANCE — value 3 — effort S — risk low — category: startup
  Why: every `fm` verb pays Python import cost before it does anything, and nothing stops a new import from slowing all of them. Running `python -X importtime` per verb in CI and failing above a per-verb budget catches the regression on the commit that adds it.
  Done when: adding a heavy import (for example `import pandas`) to a verb's module makes the CI startup check fail and name the verb and the import chain.

- **Store context-pack sections in a content-addressed chunk store** — PERFORMANCE — value 4 — effort M — risk low — category: context packs
  Why: each pack is rebuilt and re-hashed in full, and sections that did not change are read again. Storing each section as a chunk keyed by its hash lets a new pack reference unchanged chunks without reading or re-hashing them, and lets two projects with the same docs share one copy.
  Done when: rebuilding a pack after editing one section reads and hashes only that section (counted in the test), and the assembled pack is byte-identical to a full rebuild.

- **Schedule gates by their critical path through the dependency graph** — PERFORMANCE — value 3 — effort M — risk med — category: gate scheduling
  Why: gates run in a fixed order, so a slow gate at the end can leave other cores idle. Using measured durations from the journal to order a DAG of gates by critical path (longest remaining chain first) shortens wall time when gates are independent.
  Done when: on a fixture with one 40-second gate and eight 5-second gates, the scheduler finishes in about 40 seconds rather than the sequential total, with the same verdicts.

- **Pre-write the next run's journal segment during idle time** — PERFORMANCE — value 2 — effort S — risk low — category: journal writes
  Why: each event does a fresh file open and an fsync on the hot path. Preallocating the next journal segment while the machine is idle removes the open and allocation cost from the event that needs it. Assumption: fsync cost is visible on slow disks, not measured on this box yet.
  Done when: a benchmark of 10,000 journal appends shows no file creation on the append path and a p99 append under 1 ms on the test disk.

- **Snapshot the warm Foreman process at idle and restore it on the next prompt** — PERFORMANCE — value 3 — effort L — risk high — category: cold start (wild)
  Why: (wild) the cost that remains is the box plus startup, and the profile showed 124 s of CPU for a full read. A checkpoint of the warmed interpreter with its parsed rules and backlog (CRIU-style, or a pickled image restored at start) lets the first prompt after a pause skip the warm-up entirely.
  Done when: restoring the image takes under 50 ms on the test box, and the restored process produces the same `fm status` output as a cold start on the same state.

- **Speculatively run the model's likely next read-only tool call** — PERFORMANCE — value 3 — effort L — risk med — category: latency (wild)
  Why: (wild) when the model streams a `Read` or `Grep` near the start of its answer, the file it will ask for is usually predictable from the task. Starting that read in parallel, and discarding it if the model asks for something else, hides the tool round-trip. Assumption: the host lets a hook observe the stream early enough to act.
  Done when: in a recorded session, at least half of read calls hit the speculative cache, and a miss returns the same bytes as a normal read.

- **Batch every hook's file reads into one io_uring submission** — PERFORMANCE — value 2 — effort L — risk high — category: hook latency (wild)
  Why: (wild) each guard check opens and reads several small state files one after another. Submitting those reads as a single io_uring batch removes most of the syscall round-trips. Linux-only, so it stays optional behind a fallback to plain reads.
  Done when: the hook bench's PreToolUse:Bash median drops by at least 20 percent on Linux with the flag on, and the flag-off path passes the same bench unchanged.
