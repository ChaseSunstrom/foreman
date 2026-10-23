"""T-1549: the brainstorm pack holds each user quote once; a release in a historically bad hour warns; a default a
release changes is named in its notes, and fm settings changed says whether it reaches you; fm digest --say speaks."""
import json
import os
import tempfile
import unittest

from helpers import ForemanTestCase, read_text

import fmcore as c
import fmideas
import fmrelease
import fmsettings


def run(hour, failed):
    """A check_run event at this local hour (on 2026-10-01), failed or passed."""
    import datetime
    ts = datetime.datetime(2026, 10, 1, hour, 10).astimezone().astimezone(datetime.timezone.utc)
    return {"ts": ts.strftime("%Y-%m-%dT%H:%M:%SZ"), "event": "check_run",
            "data": {"results": [{"cmd": "x", "exit": 1 if failed else 0}]}}


class Pack(ForemanTestCase):
    def test_each_quote_is_in_the_pack_once(self):
        self.fm("init")
        for _ in range(2):
            tid = json.loads(self.fm("task", "new", "Make the export faster", "--type", "PERF", "--tier", "S", "--ac",
                                     "x :: true", "--step", "x", "--json").stdout)["id"]
            self.fm("task", "set", tid, "source=user", "--section", "Raw request", "--text", "> make the export faster")
        voice = fmideas.user_voice(c.find_project(self.repo))
        self.assertEqual(voice.count("make the export faster"), 1, voice)


class Release(unittest.TestCase):
    def test_a_bad_hour_is_one_that_failed_twice_as_often(self):
        events = [run(3, k < 4) for k in range(6)] + [run(14, k < 2) for k in range(20)]
        f, n, overall = fmrelease.bad_hour(events, 3)
        self.assertEqual((f, n), (4, 6))
        self.assertAlmostEqual(overall, 6 / 26)
        self.assertIsNone(fmrelease.bad_hour(events, 14), "an ordinary hour")
        self.assertIsNone(fmrelease.bad_hour(events[:6], 3), "too little history to say")
        self.assertIsNone(fmrelease.bad_hour(events, 5), "no runs at that hour")

    def test_the_notes_name_a_changed_default_and_the_snapshot_moves_on(self):
        now = fmsettings.defaults()
        key = next(k for k, v in sorted(now.items()) if isinstance(v, str))
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "plugin"))
            with open(os.path.join(root, "plugin", "defaults.json"), "w") as f:
                json.dump(dict(now, **{key: "an older value"}), f)
            with open(os.path.join(root, "CHANGELOG.md"), "w") as f:
                f.write("# Changes\n\n## Unreleased\n- a thing\n\n## 0.0.1 — 2026-01-01\n- first\n")
            fmrelease._changelog({"root": root, "version": "0.0.2"})
            text = read_text(os.path.join(root, "CHANGELOG.md"))
            self.assertIn(f"## 0.0.2 — ", text)
            self.assertIn(f'- Default changed: {key} "an older value" → {json.dumps(now[key])} (if you never set it, '
                          "this changes what you see)\n- a thing", text)
            with open(os.path.join(root, "plugin", "defaults.json")) as f:
                self.assertEqual(json.load(f), now)


class Settings(ForemanTestCase):
    def test_changed_says_whether_a_moved_default_reaches_you(self):
        old = dict(fmsettings.defaults(), **{"app.motion": "reduced"})
        path = os.path.join(self.tmp, "old.json")
        with open(path, "w") as f:
            json.dump(old, f)
        got = json.loads(self.fm("settings", "changed", path, "--json").stdout)
        self.assertEqual([(m["key"], m["old"], m["yours"]) for m in got], [("app.motion", "reduced", False)])
        self.assertIn("you never set it", self.fm("settings", "changed", path).stdout)
        os.makedirs(os.path.dirname(fmsettings.app_path()), exist_ok=True)  # as the user's own tui.toml sets it
        with open(fmsettings.app_path(), "w") as f:
            f.write('motion = "off"\n')
        got = json.loads(self.fm("settings", "changed", path, "--json").stdout)
        self.assertTrue(got[0]["yours"])

    def test_the_snapshot_ships_with_every_default(self):
        with open(fmsettings.SNAPSHOT) as f:
            self.assertEqual(set(json.load(f)), set(fmsettings.defaults()))


class Say(ForemanTestCase):
    def test_the_digest_is_read_aloud_by_an_installed_speech_program(self):
        self.fm("init")
        bindir, said = os.path.join(self.tmp, "bin"), os.path.join(self.tmp, "said")
        os.makedirs(bindir)
        with open(os.path.join(bindir, "say"), "w") as f:
            f.write(f"#!/bin/sh\nprintf '%s ' \"$@\" > {said}\n")
        os.chmod(os.path.join(bindir, "say"), 0o755)
        self.fm("digest", "--say", env={"PATH": bindir + os.pathsep + os.environ["PATH"]})
        self.assertIn("tasks done", read_text(said))


if __name__ == "__main__":
    unittest.main()
