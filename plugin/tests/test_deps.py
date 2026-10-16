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

    def test_the_hook_notes_and_never_blocks(self):
        r = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {
            "command": "pip install --index-url http://x requests"}}, env=NONET)
        self.assertEqual(r.returncode, 0)
        self.assertIn("registry", self.ctx_of(r))
        r = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "npm i lodash"}}, env=NONET)
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("lodash", self.ctx_of(r))


if __name__ == "__main__":
    unittest.main()
