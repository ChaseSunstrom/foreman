# Brainstorm — lens: capability map

Capability map against Claude Code, Aider, Codex CLI, opencode, Cline, Goose, Crush, claude-squad and Vibe Kanban. The list below skips what the pack already has (runner registry, home screen, watchdogs, worktree lanes, MCP/ACP serving, replay) and covers what a complete version still lacks.

- **Continue a closed run with a follow-up** — FEATURE — value 5 — effort M — risk low — category: conversation
  Why: assumption: `fm code` takes one request and closes; the Claude/Aider habit is "now also do X", which needs the last run's plan, diff and proof as context.
  Done when: `fm code --continue "also add a test for the empty case"` opens a new task whose prompt cites the previous task's id, files and checks, and a test asserts those are in the planner's input.

- **Mention files and images in the request** — FEATURE — value 4 — effort M — risk low — category: input
  Why: assumption: the request box takes only text; every rival takes `@path` and pasted screenshots. A UI bug report is usually a picture.
  Done when: `fm code "match @docs/mock.png in @site/index.html"` passes the file contents and the image to a vision-capable runner, and refuses with a named reason on a runner that can't take images.

- **Write one rules file per CLI from a single source** — FEATURE — value 4 — effort M — risk low — category: config
  Why: the user wants "better config/setup" across ANY CLI. Each CLI reads its own file (CLAUDE.md, AGENTS.md, GEMINI.md, `.cursorrules`), so rules drift between runners.
  Done when: `fm code rules sync` renders one `.foreman/rules.md` into each installed CLI's file with a marker block, leaves hand-written text outside the block untouched, and a second run changes nothing.

- **Pause on a runner's usage limit and resume at reset** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: assumption: Claude and Codex enforce rate and usage windows and a long queue hits them overnight. The harness should read the reset time, wait and continue, or fall to the next runner.
  Done when: a fake CLI that prints a "limit resets at T" message makes the run show "waiting until T", resume after T on an injected clock, and record both in the run's events.

- **Open a PR from a proved run** — FEATURE — value 4 — effort M — risk med — category: git workflow
  Why: runs end in a local commit, while Aider, Codex cloud and Vibe Kanban end in a branch and PR. Foreman has the proof to fill the body.
  Done when: `fm code --pr` pushes a branch and calls `gh pr create` with a body listing the criteria and the commands that passed, and does nothing without a `publish` grant on the task.

- **Turn an issue into a run** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: assumption: the nixie-style "it isn't doing anything" complaints begin as issues or messages elsewhere. A GitHub issue link should become a task with its text captured verbatim.
  Done when: `fm code --issue <url>` fetches the issue through `gh`, queues a task whose request is the issue text, and links the closing commit back to the issue.

- **Pack a repo map for small local models** — PERFORMANCE — value 4 — effort M — risk low — category: local models
  Why: local Ollama/llama.cpp models are in the registry but have small windows. Aider's repo map is why weak models work there, and `fm map` already exists.
  Done when: with a 4k-token budget, a planner call includes a ranked map of symbols touching the request, and a bench case on a fake small model passes with the map and fails without it.

- **Record recipes for repeatable requests** — FEATURE — value 3 — effort S — risk low — category: workflow
  Why: assumption: people repeat requests like "bump deps and run the gates". Today each repeat is retyped and re-planned.
  Done when: `fm code recipe save bump "update deps in {dir}"` and `fm code recipe run bump dir=plugin` work, and recipes show on the home screen.

- **Pin and watch the CLI versions of every adapter** — SECURITY — value 3 — effort S — risk low — category: adapter drift
  Why: the Gemini AfterAgent and Codex grant issues (T-0335..T-0337) show adapters break on CLI behavior. A new flag or output format fails silently.
  Done when: each run records the worker CLI's `--version`, and a version never seen passing the adapter's probe prints "unverified version" before the first turn.

- **Wild: Fix the command I just ran** — FEATURE — value 4 — effort M — risk med — category: shell integration
  Why: wild; assumption: a shell hook can keep the last failing command and its output, since `fm` isn't even on the user's PATH in some shells.
  Done when: after a failing `pytest`, typing `fm fix` opens a run with the command and the tail of its output as the request, with no copy-paste.

- **Wild: Review my own hand edits as I make them** — FEATURE — value 4 — effort L — risk med — category: ambient
  Why: wild; assumption: the harness's guard and checks only see the worker's changes. Watching the working tree while the user types would run the checks and guard on human edits too and say "this breaks test X".
  Done when: with `fm code watch` running, saving a file that breaks a named check shows the failing check within 10 s and nothing is changed in the tree.

- **Wild: Do it like that commit** — FEATURE — value 3 — effort M — risk med — category: codemod
  Why: wild; assumption: many requests are "do what abc123 did, in the other places". A past diff is a better spec than prose.
  Done when: `fm code --like abc123 --in plugin/lib` plans one step per matching file, and the checks proved on the original commit's change run on each.

- **Wild: Dictate a request** — FEATURE — value 2 — effort M — risk low — category: voice
  Why: wild; assumption: the user types short, frustrated notes ("it just isn't doing anything"). A local whisper.cpp binary, if present, turns a held key into the request text with nothing sent out.
  Done when: with a fake `whisper` command on PATH, holding the TUI's talk key puts its stdout in the request box, and with none installed the key says how to install one.

- **Undo a whole run in one command** — FEATURE — value 3 — effort S — risk low — category: safety
  Why: assumption: step snapshots are planned, but nobody says how to take back a closed run whose commit they now dislike.
  Done when: `fm code undo` reverts exactly the commits the last run made, refuses if the tree has later changes, and a test checks the files return to their pre-run state.
