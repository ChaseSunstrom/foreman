"""T-1505: fm check playbooks lints the playbook library: every file is in SKILL.md or its stage INDEX.md and every
listed path exists, SKILL.md stays in its budget, no two playbooks share a title or most of their text, each has a
Use-when line and a numbered procedure, none grew past its recorded size, every `fm lib show NAME` is a card, and every
python block not marked no-run runs; a reach report names the playbooks nobody read lately."""
import json
import os
import time
import unittest

from helpers import ForemanTestCase

import fmcore as c
import fmplaybooks as pb

CARDS = {"real-card", "three-js", "web/three-js"}  # as fmplaybooks._cards() lists them: name and dir/name


def book(title, use="Use when the alpha widget misbehaves under load.", steps="1. Measure it.\n2. Fix it.\n",
         extra=""):
    return f"# {title}\n\n{use}\n\n## The procedure\n\n{steps}\n{extra}"


class Fixture(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.root = os.path.join(self.tmp, "playbooks")
        self.write("references/fix/alpha.md", book("Alpha"))
        self.write("references/ui/INDEX.md", "# UI\n\n- `references/ui/beta.md` — beta.\n")
        self.write("references/ui/beta.md", book(
            "Beta", "Use before a gamma screen ships to the store.",
            "1. Sketch the screen on paper first.\n2. Count every tap a person needs.\n"))
        self.write("SKILL.md", "---\nname: playbooks\n---\n\n- `references/fix/alpha.md` — alpha.\n"
                               "- `references/ui/INDEX.md` — the UI index.\n")

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def problems(self, **kw):
        return pb.problems(self.root, card_names=CARDS, **kw)

    def assertFlags(self, needle, **kw):
        got = self.problems(**kw)
        self.assertTrue(any(needle in x for x in got), f"{needle!r} not in {got}")
        return got


class Index(Fixture):
    def test_the_fixture_is_clean(self):
        self.assertEqual(self.problems(), [])

    def test_an_unlisted_file(self):
        self.write("references/fix/stray.md", book("Stray", "Use when a stray file turns up in a review."))
        self.assertFlags("references/fix/stray.md: in no index")

    def test_a_file_in_an_unnamed_stage_index_is_unlisted(self):
        self.write("SKILL.md", "---\nname: playbooks\n---\n\n- `references/fix/alpha.md` — alpha.\n")
        got = self.assertFlags("references/ui/beta.md: in no index")
        self.assertTrue(any("references/ui/INDEX.md: in no index" in x for x in got), got)

    def test_a_dead_index_line(self):
        self.write("references/ui/INDEX.md", "# UI\n\n- `references/ui/beta.md` — beta.\n"
                                             "- `references/ui/gone.md` — gone.\n")
        self.assertFlags("references/ui/INDEX.md:4: references/ui/gone.md doesn't exist")

    def test_skill_md_over_its_budget(self):
        import fmdoctor
        with open(os.path.join(self.root, "SKILL.md"), "a", encoding="utf-8") as f:
            f.write("x" * fmdoctor.SKILL_MAX)
        self.assertFlags(f"over its {fmdoctor.SKILL_MAX:,}-character budget")


class Duplicates(Fixture):
    def test_a_shared_title(self):
        self.write("references/fix/alpha2.md", book("alpha", "Use when nothing else in this file is alike at all.",
                                                    "1. Totally different words appear here.\n"))
        self.write("SKILL.md", self.read("SKILL.md") + "- `references/fix/alpha2.md` — again.\n")
        self.assertFlags("same title as references/fix/alpha.md")

    def test_untitled_playbooks_never_share_a_title(self):  # ported reviewers have no '# ' heading: review/cpp.md
        self.write("references/fix/cpp.md", "Use when C++ changes land in a fix.\n\n1. Read the diff first.\n")
        self.write("references/ui/cpp.md", "Use for C++ widgets in a native toolkit.\n\n1. Build the demo app.\n")
        self.write("SKILL.md", self.read("SKILL.md") + "- `references/fix/cpp.md` — cpp.\n")
        self.write("references/ui/INDEX.md", self.read("references/ui/INDEX.md") + "- `references/ui/cpp.md` — c.\n")
        self.assertEqual(self.problems(), [])

    def test_a_near_duplicate(self):
        body = " ".join(f"word{i}" for i in range(300))
        self.write("references/fix/alpha.md", book("Alpha", extra=body))
        self.write("references/fix/copy.md", book("Copy", extra=body + " and one more line at the end"))
        self.write("SKILL.md", self.read("SKILL.md") + "- `references/fix/copy.md` — copy.\n")
        self.assertFlags("references/fix/copy.md: shares")

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as f:
            return f.read()


class Shape(Fixture):
    def test_no_use_when_line(self):
        self.write("references/fix/alpha.md", book("Alpha", "A playbook about alpha things."))
        self.assertFlags("references/fix/alpha.md: no Use-when line")

    def test_no_numbered_procedure(self):
        self.write("references/fix/alpha.md", book("Alpha", steps="- Measure it.\n- Fix it.\n"))
        self.assertFlags("references/fix/alpha.md: no numbered procedure")

    def test_a_numbered_line_inside_a_fence_is_no_procedure(self):
        self.write("references/fix/alpha.md", book("Alpha", steps="```text\n1. Measure it.\n```\n"))
        self.assertFlags("no numbered procedure")

    def test_card_names_resolve(self):
        self.write("references/fix/alpha.md", book("Alpha", extra="Cards: `fm lib show real-card`, "
                                                   "`fm lib show web/three-js`, `fm lib show look-NAME`, "
                                                   "then fm lib show three-js.\n"))
        self.assertEqual(self.problems(), [])
        self.write("references/fix/alpha.md", book("Alpha", extra="See `fm lib show no-such-card`.\n"))
        self.assertFlags("references/fix/alpha.md:10: fm lib show no-such-card: no such card")


class Ratchet(Fixture):
    def test_over_its_ratchet_until_recorded(self):
        pb.ratchet(self.root)
        self.assertEqual(self.problems(), [])
        self.write("references/fix/alpha.md", book("Alpha", extra="A new paragraph that adds tokens. " * 10))
        self.assertFlags("references/fix/alpha.md: grew")
        pb.ratchet(self.root)
        self.assertEqual(self.problems(), [])

    def test_a_new_playbook_needs_no_record(self):
        pb.ratchet(self.root)
        self.write("references/fix/fresh.md", book("Fresh", "Use when a fresh lane adds a playbook later on.",
                                                   "1. Write it down plainly.\n"))
        self.write("SKILL.md", self.read_skill() + "- `references/fix/fresh.md` — fresh.\n")
        self.assertEqual(self.problems(), [])

    def test_a_record_that_isnt_json_is_a_problem_not_a_crash(self):
        self.write(pb.RATCHET, "{nope")
        self.assertFlags(pb.RATCHET)

    def read_skill(self):
        with open(os.path.join(self.root, "SKILL.md"), encoding="utf-8") as f:
            return f.read()


class Snippets(Fixture):
    def snippet(self, code, info="python"):
        self.write("references/fix/alpha.md", book("Alpha", extra=f"\n```{info}\n{code}\n```\n"))

    def test_a_passing_block_runs_isolated_in_an_empty_folder(self):
        self.snippet("import os, sys\nassert sys.flags.isolated\nassert os.listdir('.') == [], os.listdir('.')\n"
                     "assert sys.stdin.read() == ''\nassert 'FOREMAN_HOME' not in os.environ, sorted(os.environ)")
        self.assertEqual(self.problems(), [])

    def test_a_failing_block_names_path_and_line(self):
        self.snippet("raise SystemExit(3)")
        self.assertFlags("references/fix/alpha.md:11: python block exited 3")

    def test_a_block_marked_no_run_is_skipped(self):
        self.snippet("raise SystemExit(3)", info="python no-run")
        self.assertEqual(self.problems(), [])

    def child(self, then):
        self.pidfile = os.path.join(self.tmp, "child.pid")
        self.snippet("import subprocess, time\n"
                     f"p = subprocess.Popen(['sleep', '30'])\nopen({self.pidfile!r}, 'w').write(str(p.pid))\n" + then)

    def assertChildGone(self):
        with open(self.pidfile) as f:
            pid = int(f.read())
        for _ in range(50):
            try:
                os.kill(pid, 0)
                with open(f"/proc/{pid}/stat") as f:
                    if f.read().split()[2] == "Z":
                        return  # killed, waiting for init to reap it
            except (ProcessLookupError, FileNotFoundError):
                return
            time.sleep(0.1)
        self.fail(f"the snippet's child {pid} outlived the check")

    def test_a_timeout_fails_and_kills_the_process_group(self):
        self.child("time.sleep(30)")
        t0 = time.time()
        self.assertFlags("timed out after 2 s", timeout=2)
        self.assertLess(time.time() - t0, 15)
        self.assertChildGone()

    def test_a_child_left_running_by_a_passing_block_is_killed(self):
        self.child("")
        self.assertEqual(self.problems(), [])
        self.assertChildGone()


class Reach(Fixture):
    def event(self, rel, days_ago):
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": c.iso(time.time() - days_ago * 86400), "kind": "tool", "tool": "Read",
                                "project": "any", "target": f"/x/skills/playbooks/{rel}"}) + "\n")

    def test_names_the_playbooks_no_one_read_in_the_window(self):
        os.makedirs(c.state_dir(), exist_ok=True)
        self.event("references/fix/alpha.md", 3)
        self.event("references/ui/beta.md", 90)
        got = pb.reach(self.root, days=60)
        self.assertEqual(got["unread"], ["references/ui/beta.md"])
        self.assertEqual(got["read"], {"references/fix/alpha.md": 1})

    def test_a_truncated_target_still_counts(self):
        os.makedirs(c.state_dir(), exist_ok=True)
        self.event("references/ui/be", 1)  # fmhooks keeps 120 characters of a target
        self.assertEqual(pb.reach(self.root, days=60)["read"], {"references/ui/beta.md": 1})


class Repo(ForemanTestCase):
    def test_the_repos_own_playbooks_pass(self):
        r = self.fm("check", "playbooks", check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("unread in", r.stdout)


if __name__ == "__main__":
    unittest.main()
