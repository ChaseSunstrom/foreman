"""T-1068: lanes claim the files and symbols they will change up front; an overlapping claim is refused naming the
holder and its task."""
import json
import os

from test_bus import Base

import fmcore as c

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

    def test_a_bare_drop_keeps_another_tasks_leases_in_the_same_session(self):
        # T-1216: builder lanes share the main session's id; a builder's bare drop released the main thread's leases
        self.fm("task", "new", "One", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus", env=A)
        self.fm("lease", "take", "a.py", env=A)
        self.fm("task", "new", "Two", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus", env=A)
        self.fm("lease", "take", "b.py", env=A)
        self.assertIn("Dropped 1 lease(s)", self.fm("lease", "drop", env=A).stdout)
        held = self.fm("lease", "list").stdout
        self.assertIn("a.py", held, "the first task's lease stays")
        self.assertNotIn("b.py", held)

    def test_dropping_a_file_releases_its_symbol_leases(self):
        self.fm("lease", "take", "a.py::f", "a.py::g", "c.py::h", env=A)
        self.assertIn("Dropped 2 lease(s)", self.fm("lease", "drop", "a.py", env=A).stdout)
        held = self.fm("lease", "list").stdout
        self.assertNotIn("a.py", held)
        self.assertIn("c.py::h", held)

    def test_drop_and_expiry_free_the_claim(self):
        self.fm("lease", "take", "a.py::f", env=A)
        self.fm("lease", "drop", "a.py::f", env=A)
        self.assertEqual(self.fm("lease", "take", "a.py::f", env=B).returncode, 0)
        self.fm("lease", "take", "c.py", "--minutes", "-1", env=A)
        self.assertEqual(self.fm("lease", "take", "c.py", env=B).returncode, 0, "expired")

    def test_a_bare_drop_releases_every_lease_this_session_holds(self):
        # T-1134: the brief says "fm lease drop when done"; five builders ran it bare and got only usage
        self.fm("lease", "take", "a.py::f", "b.py", env=A)
        self.fm("lease", "take", "c.py", env=B)
        r = self.fm("lease", "drop", env=A)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Dropped 2 lease(s)", r.stdout)  # T-1205: not just "No leases held."
        self.assertIn("Dropped 0 lease(s)", self.fm("lease", "drop", "z.py", env=A).stdout)
        held = self.fm("lease", "list").stdout
        self.assertNotIn("a.py", held)
        self.assertNotIn("b.py", held)
        self.assertIn("c.py", held, "another session's lease stays")

    def test_a_root_relative_path_from_a_subdirectory_is_leased_as_itself(self):
        # T-1148: from mods/ui, 'fm lease take mods/ui/x.tsx' was recorded doubled
        sub = os.path.join(self.repo, "mods", "ui")
        os.makedirs(sub)
        for f in (os.path.join(sub, "x.tsx"), os.path.join(sub, "y.tsx")):
            open(f, "w").close()
        self.fm("lease", "take", "mods/ui/x.tsx", cwd=sub, env=A)
        self.fm("lease", "take", "y.tsx", "new.tsx", cwd=sub, env=A)
        held = self.fm("lease", "list").stdout
        self.assertIn("mods/ui/x.tsx::*", held)
        self.assertNotIn("mods/ui/mods", held)
        self.assertIn("mods/ui/y.tsx::*", held, "cwd-relative as before")
        self.assertIn("mods/ui/new.tsx::*", held, "a new file keeps the cwd meaning")

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


class ClaimsReview(Base):
    def lane_task(self, scope):
        return self.task(title="Lane work", tier="S", focus=False, scope=scope)

    def test_a_brief_never_displaces_a_live_lease_and_says_so(self):
        path = os.path.join(self.repo, "a.py")
        with open(path, "w") as f:
            f.write("def f():\n    return 1\n")
        self.fm("lease", "take", "a.py", env=A)
        tid = self.lane_task(["a.py"])
        res = json.loads(self.fm("lane", "brief", tid, "--json").stdout)
        with open(res["path"]) as f:
            self.assertIn("a.py", f.read().split("## Claims")[1].split("## Your contract")[0])
        _, out = self.note("sess-a", "Edit", {"file_path": path, "old_string": "return 1", "new_string": "return 2"})
        self.assertNotEqual(out.get("permissionDecision"), "deny", "the holder keeps its lease")

    def test_warn_coexists_with_the_other_lease(self):
        path = os.path.join(self.repo, "a.py")
        with open(path, "w") as f:
            f.write("def f():\n    return 1\n")
        self.fm("lease", "take", "a.py::f", env=A)
        r = self.fm("lease", "take", "a.py::f", "--warn", env=B)
        self.assertIn("overlaps", r.stderr)
        self.assertEqual(r.stdout.count("overlaps"), 0, "warnings go to stderr")
        _, out = self.note("sess-a", "Edit", {"file_path": path, "old_string": "return 1", "new_string": "return 2"})
        self.assertNotEqual(out.get("permissionDecision"), "deny", "A's claim survived B's --warn")

    def test_release_frees_a_lane_claim_and_the_full_id_is_printed(self):
        import fmbus
        p = self.project()
        fmbus.preclaim(p, "T-1068", ["x.py"])
        r = self.fm("lease", "take", "x.py", env=B, check=False)
        self.assertIn("lane-T-1068", r.stderr + r.stdout)
        fmbus.release(p, "T-1068")
        self.assertEqual(self.fm("lease", "take", "x.py", env=B).returncode, 0)

    def test_no_lease_means_no_brief_load(self):
        import fmbus
        p = self.project()

        def boom(*a, **k):
            raise AssertionError("loaded briefs")
        real, c.load_briefs = c.load_briefs, boom
        try:
            self.assertIsNone(fmbus.conflict({"session_id": "s", "tool_name": "Edit", "tool_input": {}}, p,
                                             os.path.join(p.root, "free.py")))
        finally:
            c.load_briefs = real

    def test_json_refusal_is_structured_and_paths_are_normalised(self):
        self.fm("lease", "take", "new.py", env=A)
        r = self.fm("lease", "take", "./new.py::f", "--json", env=B, check=False)
        self.assertNotEqual(r.returncode, 0)
        refused = json.loads(r.stdout)["refused"]
        self.assertEqual(refused[0]["target"], "new.py::f")
        self.assertEqual(refused[0]["session"], "sess-a")
        self.assertIn("task", refused[0])
        r = self.fm("lease", "take", os.path.join(self.repo, "new.py"), env=B, check=False)
        self.assertNotEqual(r.returncode, 0, "an absolute path is the same file")

    def test_an_edits_lease_leaves_another_sessions_lease_intact(self):
        import fmbus
        p = self.project()
        path = os.path.join(self.repo, "a.py")
        with open(path, "w") as f:
            f.write("def f():\n    return 2\n")
        self.fm("lease", "take", "a.py::f", env=B)
        fmbus.after_edit({"session_id": "sess-a", "tool_name": "Write", "tool_input": {}}, p, path)
        held = {(v["session"], v["symbol"]) for v in fmbus._leases().values() if v["file"] == "a.py"}
        self.assertEqual(held, {("sess-b", "f"), ("sess-a", "*")})

    def test_a_lane_preclaim_never_denies_another_worktrees_edit(self):
        # T-1138: lane-T-1135's file-wide pre-claim of fmcli.py stalled T-1137's builder in its own worktree; lanes
        # edit separate checkouts and the merge settles overlaps, so a pre-claim is advisory (fm lease list shows it)
        import fmbus
        p = self.project()
        act = c.active_brief(c.load_briefs(p), p.lane)
        path = os.path.join(self.repo, "x.py")
        with open(path, "w") as f:
            f.write("x = 1\n")
        pl = {"session_id": "s", "tool_name": "Edit", "tool_input": {"old_string": "x = 1", "new_string": "x = 2"}}
        fmbus.preclaim(p, "T-9999", ["x.py"])
        self.assertIsNone(fmbus.conflict(pl, p, path), "another lane's pre-claim is advisory")
        self.assertIn("lane-T-9999", self.fm("lease", "list").stdout, "and still listed")
        fmbus.release(p, "T-9999")
        fmbus.preclaim(p, act.id, ["x.py"])
        self.assertIsNone(fmbus.conflict(pl, p, path), "the lane's own task edits its claim")
