"""T-3573: ledger_events reads only the lines of the asked kinds through a per-file kind index, with the plain scan's output."""
import json
import os
from unittest import mock

from helpers import ForemanTestCase

from sampo import core as c

KINDS = ("focus", "task_done", "capture", "touched", "evidence")


class LedgerIndex(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.live = os.path.join(self.p.dir, "ledger.jsonl")
        self.small = mock.patch.object(c, "LEDGER_INDEX_MIN", 2048)  # index past 2 KB, so a test ledger gets one
        self.small.start()
        self.addCleanup(self.small.stop)

    def lines(self, day, n, start=0):
        out = []
        for i in range(start, start + n):
            kind = KINDS[i % len(KINDS)]
            data = {"i": i, "note": "touched" if i % 7 == 0 else "x"}  # a kind's name in the data: a false hit
            if i % 11 == 0:
                data["event"] = "focus"  # nested, never the line's own kind
            out.append(json.dumps({"ts": f"2026-{day}T{i // 3600 % 24:02d}:{i // 60 % 60:02d}:{i % 60:02d}Z",
                                   "task": f"T-{i % 9:04d}", "event": kind, "data": data}) + "\n")
            if i % 13 == 0:
                out.append("not json\n" if i % 2 else "[1, 2]\n")  # unreadable and non-dict lines are skipped
        return "".join(out)

    def write(self, path, text, mode="w"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, mode, encoding="utf-8") as f:
            f.write(text)

    def plain(self, kinds, since=""):
        with mock.patch.object(c, "LEDGER_INDEX_MIN", 1 << 60):  # never indexed: the scan every reader used before
            return c.ledger_events(self.p, kinds, since)

    def same(self, msg=""):
        for kinds in (("focus",), ("task_done", "capture"), KINDS, ("nothing_here",)):
            for since in ("", "2026-10-02", "2026-10-02T00:20", "2026-11-03T00:05", "2027"):
                want = self.plain(kinds, since)
                self.assertEqual(c.ledger_events(self.p, kinds, since), want, f"{msg} {kinds} {since!r}")
        self.assertEqual(c.ledger_events(self.p), self.plain(None), msg)

    def index_path(self, name="ledger.jsonl"):
        return os.path.join(self.p.dir, "cache", f"index-{name}.json")

    def test_indexed_reads_match_the_plain_scan_and_skip_other_lines(self):
        self.write(os.path.join(self.p.dir, "archive", "ledger-2026-10.jsonl"), self.lines("10-02", 900))
        self.write(self.live, self.lines("11-03", 900))
        self.same("fresh")
        self.assertTrue(os.path.exists(self.index_path()))
        self.assertTrue(os.path.exists(self.index_path("ledger-2026-10.jsonl")))
        real, parsed = json.loads, []
        with mock.patch.object(c.json, "loads", lambda raw, *a, **k: parsed.append(raw) or real(raw, *a, **k)):
            got = c.ledger_events(self.p, ("task_done",))
        lines = [r for r in parsed if b'"v":1' not in r]  # not the index files themselves
        self.assertEqual(len(lines), len(got), "only the asked kind's lines are parsed")

    def test_appended_lines_are_read_and_indexed_once_they_pass_the_threshold(self):
        self.write(self.live, self.lines("11-03", 400))
        self.same("built")
        before = os.path.getsize(self.live)
        self.write(self.live, self.lines("11-03", 3, start=400), "a")  # under the threshold: scanned, not indexed
        self.same("small tail")
        self.write(self.live, self.lines("11-03", 300, start=403), "a")
        self.same("big tail")
        with open(self.index_path(), encoding="utf-8") as f:
            self.assertGreater(json.load(f)["n"], before, "the index grew over the appended lines")

    def test_a_partial_last_line_is_read_like_the_plain_scan(self):
        self.write(self.live, self.lines("11-03", 400))
        self.same("built")
        self.write(self.live, self.lines("11-03", 30, start=400) + '{"ts": "2026-11-03T09:00:00Z", "event": "focus"', "a")
        self.same("cut short")
        self.write(self.live, ', "task": "T-0001"}\n', "a")
        self.same("completed")

    def test_a_rewritten_or_rolled_ledger_is_reindexed_never_served_stale(self):
        self.write(self.live, self.lines("11-03", 600))
        self.same("built")
        with open(self.live, "r+b") as f:  # fm tidy's roll: a prefix cut away in place, the same inode
            data = f.read()
            keep = data[len(data) // 3:]
            keep = keep[keep.index(b"\n") + 1:]
            f.seek(0)
            f.write(keep)
            f.truncate()
        self.same("rolled in place")
        self.write(self.live, self.lines("11-03", 300, start=5000), "a")
        self.same("rolled, then grown past the old size")
        c.write_atomic(self.live, self.lines("11-03", 500, start=9000))  # a new inode
        self.same("replaced")

    def test_a_corrupt_or_foreign_index_is_rebuilt(self):
        self.write(self.live, self.lines("11-03", 600))
        self.same("built")
        for bad in ("{", "[]", '{"v": 1}', json.dumps({"v": 1, "ino": 1, "n": 5, "head": "x", "last": "y", "k": {}}),
                    json.dumps({"v": 2}), '{"v": 1, "n": "x"}'):
            self.write(self.index_path(), bad)
            self.same(bad)
        with open(self.index_path(), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["v"], 1, "written again")
        with open(self.index_path(), encoding="utf-8") as f:  # a valid index whose kinds were tampered with
            d = json.load(f)
        d["ino"] += 1
        d["k"] = {"focus": [0]}
        self.write(self.index_path(), json.dumps(d))
        self.same("another file's index")

    def test_a_read_only_state_folder_still_reads(self):
        self.write(self.live, self.lines("11-03", 600))
        with mock.patch.object(c, "write_atomic", side_effect=OSError("read-only")):
            self.same("unsaved")
        self.assertFalse(os.path.exists(self.index_path()))
        os.makedirs(os.path.dirname(self.index_path()), exist_ok=True)
        dirs = (os.path.dirname(self.index_path()), self.p.dir)
        real, parsed = json.loads, []
        try:
            for d in dirs:
                os.chmod(d, 0o555)
            with mock.patch.object(c.json, "loads", lambda raw, *a, **k: parsed.append(raw) or real(raw, *a, **k)):
                got = c.ledger_events(self.p, ("task_done",))
        finally:
            for d in dirs:
                os.chmod(d, 0o755)
        self.assertEqual(got, self.plain(("task_done",)))
        self.assertLess(len(parsed), 300, "a folder that can't keep an index is byte-scanned, not parsed whole")

    def test_a_ledger_cut_under_the_index_is_scanned_instead(self):
        self.write(self.live, self.lines("11-03", 600))
        self.same("built")
        real = c._ledger_index

        def roll_now(p, f, name):  # fm tidy's roll lands after the index checked out, before its lines are read
            got = real(p, f, name)
            with open(self.live, "r+b") as g:
                data = g.read()
                g.seek(0)
                g.write(data[len(data) // 2:][data[len(data) // 2:].index(b"\n") + 1:])
                g.truncate()
            return got
        with mock.patch.object(c, "_ledger_index", roll_now):
            got = c.ledger_events(self.p, KINDS)
        self.assertEqual(got, self.plain(KINDS))

    def test_a_tail_of_some_kinds_matches_the_filtered_tail(self):
        self.write(self.live, self.lines("11-03", 900))
        for n in (1, 7, 100, 899, 5000):
            for kinds in (("focus",), ("task_done", "capture"), ("nothing_here",)):
                c._TAIL_MEMO.clear()
                want = [e for e in c.ledger_tail(self.p, n) if isinstance(e, dict) and e.get("event") in kinds]
                self.assertEqual(c.ledger_tail(self.p, n, kinds=kinds), want, (n, kinds))
