"""T-1834: the library learns which playbooks earn their place. A task's close records the books it loaded with the
share of their steps it followed; fm playbooks coverage --unused names the books nobody used and the pairs that say
the same thing; a draft that repeats a book is refused; the skill list stays short and holds no playbook."""
import json
import os
import time
import unittest
from unittest import mock

from helpers import ForemanTestCase
from test_playbook_machinery import put

import fmcore as c
import fmplaybooks as pb

BODY = ("Use when the widget parser stalls on large inputs.\n\n## The procedure\n\n1. Profile the parser warmup.\n"
        "2. Check the cache invalidation keys.\n3. Measure the parser again after the change.\n")
PLUGIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


class Use(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.lib = os.path.join(self.tmp, "lib")
        put(self.lib, "references/fix/alpha.md", "# Alpha widget parser\n\n" + BODY)
        put(self.lib, "references/fix/alpha-copy.md", "# Alpha widget parser copy\n\n" + BODY + "4. Ship it quietly.\n")
        put(self.lib, "references/clean/gamma.md", "# Gamma tidy\n\nUse when code is messy.\n\n1. Remove dead imports "
            "from every touched module today.\n")
        put(self.lib, "references/perf/delta.md", "# Delta\n\nUse when queries crawl.\n\n1. Add the missing index "
            "to the slow table before anything else.\n")
        self.fm("init")
        self.p = c.find_project(self.repo)

    def run_fm(self, *words):
        return self.fm("playbooks", *words, check=False, env={"FOREMAN_PLAYBOOKS": self.lib})

    def event(self, target, ts=None):
        os.makedirs(c.state_dir(), exist_ok=True)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": c.iso(ts or time.time()), "kind": "tool", "tool": "Bash", "project": self.p.slug,
                                "session_id": "s", "target": target}) + "\n")

    def close(self, title, *steps):
        tid = json.loads(self.fm("task", "new", title, "--type", "FIX", "--tier", "S", "--ac", "fast :: true",
                                 *[x for s in steps for x in ("--step", s)], "--json").stdout)["id"]
        self.fm("focus", tid)
        return tid

    def done(self, tid, n):
        self.fm("task", "evidence", tid, "--step", "1", "--run", "true")
        self.fm("task", "step", tid, "done", "1")
        for k in range(2, n + 1):
            self.fm("task", "step", tid, "done", str(k), "--evidence", "x", "ok")
        self.fm("task", "ac", tid, "check", "1", "--evidence", "x", "ok")
        self.fm("task", "audit", tid, "self", "x", "ok")
        self.fm("task", "set", tid, "--section", "Regression test", "--text", "none: fixture")
        self.fm("task", "set", tid, "--section", "Lessons", "--text", "- Profile before you cache")
        self.fm("task", "done", tid, env={"FOREMAN_PLAYBOOKS": self.lib})

    def uses(self):
        return [e for e in c.ledger_events(self.p, ("playbook_use",))]

    def test_close_records_the_books_it_loaded_and_the_share_followed(self):
        self.event("fm playbooks show gamma")  # before the task: not its load
        time.sleep(1.1)
        tid = self.close("Fix the slow table", "check the missing index on the slow table")
        self.event("fm playbooks show perf/delta")
        self.event("fm playbooks show nosuch")
        self.done(tid, 1)
        got = self.uses()
        self.assertEqual(len(got), 1, got)
        self.assertEqual(got[0]["task"], tid)
        rows = got[0]["data"]["books"]
        self.assertEqual([r["playbook"] for r in rows], ["references/perf/delta.md"])
        self.assertEqual((rows[0]["followed"], rows[0]["steps"]), (1, 1))

    def test_a_close_reads_only_the_books_it_loaded(self):
        tid = self.close("Fix the slow table", "check the missing index on the slow table")
        self.event("fm playbooks show perf/delta")
        b = c.find_brief(self.p, tid)
        pb.followed(self.p, b, self.lib)  # cold: the word counts of the whole library, kept under the state dir
        reads = []
        real = pb._read
        with mock.patch.object(pb, "_read", lambda path, *a: (reads.append(os.path.basename(path)), real(path, *a))[1]):
            got = pb.followed(self.p, b, self.lib)
            self.assertEqual((reads, got[0]["followed"]), (["delta.md"], 1))
            put(self.lib, "references/clean/gamma.md", "# Gamma\n\nUse when x.\n\n1. Other.\n")  # a library edit
            reads.clear()
            pb.followed(self.p, b, self.lib)
        self.assertEqual(len(reads), 5, "a changed library counts its words again")

    def test_a_read_event_names_its_book_when_the_target_was_cut(self):
        os.makedirs(c.state_dir(), exist_ok=True)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": c.iso(time.time()), "kind": "tool", "tool": "Read", "project": "any",
                                "target": "/home/u/lanes/agent-1/plugin/skills/playbooks/refe", "book": "perf/delta"}) + "\n")
        self.assertEqual(pb.reach(self.lib, days=60)["read"], {"references/perf/delta.md": 1})

    def test_unused_reads_rotated_logs_and_says_when_the_log_is_short(self):
        logs = os.path.join(c.state_dir(), "logs")
        os.makedirs(logs)
        with open(os.path.join(logs, "events-20260101.jsonl"), "w", encoding="utf-8") as f:
            f.write(json.dumps({"ts": c.iso(time.time() - 30 * 86400), "kind": "tool", "tool": "Bash", "project": "x",
                                "session_id": "s", "target": "fm playbooks show delta"}) + "\n")
        self.event("fm playbooks show gamma", ts=time.time() - 86400)
        got = json.loads(self.run_fm("coverage", "--unused", "--json").stdout)
        self.assertNotIn("references/perf/delta.md", got["unused"])
        self.assertTrue(29 <= got["covers"] <= 31, got["covers"])
        self.assertIn("covers only", self.run_fm("coverage", "--unused").stdout)

    def test_a_book_route_text_named_is_not_unused(self):  # T-1833 x T-1834: a route TEXT hit counts as use
        with open(os.path.join(c.state_dir(), "events.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": c.iso(time.time()), "kind": "playbook", "action": "route",
                                "paths": ["references/perf/delta.md", "references/nope.md"]}) + "\n")
        self.assertNotIn("references/perf/delta.md", pb.unused(self.lib)[0])
        self.assertEqual(pb.reach(self.lib, days=60)["routed"], {"references/perf/delta.md": 1})

    def test_route_text_that_opens_with_a_stage_word_credits_no_stage(self):
        # T-1803 review: `route "performance of the login form"` read as the PERFORMANCE stage hid its unused books
        self.event('fm playbooks route "performance of the login form" -k 3')
        self.assertIn("references/perf/delta.md", pb.unused(self.lib)[0])
        self.event("fm playbooks route 'PERFORMANCE' -k 2; echo")  # a bare stage still credits its books
        self.assertNotIn("references/perf/delta.md", pb.unused(self.lib)[0])

    def test_a_window_under_a_day_is_refused(self):
        for days in ("0", "-5"):
            got = self.run_fm("coverage", "--unused", "--days", days)
            self.assertNotEqual(got.returncode, 0, days)
            self.assertIn("--days", got.stderr)

    def test_a_pair_sharing_several_title_words_is_compared_once(self):
        with mock.patch.object(pb, "overlap", wraps=pb.overlap) as m:
            got = pb.similar(self.lib)
        self.assertEqual(m.call_count, 1)
        self.assertEqual([(a, b) for a, b, _ in got], [("references/fix/alpha-copy.md", "references/fix/alpha.md")])

    def test_close_without_a_playbook_records_nothing(self):
        tid = self.close("Fix it", "profile the parser warmup")
        self.done(tid, 1)
        self.assertEqual(self.uses(), [])

    def test_unused_names_drop_and_merge_candidates(self):
        self.event("fm playbooks show alpha-copy")
        self.event("fm playbooks route CLEAN")
        self.event("fm playbooks show delta", ts=time.time() - 90 * 86400)  # outside the window
        got = json.loads(self.run_fm("coverage", "--unused", "--json").stdout)
        self.assertEqual(got["unused"], ["references/fix/alpha.md", "references/perf/delta.md"])
        self.assertEqual([(a, b) for a, b, _ in got["similar"]],
                         [("references/fix/alpha-copy.md", "references/fix/alpha.md")])
        self.assertGreaterEqual(got["similar"][0][2], 0.5)
        text = self.run_fm("coverage", "--unused").stdout
        self.assertIn("fix/alpha", text)
        self.assertIn("never deletes", text.lower())

    def test_followed_record_counts_as_use(self):
        tid = self.close("Fix the parser", "profile the parser warmup")
        self.event("fm playbooks show delta")
        self.done(tid, 1)  # delta is now read AND recorded; drop the read to prove the record alone counts
        open(os.path.join(c.state_dir(), "events.jsonl"), "w").close()
        got = json.loads(self.run_fm("coverage", "--unused", "--json").stdout)
        self.assertNotIn("references/perf/delta.md", got["unused"])

    def test_draft_that_repeats_a_book_is_refused_unless_forced(self):
        tid = self.close("Cache the parser", "measure the warmup", "add the cache")
        self.done(tid, 2)
        first = self.run_fm("draft", tid)
        self.assertEqual(first.returncode, 0, first.stderr)
        put(self.lib, "references/fix/copy.md", first.stdout)
        again = self.run_fm("draft", tid)
        self.assertEqual(again.returncode, 1)
        self.assertIn("references/fix/copy.md", again.stdout + again.stderr)
        self.assertNotIn("## Procedure", again.stdout)
        forced = self.run_fm("draft", tid, "--force")
        self.assertEqual(forced.returncode, 0)
        self.assertIn("## Procedure", forced.stdout)
        self.assertIn("references/fix/copy.md", forced.stderr)


class Cap(unittest.TestCase):
    def test_the_skill_list_is_short_and_holds_no_playbook(self):
        skills = os.path.join(PLUGIN, "skills")
        found = [os.path.join(d, "SKILL.md") for d, _, fs in os.walk(skills) if "SKILL.md" in fs]
        # T-2266: the user asked for many more skills within the listing budget (T-2072), so the budget is the
        # listing's characters (test_docs' 2,200 cap), not a count; playbooks still stay out of the list
        self.assertTrue(found)
        for f in found:
            self.assertNotIn(os.sep + "references" + os.sep, f, f"{f}: a playbook is not a skill")
        stems = {os.path.splitext(os.path.basename(b))[0] for b in pb._playbooks(pb.ROOT)}
        named = {os.path.basename(os.path.dirname(f)) for f in found} & stems
        self.assertFalse(named, f"skill and playbook share a name: {sorted(named)}")


if __name__ == "__main__":
    unittest.main()
