# Brainstorm — lens: approaches

- **Put `fm` on the shell PATH at install** — FIX — value 5 — effort S — risk low — category: onboarding
  Why: evidence A3: `fm` exists only inside Claude sessions, so the README's "run fm …" gives "command not found" in a normal shell.
  Done when: in a clean HOME after `install.sh`, `bash -lc 'fm help'` exits 0, and uninstall removes the shim.

- **Ask three install questions, with a `--plan` preview** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: evidence A2: the default install adds bypass mode, third-party plugins, a statusline wrapper and 20 deny rules, and says only "confirm once". Approach: on a TTY, ask about bypass, plugins and statusline (the Enter default keeps the current setting). `--plan` writes nothing and prints the exact settings diff.
  Done when: `install.sh --plan` in a clean HOME leaves `~/.claude` byte-identical and lists every key it would change.

- **Rewrite the README's first screen from the ledger** — FEATURE — value 4 — effort S — risk low — category: docs
  Why: evidence A1: the first screen is abstract, with no demo and no before/after. Approach: generate a redacted real before/after of one finished task, plus a table of "what this changes in ~/.claude".
  Done when: the README opens with a ≤15-line before/after and a footprint table, and a test fails if the table drifts from the installer's actual writes.

- **Make `fm task new` forgiving** — FIX — value 3 — effort S — risk low — category: onboarding
  Why: evidence A6: a capture followed by `task new` without `--from` makes a duplicate, and `--help` lists no valid `--type` or `--tier` values or an example.
  Done when: `task new` with a title matching an open capture adopts it (or asks once), and a bad `--type` error lists the valid values.

- **Keep removed verbs as one-line forwards** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: evidence D: the CLI could go from 108 verbs to about 70 by merging (`fm inspect`, `fm stats`, `fm auto`), and several of those verbs were user requests. A tombstone prints "now `fm inspect sym`" and still runs. Trade-off: it leaves a small alias table to maintain, but nothing is deleted.
  Done when: every pre-merge verb in a fixture list still exits with its old behaviour, and `fm help` shows only the merged names.

- **Stop `fm repeats` proposing single test modules as gates** — FIX — value 3 — effort S — risk low — category: reliability
  Why: evidence C: it suggests per-module test commands as every-task gates, which would pass while the rest of the suite is broken.
  Done when: on a fixture with 5 repeated single-module calls, it proposes only the whole-suite command or nothing.

- **Give folded tasks their parent's grade in `fm digest`** — FIX — value 3 — effort S — risk low — category: observability
  Why: evidence C: 159 of 370 tasks done in the last 7 days show as "ungraded", which hides the real verification picture.
  Done when: the digest reports 0 ungraded for tasks folded into a graded parent, and the fold relation is shown.

- **Publish the held-rate as a self-updating evidence page** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: evidence C: 670 of 688 finished tasks held, and 18 were fixed later (2.6%), yet "no published evidence Foreman helps". Say plainly that this is a reopen rate, not a benchmark. Approach: use the ledger, with no model calls.
  Done when: `fm page --proof` renders the rate, its method and its caveats, offline, with usernames and paths redacted.

- **Split the install into core and labs plugins** — FEATURE — value 4 — effort L — risk high — category: simplicity
  Why: evidence D: roughly 4.5k lines (the session layer, the bench stack, the ecosystem verbs) are rarely used but load for everyone. Approach: reuse marketplace multi-plugin support, keeping guard, resume, the done gate and the queue in core.
  Done when: a core-only install passes `fm doctor` and the e2e roundtrip, and SessionStart context plus rules shrink by a measured amount.

- **Merge the seven `_git` helpers into one module** — CLEAN — value 2 — effort S — risk low — category: maintainability
  Why: evidence D lists seven copies. Behaviour differences (timeouts, env, cwd) are likely accidental.
  Done when: one `fmgit` is imported everywhere, `grep -c "def _git"` over `plugin/lib` is 1, and the full suite is green.

- **Add a one-file "Foreman Seed" for marketplace install** — FEATURE — value 4 — effort M — risk med — category: distribution (wild)
  Why: evidence B: every rival is one `/plugin install` away and doesn't rewrite `~/.claude`. Approach: the marketplace entry is a tiny seed skill. On first use it shows the `--plan` preview and runs the real installer only after consent.
  Done when: `/plugin install` of the seed changes nothing in `~/.claude` until the user says yes.

- **Offer a week of observe-only mode beside the user's current plugin** — FEATURE — value 4 — effort L — risk med — category: adoption (wild)
  Why: evidence B and A2: switching from superpowers or ECC is a big trust ask. Approach: Foreman runs read-only and sends a weekly catch report with the commands it would have blocked and the "done" claims it would have refused.
  Done when: in observe mode, a fixture session records "would block" entries and no gate actually fires.

- **Run the installer as a Foreman task that prints a receipt** — FEATURE — value 3 — effort M — risk low — category: delight (wild)
  Why: the first demo of "verify with recorded evidence" is the install itself, with criteria such as hooks wired, doctor green and backup taken.
  Done when: a clean install ends with a receipt that lists each criterion and its evidence line, and fails visibly if one doesn't hold.
