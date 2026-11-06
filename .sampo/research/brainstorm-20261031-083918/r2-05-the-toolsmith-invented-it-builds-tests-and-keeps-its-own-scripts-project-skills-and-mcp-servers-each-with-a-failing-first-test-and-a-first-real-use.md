# Brainstorm — lens: the toolsmith (invented): it builds, tests and keeps its own scripts, project skills and MCP servers, each with a failing-first test and a first real use

- **Mutation-check every built tool's test** — FEATURE — value 4 — effort M — risk low — category: tool quality
  Why: T-2278 scaffolds a failing-first test, but a test that fails once against an empty stub can still pass against a broken tool. Assumption: scaffolded tests are often too weak to notice a changed line.
  Done when: `fm tool check NAME` applies 5 small mutations (flip a comparison, drop a branch, swap an exit code) and fails if more than one survives, naming the surviving mutant.

- **Turn the first real use into a golden fixture** — FEATURE — value 4 — effort S — risk low — category: regression
  Why: the lens requires a first real use, and that run is currently thrown away. Assumption: the miss that caused the tool is the best test case available.
  Done when: the first successful call of a built tool saves its redacted input and output under the tool's tests, and `fm tool check` replays it.

- **Search the user's own machine before the ecosystem** — FEATURE — value 4 — effort M — risk low — category: discovery, privacy
  Why: `fm plugins find` and `fm lib search` only look outward. The user's `~/bin`, dotfile functions, Makefile targets and shell aliases probably already do some of the missing things. Assumption: this is local-only, with no network and no history upload.
  Done when: a capability miss lists matching local scripts, with path and first help line, before any remote candidate, and nothing leaves the machine.

- **Make every built tool self-describing with `--describe`** — FEATURE — value 4 — effort S — risk low — category: tool contract
  Why: an agent calling a tool it built last week must read the source, which costs context. Assumption: a JSON contract (inputs, outputs, exit codes, side effects) cuts that cost.
  Done when: `fm new tool` generates a `--describe` that prints a schema, and `fm check` fails if it is missing or disagrees with the argparse flags.

- **Lift a stable script into an MCP server with one command** — FEATURE — value 4 — effort M — risk med — category: MCP
  Why: `fm mcp new` and the script scaffold are separate paths, so a script that proves useful has to be rewritten to be shared as an MCP server. Assumption: `--describe` supplies the schema.
  Done when: `fm tool lift NAME` emits an MCP server whose tool list matches `--describe` and passes the generated server test.

- **Record and replay MCP sessions as protocol tests** — FEATURE — value 3 — effort M — risk low — category: MCP, testing
  Why: `plugin/templates/mcp-server/test_server.py` exists, but an MCP server test normally needs a live client. Assumption: a recorded JSON-RPC transcript is enough to catch most regressions without a model in the loop.
  Done when: a built MCP server has a checked-in transcript, and `fm tool check` replays it and fails on any response diff.

- **Verify a tool's declared effects with a static scan** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: nothing checks a built script against what it says it does. Assumption: an AST scan for network, subprocess and out-of-scratch writes is cheap for stdlib scripts.
  Done when: a tool declaring `effects: read-only` that calls `open(..., "w")` or `socket` fails `fm check`, and a cold model second read is only needed for the tools the scan can't decide.

- **Require `--dry-run` on every tool that mutates** — SECURITY — value 3 — effort S — risk low — category: safety
  Why: assumption: self-built tools are the likeliest to do something irreversible on their first real use, while the user isn't watching.
  Done when: the scaffold test for a tool with effects asserts that `--dry-run` leaves the file tree hash unchanged, and the first real use runs the dry run before the live one.

- **Make each fix to a tool add a test case** — CLEAN — value 3 — effort S — risk low — category: test growth
  Why: assumption: tools get patched under pressure and the test file stays the same size as at birth.
  Done when: a commit that changes a tool's source without a new or changed test case is refused by `fm task finish`, with the exemption written on the task.

- **Preflight each tool's declared binaries at session start** — FIX — value 3 — effort S — risk low — category: portability
  Why: a built tool that shells out to `jq` or `rg` rots silently on another machine, and that machine is where the capability-miss trigger fires next. Assumption: the tools already know what they need, but nothing records it.
  Done when: a tool's manifest lists its binaries, and a missing one is reported by `fm doctor` and routed into the find-or-build path as a miss.

- **Wild: Build a tool from one example pair** — FEATURE — value 4 — effort L — risk med — category: programming by example
  Why: wild; assumption: users can show an input and the output they wish for more easily than they can describe it. The pair is the failing-first test.
  Done when: `fm new tool NAME --example in.txt out.txt` produces a tool whose test fails without the tool and passes with it, on that pair and on one held-out pair the user supplies.

- **Wild: Emit one tool source as a script, an MCP server and a skill** — FEATURE — value 3 — effort L — risk med — category: surface choice
  Why: wild; assumption: whether a capability is a script, a server or a skill is a deployment choice, not a design choice, and it is revisited as use grows.
  Done when: a single tool source file builds all three forms, and one shared test passes against each.

- **Wild: Turn a pasted pipeline into a tool** — FEATURE — value 3 — effort M — risk med — category: capture
  Why: wild; assumption: the one-liners a user pastes into the terminal are explicit capability misses that nobody files.
  Done when: a shell pipeline pasted twice in one session or across two sessions is offered as a named tool, with its failing-first test drafted from the pipeline's recorded output.

- **Wild: Fuzz the toolbelt overnight** — SECURITY — value 3 — effort M — risk low — category: unattended checks
  Why: wild; assumption: built tools get little hostile input, and a cold child with no view of the source is the right adversary.
  Done when: a nightly lane feeds each tool empty, huge, binary and non-UTF-8 inputs, and every crash or hang becomes a FIX task carrying the reproducing input.

Next question: Which built tools have actually been called a second time, and did that call hit the same code path as the first real use?
Next question: When a built tool and an ecosystem tool both answer the same miss, who sees the comparison, and does anything ever rule between them on evidence rather than on which was found first?
