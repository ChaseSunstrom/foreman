# Brainstorm — lens: 2030 worked back

- **Search the user's own scripts before any registry** — FEATURE — value 4 — effort S — risk low — category: privacy / tool search
  Why: assumption: a missing tool is often already in the user's `~/bin`, shell functions, dotfiles or repo `scripts/`. Local-first search sends nothing out and makes the new build redundant. Registry search is the only source the pack lists.
  Done when: with a planted `~/bin/foo-lint`, a gap record for "foo lint" resolves to that path with zero network calls and an offline log line.

- **Scrub tool-search queries before they leave the machine** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: assumption: gap queries are built from task text, which carries repo names, paths and ticket text. The pack has scans for injected text and evidence, but none for the search query itself.
  Done when: a test query containing a planted repo name and a planted token reaches a stub registry as a generic capability phrase, and the egress ledger shows the redaction.

- **Rank queued install grants by the work they block** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: the mission says "install grants queued", and blocked items like T-0325 (libappindicator) sit unranked. Assumption: the user clears them in file order, not by value.
  Done when: `sampo tool grants` lists each grant with the count and age of the tasks and gaps it blocks, ordered by that count, and the order flips when a planted task is added.

- **Gate tool promotion on a cold-start budget** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: `bench_hooks.py` is a ship gate, but forged tools have no latency gate. A tool that is slow on every call quietly taxes every lane. Assumption: Python stdlib tools start in 40–150 ms.
  Done when: promotion fails for a planted tool that sleeps 400 ms at import, and each shelf entry records its p95 start time.

- **Keep a warm sandbox pool for forged tools** — PERFORMANCE — value 3 — effort M — risk med — category: performance
  Why: assumption: a bwrap/landlock setup per call dominates the latency of tiny tools used hundreds of times a night. Reuse is only safe if state is wiped between calls.
  Done when: 50 sequential calls of a no-op tool run at least 3x faster than cold-per-call, and a planted file written by call 1 is absent in call 2.

- **Explain why a tool wasn't used** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: Tool selection is hidden. The pack's standing rule is that a capability must be called by a real session path, but no verb says why a shelf entry was skipped.
  Done when: `sampo tool why <session> <tool>` prints one of: not retrieved, retrieved but not chosen, chosen but blocked by the Ward, or description too long for the model's context. A test covers each case.

- **Pick the forge language from the target repo's toolchain** — FEATURE — value 3 — effort M — risk med — category: tool building
  Why: the stdlib-only Python rung assumes `python3 -I` is present. Target repos in Rust, Go or Node may lack it, and a tool in their own language is more adoptable. Assumption: forge currently defaults to Python.
  Done when: in a fixture Go repo with no Python on PATH, a gap for "check JSON files" yields a tool with passing tests in Go, and the choice and its reason are recorded.

- **Generate shell completions and man pages from tool passports** — FEATURE — value 2 — effort S — risk low — category: developer experience
  Why: assumption: forged tools are only reachable through the dispatcher, so the user can't tab-complete or `man` them. The passport already holds the verbs, flags and examples.
  Done when: `sampo tool completions bash` emits a script that completes a planted tool's flags, and `man` renders its passport.

- **Lint tool compositions against their result footers** — CLEAN — value 3 — effort M — risk low — category: tool building
  Why: tools are meant to end with a typed result footer (idea above). Nothing checks that tool A's output can feed tool B. Small models chain tools badly, and a static check is free.
  Done when: a planted pipeline whose second tool expects a field the first never emits fails the lint with the field name, and a valid pipeline passes.

- **Approve a grant from the phone with a one-time signed link** — FEATURE — value 3 — effort M — risk high — category: devices
  Why: unattended nights stall on grants only the user can give. Assumption: the user has a phone on the same LAN or VPN. The link must be single-use, scoped to one tool and one hash, and honoured by nothing else.
  Done when: a link approves exactly one planted grant once, a second use and a hash-mismatched tool are both refused, and the Ward still checks the install command.

- **Wild: Exchange tool specs between installs, never code** — SECURITY — value 4 — effort L — risk med — category: supply chain / sharing
  Why: wild. A shared spec (passport, doctests, failing tests) can be rebuilt locally from scratch under the Ward, so no foreign code is ever run. This sidesteps most of the 18-idea supply-chain cluster in T-0791.
  Done when: install B imports install A's spec bundle with zero executable files in it and forges a tool that passes the bundled tests, with provenance noting the spec's source.

- **Wild: Dictate a missing tool from a phone** — FEATURE — value 2 — effort M — risk med — category: devices
  Why: wild. A spoken sentence such as "I keep wishing I could diff two lockfiles" is the lowest-friction gap source, and the pack's surfaces are only the web UI and terminal. It becomes a Wanted-board entry with tests drafted by a local model.
  Done when: an audio or text sentence posted to the local endpoint appears as a Wanted entry with at least one drafted failing test, and nothing is built until it is approved.

- **Wild: Measure how often each model invents a tool that doesn't exist** — FEATURE — value 4 — effort M — risk low — category: small-model exams
  Why: wild. The standing steer is to match frontier results with 4B–27B models. Hallucinated tool names and flags are the characteristic small-model failure. Louhi can offer a shelf of 5 real tools and 1 absent one the task seems to need, then score invented calls against correct "I need a grant" answers.
  Done when: `sampo louhi models` prints a per-model hallucinated-call rate on the shelf scenarios, and a planted model that always invents a tool scores 100%.

Next question: Which gaps in the user's last 30 days were solved by the user's own hand-written script rather than any registry, and does the forge ever look there first?
Next question: If registries, MCP and host skill stores are all signed and curated by 2030, what share of today's quarantine and cold-read work becomes pure overhead, and what measurement would show it early?
