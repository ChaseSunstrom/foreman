"""T-3542: fm ui --json keeps its JSON while its inputs stand still. The foreman-ui mod runs it on every 2 s poll a
tool call dirties; a rebuild costs ~0.7 s CPU, so a run whose project state, briefs and HEAD are unchanged prints the
stored view, and any of them moving rebuilds it."""
import json
import os

from helpers import ForemanTestCase

from sampo import core as c

ON = {"FOREMAN_UI_CACHE_S": "60"}  # the suite runs with the cache off (helpers); these tests turn it on


class UiCache(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def hook_ms(self, *ms):
        """Hook timings in events.jsonl: the view's latency series shows them, and the cache key never reads them, so
        the series tells a rebuilt view from a kept one."""
        os.makedirs(c.state_dir(), exist_ok=True)
        with open(os.path.join(c.state_dir(), "events.jsonl"), "w") as f:
            f.writelines(json.dumps({"kind": "hook_ms", "event": "PreToolUse", "ms": m}) + "\n" for m in ms)

    def latency(self):
        return json.loads(self.fm("ui", "--json", env=ON).stdout)["latency"]

    def test_unchanged_inputs_print_the_kept_view_and_a_moved_one_rebuilds_it(self):
        self.fm("task", "new", "Tidy the parser", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.hook_ms(5)
        first = self.fm("ui", "--json", env=ON).stdout
        self.assertEqual(json.loads(first)["latency"], [5])
        self.hook_ms(7)
        self.assertNotIn("cached", json.loads(first))
        kept = json.loads(self.fm("ui", "--json", env=ON).stdout)
        self.assertEqual(kept, dict(json.loads(first), cached=True), "nothing it keys on moved: the kept view, marked")
        with open(os.path.join(self.p.dir, "map.json"), "w") as f:  # a file the key leaves to the age
            f.write("{}")
        self.assertEqual(self.latency(), [5])
        meta = os.path.join(self.p.dir, "meta.json")
        with open(meta, "a") as f:  # touched in place: the same inode, a new size and mtime
            f.write(" ")
        self.assertEqual(self.latency(), [7], "a touched state file rebuilds")
        self.hook_ms(9)
        self.assertEqual(self.latency(), [7])
        c.save_brief(self.p, c.find_brief(self.p, "T-0001"), touch=False)  # no ledger line: only the tasks folder moves
        self.assertEqual(self.latency(), [9], "a saved brief rebuilds")

    def test_the_trust_record_and_the_pause_flag_are_never_served_stale(self):
        self.hook_ms(5)
        self.latency()
        self.hook_ms(7)
        self.assertEqual(self.latency(), [5])
        with open(c.trust_path(), "w") as f:  # /fm-trust on: the mod writes it straight to disk
            json.dump({"on": True, "at": "2026-01-01T00:00:00Z", "via": "composer"}, f)
        v = json.loads(self.fm("ui", "--json", env=ON).stdout)
        self.assertEqual((v["latency"], v["mode"]["trust"]), ([7], True))
        self.hook_ms(9)
        with open(os.path.join(c.state_dir(), "PANIC"), "w") as f:  # sampo pause: autonomy reads as standard
            f.write("paused\n")
        self.assertEqual(self.latency(), [9], "a pause rebuilds")

    def test_an_old_view_is_rebuilt_and_off_never_keeps_one(self):
        self.hook_ms(5)
        self.latency()
        self.hook_ms(6)
        self.assertEqual(self.latency(), [5])
        path = os.path.join(self.p.dir, "cache", "ui.json")
        with open(path, encoding="utf-8") as f:
            kept = json.load(f)
        kept["at"] -= 61  # older than FOREMAN_UI_CACHE_S: clocks and unkeyed inputs are due
        c.write_atomic(path, json.dumps(kept))
        self.hook_ms(7)
        self.assertEqual(self.latency(), [7])
        self.hook_ms(9)
        self.assertEqual(json.loads(self.fm("ui", "--json").stdout)["latency"], [9], "FOREMAN_UI_CACHE_S=0: no cache")

    def test_a_rebuild_never_moves_the_folder_the_mod_watches(self):
        self.latency()  # the first run makes cache/ and the kept band lines
        at = os.stat(self.p.dir).st_mtime_ns
        self.hook_ms(3)
        os.utime(os.path.join(self.p.dir, "ledger.jsonl"))  # a moved input: this run rebuilds and stores again
        self.assertEqual(self.latency(), [3])
        self.assertEqual(os.stat(self.p.dir).st_mtime_ns, at, "a write there would wake the mod's next poll")
