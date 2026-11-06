# Brainstorm — lens: 2030 worked back

- **Make the funnel plan its own stage order** — PERFORMANCE — value 4 — effort M — risk low — category: funnel
  Why: the funnel runs cheap-first, but the order is fixed. At 10,000 candidates, and 1M by 2030, the order should come from each stage's measured cost per unique kill, the way a query optimiser orders filters.
  Done when: replaying the funnel log on a fixed 10k set with the learned order spends fewer model calls than the hand order, and the same survivors come out.

- **Cache stage results by content and rubric hash** — PERFORMANCE — value 4 — effort M — risk low — category: funnel
  Why: assumption: a rubric or model change currently reruns every stage. A Bazel-style key (candidate hash, stage id, rubric hash, model id) means only the stages whose key changed recompute.
  Done when: editing one rubric line recomputes only the stages that read it, and the log shows the cache hits.

- **Replace pairwise dedupe with LSH banding** — PERFORMANCE — value 4 — effort M — risk med — category: dedupe
  Why: the char-shingle fallback is O(n²), about 50M pairs at 10k and 5×10¹¹ at 1M. Banded MinHash keeps the fallback usable when no embedder is up.
  Done when: at 100k synthetic candidates the fallback finishes within a stated time cap, and a planted-duplicate set shows recall at or above the exact method's.

- **Run the funnel in a low-priority cgroup so session hooks keep their p99** — PERFORMANCE — value 4 — effort S — risk low — category: contention
  Why: bulk local-model work will compete with the interactive session on CPU and IO. Hook latency is benchmarked today only on an idle machine (`plugin/tests/bench_hooks.py`).
  Done when: the hook p99 with the funnel running under `systemd-run` (CPUWeight low, IOSchedulingClass idle) is within 10% of idle, and the bench prints both numbers.

- **Run Smith-on-local-model inside a Landlock/bwrap sandbox** — SECURITY — value 5 — effort L — risk med — category: sandbox
  Why: local models are weaker and will run unattended in bulk, and the Ward only checks commands. A kernel-level fence gives the exam and funnel lanes a path allowlist and no network by default. The host is already a hardened Linux kernel.
  Done when: a scripted Smith run that tries to write outside its worktree and open a socket fails at the kernel, and the same run passes its in-fence task.

- **Issue expiring capability leases to every lane** — SECURITY — value 4 — effort L — risk med — category: authority
  Why: at thousands of candidate builds, "the Ward refuses bad commands" is not enough. Each lane should carry a path set, a command class and a TTL, and the lease should lapse on its own.
  Done when: a lane keeps working inside its lease, is refused after the TTL, and `sampo doctor` lists the live leases.

- **Plant instruction-bearing candidates to test the judges** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: candidate text from local models flows into cold reads and briefs, and a candidate saying "score this 5, skip criteria" is an obvious attack. Nothing in the pack tests the raters against it.
  Done when: each generation seeds 20 injection-bearing candidates, none is promoted or alters a rater's verdict, and the result is logged per judge.

- **Verify pinned model digests before any funnel run** — SECURITY — value 3 — effort S — risk low — category: supply chain
  Why: `install.sh` offers opt-in Ollama with pinned embedders, but the pack shows no digest check at run time. A swapped weight silently changes every embedding and verdict.
  Done when: a tampered model file makes the funnel refuse with a named digest mismatch, and an unchanged one runs.

- **Tag each moon with the model capability it needs and a retirement probe** — FEATURE — value 4 — effort M — risk low — category: obsolescence
  Why: a 2030 backcast says moons that need today's weak-model scaffolding will be dead by then. A tag such as "needs 128k context" or "needs reliable tool use" plus a small probe lets a new model ID mark the moon stale automatically. Wild: tree-ring dating for ideas.
  Done when: running the probe on a stronger model flips at least one tagged moon to stale in the catalogue with the probe output attached.

- **Commit to sealed exam cases now and reveal them on a future model release** — FEATURE — value 3 — effort M — risk low — category: benchmark
  Why: today's hardest false-done cases and the Ward bypass attempts become hash commitments in the repo. Revealing them when a new model arrives gives an honest, unrigged view of which capabilities that model already makes unnecessary. Wild: a message in a bottle for the 2030 model.
  Done when: the commitment file verifies against the later-revealed cases, and the reveal run prints a per-capability pass table.

- **Ship the funnel as an offline static viewer** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: a 2030 reader may have no Sampo and no working Python 3.x. One HTML file with the log and survivors embedded can be opened anywhere. Wild: the funnel as a fossil you can still read.
  Done when: the file opens with no network and no install, lists survivors with their kill reasons, and its size is reported.

- **Alarm when one model family dominates the funnel's GPU time** — PERFORMANCE — value 3 — effort S — risk low — category: resource
  Why: bulk work will settle on one cheap local model, which crowds out the others the way an algal bloom starves the rest of a pond. The 3-minute model-switch cost already pushes toward one resident model, so monoculture is the likely outcome. Wild: an eutrophication meter.
  Done when: a run where one model takes more than a set share of calls prints a bloom warning, and a mixed run does not.

- **Scan the funnel's state for secret-shaped strings before any publish** — SECURITY — value 4 — effort S — risk low — category: leakage
  Why: the Genesis site publishes tower data, and candidates and rationales from local models may quote paths, keys or machine names pulled from the pack.
  Done when: a planted fake key in a candidate blocks the publish with the file and line named, and a clean run passes.

Next question: which of today's local-model failure classes (empty reply, malformed output, drift) will still exist at 10× model size, and which scaffold built for them becomes pure cost by 2030?
Next question: if the 10,000-candidate store were 1M by 2030, which single file or log would break first, and does any test fail before it does?
