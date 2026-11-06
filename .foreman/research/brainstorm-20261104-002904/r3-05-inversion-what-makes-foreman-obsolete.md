# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Write spec examples as native doctests** — FEATURE — value 5 — effort M — risk low — category: portability
  Why: the top gap is meaning (599 unproven), and a criterion that lives only in Sampo's ledger vanishes if Sampo does. Assumption: most target repos have a doctest or example-test form (pytest `>>>`, Rust doc tests, Go `Example` funcs, shell bats).
  Done when: a spec example in a fixture repo becomes a doctest in that repo's own suite, passes under the repo's runner with Sampo uninstalled, and fails when the code is broken.

- **Add criterion kinds that call the repo's own runners** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: Sampo should orchestrate pytest, cargo, tsc, Playwright and the like, not reimplement them. Each kind maps an exit code and output to proven, unproven or failed.
  Done when: a criterion of kind `runner:<cmd>` closes a task using only the repo's declared command, and a missing runner yields "unproven: runner absent", not a pass.

- **Graduate criteria that keep passing into the repo's tests** — FEATURE — value 4 — effort M — risk med — category: lean
  Why: a criterion that never failed across N closes adds no signal inside Sampo, but it is a good regression test. Assumption: the repo's test suite can take a generated test file without clashing with its conventions.
  Done when: after N passing closes, `sampo` proposes a PR adding the criterion as a repo test, and once merged its Sampo-side check is marked "graduated" and no longer runs.

- **Detect criteria the host agent already verified** — FEATURE — value 4 — effort M — risk med — category: obsolescence
  Why: assumption: strong bare agents already run the spec example before Sampo's gate asks. When the transcript shows the same command run on the same tree hash, Sampo should reuse that result and record "self-verified" rather than rerun and nag.
  Done when: a transcript where the agent ran the example yields a close with source "host-run" and no second run; a different tree hash forces a rerun.

- **Keep an `UNPROVEN.md` in the repo** — FEATURE — value 4 — effort S — risk low — category: portability
  Why: the unproven shelf is Sampo-only state, so a teammate without Sampo never sees what is unchecked. A plain file is reviewable in PRs and survives uninstall.
  Done when: closing a task regenerates `UNPROVEN.md` with each unproven claim and its typed reason, and the file reads sensibly without Sampo installed.

- **Show a lock-in meter** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: obsolescence is healthy only if the user can leave without losing proof. The meter counts proofs, verdicts and criteria that exist only in Sampo's ledger and not in the repo, git trailers or CI.
  Done when: `sampo doctor` prints "N of M proofs exist only in the ledger" with the top three classes, and graduating one proof lowers N.

- **Say nothing when everything is proven** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the best verification output is silence when nothing is unproven. Today finish cards print proven and unproven counts, which adds noise on clean closes.
  Done when: a close with every criterion proven prints a single line, and any unproven item expands the card to the full shelf.

- **Rebuild the unproven shelf from git alone** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: cloud or fresh-VM agents have no local ledger. Verdicts written as commit trailers can be read back from a bare clone.
  Done when: in a fresh clone with an empty state directory, `sampo verify --from-trailers` reproduces the same proven/unproven counts as the original machine.

- **Blind transcript test (wild)** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: assumption: if a cold child reading two transcripts cannot tell which one ran under Sampo, the discipline has no visible effect. That would be a direct, outcome-based obsolescence signal not authored by Sampo.
  Done when: a harness takes N paired same-task transcripts (with and without Sampo), has a tool-less child guess which is which, and reports accuracy per capability. Near 50% flags that capability for retirement review.

- **Ask each new model to design its own harness (wild)** — FEATURE — value 4 — effort M — risk low — category: obsolescence
  Why: assumption: a new model release can say what scaffolding it wants, given only its own failure transcripts. This gives a model-authored view of what Sampo still owes it, not Sampo's own view.
  Done when: on a new model ID, a tool-less run reads recent failure transcripts and outputs a harness spec in at most 40 lines, and a diff against current Sampo verbs lists "wanted but missing" and "present but unwanted".

- **Generate a shell-only fossil checker each release (wild)** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: if Sampo or its Python breaks, the user still needs a way to re-run every compiled criterion. A generated `verify.sh` using only grep, jq and the shell is that fallback.
  Done when: each release regenerates `verify.sh` from the current criteria, and it runs in a container with only bash, grep and jq and agrees with Sampo on all fixture verdicts.

- **Render a proven-claims badge from the claims table (wild)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: a static SVG badge reading "claims proven 412/833" in the README is something users show others. It is generated locally, makes no network call, and names no vendor or machine.
  Done when: the badge is regenerated at close from the claims table, matches the table's counts, and contains only role words.

- **Report a model-free proof share (wild)** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: assumption: the healthiest direction for a verification layer is more proof that needs no model at all. A single ratio shows whether Sampo is shrinking its model dependence or growing it.
  Done when: `sampo doctor` prints the share of proven claims whose check involved no model call, and a fixture with one model-judged and one command-judged claim reports 50%.

Next question: which of Sampo's gates does a bare strong model already pass unprompted on the user's own closed tasks, measured from existing ledgers with no new runs?
Next question: if a user wanted to leave Sampo tomorrow, what would they have to rebuild by hand, and does anything in the product show them that list before they ask?
