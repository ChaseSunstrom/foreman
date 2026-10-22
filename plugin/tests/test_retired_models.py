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
        for active in ("claude-sonnet-5-5", "gpt-4.1-mini", "", None, 3):
            self.assertIsNone(m.retired(active, "2026-10-22"), active)

    def test_an_alias_is_retired_on_its_date_and_retiring_within_60_days_before(self):
        # T-1433: gpt-4 and gpt-4-turbo are aliases of models the page retires 2026-10-23
        self.assertIsNone(m.retired("gpt-4", "2026-10-22"))
        got = m.retiring("gpt-4", "2026-10-22")
        self.assertEqual((got["date"], got["replacement"]), ("2026-10-23", "gpt-5.6-sol"))
        self.assertEqual(m.retired("gpt-4", "2026-10-23")["replacement"], "gpt-5.6-sol")
        self.assertIsNone(m.retiring("gpt-4", "2026-10-23"), "retired is not retiring")
        self.assertEqual(m.retired("openai/GPT-4-turbo", "2026-11-01")["date"], "2026-10-23")
        self.assertEqual(m.retired("o1-mini", "2026-10-22")["replacement"], "o4-mini")
        # 60 days out is in, 61 is out: sonnet 4.5 retires 2026-11-30
        self.assertIsNotNone(m.retiring("claude-sonnet-4-5-20250929", "2026-10-01"))
        self.assertIsNone(m.retiring("claude-sonnet-4-5-20250929", "2026-09-30"))
        self.assertIsNone(m.retiring("claude-sonnet-5-5", "2026-10-22"))
        self.assertIsNone(m.retiring(None, "2026-10-22"))

    def test_the_tables_are_dated_and_ordered_within_each_provider(self):
        for table in (m._RETIRED_ROWS, m._RETIRING_ROWS):
            for prov in m._PAGES:
                days = [r[1] for r in table if r[0] == prov]
                self.assertEqual(days, sorted(days, reverse=True), (prov, days))
        self.assertTrue(all(r[1] <= m.RETIRED_AS_OF for r in m._RETIRED_ROWS))
        self.assertTrue(all(r[1] > m.RETIRED_AS_OF for r in m._RETIRING_ROWS))

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

    def test_check_notes_a_model_retiring_soon_and_the_help_names_both_checks(self):
        profs = {"alias": {"kind": "openai", "base_url": "https://api.openai.com/v1", "model": "gpt-4"},
                 "far": {"kind": "openai", "base_url": "https://api.openai.com/v1", "model": "gpt-4.1-2025-04-14"}}
        with open(os.path.join(self.home, "models.json"), "w") as f:
            json.dump({"profiles": profs}, f)
        env = {"PATH": self.bin, "FOREMAN_TODAY": "2026-10-22"}
        got = {x["name"]: x for x in json.loads(self.code("runners", "--check", "--json", env=env).stdout)["models"]}
        self.assertEqual((got["alias"]["retiring_on"], got["alias"]["replacement"]), ("2026-10-23", "gpt-5.6-sol"))
        self.assertNotIn("retiring_on", got["far"])
        self.assertIn("alias (gpt-4) is retiring on 2026-10-23 -> gpt-5.6-sol",
                      self.code("runners", "--check", env=env).stdout)
        env["FOREMAN_TODAY"] = "2026-10-24"
        got = {x["name"]: x for x in json.loads(self.code("runners", "--check", "--json", env=env).stdout)["models"]}
        self.assertTrue(got["alias"]["retired"])
        helptext = self.code("runners", "--help").stdout
        self.assertIn("retired", helptext)
        self.assertIn("retiring", helptext)

    def test_without_check_nothing_is_flagged(self):
        got = json.loads(self.runners("--json").stdout)["models"]
        self.assertFalse([x for x in got if "retired" in x])
        self.assertNotIn("was retired", self.runners().stdout)


if __name__ == "__main__":
    sys.exit(unittest.main())
