"""Follow-ups from the session-wide review (T-0296): docs drift (T-0292), operator gaps (T-0293), duel rivals must be
installed plugins (T-0294)."""
import json
import os
import subprocess

from helpers import PLUGIN, ForemanTestCase, read_text

MASTER = os.path.join(os.path.dirname(PLUGIN), "MASTER.md")


class Docs(ForemanTestCase):
    def test_master_matches_the_code(self):
        lines = read_text(MASTER).splitlines()
        cli = next(ln for ln in lines if ln.startswith("CLI (on the Bash tool PATH)"))
        for word in ("landscape", "deps", "replay [", "--cmd TEXT", "duel", "versions", "court", "soak"):
            self.assertIn(word, cli)
        hunks = next(ln for ln in lines if ln.startswith("- Hunk mutation proof (T-0271"))
        self.assertNotIn("git apply", hunks)  # T-0286 replaced it
        files = next(ln for ln in lines if ln.startswith("| `plugin/lib/` |"))
        self.assertIn("duel", files.split("`fmbench`", 1)[1].split("`fmresearch`", 1)[0])


class Operator(ForemanTestCase):
    def test_doctor_checks_routing(self):
        import fmdoctor
        good = os.path.join(PLUGIN, "skills", "routing.json")
        self.assertEqual(fmdoctor.check_routing(good).status, "PASS")
        bad = os.path.join(self.tmp, "routing.json")
        with open(bad, "w") as f:
            json.dump({"lens_words": {"adversary": "security"}}, f)
        self.assertEqual(fmdoctor.check_routing(bad).status, "FAIL")
        with open(bad, "w") as f:
            f.write("{not json")
        self.assertEqual(fmdoctor.check_routing(bad).status, "FAIL")

    def test_ignored_flags_are_refused(self):
        self.fm("init")
        p = self.fm("replay", "--cwd", self.repo, check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("--cmd", p.stderr)
        tid = json.loads(self.fm("capture", "x", "--json").stdout)["id"]
        p = self.fm("second", "debate", tid, "--review", "x", "--model", "opus", check=False)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("--model", p.stderr)
        p = self.fm("second", "debate", tid, "--review", "x", check=False)  # no --model: refused for another reason
        self.assertNotIn("--model", p.stderr)

    def test_another_projects_damage_warns(self):
        import fmcore as c
        import fmdoctor
        self.fm("init")
        here = c.find_project(self.repo)
        other = os.path.join(self.tmp, "other")
        os.makedirs(other)
        subprocess.run(["git", "init", "-q", other], check=True)
        self.fm("init", cwd=other)
        there = c.find_project(other)
        with open(os.path.join(there.dir, "meta-copy.json"), "w") as f:
            f.write("{truncated")
        r = fmdoctor.check_integrity([], [here, there], current=here)
        self.assertEqual(r.status, "WARN")
        self.assertIn(there.slug, r.detail)
        with open(os.path.join(here.dir, "meta-copy.json"), "w") as f:
            f.write("{truncated")
        self.assertEqual(fmdoctor.check_integrity([], [here, there], current=here).status, "FAIL")
        os.remove(os.path.join(here.dir, "meta-copy.json"))
        os.remove(os.path.join(there.dir, "meta-copy.json"))
        for root in (other, self.repo):  # a crash's empty object, old enough to count
            obj = os.path.join(root, ".git", "objects", "ab", "c" * 38)
            os.makedirs(os.path.dirname(obj), exist_ok=True)
            open(obj, "w").close()
            os.utime(obj, (1, 1))
        self.assertEqual(fmdoctor.check_integrity([other], [here, there], current=here).status, "WARN")
        self.assertEqual(fmdoctor.check_integrity([self.repo], [here, there], current=here).status, "FAIL")
        # review: from a lane, the project's repo is still the current one; from no project, only Foreman's own fails
        wt = os.path.join(self.tmp, "lane")
        subprocess.run(["git", "-C", self.repo, "worktree", "add", "-q", "-b", "lane", wt], check=True)
        self.assertEqual(fmdoctor.check_integrity([self.repo], [here], current=c.find_project(wt)).status, "FAIL")
        self.assertEqual(fmdoctor.check_integrity([self.repo, other], [here, there], current=False).status, "WARN")


class Rival(ForemanTestCase):
    def test_only_installed_plugins_duel(self):
        import fmbench
        cc = os.path.join(self.tmp, "cc")
        rival = os.path.join(self.tmp, "rival")
        os.makedirs(os.path.join(rival, ".claude-plugin"))
        with open(os.path.join(rival, ".claude-plugin", "plugin.json"), "w") as f:
            f.write('{"name": "rival"}')
        stray = os.path.join(self.tmp, "stray")
        os.makedirs(os.path.join(stray, ".claude-plugin"))
        with open(os.path.join(stray, ".claude-plugin", "plugin.json"), "w") as f:
            f.write('{"name": "stray"}')
        os.makedirs(os.path.join(cc, "plugins"))
        with open(os.path.join(cc, "plugins", "installed_plugins.json"), "w") as f:
            json.dump({"version": 2, "plugins": {"rival@m": [{"scope": "user", "installPath": rival}]}}, f)
        os.environ["CLAUDE_CONFIG_DIR"] = cc
        try:
            self.assertEqual(fmbench._contender("rival@m")[0], rival)
            self.assertEqual(fmbench._contender("rival")[0], rival)
            self.assertEqual(fmbench._contender(rival)[0], rival)  # the folder of an installed one
            self.assertIsNone(fmbench._contender(stray)[0])  # any other folder isn't
        finally:
            del os.environ["CLAUDE_CONFIG_DIR"]


class Lfs(ForemanTestCase):
    def test_a_planted_lfs_driver_runs_only_git_lfs(self):
        # background security review: 'git-lfs smudge -- %f; <cmd>' passed the old prefix check
        import fmbench
        repo = os.path.join(self.tmp, "r")
        os.makedirs(repo)
        subprocess.run(["git", "init", "-q", repo], check=True)
        for k, v in (("user.email", "t@t"), ("user.name", "t")):
            subprocess.run(["git", "-C", repo, "config", k, v], check=True)
        with open(os.path.join(repo, ".gitattributes"), "w") as f:
            f.write("*.txt filter=lfs\n")
        with open(os.path.join(repo, "a.txt"), "w") as f:
            f.write("hi\n")
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "base"], check=True)
        marker = os.path.join(self.tmp, "ran")
        for key, cmd in (("clean", "git-lfs clean -- %f"), ("smudge", "git-lfs smudge -- %f")):
            subprocess.run(["git", "-C", repo, "config", f"filter.lfs.{key}", f"{cmd}; touch {marker}"], check=True)
        subprocess.run(["git", "-C", repo, "config", "filter.lfs.process", f"git-lfs filter-process; touch {marker}"],
                       check=True)
        with open(os.path.join(repo, "a.txt"), "w") as f:
            f.write("changed\n")
        fmbench._git(repo, "add", "-A")
        fmbench._git(repo, "checkout", "HEAD", "--", "a.txt")
        self.assertFalse(os.path.exists(marker))
