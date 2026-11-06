# Brainstorm — lens: approaches

- **Push the one matching playbook in from a prompt hook** — PERFORMANCE — value 5 — effort M — risk med — category: routing
  Why: the cost at 10,000 entries is the listing itself. A `UserPromptSubmit` hook could select and inject one body per prompt, so always-loaded text stays flat. Assumption: the hook's latency fits the prompt budget.
  Done when: with 10,000 synthetic playbooks, added context per prompt stays under 1 KB and the hook's p95 stays inside the bench budget.

- **Install playbooks per project from a lock file, like dependencies** — FEATURE — value 5 — effort M — risk low — category: install
  Why: a repo declares the playbooks it uses, and only those reach its listing. "Not all loaded" becomes a property of install, not runtime. Assumption: most projects use under 50 playbooks from the library.
  Done when: `fm install` in a fresh repo lists only locked playbooks, and `fm doctor` fails when a playbook the repo's history uses is missing from the lock.

- **Route with ripgrep over a frontmatter sidecar, with no index to build** — PERFORMANCE — value 4 — effort S — risk low — category: routing
  Why: a compiled index can go stale. A sidecar of names, triggers and descriptions, searched with `rg`, needs no build step and no daemon. Assumption: `rg` is on the target machine, which `fm doctor` can check.
  Done when: a query over 10,000 sidecar lines returns the top three matches in under 50 ms on the bench box, and a test fails when the sidecar drifts from the playbook files.

- **Let a cheap subagent pick the playbook, so the main context never holds the catalog** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: the picker reads the catalog in its own window and returns one name, so the main session pays only for that answer. Assumption: the picker's cost is below the context it saves.
  Done when: a 10,000-entry catalog adds under 500 tokens to the main session per routing decision, as measured by `fm cost`.

- **Route by a local embedding model, not keywords** — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: keyword triggers miss paraphrases. A local embedding model ranks by meaning with nothing sent off the machine. Trade-off: a model download and a few hundred MB on disk.
  Done when: on 200 labelled prompts, recall@3 beats the keyword router by a stated margin, and a test that blocks sockets passes.

- **Sign each playbook body and refuse one that changed since install** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: playbooks steer tool use, so an edited body is a prompt-injection path. Hashing at install and checking at load closes it. Assumption: playbooks are shared across machines or repos.
  Done when: changing one byte of a playbook body makes the loader refuse it and name the file.

- **Verify each playbook's example before it is listed** — CLEAN — value 4 — effort M — risk low — category: quality
  Why: a playbook whose example no longer runs is dead weight and a hazard. Listing only the passing ones shrinks the catalog and its risk together.
  Done when: `fm playbooks check` fails on a playbook whose example no longer runs, and that playbook is absent from the routed listing.

- **Generate a missing playbook on demand and promote it on its second match** — FEATURE — value 3 — effort L — risk med — category: learning
  Why: instead of writing ten thousand playbooks up front, a prompt that matches nothing yields a draft in a staging folder. It moves to the library only after a second matched use. Trade-off: tokens on first use and quality risk.
  Done when: an unmatched prompt produces a staged draft, and the draft is listed only after a second matched use.

- **Prefetch the playbook for the next queued task while the current one runs** — PERFORMANCE — value 2 — effort M — risk low — category: latency
  Why: queued tasks have known subjects, so routing can happen off the critical path. Assumption: the queue order is stable enough that most prefetches are used.
  Done when: the first routing of a queued task reads a warm cache entry in under 5 ms.

- **Encode the catalog as a frequency-sorted name table** — PERFORMANCE — value 2 — effort S — risk low — category: tokens
  Why: the catalog repeats long names on every turn. Short codes for the playbooks that fire most cut the listing's size and leave the rare ones spelled out. Assumption: firing follows a skewed distribution, which the journal can confirm.
  Done when: the encoded listing is at least 30% smaller than the plain one on the last month's journal, and every code decodes back to its name in a test.

- **Wild: replay a past success as the worked example, not the playbook text** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: a playbook says what to do, but a transcript that succeeded shows it. Loading one trimmed success gives the model a precedent. Trade-off: old transcripts go stale, so each one needs a version pin. (wild)
  Done when: a routed task loads one trimmed transcript, and its pass rate beats the text-only version on the bench cases.
