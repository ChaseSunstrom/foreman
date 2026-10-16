"""T-1068: lanes claim the files and symbols they will change up front; an overlapping claim is refused naming the
holder and its task."""
import json
import os

from test_bus import Base

A = {"CLAUDE_CODE_SESSION_ID": "sess-a"}
B = {"CLAUDE_CODE_SESSION_ID": "sess-b"}


class Claims(Base):
    def test_a_second_claim_on_the_same_symbol_fails_naming_the_holder(self):
        first = self.fm("lease", "take", "a.py::f", env=A)
        self.assertEqual(first.returncode, 0, first.stderr)
        r = self.fm("lease", "take", "a.py::f", env=B, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("sess-a", r.stderr + r.stdout)
        self.assertIn("T-", r.stderr + r.stdout, "names its task")
        self.assertEqual(self.fm("lease", "take", "a.py::g", env=B).returncode, 0, "another symbol is free")

    def test_a_file_wide_claim_overlaps_any_symbol_and_warn_takes_it(self):
        self.fm("lease", "take", "a.py", env=A)
        r = self.fm("lease", "take", "a.py::f", "b.py::h", env=B, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("b.py", self.fm("lease", "list").stdout, "a refused claim takes none of its targets")
        r = self.fm("lease", "take", "a.py::f", "--warn", env=B)
        self.assertIn("overlaps", r.stdout + r.stderr)
        self.assertIn("a.py::f", self.fm("lease", "list").stdout)

    def test_drop_and_expiry_free_the_claim(self):
        self.fm("lease", "take", "a.py::f", env=A)
        self.fm("lease", "drop", "a.py::f", env=A)
        self.assertEqual(self.fm("lease", "take", "a.py::f", env=B).returncode, 0)
        self.fm("lease", "take", "c.py", "--minutes", "-1", env=A)
        self.assertEqual(self.fm("lease", "take", "c.py", env=B).returncode, 0, "expired")

    def test_a_lane_brief_preclaims_its_concrete_scope_and_names_the_command(self):
        tid = self.task(title="Lane work", tier="S", focus=False, scope=["x.py", "lib/*.py"])
        path = json.loads(self.fm("lane", "brief", tid, "--json").stdout)["path"]
        with open(path) as f:
            self.assertIn("fm lease take", f.read())
        out = self.fm("lease", "list").stdout
        self.assertIn("x.py::*", out)
        self.assertIn(tid, out)
        self.assertNotIn("lib/*.py", out, "a glob isn't claimed")
        r = self.fm("lease", "take", "x.py::f", env=B, check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(tid, r.stderr + r.stdout)
