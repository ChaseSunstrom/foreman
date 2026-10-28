"""T-1833: fm playbooks route TEXT|--task ID ranks the library by relevance over an incremental FTS5 index kept in
Foreman's state (never the plugin tree); a stage key routes as before; without FTS5 a title/use-line scan answers."""
import json
import os
import shutil
import sqlite3
import subprocess
import time
import unittest
from unittest import mock

from helpers import ForemanTestCase

import bench_playbooks as bench
import fmcore as c
import fmplaybooks as pb


def put(root, rel, title, use, body="1. Do the thing.\n"):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{use}\n\n## The procedure\n\n{body}")
    return path


class Rank(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.root = os.path.join(self.tmp, "playbooks")
        os.environ["FOREMAN_STATE"] = os.path.join(self.tmp, "state")

    def top(self, text, k=5):
        return [x["path"] for x in pb.find(text, k, self.root)[1]]

    def test_each_planted_book_is_top_one_in_a_2k_library(self):
        asked = bench.make_library(self.root, 2000, planted=40)
        self.assertEqual(len(asked), 40)
        mode, _ = pb.find(next(iter(asked)), 5, self.root)
        self.assertEqual(mode, "fts5")
        for query, want in asked.items():
            self.assertEqual(self.top(query)[:1], [want], query)

    def test_an_added_edited_and_removed_book_shows_in_the_next_call(self):
        put(self.root, "references/fix/alpha.md", "Alpha", "Use when the alpha widget misbehaves.")
        self.assertEqual(self.top("trouble with kumquat harvesting"), [])
        beta = put(self.root, "references/fix/beta.md", "Beta", "Use when kumquat harvesting stalls.")
        self.assertEqual(self.top("trouble with kumquat harvesting"), ["references/fix/beta.md"])
        with open(beta, "w", encoding="utf-8") as f:
            f.write("# Beta\n\nUse when pomelo canning stalls.\n\n1. Go.\n")
        os.utime(beta, ns=(time.time_ns() + 10**9,) * 2)  # same size, a later mtime
        self.assertEqual(self.top("trouble with kumquat harvesting"), [])
        self.assertEqual(self.top("pomelo canning"), ["references/fix/beta.md"])
        os.remove(beta)
        self.assertEqual(self.top("pomelo canning"), [])

    def test_a_renamed_or_swapped_book_shows_in_the_next_call(self):  # the same count, mtimes and sizes
        a = put(self.root, "references/fix/alpha.md", "Alpha", "Use when kumquat harvesting stalls.")
        put(self.root, "references/fix/beta.md", "Beta", "Use when pomelo canning stalls.")
        self.assertEqual(self.top("kumquat harvesting"), ["references/fix/alpha.md"])
        os.rename(a, os.path.join(self.root, "references/fix/gamma.md"))
        self.assertEqual(self.top("kumquat harvesting"), ["references/fix/gamma.md"])
        os.makedirs(os.path.join(self.root, "references/ui"))
        os.rename(os.path.join(self.root, "references/fix/gamma.md"), os.path.join(self.root, "references/ui/gamma.md"))
        self.assertEqual(self.top("kumquat harvesting"), ["references/ui/gamma.md"])

    def test_the_index_lives_in_state_not_in_the_library(self):
        put(self.root, "references/fix/alpha.md", "Alpha", "Use when the alpha widget misbehaves.")
        self.top("alpha widget")
        self.assertEqual([n for _, _, fs in os.walk(self.root) for n in fs], ["alpha.md"])
        self.assertTrue(any(f.endswith(".db") for _, _, fs in os.walk(os.environ["FOREMAN_STATE"]) for f in fs))

    def test_indexes_and_templates_are_not_routed(self):
        put(self.root, "references/ui/INDEX.md", "UI", "Use when kumquat screens ship.")
        put(self.root, "references/ui/templates/DESIGN.md", "DESIGN", "Use when kumquat screens ship.")
        put(self.root, "references/ui/real.md", "Real", "Use when kumquat screens ship.")
        self.assertEqual(self.top("kumquat screens"), ["references/ui/real.md"])

    def test_without_fts5_a_title_and_use_line_scan_answers(self):
        put(self.root, "references/fix/alpha.md", "Alpha", "Use when the alpha widget misbehaves.")
        put(self.root, "references/fix/beta.md", "Beta kumquat", "Use when the beta widget stalls.")
        put(self.root, "references/fix/gamma.md", "Gamma", "Use when kumquat harvesting stalls.")
        with mock.patch.object(pb, "_fts_find", side_effect=sqlite3.OperationalError("no such module: fts5")):
            mode, got = pb.find("kumquat harvesting", 5, self.root)
        self.assertEqual(mode, "scan")
        self.assertEqual([x["path"] for x in got], ["references/fix/gamma.md", "references/fix/beta.md"])

    def test_a_broken_index_file_is_rebuilt(self):
        put(self.root, "references/fix/alpha.md", "Alpha", "Use when the alpha widget misbehaves.")
        self.top("alpha widget")
        for d, _, fs in os.walk(os.environ["FOREMAN_STATE"]):
            for f in fs:
                if f.endswith(".db"):
                    with open(os.path.join(d, f), "wb") as h:
                        h.write(b"not a database" * 100)
        self.assertEqual(self.top("alpha widget"), ["references/fix/alpha.md"])

    def dbs(self):
        return [os.path.join(d, f) for d, _, fs in os.walk(os.environ["FOREMAN_STATE"]) for f in fs if f.endswith(".db")]

    def test_a_corrupt_fts_table_is_rebuilt_not_scanned_forever(self):  # the signature still matches
        put(self.root, "references/fix/alpha.md", "Alpha", "Use when the alpha widget misbehaves.")
        put(self.root, "references/fix/beta.md", "Beta", "Use when the beta widget misbehaves.")
        self.assertEqual(pb.find("alpha widget", 5, self.root)[0], "fts5")
        [db] = self.dbs()
        with open(db + "-journal", "wb") as f:
            f.write(b"stale")
        con = sqlite3.connect(db)
        con.execute("update books_data set block=x'0102030405060708' where id>1")
        con.execute("update books_idx set segid=segid+7")
        con.commit()
        con.close()
        mode, got = pb.find("alpha widget", 5, self.root)
        self.assertEqual((mode, got[0]["path"]), ("fts5", "references/fix/alpha.md"))
        self.assertEqual(pb.find("beta widget", 5, self.root)[0], "fts5")  # healthy since: no scan on every call
        self.assertFalse(os.path.exists(db + "-journal"))

    def test_an_index_of_a_library_that_is_gone_is_dropped_when_another_is_built(self):
        old = os.path.join(self.tmp, "cache-1.0")
        put(old, "references/fix/alpha.md", "Alpha", "Use when the alpha widget misbehaves.")
        pb.find("alpha widget", 5, old)
        self.assertEqual(len(self.dbs()), 1)
        keep = os.path.join(self.tmp, "other")
        put(keep, "references/fix/beta.md", "Beta", "Use when the beta widget misbehaves.")
        pb.find("beta widget", 5, keep)
        self.assertEqual(len(self.dbs()), 2)  # both libraries exist: both kept
        shutil.rmtree(old)
        put(self.root, "references/fix/gamma.md", "Gamma", "Use when the gamma widget misbehaves.")
        pb.find("gamma widget", 5, self.root)
        self.assertEqual(len(self.dbs()), 2)  # old's index is gone, the new one is in

    def test_the_routed_books_are_the_ones_the_lint_walks(self):
        put(self.root, "references/fix/alpha.md", "Alpha", "Use when kumquat.")
        put(self.root, "references/ui/INDEX.md", "UI", "Use when kumquat.")
        put(self.root, "references/ui/templates/DESIGN.md", "D", "Use when kumquat.")
        put(self.root, "references/ui/deep/er/beta.md", "Beta", "Use when kumquat.")
        put(self.root, "elsewhere/gamma.md", "Gamma", "Use when kumquat.")
        with open(os.path.join(self.root, "references/ui/notes.txt"), "w") as f:
            f.write("x")
        os.symlink(os.path.join(self.root, "references/fix/alpha.md"), os.path.join(self.root, "references/fix/link.md"))
        os.symlink(os.path.join(self.root, "references/ui"), os.path.join(self.root, "references/dirlink"))
        os.mkfifo(os.path.join(self.root, "references/fix/pipe.md"))  # the walk lists it; reading it would block
        want = set(pb._playbooks(self.root)) - {"references/fix/pipe.md"}
        self.assertEqual({rel for rel, *_ in pb._stat_tree(self.root)}, want)
        self.assertEqual(set(self.top("kumquat", 50)), want)

    def test_query_syntax_in_the_text_is_only_words(self):
        put(self.root, "references/fix/alpha.md", "Alpha", "Use when the alpha widget misbehaves.")
        for text in ('"alpha" OR NEAR(widget', "alpha* AND - widget:", "(((", "", "a b c", "alpha\x00widget"):
            self.top(text)  # none raises
        self.assertEqual(self.top('"alpha" OR NEAR(widget'), ["references/fix/alpha.md"])

    def test_a_long_text_and_k_are_bounded(self):
        for i in range(8):
            put(self.root, f"references/fix/b{i}.md", f"Book {i}", "Use when kumquat harvesting stalls.")
        self.assertEqual(len(self.top("kumquat harvesting " + "wordy " * 5000)), 5)
        self.assertEqual(len(self.top("kumquat harvesting", 2)), 2)


class Cli(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.lib = os.path.join(self.tmp, "playbooks")
        put(self.lib, "references/fix/kumquat.md", "Kumquat", "Use when kumquat harvesting stalls.")
        put(self.lib, "references/fix/other.md", "Other", "Use when the other widget misbehaves.")
        put(self.lib, "references/fix/third.md", "Third", "Use when the third widget misbehaves.")  # bm25 of a term in
        self.fm("init")  # half the books is 0: three books give a score above it

    def route(self, *words, check=True):
        return self.fm("playbooks", "route", *words, check=check, env={"FOREMAN_PLAYBOOKS": self.lib})

    def test_text_prints_score_and_use_line(self):
        r = self.route("kumquat harvesting")
        self.assertIn("references/fix/kumquat.md", r.stdout)
        self.assertIn("Use when kumquat harvesting stalls.", r.stdout)
        self.assertNotIn("other.md", r.stdout)
        got = json.loads(self.route("kumquat harvesting", "--json").stdout)
        self.assertEqual(got["playbooks"][0]["path"], "references/fix/kumquat.md")
        self.assertGreater(got["playbooks"][0]["score"], 0)

    def test_a_stage_key_keeps_todays_answer(self):
        r = self.route("verifying")
        self.assertIn("verifying", r.stdout)
        self.assertNotIn("kumquat", r.stdout)

    def test_a_task_routes_by_its_title_interpretation_and_criteria(self):
        out = self.fm("task", "new", "Stalled harvesting", "--type", "FIX", "--tier", "S",
                      "--ac", "kumquat harvesting runs again :: true", "--step", "look").stdout
        tid = next(w for w in out.split() if w.startswith("T-")).rstrip(":.,")
        r = self.route("--task", tid)
        self.assertIn("references/fix/kumquat.md", r.stdout)
        self.assertNotIn("other.md", r.stdout)
        self.assertNotEqual(self.route("--task", "T-9999", check=False).returncode, 0)

    def test_a_route_is_one_event_reach_counts(self):
        self.route("kumquat harvesting")
        with open(os.path.join(c.state_dir(), "events.jsonl"), encoding="utf-8") as f:
            events = [json.loads(x) for x in f]
        got = [e for e in events if e.get("kind") == "playbook"]
        self.assertEqual(len(got), 1, events)
        self.assertEqual(got[0]["action"], "route")
        self.assertEqual(got[0]["paths"], ["references/fix/kumquat.md"])
        self.assertNotIn("harvesting", json.dumps(got[0]))  # the text stays out of the log
        got = pb.reach(self.lib)
        self.assertEqual(got["routed"], {"references/fix/kumquat.md": 1})
        self.assertNotIn("references/fix/kumquat.md", got["read"])  # named by a ranking is not read
        self.assertIn("references/fix/kumquat.md", got["unread"])

    def test_one_word_that_is_no_stage_and_fits_nothing_is_a_usage_error(self):
        r = self.route("verifing", check=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("verifying", r.stderr)  # the stages it knows
        self.assertEqual(self.route("kumquat").returncode, 0)  # one word that fits is a query

    def test_k_limits_the_list(self):
        for i in range(4):
            put(self.lib, f"references/fix/more{i}.md", f"More {i}", "Use when kumquat harvesting stalls.")
        got = json.loads(self.route("kumquat harvesting", "-k", "2", "--json").stdout)
        self.assertEqual(len(got["playbooks"]), 2)

    def test_nothing_fits_says_so(self):
        r = self.route("zzzzzz yyyyyy")
        self.assertEqual(r.returncode, 0)
        self.assertIn("no playbook", r.stdout)


if __name__ == "__main__":
    unittest.main()
