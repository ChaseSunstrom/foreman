"""T-0949: the first Edit/Write of a file in a task gets the Avoid section of the map's best stack card for that file,
once per card per task (a ledger event, logged before the note goes out); fm doctor counts the enforce events of the
last 7 days by kind (validator blocks, merge refusals, waived merges, injected cards)."""
import inspect
import json
import os
import re
import subprocess
from datetime import datetime, timedelta, timezone

from test_builder import _Tasks, git
from test_hooks import HookCase

import fmcore as c

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = "Foreman: stack card"


def card(name, area, score, *detect):
    return {"name": name, "area": area, "score": score, "detect": list(detect)}


class _CardCase(HookCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.tid = self.task()

    def map(self, cards=None, raw=None):
        with open(os.path.join(self.project().dir, "map.json"), "w", encoding="utf-8") as f:
            f.write(raw if raw is not None else json.dumps({"lib": [x["name"] for x in cards], "lib_cards": cards}))

    def edit(self, rel, env=None):
        path = os.path.join(self.repo, rel)
        proc = self.hook("PreToolUse", {"tool_name": "Edit", "tool_input": {"file_path": path, "old_string": "x",
                                                                          "new_string": "y"}}, env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn('"deny"', proc.stdout)
        ctx = self.ctx_of(proc)
        return ctx[ctx.index(HEAD):] if HEAD in ctx else ""

    def injected(self):
        return [e for e in c.ledger_tail(self.project(), 200)
                if e["event"] == "enforce" and e["data"].get("kind") == "card_injected"]



class EditCards(_CardCase):
    def test_first_edit_injects_the_cards_avoid_section_once_per_task(self):
        self.map([card("python", "lang", 5, "ext:.py", "file:pyproject.toml")])
        note = self.edit("app.py")
        self.assertIn("python", note)
        self.assertIn("Mutable default arguments", note)
        ev = self.injected()
        self.assertEqual([(e["task"], e["data"]["card"]) for e in ev], [(self.tid, "python")])
        self.assertEqual(self.edit("other.py"), "", "the card was already injected in this task")
        self.assertEqual(self.edit("app.py"), "")
        self.assertEqual(len(self.injected()), 1)
        self.assertEqual(self.edit("README.md"), "", "no card matches a markdown file")
        self.fm("task", "new", "Second", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        self.assertIn("Mutable default arguments", self.edit("app.py"), "a new task gets the card again")

    def test_a_framework_card_beats_its_language_card_and_ties_go_by_name(self):
        self.map([card("python", "lang", 9, "ext:.py"), card("pytest", "python", 2, "file:conftest.py")])
        self.assertIn("stack card pytest", self.edit("tests/conftest.py"))
        self.map([card("python", "lang", 2, "ext:.py"), card("ruff", "python", 2, "ext:.py"),
                  card("mypy", "python", 2, "ext:.py")])
        self.fm("task", "new", "Two", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        self.assertIn("stack card mypy", self.edit("a.py"), "own-ext framework cards tie by name before the language")
        self.map([card("python", "lang", 2, "ext:.py"), card("go-concurrency", "go", 9, "lext:.py"),
                  card("uv", "python", 1, "lext:.py")])
        self.fm("task", "new", "Three", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        self.assertIn("stack card python", self.edit("a.py"), "a card sharing only the language's ext comes after it")
        self.map([card("uv", "python", 7, "lext:.py"), card("ruff", "python", 2, "lext:.py")])
        self.fm("task", "new", "Four", "--type", "FIX", "--tier", "S", "--ac", "x :: true", "--step", "s", "--focus")
        self.assertIn("stack card uv", self.edit("a.py"), "without the language card, the higher score")

    def test_a_long_avoid_section_is_cut_at_a_bullet_under_700_chars(self):
        self.map([card("vault", "infra", 2, "file:*.hcl")])
        note = self.edit("policies/app.hcl")
        self.assertTrue(note, "vault's Avoid section is over 700 chars, so it is cut, not dropped")
        self.assertLessEqual(len(note), 700)
        self.assertTrue(note.endswith("…"), note[-80:])
        with open(os.path.join(PLUGIN, "skills", "library", "cards", "infra", "vault.md"), encoding="utf-8") as f:
            lines = set(f.read().splitlines())
        bullets = [l for l in note.splitlines() if l.startswith("- ")]
        self.assertTrue(bullets)
        self.assertEqual([b for b in bullets if b not in lines], [], "every bullet is whole")

    def test_no_avoid_section_missing_card_or_bad_map_injects_nothing(self):
        import fmlib
        self.assertIsNone(fmlib.avoid_note("x", "---\nname: x\n---\nSummary.\n\n## Do\n- a\n"))
        self.map([card("no-such-card", "lang", 5, "ext:.py")])
        self.assertEqual(self.edit("a.py"), "")
        self.assertEqual(self.injected(), [], "nothing injected, nothing logged")
        for raw in ("{", "[]", '{"lib_cards": 7}', '{"lib_cards": [7, {"name": 1}, {"name": "python", "detect": 3}]}',
                    '{"lib_cards": [{"name": "../../etc/passwd", "detect": ["ext:.py"]}]}'):
            self.map(raw=raw)
            self.assertEqual(self.edit("a.py"), "", raw)
        os.remove(os.path.join(self.project().dir, "map.json"))
        self.assertEqual(self.edit("a.py"), "")
        self.assertEqual(self.injected(), [])

    def test_env_and_fm_lib_inject_off_turn_it_off(self):
        self.map([card("python", "lang", 5, "ext:.py")])
        self.assertEqual(self.edit("a.py", env={"FOREMAN_NO_CARDS": "1"}), "")
        self.fm("lib", "inject", "off")
        self.assertIn("off", self.fm("lib", "inject").stdout)
        self.assertEqual(self.edit("a.py"), "")
        self.assertEqual(self.injected(), [])
        self.fm("lib", "inject", "on")
        self.assertIn("Mutable default arguments", self.edit("a.py"))

    def test_the_map_carries_each_cards_area_score_and_file_signals(self):
        import fmmap
        with open(os.path.join(self.repo, "app.py"), "w") as f:
            f.write("x = 1\n")
        subprocess.run(["git", "-C", self.repo, "add", "app.py"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "py"], check=True)
        m = fmmap.load(self.project(), rebuild=True)
        py = [x for x in m["lib_cards"] if x["name"] == "python"]
        self.assertTrue(py, m["lib_cards"])
        self.assertEqual(py[0]["area"], "lang")
        self.assertIn("ext:.py", py[0]["detect"])
        self.assertFalse([s for x in m["lib_cards"] for s in x["detect"] if s.startswith("dep:")])
        shared = [x for x in m["lib_cards"] if x["area"] != "lang" and "ext:.py" in x["detect"]]
        self.assertFalse(shared, "a non-language card keeps the language's ext only as lext:")
        self.assertEqual(m["lib"], [x["name"] for x in m["lib_cards"]])


class EditCardsDoctor(HookCase):
    def test_doctor_counts_seven_days_of_enforce_events_by_kind(self):
        import fmdoctor
        self.fm("init")
        p = self.project()
        c.log_event(p, "enforce", data={"file": "a.json", "problem": "bad"})  # T-0947's validator block
        c.log_event(p, "enforce", data={"kind": "validator_block", "file": "b.json", "problem": "bad"})
        c.log_event(p, "enforce", data={"kind": "merge_refused", "reason": "red"})
        c.log_event(p, "enforce", data={"kind": "card_injected", "card": "python"})
        c.log_event(p, "lane_unverified", data={"reason": "flaky"})
        old = (datetime.now(timezone.utc) - timedelta(days=9)).isoformat()
        with open(os.path.join(p.dir, "ledger.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": old, "event": "enforce", "data": {"kind": "card_injected"}}) + "\n")
        r = fmdoctor.check_enforce(p)
        self.assertEqual(r.status, "PASS")
        for want in ("validator_block 2", "merge_refused 1", "lane_unverified 1", "card_injected 1"):
            self.assertIn(want, r.detail)
        self.assertIn("check_enforce(", inspect.getsource(fmdoctor.run_all))
        self.assertIn("none", fmdoctor.check_enforce(None).detail)


class EditCardsMerge(_Tasks):
    def test_a_refused_merge_is_an_enforce_event(self):
        tid = json.loads(self.fm("task", "new", "Red", "--type", "FEATURE", "--tier", "S", "--ac",
                                 "it passes :: false", "--step", "build", "--json").stdout)["id"]
        wt = os.path.join(self.tmp, "wt-" + tid)
        git(self.repo, "worktree", "add", "-q", "-b", f"foreman/{tid}", wt)
        self.fm("focus", tid, cwd=wt)
        with open(os.path.join(wt, "x.py"), "w") as f:
            f.write("x = 1\n")
        git(wt, "add", "x.py")
        git(wt, "commit", "-qm", "work")
        self.assertNotEqual(self.fm("lane", "merge", tid, check=False).returncode, 0)
        ev = [e for e in c.ledger_tail(c.find_project(self.repo), 50) if e["event"] == "enforce"]
        self.assertEqual([(e["task"], e["data"]["kind"]) for e in ev], [(tid, "merge_refused")])
        self.assertTrue(re.search(r"criterion 1 is red", ev[0]["data"]["reason"]))


class EditCardsReview(_CardCase):
    """T-0949 review: every file tool, a marker instead of a ledger scan, fm lib inject never creates a project."""

    def tool(self, name, inp):
        proc = self.hook("PreToolUse", {"tool_name": name, "tool_input": inp})
        ctx = self.ctx_of(proc)
        return ctx[ctx.index(HEAD):] if HEAD in ctx else ""

    def test_write_multiedit_and_notebookedit_get_the_card(self):
        self.map([card("python", "lang", 5, "ext:.py"), card("jupyter", "ml", 5, "ext:.ipynb"),
                  card("rust", "lang", 5, "ext:.rs")])
        self.assertIn("python", self.tool("Write", {"file_path": os.path.join(self.repo, "w.py"), "content": "x"}))
        self.assertIn("rust", self.tool("MultiEdit", {"file_path": os.path.join(self.repo, "m.rs"), "edits": []}))
        nb = self.tool("NotebookEdit", {"notebook_path": os.path.join(self.repo, "n.ipynb"), "new_source": "x"})
        self.assertIn("jupyter", nb) if nb else None

    def test_dedupe_reads_a_small_marker_not_the_ledger(self):
        self.map([card("python", "lang", 5, "ext:.py")])
        self.assertIn("python", self.edit("a.py"))
        with open(os.path.join(self.project().dir, "ledger.jsonl"), "w") as f:
            f.write("")  # the ledger rolled or was archived: the marker still knows
        self.assertEqual(self.edit("b.py"), "")

    def test_fm_lib_inject_status_never_creates_a_project(self):
        other = os.path.join(self.tmp, "plain")
        os.makedirs(other)
        subprocess.run(["git", "init", "-q", other], check=True)
        r = self.fm("lib", "inject", cwd=other)
        self.assertIn("Edit-time stack cards", r.stdout)
        self.assertIsNone(c.find_project(other, create=False))
