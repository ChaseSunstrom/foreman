# Brainstorm — lens: inversion: how getting missing tools fails: it works around the gap by hand every time, installs without a grant, builds a tool nobody tests, never finds the plugin that already exists, keeps dead tools forever

- **Trip a wire on the tool-config files** — SECURITY — value 5 — effort M — risk low — category: grants
  Why: the pack covers an unforgeable queue and package-manager shims. It never covers an agent editing `.mcp.json`, plugin settings or `settings.json` directly, which bypasses the queue entirely. assumption: the guard doesn't yet watch these paths.
  Done when: a test session that appends an MCP server to `.mcp.json` outside `fm grant` is flagged at the next hook with the file diff, and a queued grant row is required before the entry loads.

- **Fence search results as data, not prose** — SECURITY — value 5 — effort M — risk low — category: injection
  Why: `fm plugins find` and `fm lib search` feed third-party READMEs and descriptions to the model. A listing saying "run this, grant yourself" is the obvious attack. T-0791 is deferred and none of its ideas is wired to this loop. assumption: results currently reach the model as free text.
  Done when: the finder returns only structured fields (name, source, hash, version, license, one capped line of description). A fixture listing containing an injected instruction never reaches the transcript verbatim.

- **Refuse a done-when command that calls a scratch script** — FIX — value 4 — effort S — risk low — category: proof
  Why: built tools start in `.fm-scratch/` (T-2259), and lane rm treats that folder as throwaway. A criterion that passes by running a scratch script and then can't be re-run after cleanup is a false done. assumption: nothing checks this today.
  Done when: `fm task new`, or finish, rejects a verify command referencing `.fm-scratch/` or an untracked file. Promoting the script to the shelf or the repo clears it.

- **Put dependencies, licence and upkeep on the grant card** — FEATURE — value 4 — effort M — risk low — category: grants
  Why: a grant approves a top-level name, but the install pulls a transitive closure. A licence that blocks use, or an abandoned upstream, only shows up after the install. assumption: the card currently shows name and scope only.
  Done when: for a fixture plugin with 3 transitive deps and a GPL licence, the card lists the closure, the licence and the last-commit age. A closure wider than the declared one is flagged.

- **Tag workaround-proven closes in the unproven rollup** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: the failure "works around the gap by hand every time" ends in a task that closes green because the agent hand-parsed the thing instead of getting a tool. The Mission 7 Unproven rollup counts typed or inconclusive evidence, but not "a capability miss fired and no tool was acquired".
  Done when: a task with a recorded miss event and no find, build or grant before close appears in the rollup as "workaround", with the miss named.

- **Retry `not-yet.md` blockers when a matching tool appears** — FEATURE — value 4 — effort M — risk low — category: genesis
  Why: standing rule: "every Seed retries items a new capability may unblock". Acquisition is exactly such a capability, but nothing connects the shelf or the ecosystem index to the blocker lines.
  Done when: adding a shelf tool or finding a plugin whose declared capability matches a `not-yet.md` blocker reopens that row with the tool named, and the next Seed lists it.

- **Suppress the trigger when failure is the expected outcome** — FIX — value 3 — effort S — risk low — category: trigger
  Why: T-2270 fires on a missing command or module. `which foo || …`, `command -v`, or a probe inside a verify that expects absence would fire it. Noise there makes the once-per-session note get ignored. assumption: no exclusion exists.
  Done when: fixtures `command -v nope || true` and a try/except ImportError probe produce no miss event, while a bare `nope --version` still does.

- **Require a no-match case in every built tool's test** — FIX — value 4 — effort S — risk low — category: tool tests
  Why: a built parser that exits 0 with empty output on unexpected input is the quietest failure, and a red-first test of the happy path won't catch it. `fm new tool` generates the failing-first test, so the template can demand more.
  Done when: the scaffold includes a failing-first empty/garbage-input case that must exit nonzero or say "no match". `fm check` flags a shelf tool whose tests lack one.

- **Grant a bounded go-bag before an unattended run** — FEATURE — value 4 — effort M — risk med — category: grants
  Why: a queued grant blocks an overnight lane for hours. Steer: wait out limits and keep going on everything unblocked. A pre-departure bag lets the user approve likely tools once. assumption: the plan or goal text can predict candidates.
  Done when: before a long `fm run`, one card lists predicted tools with vetted hashes. Approved ones carry an expiry and a use cap, and unspent ones lapse at the end of the run.

- **Handle secret-needing tools without the model** — SECURITY — value 4 — effort M — risk med — category: grants
  Why: a found MCP server that needs an API key makes the agent ask the user to paste it into chat or write it to `.env`. The key then lands in the transcript or the repo. assumption: grants only cover install, not credentials.
  Done when: a fixture tool declaring `needs: API_KEY` produces a user-run verb that stores it outside the transcript and the repo, and a leak scan of the session log finds no value.

- **Wild: Seed a honeypot registry for the exam** — SECURITY — value 4 — effort M — risk low — category: exam
  Why: the pack proposes scoring miss-handling and sandbox trials, but the finder is only tested against honest listings. A local fake registry with a typosquat, an injected README and a stale fork measures whether the finder is fooled. wild.
  Done when: `fm exam` has a miss scenario where the right tool sits beside three planted decoys, and the scorecard reports picked-right and picked-decoy rates, with the decoy rate at 0.

- **Wild: Rebuild the toolbelt on a fresh machine from the lockfile** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: the pack's lockfile, hash pins and reversible journal imply the shelf is reproducible, but nobody tests it. A new laptop or CI box loses everything silently. wild.
  Done when: `fm shelf rebuild` on an empty home reinstalls every pinned tool, re-runs each `--selftest`, and prints one grant card for the pieces that need approval again.

- **Wild: Lend the shelf to the user's own shell** — FEATURE — value 3 — effort S — risk low — category: surfaces
  Why: the user pays for each built tool, yet only agents can reach it. Exposing the same tools at the prompt, with `--describe` as help text, makes the shelf worth keeping alive and shows the user its dead entries. wild.
  Done when: `fm shelf link` puts a shim directory on PATH. A shelf tool runs from the user's shell, and the run is logged as a use event.

- **Give the acquire loop three verbs** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the pack names `fm plugins find`, `fm lib search`, `fm mcp new`, `fm new tool`, `fm new skill` and a grant queue. That is a lot to remember at the moment a session is already stuck. assumption: the agent and the user both pick the wrong entry point sometimes.
  Done when: `fm need "<what>"` runs search, then build, then test, then queue, prints one status line per stage, and a fixture miss reaches "waiting on grant" with no other fm verb typed.

Next question: Which acquisition step has no record of the options the session rejected, so we can't tell a good "no" from a lazy one?
Next question: When a grant is approved and the tool fails on first real use, who learns that, and does the refusal-memory or the shelf ever get corrected?
