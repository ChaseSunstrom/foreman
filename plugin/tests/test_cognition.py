"""T-0685 (Intelligence — cognitive architecture): memory by activation, lesion reports, and a dream pass over the day's
failures."""
import json
import os

from helpers import ForemanTestCase

import fmcore as c


class Base(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def done(self, title, *files):
        tid = json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", "S", "--ac", "ok :: true",
                                 "--step", "s", "--json").stdout)["id"]
        with c.lock(self.p.dir):
            b = c.find_brief(self.p, tid)
            b.meta["status"] = "done"
            b.set_section("Files touched", "\n".join(f"- {f}" for f in files))
            c.save_brief(self.p, b)
        return tid


class Activation(Base):
    def test_a_past_task_on_the_files_being_touched_now_ranks_first(self):
        a = self.done("Fix the export timeout on slow disks", "export/csv.py")
        b = self.done("Fix the export timeout on slow links", "net/upload.py")
        self.fm("task", "new", "Export hangs again", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        c.log_event(self.p, "touched", task="T-0003", data={"file": os.path.join(self.repo, "net/upload.py")})
        hits = json.loads(self.fm("recall", "export timeout slow", "--json").stdout)
        ids = [h["label"].split()[0] for h in hits]
        self.assertLess(ids.index(b), ids.index(a), ids)


class Lesions(Base):
    def test_ablations_are_reported_with_the_next_lesion_to_run(self):
        c.log_event(self.p, "evolve", data={"kept": True, "target": "plugin/skills/tidy/SKILL.md",
                                             "why": "ablation: the file emptied", "branch": "evolve/1"})
        c.log_event(self.p, "evolve", data={"kept": False, "target": "plugin/skills/next/SKILL.md",
                                             "why": "ablation: the file emptied", "branch": "evolve/2"})
        out = self.fm("usage", "--lesions").stdout
        self.assertRegex(out, r"tidy/SKILL\.md.*held without it")
        self.assertRegex(out, r"next/SKILL\.md.*earns its place")


class Dream(Base):
    def test_repeated_failures_become_tripwire_candidates_with_their_counterfactual(self):
        path = os.path.join(self.p.dir, "failures.jsonl")
        with open(path, "w") as f:
            for _ in range(3):
                f.write(json.dumps({"sig": "ModuleNotFoundError: No module named 'yaml'", "task": "T-0001",
                                    "at": c.now()}) + "\n")
            f.write(json.dumps({"sig": "AssertionError: 3 != 4", "task": "T-0001", "at": c.now()}) + "\n")
        out = self.fm("dream").stdout
        self.assertIn("No module named 'yaml'", out)
        self.assertIn("would have caught 2", out)
        self.assertNotIn("3 != 4", out, "a one-off isn't a pattern")
        self.assertTrue([n for n in os.listdir(os.path.join(self.p.dir, "research")) if n.startswith("dream-")])
        self.assertIn("dream", self.fm("night", "--dry-run").stdout)
