# Brainstorm — lens: unspoken needs

- **Make a fresh install pass its own `fm doctor`** — FIX — value 5 — effort S — risk low — category: onboarding
  Why: Finding A8: a clean install fails its own doctor (missing backup) and prints 40 lines of passes. The first command a newcomer runs should end green, or with one line naming the first fix.
  Done when: in a clean HOME, `install.sh` followed by `fm doctor` exits 0 and prints at most 3 lines. A check that can't apply yet shows "not yet" rather than FAIL.

- **Put `fm` on the shell PATH, and never shadow another `fm`** — FIX — value 5 — effort S — risk med — category: onboarding
  Why: Finding A3: `fm` is "command not found" in a plain shell, yet the README says "run fm …" everywhere. `fm` also collides with other programs of that name (assumption: file managers on some distros).
  Done when: a fresh login shell resolves `fm`. If a different `fm` already exists on PATH, the installer says so, installs `foreman` as the alias, and README examples work with either.

- **Show the full `~/.claude` diff at install and let the user decline each change** — SECURITY — value 5 — effort M — risk med — category: trust
  Why: Finding A2: bypassPermissions, outputStyle, 70% autocompact, a statusline wrapper and 20 deny rules are set silently. Rivals only add commands. This is the biggest trust ask in the product.
  Done when: `install.sh` prints each wiring change with a one-line reason and a y/n prompt (default shown). `--dry-run` writes nothing. `--yes` reproduces today's result. Declining bypass leaves the guard on in the previous mode.

- **Offer bypass only after Foreman has earned it** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: The user wants "THE plugin" but the default is a large trust ask. Assumption: a newcomer who has watched the guard block something is far more willing to say yes.
  Done when: after the 5th held task, or the first guard block, one yes/no appears with a receipt ("5 tasks held, 2 commands blocked"). Saying yes switches the mode and `fm doctor` shows the reason.

- **Grade folded tasks through their parent** — FIX — value 4 — effort S — risk low — category: honesty
  Why: Finding C: of 370 tasks done in 7 days, 159 are folded into other tasks and show as "ungraded" in `fm digest`. That hides the real strong/ok split.
  Done when: a folded task inherits its parent's grade. On last week's data, ungraded falls below 5% and the digest says "folded into T-x".

- **Stop `fm repeats` suggesting single test modules as every-task gates** — FIX — value 4 — effort S — risk low — category: correctness
  Why: Finding C: the most-repeated commands are the full runner (1,586 calls), unittest (281) and one plugin test (124). The tool currently recommends the narrow module, which is bad advice.
  Done when: given the C-section command histogram, `fm repeats` proposes the full-suite command, and a test fixture asserts it never proposes a path to a single test file.

- **Make the `fm task done` refusal print a prefilled `fm task finish` call** — FIX — value 4 — effort S — risk low — category: onboarding
  Why: Finding A9: `done` refuses with 4 bullets and the one-call `finish` shortcut is buried. The refusal already knows the missing pieces.
  Done when: the refusal's last line is a copy-pasteable `fm task finish …` with the known flags filled in. Running it on the refused task closes it.

- **Warn when `fm task new` duplicates an open capture, and offer to adopt it** — FIX — value 3 — effort S — risk low — category: queue
  Why: Finding A6: `capture` then `task new` without `--from` makes a duplicate. `task new --help` also lists no valid `--type` or `--tier` values and no example.
  Done when: `task new "same text"` after a capture prints "adopt capture C-n? (--from C-n)". `--help` lists the types, tiers and one example.

- **Keep the clean-HOME newcomer walkthrough as a permanent no-model gate** — FEATURE — value 4 — effort M — risk low — category: regression
  Why: Findings A1–A11 came from one manual run. Without a script they will regress, and rounds 2–3 show internal polish is exhausted.
  Done when: a script in a temp HOME runs install, init, status, capture, task new, check, doctor and uninstall, and asserts on A3, A4, A5, A8 and A10 (PATH, help length, empty-status text, doctor green, no residue). It runs in the gate list and fails if any regresses.

- **Publish the real held-rate with its denominators** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: Finding C: 670 of 688 tasks held and 18 were fixed later (2.6%), but the bench has 1 case and no public evidence. These numbers exist today and can be shown honestly.
  Done when: `fm stats --readme` emits a redacted block (held, reworked, graded-strong, n, window) and says "self-reported, one user" when n comes from one machine. The README includes it.

- **Add a "when not to use Foreman" section** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: The README's first screen is abstract (A1). Rivals sell breadth. Saying who it's not for builds trust and shortens the pitch. Assumption: the user hasn't written this.
  Done when: the README has 5 plain lines on when to skip Foreman, plus a before/after example of one refused "done" on a failing test.

- **Wild: Give repos a "Foreman-verified" badge backed by a proof pack** — FEATURE — value 3 — effort M — risk med — category: reach — wild
  Why: assumption: "THE plugin" means other people must see it. A badge in a repo's README links to the held-rate and evidence for the last N tasks, so every repo becomes a signpost.
  Done when: `fm badge` writes an SVG and a redacted proof page. The page contains no paths, usernames or secrets, which a test checks with a scrubber.

- **Wild: Collect an opt-in, verb-only usage census across users** — FEATURE — value 3 — effort M — risk high — category: simplicity — wild
  Why: Finding C: 46 of 108 verbs were never run by Claude in 11 days, but that is one user's data. Pruning to about 70 verbs needs more than one machine.
  Done when: `fm census --send` shows the exact payload (verb name and count only) before any upload, and is off by default. With the setting unset, no request is made, which a test confirms.

- **Wild: Offer a "first real task" tour on the newcomer's own repo** — FEATURE — value 3 — effort L — risk med — category: onboarding — wild
  Why: A5 and A11: `fm init` prints a random slug and the jargon is unexplained. Assumption: a newcomer learns fastest by watching one tiny real fix on their own code.
  Done when: `fm tour` picks a TODO or small lint issue, walks capture, plan, verify and finish in plain words with a glossary line per term, and ends with `fm undo`-style cleanup. A scripted fixture repo runs it end to end without a model.
