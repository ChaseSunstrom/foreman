# Brainstorm — lens: capability map

- **Parse commands with a real shell tokenizer in the brief guard** — FIX — value 4 — effort M — risk med — category: guard
  Why: the pack reports 2 brief-guard false positives that read a dict key and a `.join(` call as written paths, which regex path-sniffing produces. A tokenizer (shlex or a bash AST) removes the class instead of patching two cases.
  Done when: a test corpus holding both known false positives plus 20 child-written look-alikes yields zero blocks, and every existing true-positive block still fires.

- **Gate hook import time with a per-module budget** — PERFORMANCE — value 4 — effort S — risk low — category: hooks
  Why: hook p95 is 278 ms over 13.5k runs, and Python hooks pay mostly for imports. assumption: much of that is eager imports, which `python -X importtime` would show.
  Done when: `fm doctor` prints the top 3 import costs per hook event, and CI fails if any hook's import time exceeds its stated budget.

- **Scan every task's diff for secrets before finish and ship** — SECURITY — value 4 — effort M — risk low — category: ship
  Why: assumption: `fm task finish` and `fm ship` audit evidence but not for credentials, while the guard stops commands only. gitleaks and trufflehog show the pattern, and a stdlib entropy-and-regex pass suffices. Only the hit location is reported, never the value.
  Done when: a planted fake AWS key in a task diff makes `fm task finish` refuse, naming the file and line without echoing the key.

- **Pin MCP tool descriptions and flag changes at session start** — SECURITY — value 4 — effort M — risk med — category: MCP
  Why: the MCP cell of the grid is empty for safety. Tool-description "rug pulls" (a server changing its descriptions after approval) are the known MCP attack, and a hash of name, schema and description per server catches them.
  Done when: editing one description in a test MCP server makes the next session start print a warning naming the server and tool, and the diff is shown.

- **Reject foreign Host and Origin headers on the web UI and require a token off loopback** — SECURITY — value 4 — effort S — risk low — category: web UI, headless
  Why: web UI is the one surface found, and headless/server use is a cell. DNS rebinding against a local dev server is a standard attack. assumption: the current server doesn't check Host.
  Done when: a request with `Host: evil.example` gets 403, and a non-loopback bind without a token refuses to start.

- **Measure a silence ratio: the share of turns where Foreman injects zero bytes** — PERFORMANCE — value 3 — effort S — risk low — category: context
  Why: context averages 387k per reply and the SessionStart note is about 2k chars across 89 sessions. A ratio gives lean a positive target rather than only a ceiling.
  Done when: `fm cost` prints the silence ratio per hook event, and a unit test shows an unchanged-state turn emits 0 bytes.

- **Collect old state, research packs and run logs under a retention policy** — CLEAN — value 3 — effort M — risk med — category: operate
  Why: the repo has 2098 files and state accumulates under `~/.claude/foreman/state` (research packs, mission notes). assumption: nothing prunes them today. Pruning a log or pack that evidence points at must be refused.
  Done when: `fm gc --dry-run` lists what would be removed with sizes, a real run frees it, and no file referenced by an open task is touched.

- **Cap each lane's memory, CPU and wall time with a cgroup or `ulimit` wrapper** — SECURITY — value 3 — effort M — risk med — category: lanes, headless
  Why: parallel builder lanes and `fm night` run unattended, and nothing in the pack bounds a runaway child. This is the "operate" cell for headless.
  Done when: a lane running a memory hog is killed at its cap, with the reason recorded in the lane's stop-cause, and the other lanes continue.

- **Run brainstorm and cold-read children with an allowlisted environment** — SECURITY — value 3 — effort S — risk low — category: children
  Why: children are tool-less by design, but they inherit the parent environment. Tokens in env vars shouldn't reach a model call that needs none.
  Done when: a test sets `FAKE_TOKEN` in the parent and a child's captured environment doesn't contain it.

- **Add a weight and accessibility budget for `site/genesis`** — PERFORMANCE — value 2 — effort S — risk low — category: site
  Why: the standing rule publishes site data to main on every tower change, so the page only grows, and the site cell has no lean check.
  Done when: CI fails if the genesis page exceeds a stated byte budget or ships a script from a third-party origin.

- **Compact stored lessons by merging duplicates and capping injected bytes** — CLEAN — value 3 — effort M — risk med — category: learn
  Why: T-0217 (lesson confidence) is deferred, and lessons feed injected context. assumption: duplicates accumulate. Compaction needs a cap in the injected block, never a deletion without a trail.
  Done when: running compaction on a fixture of 40 lessons with 10 near-duplicates leaves 30, and the injected lesson block stays under its cap.

- **Wild: Plant honeytoken credentials and alert if any agent reads them** — SECURITY — value 3 — effort M — risk med — category: other agents
  Why: wild. Claude Code, Codex, Gemini CLI and opencode each have different permission models, but all run as the user. A fake `~/.aws/credentials`-style file that the guard watches is agent-neutral, and a read means the agent went where it shouldn't.
  Done when: a scripted agent that cats the decoy produces an alert naming the harness and path, and a normal session produces none.

- **Wild: Offer a guard playground on the site where a visitor pastes a command and sees the verdict** — FEATURE — value 3 — effort L — risk med — category: site, guard
  Why: wild. It lets a skeptic try to break the guard without installing, and it feeds each attempt back as a candidate evasion test (opt-in, scrubbed). It requires the guard's rules to run in the browser, which also forces them to be data rather than code.
  Done when: pasting `rm -rf ~` into the page returns the same verdict and reason as `fm` on the CLI, checked by a shared test corpus.

- **Wild: Run a nightly prompt-injection corpus against Foreman's own fenced inputs** — SECURITY — value 3 — effort L — risk med — category: injection
  Why: wild. T-0791 (injection defenses) is deferred. Foreman fences data from tools, issues and docs, and a garak-style corpus planted in a fixture issue, CI log and README would show whether any reaches a plan or a command.
  Done when: the nightly run reports the number of corpus payloads that changed a plan or a command, and zero is the gate.

Next question: Which of the 61 empty cells are bounded by the user's hardware (a cgroup, a kernel feature, a missing package like libappindicator) rather than by Foreman's code, and can the grid mark them as environment-blocked instead of empty?
Next question: For each safety check proposed here, who sees a failure first (the user, a lane, CI), and is that the right person?
