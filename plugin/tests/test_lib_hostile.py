"""T-1396: hostile skills, agents and marketplaces can't get past fm lib's source indexer or fm plugins' marketplace read.
The corpus (fixtures/hostile/corpus.json) runs through the indexer: every bad item is quarantined with its reason and
held out of fm lib search, the clean ones are indexed. The marketplace fixture has bad entries among good ones, a
rename and a re-sourced plugin."""
import json
import os
import re
import shutil
import subprocess

from helpers import ForemanTestCase, read_json

import fmcore as c
import fmlib
import fmplugins

HOSTILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "hostile")


def _expand(s):
    return re.sub(r"\{(.)\*(\d+)\}", lambda m: m.group(1) * int(m.group(2)), s)


def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data if isinstance(data, str) else json.dumps(data))


class HostileCorpus(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.items = [dict(x, path=_expand(x["path"])) for x in read_json(os.path.join(HOSTILE, "corpus.json"))["items"]]
        self.zoo = os.path.join(self.tmp, "zoo")
        for x in self.items:
            path = os.path.join(self.zoo, x["path"])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if "link" in x:
                os.symlink(x["link"], path)
            else:
                _write(path, _expand(x["body"]))
        _write(os.path.join(self.zoo, "LICENSE"), "MIT License\n")
        for args in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "zoo"]):
            subprocess.run(["git", "-C", self.zoo, "-c", "user.email=t@t", "-c", "user.name=t", *args], check=True,
                           capture_output=True)

    def test_the_corpus_is_big_enough(self):
        self.assertGreaterEqual(sum(bool(x["expect"]) for x in self.items), 25)

    def test_every_bad_item_is_quarantined_with_its_reason_and_the_clean_ones_are_not(self):
        index = {x["path"]: x for x in fmlib._index_source(self.zoo)}
        for x in self.items:
            with self.subTest(x["path"]):
                self.assertIn(x["path"], index, "every skill and agent is in the index, quarantined or not")
                got = index[x["path"]]
                if x["expect"]:
                    self.assertIn(x["expect"], got.get("quarantine", ""))
                else:
                    self.assertNotIn("quarantine", got)
                # whatever the item, what is stored is safe to print and bounded
                self.assertEqual(c.plain(got["name"] + got["description"] + got.get("quarantine", "")),
                                 got["name"] + got["description"] + got.get("quarantine", ""))
                self.assertLessEqual(len(got["name"]), 64)
                self.assertLessEqual(len(got["description"]), 400)

    def test_quarantined_items_are_held_out_of_search_and_show(self):
        out = self.fm("lib", "source", "add", self.zoo, "--name", "zoo").stdout
        self.assertIn("quarantined", out)
        self.assertIn("agents/hijack.md: over-broad description", out)  # the reason is shown with the path
        self.assertIn("zoo:good-skill", self.fm("lib", "search", "tide", "tables").stdout)
        self.assertIn("zoo:good-agent", self.fm("lib", "search", "tidepool").stdout)
        for q in (["every", "task"], ["always", "use"], ["override"], ["dupe", "squatting"], ["hijack"]):
            found = self.fm("lib", "search", *q).stdout
            self.assertNotIn("zoo:every-task", found)
            self.assertNotIn("zoo:hijack", found)
            self.assertNotIn("squatting", found)
        shown = self.fm("lib", "show", "zoo:every-task", check=False)
        self.assertNotEqual(shown.returncode, 0)
        meta = read_json(os.path.join(c.state_dir(), "lib-sources", "zoo", "source.json"))
        self.assertEqual(meta["skills"], 3)  # dupe, good-skill, quoted-ok
        self.assertEqual(meta["agents"], 1)
        self.assertGreaterEqual(meta["quarantined"], 25)
        self.assertIn("quarantined", self.fm("lib", "source", "list").stdout)


class HostileMarketplace(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.cc = os.path.join(self.tmp, "cc")
        mk = os.path.join(self.cc, "plugins", "marketplaces", "hostile")
        self.mk_file = os.path.join(mk, ".claude-plugin", "marketplace.json")
        os.makedirs(os.path.dirname(self.mk_file))
        shutil.copy(os.path.join(HOSTILE, "marketplace.json"), self.mk_file)
        _write(os.path.join(mk, "plugins", "good-one", "skills", "tide", "SKILL.md"),
               "---\nname: tide\ndescription: Tide tables.\n---\n")
        # two more marketplaces that are wrong as a whole: a list, and plugins as a string
        _write(os.path.join(self.cc, "plugins", "marketplaces", "a-list", ".claude-plugin", "marketplace.json"), [1, 2])
        _write(os.path.join(self.cc, "plugins", "marketplaces", "a-string", ".claude-plugin", "marketplace.json"),
               {"name": "a-string", "plugins": "everything"})
        os.environ["CLAUDE_CONFIG_DIR"] = self.cc

    def tearDown(self):
        os.environ.pop("CLAUDE_CONFIG_DIR", None)
        super().tearDown()

    def test_bad_entries_are_skipped_with_reasons_and_the_rest_load(self):
        skipped = []
        rows = {p["id"]: p for p in fmplugins.index(skipped)}
        self.assertEqual(sorted(rows), ["good-one@hostile", "moved-tool@hostile", "new-tool@hostile"])
        self.assertEqual(rows["good-one@hostile"]["description"], "Tide tables for the shell")  # the first one wins
        self.assertEqual(rows["new-tool@hostile"]["description"], "")  # not a string: nothing, not a crash
        self.assertIsNotNone(rows["good-one@hostile"]["local"])
        text = "\n".join(skipped)
        for why in ("entry 1: not an object", "entry 4: not an object", "entry 5: no name", "entry 6: no name",
                    "entry 7: name '../escape'", "entry 8: name 'two@ids'", "entry 9: its source is outside",
                    "entry 11: a second entry named good-one", "a-list", "a-string"):
            self.assertIn(why, text)
        self.assertEqual(rows["new-tool@hostile"]["renamed_from"], ["old-tool"])
        # the guard's pin reads the same index: a good entry still hashes, a skipped one is unknown
        self.assertTrue(fmplugins.content_hash("good-one@hostile"))
        self.assertIsNone(fmplugins.content_hash("outside@hostile"))
        out = self.fm("plugins", "find", "tide").stdout
        self.assertIn("good-one@hostile", out)
        self.assertIn("skipped", out)

    def test_a_renamed_or_re_sourced_plugin_reads_as_untrusted(self):
        for pid in ("good-one@hostile", "moved-tool@hostile"):
            fmplugins.record_trust(pid)
        trust = {p["id"]: fmplugins.trust(p) for p in fmplugins.index()}
        self.assertEqual(trust["good-one@hostile"], (True, ""))
        self.assertEqual(trust["moved-tool@hostile"], (True, ""))
        trusted, why = trust["new-tool@hostile"]
        self.assertFalse(trusted)
        self.assertIn("renamed from old-tool", why)
        # the marketplace repoints moved-tool to another repo, and renames good-one's source to another folder
        data = read_json(self.mk_file)
        data["plugins"][12]["source"]["repo"] = "evil/moved-tool"
        _write(self.mk_file, data)
        trusted, why = fmplugins.trust(next(p for p in fmplugins.index() if p["id"] == "moved-tool@hostile"))
        self.assertFalse(trusted)
        self.assertIn("changed since", why)
        data["plugins"][12]["source"] = {"source": "github", "repo": "org/moved-tool", "sha": "0000"}
        _write(self.mk_file, data)
        self.assertFalse(fmplugins.trust(next(p for p in fmplugins.index() if p["id"] == "moved-tool@hostile"))[0])
        out = self.fm("plugins", "find", "tide", "tool").stdout
        self.assertIn("untrusted: renamed from old-tool", out)
        self.assertIn("untrusted: its name, source or sha changed", out)
