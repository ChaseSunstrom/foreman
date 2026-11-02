"""T-2563 (gen-2 moonshot): anergy for permission prompts. PermissionRequest notes each prompt, PostToolUse with the
same id closes it, and the report names command classes a person approves by reflex (5+ prompts, median within 2 s
once the tool's own run time is taken out), never a class that writes, deletes or reaches out."""
import json
import os
from unittest import mock

from helpers import ForemanTestCase

import fmanergy as a


def ask(tid, cmd=None, tool="Bash"):
    return {"tool_use_id": tid, "tool_name": tool, "tool_input": {"command": cmd} if cmd else {"file_path": "/x"}}


class Anergy(ForemanTestCase):
    def prompt(self, tid, cmd, wait, ms=0, t0=1000.0):
        with mock.patch("time.time", return_value=t0):
            a.record("ask", ask(tid, cmd))
        with mock.patch("time.time", return_value=t0 + wait + ms / 1000):
            a.record("done", {"tool_use_id": tid, "duration_ms": ms})

    def test_reflex_read_class_is_named_with_its_rule(self):
        for i in range(5):
            self.prompt(f"g{i}", f"git status --short {i}", 0.8, ms=3000)  # a slow run is not the person's time
        r = a.report()
        self.assertEqual(r["prompts"], 5)
        self.assertEqual(r["timed"], 5)
        self.assertEqual([x[0] for x in r["reflex"]], ["Bash(git status *)"])
        self.assertEqual(r["reflex"][0][1], 5)
        self.assertLessEqual(r["reflex"][0][2], 2.0)

    def test_deliberated_or_too_few_is_not_reflex(self):
        for i in range(5):
            self.prompt(f"s{i}", "git log -3", 9.0)
        for i in range(4):
            self.prompt(f"d{i}", "git diff HEAD", 0.5)
        self.assertEqual(a.report()["reflex"], [])

    def test_destructive_class_is_never_named(self):
        for i in range(6):
            self.prompt(f"r{i}", f"rm -rf build{i}", 0.3)
        self.assertEqual(a.report()["reflex"], [])

    def test_a_class_with_one_writing_prompt_is_never_named(self):
        for i in range(5):
            self.prompt(f"c{i}", "git status", 0.3)
        self.prompt("w", "git status > out.txt", 0.3)
        self.assertEqual(a.report()["reflex"], [])

    def test_a_class_people_refuse_is_not_reflex(self):
        for i in range(5):
            self.prompt(f"k{i}", "git status", 0.3)
        a.record("ask", ask("open", "git status"))  # still open: allowed
        self.assertEqual(len(a.report()["reflex"]), 1)
        a.record("ask", ask("refused", "git status"))  # a second that never ran was refused
        self.assertEqual(a.report()["reflex"], [])

    def test_unpaired_prompt_counts_but_is_not_timed(self):
        a.record("ask", ask("lonely", "ls -la"))
        a.record("done", {"tool_use_id": "never-asked"})
        r = a.report()
        self.assertEqual((r["prompts"], r["timed"]), (1, 0))
        rows = [json.loads(x) for x in open(os.path.join(a.c.state_dir(), a.STORE))]
        self.assertEqual([x["ev"] for x in rows], ["ask"], "a call nobody was asked about writes nothing")

    def test_reading_tool_class_and_bad_input_never_raise(self):
        a.record("ask", ask("rd", tool="Read"))
        a.record("ask", {})
        a.record("ask", {"tool_use_id": "x", "tool_name": "Bash", "tool_input": None})
        self.assertEqual(a.klass("Read", {}), ("Read", True))
        self.assertEqual(a.klass("Write", {})[1], False)

    def test_store_is_capped(self):
        path = os.path.join(a.c.state_dir(), a.STORE)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.writelines(json.dumps({"id": f"i{n}", "ev": "ask", "at": n, "cls": "Read", "ro": True}) + "\n"
                         for n in range(a.CAP + 10))
        self.assertEqual(len(a.rows()), a.CAP // 2)
        self.assertLessEqual(sum(1 for _ in open(path)), a.CAP // 2)

    def test_hooks_record_the_pair(self):
        import fmhooks
        pl = {"tool_use_id": "h1", "tool_name": "Bash", "tool_input": {"command": "git status"}, "session_id": "s",
              "cwd": self.tmp if hasattr(self, "tmp") else os.getcwd()}
        fmhooks.permission_request(pl)
        fmhooks.post_tool_use(dict(pl, duration_ms=5))
        evs = [json.loads(x)["ev"] for x in open(os.path.join(a.c.state_dir(), a.STORE))]
        self.assertEqual(evs, ["ask", "done"])

    def test_doctor_row(self):
        import fmdoctor
        r = fmdoctor.check_anergy()
        self.assertEqual(r.status, "PASS")
        self.assertIn("none", r.detail)
        for i in range(5):
            self.prompt(f"q{i}", "git status", 0.4)
        r = fmdoctor.check_anergy()
        self.assertEqual(r.status, "PASS", "advisory: Foreman never applies the rule")
        self.assertIn("Bash(git status *)", r.detail)

    def test_digest_line(self):
        self.fm("init")
        self.assertNotIn("reflex", self.fm("digest").stdout)
        for i in range(5):
            self.prompt(f"q{i}", "git status", 0.4)
        self.assertIn("Approved by reflex", self.fm("digest").stdout)
