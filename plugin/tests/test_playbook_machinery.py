"""T-1621: a playbook loaded with `fm playbooks show NAME` (how the playbooks skill reads one) has each {{fact}} filled
in from fm map's facts for the project it runs in, an unknown or empty fact left visible as {{fact?}}, and the
project's .foreman/playbooks/<stage>/<name>.md overlay after the shipped text under a 'This project' heading. An
overlay is plain markdown read from the repo itself: never through a link, and cut at a size."""
import json
import os
import subprocess
import time
import unittest

from helpers import ForemanTestCase

import fmcore as c
import fmplaybooks as pb

SHIPPED = ("# Alpha\n\nUse when the alpha widget misbehaves.\n\n## The procedure\n\n1. Run {{test}} first.\n"
           "2. Then {{nosuch}}; CI: {{ci}}.\n3. Leave {{ .GoFiles }}, {{.Name}}, ${{matrix}} and {{{raw}}} alone.\n")


def put(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


class Load(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.lib = os.path.join(self.tmp, "playbooks")
        put(self.lib, "references/fix/alpha.md", SHIPPED)
        put(self.lib, "references/ui/beta.md", "# Beta\n\nUse when beta.\n\n1. Go.\n")
        put(self.repo, "pyproject.toml", "[tool.pytest.ini_options]\n")
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "pytest"], check=True)
        self.fm("init")

    def show(self, *words, cwd=None):
        return self.fm("playbooks", "show", *words, check=False, cwd=cwd, env={"FOREMAN_PLAYBOOKS": self.lib})

    def test_overlay_follows_the_shipped_text_and_facts_resolve(self):
        put(self.repo, ".foreman/playbooks/fix/alpha.md", "Here {{test}} runs under xvfb.\n")
        r = self.show("fix/alpha")
        self.assertEqual(r.returncode, 0, r.stderr)
        shipped, heading, mine = r.stdout.partition("## This project")
        self.assertTrue(heading, r.stdout)
        self.assertIn("1. Run python3 -m pytest -q first.", shipped)
        self.assertIn("Then {{nosuch?}}; CI: {{ci?}}.", shipped)  # unknown, and known but empty here: both visible
        self.assertIn("Leave {{ .GoFiles }}, {{.Name}}, ${{matrix}} and {{{raw}}} alone.", shipped)  # not a fact
        self.assertIn(".foreman/playbooks/fix/alpha.md", mine.splitlines()[0])  # where to edit it
        self.assertIn("Here python3 -m pytest -q runs under xvfb.", mine)

    def test_no_overlay_no_heading(self):
        r = self.show("alpha")
        self.assertNotIn("This project", r.stdout)
        self.assertIn("python3 -m pytest -q", r.stdout)

    def test_json_names_the_playbook(self):
        got = json.loads(self.show("alpha", "--json").stdout)
        self.assertEqual(got["playbook"], "references/fix/alpha.md")
        self.assertIn("Run python3 -m pytest -q first.", got["text"])

    def test_names_resolve_by_path_stage_or_one_bare_name(self):
        for name in ("references/fix/alpha.md", "fix/alpha", "fix/alpha.md", "alpha"):
            self.assertIn("# Alpha", self.show(name).stdout, name)
        for name, why in (("gamma", "no playbook"), ("../../../etc/passwd", "no playbook"), ("", "no playbook")):
            r = self.show(name)
            self.assertNotEqual(r.returncode, 0, name)
            self.assertIn(why, r.stderr, name)
        put(self.lib, "references/ui/alpha.md", "# Alpha UI\n\nUse when.\n\n1. Go.\n")
        r = self.show("alpha")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("references/fix/alpha.md", r.stderr)
        self.assertIn("references/ui/alpha.md", r.stderr)

    def test_outside_a_project_facts_stay_unknown(self):
        bare = os.path.join(self.tmp, "bare")
        os.makedirs(bare)
        r = self.show("fix/alpha", cwd=bare)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("1. Run {{test?}} first.", r.stdout)

    def test_a_linked_overlay_or_folder_is_not_read(self):
        secret = put(self.tmp, "secret/fix/alpha.md", "TOKEN=hunter2\n")
        os.makedirs(os.path.join(self.repo, ".foreman/playbooks/fix"))
        os.symlink(secret, os.path.join(self.repo, ".foreman/playbooks/fix/alpha.md"))
        out = self.show("fix/alpha").stdout
        self.assertNotIn("hunter2", out)
        self.assertIn("not read", out)  # said, not silently skipped
        os.remove(os.path.join(self.repo, ".foreman/playbooks/fix/alpha.md"))
        os.rmdir(os.path.join(self.repo, ".foreman/playbooks/fix"))
        os.symlink(os.path.dirname(secret), os.path.join(self.repo, ".foreman/playbooks/fix"))
        out = self.show("fix/alpha").stdout
        self.assertNotIn("hunter2", out)
        self.assertIn("not read", out)

    def test_a_long_overlay_is_cut_and_says_so(self):
        put(self.repo, ".foreman/playbooks/fix/alpha.md", "x" * (pb.OVERLAY_MAX * 3))
        out = self.show("fix/alpha").stdout
        self.assertLess(len(out), pb.OVERLAY_MAX + len(SHIPPED) + 500)
        self.assertIn("cut at", out)

    def test_an_overlay_cannot_drive_the_terminal(self):
        put(self.repo, ".foreman/playbooks/fix/alpha.md", "a\x1b]0;owned\x07b\n")
        out = self.show("fix/alpha").stdout
        self.assertNotIn("\x1b", out)
        self.assertIn("a]0;ownedb", out)

    def test_facts_from_a_map(self):
        m = {"gates": ["fm doctor", "claude plugin test mods/x", "python3 plugin/tests/run.py"], "entry": ["bin/fm"],
             "lib_cards": [{"name": "python", "area": "lang"}, {"name": "flask", "area": "web"}], "ci": [],
             "layout": [["src/", 3], [".", 1]], "hot": ["src/a.py"], "lib": ["python", "flask"]}
        f = pb.facts(m)
        self.assertEqual(set(f), set(pb.FACTS))
        self.assertEqual(f["test"], "python3 plugin/tests/run.py")  # the runner, not the first gate saying test
        self.assertEqual((f["language"], f["entry"], f["layout"], f["cards"]), ("python", "bin/fm", "src/, .",
                                                                                 "python, flask"))
        self.assertEqual(pb.facts({"gates": ["fm doctor", "claude plugin test x"]})["test"], "claude plugin test x")
        self.assertEqual(pb.render("{{ci}} {{language}} {{test}}", f), "{{ci?}} python python3 plugin/tests/run.py")
        self.assertNotIn("\x1b", pb.facts({"gates": ["make test\x1b]0;x\x07"]})["test"])


class Count(ForemanTestCase):
    """A load through fm counts as a read, for fm check playbooks' reach report and fm usage."""
    def event(self, target, project="any"):
        os.makedirs(c.state_dir(), exist_ok=True)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": c.iso(time.time() - 3600), "kind": "tool", "tool": "Bash", "project": project,
                                "session_id": "s", "target": target}) + "\n")

    def test_reach_counts_a_show(self):
        lib = os.path.join(self.tmp, "playbooks")
        put(lib, "references/fix/alpha.md", SHIPPED)
        put(lib, "references/ui/beta.md", "# Beta\n")
        self.event("fm playbooks show alpha")
        self.event("fm playbooks show nosuch")
        self.assertEqual(pb.reach(lib, days=60)["read"], {"references/fix/alpha.md": 1})

    def test_usage_counts_a_show(self):
        self.fm("init")
        self.event("fm playbooks show verify/tdd-workflow", project=c.find_project(self.repo).slug)
        got = self.fm_json("usage")
        self.assertEqual(got["playbooks"].get("verify/tdd-workflow"), 1)
        self.assertEqual(got["commands"].get("playbooks"), 1)


class Lint(ForemanTestCase):
    def test_an_unknown_fact_in_a_shipped_playbook_is_a_finding(self):
        lib = os.path.join(self.tmp, "playbooks")
        put(lib, "references/fix/alpha.md", SHIPPED)
        got = pb.problems(lib, card_names=set(), run=False)
        self.assertTrue(any("{{nosuch}}" in x for x in got), got)
        self.assertFalse(any("{{test}}" in x or "{{ci}}" in x for x in got), got)


if __name__ == "__main__":
    unittest.main()
