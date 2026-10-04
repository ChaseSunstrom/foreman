"""fm oracle (T-0226): behaviour examples and ambiguities from the request alone, written before the code is read, so
tests come from an independent spec instead of mirroring the implementation."""
import json
import os

from helpers import ForemanTestCase, read_text

STUB = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
stdin = sys.stdin.read()
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"args": args, "stdin": stdin, "cwd": os.getcwd()}) + "\n")
print("""## Examples
- GIVEN a CSV report WHEN exported THEN fields with commas are quoted
- GIVEN an empty report WHEN exported THEN only the header row is written
## Ambiguities
- Is the delimiter configurable? — fixed comma vs a --delimiter flag changes the CLI tests
Some closing prose that isn't a line item.""")
'''


class Oracle(ForemanTestCase):
    def setUp(self):
        super().setUp()
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "claude"), "w") as f:
            f.write(STUB)
        os.chmod(os.path.join(bindir, "claude"), 0o755)
        self.log = os.path.join(self.tmp, "stub.log")
        self.env = {"PATH": bindir + os.pathsep + os.environ["PATH"], "STUB_LOG": self.log}
        self.fm("init")
        with open(os.path.join(self.repo, "report.py"), "w") as f:
            f.write("IMPLEMENTATION_DETAIL = 'mirror me'\n")
        self.tid = json.loads(self.fm("task", "new", "Export the report as CSV", "--type", "FEATURE", "--tier", "M",
                                      "--ac", "the CSV opens in a spreadsheet :: true", "--step", "do it",
                                      "--json").stdout)["id"]
        self.fm("task", "set", self.tid, "--section", "Raw request", "--text", "> export the report as CSV")

    def test_examples_and_ambiguities_land_in_the_brief(self):
        out = self.fm("oracle", self.tid, env=self.env).stdout
        self.assertIn("1 ambiguit", out)
        brief = self.fm("task", "show", self.tid).stdout
        sec = brief.split("## Oracle\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("- GIVEN a CSV report WHEN exported THEN fields with commas are quoted", sec)
        self.assertIn("- Is the delimiter configurable?", sec)
        self.assertNotIn("closing prose", sec)

    def test_the_child_sees_the_spec_not_the_code(self):
        self.fm("oracle", self.tid, env=self.env)
        call = json.loads(read_text(self.log).splitlines()[0])
        self.assertIn("export the report as CSV", call["stdin"])
        self.assertIn("the CSV opens in a spreadsheet", call["stdin"])
        self.assertNotIn("mirror me", call["stdin"])
        self.assertEqual(call["args"][call["args"].index("--tools") + 1], "")
        self.assertNotEqual(os.path.realpath(call["cwd"]), os.path.realpath(self.repo), "not in the repo")
