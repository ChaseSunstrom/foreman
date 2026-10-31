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


def cli(mark, say=""):
    """A stub CLI whose --help lists --out and build; --ghost appears only in this comment (a grep finds it, --help
    doesn't). Running it leaves the marker file, and prints say after a successful parse."""
    return ("#!/usr/bin/env python3\nimport argparse\n# --ghost\n"
            f"open({mark!r}, 'w').close()\n"
            "p = argparse.ArgumentParser(prog='mycli')\ns = p.add_subparsers(dest='cmd', required=True)\n"
            "s.add_parser('build').add_argument('--out')\ns.add_parser('clean')\np.parse_args()\n"
            + (f"print({say!r})\n" if say else ""))


class DocsProof(ForemanTestCase):
    """T-2381: fm prove --docs: the docs' flags, subcommands, paths and fenced commands against the code."""

    def tree(self, readme, mark=None, say=""):
        self.mark = mark or os.path.join(self.tmp, "ran")
        write(self.repo, {"bin/mycli": cli(self.mark, say), "README.md": readme})
        os.chmod(os.path.join(self.repo, "bin", "mycli"), 0o755)
        return self.repo

    def prove(self, *args):
        r = self.fm("prove", "--docs", "--json", *args, check=False)
        return r.returncode, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else r.stdout)

    def by(self, out):
        return {(c["kind"], c["detail"]): c["verdict"] for c in out["claims"]}

    def test_docs_proof_static_a_flag_or_subcommand_no_file_has_fails_and_text_in_a_file_is_unproven(self):
        self.tree("Use `mycli build --out x`, `mycli build --gone` and `mycli frobnicate`.\n"
                  "See `src/missing.py` and `src/mycli.py`.\n")
        write(self.repo, {"src/mycli.py": "x = 1\n"})
        code, out = self.prove()
        got = self.by(out)
        self.assertEqual(code, 1, out)
        self.assertEqual(got[("flag", "--gone")], "failed")
        self.assertEqual(got[("subcommand", "mycli frobnicate")], "failed")
        self.assertEqual(got[("path", "src/missing.py")], "failed")
        self.assertEqual(got[("flag", "--out")], "unproven")  # text in a file is not a working flag
        self.assertEqual(got[("subcommand", "mycli build")], "unproven")
        self.assertIn("text in a file", next(c for c in out["claims"] if c["detail"] == "--out")["why"])
        self.assertEqual(got[("path", "src/mycli.py")], "proven")
        self.assertFalse(os.path.exists(self.mark), "an untrusted tree's command ran")

    def test_docs_proof_static_text_in_a_file_alone_is_not_a_pass(self):
        self.tree("Build:\n\n```\n$ mycli build --out dist\n```\n")
        code, out = self.prove()
        self.assertEqual(code, 2, out)  # nothing failed, but nothing was proven either
        got = self.by(out)
        self.assertEqual(got[("command", "mycli build --out dist")], "unproven")
        self.assertEqual(got[("flag", "--out")], "unproven")
        self.assertFalse(os.path.exists(self.mark))

    def test_docs_proof_static_a_lone_positional_may_be_an_argument_not_a_subcommand(self):
        self.tree("Run `mycli frobnicate`.\n")
        code, out = self.prove()
        self.assertEqual((code, self.by(out)[("subcommand", "mycli frobnicate")]), (2, "unproven"))  # one word: maybe a file name
        self.tree("Run `mycli frobnicate` or `mycli other`.\n")
        self.assertEqual(self.by(self.prove()[1])[("subcommand", "mycli frobnicate")], "failed")

    def test_docs_proof_static_words_after_a_double_dash_are_another_tools(self):
        self.tree("Run `mycli run -- pytest --maxfail=1`.\n")
        got = self.by(self.prove()[1])
        self.assertNotIn(("flag", "--maxfail"), got)

    def test_docs_proof_static_a_flag_from_a_parameter_name_is_in_the_code(self):
        write(self.repo, {"pyproject.toml": "[project.scripts]\napp = 'pkg.cli:main'\n",
                          "pkg/cli.py": "def main(\n    name: str,\n    verbose: bool = False,\n):\n    pass\n",
                          "README.md": "Run `app --verbose` or `app --nope`.\n"})
        code, out = self.prove()
        got = self.by(out)
        self.assertEqual(got[("flag", "--verbose")], "unproven")  # Typer/Fire derive --verbose from the parameter
        self.assertEqual(got[("flag", "--nope")], "failed")

    def test_docs_proof_static_a_bin_shim_that_runs_another_tool_is_not_the_repos_cli(self):
        write(self.repo, {"bin/rails": "#!/usr/bin/env ruby\nAPP_PATH = File.expand_path('../config/application', __dir__)\n"
                                       "require_relative '../config/boot'\nrequire 'rails/commands'\n",
                          "README.md": "Run `rails server --fancy` and `rails about`.\n"})
        os.chmod(os.path.join(self.repo, "bin", "rails"), 0o755)
        code, out = self.prove()
        got = self.by(out)
        self.assertEqual(got.get(("flag", "--fancy"), "unproven"), "unproven")
        self.assertNotIn("failed", got.values())

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
        self.assertEqual(got[("flag", "--out")], "failed")  # a later failure sticks: `mycli clean --help` lacks it
        self.assertTrue(os.path.exists(self.mark), "the trusted run never ran the command")
        code, again = self.prove()  # the yes was kept for the tree
        self.assertEqual(self.by(again)[("command", "mycli build --out dist")], "proven")

    def test_docs_proof_a_run_that_exits_0_with_the_flag_in_help_proves_the_flag_and_subcommand(self):
        self.tree("```\nmycli build --out dist\n```\n")
        code, out = self.prove("--yes-run")
        got = self.by(out)
        self.assertEqual(code, 0, out)
        self.assertEqual((got[("flag", "--out")], got[("subcommand", "mycli build")]), ("proven", "proven"))

    def test_docs_proof_files_limit_what_is_read_and_shell_syntax_is_not_run(self):
        self.tree("`mycli build --gone`\n")
        write(self.repo, {"docs/ok.md": "```\nmycli build | tee log\nmycli build <dir>\nmycli build /etc/passwd\n"
                                        "mycli build ~/x\n```\n"})
        code, out = self.prove("--yes-run", "docs/ok.md")
        self.assertEqual(code, 2, out)  # README's lie is not in the named file; nothing here is run or proven
        self.assertFalse(os.path.exists(self.mark))  # a pipe, a placeholder, an absolute path and ~ are never run
        self.assertNotIn(("flag", "--gone"), self.by(out))
        self.assertEqual({v for (k, _), v in self.by(out).items() if k == "command"}, {"unproven"})
        self.assertEqual(self.fm("prove", "--docs", "../nope.md", check=False).returncode, 2)

    def test_docs_proof_a_folder_then_files_resolve_against_the_folder_without_a_folder_error(self):
        self.tree("`mycli build --gone`\n")
        write(self.repo, {"docs/ok.md": "`mycli build --gone2`\n"})
        r = self.fm("prove", "--docs", "--json", self.repo, "docs/ok.md", check=False, cwd=self.tmp)
        self.assertNotIn("folder", r.stderr)
        got = self.by(json.loads(r.stdout))
        self.assertEqual(got[("flag", "--gone2")], "failed")
        self.assertNotIn(("flag", "--gone"), got)

    def test_docs_proof_yes_run_from_a_subfolder_trusts_that_folder_not_the_whole_repo(self):
        self.tree("`mycli build`\n")
        sub = os.path.join(self.repo, "sub")
        write(self.repo, {"sub/README.md": "`mycli build`\n"})
        self.fm("prove", "--docs", "--yes-run", check=False, cwd=sub)
        self.assertTrue(fmprove.trusted(sub))
        self.assertFalse(fmprove.trusted(self.repo))

    def test_docs_proof_output_shown_in_the_block_must_be_in_the_run(self):
        self.tree("```\n$ mycli build --out dist\nbuilt dist\n```\n", say="built dist")
        code, out = self.prove("--yes-run")
        got = self.by(out)
        self.assertEqual((code, got[("command", "mycli build --out dist")], got[("flag", "--out")]), (0, "proven", "proven"), out)

    def test_docs_proof_output_that_differs_fails_the_command_and_proves_nothing_it_used(self):
        self.tree("```\n$ mycli build --out dist\nbuilt dist\n```\n", say="removed everything")
        code, out = self.prove("--yes-run")
        got = self.by(out)
        self.assertEqual(code, 1, out)  # exits 0, but does something other than the docs show
        self.assertEqual(got[("command", "mycli build --out dist")], "failed")
        self.assertIn("built dist", next(c for c in out["claims"] if c["kind"] == "command")["why"])
        self.assertEqual((got[("flag", "--out")], got[("subcommand", "mycli build")]), ("unproven", "unproven"))

    def test_docs_proof_output_compares_whitespace_normalised_lines_and_ignores_ansi_codes(self):
        self.tree("```\n$ mycli build\n  built    dist  \n```\n", say="\x1b[32mbuilt\x1b[0m\tdist\nextra line")
        self.assertEqual(self.by(self.prove("--yes-run")[1])[("command", "mycli build")], "proven")

    def test_docs_proof_output_ignores_elisions_and_a_command_without_shown_output_is_unchanged(self):
        self.tree("```\n$ mycli build\nbuilt dist\n...\n```\n\n```\nmycli clean\nmycli build --out x\n```\n", say="built dist")
        got = self.by(self.prove("--yes-run")[1])
        self.assertEqual(got[("command", "mycli build")], "proven")
        self.assertEqual(got[("command", "mycli clean")], "proven")  # the next command is not its output
        self.assertEqual(got[("command", "mycli build --out x")], "proven")

    def test_docs_proof_output_block_right_after_the_command_block_is_matched(self):
        self.tree("```\nmycli build\n```\n\nprints:\n\n```\nbuilt dist\n```\n", say="built dist")
        self.assertEqual(self.by(self.prove("--yes-run")[1])[("command", "mycli build")], "proven")
        self.tree("```\nmycli build\n```\n\nprints:\n\n```\nbuilt dist\n```\n", say="gone")
        self.assertEqual(self.by(self.prove("--yes-run")[1])[("command", "mycli build")], "failed")

    def test_docs_proof_output_is_never_compared_in_an_untrusted_tree(self):
        self.tree("```\n$ mycli build\nbuilt dist\n```\n", say="gone")
        code, out = self.prove()
        self.assertEqual((code, self.by(out)[("command", "mycli build")]), (2, "unproven"))
        self.assertFalse(os.path.exists(self.mark))


if __name__ == "__main__":
    import unittest
    unittest.main()
