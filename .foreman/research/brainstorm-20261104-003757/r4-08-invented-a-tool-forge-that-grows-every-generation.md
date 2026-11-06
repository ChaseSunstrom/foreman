# Brainstorm — lens: invented: a tool forge that grows every generation

- **Grow the forge by generation, with a ledger of what each generation added** — FEATURE — value 4 — effort M — risk low — category: forge growth
  Why: Mission 7 says the forge is "grown every generation", yet the pack shows no per-generation record of tools, cards and playbooks added or retired.
  Done when: `sampo forge ledger` prints, for each generation, counts of tools and cards added, retired and called on a real path, and `sampo genesis check` fails if a generation has no row.

- **Mint a tool-shape template from every repeated hand-built script** — FEATURE — value 4 — effort M — risk med — category: tool mining
  Why: The ideas list says to mine repeated shell pipelines and closed-task scripts. The "Missing tool shellcheck" item was dropped by hand, and no template pipeline exists. Assumption: the closed-task ledger keeps the commands that were run.
  Done when: given three closed tasks that ran a similar pipeline, the verb proposes one passport with a failing-first test, and a held-out fourth task uses it.

- **Add a stdlib-only lint pack for the commonest shellcheck findings** — FEATURE — value 3 — effort M — risk low — category: tool building
  Why: shellcheck was dropped under the no-installs rule, and `install.sh` is currently only checked with `bash -n`. This is a real, concrete case of a missing tool the rules say to build rather than install.
  Done when: the lint catches unquoted variables, `cd` without `||`, and `[ ]` against unset names in a seeded script corpus, with zero hits on the repo's own passing scripts.

- **Run a build-off between the 27B and the frontier model on each gap, judged only by the gap's own tests** — EXPERIMENT — value 4 — effort M — risk low — category: tool tournament
  Why: The steer is that local models match frontier through scaffolding. A tool the gap's tests accept is the cleanest signal for that, and Louhi already has the arms.
  Done when: `sampo louhi forge` writes a table of pass rate, wall time and tokens per model across at least 10 gaps, and it appears in the Models section.
  (Type mapped to FEATURE: Louhi arm.)

- **Keep a forge shelf of passports that load lazily on first call** — PERFORMANCE — value 3 — effort S — risk low — category: context cost
  Why: Context cost is a recurring worry in the pack (2,733 chars and 75,758 tokens). A growing forge must not enlarge the start text.
  Done when: with 200 passports on the shelf, SessionStart size is unchanged within 1%, and a call to one loads exactly its own passport.

- **Verify each forged tool in a no-network, scratch-write cage before its first real use** — SECURITY — value 5 — effort M — risk med — category: quarantine
  Why: Mission 7 requires "tests it, uses it". The injection and supply-chain defences (T-0791) are still deferred, so a tool built by a 4B model must not touch the network or the repo on its first run.
  Done when: a planted tool that opens a socket or writes outside its scratch directory is refused, and the refusal is a distinct, logged verdict.

- **Turn each Ward refusal of a legitimate intent into a safe-equivalent tool gap** — FEATURE — value 3 — effort M — risk med — category: gap mining
  Why: Ward blocks are a gap source nobody has used. A refused `rm` of state could become a `prune --plan` tool. Assumption: Ward logs the refused intent with enough context.
  Done when: five refusals from the log each yield a gap record, and at least one becomes a tested tool with no Ward exemption.

- **Retire a forged tool when the bare model passes the same gap without it** — CLEAN — value 4 — effort M — risk low — category: shelf hygiene
  Why: The forge grows every generation, and nothing in the pack removes entries. Models change, so what was a gap for the 4B may not be one for the 27B.
  Done when: after a model swap, a rerun of a tool's gap bare marks it dormant for that model, and the shelf's active count drops.

- **Give every forged tool a failure grammar a 4B can act on** — FEATURE — value 3 — effort S — risk low — category: small-model usability
  Why: The standing steer is that small models should reach frontier results by scaffolding. Free-form tool errors defeat that.
  Done when: every shelf tool ends with a typed footer (`ok`, `needs:<x>`, `bad-input:<field>`), and a 4B recovers from three seeded failures in a held-out scenario.

- **Pin and re-test the forge against runtime upgrades nightly** — FIX — value 3 — effort S — risk low — category: durability
  Why: The machine runs a rolling Arch kernel (7.2.10-hardened) and a hardened Python setup (`-I`), and forged scripts will drift. Assumption: the shelf has stored tests.
  Done when: a nightly lane runs every shelf test under `python3 -I` and files a task for each failure.

- **Wild: Hold a tool bazaar where local models bid by writing the passport and test first** — FEATURE — value 3 — effort L — risk med — category: wild
  Why: wild. Models write the spec and test before any code. The test is the bid, and the winner is whichever's test a cold reader accepts and whose code passes the rival's tests.
  Done when: for one real gap, three models each submit a test, the cross-run matrix is printed, and the winning tool lands on the shelf.

- **Wild: Let a failed forge attempt leave a scar card the next attempt must read** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: wild. Failed spikes already go to not-yet.md. Turning each into a short card that the next builder (including the 4B) is handed would make the second attempt cheaper.
  Done when: a repeated attempt at the same gap receives the earlier scar card, and its pass rate beats the first attempt in a paired run.

- **Wild: Let the forge forge itself, with a tool that writes tools, tested by forging a known tool** — FEATURE — value 3 — effort L — risk high — category: wild
  Why: wild. The task is a pipeline (need, search, build, test, quarantine, promote), and its steps could be a tool a small model runs.
  Done when: the forge-tool, given a gap record for a tool already on the shelf with the shelf entry hidden, rebuilds one that passes the original's tests.

- **Show the shelf as a web UI page with each tool's calls, saves and age** — FEATURE — value 2 — effort M — risk low — category: visibility
  Why: The forge is invisible until it is shown, and the user watches progress through the web UI and the site's Models section.
  Done when: the page lists each tool with call count, last call, retire-when status and the gap that created it, and renders an empty state with no tools.

Next question: Which gaps in the closed-task history were solved by an inline one-off script that was never promoted, and how many would a shelf have saved?
Next question: What does a forged tool cost to keep (tokens in descriptions, tests to run, drift) compared with its measured savings, and who decides the break-even?
