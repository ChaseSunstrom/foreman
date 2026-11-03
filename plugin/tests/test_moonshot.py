"""Every Genesis generation advances the moonshot campaign (T-2626; MOONSHOT.md part A, the user's steer of 2026-11-02
"integrate MOONSHOT into each gen of the tower"): one catalogue across generations toward 100 on the six-tier mix, cold
tiers from the strongest model, kill tests for extreme and massive, the climb fm orders, a floor of one big stage a
generation, the seed showing it and the steer exam's held-out rate, the Genesis page carrying the catalogue."""
import json
import os
from unittest import mock

from helpers import CLEAN_READER, ForemanTestCase, read_text
from test_genesis import GEN0_CAPS, SEED, line, tower_file


def setUpModule():  # every put here passes its cold read, as in test_genesis
    os.environ["PATH"] = CLEAN_READER + os.pathsep + os.environ["PATH"]


def tearDownModule():
    os.environ["PATH"] = os.environ["PATH"].replace(CLEAN_READER + os.pathsep, "", 1)


def moon(mid, title, tier, domain="ecology", stage="idea", extra=""):
    return (f"### {mid} · {title}\n- Tier: {tier}\n- Domain: {domain}\n- Lens: far-domain\n"
            f"- Prior art: none found\n- Better by: no harness does it\n- Novelty: 4\n- Stage: {stage}\n{extra}\n")


class _Tower(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        from sampo import core as c
        from sampo import rune
        self.p = c.find_project(self.repo)
        self.tower = rune.home(self.p)
        rune.init(self.p, GEN0_CAPS.encode())

    def catalogue(self, *blocks):
        tower_file(self.tower, "moonshot.md", "# Moonshot catalogue\n\n" + "".join(blocks))

    def problems(self):
        from sampo import moons
        return moons.check(self.p)

    def rated(self, **tiers):
        """Reviewer tiers as fm genesis moonshot rate records them (keyed by moonshot id: the first rating stands)."""
        from sampo import moons
        rows = {r["id"]: r for r in moons.parse(read_text(os.path.join(self.tower, "moonshot.md")))}
        store = {k: {"tier": v, "author": rows[k]["author"], "key": rows[k]["key"]} for k, v in tiers.items()}
        with open(os.path.join(self.p.dir, moons.STORE), "w") as f:
            json.dump(store, f)


class Shape(_Tower):
    def test_the_check_holds_the_mix_the_lines_duplicates_kill_results_and_measures(self):
        self.assertEqual(self.problems(), [])  # no catalogue yet: nothing to hold
        self.catalogue(*(moon(f"M-{i:02d}", f"Low idea number {i} about grafting", "low") for i in range(1, 7)))
        self.assertTrue(any("6 low" in x and "mix" in x for x in self.problems()), self.problems())
        self.catalogue(moon("M-01", "Immune memory for the guard", "extreme").replace("- Prior art: none found\n", ""),
                       moon("M-02", "Immune memory for the guard rules", "high"),
                       moon("M-03", "Auction the queue among lanes", "massive", stage="slice"),
                       moon("M-04", "Price every task by its risk", "xhigh", stage="full"),
                       moon("M-05", "Tier typed by hand", "low").replace("- Tier: low", "- Tier: low (reviewer: high)"))
        got = "\n".join(self.problems())
        self.assertIn("M-01", got)
        self.assertIn("Prior art", got)
        self.assertIn("M-02", got)  # near-duplicate of M-01
        self.assertIn("M-03", got)  # a staged massive with no kill result
        self.assertIn("M-04", got)  # built with no measure
        self.assertIn("M-05", got)  # a typed reviewer tier counts for nothing
        tid = json.loads(self.fm("task", "new", "Auction the queue among lanes", "--type", "FEATURE", "--tier", "M",
                                 "--json").stdout)["id"]
        self.catalogue(moon("M-03", "Auction the queue among lanes", "massive"))
        self.assertTrue(any(tid in x for x in self.problems()))  # a duplicate of queued work
        self.catalogue(moon("M-03", "Auction the queue among lanes", "massive", extra=f"- Evidence: {tid}\n"))
        self.assertEqual(self.problems(), [])  # the task that builds it is its own, not a duplicate
        # review: "not viable" is no viable result, and a kill result cites its evidence
        self.catalogue(moon("M-03", "Auction the queue among lanes", "massive", stage="kill",
                            extra=f"- Evidence: {tid}\n- Kill: one queue offline → not viable\n- Needs: none\n"))
        self.assertTrue(any("kill result" in x for x in self.problems()), self.problems())
        self.catalogue(moon("M-03", "Auction the queue among lanes", "massive", stage="kill",
                            extra="- Kill: one queue offline → viable\n- Needs: none\n"))
        self.assertTrue(any("cites no evidence" in x for x in self.problems()), self.problems())
        self.catalogue(moon("M-03", "Auction the queue among lanes", "massive", stage="kill",
                            extra=f"- Kill: one queue offline ({tid}) → viable\n- Needs: none\n"))
        self.assertEqual(self.problems(), [])

    def test_fm_genesis_check_carries_the_campaign_problems(self):
        from sampo import rune
        self.catalogue(moon("M-01", "Immune memory for the guard", "extreme").replace("- Novelty: 4\n", ""))
        self.assertTrue(any("Novelty" in x for x in rune.moonshot_check(self.p)["problems"]))


class Rate(_Tower):
    def test_the_strongest_model_tiers_the_unrated_blind_to_the_authors_tier_and_demotions_are_logged(self):
        from sampo import rune
        from sampo import moons
        self.catalogue(moon("M-01", "Immune memory for the guard", "massive"),
                       moon("M-02", "Auction the queue among lanes", "extreme"))
        calls = []

        def child(feature, system, prompt, model, timeout, **kw):
            calls.append((model, prompt))
            return "1: high | an existing loop with a new signal\n2: extreme | no harness prices work\n9: low | none"
        with mock.patch("sampo.ideas.run_child", child):
            r = moons.rate(self.p)
        self.assertEqual(calls[0][0], rune.REVIEW_MODELS[-1])
        self.assertNotIn("massive", calls[0][1])  # the author's tier never reaches the reader
        self.assertEqual((r["rated"], r["demoted"]), (2, 1))
        tiers = {x["id"]: (x["author"], x["reviewer"]) for x in moons.rows(self.p)}
        self.assertEqual(tiers, {"M-01": ("massive", "high"), "M-02": ("extreme", "extreme")})
        with mock.patch("sampo.ideas.run_child", child):
            self.assertEqual(moons.rate(self.p)["rated"], 0)  # a rated block isn't read again
        ev = [e for e in self.read_events() if e.get("event") == "genesis_moonshot_rate"]
        self.assertEqual(ev[-1]["data"]["demoted"], 1)
        self.assertEqual(ev[-1]["data"]["moved"], [{"id": "M-01", "from": "massive", "to": "high",
                                                     "why": "an existing loop with a new signal"}])
        self.catalogue(moon("M-01", "Immune memory for the guard, now bigger", "massive"),
                       moon("M-02", "Auction the queue among lanes", "extreme"))
        with mock.patch("sampo.ideas.run_child", child):
            self.assertEqual(moons.rate(self.p)["rated"], 0)  # an edit can't re-roll the first rating

    def read_events(self):
        from sampo import core as c
        return c.ledger_events(self.p, kinds=["genesis_moonshot_rate"])


class Climb(_Tower):
    def test_unblockers_first_then_big_ones_by_tier_and_stage_then_the_rest_with_a_big_stage_early(self):
        from sampo import moons
        self.catalogue(moon("M-01", "Market for lane time", "massive", stage="kill",
                            extra="- Kill: auction one queue offline → viable\n- Needs: M-04\n"),
                       moon("M-02", "Swarm repair of flaky tests", "extreme", stage="kill",
                            extra="- Kill: replay ten flakes → viable\n- Needs: none\n"),
                       moon("M-03", "Colour the pane by mood", "low"),
                       moon("M-04", "Price signal per task", "medium", extra="- Unblocks: M-01, M-05\n"),
                       moon("M-05", "Futures on finishing", "massive"),
                       moon("M-06", "A ledger of lane bids", "high", extra="- Unblocks: M-01\n"),
                       moon("M-07", "Sleep cycles for memory", "massive", stage="not-yet",
                            extra="- Kill: no slow store yet → not-yet: needs M-06\n- Needs: M-06\n"))
        got = [(x["id"], x["next"]) for x in moons.order(self.p)]
        self.assertEqual(got[0], ("M-04", "full"))  # unblocks two big ones
        self.assertEqual(got[1], ("M-06", "full"))
        self.assertIn(("M-02", "slice"), got[:3])  # a big stage within the first three: the floor
        self.assertNotIn("M-01", [i for i, _ in got])  # its need (M-04) isn't built yet
        self.assertNotIn("M-07", [i for i, _ in got])  # not-yet until M-06 is built
        self.assertEqual(got[-1], ("M-03", "full"))  # unblocks nothing: last
        self.catalogue(moon("M-06", "A ledger of lane bids", "high", stage="full",
                            extra="- Unblocks: M-07\n- Measure: fm exam kind bids\n"),
                       moon("M-07", "Sleep cycles for memory", "massive", stage="not-yet",
                            extra="- Kill: no slow store yet → not-yet: needs M-06\n- Needs: M-06\n"))
        self.assertEqual([(x["id"], x["next"]) for x in moons.order(self.p)], [("M-07", "kill")])  # re-check

    def test_a_generation_that_advanced_no_big_moonshot_is_red_once_a_later_one_exists(self):
        from sampo import moons
        self.catalogue(moon("M-02", "Swarm repair of flaky tests", "extreme", stage="slice",
                            extra="- Kill: replay ten flakes → viable\n- Needs: none\n"))
        self.rated(**{"M-02": "extreme"})
        tower_file(self.tower, "gen-3/mission-moonshot.md", "# Moonshot\n\nAdded: M-02\n")
        tower_file(self.tower, "gen-3/seed.md", SEED)
        self.assertEqual(moons.floor(self.p), [])  # gen 3 is still running for check
        self.assertTrue(any("gen-3" in x for x in moons.floor(self.p, upto=3)))  # its own sweep holds it
        tower_file(self.tower, "gen-4/seed.md", SEED)
        self.assertTrue(any("gen-3" in x for x in moons.floor(self.p)))
        self.assertTrue(any("gen-4/seed.md" in x and "campaign" in x for x in moons.floor(self.p)))  # flagged
        tower_file(self.tower, "gen-4/seed.md", SEED + "\n## Moonshot\n\n" + "\n".join(moons.seed_lines(self.p, 4)))
        self.assertFalse(any("gen-4/seed.md" in x for x in moons.floor(self.p)))
        tid = json.loads(self.fm("task", "new", "M-02 slice", "--type", "FEATURE", "--tier", "S", "--json").stdout)["id"]
        tower_file(self.tower, "gen-3/mission-moonshot.md", f"# Moonshot\n\nAdvanced: M-02 slice ({tid})\n")
        self.assertTrue(any("done" in x for x in moons.floor(self.p)))  # the task must be done
        self.fm("task", "drop", tid, "x")
        self.assertTrue(any("done" in x for x in moons.floor(self.p)))  # dropped isn't done
        # a typed line alone never holds: the task names the moonshot, is done, and the catalogue reached the stage
        other = self.done_task("Tidy the docs")
        tower_file(self.tower, "gen-3/mission-moonshot.md", f"# Moonshot\n\nAdvanced: M-02 slice ({other})\n")
        self.assertTrue(moons.floor(self.p))
        mine = self.done_task("M-02 smallest working slice")
        tower_file(self.tower, "gen-3/mission-moonshot.md", f"# Moonshot\n\nAdvanced: M-02 full ({mine})\n")
        self.assertTrue(moons.floor(self.p))  # the catalogue still says slice
        tower_file(self.tower, "gen-3/mission-moonshot.md", f"# Moonshot\n\nAdvanced: M-02 slice ({mine})\n")
        self.assertFalse(any(x.startswith("gen-3") for x in moons.floor(self.p)))
        self.rated(**{"M-02": "high"})  # rated below extreme: the floor needs a big one by the reviewer's tier
        self.assertTrue(any(x.startswith("gen-3") for x in moons.floor(self.p)))

    def done_task(self, title):
        from sampo import core as c
        tid = json.loads(self.fm("task", "new", title, "--type", "FEATURE", "--tier", "S", "--json").stdout)["id"]
        b = c.find_brief(self.p, tid)
        b.meta["status"] = "done"
        c.save_brief(self.p, b)
        return tid


class Seed(_Tower):
    def test_each_seed_shows_the_campaign_and_the_steer_rate(self):
        from sampo import rune
        rune.put(self.p, "gen-1/seed.md", SEED)
        rune.put(self.p, "gen-2/seed.md", SEED)
        tower_file(self.tower, "lineage.md", "# Lineage\n\n## gen-1\n- baseline: first\n- seed base: gen-1\n\n"
                                             "## gen-2\n- kept: x\n- seed base: gen-2\n")
        tower_file(self.tower, "exam.jsonl", line("r1", 1, ["a"]) + line("r1", 2, ["a"]))
        self.catalogue(moon("M-01", "Market for lane time", "massive"), moon("M-04", "Price signal per task", "medium",
                                                                             extra="- Unblocks: M-01\n"))
        tower_file(self.tower, "steer.jsonl", json.dumps({"run": "steer-x", "model": "sonnet", "judge": "opus",
                                                          "holdout": {"cases": 13, "rate": 0.192}}) + "\n")
        rune.seed(self.p, 3)
        text = read_text(os.path.join(self.tower, "gen-3/seed.md"))
        sec = text.split("## " + rune.MOONSHOT, 1)[1].split("\n## ", 1)[0]
        for want in ("2 of 100", "massive 1/25", "medium 1/10", "inversion", "2030", "fm genesis moonshot rate",
                     "Kill:", "M-04 full", "Advanced: M-NN", "Measure:", "19%", "13"):
            self.assertIn(want, sec)


class Page(_Tower):
    def test_the_export_and_page_carry_the_catalogue(self):
        from sampo import rune
        self.catalogue(moon("M-01", "Market for lane time", "massive", extra="- Unblocks: M-02\n"),
                       moon("M-02", "<img src=x onerror=alert(1)>", "low"))
        self.rated(**{"M-01": "extreme"})
        out = os.path.join(self.tmp, "site")
        rune.export(self.p, out)
        got = json.loads(read_text(os.path.join(out, "genesis.json")))["moonshots"]
        r = {x["id"]: x for x in got["rows"]}
        self.assertEqual((r["M-01"]["author"], r["M-01"]["reviewer"], r["M-01"]["unblocks"]), ("massive", "extreme", ["M-02"]))
        self.assertEqual(r["M-01"]["asked"], "no")
        self.assertEqual(got["total"], 2)
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        js = read_text(os.path.join(root, "site", "genesis", "genesis.js"))
        self.assertIn('id="moonshots"', read_text(os.path.join(root, "site", "genesis", "index.html")))
        body = js[js.index("function moonshotTable"):js.index("function moonshotTable") + 2500]
        self.assertIn("D.moonshots", body)
        self.assertNotIn("innerHTML", body)
