"""fm ui --json: the view model the foreman-ui mod renders (mods/foreman-ui/types/index.d.ts is its TS twin), and
fm task show --json carrying steps, criteria and depends (T-0076)."""
import json
import os

from helpers import ForemanTestCase


class UiSkills(ForemanTestCase):
    """T-0939: the pane's Skills card: Skill tool calls and fm lib card reads, this week, and the unread suggestions."""

    def setUp(self):
        super().setUp()
        self.fm("init")
        import fmcore as c
        self.c, self.p = c, c.find_project(self.repo)

    def skills(self):
        return json.loads(self.fm("ui", "--json").stdout)["skills"]

    def test_empty_without_any_use_or_map(self):
        self.assertEqual(self.skills(), {"recent": [], "counts": {}, "suggested": [], "unread": []})

    def test_skill_calls_and_card_reads_this_week(self):
        c, p, slug = self.c, self.p, self.p.slug
        old = c.time.strftime("%Y-%m-%dT%H:%M:%SZ", c.time.gmtime(c.time.time() - 8 * 86400))
        at = [c.time.strftime("%Y-%m-%dT%H:%M:%SZ", c.time.gmtime(c.time.time() - 60 * n)) for n in range(5, 0, -1)]
        rows = [{"ts": old, "kind": "tool", "tool": "Skill", "target": "foreman:old", "project": slug},
                {"ts": at[0], "kind": "tool", "tool": "Skill", "target": "foreman:brainstorm", "project": slug},
                {"ts": at[1], "kind": "tool", "tool": "Skill", "target": "foreman:brainstorm", "project": slug},
                {"ts": at[1], "kind": "tool", "tool": "Skill", "target": "elsewhere:x", "project": "other-1"},
                {"ts": at[2], "kind": "tool", "tool": "Bash", "target": "ls", "project": slug},
                {"kind": "tool", "tool": "Skill", "target": "no:ts", "project": slug},
                {"ts": at[3], "kind": "tool_fail", "tool": "Skill", "target": "foreman:broken", "project": slug}]
        os.makedirs(c.state_dir(), exist_ok=True)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "w") as f:
            f.writelines(json.dumps(r) + "\n" for r in rows)
            f.write("{not json\n")
        with open(os.path.join(p.dir, "ledger.jsonl"), "a") as f:
            f.write(json.dumps({"ts": old, "event": "lib", "data": {"cards": ["bash"]}}) + "\n")
            f.write(json.dumps({"ts": at[2], "event": "lib", "data": {"cards": ["python", "bash"]}}) + "\n")
            f.write(json.dumps({"event": "lib", "data": {"cards": ["nots"]}}) + "\n")
            f.write(json.dumps({"ts": at[4], "event": "lib", "data": {"cards": "python"}}) + "\n")  # malformed
        with open(os.path.join(p.dir, "map.json"), "w") as f:
            json.dump({"lib": ["python", "typescript", "bash", "semver"]}, f)
        s = self.skills()
        self.assertEqual([(x["name"], x["kind"]) for x in s["recent"]],
                         [("python", "card"), ("bash", "card"), ("foreman:brainstorm", "skill")])
        self.assertEqual(s["recent"][2]["at"], at[1], "a name shows once, at its newest use")
        self.assertEqual(s["counts"], {"foreman:brainstorm": 2, "python": 1, "bash": 1})
        self.assertEqual(s["suggested"], ["python", "typescript", "bash", "semver"])
        self.assertEqual(s["unread"], ["typescript", "semver"])

    def test_a_call_from_days_ago_shows_behind_a_busy_events_file(self):
        # a tail of events.jsonl holds an hour or two on a busy day; the week is the whole file
        c, slug = self.c, self.p.slug
        at = c.time.strftime("%Y-%m-%dT%H:%M:%SZ", c.time.gmtime(c.time.time() - 3 * 86400))
        filler = json.dumps({"ts": at, "kind": "tool", "tool": "Read", "target": "x" * 200, "project": slug}) + "\n"
        os.makedirs(c.state_dir(), exist_ok=True)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "w") as f:
            f.write(json.dumps({"ts": at, "kind": "tool", "tool": "Skill", "target": "foreman:intake", "project": slug}) + "\n")
            f.write(filler * 2000)  # ~500 KB
        self.assertEqual(self.skills()["counts"], {"foreman:intake": 1})

    def test_recent_holds_eight_and_a_broken_map_is_no_map(self):
        c, p = self.c, self.p
        for i in range(12):
            c.log_event(p, "lib", data={"cards": [f"card-{i}"]})
        with open(os.path.join(p.dir, "map.json"), "w") as f:
            f.write("{broken")
        s = self.skills()
        self.assertEqual(len(s["recent"]), 8)
        self.assertEqual(s["recent"][0]["name"], "card-11")
        self.assertEqual(len(s["counts"]), 12)
        self.assertEqual((s["suggested"], s["unread"]), ([], []))


class UiView(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.fm("task", "new", "Login times out", "--type", "FIX", "--tier", "S", "--ac", "slow wifi logs in :: true",
                "--step", "red test", "--step", "raise the timeout", "--focus")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true")
        self.fm("task", "step", "T-0001", "done", "1")
        self.fm("task", "new", "CSV export", "--type", "FEATURE", "--tier", "L", "--interpretation", "x",
                "--approach", "y", "--ac", "csv opens :: true", "--step", "build", "--depends", "T-0001")
        self.fm("capture", "Merge the date helpers")

    def test_view_model_contract(self):
        v = json.loads(self.fm("ui", "--json").stdout)
        self.assertEqual(v["v"], 1)
        self.assertTrue(v["project"])
        self.assertEqual(v["mode"], {"autonomy": "standard", "drive": True, "sensitive": False, "trust": False,
                                     "standing": []})
        a = v["active"]
        self.assertEqual((a["id"], a["type"], a["tier"], a["stage"]), ("T-0001", "FIX", "S", "executing"))
        self.assertIn("executing", a["stages"])
        self.assertEqual([(s["n"], s["done"], s["current"]) for s in a["steps"]], [(1, True, False), (2, False, True)])
        self.assertEqual(a["criteria"], [{"n": 1, "text": "slow wifi logs in", "verify": "true", "checked": False}])
        self.assertEqual(set(a["audits"]), {"done", "need"})
        self.assertTrue(a["blockers"])
        self.assertIn("T-0001", v["next"])
        q = {x["id"]: x for x in v["queue"]}
        self.assertEqual(q["T-0002"]["waits"], "plan approval")
        self.assertNotIn("T-0001", q, "the active task isn't repeated in the queue")
        self.assertEqual([x["title"] for x in v["inbox"]], ["Merge the date helpers"])
        self.assertEqual(v["inbox_total"], 1)
        self.assertEqual(v["approvals"], [])
        self.assertIsInstance(v["recent"], list)
        self.assertEqual(set(v["skills"]), {"recent", "counts", "suggested", "unread"})  # T-0939
        self.assertEqual(set(v["health"]), {"hook_p95_ms", "guard_blocks", "hook_errors", "paused_hooks"})
        self.assertTrue(v["watch"] and all(os.path.exists(w) for w in v["watch"]))
        self.assertTrue(any(w.endswith("ledger.jsonl") for w in v["watch"]), "appends move the ledger, not the dir")
        plan = q["T-0002"]["plan"]  # what a yes approves is shown where it's given
        self.assertEqual((plan["interpretation"], plan["approach"]), ("x", "y"))
        self.assertEqual([s["text"] for s in plan["steps"]], ["build"])
        self.assertEqual([a["text"] for a in plan["criteria"]], ["csv opens"])
        self.assertNotIn("plan", q.get("T-0003", {}))

    def test_the_view_carries_budget_bench_research_and_the_tasks_ledger(self):
        # T-0228: what the last sessions added, for the pane
        import fmbudget
        import fmcore as c
        fmbudget.record("bench", 0.4, runs=2)
        fmbudget.record("subagent:foreman:fm-reviewer", tokens=12000)
        self.fm("task", "hypo", "T-0001", "add", "the timeout is per request", "--probe", "grep -n timeout x.py")
        self.fm("task", "assume", "T-0001", "add", "the timeout lives in x.py")
        self.fm("task", "evidence", "T-0001", "--step", "1", "--run", "true", "--inconclusive")
        self.fm("task", "set", "T-0001", "--section", "Oracle", "--text",
                "Examples from the request alone:\n- GIVEN a WHEN b THEN c\nAmbiguities (decide each):\n- which timeout?\n")
        p = c.find_project(self.repo)
        with c.lock(p.dir):
            c.log_event(p, "research", data={"name": "ask-parser-speed", "claims": 5, "verified": 3, "not found": 1,
                                             "unchecked": 1})
            c.log_event(p, "evolve", data={"kept": False, "branch": "evolve/x", "target": "plugin/rules/foreman.md",
                                           "why": "shorter"})
        v = json.loads(self.fm("ui", "--json").stdout)
        self.assertEqual((v["budget"]["today_usd"], v["budget"]["subagent_tokens"]), (0.4, 12000))
        self.assertIn("day", v["budget"]["caps"])
        self.assertEqual(v["budget"]["top"][0]["feature"], "bench")
        self.assertEqual(v["research"][0], {"name": "ask-parser-speed", "claims": 5, "verified": 3, "not_found": 1,
                                            "unchecked": 1, "at": v["research"][0]["at"], "conflicts": 0, "single": 0})
        self.assertEqual(v["bench"]["evolve"][0]["target"], "plugin/rules/foreman.md")
        a = v["active"]
        self.assertEqual(a["hypotheses"], [{"n": 1, "status": "open",
                                            "text": "the timeout is per request — probe: `grep -n timeout x.py`"}])
        self.assertEqual(a["oracle"], {"examples": 1, "ambiguities": ["which timeout?"]})
        self.assertEqual(a["batch"], [])
        self.assertEqual((a["inconclusive"], a["unverified"]), (1, ["the timeout lives in x.py"]))
        self.assertEqual(v["revisit"], [])
        self.assertEqual(v["vetoes"], [])
        self.assertTrue(any("≈" in x and "true" in x for x in v["recent"]), v["recent"])

    def test_step_text_is_plain(self):
        self.fm("task", "step", "T-0001", "add", "bell\x07 and \x1b[31mred")
        steps = json.loads(self.fm("ui", "--json").stdout)["active"]["steps"]
        self.assertEqual(steps[-1]["text"], "bell and [31mred")

    def test_closed_tasks_are_listed_newest_first(self):
        self.fm("task", "drop", "T-0003", "not needed")
        v = json.loads(self.fm("ui", "--json").stdout)
        self.assertEqual({k: v["closed"][0][k] for k in ("id", "status")}, {"id": "T-0003", "status": "dropped"})

    def test_the_view_lists_worktrees_with_their_agent_task_and_unmerged_commits(self):
        # T-1023: the pane's Agents graph joins a builder's worktree to its subagent (Claude Code names the branch
        # worktree-agent-<id>) and shows a lone or stale one
        import subprocess
        git = lambda *a, cwd=self.repo: subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *a],  # noqa: E731
                                                       cwd=cwd, check=True, capture_output=True)
        git("commit", "--allow-empty", "-qm", "base")
        tree = os.path.join(self.tmp, "wt-agent")
        git("worktree", "add", "-q", "-b", "worktree-agent-a1b2c3d4", tree)
        git("commit", "--allow-empty", "-qm", "work", cwd=tree)
        import fmcore as c
        p = c.find_project(self.repo)
        b = c.find_brief(p, "T-0001")
        b.meta["lane"] = tree  # what fm lane new records
        c.save_brief(p, b)
        w = json.loads(self.fm("ui", "--json").stdout)["worktrees"]
        self.assertEqual([(x["branch"], x["agent"], x["task"], x["ahead"]) for x in w],
                         [("worktree-agent-a1b2c3d4", "a1b2c3d4", "T-0001", 1)])
        self.assertIsInstance(w[0]["age_s"], int)
        # review (T-1023): a detached worktree's merge state is unknown, not 'nothing to merge'; the newest come first
        loose = os.path.join(self.tmp, "wt-detached")
        git("worktree", "add", "-q", "--detach", loose)
        os.utime(os.path.join(tree, ".git"), (1, 1))  # made long ago
        w = json.loads(self.fm("ui", "--json").stdout)["worktrees"]
        self.assertEqual([(x["branch"], x["ahead"]) for x in w], [("", None), ("worktree-agent-a1b2c3d4", 1)])

    def test_outside_a_project_the_view_is_empty_not_an_error(self):
        elsewhere = os.path.join(self.tmp, "plain")
        os.makedirs(elsewhere)
        p = self.fm("ui", "--json", cwd=elsewhere)
        self.assertEqual(json.loads(p.stdout), {"v": 1, "project": None})
        self.assertFalse(os.path.exists(os.path.join(elsewhere, ".foreman")))

    def test_task_show_json_has_steps_criteria_and_depends(self):
        t = json.loads(self.fm("task", "show", "T-0002", "--json").stdout)
        self.assertEqual(t["steps"], [{"n": 1, "text": "build", "done": False, "current": True}])
        self.assertEqual(t["criteria"], [{"n": 1, "text": "csv opens", "verify": "true", "checked": False}])
        self.assertEqual(t["depends"], ["T-0001"])


    def test_cards_get_queue_progress_inbox_age_latency_and_the_last_check(self):
        self.fm("check", "add", "python3 -c 'print(1)'")
        self.fm("check")
        self.hook("UserPromptSubmit", {"prompt": "hello"})
        v = json.loads(self.fm("ui", "--json").stdout)
        q = {x["id"]: x for x in v["queue"]}
        self.assertEqual((q["T-0002"]["steps_done"], q["T-0002"]["steps_total"]), (0, 1))
        self.assertEqual(v["inbox"][0]["age_days"], 0)
        self.assertTrue(v["latency"] and all(isinstance(x, (int, float)) for x in v["latency"]))
        self.assertEqual([(r["cmd"], r["exit"]) for r in v["checks"]["results"]], [("python3 -c 'print(1)'", 0)])
        self.assertTrue(v["checks"]["at"])

    def test_today_done_counts_tasks_closed_today(self):
        self.fm("task", "evidence", "T-0001", "--step", "2", "--run", "true")
        self.fm("task", "step", "T-0001", "done", "2")
        self.fm("task", "set", "T-0001", "--section", "Regression test", "--text", "none: fixture")
        self.fm("task", "finish", "T-0001", "--audit", "self checklist")
        self.assertEqual(json.loads(self.fm("ui", "--json").stdout)["today_done"], 1)

    def test_done_days_counts_closes_per_day_for_two_weeks(self):
        # T-0909: the pane's day bars; oldest first, today last, a day counts a task once
        import datetime
        import fmcore as c
        p = c.find_project(self.repo)
        day = lambda n: (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=n)).strftime("%Y-%m-%dT12:00:00Z")  # noqa
        for t in ("T-0001", "T-0002"):  # done briefs; T-0003 and T-0004 aren't (gone or reopened): they don't count
            b = c.find_brief(p, t)
            with open(b.path) as f:
                text = f.read()
            with open(b.path, "w") as f:
                f.write(text.replace("status: planned", "status: done", 1).replace("status: active", "status: done", 1))
        rows = [(day(0), "T-0001"), (day(0), "T-0001"), (day(2), "T-0002"), (day(2), "T-0003"), (day(20), "T-0004")]
        noise = [{"ts": day(0), "event": "note", "task": "T-0009", "data": {}}] * 6000  # past a 5000-event tail (review)
        with open(os.path.join(p.dir, "ledger.jsonl"), "a") as f:
            f.writelines(json.dumps({"ts": ts, "event": "task_done", "task": t, "data": {}}) + "\n" for ts, t in rows)
            f.writelines(json.dumps(e) + "\n" for e in noise)
        v = json.loads(self.fm("ui", "--json").stdout)
        days = v["done_days"]
        self.assertEqual(len(days), 14)
        self.assertEqual((days[-1], days[-3], sum(days)), (1, 1, 2))
        self.assertEqual(v["today_done"], days[-1])

    def test_today_done_ignores_tasks_closed_earlier_and_edited_today(self):
        import fmcore as c
        p = c.find_project(self.repo)
        with open(os.path.join(p.dir, "ledger.jsonl"), "a") as f:  # T-0002 was closed long ago…
            f.write(json.dumps({"ts": "2000-01-01T00:00:00Z", "event": "task_done", "task": "T-0002", "data": {}}) + "\n")
        b = c.find_brief(p, "T-0002")
        with open(b.path) as f:
            text = f.read()
        with open(b.path, "w") as f:  # …and its brief, done, was saved today (an audit note, a lesson)
            f.write(text.replace("status: planned", "status: done", 1))
        self.assertEqual(json.loads(self.fm("ui", "--json").stdout)["today_done"], 0)

    def test_typical_minutes_per_type_and_size_and_time_on_task(self):
        # T-0116: "medium" means more beside "usually ~30 min", from this project's own history
        import fmcore as c
        p = c.find_project(self.repo)
        rows = []
        for i, took in enumerate([10, 30, 50, 20]):  # three closed FIX/S tasks (median 30) and one FEATURE/M
            tid, kind = f"T-09{i:02d}", ("FEATURE", "M") if i == 3 else ("FIX", "S")
            rows += [{"ts": f"2026-01-0{i + 1}T09:00:00Z", "event": "task_new", "task": tid,
                      "data": {"type": kind[0], "tier": kind[1]}},
                     {"ts": f"2026-01-0{i + 1}T10:00:00Z", "event": "focus", "task": tid},
                     {"ts": f"2026-01-0{i + 1}T10:{took:02d}:00Z", "event": "task_done", "task": tid}]
        with open(os.path.join(p.dir, "ledger.jsonl"), "a") as f:
            f.writelines(json.dumps(r) + "\n" for r in rows)
        v = json.loads(self.fm("ui", "--json").stdout)
        self.assertEqual(v["typical"], {"FIX/S": 30}, "one FEATURE/M sample is too few to call typical")
        self.assertGreaterEqual(v["active"]["on_task_s"], 0)
        self.assertLess(v["active"]["on_task_s"], 600)

    def test_the_newest_brainstorm_shows_while_it_runs_and_after(self):
        # T-0124: brainstorms ran unseen inside one long Bash call until it ended
        import fmcore as c
        p = c.find_project(self.repo)
        d = os.path.join(p.dir, "research", "brainstorm-20261003-010203")
        os.makedirs(d)
        with open(os.path.join(d, "status.json"), "w") as f:
            json.dump({"lenses": ["user value", "delight"], "rounds": 2, "started": c.now()}, f)
        with open(os.path.join(d, "r1-01-user-value.md"), "w") as f:
            f.write("# Brainstorm — lens: user value\n\n- **Faster gates** — PERF — value 5\n- **A mascot** — FEATURE\n")
        b = json.loads(self.fm("ui", "--json").stdout)["brainstorm"]
        self.assertEqual((b["running"], b["answers"], b["expected"]), (True, 1, 4))
        self.assertEqual(b["ideas"], ["Faster gates", "A mascot"])
        with open(os.path.join(d, "ideas.md"), "w") as f:
            f.write("# Ideas by round\n\n## Round 1\n- Faster gates\n- A mascot\n- Wild: talk to it\n\n"
                    "## New ideas per lens\n- user value: 3\n")
        b = json.loads(self.fm("ui", "--json").stdout)["brainstorm"]
        self.assertFalse(b["running"])
        self.assertEqual(b["count"], 3)
        self.assertEqual(b["ideas"][:2], ["Faster gates", "A mascot"])
        self.assertEqual(b["name"], "brainstorm-20261003-010203")
        self.assertLess(b["age_h"], 1)  # T-0146: an old one folds to a line in the pane
        self.assertFalse(b["grounded"])
        note = os.path.join(p.dir, "research", "brainstorm-20261003-round1.md")  # T-0196: its slate is built
        with open(note, "w") as f:
            f.write("# Grounded slate\n")
        os.utime(note, (c.time.time() + 5,) * 2)
        self.assertTrue(json.loads(self.fm("ui", "--json").stdout)["brainstorm"]["grounded"])
