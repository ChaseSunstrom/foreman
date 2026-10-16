"""The feature pages (T-1220): content as data, charts as calls into build.py's helpers over site/data/stats.json.
Every claim here is something Foreman does today; the charts are its own record of building itself."""
from build import TYPES, columns, hbars, line, pairs, tiles, verdicts


def _daily_types(s):
    return columns("Tasks closed per day, by type", "Every task Foreman closed on its own code, from the ledger.",
                   s["daily"], TYPES)


def _sizes(s):
    return hbars("Closed tasks by size", "S is a small obvious change, M several files or a design choice, L cross-cutting.",
                 [("S  small", s["tiers"]["S"]), ("M  medium", s["tiers"]["M"]), ("L  large", s["tiers"]["L"])])


def _types(s):
    return hbars("Closed tasks by type", None, sorted(s["types"].items(), key=lambda kv: -kv[1]))


def _evidence(s):
    return columns("Evidence runs recorded per day", "Each one is a command Foreman ran and stored with its exit code and output.",
                   s["daily"], ["evidence"])


def _guard(s):
    return hbars("Guard refusals by rule", "Every block on record, all time. Most are Foreman protecting its own code and state.",
                 sorted(s["guard"].items(), key=lambda kv: -kv[1]))


def _latency(s, keys=None):
    rows = [(k, v["p95"]) for k, v in s["bench"].items() if not keys or k in keys]
    rows.sort(key=lambda kv: -kv[1])
    return hbars("Hook time per event, p95", "Measured by bench_hooks.py; the dashed tick is each hook's budget.", rows,
                 unit=" ms", budget={k: s["bench"][k]["budget"] for k, _ in rows})


def _findings(s):
    return hbars("Review findings by lens", "Confirmed findings from independent reviewers, logged when they report.",
                 sorted(s["findings"]["lenses"].items(), key=lambda kv: -kv[1]))


def _severity(s):
    order = ["HIGH", "MEDIUM", "LOW"]
    return hbars("Findings by severity", None, [(k.title(), s["findings"]["severity"].get(k, 0)) for k in order], series=2)


def _agents(s):
    return hbars("Subagents launched, by kind", "Builders work in worktrees, reviewers read diffs, recon answers questions.",
                 sorted(s["subagents"].items(), key=lambda kv: -kv[1]))


def _lanes(s):
    return columns("Builder lanes merged per day", "Each lane is one task built in its own git worktree, reviewed, then merged.",
                   s["daily"], ["lanes"])


def _cards(s):
    return hbars("Stack cards per area", f"{sum(s['cards'].values()):,} cards in {len(s['cards'])} areas, read only when needed.",
                 list(s["cards"].items()))


def _tests(s):
    return line("Tests in the suite, release by release", "Counted at each release commit; every release passes all of them.",
                s["releases"], "tests", "version")


def _totals(s, keys):
    t = s["totals"]
    names = {"tasks_done": "Tasks closed", "evidence": "Evidence runs", "proofs": "Red-to-green proofs",
             "commits": "Commits", "gate_runs": "Gate runs", "subagents": "Subagents", "lanes_merged": "Lanes merged",
             "findings": "Review findings", "guard_blocks": "Guard blocks", "captures": "Ideas captured",
             "lessons_shown": "Lessons recalled"}
    return tiles([(names[k], t[k]) for k in keys])


def _safety(s):
    x = s.get("safety")
    if not x:
        return "<p>The safety benchmark hasn't been run on this build.</p>"
    n, m = len(x["dangerous"]), len(x["everyday"])
    return tiles([("Dangerous commands stopped", f"{x['stopped']} of {n}"), ("Allowed after saving your work", x["saved"]),
                  ("Everyday commands stopped", f"{x['false_stops']} of {m}")]) + verdicts(x["dangerous"])


def _duel(s):
    d = s.get("duel")
    if not d or not d.get("cases"):
        return ("<p><strong>Running.</strong> The first run of this benchmark is in progress; its results replace this "
                "line when it finishes.</p>")
    cs = d["cases"]
    won, lost = sum(c["foreman"]["pass"] for c in cs), sum(c["bare"]["pass"] for c in cs)
    cost_f, cost_b = sum(c["foreman"]["cost"] for c in cs), sum(c["bare"]["cost"] for c in cs)
    head = tiles([("Passed, with Foreman", f"{won} of {len(cs)}"), ("Passed, Claude Code", f"{lost} of {len(cs)}"),
                  (f"Cost of all {len(cs)}, with Foreman", f"${cost_f:.2f}"),
                  (f"Cost of all {len(cs)}, Claude Code", f"${cost_b:.2f}")])
    if won > lost:
        verdict = f"Foreman passed {won - lost} more of the {len(cs)} tasks."
    elif won == lost:
        verdict = f"Both passed {won} of the {len(cs)} tasks: no difference in what was finished on this run."
    else:
        verdict = (f"Foreman did not do better on this run: it passed {won} of {len(cs)} and Claude Code passed {lost}. "
                   "Single runs of so few tasks are noisy, so read it as no measured gain, not as a measured loss.")
    if cost_f > cost_b * 1.15:
        verdict += f" Foreman's planning, evidence and audits cost {round((cost_f / cost_b - 1) * 100)}% more in all."

    def cell(x):
        mark = "✓ passed" if x["pass"] else "✗ failed"
        return f"{mark} (judge {x['score']} of 5)" if x.get("score") is not None else f"{mark} (hidden tests)"
    rows = "".join(f"<tr><td>{c['case']}</td><td>{cell(c['foreman'])}</td><td>{cell(c['bare'])}</td></tr>" for c in cs)
    table = ('<div class="verdicts"><table><thead><tr><th>Task</th><th>With Foreman</th><th>Claude Code</th></tr>'
             f'</thead><tbody>{rows}</tbody></table></div>')
    return (head + f"<p><strong>{verdict}</strong></p>" + table
            + pairs("Cost per task", "USD, as Claude Code reports it.", [(c["case"], c["foreman"]["cost"], c["bare"]["cost"]) for c in cs], unit="")
            + pairs("Time per task", "Seconds from the first prompt to the session ending.",
                    [(c["case"], c["foreman"]["seconds"], c["bare"]["seconds"]) for c in cs], unit=" s"))


FLOW_CODE = """<div class="flow"><svg viewBox="0 0 760 210" role="img" aria-label="fm code: the harness runs every station; the model fills one slot at a time">
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
<rect class="box" x="10" y="20" width="130" height="64" rx="10"/><text class="t" x="24" y="46">Your request</text><text class="s" x="24" y="66">one line is enough</text>
<rect class="box hot" x="170" y="20" width="150" height="64" rx="10"/><text class="t" x="184" y="46">Plan slot</text><text class="s" x="184" y="66">type, size, checks, steps</text>
<rect class="box hot" x="350" y="20" width="150" height="64" rx="10"/><text class="t" x="364" y="46">Action slot</text><text class="s" x="364" y="66">read, search, edit, run</text>
<rect class="box" x="530" y="20" width="210" height="64" rx="10"/><text class="t" x="544" y="46">Foreman's guard</text><text class="s" x="544" y="66">refusals go back to the model</text>
<rect class="box" x="350" y="126" width="150" height="64" rx="10"/><text class="t" x="364" y="152">Harness verifies</text><text class="s" x="364" y="172">runs the checks itself</text>
<rect class="box" x="530" y="126" width="210" height="64" rx="10"/><text class="t" x="544" y="152">Task closed</text><text class="s" x="544" y="172">evidence, audit, commit</text>
<path class="arrow" d="M140 52H166"/><path class="arrow" d="M320 52H346"/><path class="arrow" d="M500 52H526"/>
<path class="arrow" d="M425 84V122"/><path class="arrow" d="M500 158H526"/>
</svg></div>"""

PAGES = [
    {"slug": "planning", "nav": "Planning", "title": "Every request becomes a plan first",
     "desc": "Intake turns a request into a brief with a type, a size, criteria and the commands that prove them.",
     "lede": "A plain request is enough. Foreman classifies it, writes a brief with what done means and the command "
             "that proves it, and only then lets an edit happen.",
     "blocks": [
         ("text", "What a brief holds", "<ul><li><strong>Type and size.</strong> FIX, FEATURE, CLEAN, PERFORMANCE, "
          "SECURITY or RESEARCH, and S, M or L.</li><li><strong>Acceptance criteria</strong>, each with the command "
          "that proves it.</li><li><strong>Steps, scope and risks.</strong> M and L work lists its approaches first "
          "and says why it chose one.</li><li><strong>An approval</strong> when the work is large, unless you put "
          "Foreman in full auto.</li></ul>"),
         ("term", "FIX: login times out after 30s on slow networks\n"
                  "FEATURE: export report as CSV @src/reports\n"
                  "CONTEXT: Django app; don't touch migrations\n"
                  "DONE-WHEN: all tests pass and the CSV opens in Excel"),
         ("text", "One task at a time", "<p>One task is active. New ideas land in the inbox instead of being chased "
          "halfway, and the queue orders itself: baseline, cleanups, performance, security, fixes, then features, "
          "dependencies first. <code>NOW:</code> switches on purpose.</p>"),
         ("chart", _sizes), ("chart", _types)]},
    {"slug": "proof", "nav": "Proof", "title": "Nothing is done until a command proves it",
     "desc": "Evidence is a command Foreman ran and recorded; a fix needs a test that failed first.",
     "lede": "Saying the tests pass is not evidence. Foreman records the real command, its exit code and its output, "
             "and refuses to close a task without it.",
     "blocks": [
         ("chart", lambda s: _totals(s, ["evidence", "proofs", "gate_runs", "tasks_done"])),
         ("text", "How a task closes", "<ul><li><strong>Evidence per step.</strong> <code>fm task evidence --run</code> "
          "runs the check and stores what happened.</li><li><strong>Red, then green.</strong> <code>fm task prove</code> "
          "runs the test on the starting tree and on the changed one, and shows it fails without the change.</li>"
          "<li><strong>Gates.</strong> <code>fm check</code> runs the project's gates and reuses a pass on an "
          "identical tree.</li><li><strong>One call to close.</strong> <code>fm task finish</code> checks the evidence, "
          "the audits, the docs note and the lesson the task's size needs, then commits its own files.</li></ul>"),
         ("chart", _evidence),
         ("term", "T-0042  FIX small  login times out on slow wifi\n"
                  "✓ step 1  $ pytest tests/test_login.py -k slow   → ✗ exit 1  (fails for the right reason)\n"
                  "✓ step 2  $ pytest tests/test_login.py           → exit 0 · 14 passed\n"
                  "✓ proved  fails without the change, passes with it\n"
                  "✓ audits  self, adversary")]},
    {"slug": "guard", "nav": "The guard", "title": "A guard built for bypass mode",
     "desc": "Every command and edit is read before it runs; dangerous ones are refused and destructive git saves your work first.",
     "lede": "Foreman is meant to run without permission prompts, so the brake has to be real: it reads every Bash "
             "command and file edit before it runs, including the scripts a command calls.",
     "blocks": [
         ("text", "What it refuses", "<ul><li><strong>Deletes outside the project</strong>, the home folder, the root.</li>"
          "<li><strong>Downloads piped into a shell</strong>, force pushes to the default branch, credential reads.</li>"
          "<li><strong>Edits to Foreman itself and its state</strong>, unless you say yes for that task.</li>"
          "<li><strong>Hidden ways to run code:</strong> <code>tar -I</code>, <code>find -exec</code>, "
          "<code>git -c core.*</code>, <code>BASH_ENV</code>, and scripts it reads line by line.</li></ul>"),
         ("chart", _guard),
         ("text", "It fails closed, and saves your work", "<p>If the guard crashes or times out, the call is blocked. "
          "Before <code>git reset --hard</code>, <code>checkout -- .</code> or <code>clean -f</code>, Foreman snapshots "
          "your uncommitted work; <code>fm oops --apply</code> brings it back. Every change to the guard is replayed "
          "against thousands of real commands to show what it would newly block or allow.</p>"),
         ("chart", lambda s: _latency(s, {"PreToolUse:Bash", "PreToolUse:Bash:block", "PreToolUse:Bash:script",
                                          "PreToolUse:Edit"}))]},
    {"slug": "permissions", "nav": "Permissions", "title": "You decide what Claude may never grant itself",
     "desc": "Grants, trust mode, sensitive repos and a daily risk budget keep the dangerous switches in your hands.",
     "lede": "Some things only you can allow: editing Foreman, pushing, starting a server, installing plugins. Claude "
             "asks once through Claude Code's own prompt, and your yes covers exactly that.",
     "blocks": [
         ("text", "The switches", "<ul><li><strong>Grants per task.</strong> <code>core</code> (Foreman's own code), "
          "<code>publish</code> (a push or release), <code>remote</code> (serving a repo), <code>plugin</code> "
          "(installs).</li><li><strong>Trust mode.</strong> <code>/fm-trust on</code> lets Claude edit the guard and "
          "Claude Code's settings; only you can type it.</li><li><strong>Sensitive repos.</strong> "
          "<code>fm sensitive on</code> keeps a repo's content from leaving the machine.</li><li><strong>A daily risk "
          "budget.</strong> Destructive blocks and failed closes spend points; past the cap, autonomy steps down a "
          "notch until tomorrow.</li></ul>"),
         ("chart", lambda s: hbars("Refusals that waited for a yes", "Blocks in the categories only you can grant.",
                                   [(k, v) for k, v in sorted(s["guard"].items(), key=lambda kv: -kv[1])
                                    if k in ("core", "plugin", "state-direct", "credentials")], series=2))]},
    {"slug": "review", "nav": "Audits and review", "title": "Independent eyes before anything is done",
     "desc": "Five audit lenses, reviewers that didn't write the code, and skeptics that try to refute every finding.",
     "lede": "Finished work is checked through lenses with different prompts and context: intent, adversary, edge "
             "cases, operations and maintainability. Small tasks get a self-check; large ones get all five.",
     "blocks": [
         ("chart", _findings), ("chart", _severity),
         ("text", "Review that learns", "<p>Every confirmed finding is logged with its lens and severity. The defect "
          "classes a project keeps shipping go into the next builder's brief, so the same mistake is checked for "
          "before it is made again. <code>/foreman:review</code> runs one reviewer per lens over a diff, then two "
          "skeptics try to refute each finding.</p>")]},
    {"slug": "lanes", "nav": "Builder lanes", "title": "Many hands, one foreman",
     "desc": "Independent tasks run in parallel git worktrees, each reviewed before Foreman merges it.",
     "lede": "Independent tasks go to builder subagents, each in its own git worktree with a brief that says exactly "
             "what to build, how to test it and what not to touch.",
     "blocks": [
         ("chart", _lanes), ("chart", _agents),
         ("text", "From brief to merge", "<ul><li><strong>Brief.</strong> <code>fm lane brief ID</code> writes the "
          "contract: the base commit, test first, the files it may change, the defects reviewers keep finding.</li>"
          "<li><strong>Review.</strong> An independent reviewer reads the branch; findings go back to the builder.</li>"
          "<li><strong>Merge.</strong> <code>fm lane merge</code> runs the task's criteria first and refuses a red "
          "branch.</li><li><strong>Resume.</strong> A stopped session picks its lanes back up.</li></ul>")]},
    {"slug": "drive", "nav": "Drive and headless", "title": "It keeps going until the queue is done",
     "desc": "Drive mode, full auto, fm run and fm serve keep work moving without you watching.",
     "lede": "Drive mode works through the whole queue. In full auto Claude decides, records why, and saves what only "
             "you can approve for one summary at the end.",
     "blocks": [
         ("chart", _daily_types),
         ("text", "Ways to run unattended", "<ul><li><strong>Drive.</strong> The Stop hook names the next task, so a "
          "session doesn't stop while work remains.</li><li><strong><code>fm run</code></strong> works the queue in "
          "fresh headless sessions, one task each, and waits out usage limits.</li><li><strong><code>fm serve</code>"
          "</strong> runs Claude Code Remote Control on a server as a service, so you can send work from your phone."
          "</li><li><strong><code>fm loop on</code></strong> keeps improving without being asked: build a round, "
          "review it, brainstorm on top, repeat.</li></ul>"),
         ("chart", lambda s: _totals(s, ["tasks_done", "commits", "captures", "subagents"]))]},
    {"slug": "cards", "nav": "Stack cards", "title": "It knows your stack, and costs no context until it matters",
     "desc": "Over a thousand stack cards with exact verify commands, failing-test recipes and the mistakes models make.",
     "lede": "Each card gives the commands that verify the work, a failing-test recipe, the mistakes models actually "
             "make and a review checklist. Cards cost nothing until a matching file is edited.",
     "blocks": [
         ("chart", _cards),
         ("text", "Picked by what you touch", "<p><code>fm lib</code> picks the cards that match your repo's manifests "
          "and files. The first edit of a file a card covers brings in that card's pitfalls, once per session; a file "
          "that imports a framework gets that framework's card too. <code>fm lib source add</code> indexes another "
          "skills repo read-only.</p>")]},
    {"slug": "panel", "nav": "The panel", "title": "Foreman, live inside Claude Code",
     "desc": "The foreman-ui mod draws the task, the stage rail, agents, activity and charts in the session itself.",
     "lede": "The foreman-ui mod shows Foreman's state as you work: a card above the prompt, a docked panel beside the "
             "chat, a status line under it, and a chat that reads as a tree.",
     "blocks": [
         ("raw", '<img class="shot" src="../assets/poster.jpg" alt="Claude Code with the foreman-ui panel: the task, '
                 'its stage rail and steps, activity lanes, agents, history and today\'s charts" loading="lazy">'),
         ("text", "What it shows", "<ul><li><strong>The task</strong>, its stage from plan to close, and the step bar."
          "</li><li><strong>Activity lanes</strong> for edits, runs, reads, agents, skills and web calls.</li><li>"
          "<strong>Agents</strong> as a graph with their own recent calls and time bars.</li><li><strong>Today</strong>"
          ": context, spend, hook time and gates as small charts.</li></ul>"),
         ("chart", lambda s: _latency(s, {"SessionStart", "UserPromptSubmit", "Stop", "PostToolUse"}))]},
    {"slug": "speed", "nav": "Speed", "title": "Light enough to forget it's there",
     "desc": "Only the guard runs synchronously; everything else records asynchronously or once per turn.",
     "lede": "Hooks run on every tool call, so each has a time budget and the bench holds them to it. Only the guard "
             "and the write validators run in the call's path.",
     "blocks": [
         ("chart", _latency),
         ("text", "How it stays fast", "<ul><li><strong>Budgets per hook</strong>, checked by "
          "<code>bench_hooks.py</code> on every release.</li><li><strong>Reused gate passes.</strong> "
          "<code>fm check</code> skips a gate that passed on an identical tree.</li><li><strong>Cached verdicts.</strong> "
          "Scripts the guard read are cached by content.</li><li><strong>Notes once.</strong> Context is injected only "
          "when it changes what Claude should do next.</li></ul>"),
         ("chart", lambda s: tiles([("Gate runs", s["gate_seconds"]["runs"]),
                                    ("Median full gate run, s", s["gate_seconds"]["median"])]))]},
    {"slug": "learning", "nav": "Learning", "title": "It learns a fix once, and improves itself",
     "desc": "Known fixes, lessons, tripwires and a self-improvement loop turn friction into fixes.",
     "lede": "When a command fails and a later one gets past it, Foreman keeps the pair. The next session that meets "
             "the same failure gets the fix in the failure message, in any project on the machine.",
     "blocks": [
         ("chart", lambda s: _totals(s, ["lessons_shown", "findings", "captures", "tasks_done"])),
         ("text", "Where improvements come from", "<ul><li><strong>Lessons</strong> written at each close and shown "
          "to the next task that touches the same code.</li><li><strong>Friction passes</strong> that mine real guard "
          "refusals and repeated manual work into tasks.</li><li><strong>Backtests.</strong> <code>fm backtest</code> "
          "shows how often a rule change would have fired on your real sessions before it ships.</li><li><strong>"
          "Foreman on Foreman.</strong> It is built with itself; the charts on these pages are that record.</li></ul>"),
         ("chart", _tests)]},
    {"slug": "tools", "nav": "Tools", "title": "Small tools that save whole turns",
     "desc": "Batch edits, history tracing, time travel and branch tours.",
     "lede": "A handful of commands do in one call what usually takes several turns.",
     "blocks": [
         ("text", "The ones you'll use", "<ul><li><strong><code>fm edit</code></strong> applies a batch of exact "
          "replacements across files, all or none.</li><li><strong><code>fm why FILE:LINE</code></strong> traces a "
          "line back to the task and the words you asked in.</li><li><strong><code>fm at T-0042 -- pytest</code>"
          "</strong> runs any command as of a task's start.</li><li><strong><code>fm tour --since main</code>"
          "</strong> ranks a branch by review risk and says what's safe to skim.</li><li><strong><code>fm digest"
          "</code></strong> sums up the week.</li></ul>"),
         ("term", "@@ src/app.py\n<<<\ntimeout = 30\n===\ntimeout = 90\n>>>\n@@ src/old.py\n<<<\nimport legacy\n===\n>>>"),
         ("chart", lambda s: _totals(s, ["commits", "evidence", "gate_runs"]))]},
    {"slug": "code", "nav": "Foreman Code", "title": "Foreman Code: the loop, on any model",
     "desc": "fm code runs Foreman's stations itself, so small and local models only fill small checked slots.",
     "lede": "In progress. <code>fm code</code> is Foreman's own harness: it runs plan, edit, verify and close itself, "
             "and the model only fills one small checked slot at a time. That is what lets a small local model do "
             "real work, and a big one go faster.",
     "blocks": [
         ("raw", FLOW_CODE),
         ("text", "Any model, any CLI", "<ul><li><strong>Any OpenAI-compatible endpoint</strong>: Ollama, LM Studio, "
          "llama.cpp, vLLM, OpenRouter, Groq, OpenAI, Gemini's compatible endpoint, and Anthropic's API.</li><li>"
          "<strong>Other CLIs as workers.</strong> claude, codex, gemini, opencode or aider do a step; the harness "
          "judges the diff and runs the checks itself.</li><li><strong>The same guard</strong> on every command and "
          "edit, through the hook other harnesses use.</li><li><strong>A bench</strong> that grades any model as a "
          "Foreman worker on seeded tasks.</li></ul>"),
         ("chart", lambda s: tiles([("Model client tests", 52), ("Endpoints it finds", 9), ("Status", "Building")]))]},
    {"slug": "benchmarks", "nav": "Benchmarks", "title": "Measured against Claude Code",
     "desc": "Real runs, published whichever way they fall: dangerous commands, and real tasks graded blind.",
     "lede": "Two benchmarks, run for real on this machine and published as they came out: a set of commands that "
             "destroy work or leak secrets, and real coding tasks graded by hidden tests or a judge, run once with "
             "Foreman and once with Claude Code on its own.",
     "blocks": [
         ("text", "Safety: what runs in bypass mode", "<p>Bypass mode is how Foreman is meant to run: no permission "
          "prompts. Claude Code on its own asks before none of these in that mode. Foreman's guard judges each one "
          "before it runs; the everyday set checks that it doesn't get in the way of normal work.</p>"),
         ("chart", _safety),
         ("text", "Quality: real tasks, graded blind", "<p>Each case is a task Foreman already finished in its own "
          "repo, rewound to its starting commit; the session gets only the original request. Three are graded by the "
          "tests written for them, hidden from the session. Three have no such tests, so a judge model scores the diff "
          "and the final reply against the task's criteria and the user's corrections, and 4 of 5 passes. Both sides "
          "use the same model, budget and time limit, each in a clean worktree. The Claude Code side runs with no "
          "plugins but keeps Foreman's guard on, so neither side can damage the machine.</p>"),
         ("chart", _duel),
         ("text", "What the losses showed", "<ul><li><strong>An unattended reply left out the proof.</strong> On the "
          "task Foreman lost, it recorded its checks in its ledger, but the final reply the judge read didn't show "
          "them.</li><li><strong>A "
          "side task was opened and dropped</strong> mid-run, which the judge counted against it.</li><li><strong>The "
          "three hidden-test tasks were failed by both sides</strong>, so they didn't separate them; each passes with "
          "its original solution under the same grading.</li></ul>"),
         ("text", "Method and limits", "<ul><li><strong>Small sample.</strong> Six tasks, one run each, one model "
          "(Sonnet): enough to see a direction, not a precise rate; <code>--runs 3</code> measures the noise."
          "</li><li><strong>Foreman's own repo.</strong> The tasks come from building Foreman; a public benchmark is "
          "next.</li><li><strong>Reproduce it.</strong> <code>fm bench duel --vs none</code> runs the quality "
          "benchmark on your own finished tasks; <code>python3 site/bench_safety.py</code> reruns the safety set."
          "</li><li><strong>Other plugins.</strong> <code>fm bench duel PLUGIN</code> runs the same cases with another "
          "plugin beside Foreman.</li></ul>")]},
    {"slug": "releases", "nav": "Releases", "title": "Shipped in small, gated releases",
     "desc": "Every release passes the full gates and a release check before it reaches main.",
     "lede": "<code>fm release</code> runs the ritual as nine named steps with a checkpoint after each: gates, version "
             "bumps, changelog, commit, release check, push, round close and a canary in every local project.",
     "blocks": [
         ("chart", _tests),
         ("text", "What a release proves", "<ul><li><strong>The full gates</strong> on the exact commit that is "
          "pushed, never later work.</li><li><strong>A release check</strong>: doctor and the demo in a throwaway "
          "home.</li><li><strong>Your yes to push</strong>, spent by that one push.</li><li><strong>Resumable.</strong> "
          "A stop at any step continues from there with <code>--resume</code>.</li></ul>")]},
]
