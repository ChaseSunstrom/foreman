"""fm tidy: seeded rot is found in a dry run; --apply archives without losing anything (§12 scenario 9)."""
import json
import os
import re

from helpers import ForemanTestCase, read_text

import fmcore as c


def age(p, tid, days, status=None):
    """Backdate a brief (and optionally set its status) directly — test setup only."""
    b = c.find_brief(p, tid)
    old = c.datetime.datetime.now(c.datetime.timezone.utc) - c.datetime.timedelta(days=days)
    b.meta["updated"] = b.meta["created"] = old.strftime("%Y-%m-%dT%H:%M:%SZ")
    if status:
        b.meta["status"] = status
    c.save_brief(p, b, touch=False)


class TidyCase(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fake_home = os.path.join(self.tmp, "home")
        os.makedirs(os.path.join(self.fake_home, ".claude"))
        self.fm("init")
        self.p = c.find_project(self.repo)
        encoded = re.sub(r"[^A-Za-z0-9]", "-", self.repo)
        self.mem = os.path.join(self.fake_home, ".claude", "projects", encoded, "memory")
        os.makedirs(self.mem)

    def tidy(self, *args):
        return json.loads(self.fm("tidy", "--json", *args, env={"HOME": self.fake_home}).stdout)

    def kinds(self, report):
        return {f["kind"] for f in report["findings"]}

    def seed_rot(self):
        with open(os.path.join(self.repo, "CLAUDE.md"), "w") as f:
            f.write("# app\n## Map\n- `src/api/` — handlers\n- `docs/missing-guide.md` — guide\n"
                    "## Commands\n- Test: `npm run test:unit`\n- Plan with `/foreman:intake`, graph with `/graphify`\n")
        with open(os.path.join(self.repo, "package.json"), "w") as f:
            json.dump({"scripts": {"test": "jest"}}, f)
        os.makedirs(os.path.join(self.repo, "src", "api"))
        with open(os.path.join(self.mem, "MEMORY.md"), "w") as f:
            f.write("- Use pnpm, not npm\n- Build with `make all`\n- Use pnpm, not npm\n- Config lives in `config/old.yaml`\n")
        self.fm("capture", "old idea nobody touched")
        age(self.p, "T-0001", 40)
        self.fm("task", "new", "a", "--type", "FIX", "--tier", "S", "--depends", "T-0003")
        self.fm("task", "new", "b", "--type", "FIX", "--tier", "S", "--depends", "T-0002")
        self.fm("task", "new", "old finished work", "--type", "CLEAN", "--tier", "S")
        age(self.p, "T-0004", 20, status="done")


class DryRun(TidyCase):
    def test_finds_all_seeded_rot_and_changes_nothing(self):
        self.seed_rot()
        before = sorted(os.listdir(os.path.join(self.p.dir, "tasks")))
        mem_before = read_text(os.path.join(self.mem, "MEMORY.md"))
        report = self.tidy()
        kinds = self.kinds(report)
        for k in ("dead_path", "stale_command", "memory_duplicate", "memory_dead_path", "inbox_stale", "cycle", "archive_task"):
            self.assertIn(k, kinds)
        dead = [f for f in report["findings"] if f["kind"] == "dead_path"]
        self.assertTrue(any("docs/missing-guide.md" in f["detail"] for f in dead))
        self.assertFalse(any("src/api" in f["detail"] for f in dead), "existing paths are not dead")
        self.assertFalse(any("/foreman:intake" in f["detail"] or "/graphify" in f["detail"] for f in dead),
                         "slash commands are not paths")
        self.assertEqual(sorted(os.listdir(os.path.join(self.p.dir, "tasks"))), before)
        self.assertEqual(read_text(os.path.join(self.mem, "MEMORY.md")), mem_before)
        self.assertFalse(report["applied"])

    def test_reports_doc_drift_in_project_docs(self):
        os.makedirs(os.path.join(self.repo, "src"))
        with open(os.path.join(self.repo, "README.md"), "w") as f:
            f.write("Entry point: `src/gone.py`\n")
        drift = [f for f in self.tidy()["findings"] if f["kind"] == "docs_drift"]
        self.assertEqual(len(drift), 1)
        self.assertIn("src/gone.py", drift[0]["detail"])

    def test_clean_project_has_no_findings_that_need_action(self):
        report = self.tidy()
        self.assertFalse([f for f in report["findings"] if f["severity"] != "info"])


class Apply(TidyCase):
    def test_apply_archives_and_loses_nothing(self):
        self.seed_rot()
        done_text = read_text(c.find_brief(self.p, "T-0004").path)
        report = self.tidy("--apply")
        self.assertTrue(report["applied"])
        self.assertIsNone(c.find_brief(self.p, "T-0004"), "archived out of tasks/")
        archived = [os.path.join(d, f) for d, _, fs in os.walk(os.path.join(self.p.dir, "archive")) for f in fs
                    if f.startswith("T-0004")]
        self.assertEqual(len(archived), 1)
        self.assertEqual(read_text(archived[0]), done_text)
        self.assertIsNotNone(c.find_brief(self.p, "T-0001"), "user requests are never auto-deleted")
        self.assertEqual(read_text(os.path.join(self.mem, "MEMORY.md")).count("Use pnpm, not npm"), 1)
        backups = [f for f in os.listdir(os.path.join(self.p.dir, "archive")) if f.startswith("memory-")]
        self.assertTrue(backups, "memory archived before dedupe")
        self.assertIsNotNone(c.read_meta(self.p)["last_tidy"])
        self.assertIn("tidy", [e["event"] for e in c.ledger_tail(self.p)])
        again = self.kinds(self.tidy())
        self.assertNotIn("archive_task", again)
        self.assertNotIn("memory_duplicate", again)
        self.assertIn("cycle", again, "judgment calls stay reported")

    def test_rotates_large_event_log(self):
        events = os.path.join(self.home, "state", "events.jsonl")
        with open(events, "w") as f:
            f.write((json.dumps({"ts": c.now(), "kind": "tool", "target": "x" * 200}) + "\n") * 30000)
        self.assertIn("rotate_events", self.kinds(self.tidy()))
        self.tidy("--apply")
        self.assertLess(os.path.getsize(events), 1024)
        rotated = [f for f in os.listdir(os.path.join(self.home, "state", "logs")) if f.startswith("events-")]
        self.assertEqual(len(rotated), 1)

    def test_rolls_large_ledger_by_month(self):
        ledger = os.path.join(self.p.dir, "ledger.jsonl")
        old = {"ts": "2026-01-15T00:00:00Z", "session_id": None, "project": self.p.slug, "task": None,
               "event": "note", "data": {"pad": "y" * 300}}
        with open(ledger, "a") as f:
            f.write((json.dumps(old) + "\n") * 4000)
        self.assertIn("roll_ledger", self.kinds(self.tidy()))
        self.tidy("--apply")
        monthly = read_text(os.path.join(self.p.dir, "archive", "ledger-2026-01.jsonl"))
        self.assertEqual(len(monthly.splitlines()), 4000)
        kept = [json.loads(l) for l in read_text(ledger).splitlines()]
        self.assertTrue(all(not e["ts"].startswith("2026-01") for e in kept if e["event"] != "ledger_rolled"))
        self.assertIn("ledger_rolled", [e["event"] for e in kept])

    def test_all_covers_every_registered_project(self):
        other = os.path.join(self.tmp, "other")
        os.makedirs(other)
        self.fm("init", other)
        self.assertEqual(len(self.tidy("--all")["projects"]), 2)
