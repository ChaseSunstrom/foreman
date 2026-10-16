"""The feature pages (T-1220): content as data, charts as calls into build.py's helpers over site/data/stats.json.
Every claim here is something Foreman does today; the charts are its own record of building itself."""
from build import TYPES, columns, esc, hbars, line, pairs, tiles, verdicts


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


def _duel(s, name):
    d = next((x for x in s.get("duels") or [] if x.get("name") == name), None)
    if not d or not d.get("cases"):
        return "<p><strong>Not run yet.</strong> Its results replace this line when the run finishes.</p>"
    cs = d["cases"]
    won, lost = sum(c["foreman"]["pass"] for c in cs), sum(c["bare"]["pass"] for c in cs)
    cost_f, cost_b = sum(c["foreman"]["cost"] for c in cs), sum(c["bare"]["cost"] for c in cs)
    time_f, time_b = sum(c["foreman"]["seconds"] for c in cs), sum(c["bare"]["seconds"] for c in cs)
    pct = lambda a, b: round((a / b - 1) * 100) if b else 0
    n = len(cs)
    head = tiles([("Tasks passed, with Foreman", f"{won} of {n}"), (f"Cost of the {n}, with Foreman", f"${cost_f:.2f}"),
                  (f"Time for the {n}, with Foreman", f"{time_f:.0f} s"), ("Tasks passed, Claude Code", f"{lost} of {n}"),
                  (f"Cost of the {n}, Claude Code", f"${cost_b:.2f}"), (f"Time for the {n}, Claude Code", f"{time_b:.0f} s")],
                 "three")
    if won > lost:
        verdict = f"Foreman passed {won - lost} more of the {len(cs)} tasks."
    elif won == lost:
        verdict = f"Both passed {won} of the {len(cs)} tasks."
    else:
        verdict = f"Foreman passed {lost - won} fewer of the {len(cs)} tasks."
    for what, a, b in (("cost", cost_f, cost_b), ("time", time_f, time_b)):
        p = pct(a, b)
        verdict += (f" Foreman's {what} was {abs(p)}% {'lower' if p < 0 else 'higher'}." if abs(p) >= 3 else
                    f" Its {what} was within 3% of Claude Code's.")

    def cell(x):
        mark = "✓" if x["pass"] else "✗"
        if x.get("score") is not None:
            return f"{mark} judge {x['score']} of 5"
        return f"{mark} {x['passed']} of {x['runs']} runs" if x.get("runs", 1) > 1 else f"{mark} hidden tests"
    rows = "".join(f"<tr><td>{c['case']}</td><td>{cell(c['foreman'])}</td><td>{cell(c['bare'])}</td></tr>" for c in cs)
    table = ('<div class="verdicts"><table><thead><tr><th>Task</th><th>With Foreman</th><th>Claude Code</th></tr>'
             f'</thead><tbody>{rows}</tbody></table></div>')
    return (head + f"<p><strong>{verdict}</strong></p>" + table
            + pairs("Cost per task", "USD, as Claude Code reports it.", [(c["case"], c["foreman"]["cost"], c["bare"]["cost"]) for c in cs], unit="")
            + pairs("Time per task", "Seconds from the first prompt to the session ending.",
                    [(c["case"], round(c["foreman"]["seconds"]), round(c["bare"]["seconds"])) for c in cs], unit=" s"))


def _long(s, name):
    """T-1242: one multi-request session per side, compacting as it goes: the hidden tests passing at the end, the
    compactions, cost and time; for a marathon, the work Foreman found and did after the asked work."""
    d = next((x for x in s.get("duels") or [] if x.get("name") == name), None)
    if not d or not d.get("cases"):
        return "<p><strong>Not run yet.</strong> Its results replace this line when the run finishes.</p>"
    f, b = d["cases"][0]["foreman"], d["cases"][0]["bare"]
    tests = lambda x: f"{x['tests'][0]} of {x['tests'][1]}" if x.get("tests") else ("all" if x["pass"] else "failed")
    head = tiles([("Hidden tests passing, with Foreman", tests(f)), ("Compactions, with Foreman", f.get("compactions") or 0),
                  ("Cost, with Foreman", f"${f['cost']:.2f}"), ("Hidden tests passing, Claude Code", tests(b)),
                  ("Compactions, Claude Code", b.get("compactions") or 0), ("Cost, Claude Code", f"${b['cost']:.2f}")],
                 "three")
    said = (f"Foreman's session took {f['seconds'] / 60:.0f} min and Claude Code's {b['seconds'] / 60:.0f} min."
            + (" Foreman's ran until its dollar cap, as a marathon does." if f.get("capped") else ""))
    found = f.get("found") or []
    work = ("<p>What Foreman found and did on its own after the asked work:</p><ul>"
            + "".join(f"<li>{esc(x.rsplit(' (discovered)', 1)[0])}</li>" for x in found) + "</ul>") if found else (
        "<p>Foreman found nothing more worth doing before its cap.</p>" if d.get("marathon") else "")
    return head + f"<p><strong>{said}</strong></p>" + work


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
             "destroy work or leak secrets, and sixteen fully specified coding tasks graded by hidden tests, each run "
             "three times with Foreman and three times with Claude Code on its own.",
     "blocks": [
         ("text", "Why use Foreman", "<p><strong>It stops what you'd regret.</strong> In bypass mode, out of 24 "
          "dangerous commands (deleting a home folder, force-pushing, reading SSH keys, publishing a package) Foreman "
          "stopped 20 and saved a copy before the other 4. Claude Code on its own ran all 24. Foreman stopped none of "
          "25 everyday commands.</p><p><strong>It leaves a record.</strong> Every task has a plan, the checks that "
          "ran and their output, and a commit you can revert.</p><p><strong>What the quality runs show.</strong> On "
          "small tasks where the request spells out every rule, both sides pass everything. There Foreman costs about "
          "10% more with Sonnet and 29% more with Haiku, and takes about the same time, so for a short, fully "
          "specified task you're watching, Claude Code alone is cheaper.</p><p><strong>What they can't show "
          "yet.</strong> Long unattended work across many requests and context compactions, which is what Foreman "
          "is built for, is not measured yet. That benchmark is being built and goes on this page whichever way it "
          "falls.</p>"),
         ("text", "Safety: what runs in bypass mode", "<p>Bypass mode is how Foreman is meant to run: no permission "
          "prompts. Claude Code on its own asks before none of these in that mode. Foreman's guard judges each one "
          "before it runs; the everyday set checks that it doesn't get in the way of normal work.</p>"),
         ("chart", _safety),
         ("text", "Quality: eight fully specified tasks, graded blind", "<p>Each task asks for one small module in "
          "a neutral Python repo (durations, an LRU cache, SemVer precedence, text tables, ranges, dotted paths, a "
          "token bucket, CSV lines). The request states every rule its hidden tests check, so passing means doing "
          "the whole spec, not guessing wording. Both sides get the same request, model, budget and time limit, each "
          "in a clean worktree, three runs per task; a task counts as passed when at least two of its three runs pass. "
          "The Claude Code side runs with no plugins but keeps Foreman's guard on, so neither side can damage the "
          "machine. <code>bench/spec-suite/make.py</code> builds the repo.</p>"),
         ("chart", lambda s: _duel(s, "quality")),
         ("text", "Harder: eight tasks where checking matters", "<p>A second neutral repo, an invoicing package whose "
          "modules share helpers, graded by its whole test suite. Four tasks change a shared helper, where the obvious "
          "edit breaks another module's existing tests unless the request's \"Keep\" rules are followed; four are dense "
          "edge-case specs (text wrapping, INI files, interval arithmetic, a tokenizer). Each task's plausible shortcut "
          "is recorded and proven to fail. Grading restores the reference tests, so editing an existing test can't "
          "pass. <code>bench/spec-suite/make.py --suite hard</code> builds it.</p>"),
         ("chart", lambda s: _duel(s, "hard")),
         ("text", "The harder tasks with a smaller model", "<p>The same eight harder tasks with Haiku on both sides, "
          "where mistakes should be likelier and a test run at the end should matter more. Haiku sessions cost about "
          "a cent each, so Foreman's fixed cost (its skill and agent listings, its hooks and the test run at the end) "
          "weighs more here.</p>"),
         ("chart", lambda s: _duel(s, "hard-haiku")),
         ("text", "One long session: eight requests, compacting as it goes", "<p>The eight harder tasks asked for "
          "at once, in one Haiku session per side. Each side's context is compacted whenever it nears 40,000 tokens, "
          "which brings forward what happens in any long session: earlier work is summarised and the details are "
          "gone. The hidden tests of all eight requests grade where each side ends up.</p>"),
         ("chart", lambda s: _long(s, "long")),
         ("text", "A marathon: Foreman keeps going", "<p>The same long session, but once the asked work is closed, "
          "Foreman's side looks for more work in the repo and does it, test first, until its dollar cap. Claude Code "
          "on its own stops when the asked work is done. The hidden tests still grade the end state, so work found "
          "later can't quietly break what was asked for.</p>"),
         ("chart", lambda s: _long(s, "marathon")),
         ("text", "What the duels changed in Foreman", "<p>Reading the sessions turn by turn showed where Foreman's "
          "extra cost went: not into its context (about 2,000 tokens), but into turns spent on its own commands. A "
          "first run on these tasks cost Foreman 8 to 13 turns where Claude Code used 4. The fixes moved Foreman's "
          "bookkeeping out of the model and into its hooks:</p><ul><li><strong>The task makes itself.</strong> The "
          "first edit of a one-request session creates its task from the request and goes ahead.</li><li><strong>It "
          "closes itself.</strong> At the end, Foreman runs the project's tests and closes and commits the task when "
          "they pass. When they fail, it tells the agent once, so the run fixes its work instead of ending on "
          "it.</li><li><strong>It starts informed.</strong> The session begins with the project's layout and test "
          "command, so the agent writes instead of listing folders.</li><li><strong>Less friction.</strong> Commands "
          "default to the active task, a broken check can be corrected, and only real security names ask for an "
          "adversary review.</li></ul>"),
         ("text", "The first run, and why it was replaced", "<p>The first duel used six tasks from Foreman's own "
          "history and came out at 0 of 6 for Foreman, 1 of 6 for Claude Code, with Foreman costing 33% more. "
          "Reading its transcripts showed the case set couldn't measure either side: three cases graded what Foreman "
          "had learned from this user's own past corrections, which a fresh session can't have, and the other three "
          "checked exact wording their requests never stated. Both sides also worked inside Foreman's own code, which "
          "the guard protects. The transcripts did show where Foreman spent extra turns on its own commands; those "
          "were cut before this run.</p>"),
         ("text", "Method and limits", "<ul><li><strong>Small sample.</strong> Sixteen tasks, three runs each, two "
          "models: enough to see a direction, not a precise rate.</li><li><strong>Both sides passed everything."
          "</strong> Fully specified tasks this size are within reach of today's models without help, so these runs "
          "measure cost and time more than quality; larger, multi-file work and a public benchmark are next."
          "</li><li><strong>Reproduce it.</strong> <code>fm bench duel --vs none</code> runs the quality "
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
