# Brainstorm — lens: sci-fi: the 2030 harness that notices any capability it lacks, finds or builds the tool, proves it and uses it in the same task, worked back to what Python and Foreman can do today

- **Predict the miss at plan time** — FEATURE — value 4 — effort M — risk low — category: plan gate
  Why: T-1208 already notes a verify command whose test module doesn't exist. The same scan can cover binaries and imports named in Approach text and criteria (`shutil.which`, `importlib.util.find_spec`), so find-or-build starts before the first failure. Assumption: most misses are visible in the plan text.
  Done when: a task whose criterion runs `pdftotext` on a machine without it gets a plan-gate note naming `fm plugins find` before focus, and a test shows the note absent when the binary exists.

- **Answer "can fm do X?" with a path and a price** — FEATURE — value 4 — effort M — risk low — category: capability oracle
  Why: assumption: the user wonders about capabilities in plain words. Today they'd have to know `fm plugins find`, `fm lib search` and `fm mcp new` exist. `fm can "<sentence>"` returns one of have, findable, buildable or needs grant, with the next command.
  Done when: `fm can "read xlsx files"` prints a status word, a one-line source and the command to run, and a test covers each of the four statuses.

- **Census the machine once, then answer misses from the cache** — PERFORMANCE — value 3 — effort S — risk low — category: environment
  Why: assumption: find-or-build wastes a search on tools already on PATH under another name. A cached per-machine table of binaries, Python modules and MCP servers, invalidated by a PATH and mtime fingerprint, lets the capability-miss note say "you have X" first.
  Done when: a miss for `convert` on a box with `magick` names `magick` with no network call, and the cache rebuilds after a PATH change.

- **Spend an install grant on one invocation** — SECURITY — value 4 — effort M — risk med — category: grants
  Why: the push grant is "set on the one task and spent on use" (steer 2026-10-30). Install grants can follow the same shape: run `uvx`/`npx`/`pip --target .fm/tools` once, with no global install, and keep the grant ephemeral until the user promotes the tool.
  Done when: an approved grant runs the tool once, a second run asks again, and the guard test shows the grant can't be spent by a different command line.

- **Lint a built tool's effects statically before it runs** — SECURITY — value 4 — effort S — risk low — category: tool safety
  Why: built tools are stdlib scripts (T-2278), so `ast` can list imports and calls (`socket`, `subprocess`, `os.remove`, `open(..., "w")`) with no sandbox. The list is recorded on the shelf entry and compared with what the miss needed.
  Done when: a scaffolded tool that opens a socket fails `fm check` with the line number, and a pure-parser tool passes.

- **Make the user drop one real sample for every built parser** — FIX — value 4 — effort S — risk low — category: proof
  Why: the earlier question about a model on both sides applies here. The same model writes the tool and its test, and shares blind spots. A user-owned `.fm/samples/` file the model can't author breaks that loop.
  Done when: `fm new tool` for a file-format miss refuses to count the tool as proven until it passes on a file under `.fm/samples/` that git blame shows the model didn't add.

- **Let a strong model build the tool once and a cheap model use it forever** — PERFORMANCE — value 3 — effort M — risk med — category: model routing
  Why: assumption: `fm code` runs on weaker models that fail at tool-writing. T-2291's history-based router already picks models per lane. A build-once lane routed to the strongest model, with a frozen, tested result handed to the cheaper session, cuts the cost.
  Done when: a miss in a Haiku session spawns one build lane on a stronger model, and the Haiku session calls the finished tool within the same task.

- **Turn an OpenAPI or CLI `--help` into a scaffolded MCP server** — FEATURE — value 3 — effort M — risk med — category: build
  Why: `fm mcp new` exists, but nothing seeds it from a spec the project already contains. A miss like "call the billing API" has a spec file in the repo. Assumption: such specs are common.
  Done when: `fm mcp new billing --from openapi.json` yields a server whose generated tests fail first, then pass against a recorded fixture.

- **Scrub search queries before they leave the machine** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: queries to `fm plugins find` and `fm lib search` are likely built from error text, which holds paths, hostnames and tokens. Assumption: the queries are built that way. Reduce each to the tool noun and verb, and show the query that was sent.
  Done when: a miss whose error contains `~/secret-proj` and a token produces a logged query with neither string.

- **Search during the pause** — FEATURE — value 3 — effort S — risk low — category: idle time
  Why: steer 2026-10-31 #3 says to wait out usage limits. Free finds (no model tokens) over open misses can run in that wait, so the grant card is ready on return. Wild: it also means the harness wakes up with an answer.
  Done when: a task paused on a usage limit has a ready find result attached to its miss on resume, with zero model calls logged during the pause.

- **Port a found skill to every host** — FEATURE — value 3 — effort L — risk med — category: portability
  Why: standing rule: Foreman isn't specific to Claude Code. MCP servers port well. Skills and plugins don't, so a find for Codex or Gemini CLI should translate the instructions, or offer the MCP wrapper. Wild.
  Done when: a skill found for Claude Code is rendered for opencode with a diff of what could not be carried, and a test covers the rendering.

- **Wild: Borrow a capability from another of the user's machines** — FEATURE — value 3 — effort L — risk high — category: delegation
  Why: assumption: some misses are physical (no GPU, no display, no Windows). The miss could resolve to a remote runner or cloud routine (T-0793) that runs the tool and returns the result. Wild.
  Done when: a miss "needs a GPU" is routed to a named remote runner, runs one command there, and its output is recorded as run evidence.

- **Wild: Keep a "capability weather" line on every surface** — FEATURE — value 2 — effort S — risk low — category: status
  Why: a one-line ambient status such as "3 tools on the shelf, 1 grant waiting, 0 misses open" in the pane, status line and site makes the 2030 feel visible. Wild.
  Done when: the foreman-ui pane shows the line, and it changes within one refresh after a grant is approved.

- **Wild: Let a failing shelf tool file its own repair task with the failing input** — FIX — value 3 — effort M — risk med — category: self-repair
  Why: when a shelf tool exits nonzero, the harness stores the input (scrubbed), the stderr and the tool hash as one FIX task, so the tool heals in a later session. Wild.
  Done when: a shelf tool run that fails creates one deduped FIX task with a replayable failing case, and the second identical failure adds no task.

Next question: Which misses did users resolve by hand with something the harness never searched for, and what would a first-run census have shown?
Next question: Where does a built tool's test leave the writer's blind spots, and who other than the writer holds a sample?
