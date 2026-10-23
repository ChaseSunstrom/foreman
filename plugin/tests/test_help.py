"""T-0094: fm help lists every command once, in tiers (the everyday ones first); fm alone prints it."""
import argparse
import re
import os
import sys
import unittest

from helpers import ForemanTestCase

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))


class Help(ForemanTestCase):
    def test_every_command_once_in_tiers_everyday_first(self):
        import fmcli
        sub = next(a for a in fmcli.build_parser()._actions if isinstance(a, argparse._SubParsersAction))
        out = self.fm("help").stdout
        lines = [ln.split()[0] for ln in out.splitlines() if ln.startswith("  ")]
        self.assertEqual(sorted(lines), sorted(sub.choices), "every command, each once (a new one needs a tier)")
        self.assertTrue(out.startswith("Every task"), out[:80])
        self.assertLess(out.index("  next "), out.index("  sentinel "))
        self.assertEqual(self.fm().stdout, out, "fm alone prints it")

    def test_tiers_come_from_registrations(self):
        # T-1144: each command declares its tier where it is registered; no shared table to conflict on
        import fmcli
        sub = next(a for a in fmcli.build_parser()._actions if isinstance(a, argparse._SubParsersAction))
        listed = [w for _, names in fmcli.HELP_TIERS for w in names.split()]
        self.assertEqual(sorted(listed), sorted(sub.choices))
        self.assertEqual([t for t, _ in fmcli.HELP_TIERS][0], "Every task")
        src = open(os.path.join(os.path.dirname(__file__), "..", "lib", "fmcli.py")).read()
        self.assertNotIn('("Every task", "next', src, "no hand-kept name list")

    def test_each_command_has_its_own_help_position(self):
        # T-1686: img, shot and critique all took 93; a tie silently falls back to registration order. One position per
        # registration site: the instruments loop (fminstr.TOOLS) is one site, its tools in the registry's order
        import fmcli
        import fminstr
        sub = next(a for a in fmcli.build_parser()._actions if isinstance(a, argparse._SubParsersAction))
        with open(os.path.join(os.path.dirname(__file__), "..", "lib", "fmcli.py"), encoding="utf-8") as f:
            sites = re.findall(r'\btier=\("[^"]+", (\d+)\)', f.read())
        commands = len({id(p) for p in sub.choices.values()})  # an alias (status) is its command's parser
        self.assertEqual(len(sites), commands - len(fminstr.TOOLS) + 1, "every registration site read")
        self.assertEqual(sorted({p for p in sites if sites.count(p) > 1}, key=int), [], "positions shared")

    def test_help_text_carries_no_ticket_ids(self):
        # T-0873 (round 4): "(T-0594)" in help reads as noise to anyone who isn't Foreman's maintainer
        import fmcli
        sub = next(a for a in fmcli.build_parser()._actions if isinstance(a, argparse._SubParsersAction))
        texts = {"fm help --all": self.fm("help", "--all").stdout, "fm --help": self.fm("--help").stdout}
        texts.update({f"fm {name} -h": p.format_help() for name, p in sub.choices.items()})
        leaks = {where: re.findall(r"\bT-\d{3,4}\b", t) for where, t in texts.items() if re.search(r"\bT-\d{3,4}\b", t)}
        self.assertEqual(leaks, {})

    def test_status_is_state(self):
        # T-0393: "status" is the word the rules and /foreman:status use; `fm status` was an invalid choice
        self.fm("init")
        self.fm("capture", "something")  # T-0847: an empty project's status is one line on how to start
        p = self.fm("status", check=False)
        self.assertEqual(p.returncode, 0, p.stderr[-300:])
        stamp = lambda t: re.sub(r"_Generated \S+", "", t)  # noqa: E731 — the two calls may straddle a second
        self.assertEqual(stamp(p.stdout), stamp(self.fm("state").stdout))


if __name__ == "__main__":
    unittest.main()
