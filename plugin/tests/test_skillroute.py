"""fm next names the installed third-party skills that fit a task's stage (T-0205)."""
import json
import os

from helpers import ForemanTestCase

import fmcore as c


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text if isinstance(text, str) else json.dumps(text))


def skill(root, name, desc):
    write(os.path.join(root, "skills", name, "SKILL.md"), f"---\nname: {name}\ndescription: {desc}\n---\nbody\n")


class SkillRoute(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.cc = os.path.join(self.tmp, "cc")
        cache = os.path.join(self.cc, "plugins", "cache", "m")
        paths = {n: os.path.join(cache, n, "1.0") for n in ("pony", "front", "sec")}
        skill(paths["pony"], "pony-audit", "Find over-engineering and bloat to simplify or delete.")
        skill(paths["front"], "front-design", "Distinctive frontend design for web interfaces.")
        skill(paths["sec"], "sec-scan", "Security vulnerability scan.")
        write(os.path.join(self.cc, "plugins", "installed_plugins.json"), {"version": 2, "plugins": {
            f"{n}@m": [{"scope": "user", "installPath": p}] for n, p in paths.items()}})
        write(os.path.join(self.cc, "settings.json"),
              {"enabledPlugins": {"pony@m": True, "front@m": True, "sec@m": False}})
        skill(self.cc, "graphy", "Turn anything into a knowledge graph.")
        self.env = {"CLAUDE_CONFIG_DIR": self.cc}
        self.fm("init")

    def start(self, type_, scope=None):
        tid = json.loads(self.fm("task", "new", f"A {type_} task", "--type", type_, "--tier", "S", "--ac", "ok :: true",
                                 "--step", "do it", "--json").stdout)["id"]
        if scope:
            self.fm("task", "set", tid, f"scope={scope}")
        self.fm("focus", tid)
        return self.fm("next", env=self.env).stdout

    def test_a_matching_enabled_skill_is_named(self):
        out = self.start("CLEAN")
        self.assertIn("/pony:pony-audit", out)
        self.assertIn("/simplify", out, "Claude Code's own skill for the stage")
        self.assertNotIn("front-design", out)

    def test_disabled_plugins_and_unrelated_stages_name_nothing(self):
        out = self.start("FIX")
        self.assertNotIn("skills that fit", out)
        self.assertNotIn("sec-scan", self.start("SECURITY"), "sec@m is installed but disabled")

    def test_ui_work_gets_the_design_skill(self):
        self.assertIn("/front:front-design", self.start("FEATURE", "src/App.tsx"))

    def test_skills_used_before_rank_first(self):
        skill(os.path.join(self.cc, "plugins", "cache", "m", "pony", "1.0"), "pony-debt", "Harvest simplify debt.")
        events = os.path.join(c.state_dir(), "events.jsonl")
        slug = json.loads(self.fm("state", "--json").stdout)["project"]
        with open(events, "a") as f:
            for _ in range(2):
                f.write(json.dumps({"kind": "tool", "tool": "Skill", "target": "pony:pony-debt", "project": slug,
                                    "ts": c.now()}) + "\n")
        out = self.start("CLEAN")
        self.assertLess(out.index("/pony:pony-debt"), out.index("/pony:pony-audit"))
