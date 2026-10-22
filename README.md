# Foreman

[![tests](https://github.com/ChaseSunstrom/foreman/actions/workflows/test.yml/badge.svg)](https://github.com/ChaseSunstrom/foreman/actions/workflows/test.yml)

**The discipline layer for Claude Code.** Foreman makes Claude plan before it edits, prove its work with commands it actually ran, stay on one task at a time, and keep going through the queue until it's done or needs you, while a guard hook stops the commands you'd never want run in bypass mode.

<p align="center">
  <img src="demo/live.svg" width="960" alt="Claude Code 2.1.301 with the foreman-ui mod, working a real Foreman fix in a copy of this repo: the chat reads as a tree, each call a compact branch under the prompt with its diff or result; a scout subagent finds the parser; Claude writes the test and the fix, fm task prove shows the test fails without the change, and the task closes; the live tree above the prompt shows the session and its subagent with their latest calls and time bars, and the Foreman pane beside it shows the work bar, the stage rail and steps, the Activity lanes, the Agents graph, History and the Today charts">
</p>
<p align="center"><sub>A real session, recorded in a copy of this repo: one typed request (<code>fm edit</code>'s block form couldn't delete text: a block whose <code>===</code> runs straight into <code>&gt;&gt;&gt;</code> was refused; send a scout subagent to find the parser first), the rest is Claude working through Foreman, about 2 minutes, sped up where the model thinks. Its change is in Foreman now (T-1213). <a href="demo/live.mp4">MP4</a>.</sub></p>

## Why

Claude Code is fast. Left to itself it also fails in familiar ways: it edits before it understands the problem, says "tests pass" without running them, chases every new idea halfway through a task, loses its place after `/compact`, and in bypass mode it will run the one command you'd never type. Foreman is the foreman on that job site.

| | |
|---|---|
| **Plans first** | Every request becomes a brief before any edit: its type and size, what "done" means, the command that proves it, and the steps. An edit with no active task is refused. |
| **Proves it** | Evidence is a command fm ran and recorded, not a sentence. A fix needs a test that failed first. A reply claiming the tests pass is checked against the turn's own runs. Nothing closes without its audits. |
| **Guards bypass mode** | A fail-closed guard stops recursive deletes outside the project, force-pushes, credential reads, `curl \| sh`, publishes and edits to Foreman itself. Before a git command throws away uncommitted work, Foreman saves that work first. |
| **Stays on task** | One active task. New requests go to the inbox instead of being chased. `NOW:` switches tasks on purpose. |
| **Never loses its place** | State lives on disk, so after `/compact` or in a new session Claude resumes at the exact step. |
| **Keeps going** | Drive mode works through the whole queue. In full auto, Claude decides and records its decisions instead of asking. When the queue drains it finds its own next work (`fm scout`: a newer Claude Code to adopt, dependencies with no stack card, doctor failures, a weekly brainstorm), so you never have to ask. `fm run` and `fm serve` keep it working headless. |
| **Learns** | Lessons, tripwires and a self-improvement loop turn your corrections and Foreman's own friction into fixes. |

## Quick start

```bash
curl -fsSL https://raw.githubusercontent.com/ChaseSunstrom/foreman/main/install.sh | bash
```

Or from inside Claude Code:

```
/plugin marketplace add ChaseSunstrom/foreman
/plugin install foreman@foreman
```

Then just ask Claude for something: `fix the login timeout on slow wifi`. To see it work before you trust it with your repo, run `fm demo`: the real `fm` and guard hook on a seeded bug, in a throwaway repo, with no model calls and nothing left behind (`--pace 1` plays it at this speed). Bare `fm` in a project says where things stand and what's next; `eval "$(fm complete --shell bash)"` in your `~/.bashrc` (or `--shell zsh`) gives tab completion for commands, options and live task ids.

<p align="center">
  <img src="demo/demo.svg" width="860" alt="fm demo: Foreman refuses an edit made before any task exists and an rm -rf ~, records a failing test, the fix and a passing test, refuses to close the task until the audit is given, then closes and commits it">
</p>

<details>
<summary><b>More ways to install, requirements and flags</b></summary>

The plugin-system install changes nothing outside the plugin: the hooks and the guard run, and the first session reads Foreman's rules from the plugin. Say "finish setting up Foreman" later to add the rest (status line, deny rules, the bypass question, `fm` in your shell). `fm uninstall-user` undoes it.

**Having Claude install it for you?** Tell it: "install Foreman following https://github.com/ChaseSunstrom/foreman/blob/main/INSTALL.md". [INSTALL.md](INSTALL.md) has it explain the defaults and ask before each change.

**Private repo** (uses your `gh` login):

```bash
gh repo clone ChaseSunstrom/foreman ~/.claude/foreman && ~/.claude/foreman/install.sh
```

**Requirements:** Linux, macOS or WSL (not native Windows), `git`, `claude` (tested on 2.1.304; the pane needs 2.1.299 or later), and Python 3.12.7 or newer as `python3`. When Python is older or missing, the installer gets it with Homebrew on macOS or with `uv` elsewhere (no sudo; `python3` goes in `~/.local/bin`).

**Flags:**

- `--security`: Trail of Bits security skills.
- `--docs`: Office and PDF skills.
- `--apply-conflicts`: disable plugins that compete with Foreman instead of only reporting them.
- `--no-plugins`: skip the curated plugin setup.
- `--bypass` / `--no-bypass`: make bypass mode your default, or keep your current permission mode, without being asked.
- `--no-mod`: skip the foreman-ui mod.
- `--no-wiring`: don't touch `~/.claude`.
- `--build`: open Claude Code on `/foreman:build` to rebuild from `BUILD_PROMPT.md`.
- `--desktop`: also install Foreman Desktop from its newest release (the AppImage and a menu entry on Linux x86_64, the app in `~/Applications` on macOS).

**What `install.sh` does:**

1. Clones this repo to `~/.claude/foreman`, or fast-forwards it if it's clean and on `main`.
2. Runs `setup-plugins.sh`. It installs the curated plugins that are missing, and installs language-server plugins only when the server is on your PATH. It reports conflicting or heavy plugins but never uninstalls anything.
3. Registers this repo as a local plugin marketplace and installs `foreman@foreman`. The plugin loads in place, so edits under `plugin/` apply on `/reload-plugins`.
4. Asks whether to make `bypassPermissions` your default permission mode. That is Foreman's recommended mode, because its guard is built for it. On a yes (or `--bypass`) it sets it, backing up `settings.json` and recording the original. With no terminal to ask on and no `--bypass`, your permission mode stays as it was.
5. Wires Foreman into `~/.claude` with `fm install-user` unless you pass `--no-wiring`. That adds:
   - a statusLine wrapper (your original line and claude-hud still render above the Foreman line);
   - deny rules for catastrophic commands;
   - a raised Stop-hook continuation cap for drive mode;
   - a marked block in `~/.claude/CLAUDE.md` and the `~/.claude/rules/foreman.md` symlink;
   - a `~/.local/bin/fm` link so `fm` works in any shell (unless a different `fm` is already there).

   Every change is recorded in `state/install-manifest.json`, so it can be undone exactly.

</details>

## Talking to it

Plain requests work. Tags and a few lines of context make them precise:

```
fix the login timeout on slow wifi                    # plain request: classified, planned, done with evidence
FIX: login times out after 30s on slow networks
FEATURE: export report as CSV @src/reports
CLEAN: collapse the three date helpers into one
CONTEXT: Django app; don't touch migrations
DONE-WHEN: all tests pass and the CSV opens in Excel
```

Work runs in the order CLEAN → PERFORMANCE → SECURITY → FIX → FEATURE, after a baseline check. Mid-task ideas are captured and queued: `NOW:` switches tasks, `PAUSE` checkpoints and `STATUS` shows where things stand. You never have to run a command yourself. Say it in plain words ("is foreman ok?", "clean up", "this repo is sensitive") and Claude runs it.

- **Open-ended requests** ("super improve it", "just get it done") get a brainstorm first. Several tool-less sub-agents each look through a different lens, then Claude checks every idea against the real code and queues the best. A brainstorm runs up to six short `claude -p` (Sonnet) sessions, which count against your plan's usage.
- **Audits before done:** finished work is checked through independent lenses: intent, adversary, edge cases, operations and maintainability. Each lens gets different prompts and context. Small tasks get a self-check; large ones get all five. A change that touches UI also gets a design read: an art director, an accessibility reviewer and a first-time user, with the task's screenshots.
- **Workflows:** `/foreman:review [range | branch | T-0123]` runs one reviewer per lens over a diff, then two skeptics try to refute every finding, so only confirmed defects come back, with the `fm task finding` lines to record them. `/foreman:ideas "<request>"` brainstorms with agents that read the code while they think, so each idea arrives marked new, partial or already built, with evidence and a ready intake block. Both are multi-agent runs and cost more than a single pass.
- **Docs stay current:** bigger tasks can't close until they record which docs they changed, and those docs must exist and match the code. Drift elsewhere is reported when a task closes (`fm docs` shows it any time). Long sessions compact earlier, since Foreman's state makes that cheap.
- **Full auto:** say `FULL AUTO` (or "don't ask me anything") and Claude works through the whole queue without questions, recording its decisions. Anything only you can approve waits for one summary at the end. `STANDARD AUTONOMY` switches back.

## What it does for you

**Plans.** Intake turns a request into briefs: type and tier (S, M or L), acceptance criteria with the commands that prove them, steps, scope and risks. M and L work lists the approaches first. The queue orders itself, dependencies included. Each brief lives in Foreman's state, outside your repo, unless you turn on `fm sync`.

**Knows your stack.**
- A library of over 1,000 stack cards spans 28 areas: languages, Python, Node, web, JVM, .NET, mobile, Rust, Go, C/C++ and embedded, data, ML and LLM apps, infra, cloud, ops, testing, security, architecture, product domains, tools, games and hardware, building Claude Code plugins, hooks, skills and mods, practice (brainstorming, premortems, experiments, self-improvement loops), and a style shelf of twelve named visual looks with measured palettes.
- Each card gives the exact commands that verify the work, a failing-test recipe, the mistakes models actually make, and a review checklist.
- Cards cost no context until they are read. `fm lib` picks the ones that match your repo's manifests and files, and the session start names them.
- `fm lib show fastapi pytest --section verify` reads just the parts you need.
- The first edit of a file a card covers brings that card's pitfalls (its Avoid section, under 700 characters) into Claude's context, once per card per task. A card is picked by what the file imports as well as by its type: a file that imports `@tauri-apps/api`, `fastapi`, `tokio` or `github.com/gin-gonic/gin` gets that framework's card beside its language's (at most two an edit; Python, JS/TS, Rust and Go imports, matched to the project's own dependencies). The audit brief carries the review checklists of the cards a task used, and `fm lib stats` shows which cards actually reach Claude. `fm lib inject off` turns it off; `fm doctor -v` counts how often it and the other enforced checks fired this week.
- `fm lib search` also finds installed plugins' skills, disabled ones included, so a big skill pack can stay off and still be found.
- `fm lib source add <git URL>` indexes a third-party skills repo read-only: a shallow, markdown-only checkout in Foreman's state, with no hooks, filters, submodules or symlinks, and nothing run. `fm lib source defaults` adds eleven vetted ones (wshobson/agents, trailofbits/skills, VoltAgent subagents, K-Dense scientific skills, morluto/rea, and anthropics' skills, claude-code, claude-cookbooks, claude-plugins-official, financial-services and prompt-eng-interactive-tutorial), searchable next to the cards at no context cost; `--dry` lists them without cloning. Each is pinned to the commit it was added at (`fm lib source update` moves the pin) and has a depth (reference: each README a searchable note; index: skills, agents and a marketplace.json's plugins) and a licence class read from its licence file: open (MIT, Apache, BSD, ISC, MPL), source-available (any other licence) or ideas-only (none); a skill folder with its own licence file takes that file's class, `fm lib source update` names a class that moved, and ideas-only entries `fm lib show` gives as name and description only, with no path to copy from.

**Verifies.**
- `fm check` runs the project's gates and reuses a pass on an identical tree. A new test file that is only another open task's red-first test is left out and named, so one task's deliberate red doesn't block another's close. A close runs the tests linked to what the task changed and refuses a new failure; every few closes the full gates run in the background, and a red run becomes one urgent baseline task by itself.
- `fm task evidence --run` records a command's real exit code and output.
- Test first at edit time: in a fix or feature task that has changed no test and recorded no failing run, the first edit of a source file brings one line saying to write and run the failing test first. Once per task, never a block.
- `fm task prove` shows a test failing on the start tree and passing now. `--hunks` reverts each hunk to show the tests notice it.
- `fm task finish` closes a task in one call, but only with fresh evidence and the audits, docs note and lesson its size needs. It counts its warnings in one line first (a leftover `breakpoint()` or conflict marker among them) and ends by saying where the work landed: committed and pushed, or not.
- The suite runs in CI on every push.

**Protects.**
- The guard reads every Bash command and file edit before it runs, including the commands fm stores and runs later.
- Work snapshots save uncommitted work before `git reset --hard`, `checkout -- .`, `clean -f` and the like. `fm snapshots` lists them, each with the command that brings it back; `fm oops` shows the newest and `fm oops --apply` restores it.
- `fm sensitive on` keeps a repo's content from leaving the machine; `fm sensitive suggest` lists what hints a repo needs it (`.env*`, `*.pem`, secret or prod in a path) and changes nothing.
- A daily risk budget: destructive guard blocks, failed closes and reverts spend points, and past the cap Claude's autonomy steps down a notch until tomorrow (`fm risk`; only you move the cap).
- Install commands are checked before they run: a package one edit from a popular name, or published in the last 30 days, gets a note (`fm deps check "<cmd>"`). A command copied from a web page or MCP result asks before it runs.
- `fm posture lite` (yours to type: `! fm posture lite`; Claude may not lower it) keeps only the guard and the evidence gate in a repo where the rest of Foreman is in the way (no injected notes, no drive); `fm posture full` brings it back.

**Shows you what happened.**
- `fm tour --since main` ranks a whole branch, or a night's run, by review risk and says which files are safe to skim.
- `fm why FILE:LINE` traces a line back to the task and the words you asked in.
- `fm at T-0042 -- pytest` runs any command as of a task's start.
- `fm show X` takes a task id, a FILE:LINE or plain words and shows the task, the line's history or related past work.
- `fm digest` sums up the week; `fm outcomes --readme` gives the track record in one sentence; `fm outcomes` grades every close by whether it survived 30 days (nothing reverted it, fixed it or corrected it), and `--claims`, `--regret`, `--graveyard` and `--seen` read those grades; `fm round close` tags a round and lists what it closed.

**Runs unattended.** Drive mode, full autonomy, `fm run` (one fresh `claude -p` session per task; `--max-usd` caps what it spends), `fm serve` (Remote Control on a server), `fm scout` (finds work nobody asked for), `fm night` (budgeted background jobs: it works the queue under the night's budget, composts finished lanes and proposes merged lessons) and `fm notify` for when it's done.
- `fm draft` has the top queued small task drafted on a throwaway branch while Claude waits; `fm lane race T` has two builders take different approaches and `fm lane pick` merges the better one.
- `fm ci-watch` follows the CI run of the commit you pushed and turns a failure into a fix task; `fm pr threads` turns review comments into steps and `fm pr train` merges approved, green PRs in order after a re-test.

**Stays light.** Only the guard (on tool calls that can change something) and the write validators (after a write) run synchronously; everything else that records runs async or once per turn, and nothing is injected unless it changes what Claude should do next. `fm doctor` reports each hook's p95 latency, and the pane's hooks tank shows it live (about 20 ms here).

**Changes many spots in one call.** `fm edit` takes a batch of exact replacements on stdin (JSON, or `@@ file` / `<<<` old / `===` new / `>>>` blocks) and applies them all or none: each old text must be there once (or be marked `all`), each file inside the task's scope, and each one the guard would let an Edit write. `fm sub PATTERN REPL --glob G` previews a regex change as per-file counts and writes it with `--apply`. The third edit of one file in a row says so, once. `fm lane max N` lets up to six builders work at once on an unattended run. When the session that launched a builder ends, `fm next` names the stopped builder and `fm lane resume ID` takes it back: its uncommitted files (secret-looking ones left out) become a WIP commit on its branch, the worktree is freed, and a new builder brief merges that branch first. It refuses a builder that may still run, or one recorded on another host, unless you give `--force "<why>"`.

**Learns a fix once.** When a command fails and a later one on the same program gets past it, Foreman keeps the pair with no one asking. The next time any session meets that failure, in this project or another on the machine, Claude gets the fix in the failure's context (`Foreman: known fix for this failure … Try that before anything else`), and a command that failed before is flagged before it runs again. A look around (`ls`, `cat`, `git status`) or a retry that happens to pass teaches nothing. A fix that keeps missing stops being offered, and a failure met three times with no fix becomes a task to remove its cause. Project fixes travel with the repo: `fm sync on` mirrors them into `.foreman/fixes.md`, so clones, other machines and teammates' sessions get them through git; a fix that only came with the repo is offered as a hint to check (never as an instruction, never before a command runs) until you adopt it with `fm fix trust N`. A sensitive project's fixes stay in that project. A code edit between the failure and the pass makes it a code fix, so nothing is kept. `fm fix list` shows them, `fm fix add "<error>" --do "<what works>"` teaches one the hooks can't see, `fm fix rm N` forgets one. A hook only ever says a fix; it never runs one. The UI harness answers Claude Code's folder-trust prompt itself, for folders Foreman made only.

**Improves itself.** `fm backtest --rule/--fix/--card` shows how often a change would have fired on your real recent sessions before it ships; `fm rule add … --moves corrections --by 30` makes a change a trial the digest grades later; `fm adopt` learns from a repo's history of reverts and fixes. `fm friction` digests Foreman's own friction (`--minutes`: an estimate of the minutes it cost this week), `fm burden --by-verb` lists the verbs nobody calls, `/foreman:improve` builds candidate changes in a worktree and keeps only the ones that score at least as well on the eval suite, and lessons come back as tripwires on related work.

## Seeing what's going on

**In Claude Code**, the `foreman-ui` mod draws Foreman live in the session: a card above the prompt shows the task, a mini stage rail and a step bar, and each tool call gets an animated row. `/fm` opens a dashboard that reads top-down by urgency, with live charts. Below the prompt is a true-color status line. **Foreman Desktop** shows every project, agent session and device in one window. **Other agents** (Codex, Gemini CLI, opencode) can run the same guard and context.

<details>
<summary><b>The foreman-ui mod in detail</b></summary>

The `foreman-ui` mod draws Foreman live inside the session.

**The card.** Above the prompt sits a card showing:
- the task's type chip, id and title, and its stage on a mini rail (●━●━◉─○─○);
- a true-color gradient step bar that animates while Claude works;
- audits, queue and inbox counts, and what waits on you;
- speedrun splits: each stage's time against your typical for that kind of task, green under and red over;
- when idle, one line on what Foreman learned this week (fixes that worked or missed, rules to propose);
- `[f]` dashboard and `[n]` next.

Set `palette: 'cb'` for a colourblind-safe ok/error pair (errors keep their ✗), and in the history press `b` to step back in time and `l` to return to live.

**The chat.** Every row reads like a section of the pane: a mark, a bold label in the row's colour, its subject, a rule fading out in that colour and the facts on the right, with a blank line above it and no box. Your prompts (`❯ You`), Claude's replies (`● Claude`), commands, edits, subagents and every other tool (skills, MCP calls, artifacts …) get one (a tool's result of up to three lines sits in its row; a longer one keeps Claude Code's own block under it, which expands; a failed call keeps Claude Code's row); a review's findings list each one with what came of it (fixed, skipped), where it is and the short claim. While a call runs, a comet runs along its rule beside the elapsed time. A command shows its lines, its output (failures first when it failed), the files it changed and a commit. An edit's diff keeps a line of context either side of each change, breaks between hunks with `┄`, and washes only the words that changed in a changed line, never the whole width. Successful `fm` bookkeeping commands fold to one quiet `⚙ fm …  ✓ …` line, while failures keep their full row; finished reads and background-task notifications also fold to one quiet line.

**Turns.** The working spinner names the Foreman step it's on. The line closing each turn says what the turn did (`4 tools · 2 edits +30 −4 · ✓ T-0012 step 3/5`). When Claude stops with Foreman work waiting, the prompt offers `/foreman:next` as ghost text (never while a question waits on you). The footer says when Foreman needs you and shows `full auto` and `drive off` as modes.

**Context.** The band carries a context meter. At 85% Foreman checkpoints the task once, so a `/compact` resumes at the exact step. When a task closes with context at 40% or more, the mod compacts right there. It keeps your standing requests and live decisions, drops finished work, and Foreman's resume note restores the exact point. The threshold is the mod's `freshAt` setting; 0 turns it off.

**Your project's own timings.** Sizes read as words (`FIX · small`, `· medium`, `· large`) and carry this project's history:
- The band shows how long you've been on the task and what that type and size usually takes (`12m on it · usually ~25m`). That is the median from first focus to done, once three such tasks have closed.
- The band shows the whole queue (done today, queued, in the inbox, what's next), so it never looks nearly finished while work waits.

**Prompts and background work.**
- Every Foreman permission prompt gets a plain-words note under it saying what a yes grants and why.
- When Claude waits on background shells (started in the background, or moved there with ctrl+b), the band says so (`◷ waiting on 2 background shells · cargo test · 3m 12s · Claude picks up when they finish`) and the pane lists them. Each leaves when its notification arrives or it is stopped.
- Coming back to a long unattended run, the band tells you what closed since your last message (`✔ since your last message: 3 done · …`) until you write again.

**The mascot.** The pane's top-right corner has Claude Code's own Claude from the welcome screen. Its `mascot` setting picks blue, orange, purple, green or off. It dances while Claude works, blinks while idle and cheers when a task closes, with a mini Claude in its own color beside it for each running subagent.

**The dashboard.** `/fm` (or `[f]`) opens one panel beside the chat that fills the dock exactly, no more and no less. Each section sits under a titled divider drawn in its own colour (with a blank row above it on a tall dock), says only what it must, and draws its numbers as pictures. Activity and Today keep a fixed height, the lists take the rows they hold, and History takes what's left; rows History can't fill give Activity every lane and the Today charts more height first, so nothing jumps as work comes and goes and a new project's pane isn't half empty. Top to bottom:
- the head: project, mode and the mascot; a bar of the work, done today against what's left (now, queued, inbox, blocked), each part counted beside it; and the one thing that needs you, most urgent first: a paused Foreman hook, a question waiting for your answer, a yes Foreman is waiting for, a plan waiting for approval (✓ approve, or *show* to read it in the task block), a task that just closed (a green sweep, grade, proof and time, for six seconds), failing gates, halved spend caps, a decision due for another look, what closed since your last message; otherwise *nothing needs you*;
- the task: type, id and size, criteria proved and time on it against the usual, the title, a bar with a segment per step (*3 of 5 steps done · 2 left*), the stage rail from plan to close, and the steps around the current one (one glows green as it gets done). With nothing active: what's next and how many closed today, or a plan waiting for your yes;
- **Activity**: one braille lane per kind of tool call (edit, run, read, agent, skill, web) plotting the session's calls over the last 30 minutes; at the end of each lane, what runs there now (a background shell its command) or the count and the last thing it touched;
- **Agents**, while there are any: a node graph rooted at this session, its calls on the root's bar, with a branch (`├─`, `└─`) to each subagent (running, or finished in the last half hour), each brainstorm and each lone git worktree (whether it holds commits to merge), and a builder's worktree hanging under its agent; every node's bar sits in one column on an axis of its own: each bar runs from start to end (or now) with a dot where a tool call or an answer landed, then the name and how it stands (time, quiet, ✓ calls), and ■ stop for a subagent quiet ten minutes;
- **Up next**: plans waiting for your yes (each with ✓ approve), the queue, the inbox with Start and Drop, and a capture box (Enter runs `fm capture` without interrupting Claude);
- **Sessions**, when there are others: each with its context and task, and one steer for all;
- **History**: what happened, newest first, one line each: the time, the id, the event in its colour (red for a failure, green for a pass or a close) and the task's title;
- **Closed per day** for 14 days beside **Today**: four tanks for context, spend against the day's cap, hook latency and gates passed, each with its value over it;
- Next, Drive, Autonomy, Mute and Refresh.

**The live tree.** The band above the prompt stays put while the chat scrolls, so while work runs it holds one tree of everything happening now: this session at the root (its task and step, a comet along its rule) with the last thing Claude said it is doing, its latest calls under it, then a branch per subagent with its own words (each model step's first line, streaming in as it is written), its worktree if it is a builder, and its own latest calls, each call spinning while it runs, then ✓ or ✗ with its time. A fading rule separates it from the chat above. It keeps one height for the whole turn, with a blank row under it, so the chat above never shifts as calls come and go, and every node has a time bar in one column, as in the pane's Agents graph. It fits the band: words go last (one line per node is kept while calls shrink, fewer lines each as agents multiply), the agents keep one call each before the session's older calls go, then the least recent agents fold into a count. It stays two minutes after the last call, then shrinks to one line for the session. With the panel open the band shows only that tree (the prompt hint still says when Foreman needs you). The charts move at about 30 fps while Claude works and stand still when idle; the `motion` setting picks `full`, `calm` (8 fps) or `off`. Toasts mark finished steps and tasks, needed yeses (with a soft chime) and guard refusals. The mod only renders `fm ui --json` and runs `fm` on your presses; rules and gates stay in fm and the classic hooks.

**The forever loop.** `fm loop on` makes Foreman keep improving without being asked: when the queue and inbox run out, `fm next` and the Stop drive start the next round instead of ending the run. A round reviews what shipped since the last one, brainstorms past the newest earlier brainstorms, grounds the ideas in the code, queues every one that holds up and builds them; it counts how many ideas the round queued (`fm loop yield N` says it outright; otherwise Foreman counts the tasks made during the round), and two thin rounds in a row (fewer than three each) or `fm loop off` end it; usage running ahead of pace pauses it until there is room, and a closed task or a new round counts as progress, so the drive's 50-push cap stops only real spinning. The pane and the band show `∞ round N` while it runs.

**The chat as a tree.** The scrolling transcript reads the same way: each turn is one tree, your prompt at the root, every call Claude makes a branch (`├─`) on a rail down the left, its replies on branches too, and the turn's closing line (`└─ ✻ worked 22s · 6 tools · 1 edit`) the tip. Finished calls are compact so the chat scrolls far less: a passing command shows its description, one line of the command and a line count (its output only when it is a line or two), a failure shows its failures in full, a diff shows four changed lines and a count of the rest, reads and searches sit on one line. The `chat` setting `full` brings back the long rows.

**The status line.** Under the prompt is one clean true-color layout:
- a session line: model, folder, branch, context and rate-limit bars, cost, lines changed;
- a Foreman line: task, stage, step bar, audits, queue, autonomy, guard.

When the mod's card is above the prompt, the Foreman line shrinks to a chip on the session line. `"statusline_layout": "stack"` in the install manifest brings back the old stack of your original line, claude-hud and the Foreman lines. `NO_COLOR` set drops the colour from Foreman's own lines. In tmux, `set -g status-right '#(cd #{pane_current_path} && fm state --line)'` puts the same task, step and queue in the status bar for the pane you're in (it never creates a project).

Also: per-subagent rows, terminal titles and desktop notifications, `fm watch`, and an optional OpenTelemetry → telegraf → InfluxDB → Grafana setup in `plugin/observability/`. `/tui fullscreen`, `/focus` and `Ctrl+O` help too.

</details>

<details>
<summary><b>Other agents and the desktop app</b></summary>

**Other agents:** `fm agents install codex|gemini|opencode` puts Foreman into Codex, Gemini CLI or opencode: its guard, per-turn context, `fm mcp` server and a short rules block. They run through the same hook Claude Code runs (`hook --agent X EVENT`). The adapters are built to each tool's documented hook format and tested against recorded payloads, but not yet verified against live CLIs: check that a refused command is refused there before relying on the guard.
- `fm agents list` shows what's wired, and `fm agents uninstall X` takes out exactly what install added.
- Codex also gets the drive and done-gate (its Stop hook).
- Two things stay Claude Code only: Gemini's AfterAgent would discard the answer it blocks, and the `fm ask` permission prompt needs Claude Code to show it.

**MCP:** `fm mcp` serves the project to any MCP client over stdio, read-only: its state, next action, recall, research and briefs, the stack library (`lib_suggest`, `lib_search`, `lib_show`) and the instruments (`outline`, `sym`, `impact`, `why`, `fail` on given text, `logs`, `data`, `trace`). Paths must resolve inside the project, values can't start with `-`, each is length-capped, each call has a timeout, and everything sent is redacted. `fm mcp register claude` prints the `claude mcp add` line. `fm mcp new NAME --wrap 'CMD' [--sub a,b]` writes a stdlib-only MCP server for any CLI, plus a test that drives it over stdio. The server runs argv, never a shell; each argument is a plain value or one of the subcommands; it has a timeout and an output cap; and it refuses to wrap destructive commands (`rm`, `git push`, a shell…). Register it with `fm mcp register claude DIR`.
- A config with comments (JSONC) is left alone with a note.
- The files that load the hooks are protected core, like Claude Code's settings: `~/.codex/hooks.json` and `config.toml`, `~/.gemini/settings.json`, and opencode's `opencode.json` and `plugins/`, including their project-level copies. An agent that edits them, or runs `fm agents uninstall`, needs your yes.

**Knowledge out:** `fm recall --export-rules` writes the lessons from finished tasks to `.claude/rules/foreman-lessons/`, one rule file per task scoped by `paths:` to the files it touched, so Claude Code loads a lesson only with its files, even without Foreman. `fm decide --export-adr DIR` writes one ADR file per recorded decision. `fm task defer ID --until "when PATH changes"` brings a task back in `fm next` once that file changes.

**Desktop app:** [Foreman Desktop](https://github.com/ChaseSunstrom/foreman-desktop) (Tauri 2 + Svelte 5; `install.sh --desktop` installs its newest release) shows every project, agent session and device in one animated window.
- Live project dashboards with Start, Drop, Approve-plan, capture, drive and autonomy controls.
- It starts, watches, messages and stops sessions for Claude Code, Codex, Gemini CLI and opencode.
- It opens every Claude Code session on every device: terminal, Remote Control and headless. For each, it shows the conversation with images, subagents and their transcripts, and scratchpad files and pictures, and it can continue the session.
- A Remote control page, a Ctrl+K palette, and agents and devices pages, with your tailnet's machines suggested.

The app never talks to a server: it runs `fm … --json` on this machine, and on other devices over ssh. Its live views come from `fm projects --follow`, `fm ui --follow`, `fm session list --follow` and `fm session tail --follow`.

</details>

## Permissions

Foreman is built for bypass mode (no tool-call prompts), which the installer offers to turn on. What still stops a dangerous command is Foreman's guard hook, plus 20 deny rules for the truly catastrophic cases. The guard covers:
- recursive deletes outside the project;
- force-pushes and hard resets on default branches;
- reading credential files (~/.ssh keys, ~/.aws/credentials, ~/.netrc …), sending the environment or a key over the network, and `curl | sh`;
- recursive or world-writable `chmod`/`chown` on /, the home folder or system folders;
- disk, firewall and system-service changes;
- publish and deploy commands;
- direct writes to Foreman state, edits to Foreman's own protected core and to Claude Code's `~/.claude.json`;
- starting a remote session.

A blocked command says how to authorize it for the current task. For anything that needs you (Foreman's own code, a remote session, installing plugins or MCP servers, destructive categories), Claude Code shows its own permission prompt saying exactly what would be granted. Approving it grants it, and nothing else can. Chat messages don't cancel it. Like the rest of the guard it is a speed bump, not a sandbox.

<details>
<summary><b>Standing yes, trust mode, sensitive repos and turning bypass off</b></summary>

**Working on Foreman itself a lot?** Say "don't ask to edit Foreman". One prompt (`fm ask ID core --standing`) asks for a standing yes. It covers Foreman's own code, rules and evals for every later task, until `fm standing off`. Claude Code's settings, Foreman state and the guard file itself still ask each time.

**Trust mode.** To let Claude edit those too (the guard and Claude Code's settings, never Foreman state), type `/fm-trust on` yourself. The foreman-ui mod only accepts it from your own prompt (or your phone), never from Claude, a scheduled prompt or a skill, and the guard refuses any attempt by Claude to turn it on. The band shows `⚠ trust on` while it lasts. `/fm-trust off` (or `fm trust off`) ends it. Other questions come as a prompt too.

**Fewer dialogs outside bypass mode.** In Claude Code's default mode every Bash command off your allow list asks. Type `! fm approve-reads on` and Foreman answers that dialog for commands that only read (`ls`, `cat`, `grep`, `git status` or `git log`, `find` without `-exec` or `-delete`, …): every part of the command has to be one of those without a writing flag, with no redirect except to `/dev/null` and no `$` (a variable can print a secret). Anything else still asks. Only you can turn it on (the guard refuses it from Claude); `fm approve-reads off` ends it.

**Sensitive repos.** To opt a repo out (client code, anything with production credentials), tell Claude "this repo is sensitive" (it runs `fm sensitive on`). That writes this to the repo's `.claude/settings.local.json`, kept out of commits via `.git/info/exclude`, and Foreman shows the repo as sensitive at session start:

```json
{ "permissions": { "defaultMode": "default" } }
```

Use `"default"` (or `"acceptEdits"`), not `"auto"`: Claude Code ignores `auto` and `bypassPermissions` in project and local settings. `fm sensitive off` undoes it.

**Turning bypass off.** To turn bypass off everywhere, set `defaultMode` back to `"auto"` (or delete it) in `~/.claude/settings.json`. The original is in `~/.claude/foreman/backups/`.

</details>

## Headless: keep it working on a server

In a repo on your server, ask Claude to "serve this repo". Claude asks you once (a yes grants `remote`), then `fm serve` starts Claude Code Remote Control there as a systemd user unit, and the project switches to full autonomy with drive on.
- The unit survives logout and reboot: it turns on linger, or says why it couldn't.
- It restarts on failure. After five failed restarts in ten minutes it stops, and `fm serve status` or `fm doctor` says why. It doesn't wait out usage limits.
- Send feature requests from claude.ai/code or the Claude app whenever you like. They're captured, planned, built, audited and committed one after another.
- "Stop serving" (`fm serve stop`) undoes it, and uninstall stops every unit.
- Claude Code has to trust the repo first: open `claude` there once.

`fm run` is the other option. It works the queue in fresh `claude -p` sessions, one task each, so a long queue never piles up in one context. It waits out a usage limit (up to six hours by default) before retrying. A task that makes no progress is blocked with the reason, so the next run moves on, and the machine is kept from sleeping while it runs (systemd-inhibit, where there is one). To run `fm night` every night, `fm night --print-timer` prints a systemd timer and a crontab line to paste. The sandbox is opt-in: `fm run --sandbox`, or `fm sandbox on` to keep it for later runs and `fm night` timers (`--no-sandbox` skips it for one run). Each session then runs under Claude Code's own sandbox (bubblewrap with socat on Linux, Seatbelt on macOS): Bash writes only the checkout, the cache dirs, Foreman's state and the git dir, and reaches only the allowed domains (`fm sandbox allow DOMAIN`; default: the git remote's host and the package registries for the project's languages). `fm run` refuses to start when the host can't run the sandbox. `fm outbound ID` lists the hosts and queries a task's sessions reached.

### Foreman Code: any model, Foreman's loop

`fm code "make calc.add add"` runs Foreman's loop without Claude Code, on whatever model you have: a local server (Ollama, LM Studio, llama.cpp, vLLM), a profile in `$FOREMAN_HOME/models.json`, or a cloud whose API key is set (`fm code models` lists them). The harness does the stations itself: the model writes a short plan (checked, and sent back to fix when it's malformed), then picks one action at a time for each step. Every edit, file write and command goes past Foreman's guard first, so a refused `rm -rf ~` never runs; the model reads the refusal and tries another way. The harness runs each criterion's check, hands a failure back to the model (three rounds, three more on `--escalate MODEL`), and closes and commits the task, or blocks it with the reason.
- `--dry-plan` shows the plan and changes nothing. `--no-commit` closes without committing. `--json` prints one event per line.

#### What you can ask

Anything you'd ask a coding agent, in plain words. With no model or API key set up, fm code uses the Claude Code CLI if you have it (it says so when it starts); `--worker codex` (or `gemini`, `aider`) picks another: that CLI plans in its read-only mode and does each step, and fm code still makes the task, runs every check before and after, and commits only when they pass. Real runs of each kind are on the [fm code page](https://chasesunstrom.github.io/foreman/features/code.html#ex-fix), recorded in `demo/examples/`.

- A bug: `fm code "total() in cart.py ignores the quantity" --worker claude` writes a failing test, fixes it, proves both.
- A feature: `fm code "add a --json flag to todo.py, with a test"`.
- A change across files: `fm code "rename fetch_user to load_user everywhere"`.
- Docs: `fm code "document every environment variable config.py reads in README.md"`.
- A question: `fm code "what does parse_dates do with a date that has no timezone?"` answers from the files, citing them, and changes nothing (no task).
- A new project: in an empty `git init` folder, `fm code "make a Python CLI that counts lines, words and characters, with tests"`.
- Any language: the checks are the project's own commands (`npm test`, `cargo test`, `go test`, `pytest`, a one-line assert).
- A run that was killed or lost its model carries on with `fm code --resume`.
- claude's own flags work where they mean the same thing: `fm code -p "fix add"` (`--print`) is `--plain`, `-c` (`--continue`) is `--resume` (the newest unfinished run), and `--output-format json` is `--json` (fm code's own events; `text` and `stream-json` are refused). fm's `-p PROJECT` goes before the verb (`fm -p SLUG code …`), or `--project` after it.
- The claude sessions fm code starts run lean: none of your plugins, MCP servers or settings hooks load there, only Foreman's guard, and the planner also has no tool that runs code (`--restricted`). On this machine that halved a planner call's input (31,620 → 15,286 tokens); `python3 plugin/tests/e2e/lean_probe.py` measures it and checks the guard still refuses. `lean = false` in `$FOREMAN_HOME/code.toml` launches them as before. A lean worker whose session starts with an MCP server, an `mcp__` tool or a plugin that isn't built in (a repo's `.mcp.json` or `.claude` settings got through) is stopped at its first line and the run blocks, naming them. Inside a run, a coding CLI's `fm` only reads: every command that changes Foreman's state, grants above all, is refused there.
- While a coding CLI works, each file it reads or edits and each command it runs shows as it happens (claude's stream; `--json` gives `tool` events), and a quiet turn says it's still working every 10 s.
- `fm code runners` lists every coding CLI fm code knows (claude, codex, gemini, aider, opencode, qwen, cursor-agent, goose, amp), which are installed, which can plan read-only, and the one a run with no flags uses (`--check` asks each for its version, and names any configured model id its provider has retired, with the replacement, from a table dated in the output). `fm code runners --use codex` makes it the default; add `--here` for this project only (a name, never a command; `--use ''` clears it). It lists the models set up too. Your own CLI goes in `$FOREMAN_HOME/code.toml`: `[runners.mine]` with `work = "mycli {prompt}"` (and `plan = …` for its read-only mode), then `runner = "mine"`. Only claude's read-only mode has been verified to only read; another plans only when you name it, with a note, and the run stops if its plan changes a file. A template that turns its CLI's own approvals off (`--yolo`, `--dangerously-skip-permissions`, `danger-full-access`, `--approval-mode yolo`, …) is refused until you add the `[ack]` line the refusal prints, which holds that exact template's hash: change the template and it needs a new one. The list says which runners' shell commands Foreman's guard confines (claude, launched lean) and which only have their file changes judged afterwards.
- `fm code bench --model qwen2.5-coder:32b` (or `--worker codex`) grades a model or CLI as a Foreman worker on five seeded tasks in throwaway repos: a seed counts only when its own check passes afterwards, the dangerous one must leave its canary file alone, and the score is kept in `code-bench.jsonl` so runs can be compared (a subset only with the same subset). `--seeds operator,rename` picks seeds, `--seed-timeout` (600 s) and `--max-steps` (40) bound each one; a worker CLI runs with your real home folder, for its sign-in, so it skips the dangerous seed. `--json` prints the run: `ts`, `foreman`, `seed_set`, `seed_names`, `model`/`worker`, `seeds`, `closed`, `score`, `previous` and per seed `seed`, `closed`, `reason`, `verify_runs`, `refusals`, `tokens`, `seconds`, `canary` (or `skipped`).
- `fm code` on its own opens the app, the way `claude` does: inside a project, that project's active task, queue, inbox, blocked tasks and past runs; `Esc` (or `p` from a run) lists every Foreman project on the machine, newest first, with what each is doing. `Enter` or `r` on a task runs it there (`fm code --task ID`: the task's own criteria and steps are the plan, no planner call; one run per task at a time), `Enter` on a past run replays it, `n` starts a new request in that project's folder, and `m` picks the runner.
- On a terminal, `fm code "make calc.add add"` opens the app with that run going, the way `claude "<prompt>"` does; `--plain`, `--json`, `--dry-plan` or a pipe keep the line-by-line output.
- `fm code tui "make calc.add add"` runs the same loop in a terminal UI: a track of the stations, check chips, change bars, a time chart and tokens per call, with the diff (`d`), past runs (`h`), the model or worker picker (`m`) and the settings (`,`) a key away. It draws in 24-bit colour and moves: the working station pulses, counters and bars ease to their values, a guard refusal flashes and the close sweeps the track (`motion = reduced` or `off` stills it; `--record run.mp4 --events RUN.jsonl` films a run, [demo](demo/code-tui.mp4)). `fm code tui --print-config > ~/.claude/foreman/tui.toml` gives you its theme (night, paper, signal for colour-blind eyes, mono), motion, layout and keys to edit (`fm settings list` shows them beside the Claude Code pane's, and `fm settings set motion reduced` changes one in place, keeping your comments; `fm settings diff` lists the ones you changed and flags any nothing reads, `fm settings export` prints them as one share code for `fm settings import CODE`, which checks every key before writing any, and `fm settings undo` puts the last set or import back; inside the app, `,` lists them by group with search, changed-only and `:set KEY VALUE`, and the app's own apply at once; a theme, palette or motion change is a preview until a key keeps it, and goes back after 10 s without one); a Python file in `~/.claude/foreman/tui/` can add a panel or a command (see `plugin/templates/tui/cost_meter.py`); one that fails or runs slow (a panel over 50 ms, a command over 2 s) is switched off with a note, never taking the screen down.
- In a repo marked sensitive, only a model on this machine is used.
- `fm code "FIX: make calc.add add" --worker codex --verify "python3 test_calc.py"` hands each step to a CLI you already have (`claude`, `codex`, `gemini`, `aider`, or your own `'CMD {prompt}'`; only codex runs shell commands, inside its own sandbox; it and the verify get no forge, cloud, registry or other credentials, and a sensitive repo is refused), one unattended turn at a time, killed after `--worker-timeout` seconds (1200). After each turn the harness kills what it left running and puts back anything Foreman refuses (a protected file, ignored or not, a planted git hook or config, your shell startup files, other agents' settings and the MCP servers in `~/.claude.json`) and says so; the worker runs as you, so Foreman judges what it wrote, not what it read or sent; its own verify decides, never the worker's word. `--verify` plans without a model.

## When not to use Foreman

- **Quick one-off questions or scripts.** Planning, evidence and audits are overhead for a five-minute job; plain Claude Code is faster. Foreman sizes work as S/M/L, but even S has a brief.
- **Native Windows.** Foreman needs Linux, macOS or WSL.
- **When you want to approve every command yourself.** Foreman is built for bypass mode with its guard as the brake. It works in the default mode too, but its unattended drive will keep stopping at prompts.
- **Tight token budgets.** Brainstorms, second plans and audits run extra model sessions (capped by `fm budget`). Turn them down, or skip Foreman for budget-critical work.
- **Code that must not leave the machine.** Mark the repo sensitive (`fm sensitive on`) so outward tools are refused, or don't use cloud-facing features there at all.

## Does it improve itself?

Within limits. Ideas come from retros, your corrections and its own metrics, and land in Foreman's own inbox. `/foreman:improve` builds candidates in a separate git worktree, runs the `claude plugin eval` suite against the live version, and only proposes changes that score at least as well. You approve every merge, and it can't edit its own guard, permission settings, rules or eval suite without your authorization.

## Documentation

| | |
|---|---|
| [`MASTER.md`](MASTER.md) | The system map: how to prompt it, every file, how the parts interact, operations and limitations. Start here. |
| [`INSTALL.md`](INSTALL.md) | Installation steps written for an agent to follow, asking before each change. |
| [`CHANGELOG.md`](CHANGELOG.md) | Release notes. |
| [`BUILD_PROMPT.md`](BUILD_PROMPT.md) | The spec Foreman was built from, including the plugin choices (§4.6 and Appendix A). |

## Updating and removing

- **Update:** `git pull` in `~/.claude/foreman` (then `/reload-plugins`), or rerun `install.sh`.
- **Health check:** ask "is foreman ok?" (`fm doctor`). **Hygiene:** "clean up" (`fm tidy`).
- **Remove:** `~/.claude/foreman/plugin/uninstall.sh`. It uninstalls the plugin and marketplace and undoes the wiring. It keeps `state/` unless you pass `--purge-state`, and `--dry-run` previews.

<details>
<summary><b>Starting from a clean slate (optional)</b></summary>

`reset-claude.sh` resets only the parts that change Claude's behavior, after backing up `~/.claude` and `~/.claude.json` to `~/.claude-reset/<timestamp>/`. It resets:
- plugins, except the ones Foreman keeps;
- user hooks and permissions;
- the global CLAUDE.md, rules, skills, agents and commands.

Login, MCP servers, history, memory, themes and per-repo `.claude/` folders are untouched. Undo with the `tar` command it prints.

```bash
./reset-claude.sh            # dry run
./reset-claude.sh --apply    # close Claude Code first
```

</details>

## Development

```bash
python3 plugin/tests/run.py                                     # unit + behaviour, one test class per core (~80 s)
python3 plugin/tests/bench_hooks.py --runs 50                   # hook latency
python3 plugin/tests/e2e/roundtrip.py                           # install/uninstall/reinstall in a sandbox HOME
python3 plugin/tests/e2e/scenarios.py                           # live §12 scenarios (uses claude -p; costs tokens)
python3 demo/record.py [--mp4]                                  # re-record the demo above (demo/demo.cast, .svg, .mp4)
python3 demo/record_live.py [--from-cast]                       # re-record Claude Code + the mod (demo/live.*; a Sonnet turn)
```

```
BUILD_PROMPT.md       the spec Foreman was built from
MASTER.md             system map (start here)
CHANGELOG.md          release notes
install.sh            one-liner bootstrap
setup-plugins.sh      curated plugin setup (safe to re-run; --dry-run to preview)
configure-repo.sh     one-time for forks: point everything at your GitHub repo
reset-claude.sh       optional: reset Claude Code's behavior layer before installing
release.py            thin wrapper over `fm release VERSION [--push]` (--push needs the task's publish grant)
.claude-plugin/       local marketplace "foreman"
plugin/               the Foreman plugin (fm, hooks, skills, rules, agents, tests, evals)
demo/                 the README's recordings (Claude Code with the mod; fm demo) and the scripts that make them
local/ state/ backups/   machine-specific, gitignored
```

The reasoning behind the curated plugins, their measured context costs and conflicts are in `BUILD_PROMPT.md` (§4.6 and Appendix A) and `MASTER.md`. Preview what `setup-plugins.sh` would change with `./setup-plugins.sh --dry-run`.
