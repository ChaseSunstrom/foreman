# Brainstorm — lens: the toolsmith (invented): it builds, tests and keeps its own scripts, project skills and MCP servers, each with a failing-first test and a first real use

- **Bind each built tool to a miss-replay fixture** — FEATURE — value 5 — effort M — risk low — category: tool tests
  Why: T-2270 fires on a miss and T-2278 scaffolds a tool with a failing-first test, but nothing ties the test to the *original* miss. A tool can pass its own test and still not fill the gap. Assumption: the miss event records the failing command and its stderr.
  Done when: `fm new tool NAME --from-miss ID` seeds the test with that miss's command and output, and `fm tool check NAME` fails if the test doesn't reproduce the miss on the pre-tool tree.

- **Record a toolbelt ledger with one event per use** — FEATURE — value 5 — effort M — risk low — category: toolbelt
  Why: The loop is find/build/test/use, but "use" has no record, so "held up" and "retire unused" can't be computed. Assumption: no use ledger exists yet (none in the pack).
  Done when: running a shelf tool appends `{tool, task, exit, ms}` to the event log and `fm toolbelt` lists uses and last-used per tool.

- **Refuse a build without a search receipt** — FIX — value 4 — effort S — risk low — category: find-before-build
  Why: The request says "finds an existing plugin... or builds one", in that order; `fm new tool` is enforceable only if a receipt exists. Assumption: `fm plugins find` and `fm lib search` can write a query+result hash.
  Done when: `fm new tool X` exits non-zero with the exact search commands to run when no receipt from the current session names X's capability, and passes after them.

- **Make the install-grant queue writable only by a user-run verb** — SECURITY — value 5 — effort M — risk med — category: grants
  Why: "Install grants are queued for me, never self-granted" and T-2252 already made `fm mandate set` user-only; the queue file itself is a gap if an agent can edit it. Assumption: the queue is a plain file under the state dir.
  Done when: a test where the agent's Bash edits the grants file is blocked by the guard, and only `fm grant yes ID` (in USER_ONLY_FM) flips a row.

- **Pin each grant to an artifact hash and scope** — SECURITY — value 4 — effort M — risk low — category: grants
  Why: A grant for "plugin X" can be satisfied by a later, different X (supply-chain defenses sit deferred in T-0791). Assumption: found tools come from git or registry sources with a resolvable digest.
  Done when: installing a version whose hash differs from the granted one is refused with both hashes printed.

- **Run a candidate in a no-network sandbox before it reaches the card** — SECURITY — value 4 — effort L — risk med — category: sandbox
  Why: The user must approve installs blind otherwise; the grant card is far more useful with a trial result. Assumption: bubblewrap or unshare is available on the target hosts (hardened Linux kernel seen in the environment).
  Done when: the grant card shows "ran `--selftest` offline: pass/fail, files touched, network attempts" for each candidate.

- **Give every built tool a `--selftest` and a `--describe`** — DEVELOPER EXPERIENCE — value 4 — effort S — risk low — category: tool contract
  Why: T-2278's scaffold produces a script plus a test, but later sessions can't tell what a shelf tool does or whether it still works without opening it. Assumption: the scaffold template is editable.
  Done when: every `fm new tool` output answers both flags, and `fm doctor` runs all selftests and names the failures.

- **Mutation-check the failing-first test** — FEATURE — value 4 — effort M — risk low — category: tool tests
  Why: "Failing-first" proves the test fails with no code, not that it fails on a *wrong* implementation; the standing rule distrusts signals Foreman wrote itself. Assumption: a simple mutator (flip a comparison, empty the output, swap an exit code) suffices.
  Done when: a built tool is not marked proven unless at least 3 of 4 mutants of its script are caught by its test.

- **Promote a tool reused in a second repo to a library card** — FEATURE — value 3 — effort M — risk med — category: shared tools
  Why: `fm lib` exists, but nothing moves a project-built tool into it, so the same miss is rebuilt per repo. Assumption: `fm lib` cards can hold a script plus its test.
  Done when: a tool that records uses in two repos produces a proposed `fm lib` card in the user's queue, one word to accept.

- **Lift a stable script to an MCP server in one command** — FEATURE — value 3 — effort M — risk med — category: tool forms
  Why: `fm mcp new` and `plugin/templates/mcp-server/test_server.py` exist, but the path from a working script to a server is manual. Assumption: scripts follow the `--describe` contract above.
  Done when: `fm tool lift NAME --mcp` writes a server whose tool list matches `--describe`, with its test passing.

- **Wild: Forge a tool from a recorded manual session** — FEATURE — value 4 — effort L — risk med — category: synthesis — wild
  Why: assumption: the event log holds the shell sequence a session ran by hand when it hit the miss. Done when: `fm tool forge --from-session ID` emits a script plus a failing-first test, and replaying the recorded commands through it yields the same output.

- **Wild: Build two independent versions and differential-test them** — FEATURE — value 3 — effort L — risk med — category: tool tests — wild
  Why: the standing rule wants checks the writer didn't author; a second model's version is one. Assumption: the user accepts the doubled build cost for tools above a stated risk. Done when: disagreement between the two versions on a fuzzed input set blocks the tool and prints the differing input.

- **Wild: Fire-drill the shelf with a deliberately broken tool** — FIX — value 3 — effort M — risk low — category: resilience — wild
  Why: assumption: nothing shows that a rotted shelf tool is caught. Done when: a planted broken tool is flagged by `fm doctor` within one run and a repair task is filed with the failing input.

- **Wild: Let the toolbelt grade itself on the site** — FEATURE — value 2 — effort S — risk low — category: transparency — wild
  Why: the site already publishes genesis stats daily (T-2326); a toolbelt card with found/built counts, held-up rate and retirements would show the loop is real. Assumption: the ledger above exists. Done when: the published genesis data includes toolbelt counts and the page renders them.

Next question: Which built tools have ever been used by a session other than the one that built them, and did they work the second time?
Next question: When a search finds nothing, how long should that "nothing" be trusted before the next session searches again?
