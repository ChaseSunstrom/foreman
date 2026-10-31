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


def cli(mark):
    """A stub CLI whose --help lists --out and build; --ghost appears only in this comment (a grep finds it, --help
    doesn't). Running it leaves the marker file."""
    return ("#!/usr/bin/env python3\nimport argparse\n# --ghost\n"
            f"open({mark!r}, 'w').close()\n"
            "p = argparse.ArgumentParser(prog='mycli')\ns = p.add_subparsers(dest='cmd', required=True)\n"
            "s.add_parser('build').add_argument('--out')\ns.add_parser('clean')\np.parse_args()\n")


class DocsProof(ForemanTestCase):
    """T-2381: fm prove --docs: the docs' flags, subcommands, paths and fenced commands against the code."""

    def tree(self, readme, mark=None):
        self.mark = mark or os.path.join(self.tmp, "ran")
        write(self.repo, {"bin/mycli": cli(self.mark), "README.md": readme})
        os.chmod(os.path.join(self.repo, "bin", "mycli"), 0o755)
        return self.repo

    def prove(self, *args):
        r = self.fm("prove", "--docs", "--json", *args, check=False)
        return r.returncode, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else r.stdout)

    def by(self, out):
        return {(c["kind"], c["detail"]): c["verdict"] for c in out["claims"]}

    def test_docs_proof_a_flag_or_subcommand_no_file_has_fails_in_any_tree(self):
        self.tree("Use `mycli build --out x`, `mycli build --gone` and `mycli frobnicate`.\n"
                  "See `src/missing.py` and `src/mycli.py`.\n")
        write(self.repo, {"src/mycli.py": "x = 1\n"})
        code, out = self.prove()
        got = self.by(out)
        self.assertEqual(code, 1, out)
        self.assertEqual(got[("flag", "--gone")], "failed")
        self.assertEqual(got[("subcommand", "mycli frobnicate")], "failed")
        self.assertEqual(got[("path", "src/missing.py")], "failed")
        self.assertEqual(got[("flag", "--out")], "proven")
        self.assertEqual(got[("subcommand", "mycli build")], "proven")
        self.assertEqual(got[("path", "src/mycli.py")], "proven")
        self.assertFalse(os.path.exists(self.mark), "an untrusted tree's command ran")

    def test_docs_proof_a_correct_readme_passes_and_a_fenced_command_waits_for_trust(self):
        self.tree("Build:\n\n```\n$ mycli build --out dist\n```\n")
        code, out = self.prove()
        self.assertEqual(code, 0, out)
        got = self.by(out)
        self.assertEqual(got[("command", "mycli build --out dist")], "unproven")
        self.assertEqual(got[("flag", "--out")], "proven")
        self.assertFalse(os.path.exists(self.mark))

    def test_docs_proof_prose_and_other_tools_give_nothing_to_check(self):
        self.tree("Some prose about the app. Run `git status`; pass `--force` to git.\n")
        code, out = self.prove()
        self.assertEqual((code, out["claims"]), (2, []), out)

    def test_docs_proof_a_trusted_tree_runs_fenced_commands_and_checks_help(self):
        self.tree("```\nmycli build --out dist\nmycli clean\nmycli build --ghost\nmycli clean --out x\n```\n")
        code, out = self.prove("--yes-run")
        got = self.by(out)
        self.assertEqual(code, 1, out)
        self.assertEqual(got[("command", "mycli build --out dist")], "proven")
        self.assertEqual(got[("command", "mycli clean")], "proven")
        self.assertEqual(got[("command", "mycli build --ghost")], "failed")
        self.assertEqual(got[("flag", "--ghost")], "failed")  # in the code, not in `mycli build --help`
        self.assertEqual(got[("command", "mycli clean --out x")], "failed")
        self.assertTrue(os.path.exists(self.mark), "the trusted run never ran the command")
        code, again = self.prove()  # the yes was kept for the tree
        self.assertEqual(self.by(again)[("command", "mycli build --out dist")], "proven")

    def test_docs_proof_files_limit_what_is_read_and_shell_syntax_is_not_run(self):
        self.tree("`mycli build --gone`\n")
        write(self.repo, {"docs/ok.md": "```\nmycli build | tee log\nmycli build <dir>\n```\n"})
        code, out = self.prove("--yes-run", "docs/ok.md")
        self.assertEqual(code, 0, out)  # README's lie is not in the named file
        self.assertFalse(os.path.exists(self.mark))  # a pipe and a placeholder are never run
        self.assertNotIn(("flag", "--gone"), self.by(out))
        self.assertEqual({v for (k, _), v in self.by(out).items() if k == "command"}, {"unproven"})
        self.assertEqual(self.fm("prove", "--docs", "../nope.md", check=False).returncode, 2)


if __name__ == "__main__":
    import unittest
    unittest.main()
