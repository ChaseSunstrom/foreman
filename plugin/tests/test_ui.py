"""fm ui --json: the view model the foreman-ui mod renders (mods/foreman-ui/types/index.d.ts is its TS twin), and
fm task show --json carrying steps, criteria and depends (T-0076)."""
import json
import os

from helpers import ForemanTestCase


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
        self.assertEqual(v["mode"], {"autonomy": "standard", "drive": True, "sensitive": False})
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
        self.assertEqual(set(v["health"]), {"hook_p95_ms", "guard_blocks", "hook_errors"})
        self.assertTrue(v["watch"] and all(os.path.exists(w) for w in v["watch"]))
        self.assertTrue(any(w.endswith("ledger.jsonl") for w in v["watch"]), "appends move the ledger, not the dir")
        plan = q["T-0002"]["plan"]  # what a yes approves is shown where it's given
        self.assertEqual((plan["interpretation"], plan["approach"]), ("x", "y"))
        self.assertEqual([s["text"] for s in plan["steps"]], ["build"])
        self.assertEqual([a["text"] for a in plan["criteria"]], ["csv opens"])
        self.assertNotIn("plan", q.get("T-0003", {}))

    def test_step_text_is_plain(self):
        self.fm("task", "step", "T-0001", "add", "bell\x07 and \x1b[31mred")
        steps = json.loads(self.fm("ui", "--json").stdout)["active"]["steps"]
        self.assertEqual(steps[-1]["text"], "bell and [31mred")

    def test_closed_tasks_are_listed_newest_first(self):
        self.fm("task", "drop", "T-0003", "not needed")
        v = json.loads(self.fm("ui", "--json").stdout)
        self.assertEqual(v["closed"][0], {"id": "T-0003", "status": "dropped"})

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
