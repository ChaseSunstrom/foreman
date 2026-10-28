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

    def test_real_task_titles_route_to_their_book(self):
        # T-1838: real task titles, verbatim (type, title, the books that fit) against the shipped library; tuned on the first 16,
        # the last 8 held out
        labelled = [
            ("FIX", "Flaky under load: test_code.Review.test_tool_results_and_the_journal_are_redacted and test",
             "fix/flaky-tests"),
            ("FIX", "Flaky under load: test_site_hero.Scene frame counts (133 != 198) and test_showpieces.CityB",
             "fix/flaky-tests"),
            ("FEATURE", "Profile fm ui gather (the pane polls it every 2 s) and memoize what's slow; skip if it's u",
             "perf/profiling"),
            ("FIX", "The hook benchmark judges by CPU time when the machine is busy, so load alone never fails the gate",
             "perf/benchmark-loop perf/latency-critical"),
            ("CLEAN", "CHANGELOG: Unreleased entries for the 2026-10-14 rounds (CC integration, compact output, fm page, review fixes)",
             "release/release-and-changelog"),
            ("FEATURE", "Dependency-install check in the guard: a new npm/pip/cargo package named in an install get",
             "release/dependency-admission"),
            ("FIX", "Compact output caps the saved full text (keeps head and tail, marks the cut) so a runaway output can't fill the disk",
             "context/context-budget"),
            ("FIX", "Fm edit silently drops a second <<< === >>> block written under the same @@ file header (o",
             "review/silent-failures"),
            ("FIX", "Fmsettings.set_key accepts an unknown key silently; only cmd_settings and apply check firs",
             "review/silent-failures"),
            ("FIX", "Stop hook still judges the turn when the project lock is busy",
             "review/silent-failures"),
            ("SECURITY", "fm approve-reads: exec-capable and abbreviated flags are not reads",
             "security/security-review review/security"),
            ("FIX", "Round-2 review fixes: lane rm keeps secrets inside build dirs, step pointer ignores extensionless names, broken pipe exits 141, tidy prune race-safe and keeps read marks, compact survives lone surrogates",
             "security/security-review review/security"),
            ("FEATURE", "foreman-ui motion setting: full (30 fps charts) · calm (8 fps, no blit) · off (still: no clocks, static glyphs)",
             "ui/motion ui/data-viz"),
            ("FEATURE", "Integrations desk card and animated SVG charts (T-1551 step 4): needs a decision on an HTT",
             "ui/data-viz"),
            ("FEATURE", "3D template: a zero-dependency single-file WebGL2 scene",
             "ui/scene-3d"),
            ("FEATURE", "Later from T-0760: Terminal UI polish: clickable ids, progress bar, spinner, motion, palet",
             "ui/terminal-ui"),
            ("PERFORMANCE", "Fm cost takes 6.8 s on the real state: fmcost._task_at is a linear scan per turn (11,993 c",
             "perf/profiling"),
            ("PERFORMANCE", "Bench_hooks.py has no 'bash <script>' payload: a PreToolUse slowdown from reading scripts",
             "perf/benchmark-loop perf/latency-critical"),
            ("FIX", "test_parallel mid-batch test waits for the slow session's pid instead of racing it",
             "fix/flaky-tests"),
            ("FIX", "fm code's write and edit keep a file's line endings and refuse a non-UTF-8 target; option-shaped paths are refused cleanly",
             "fix/text-time-bytes"),
            ("FEATURE", "Pane: no gaps, everything visual — sections sized to what they hold, the charts stretch to fill the dock exactly; Live shows tool lanes when quiet; every More line gets a bar or meter",
             "ui/data-viz"),
            ("FEATURE", "Test-first at edit time: the first edit of a non-test file in a FIX/FEATURE task with no t",
             "verify/tdd-workflow verify/tdd-guide"),
            ("FEATURE", "Static trigger eval: phrased requests per skill must match that skill's description best, with no tie",
             "evals/eval-harness"),
            ("FEATURE", "Knowledge out: lessons as native rules, decisions as ADRs, deferrals that wake when a file changes",
             "reflect/architecture-decision-records"),
        ]
        for _, _, want in labelled:  # a renamed or dropped book fails here, by name, not as a lower count
            for w in want.split():
                self.assertTrue(os.path.isfile(os.path.join(pb.ROOT, "references", w + ".md")), w)
        if pb.find("verify", 1, pb.ROOT)[0] != "fts5":
            self.skipTest("no FTS5: the scan fallback has no weights")
        # before the tuning: tuned 12 in the top 3 and 7 at the top, held out 3 and 0
        for part, (want3, want1) in ((labelled[:16], (13, 8)), (labelled[16:], (4, 1))):
            top1 = top3 = 0
            missed = []
            for kind, title, want in part:
                got = [x["path"][len("references/"):-3] for x in pb.find(title, 3, pb.ROOT, kind=kind)[1]]
                top1 += bool(got) and got[0] in want.split()
                hit = any(g in want.split() for g in got)
                top3 += hit
                missed += [] if hit else [f"{title[:40]} -> {got}"]
            self.assertTrue(top3 >= want3 and top1 >= want1,
                            f"{top3} of {len(part)} in the top 3, {top1} at the top; missed: {missed}")

    def test_a_task_type_prefers_its_folder(self):  # T-1838
        put(self.root, "references/perf/kiln.md", "Kiln", "Use when the kiln heats slowly.")
        put(self.root, "references/ui/kiln.md", "Kiln", "Use when the kiln heats slowly.")
        for i in range(3):  # bm25 is 0 for a word in half the books or more
            put(self.root, f"references/ui/other{i}.md", "Other", "Use when the widget misbehaves.")
        same = pb.find("slowly heating kiln", 2, self.root)[1]
        self.assertEqual(same[0]["score"], same[1]["score"], "the same book in two folders")
        got = pb.find("slowly heating kiln", 2, self.root, kind="PERFORMANCE")[1]
        self.assertEqual(got[0]["path"], "references/perf/kiln.md")
        self.assertGreater(got[0]["score"], got[1]["score"])
        self.assertEqual(pb.find("slowly heating kiln", 2, self.root, kind="FEATURE")[1][0]["score"], got[1]["score"],
                         "a type with no folder boosts nothing")

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

    def test_a_task_of_a_hand_edited_lowercase_type_prefers_its_folder(self):  # T-1838 review
        put(self.lib, "references/perf/kumquat.md", "Kumquat", "Use when kumquat harvesting stalls.")
        for i in range(2):  # kumquat in under half the books: bm25 above 0
            put(self.lib, f"references/ui/filler{i}.md", "Filler", "Use when the widget misbehaves.")
        out = self.fm("task", "new", "Kumquat harvesting stalls", "--type", "PERFORMANCE", "--tier", "S",
                      "--ac", "it runs :: true", "--step", "look").stdout
        tid = next(w for w in out.split() if w.startswith("T-")).rstrip(":.,")
        [brief] = [os.path.join(d, f) for d, _, fs in os.walk(self.home) for f in fs
                   if f.startswith(tid + "-") and f.endswith(".md")]
        with open(brief) as f:
            text = f.read()
        with open(brief, "w") as f:
            f.write(text.replace("type: PERFORMANCE", "type: performance", 1))
        got = json.loads(self.route("--task", tid, "--json").stdout)["playbooks"]
        self.assertEqual(got[0]["path"], "references/perf/kumquat.md")
        self.assertGreater(got[0]["score"], got[1]["score"], "the same book in fix/ scores lower")

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

    def test_a_busy_machine_widens_the_warm_route_cpu_limit(self):  # T-1836: a parallel suite's load is no regression
        self.assertEqual([bench.route_cpu_limit(x) for x in (0.0, 0.5, 0.51, 3.0)], [50, 50, 75, 75])
        with mock.patch.object(bench, "load_per_core", return_value=2.0):
            r = bench.run(300, runs=3)
        self.assertEqual((r["load"], r["route_cpu_limit_ms"]), (2.0, 75))


if __name__ == "__main__":
    unittest.main()
