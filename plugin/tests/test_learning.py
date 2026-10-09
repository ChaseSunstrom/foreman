"""T-0680: self-improvement and learning — first versions: the hooks log what they inject and which lessons they
show; the friction digest turns that into a note budget, check candidates and lesson counts; and dead ends stay out."""
import datetime
import json
import os

from helpers import ForemanTestCase

import fmcore as c


def events():
    try:
        with open(os.path.join(c.state_dir(), "events.jsonl")) as f:
            return [json.loads(x) for x in f if x.strip()]
    except OSError:
        return []


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.fm("task", "new", "Edit a", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")

    def log(self, **e):
        e.setdefault("ts", datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        e.setdefault("project", self.p.slug)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a") as f:
            f.write(json.dumps(e) + "\n")


class InjectLog(Base):
    def test_a_shown_lesson_and_its_note_are_logged(self):
        with open(os.path.join(self.p.dir, "tripwires.json"), "w") as f:
            json.dump({"a.py": [["T-0009", "retry the token refresh with backoff"]]}, f)
        path = os.path.join(self.repo, "a.py")
        out = self.hook("PreToolUse", {"tool_name": "Edit", "tool_input": {"file_path": path, "old_string": "x",
                                                                          "new_string": "y"}}).stdout
        self.assertIn("retry the token refresh", out)
        ev = events()
        self.assertTrue([e for e in ev if e.get("kind") == "lesson_shown" and e.get("task") == "T-0009"])
        inj = [e for e in ev if e.get("kind") == "inject" and e.get("event") == "PreToolUse"]
        self.assertTrue(inj and inj[-1]["chars"] > 20 and inj[-1]["key"])


class FrictionSections(Base):
    def test_the_digest_shows_the_note_budget_repeats_and_lessons(self):
        for _ in range(4):
            self.log(kind="inject", event="PostToolUse", key="edited times without a check", chars=180)
        self.log(kind="inject", event="PreToolUse", key="also changed this file", chars=120)
        self.log(kind="lesson_shown", task="T-0009", file="a.py")
        text = self.fm("friction").stdout
        self.assertIn("injected notes", text)
        self.assertIn("edited times without a check", text)
        self.assertIn("a hard check", text)
        self.assertIn("lessons shown", text)
        self.assertIn("T-0009", text)


class DeadEnds(Base):
    def test_a_rejected_item_is_skipped_and_counted(self):
        self.fm("task", "log", "T-0001", "steer: the flaky export check again")
        self.assertIn("flaky export", self.fm("friction").stdout)
        self.fm("friction", "--reject", "flaky export", "--why", "fixed upstream; not ours")
        text = self.fm("friction").stdout
        self.assertNotIn("flaky export check again", text)
        self.assertIn("dead end", text)
