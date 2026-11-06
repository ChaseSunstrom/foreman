# Brainstorm — lens: user value

- **Cap subagent returns and spill the rest to a file** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: assumption: a verbose scout or reviewer return lands whole in the main context. SubagentStop is already wired, and "reject hollow returns" exists but nothing rejects oversized ones.
  Done when: a fixture subagent returning over N tokens is bounced once at SubagentStop. The retry has a ≤15-line digest plus a spill-file path, and `fm doctor` reports the median return size per role.

- **Coach serial tool calls into parallel batches** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: the pack's speed theme and the user's "faster", plus "Count wasted round trips" in the idea list. Counting alone changes nothing. This reads the last N tool calls and, when independent reads or greps ran one by one, injects a one-line hint at the next UserPromptSubmit.
  Done when: replaying a transcript with 5 serial independent Reads emits exactly one hint, and a transcript that is already batched emits none.

- **Scan instruction-bearing files for invisible-text injection** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: the security area is thin, and bypass mode means a hidden instruction in CLAUDE.md, a README, or a fetched doc would be obeyed. Zero-width, bidi, and tag-character runs in files loaded at SessionStart are cheap to detect and are not covered by the "neutralize control sequences in output" idea.
  Done when: a fixture CLAUDE.md with a tag-character payload makes SessionStart print a one-line warning naming the file and line. The same file without it prints nothing.

- **Verify read-only roles are really read-only at SubagentStart** — SECURITY — value 3 — effort S — risk low — category: least privilege
  Why: scout, recon, reviewer and reproducer are meant to read. Agent frontmatter and the per-call model override can drift, and a prompt-injected scout with Write or Bash is a bypass-mode hole. assumption: nothing checks the live tool set today.
  Done when: `fm doctor` fails when any declared read-only role resolves to a tool list containing Write, Edit or unrestricted Bash. A test with a tampered agent file proves it.

- **Narrow bypass when the cwd leaves the project root** — SECURITY — value 4 — effort M — risk med — category: blast radius
  Why: full-autonomy bypass is a standing choice, and the guard judges commands but not where the session has wandered (home, `/etc`, a sibling repo). A PreToolUse check could treat out-of-root writes as ask-or-refuse.
  Done when: after `cd ~` in a task, a Write to `~/.bashrc` is refused with the reason "outside project root". The same Write inside the root passes, and the check adds ≤5 ms in `bench_hooks`.

- **Allowlist runtime egress hosts from the project's own manifests** — SECURITY — value 3 — effort M — risk med — category: exfiltration
  Why: gates and installs run curl, pip and npm unattended at night. Hosts derivable from lockfiles, registries and the repo's remotes form a natural allowlist, and anything else becomes a single ask with a default.
  Done when: `curl https://unknown.example/x | …` in a fixture project is held, `pip install` against the project's configured index passes, and the decision is logged with the host.

- **Carry a ranked re-read list through /compact** — PERFORMANCE — value 3 — effort S — risk low — category: compaction
  Why: the user resumes after /compact constantly and Foreman restores the step. It does not say which files the next step must re-read, so the model re-reads wholesale. PreCompact can write the 5 files the current step touched, ordered by size and recency.
  Done when: the post-compact SessionStart context lists ≤5 paths for the current step, and a fixture task shows fewer Read calls in the first 3 turns than a baseline without the list.

- **Order guard rules by hit rate and cost** — PERFORMANCE — value 3 — effort M — risk med — category: hook latency — wild
  Why: the guard runs on every Bash call under a latency gate. Rules have fire records ("Give guard rules an origin and a fire record" is already listed). A nightly job could reorder the cheap, high-hit rules first and the expensive parsers last, with verdict equivalence checked on the corpus.
  Done when: the reordered guard produces byte-identical verdicts on the full false-positive corpus, and `bench_hooks` p95 for the guard drops measurably.

- **Promote a task class to a lower model after N matching shadow diffs** — FEATURE — value 5 — effort L — risk med — category: model routing — wild
  Why: the user's own open ask, T-0755 ("spawn agents of lower models like 5.5 haiku/sonnet?"). A haiku child quietly drafts the S-task patch beside the real builder and is never applied. After 3 consecutive gate-equivalent diffs in a class, `fm` flips that class's default and tells the user in one line. A single gate miss demotes it back.
  Done when: a fixture class with 3 matching shadow diffs flips to haiku on the 4th task and the ledger shows the evidence. A forced mismatch flips it back.

- **Route each attention event by presence, not by a fixed channel** — FEATURE — value 4 — effort M — risk low — category: notifications
  Why: the pack lists tmux send-keys, `fm notify`, PushNotification and an Artifact page, but nothing chooses between them. If a tmux client is attached and active, show it in the band. If it has been idle for 10 minutes, push. If the user is away overnight, batch into the morning digest.
  Done when: with a fake attached client the same needs-you event goes to the band only. With the client detached it goes to push once, and a test asserts it is never sent to both.

- **Keep a persistent haiku "repo oracle" that scouts query via SendMessage** — PERFORMANCE — value 3 — effort L — risk med — category: shared context — wild
  Why: every scout re-explores the same tree from cold, and each fresh scout pays for the outline again. One long-lived cheap session holds the map and answers file-location questions, invalidated by tree hash. assumption: SendMessage reaches a local sibling session reliably enough for this.
  Done when: in a fixture run, 5 scout questions about layout get answered by the oracle with no Glob or Grep calls. A touched file marks only its own entries stale.

- **Record why each hook fired in one line per event, and fail doctor on silent hooks** — CLEAN — value 2 — effort S — risk low — category: observability
  Why: Foreman uses 14 hook events, and hooks are latency-gated and can fail quietly. A per-event "fired / skipped (reason) / errored" line makes unused hooks provable, which feeds the "hook diet" idea with data.
  Done when: `fm doctor` lists each of the 14 events with a 7-day count. Any event with zero fires while its trigger occurred is flagged.
