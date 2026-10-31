#!/usr/bin/env python3
# T-2288: fm prove --migration: up, down, up again on a throwaway sqlite file, schema compared each time
import json
import os
import tempfile

from helpers import ForemanTestCase

import fmprove
import fminfra as fmprove_infra

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


class InfraProof(ForemanTestCase):
    """T-2385: fm prove --infra: each class's own validator on a throwaway copy; stubs on PATH stand in for the tools.
    A stub keeps to shell builtins (the PATH here holds only the stubs); it fails a file whose first line says BAD."""
    LIVE = ("apply", "plan", "destroy", "init", "install", "upgrade", "push", "pull", "run", "up", "deploy")

    def setUp(self):
        super().setUp()
        import fmcore as c
        from unittest import mock
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.bin, self.log = os.path.join(self.tmp, "bin"), os.path.join(self.tmp, "calls.log")
        os.makedirs(self.bin)
        self.tree = os.path.join(self.tmp, "tree")
        write(self.tree, {"Dockerfile": "FROM scratch\n", "Dockerfile.bad": "FROM BAD\n",
                          ".github/workflows/ci.yml": "on: push\n", "notes.txt": "x"})
        self.stub("hadolint")
        patch = mock.patch.dict(os.environ, {"PATH": self.bin, "GITHUB_TOKEN": "t0ps3cret"})
        patch.start()
        self.addCleanup(patch.stop)
        os.environ.pop("KUBECONFORM_SCHEMAS", None)  # restored by the patch's cleanup

    def stub(self, name, bin_dir=None):
        path = os.path.join(bin_dir or self.bin, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(f'#!/bin/sh\necho "{name} $* pwd=$PWD home=$HOME tok=$GITHUB_TOKEN" >> {self.log}\n'
                    'for last; do :; done\nIFS= read -r l < "$last" 2>/dev/null\n'
                    f'case "$l" in *BAD*) echo "{name}: DL3000 it is bad"; exit 1;; esac\nexit 0\n')
        os.chmod(path, 0o755)

    def calls(self):
        try:
            with open(self.log) as f:
                return f.read().splitlines()
        except OSError:
            return []

    def by_file(self, r):
        return {x["file"]: x for x in r["files"]}

    def test_infra_proof_one_passes_one_fails_one_is_unproven(self):
        r = fmprove_infra.infra(self.tree, allowed=False, p=self.p)
        got = self.by_file(r)
        self.assertEqual(got["Dockerfile"]["verdict"], "pass")
        self.assertEqual(got["Dockerfile.bad"]["verdict"], "fail")
        self.assertIn("DL3000", got["Dockerfile.bad"]["why"])
        self.assertEqual(got[".github/workflows/ci.yml"]["verdict"], "unproven")
        self.assertIn("actionlint", got[".github/workflows/ci.yml"]["why"])
        self.assertNotIn("notes.txt", got)
        self.assertEqual(r["verdict"], "fail")

    def test_infra_proof_runs_on_a_copy_with_a_scrubbed_environment(self):
        mine = lambda: {d for d in os.listdir(tempfile.gettempdir()) if d.startswith("fm-prove-")}  # noqa: E731
        before = mine()
        fmprove_infra.infra(self.tree, allowed=False)
        calls = self.calls()
        self.assertEqual(len(calls), 2, calls)
        for call in calls:
            self.assertIn("pwd=" + os.path.join(tempfile.gettempdir(), "fm-prove-"), call)
            self.assertNotIn(os.path.realpath(self.tree), call)
            self.assertIn("tok=", call)
            self.assertNotIn("t0ps3cret", call)
            self.assertNotIn("home=" + os.environ.get("HOME", "/nonexistent") + " ", call)
        self.assertEqual(mine() - before, set())  # the copy is gone

    def test_infra_proof_exit_codes_and_what_is_said(self):
        env = {"PATH": self.bin}
        r = self.fm("prove", "--infra", self.tree, check=False, env=env)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("unproven", r.stdout)
        self.assertIn("actionlint", r.stdout)
        os.remove(os.path.join(self.tree, "Dockerfile.bad"))
        self.assertEqual(self.fm("prove", "--infra", self.tree, check=False, env=env).returncode, 0)
        os.remove(os.path.join(self.tree, "Dockerfile"))  # only an unproven file is left: nothing was checked
        self.assertEqual(self.fm("prove", "--infra", self.tree, check=False, env=env).returncode, 2)
        os.remove(os.path.join(self.tree, ".github/workflows/ci.yml"))
        r = self.fm("prove", "--infra", self.tree, "--json", check=False, env=env)
        self.assertEqual((r.returncode, json.loads(r.stdout)["files"]), (2, []))

    def test_infra_proof_a_missing_tool_is_filed_once_for_the_capability_miss_path(self):
        import fmcore as c
        for _ in range(2):
            fmprove_infra.infra(self.tree, allowed=False, p=self.p)
        mine = [b for b in c.load_briefs(self.p, include_archive=True) if "capability-miss: actionlint" in b.section("Raw request")]
        self.assertEqual(len(mine), 1)

    def test_infra_proof_never_runs_a_live_verb_and_the_table_holds_none(self):
        write(self.tree, {"compose.yaml": "services: {}\n", "main.tf": "x", ".terraform/p": "x", "run.sh": "echo\n",
                          "app.service": "[Unit]\n", "k8s/a.yaml": "kind: Pod\n", "chart/Chart.yaml": "name: c\n"})
        for n in ("docker", "terraform", "shellcheck", "systemd-analyze", "helm", "kubeconform"):
            self.stub(n)
        fmprove_infra.infra(self.tree, allowed=True)
        for call in self.calls():
            self.assertFalse(set(call.split(" pwd=")[0].split()[1:]) & set(self.LIVE), call)
        for k in fmprove_infra.CLASSES.values():
            self.assertFalse(set(k["argv"]) & set(self.LIVE), k["argv"])

    def test_infra_proof_terraform_needs_an_initialised_folder_and_a_trusted_tree(self):
        self.stub("terraform")
        write(self.tree, {"main.tf": "resource {}\n"})
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=True))
        self.assertEqual(got["main.tf"]["verdict"], "unproven")
        self.assertIn("init", got["main.tf"]["why"])
        write(self.tree, {".terraform/providers/x": "plugin"})
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(got["main.tf"]["verdict"], "unproven")
        self.assertIn("--yes-run", got["main.tf"]["why"])
        self.assertFalse([x for x in self.calls() if x.startswith("terraform")])
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=True))
        self.assertEqual(got["main.tf"]["verdict"], "pass")
        (call,) = [x for x in self.calls() if x.startswith("terraform")]
        self.assertIn("validate", call)

    def test_infra_proof_a_helm_chart_is_linted_once_and_kubeconform_needs_local_schemas(self):
        write(self.tree, {"chart/Chart.yaml": "name: c\n", "chart/values.yaml": "a: 1\n", "chart/templates/x.tpl": "x",
                          "values.yaml": "orphan: 1\n", "k8s/pod.yaml": "kind: Pod\n"})
        self.stub("helm")
        self.stub("kubeconform")
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(len([x for x in self.calls() if x.startswith("helm")]), 1, self.calls())
        self.assertEqual(got["chart/Chart.yaml"]["verdict"], "pass")
        self.assertNotIn("values.yaml", got)  # no chart above it: helm lint has nothing to lint
        self.assertEqual(got["k8s/pod.yaml"]["verdict"], "unproven")
        self.assertIn("KUBECONFORM_SCHEMAS", got["k8s/pod.yaml"]["why"])
        self.assertFalse([x for x in self.calls() if x.startswith("kubeconform")])

    def test_infra_proof_the_trees_own_binary_symlinks_and_the_clock_cannot_move_it(self):
        from unittest import mock
        self.stub("hadolint", os.path.join(self.tree, "bin"))
        os.symlink("/etc/hostname", os.path.join(self.tree, "Dockerfile.link"))
        with mock.patch.dict(os.environ, {"PATH": os.path.join(self.tree, "bin")}):
            got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(got["Dockerfile"]["verdict"], "unproven")  # the tree's hadolint isn't the user's
        self.assertNotIn("Dockerfile.link", got)
        self.assertEqual(self.calls(), [])
        with mock.patch.object(fmprove_infra, "INFRA_T", 0):
            got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual({x["verdict"] for x in got.values()}, {"unproven"})
        self.assertIn("time", got["Dockerfile"]["why"])

    def test_infra_proof_every_class_names_a_card_that_exists_and_has_file_signals(self):
        for name, k in fmprove_infra.CLASSES.items():
            self.assertTrue(fmprove_infra._signals(k), name)

    def test_infra_proof_a_validator_that_says_it_is_not_installed_or_hangs_is_unproven_not_failed(self):
        from unittest import mock
        write(self.tree, {"compose.yaml": "services: {}\n"})
        with open(os.path.join(self.bin, "docker"), "w") as f:
            f.write("#!/bin/sh\necho \"docker: 'compose' is not a docker command.\" >&2\nexit 1\n")
        os.chmod(os.path.join(self.bin, "docker"), 0o755)
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(got["compose.yaml"]["verdict"], "unproven")
        with open(os.path.join(self.bin, "hadolint"), "w") as f:
            f.write("#!/bin/sh\nwhile :; do :; done\n")  # a builtin loop: the PATH here holds no sleep
        with mock.patch("fmfind.TOOL_T", 1):
            got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(got["Dockerfile"]["verdict"], "unproven")
        self.assertIn("timed out", got["Dockerfile"]["why"])

    def script(self, name, body):
        path = os.path.join(self.bin, name)
        with open(path, "w") as f:
            f.write(body)
        os.chmod(path, 0o755)

    def test_infra_proof_a_silent_non_zero_exit_fails_the_file_and_a_tool_that_cannot_start_is_unproven(self):
        self.script("hadolint", "#!/bin/sh\nexit 3\n")
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(got["Dockerfile"]["verdict"], "fail")
        self.assertIn("exit 3", got["Dockerfile"]["why"])
        self.script("hadolint", "#!/nonexistent/interpreter\n")
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(got["Dockerfile"]["verdict"], "unproven")
        self.assertIn("start", got["Dockerfile"]["why"])
        write(self.tree, {"app.service": "[Unit]\n"})  # systemd: only a missing ExecStart binary is benign
        self.script("systemd-analyze", "#!/bin/sh\necho \"/x is not executable: No such file or directory\" >&2\nexit 1\n")
        self.assertEqual(self.by_file(fmprove_infra.infra(self.tree, allowed=False))["app.service"]["verdict"], "pass")
        self.script("systemd-analyze", "#!/bin/sh\nexit 1\n")
        self.assertEqual(self.by_file(fmprove_infra.infra(self.tree, allowed=False))["app.service"]["verdict"], "fail")

    def test_infra_proof_terraform_with_missing_providers_is_unproven_not_failed(self):
        write(self.tree, {"main.tf": "x\n", ".terraform/p": "x"})
        self.script("terraform", "#!/bin/sh\necho 'Error: Missing required provider' >&2\nexit 1\n")
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=True))
        self.assertEqual(got["main.tf"]["verdict"], "unproven")
        self.script("terraform", "#!/bin/sh\necho 'Error: Unsupported argument' >&2\nexit 1\n")
        self.assertEqual(self.by_file(fmprove_infra.infra(self.tree, allowed=True))["main.tf"]["verdict"], "fail")

    def test_infra_proof_a_compose_include_of_a_remote_source_is_unproven_and_not_run(self):
        self.stub("docker")
        write(self.tree, {"compose.yaml": "include:\n  - oci://example.com/stack:1\nservices: {}\n"})
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(got["compose.yaml"]["verdict"], "unproven")
        self.assertFalse([x for x in self.calls() if x.startswith("docker")])
        write(self.tree, {"compose.yaml": "include:\n  - ./other.yaml\nservices: {}\n"})
        self.assertEqual(self.by_file(fmprove_infra.infra(self.tree, allowed=False))["compose.yaml"]["verdict"], "pass")

    def test_infra_proof_style_notes_do_not_fail_a_file(self):
        self.stub("shellcheck")
        write(self.tree, {"run.sh": "echo\n"})
        fmprove_infra.infra(self.tree, allowed=False)
        (hado,) = [x for x in self.calls() if x.startswith("hadolint") and "Dockerfile " in x]
        self.assertIn("--failure-threshold warning", hado)
        (shell,) = [x for x in self.calls() if x.startswith("shellcheck")]
        self.assertIn("-S warning", shell)
        self.assertIn("SC1091", shell)

    def test_infra_proof_the_tool_runs_without_a_network_where_unshare_works_and_plain_where_it_does_not(self):
        self.script("unshare", f'#!/bin/sh\necho "unshare $*" >> {self.log}\nshift 2\nexec "$@"\n')
        fmprove_infra.infra(self.tree, allowed=False)
        self.assertTrue([x for x in self.calls() if x.startswith("unshare -r -n")], self.calls())
        self.assertTrue([x for x in self.calls() if x.startswith("hadolint")], self.calls())
        os.remove(self.log)
        self.script("unshare", "#!/bin/sh\nexit 1\n")  # no user namespaces here
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(got["Dockerfile"]["verdict"], "pass")
        self.assertTrue([x for x in self.calls() if x.startswith("hadolint")])

    def test_infra_proof_a_folder_named_like_an_option_and_a_tree_over_the_copy_cap(self):
        from unittest import mock
        self.stub("terraform")
        write(self.tree, {"--x/main.tf": "x\n", "--x/.terraform/p": "x"})
        fmprove_infra.infra(self.tree, allowed=True)
        (call,) = [x for x in self.calls() if x.startswith("terraform")]
        self.assertIn("-chdir=./--x", call)
        with mock.patch.object(fmprove_infra, "STAGE_MAX", 1):
            got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(got["Dockerfile"]["verdict"], "unproven")
        self.assertIn("copy", got["Dockerfile"]["why"])

    def test_infra_proof_a_claude_worktree_folder_is_not_looked_at(self):
        write(self.tree, {".claude/worktrees/w/Dockerfile": "FROM BAD\n"})
        got = self.by_file(fmprove_infra.infra(self.tree, allowed=False))
        self.assertEqual(set(got), {"Dockerfile", "Dockerfile.bad", ".github/workflows/ci.yml"})


class InfraFinish(ForemanTestCase):
    """T-2385: fm task finish runs the infra proof on the infra files the task touched."""

    def setUp(self):
        super().setUp()
        self.bin, self.log = os.path.join(self.tmp, "bin"), os.path.join(self.tmp, "calls.log")
        tools = os.path.join(self.tmp, "tools")  # what fm itself needs, and no validator
        os.makedirs(tools)
        os.makedirs(self.bin)
        import shutil
        for need in ("git", "bash"):
            os.symlink(shutil.which(need), os.path.join(tools, need))
        self.env = {"PATH": self.bin + os.pathsep + tools}
        self.fm("init", env=self.env)
        self.fm("task", "new", "infra change", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus", env=self.env)

    def hadolint(self):
        path = os.path.join(self.bin, "hadolint")
        with open(path, "w") as f:
            f.write(f'#!/bin/sh\necho "$*" >> {self.log}\nfor last; do :; done\nIFS= read -r l < "$last"\n'
                    'case "$l" in *BAD*) echo "DL3000 it is bad"; exit 1;; esac\nexit 0\n')
        os.chmod(path, 0o755)

    def finish(self):
        return self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", "--lens", "adversary: held",
                       env=self.env, check=False)

    def evidence(self):
        import fmcore as c
        return [l for l in c.find_brief(c.find_project(self.repo), "T-0001").evidence() if "fm prove --infra" in l]

    def test_infra_finish_records_a_passing_run_as_evidence_and_a_failing_one_refuses_the_close(self):
        self.hadolint()
        write(self.repo, {"Dockerfile": "FROM BAD\n"})
        r = self.finish()
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("DL3000", r.stdout + r.stderr)
        self.assertTrue(self.evidence())
        write(self.repo, {"Dockerfile": "FROM scratch\n"})
        r = self.finish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(any("exit 0" in l and "[ran]" in l for l in self.evidence()), self.evidence())

    def test_infra_finish_a_missing_validator_is_said_once_filed_once_and_never_installed(self):
        import fmcore as c
        write(self.repo, {"Dockerfile": "FROM scratch\n"})
        r = self.finish()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("hadolint", r.stdout)
        self.assertIn("unproven", r.stdout)
        self.assertEqual(self.evidence(), [])  # an unproven file is no run
        self.fm("task", "new", "more infra", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus", env=self.env)
        write(self.repo, {"Dockerfile": "FROM scratch\n# again\n"})
        self.fm("task", "finish", "T-0002", "--audit", "self", "--run", "true", "--lens", "adversary: held",
                "--lens", "intent: ok", "--docs", "none: test", "--lesson", "none: test", env=self.env)
        mine = [b for b in c.load_briefs(c.find_project(self.repo), include_archive=True)
                if "capability-miss: hadolint" in b.section("Raw request")]
        self.assertEqual(len(mine), 1)
        self.assertEqual(self.calls(), [])

    def test_infra_finish_the_refusal_names_every_failing_file(self):
        self.hadolint()
        write(self.repo, {"Dockerfile": "FROM BAD\n", "Dockerfile.two": "FROM BAD\n", "Dockerfile.three": "FROM scratch\n"})
        r = self.finish()
        self.assertNotEqual(r.returncode, 0)
        out = r.stdout + r.stderr
        self.assertIn("Dockerfile ", out)
        self.assertIn("Dockerfile.two", out)
        self.assertNotIn("Dockerfile.three", out.split("failing (recorded)")[-1])

    def test_infra_finish_a_task_that_touched_no_infra_file_runs_nothing(self):
        self.hadolint()
        write(self.repo, {"app.py": "x = 1\n"})
        self.assertEqual(self.finish().returncode, 0)
        self.assertEqual((self.evidence(), self.calls()), ([], []))

    def calls(self):
        try:
            with open(self.log) as f:
                return f.read().splitlines()
        except OSError:
            return []


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
