"""SECURITY T-1065: each ledger line carries the hash of the one before (prev); fm verify-ledger proves no chained line
was edited or removed; fm task finish's receipt names the chain head; the chain survives fm tidy's monthly roll."""
import hashlib
import json
import os
import re
import threading
from unittest import mock

from helpers import ForemanTestCase, read_text

import fmcore as c
import fmtidy


def h(raw):
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class Chain(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        self.ledger = os.path.join(self.p.dir, "ledger.jsonl")

    def lines(self):
        return read_text(self.ledger).splitlines()

    def put(self, lines):
        with open(self.ledger, "w", encoding="utf-8") as f:
            f.write("".join(x + "\n" for x in lines))

    def verify(self, *args):
        return self.fm("verify-ledger", *args, check=False)

    def test_untouched_ledger_verifies(self):
        for i in range(5):
            c.log_event(self.p, "note", data={"i": i})
        lines = self.lines()
        self.assertTrue(all(json.loads(x).get("prev") for x in lines), "every line fm writes is chained")
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(h(lines[-1]), r.stdout, "OK names the head: the hash of the last line")
        self.assertIn("only with --head", r.stdout, "OK says the last line's edit needs the receipt's head")

    def test_broken_chain_has_no_head(self):
        for i in range(3):
            c.log_event(self.p, "note", data={"i": i})
        lines = self.lines()
        lines[1] = lines[1].replace('"event": "', '"event": "x', 1)
        self.put(lines)
        r = self.verify("--json")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIsNone(json.loads(r.stdout)["head"], "a broken chain has no head, not the genesis hash")

    def archive_unreadable(self):
        if os.geteuid() == 0:
            self.skipTest("root reads a mode-000 file")
        os.makedirs(os.path.join(self.p.dir, "archive"), exist_ok=True)
        path = os.path.join(self.p.dir, "archive", "ledger-2026-01.jsonl")
        with open(path, "w") as f:
            f.write(json.dumps({"ts": "2026-01-01T00:00:00Z", "event": "note"}) + "\n")
        os.chmod(path, 0)  # the test's folder is removed whole: no mode to restore

    def test_unreadable_archive_never_loses_an_event(self):
        self.archive_unreadable()
        self.put([])  # an empty live ledger: the first line's prev would come from the archive
        c.log_event(self.p, "note", data={"kept": 1})
        self.assertEqual([json.loads(x)["data"] for x in self.lines()], [{"kept": 1}])

    def test_no_lock_never_loses_an_event(self):
        n = len(self.lines())
        with mock.patch.object(c.fcntl, "flock", side_effect=OSError(37, "No locks available")):
            c.log_event(self.p, "note", data={"kept": 1})
        self.assertEqual(len(self.lines()), n + 1)
        self.assertEqual(json.loads(self.lines()[-1])["data"], {"kept": 1})
        c.log_event(self.p, "note")
        self.assertEqual(self.verify().returncode, 0, "the unchained line is a gap, not a break")

    def test_edit_is_named(self):
        for i in range(5):
            c.log_event(self.p, "note", data={"i": i})
        lines = self.lines()
        lines[2] = lines[2].replace('"event": "', '"event": "x', 1)
        self.put(lines)
        r = self.verify()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("ledger.jsonl:3", r.stdout + r.stderr)

    def test_deletion_is_named(self):
        for i in range(5):
            c.log_event(self.p, "note", data={"i": i})
        lines = self.lines()
        n = len(lines)
        del lines[n - 3]  # line n-2 goes: line n-3 is the one its successor no longer follows
        self.put(lines)
        r = self.verify()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn(f"ledger.jsonl:{n - 3}", r.stdout + r.stderr)

    def test_first_line_deleted_is_caught(self):
        c.log_event(self.p, "note")
        self.put(self.lines()[1:])
        r = self.verify()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("ledger.jsonl:1", r.stdout + r.stderr)

    def test_truncation_mid_line_is_named(self):
        for i in range(3):
            c.log_event(self.p, "note", data={"i": i})
        n = len(self.lines())
        with open(self.ledger, "rb+") as f:
            f.truncate(os.path.getsize(self.ledger) - 10)
        r = self.verify()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn(f"ledger.jsonl:{n}", r.stdout + r.stderr)
        c.log_event(self.p, "note")  # a write after the cut starts its own line; the cut one stays named
        r = self.verify()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn(f"ledger.jsonl:{n}", r.stdout + r.stderr)

    def test_head_anchor_catches_removed_tail(self):
        c.log_event(self.p, "note")
        head = h(self.lines()[-1])
        for i in range(3):
            c.log_event(self.p, "note", data={"i": i})
        self.assertEqual(self.verify("--head", head).returncode, 0)
        self.put(self.lines()[:-4])  # the anchored line and all after it: the rest still chains
        self.assertEqual(self.verify().returncode, 0, "tail truncation alone is invisible to a chain")
        r = self.verify("--head", head)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn(head, r.stdout + r.stderr)

    def test_legacy_prefix_is_tolerated(self):
        legacy = [json.dumps({"ts": "2026-09-01T00:00:00Z", "event": "note", "data": {"i": i}}) for i in range(3)]
        self.put(legacy)
        c.log_event(self.p, "note")
        c.log_event(self.p, "note")
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("ledger.jsonl:4", r.stdout)
        lines = self.lines()
        lines[2] = lines[2].replace('"i": 2', '"i": 9')  # the last legacy line: the first chained line vouches for it
        self.put(lines)
        r = self.verify()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("ledger.jsonl:3", r.stdout + r.stderr)

    def test_unchained_line_after_the_start_is_a_reported_gap(self):
        c.log_event(self.p, "note")
        with open(self.ledger, "a") as f:  # an older Foreman still running in another session
            f.write(json.dumps({"ts": c.now(), "event": "note"}) + "\n")
        n = len(self.lines())
        c.log_event(self.p, "note")
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn(f"ledger.jsonl:{n}", r.stdout)

    def test_concurrent_writers_keep_the_chain(self):
        def burst(k):
            for i in range(25):
                c.log_event(self.p, "note", data={"k": k, "i": i})
        threads = [threading.Thread(target=burst, args=(k,)) for k in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        r = self.verify("--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout)["chained"], len(self.lines()))

    def test_chain_survives_the_monthly_roll(self):
        self.put([])
        with mock.patch.object(c, "now", return_value="2026-01-15T00:00:00Z"):
            for i in range(5):
                c.log_event(self.p, "note", data={"pad": "y" * 50})
        with mock.patch.object(fmtidy, "LEDGER_ROLL_BYTES", 0):
            fmtidy._roll_ledger(self.p, True, [])  # every line is a past month's: the live file starts empty
        self.assertEqual(len(read_text(os.path.join(self.p.dir, "archive", "ledger-2026-01.jsonl")).splitlines()), 5)
        c.log_event(self.p, "note")
        r = self.verify("--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout)["chained"], 7)  # 5 archived, ledger_rolled, note
        archived = read_text(os.path.join(self.p.dir, "archive", "ledger-2026-01.jsonl")).splitlines()
        archived[1] = archived[1].replace("yyy", "yyz", 1)
        with open(os.path.join(self.p.dir, "archive", "ledger-2026-01.jsonl"), "w") as f:
            f.write("".join(x + "\n" for x in archived))
        r = self.verify()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("ledger-2026-01.jsonl:2", r.stdout + r.stderr)

    # T-1099: the roll reads bytes, keeps time order and takes the ledger's own flock
    def roll(self):
        with mock.patch.object(fmtidy, "LEDGER_ROLL_BYTES", 0), mock.patch.object(c, "now", return_value=MARCH):
            fmtidy._roll_ledger(self.p, True, [])

    def archived(self):
        with open(os.path.join(self.p.dir, "archive", "ledger-2026-01.jsonl"), "rb") as f:
            return f.read().splitlines()

    def test_roll_survives_a_bad_byte(self):
        bad, deep = b'{"ts": "2026-01-15T00:00:00Z", "event": "note", "data": "\xff"}', b"[" * 100000  # RecursionError
        with open(self.ledger, "wb") as f:
            f.write(bad + b"\n" + deep + b"\n" + json.dumps({"ts": MARCH, "event": "note"}).encode() + b"\n")
        self.roll()
        self.assertEqual(self.archived(), [bad, deep], "the bad byte is archived byte for byte")
        self.assertEqual(json.loads(self.lines()[0])["ts"], MARCH)

    # T-1099 review: a roll that dies at any point loses no line, archives none twice and leaves a green chain
    def crash_roll(self, target, name, again=()):
        self.put([])
        for ts in ("2026-01-15T00:00:00Z", "2026-01-16T00:00:00Z", MARCH):
            with mock.patch.object(c, "now", return_value=ts):
                c.log_event(self.p, "note")
        with mock.patch.object(target, name, side_effect=OSError(5, "crash")), self.assertRaises(OSError):
            self.roll()
        c.log_event(self.p, "note", data={"after": 1})  # lands before the next roll
        self.roll()
        self.assertEqual([json.loads(x)["ts"] for x in self.archived()], ["2026-01-15T00:00:00Z", "2026-01-16T00:00:00Z"])
        self.assertEqual([json.loads(x)["data"] for x in self.lines()], [{}, {"after": 1}, *again],
                         "ledger_rolled only when lines left the live file")
        self.assertFalse(os.path.exists(self.ledger + ".rolling"))
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_crash_before_the_rewrite_archives_nothing_twice(self):
        self.crash_roll(c, "write_atomic", [{"2026-01": 2}])  # the live file still had them: rolled again, appended once

    def test_crash_mid_rewrite_is_restored_from_the_sidecar(self):
        self.crash_roll(os, "ftruncate")

    def test_crash_after_the_rewrite_drops_the_stale_sidecar(self):
        self.crash_roll(os, "remove")

    def test_unparseable_ts_rolls_with_its_neighbours(self):
        self.put(["not json"])  # a leading line with no ts goes with the first line that has one
        old = ["2026-01-15T00:00:00Z", "not a time", "2099-01-01T00:00:00Z", "2026-01-16T00:00:00Z"]  # 2099: a clock ahead
        for ts in old + [MARCH]:
            with mock.patch.object(c, "now", return_value=ts):
                c.log_event(self.p, "note")
        self.roll()
        self.assertEqual(self.archived()[0], b"not json")
        self.assertEqual([json.loads(x)["ts"] for x in self.archived()[1:]], old)
        self.assertEqual(json.loads(self.lines()[0])["ts"], MARCH)
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_roll_waits_for_a_writer_and_keeps_its_line(self):
        self.put([])
        with mock.patch.object(c, "now", return_value="2026-01-15T00:00:00Z"):
            for _ in range(3):
                c.log_event(self.p, "note")
        with open(self.ledger, "a+b") as f:  # a writer mid-log_event: holds the ledger's flock
            c.fcntl.flock(f, c.fcntl.LOCK_EX)
            t = threading.Thread(target=self.roll)
            t.start()
            t.join(0.3)
            self.assertTrue(t.is_alive(), "the roll waits for the ledger's flock")
            prev = c.ledger_hash(c._last_line(f))
            f.write((json.dumps({"prev": prev, "ts": MARCH, "event": "note", "data": {"racer": 1}}) + "\n").encode())
        t.join(5)
        self.assertEqual(len(self.archived()), 3)
        self.assertEqual(json.loads(self.lines()[0])["data"], {"racer": 1}, "the writer's line survives the roll")
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


MARCH = "2026-03-02T00:00:00Z"


class Receipt(ForemanTestCase):
    def test_finish_names_the_head(self):
        self.fm("task", "new", "First", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        r = self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true")
        m = re.search(r"Ledger: head ([0-9a-f]{16}) \((\d+) chained lines?\)", r.stdout)
        self.assertTrue(m, r.stdout)
        self.assertEqual(self.fm("verify-ledger", "--head", m.group(1)).returncode, 0)

    def test_finish_json_carries_the_head(self):
        self.fm("task", "new", "First", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        out = json.loads(self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", "--json").stdout)
        self.assertRegex(out["ledger"]["head"], r"^[0-9a-f]{16}$")

    def unreadable_archive(self):
        if os.geteuid() == 0:
            self.skipTest("root reads a mode-000 file")
        self.fm("task", "new", "First", "--type", "FEATURE", "--tier", "S", "--ac", "ok :: true", "--step", "s",
                "--focus")
        folder = os.path.join(c.find_project(self.repo).dir, "archive")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "ledger-2026-01.jsonl")
        with open(path, "w") as f:
            f.write("{}\n")
        os.chmod(path, 0)

    def test_unreadable_ledger_never_fails_the_finish(self):
        self.unreadable_archive()
        r = self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Ledger: unreadable", r.stdout)
        self.assertTrue(r.stdout.strip().splitlines()[-1].startswith("Landed:"), r.stdout)

    def test_unreadable_ledger_never_fails_done_json(self):
        self.unreadable_archive()
        r = self.fm("task", "finish", "T-0001", "--audit", "self", "--run", "true", "--json", check=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        led = json.loads(r.stdout)["ledger"]
        self.assertIsNone(led["head"])
        self.assertIn("unreadable", led)
