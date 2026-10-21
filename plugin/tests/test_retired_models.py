"""T-1409: fm code runners --check flags a configured model id the provider has retired, from fmmodels' dated table,
and names its replacement. No network: the table is static and --check only reads it."""
import json
import os
import shutil
import sys
import unittest

import helpers  # noqa: F401  (puts plugin/lib on sys.path)
import fmmodels as m
from test_code import CodeCase


class RetiredTable(unittest.TestCase):
    def test_lookup_strips_a_provider_prefix_and_ignores_active_or_future_ids(self):
        self.assertEqual(m.retired("claude-3-opus-20240229")["replacement"], "claude-opus-4-8")
        self.assertEqual(m.retired("openai/gpt-4.5-preview")["date"], "2025-07-14")
        self.assertEqual(m.retired("models/gemini-2.0-flash")["replacement"], "gemini-3.6-flash")
        self.assertEqual(m.retired(" GPT-4.5-Preview ")["replacement"], "gpt-4.1")
        for active in ("claude-sonnet-5-5", "gpt-4.1-mini", "gpt-4-turbo", "claude-sonnet-4-5-20250929", "", None, 3):
            self.assertIsNone(m.retired(active), active)

    def test_every_row_is_dated_on_or_before_the_tables_date_and_names_its_page(self):
        for model, (date, repl, page) in m.RETIRED.items():
            self.assertLessEqual(date, m.RETIRED_AS_OF, model)
            self.assertTrue(repl and page.startswith("https://"), model)
        for _, _, _, mo, _, _ in m.CLOUD:
            self.assertIsNone(m.retired(mo), f"a built-in default ({mo}) is retired")


class RunnersCheck(CodeCase):
    def setUp(self):
        super().setUp()
        self.bin = os.path.join(self.tmp, "bin")  # git only: no real CLI answers --version
        os.makedirs(self.bin)
        os.symlink(shutil.which("git"), os.path.join(self.bin, "git"))
        profs = {"old": {"kind": "anthropic", "base_url": "https://api.anthropic.com/v1",
                         "model": "claude-3-opus-20240229"},
                 "router": {"kind": "openai", "base_url": "https://openrouter.ai/api/v1",
                            "model": "openai/gpt-4.5-preview"},
                 "fresh": {"kind": "anthropic", "base_url": "https://api.anthropic.com/v1",
                           "model": "claude-sonnet-5-5"}}
        with open(os.path.join(self.home, "models.json"), "w") as f:
            json.dump({"profiles": profs}, f)

    def runners(self, *args):
        return self.code("runners", *args, env={"PATH": self.bin})

    def test_check_reports_retired_ids_with_date_and_replacement(self):
        got = {x["name"]: x for x in json.loads(self.runners("--check", "--json").stdout)["models"]}
        self.assertEqual((got["old"]["retired"], got["old"]["retired_on"], got["old"]["replacement"]),
                         (True, "2026-01-05", "claude-opus-4-8"))
        self.assertEqual((got["router"]["retired"], got["router"]["retired_on"], got["router"]["replacement"]),
                         (True, "2025-07-14", "gpt-4.1"))
        self.assertNotIn("retired", got["fresh"], "an active id reports nothing")
        text = self.runners("--check").stdout
        self.assertIn("old (claude-3-opus-20240229) was retired 2026-01-05: use claude-opus-4-8", text)
        self.assertIn("router (openai/gpt-4.5-preview) was retired 2025-07-14: use gpt-4.1", text)
        self.assertNotIn("fresh (claude-sonnet-5-5) was retired", text)

    def test_without_check_nothing_is_flagged(self):
        got = json.loads(self.runners("--json").stdout)["models"]
        self.assertFalse([x for x in got if "retired" in x])
        self.assertNotIn("was retired", self.runners().stdout)


if __name__ == "__main__":
    sys.exit(unittest.main())
