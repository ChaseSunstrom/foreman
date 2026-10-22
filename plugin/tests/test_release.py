"""T-1188: fm release VERSION: the release ritual as named steps with a checkpoint after each. (release.py, the thin
wrapper over it, is tested in test_release_py.py.)"""
import json
import os
import subprocess
import sys
import time

from helpers import ForemanTestCase, read_json, read_text, stub_corpus_replay

import fmcore as c

STUB = '''import json, os, sys, time
verb = sys.argv[1]
once = os.path.join(os.environ.get("STUB_FAIL_ONCE", "/nonexistent"), verb)
if os.path.exists(once):  # this gate fails once, then passes
    os.remove(once)
    sys.exit(1)
if verb == "projects":
    n = int(os.environ.get("STUB_N", "1"))
    print(json.dumps({"projects": [{"project": "app" + (str(i) if n > 1 else ""), "root": os.environ["STUB_ROOT"],
                                    "exists": True} for i in range(n)]}))
elif verb == "sentinel":
    log = os.environ.get("STUB_LOG")
    if log:
        with open(log, "a") as f:
            f.write("start\\n")
        time.sleep(0.5)
        with open(log, "a") as f:
            f.write("end\\n")
    time.sleep(float(os.environ.get("STUB_SLEEP", "0")))
    print("1 proof fails now")
    sys.exit(1 if os.environ.get("STUB_FAIL") else 0)
'''


def put(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def sh(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, check=True).stdout


def stub_env(tmp, root):
    """A stub fm for the gates (check, release-check) and the canary (projects, sentinel): every gate passes."""
    path = os.path.join(tmp, "fmstub.py")
    put(tmp, "fmstub.py", STUB)
    return {"FOREMAN_RELEASE_FM": path, "STUB_ROOT": root}


class ReleaseCase(ForemanTestCase):
    replayed = True  # T-1401: a fresh green guard corpus replay on record, so --push isn't refused

    def setUp(self):
        super().setUp()
        put(self.repo, "plugin/.claude-plugin/plugin.json", '{\n  "name": "foreman",\n  "version": "1.0.0"\n}\n')
        put(self.repo, "CHANGELOG.md", "# Changelog\n\n## Unreleased\n- a thing\n\n## 1.0.0 — 2026-01-01\n- first\n")
        put(self.repo, "mods/foreman-ui/.claude-plugin/plugin.json", '{\n  "name": "foreman-ui",\n  "version": "0.1.0"\n}\n')
        put(self.repo, "mods/foreman-ui/hooks/a.tsx", "a\n")
        self.market = {"name": "foreman", "metadata": {"version": "1.0.0"}, "plugins": [
            {"name": "foreman", "version": "1.0.0"}, {"name": "foreman-ui", "version": "0.1.0"}]}
        put(self.repo, ".claude-plugin/marketplace.json", json.dumps(self.market))
        self.fm("init")
        if self.replayed:
            stub_corpus_replay(self.repo)
        sh(self.repo, "add", ".")
        sh(self.repo, "commit", "-qm", "Foreman 1.0.0")
        self.env = stub_env(self.tmp, self.repo)

    def rel(self, *a, check=True, env=True):
        return self.fm("release", *a, check=check, env=self.env if env else None)

    def tid(self, grant=False):
        t = json.loads(self.fm("task", "new", "ship", "--type", "FEATURE", "--tier", "S", "--json").stdout)["id"]
        self.fm("task", "step", t, "add", "ship it")
        self.fm("task", "ac", t, "add", "shipped", "--verify", "true")
        self.fm("focus", t)
        if grant:
            self.grant(t)
        return t

    def grant(self, t):
        p = c.find_project(self.repo)
        b = c.find_brief(p, t)
        b.meta["allow"] = ["publish"]
        c.save_brief(p, b)

    def origin(self):
        origin = os.path.join(self.tmp, "origin.git")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", origin], check=True)
        sh(self.repo, "remote", "add", "origin", origin)
        sh(self.repo, "push", "-q", "origin", "main")
        sh(self.repo, "checkout", "-q", "-b", "work")
        return origin

    def subject(self):
        return sh(self.repo, "log", "-1", "--format=%s").strip()


class Release(ReleaseCase):
    def test_dry_run_lists_every_step_and_changes_nothing(self):
        out = self.rel("9.9.9", "--dry-run").stdout
        for name in ("tree", "check", "bump", "changelog", "commit", "release-check", "canary", "push", "round"):
            self.assertIn(name, out)
        # T-1199: the canary is never fatal, so it never holds the push: it runs last
        self.assertLess(out.index("push:"), out.index("canary:"))
        self.assertLess(out.index("round:"), out.index("canary:"))
        self.assertEqual(sh(self.repo, "status", "--porcelain"), "")
        self.assertEqual(read_json(os.path.join(self.repo, "plugin/.claude-plugin/plugin.json"))["version"], "1.0.0")

    def test_a_run_stopped_after_step_two_resumes_at_step_three(self):
        mk = os.path.join(self.repo, ".claude-plugin/marketplace.json")
        put(self.repo, ".claude-plugin/marketplace.json", "{broken")  # step 3 can't bump it
        sh(self.repo, "commit", "-qam", "break it")
        r = self.rel("9.9.9", "--no-check", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("bump", r.stderr + r.stdout)
        self.assertEqual(self.subject(), "break it")
        put(self.repo, ".claude-plugin/marketplace.json", json.dumps(self.market))
        sh(self.repo, "commit", "-qam", "fix it")
        self.assertNotEqual(self.rel("8.0.0", "--resume", check=False).returncode, 0, "another version")
        out = self.rel("9.9.9", "--resume").stdout
        self.assertIn("resuming at step 3", out)
        self.assertEqual(self.subject(), "Foreman 9.9.9")
        self.assertEqual(read_json(mk)["plugins"][0]["version"], "9.9.9")
        self.assertEqual(read_json(mk)["plugins"][1]["version"], "0.1.0", "the UI didn't change")
        self.assertIn("## 9.9.9 — ", read_text(os.path.join(self.repo, "CHANGELOG.md")))
        self.assertIn("round-1", sh(self.repo, "tag", "--list"))
        self.assertIn("already released", self.rel("9.9.9", "--resume").stdout)

    def test_a_resume_keeps_the_first_runs_flags(self):
        put(self.repo, "mods/foreman-ui/hooks/a.tsx", "b\n")
        sh(self.repo, "commit", "-qam", "ui change")
        r = self.rel("9.9.9", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--ui", r.stderr + r.stdout)
        self.rel("9.9.9", "--resume", "--ui", "0.2.0")
        mk = read_json(os.path.join(self.repo, ".claude-plugin/marketplace.json"))
        self.assertEqual(mk["plugins"][1]["version"], "0.2.0")
        self.assertEqual(read_json(os.path.join(self.repo, "mods/foreman-ui/.claude-plugin/plugin.json"))["version"], "0.2.0")

    def test_a_ui_version_that_isnt_semver_is_refused(self):
        r = self.rel("9.9.9", "--ui", "0.2", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(sh(self.repo, "status", "--porcelain"), "")

    def test_the_first_runs_ui_is_reused_on_resume(self):
        self.rel("9.9.9", "--ui", "0.2.0", "--no-check")
        state = read_json(os.path.join(c.find_project(self.repo).dir, "release.json"))
        self.assertEqual((state["ui"], state["no_check"]), ("0.2.0", True))
        self.assertEqual(sorted(state["skipped"]), ["canary", "check", "release-check"])
        self.assertNotIn("check", state["done"])

    def test_push_without_the_publish_grant_refuses_before_any_change(self):
        r = self.rel("9.9.9", "--push", check=False)
        self.assertNotEqual(r.returncode, 0)
        out = r.stderr + r.stdout
        self.assertIn("fm ask ID publish", out)  # T-1322: both ways, the ask first
        self.assertIn("fm task set ID --allow publish", out)
        self.assertLess(out.index("fm ask ID publish"), out.index("--allow publish"))
        self.assertEqual(sh(self.repo, "status", "--porcelain"), "")
        self.assertEqual(self.subject(), "Foreman 1.0.0")

    def test_skipped_gates_cannot_push(self):
        self.origin()
        self.tid(grant=True)
        r = self.rel("9.9.9", "--push", "--no-check", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("skipped", r.stderr + r.stdout)
        self.assertEqual(self.subject(), "Foreman 1.0.0")

    def test_push_with_the_grant_merges_into_origin_main_and_spends_it(self):
        origin = self.origin()
        tid = self.tid(grant=True)
        self.rel("9.9.9", "--push")
        self.assertEqual(sh(origin, "log", "-1", "--format=%s", "main").strip(), "Foreman 9.9.9")
        self.assertEqual(sh(origin, "log", "-1", "--format=%p", "main").count(" "), 1, "a --no-ff merge")
        p = c.find_project(self.repo)
        self.assertNotIn("publish", c.find_brief(p, tid).meta.get("allow") or [])
        self.assertIn("grant_spent", read_text(os.path.join(p.dir, "ledger.jsonl")))
        self.assertEqual(sh(self.repo, "branch", "--show-current").strip(), "work")

    def fail_once(self, verb):
        d = os.path.join(self.tmp, "failonce")
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, verb), "w").close()
        self.env["STUB_FAIL_ONCE"] = d

    def test_a_later_push_merges_the_release_commit_not_later_work(self):
        origin = self.origin()
        self.rel("9.9.9")
        put(self.repo, "later.txt", "x\n")
        sh(self.repo, "add", "later.txt")
        sh(self.repo, "commit", "-qm", "later, never gated")
        self.tid(grant=True)
        self.rel("9.9.9", "--push")
        self.assertNotIn("later, never gated", sh(origin, "log", "--format=%s", "main"))
        self.assertEqual(sh(origin, "log", "-1", "--format=%s", "main").strip(), "Foreman 9.9.9")

    def test_a_failed_gate_resumes_at_that_gate_and_a_plain_rerun_resumes_too(self):
        self.fail_once("check")
        self.assertNotEqual(self.rel("9.9.9", check=False).returncode, 0)
        self.assertEqual(self.subject(), "Foreman 1.0.0")
        self.assertIn("resuming at step 2", self.rel("9.9.9", "--resume").stdout)
        self.assertEqual(self.subject(), "Foreman 9.9.9")
        self.rel("--abandon")
        self.fail_once("release-check")  # stopped after the bump and commit
        self.assertNotEqual(self.rel("9.9.10", check=False).returncode, 0)
        self.assertIn("resuming at step 6", self.rel("9.9.10").stdout)  # not "9.9.10 isn't newer than 9.9.10"

    def test_stubbed_gates_never_push_to_a_real_remote(self):
        self.origin()
        sh(self.repo, "remote", "set-url", "origin", "https://example.invalid/foreman.git")
        self.tid(grant=True)
        r = self.rel("9.9.9", "--push", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("FOREMAN_RELEASE_FM", r.stderr + r.stdout)
        self.assertEqual(self.subject(), "Foreman 1.0.0")

    def test_a_remote_that_looks_like_an_option_is_refused(self):
        self.tid(grant=True)
        r = self.rel("9.9.9", "--push", "--remote=--upload-pack=touch x", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.subject(), "Foreman 1.0.0")

    def test_abandon_with_dry_run_keeps_the_state_and_a_corrupt_state_can_be_abandoned(self):
        self.fail_once("check")
        self.rel("9.9.9", check=False)
        state = os.path.join(c.find_project(self.repo).dir, "release.json")
        self.rel("--abandon", "--dry-run")
        self.assertTrue(os.path.isfile(state))
        put(os.path.dirname(state), "release.json", "{torn")
        self.assertIn("abandon", self.rel("9.9.9", check=False).stderr)  # a clear error, not a traceback
        self.rel("--abandon")
        self.assertFalse(os.path.isfile(state))

    def test_the_commit_takes_only_the_release_files(self):
        self.fail_once("check")
        self.rel("9.9.9", check=False)  # stopped at step 2: the tree step, done, isn't rerun on resume
        put(self.repo, "staged.txt", "x\n")
        sh(self.repo, "add", "staged.txt")
        self.rel("9.9.9", "--resume")
        self.assertEqual(self.subject(), "Foreman 9.9.9")
        self.assertNotIn("staged.txt", sh(self.repo, "show", "--name-only", "--format=", "HEAD"))

    def test_a_release_without_push_can_be_pushed_later_and_only_pushes(self):
        origin = self.origin()
        self.rel("9.9.9")
        self.assertNotIn("Foreman 9.9.9", sh(origin, "log", "-3", "--format=%s", "main"))
        self.assertIn("already released", self.rel("9.9.9", "--resume").stdout, "no push asked, none left to do")
        self.tid(grant=True)
        out = self.rel("9.9.9", "--push").stdout
        self.assertNotIn("step 3/", out)
        self.assertIn("step 7/9 push", out)
        self.assertEqual(sh(origin, "log", "-1", "--format=%s", "main").strip(), "Foreman 9.9.9")
        self.assertEqual(sh(self.repo, "tag", "--list").split().count("round-1"), 1, "no second round")

    def canary_report(self, v):
        """The detached canary's report once it has finished."""
        path = os.path.join(c.find_project(self.repo).dir, "logs", f"canary-{v}.txt")
        for _ in range(100):
            if os.path.isfile(path) and "canary done" in read_text(path):
                return read_text(path)
            time.sleep(0.2)
        self.fail("the canary never finished")

    def test_the_canary_runs_detached_and_its_failure_lands_in_the_inbox_and_the_notify_hook(self):
        note = os.path.join(self.tmp, "note.txt")
        self.fm("notify", f'echo "$1" > {note}')
        self.env.update(STUB_SLEEP="3", STUB_FAIL="1", FOREMAN_NO_BACKGROUND="")  # detached for real; waited on below
        out = self.rel("9.9.9").stdout  # returns before the 3 s sentinel ends: the status below finds it unfinished
        self.assertIn("canary-9.9.9.txt", out)
        self.assertIn("--canary-status", out)
        self.assertNotIn("canary done", self.rel("--canary-status").stdout)
        report = self.canary_report("9.9.9")
        self.assertIn("app: 1 proof fails now", report)
        titles = [b.title for b in c.load_briefs(c.find_project(self.repo))]
        self.assertTrue(any("canary" in t.lower() and "app" in t for t in titles), titles)
        for _ in range(50):
            if os.path.isfile(note):
                break
            time.sleep(0.2)
        self.assertIn("app", read_text(note))
        self.assertIn("app: 1 proof fails now", self.rel("--canary-status").stdout)

    def test_canary_status_without_a_run_says_so(self):
        self.assertIn("no canary", self.rel("--canary-status").stdout)

    def test_the_canary_runs_for_real_and_is_never_fatal(self):
        self.rel("9.9.9")
        report = self.canary_report("9.9.9")
        self.assertIn("canary: fm sentinel in 1 project", report)
        self.assertIn("app: 1 proof fails now", report)
        put(self.tmp, "gone", "")
        self.env["STUB_ROOT"] = os.path.join(self.tmp, "no-such-dir")  # sentinel can't start there: OSError
        sh(self.repo, "checkout", "-q", "-b", "second")
        put(self.repo, "CHANGELOG.md", read_text(os.path.join(self.repo, "CHANGELOG.md")).replace("## Unreleased", "## Unreleased\n- more", 1))
        sh(self.repo, "commit", "-qam", "more")
        self.rel("9.9.10")
        self.assertIn("couldn't run", self.canary_report("9.9.10"))

    def test_the_canary_runs_sentinels_side_by_side_and_reports_in_project_order(self):
        log = os.path.join(self.tmp, "sentinels.log")
        self.env.update(STUB_N="4", STUB_LOG=log)
        self.rel("9.9.9")
        out = self.canary_report("9.9.9")
        self.assertGreaterEqual(read_text(log).split("end")[0].count("start"), 2, "two sentinels ran at once")
        lines = [ln.strip() for ln in out.splitlines() if ": 1 proof fails now" in ln]
        self.assertEqual([ln.split(":")[0][2:] for ln in lines], ["app0", "app1", "app2", "app3"])

    def test_an_unfinished_release_of_another_version_blocks_a_new_one_until_abandoned(self):
        put(self.repo, "CHANGELOG.md", "# Changelog\n")  # step 4 fails with the bump already written
        sh(self.repo, "commit", "-qam", "break it")
        self.assertNotEqual(self.rel("9.9.9", check=False).returncode, 0)
        r = self.rel("9.9.10", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("9.9.9", r.stderr)
        self.assertIn("--abandon", r.stderr)
        self.rel("--abandon")
        sh(self.repo, "checkout", "--", ".")
        put(self.repo, "CHANGELOG.md", "# Changelog\n\n## Unreleased\n- a thing\n")
        sh(self.repo, "commit", "-qam", "fix it")
        self.rel("9.9.10")
        self.assertEqual(self.subject(), "Foreman 9.9.10")

    def test_a_plugin_json_version_that_isnt_numeric_is_a_clear_error(self):
        put(self.repo, "plugin/.claude-plugin/plugin.json", '{"name": "foreman", "version": "1.x"}\n')
        sh(self.repo, "commit", "-qam", "odd")
        r = self.rel("9.9.9", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("MAJOR.MINOR.PATCH", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_outside_foremans_own_repo_it_refuses(self):
        os.remove(os.path.join(self.repo, "plugin/.claude-plugin/plugin.json"))
        self.assertIn("Foreman's own repo", self.rel("9.9.9", "--dry-run", check=False).stderr)
