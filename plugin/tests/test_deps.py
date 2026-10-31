"""T-1049: the dependency-install check: typosquat, age and registry notes before an install runs."""
import json
import os
import time
import unittest

from test_hooks import HookCase

import fmcore as c
import fmdeps

NONET = {"FOREMAN_NO_NET": "1"}




class Deps(HookCase):
    def setUp(self):
        super().setUp()
        old = os.environ.get("HOME")
        os.environ["HOME"] = self.tmp  # no registry config of the machine's own reaches the lookups
        self.addCleanup(lambda: os.environ.__setitem__("HOME", old) if old else os.environ.pop("HOME", None))
        self.task()  # registers the project and gives the session a brief

    def found(self, cmd, env=NONET):
        return json.loads(self.fm("deps", "check", cmd, "--json", env=env).stdout)["findings"]

    def test_a_typosquat_is_named_and_the_real_name_is_silent(self):
        f = self.found("npm i lodahs")
        self.assertTrue(any(x["kind"] == "typosquat" and "lodash" in x["why"] for x in f), f)
        self.assertEqual(self.found("npm i lodash"), [])

    def test_a_custom_registry_or_url_spec_is_flagged(self):
        self.assertTrue(any(x["kind"] == "registry" for x in self.found("pip install --index-url http://x requests")))
        self.assertTrue(any(x["kind"] == "registry" for x in self.found("pip install git+https://x/y.git")))
        self.assertTrue(any(x["kind"] == "registry" for x in self.found("npm i left-pad --registry=http://x")))

    def test_a_package_already_in_the_manifest_is_not_new(self):
        with open(os.path.join(self.repo, "package.json"), "w") as f:
            json.dump({"dependencies": {"lodahs": "1.0.0"}}, f)
        self.assertEqual(self.found("npm i lodahs"), [])

    def test_a_young_package_is_flagged_with_a_fake_fetcher(self):
        p = self.project()
        new = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 3 * 86400))
        f = fmdeps.check(p, "npm i brand-new-thing", fetch=lambda eco, name: new)
        self.assertTrue(any(x["kind"] == "age" for x in f), f)
        old = fmdeps.check(p, "npm i brand-new-thing", fetch=lambda eco, name: "2015-01-01T00:00:00Z")
        self.assertEqual(old, [])

    def test_a_failing_fetcher_is_age_unknown_not_an_error(self):
        def boom(eco, name):
            raise OSError("down")
        f = fmdeps.check(self.project(), "cargo add serde_x", fetch=boom)
        self.assertFalse(any(x["kind"] == "age" for x in f))

    def test_a_slow_fetcher_is_cut_off_by_one_total_budget(self):
        t = time.time()
        f = fmdeps.check(self.project(), "npm i lodahs brand-a brand-b", fetch=lambda e, n: time.sleep(5))
        self.assertLess(time.time() - t, 1.6)  # wall clock: the total fetch budget deadline (the fetcher sleeps)
        self.assertTrue(any(x["kind"] == "typosquat" for x in f))

    def test_at_most_two_lookups_and_never_for_popular_scoped_or_configured(self):
        seen = []
        fmdeps.check(self.project(), "npm i lodash @s/x aa-1 bb-2 cc-3", fetch=lambda e, n: seen.append(n))
        self.assertEqual(seen, ["aa-1", "bb-2"])
        with open(os.path.join(self.repo, ".npmrc"), "w") as f:
            f.write("registry=https://corp.example/\n")
        seen.clear()
        fmdeps.check(self.project(), "npm i aa-1", fetch=lambda e, n: seen.append(n))
        self.assertEqual(seen, [])

    def test_flags_are_read_per_tool(self):
        self.assertEqual([k["name"] for k in fmdeps.parse_install("npm i -f typo")], ["typo"])
        self.assertEqual(fmdeps.parse_install("npm i -f typo")[0]["registry"], "")
        self.assertEqual([k["name"] for k in fmdeps.parse_install("pip install --trusted-host h requests")], ["requests"])
        self.assertEqual([k["name"] for k in fmdeps.parse_install("npm i --omit dev foo")], ["foo"])
        self.assertTrue(fmdeps.parse_install("pip install -f http://x requests")[0]["registry"])
        for cmd in ("uv add foo", "uv pip install foo", "poetry add foo", "pipx install foo", "yarn global add foo",
                    "python3.12 -m pip install foo", 'bash -c "npm i foo"', "cargo add foo"):
            self.assertEqual([k["name"] for k in fmdeps.parse_install(cmd)], ["foo"], cmd)
        self.assertEqual(fmdeps.parse_install("cargo add foo")[0]["eco"], "crates")

    def test_boto_and_pyaml_are_not_typosquats(self):
        self.assertEqual([x for x in fmdeps.check(self.project(), "pip install boto pyaml", fetch=None)
                          if x["kind"] == "typosquat"], [])

    def test_the_hook_notes_and_never_blocks(self):
        r = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {
            "command": "pip install --index-url http://x requests"}}, env=NONET)
        self.assertEqual(r.returncode, 0)
        self.assertIn("registry", self.ctx_of(r))
        r = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "npm i lodash"}}, env=NONET)
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("lodash", self.ctx_of(r))

    def test_a_command_with_no_install_word_skips_the_check(self):
        # T-2017: every Bash call imported fmdeps (urllib, socket) to find nothing to check
        import fmhooks
        from unittest import mock
        p = c.find_project(self.repo)
        with mock.patch.object(fmdeps, "note") as note:
            self.assertIsNone(fmhooks._dep_note({"tool_name": "Bash", "tool_input": {"command": "ls -la && git status"}}, p))
            note.assert_not_called()
        for cmd in ("pip install --index-url http://x requests", "cd x && npm i lodash", "uv add foo", "cargo install x"):
            self.assertTrue(fmhooks._INSTALL_WORD.search(cmd), cmd)


if __name__ == "__main__":
    unittest.main()
