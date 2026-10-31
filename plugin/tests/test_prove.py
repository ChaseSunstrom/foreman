#!/usr/bin/env python3
# T-2288: fm prove --migration: up, down, up again on a throwaway sqlite file, schema compared each time
import json
import os

from helpers import ForemanTestCase

import fmprove

M = "migrations/"
GOOD = {M + "001_users.up.sql": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);",
        M + "001_users.down.sql": "DROP TABLE users;",
        M + "002_idx.up.sql": "CREATE TABLE logs (users_name TEXT);",
        M + "002_idx.down.sql": "DROP TABLE logs;"}


def write(root, files):
    for rel, text in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(text)


class Migration(ForemanTestCase):
    def proj(self, files, name="proj"):
        root = os.path.join(self.tmp, name)
        write(root, files)
        return root

    def test_a_reversible_pair_passes_with_the_schema_before_and_after(self):
        r = fmprove.migration(self.proj(GOOD), True)
        self.assertEqual(r["verdict"], "pass", r)
        self.assertEqual(r["tool"], "sql")
        self.assertEqual(r["before"], [])
        self.assertEqual(r["after_up"], r["after_up2"])
        self.assertIn("CREATE TABLE users", "".join(r["after_up"]))

    def test_a_down_that_leaves_something_behind_fails_and_says_what(self):
        files = dict(GOOD, **{M + "002_idx.down.sql": "SELECT 1;"})
        r = fmprove.migration(self.proj(files), True)
        self.assertEqual(r["verdict"], "fail")
        self.assertIn("down", r["why"])
        self.assertIn("logs", r["why"])

    def test_a_missing_down_and_a_broken_up_fail(self):
        r = fmprove.migration(self.proj({M + "001_a.up.sql": "CREATE TABLE a (x);"}), True)
        self.assertEqual(r["verdict"], "fail")
        self.assertIn("001_a", r["why"])
        r = fmprove.migration(self.proj({M + "001_a.up.sql": "CREAT TABLE a;", M + "001_a.down.sql": "SELECT 1;"}, "p2"), True)
        self.assertEqual(r["verdict"], "fail")
        self.assertIn("up", r["why"])

    def test_untrusted_unknown_and_unsupported_tools_run_nothing(self):
        r = fmprove.migration(self.proj(GOOD), False)
        self.assertEqual(r["verdict"], "refused")
        self.assertIn("--yes-run", r["why"])
        r = fmprove.migration(self.proj({"app.py": "x = 1"}, "p3"), True)
        self.assertEqual(r["verdict"], "unknown")
        r = fmprove.migration(self.proj({"alembic.ini": "[alembic]"}, "p4"), True)
        self.assertEqual(r["verdict"], "unknown")
        self.assertIn("alembic", r["why"])

    def test_sql_cannot_reach_a_file_outside_the_throwaway_database(self):
        victim = os.path.join(self.tmp, "real.db")
        files = {M + "001_a.up.sql": f"ATTACH DATABASE '{victim}' AS x; CREATE TABLE x.t (a);",
                 M + "001_a.down.sql": "SELECT 1;"}
        r = fmprove.migration(self.proj(files), True)
        self.assertEqual(r["verdict"], "fail")
        self.assertFalse(os.path.exists(victim))

    def test_a_runaway_migration_is_cut_off(self):
        loop = "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i+1 FROM n) SELECT count(*) FROM n;"
        r = fmprove.migration(self.proj({M + "001_a.up.sql": loop, M + "001_a.down.sql": "SELECT 1;"}), True, limit=1)
        self.assertEqual(r["verdict"], "fail")
        self.assertIn("time", r["why"])

    def test_the_command_refuses_an_untrusted_tree_and_passes_a_trusted_one(self):
        root = self.proj(GOOD)
        r = self.fm("prove", "--migration", root, check=False)
        self.assertEqual(r.returncode, 2, r.stderr)
        r = self.fm("prove", "--migration", root, "--yes-run", "--json", check=False)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["verdict"], "pass")


if __name__ == "__main__":
    import unittest
    unittest.main()
