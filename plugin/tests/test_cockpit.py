"""T-0711 (Frontier 11, first slice): the pane's view model carries the fleet (live sessions here, cached tiles from
remotes the user added) and the active task's children."""
import json
import os

from helpers import ForemanTestCase

import fmcore as c


class Cockpit(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")

    def ui(self, **env):
        return json.loads(self.fm("ui", "--json", env=env).stdout)

    def test_the_fleet_has_live_sessions_and_only_added_remotes(self):
        d = os.path.join(self.home, "state", "sessions")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "sess-x.json"), "w") as f:
            json.dump({"ts": c.now(), "session_id": "sess-x", "project": "demo", "cwd": self.repo, "context_pct": 40}, f)
        fleet = self.ui()["fleet"]
        self.assertEqual([s["session"] for s in fleet], ["sess-x"])
        self.assertFalse(any(s.get("remote") for s in fleet), "no remote was added")
        self.fm("conductor", "remote", "add", "jarvis", "jarvisdev@jarvis.example")
        bus = os.path.join(self.home, "state", "bus")
        with open(os.path.join(bus, "remote-jarvis.json"), "w") as f:  # what a refresh over ssh leaves
            json.dump({"ts": c.now(), "sessions": [{"session": "j-1", "project": "jarvis-d7aeca", "task": "T-0341",
                                                    "context_pct": 38}]}, f)
        tiles = [s for s in self.ui()["fleet"] if s.get("remote")]
        self.assertEqual((tiles[0]["remote"], tiles[0]["task"]), ("jarvis", "T-0341"))
        self.assertIn("jarvis", self.fm("conductor", "remote").stdout)

    def test_the_active_task_lists_its_children(self):
        self.fm("task", "new", "Big one", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        self.fm("task", "new", "Part a", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        p = c.find_project(self.repo)
        with c.lock(p.dir):
            kid = c.find_brief(p, "T-0002")
            kid.meta["parent"] = "T-0001"
            c.save_brief(p, kid)
        kids = self.ui()["active"]["children"]
        self.assertEqual([(k["id"], k["status"]) for k in kids], [("T-0002", "planned")])
