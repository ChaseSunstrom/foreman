"""Unit tests for fmcore: paths, locking, writes, redaction, ledger, briefs, intake, queue."""
import json
import multiprocessing
import os
import time
import unittest

from helpers import ForemanTestCase

import fmcore as c


class PathsAndProjects(ForemanTestCase):
    def test_foreman_home_honours_env(self):
        self.assertEqual(c.foreman_home(), self.home)
        self.assertEqual(c.state_dir(), os.path.join(self.home, "state"))

    def test_state_falls_back_when_foreman_home_is_read_only(self):
        # Sandboxes (claude plugin eval) and containers can mount ~/.claude read-only; fm must keep working.
        os.chmod(self.home, 0o500)
        try:
            os.environ["XDG_STATE_HOME"] = os.path.join(self.tmp, "xdg")
            self.assertEqual(c.state_dir(), os.path.join(self.tmp, "xdg", "foreman"))
            p = c.init_project(self.repo)
            self.assertTrue(p.dir.startswith(os.path.join(self.tmp, "xdg", "foreman")))
        finally:
            os.chmod(self.home, 0o700)

    def test_foreman_state_env_overrides(self):
        os.environ["FOREMAN_STATE"] = os.path.join(self.tmp, "elsewhere")
        self.assertEqual(c.state_dir(), os.path.join(self.tmp, "elsewhere"))

    def test_foreman_home_defaults_under_user_home(self):
        del os.environ["FOREMAN_HOME"]
        os.environ["HOME"], old = self.tmp, os.environ["HOME"]
        try:
            self.assertEqual(c.foreman_home(), os.path.join(self.tmp, ".claude", "foreman"))
        finally:
            os.environ["HOME"] = old
            os.environ["FOREMAN_HOME"] = self.home

    def test_slug_is_dirname_plus_stable_hash(self):
        s1 = c.slug_for("/a/b/My App")
        self.assertRegex(s1, r"^my-app-[0-9a-f]{6}$")
        self.assertEqual(s1, c.slug_for("/a/b/My App"))
        self.assertNotEqual(s1, c.slug_for("/other/My App"))

    def test_git_root_found_from_subdir(self):
        sub = os.path.join(self.repo, "src", "deep")
        os.makedirs(sub)
        self.assertEqual(c.git_root(sub), self.repo)
        self.assertIsNone(c.git_root(self.tmp))

    def test_init_project_creates_state_and_registry(self):
        p = c.init_project(self.repo)
        self.assertTrue(os.path.isdir(os.path.join(p.dir, "tasks")))
        meta = c.read_meta(p)
        self.assertEqual(meta["path"], self.repo)
        self.assertFalse(meta["sensitive"])
        with open(os.path.join(c.state_dir(), "registry.md")) as f:
            self.assertIn(p.slug, f.read())

    def test_find_project_auto_registers_git_repo_only_when_asked(self):
        self.assertIsNone(c.find_project(self.repo))
        p = c.find_project(self.repo, create=True)
        self.assertEqual(p.root, self.repo)
        self.assertEqual(c.find_project(os.path.join(self.repo)).slug, p.slug)

    def test_find_project_non_git_dir_needs_init(self):
        plain = os.path.join(self.tmp, "plain")
        os.makedirs(plain)
        self.assertIsNone(c.find_project(plain, create=True))
        p = c.init_project(plain)
        self.assertEqual(c.find_project(os.path.join(plain)).slug, p.slug)

    def test_detects_sensitive_repo_from_local_settings(self):
        os.makedirs(os.path.join(self.repo, ".claude"))
        with open(os.path.join(self.repo, ".claude", "settings.local.json"), "w") as f:
            json.dump({"permissions": {"defaultMode": "default"}}, f)
        p = c.init_project(self.repo)
        self.assertTrue(c.read_meta(p)["sensitive"])


class WritesAndLocks(ForemanTestCase):
    def test_write_atomic_replaces_content_and_leaves_no_temp(self):
        path = os.path.join(self.tmp, "x", "f.txt")
        c.write_atomic(path, "one")
        c.write_atomic(path, "two")
        with open(path) as f:
            self.assertEqual(f.read(), "two")
        self.assertEqual(os.listdir(os.path.dirname(path)), ["f.txt"])

    def test_lock_times_out_when_held_by_another_process(self):
        d = os.path.join(self.tmp, "lockdir")
        os.makedirs(d)
        ready = multiprocessing.Event()
        proc = multiprocessing.Process(target=_hold_lock, args=(d, ready, 1.5))
        proc.start()
        try:
            ready.wait(5)
            t0 = time.monotonic()
            with self.assertRaises(c.LockTimeout):
                with c.lock(d, timeout=0.3):
                    pass
            self.assertLess(time.monotonic() - t0, 1.2)
        finally:
            proc.join()
        with c.lock(d, timeout=0.3):
            pass


def _hold_lock(d, ready, secs):
    with c.lock(d, timeout=1):
        ready.set()
        time.sleep(secs)


class Redaction(unittest.TestCase):
    CASES = [
        "export ANTHROPIC_API_KEY=sk-ant-api03-abcdefghijklmnop",
        "token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ012345",
        "curl -H 'Authorization: Bearer abc.def.ghi' https://x",
        "password=hunter2hunter2",
        "aws AKIAABCDEFGHIJKLMNOP",
        "git clone https://user:s3cretpass@github.com/x/y",
        "-----BEGIN OPENSSH PRIVATE KEY-----\nAAAA\n-----END OPENSSH PRIVATE KEY-----",
        "jwt eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    ]
    SECRETS = ["sk-ant-api03-abcdefghijklmnop", "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ012345", "abc.def.ghi",
               "hunter2hunter2", "AKIAABCDEFGHIJKLMNOP", "s3cretpass", "AAAA", "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"]

    def test_known_secret_shapes_are_redacted(self):
        for text, secret in zip(self.CASES, self.SECRETS):
            with self.subTest(text=text):
                out = c.redact(text)
                self.assertNotIn(secret, out)
                self.assertIn("REDACTED", out)

    def test_ordinary_text_is_untouched(self):
        for text in ["run pytest -q", "the token count is 400", "password field validation", "key: value"]:
            self.assertEqual(c.redact(text), text)

    def test_redacted_json_stays_valid(self):
        s = json.dumps({"cmd": "export TOKEN=abcd1234efgh && curl -H \"Authorization: Bearer xyz123\""})
        self.assertIsInstance(json.loads(c.redact(s)), dict)


class Ledger(ForemanTestCase):
    def test_tail_returns_n_events_beyond_64k(self):
        p = c.init_project(self.repo)
        c.log_event(p, "touched", task="T-0001", data={"file": "x.py"})
        for i in range(600):  # ~120 KB of later events
            c.log_event(p, "tool", data={"pad": "y" * 150, "i": i})
        events = c.ledger_tail(p, 1000)
        self.assertEqual(len(events), 601)
        self.assertEqual(events[0]["event"], "touched")
        self.assertEqual(len(c.ledger_tail(p, 5)), 5)

    def test_log_event_appends_redacted_json_lines(self):
        p = c.init_project(self.repo)
        c.log_event(p, "note", task="T-0001", data={"cmd": "export API_KEY=abcdef123456"}, session="s1")
        c.log_event(p, "note2")
        with open(os.path.join(p.dir, "ledger.jsonl")) as f:
            lines = [json.loads(l) for l in f]
        self.assertEqual([l["event"] for l in lines[-2:]], ["note", "note2"])
        rec = lines[-2]
        self.assertEqual(set(rec), {"ts", "session_id", "project", "task", "event", "data"})
        self.assertEqual(rec["session_id"], "s1")
        self.assertNotIn("abcdef123456", json.dumps(rec))
        self.assertRegex(rec["ts"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")


SAMPLE = """---
id: T-0012
type: FIX
tier: M
status: active
priority: normal
scope: [src/auth/**, tests/auth/**]
depends_on: [T-0003]
source: user   # user|discovered
allow: []
created: 2026-09-25T10:00:00Z
updated: 2026-09-25T10:00:00Z
---
# Fix login timeout on slow networks
## Raw request
> FIX: login times out after 30s on slow networks
## Acceptance criteria
- [ ] login succeeds at 3G latency — verify with `pytest tests/auth -k slow`
- [x] no regression — verify with `pytest`
## Steps
1. [x] Reproduce with a failing test
2. [ ] Add retry with backoff  <- CURRENT
3. [ ] Update docs
## Resume here
Retry helper half written.
## Verification evidence
- (step 1) `pytest tests/auth -k slow` → 1 failed as expected (2026-09-25T10:05:00Z)
- (ac 2) `pytest` → 40 passed (2026-09-25T10:06:00Z)
## Log
- 2026-09-25T10:00:00Z created
"""


class Briefs(unittest.TestCase):
    def test_parse_frontmatter_lists_comments_and_title(self):
        b = c.Brief.parse(SAMPLE)
        self.assertEqual(b.id, "T-0012")
        self.assertEqual(b.type, "FIX")
        self.assertEqual(b.meta["scope"], ["src/auth/**", "tests/auth/**"])
        self.assertEqual(b.meta["depends_on"], ["T-0003"])
        self.assertEqual(b.meta["source"], "user")
        self.assertEqual(b.meta["allow"], [])
        self.assertEqual(b.title, "Fix login timeout on slow networks")

    def test_round_trip_is_lossless(self):
        self.assertEqual(c.Brief.parse(SAMPLE).render(), SAMPLE)

    def test_steps_and_current(self):
        steps = c.Brief.parse(SAMPLE).steps()
        self.assertEqual([(s.n, s.done, s.current) for s in steps], [(1, True, False), (2, False, True), (3, False, False)])
        self.assertEqual(steps[1].text, "Add retry with backoff")

    def test_evidence_lookup_by_step_and_ac(self):
        b = c.Brief.parse(SAMPLE)
        self.assertTrue(b.has_evidence(step=1))
        self.assertFalse(b.has_evidence(step=2))
        self.assertTrue(b.has_evidence(ac=2))
        self.assertFalse(b.has_evidence(ac=1))

    def test_mark_step_requires_evidence(self):
        b = c.Brief.parse(SAMPLE)
        with self.assertRaises(c.PolicyError):
            b.mark_step(2)
        b.add_evidence("pytest tests/auth", "3 passed", step=2, ts="2026-09-25T11:00:00Z")
        b.mark_step(2)
        steps = b.steps()
        self.assertTrue(steps[1].done)
        self.assertTrue(steps[2].current, "marking the current step done advances CURRENT")

    def test_add_step_and_set_current(self):
        b = c.Brief.parse(SAMPLE)
        b.add_step("Changelog entry")
        b.set_current(4)
        self.assertEqual([s.current for s in b.steps()], [False, False, False, True])

    def test_add_step_creates_current_marker_on_first_step(self):
        b = c.Brief.new("T-0001", "Do a thing", "FEATURE", "S", now="2026-01-01T00:00:00Z")
        b.add_step("first")
        b.add_step("second")
        self.assertEqual([s.current for s in b.steps()], [True, False])

    def test_acceptance_criteria_parse_and_check(self):
        b = c.Brief.parse(SAMPLE)
        self.assertEqual([(a.n, a.checked) for a in b.acceptance()], [(1, False), (2, True)])
        with self.assertRaises(c.PolicyError):
            b.check_ac(1)
        b.add_evidence("pytest tests/auth -k slow", "1 passed", ac=1)
        b.check_ac(1)
        self.assertTrue(all(a.checked for a in b.acceptance()))

    def test_done_blockers_lists_what_is_missing(self):
        b = c.Brief.parse(SAMPLE)
        reasons = b.done_blockers()
        self.assertTrue(any("step 2" in r for r in reasons))
        self.assertTrue(any("criterion 1" in r for r in reasons))

    def _finished(self, tier):
        b = c.Brief.new("T-0001", "Do a thing", "FEATURE", tier, now="2026-01-01T00:00:00Z")
        b.add_step("work")
        b.add_evidence("make test", "ok", step=1, ts="2026-01-01T10:00:00Z")
        b.mark_step(1)
        return b

    def test_audits_required_by_tier(self):
        s = self._finished("S")
        self.assertTrue(any("audit" in r for r in s.done_blockers()))
        s.add_audit("intent", "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        self.assertIn("audit missing: self", s.done_blockers(), "one lens doesn't replace the five-lens self checklist")
        s.add_audit("self", "lens checklist", "no findings", ts="2026-01-01T11:00:00Z")
        self.assertEqual(s.done_blockers(), [])
        m = self._finished("M")
        m.add_audit("intent", "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        self.assertTrue(any("audit" in r for r in m.done_blockers()))
        m.add_audit("edge", "fm-reviewer", "1 finding fixed", ts="2026-01-01T11:00:00Z")
        self.assertEqual(m.done_blockers(), [])
        big = self._finished("L")
        for lens in ("intent", "adversary", "edge", "operator"):
            big.add_audit(lens, "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        self.assertEqual([r for r in big.done_blockers() if "audit" in r], ["audit missing: maintainer"])
        big.add_audit("maintainer", "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        self.assertEqual(big.done_blockers(), [])

    def test_audit_must_postdate_the_last_change(self):
        b = self._finished("S")
        b.add_audit("self", "checklist", "ok", ts="2026-01-01T09:00:00Z")  # before the step evidence
        self.assertTrue(any("audit" in r for r in b.done_blockers()))
        b.add_audit("self", "checklist", "ok", ts="2026-01-01T11:00:00Z")
        self.assertEqual(b.done_blockers(), [])
        self.assertTrue(any("audit" in r for r in b.done_blockers(since="2026-01-01T12:00:00Z")), "edited after audit")

    def test_unknown_lens_is_rejected(self):
        with self.assertRaises(ValueError):
            self._finished("S").add_audit("vibes", "x", "y")

    def test_new_brief_has_frontmatter_and_raw_request(self):
        b = c.Brief.new("T-0007", "Export CSV", "FEATURE", "M", raw="FEATURE: export report as CSV @src/reports",
                        scope=["src/reports"], now="2026-01-01T00:00:00Z")
        text = b.render()
        self.assertTrue(text.startswith("---\nid: T-0007\n"))
        self.assertIn("> FEATURE: export report as CSV @src/reports", text)
        self.assertEqual(c.Brief.parse(text).meta["scope"], ["src/reports"])
        self.assertEqual(c.Brief.parse(text).status, "planned")

    def test_resume_auto_block_is_replaced_not_duplicated(self):
        b = c.Brief.parse(SAMPLE)
        b.set_resume_auto("- step 2/3\n- git: 1 changed")
        b.set_resume_auto("- step 3/3")
        sec = b.section("Resume here")
        self.assertIn("Retry helper half written.", sec)
        self.assertEqual(sec.count("<!-- auto -->"), 1)
        self.assertIn("step 3/3", sec)
        self.assertNotIn("step 2/3", sec)


class Stages(unittest.TestCase):
    """The harness derives stage and the one next required action from the brief itself (T-0012)."""

    def brief(self, tier="S", type_="FIX", status="planned"):
        b = c.Brief.new("T-0001", "Fix login", type_, tier, now="2026-01-01T00:00:00Z", status=status)
        return b

    def plan(self, b):
        b.set_section("Interpretation", "Login times out on slow networks.")
        b.set_section("Approach (options → choice → why)", "Retry with backoff vs longer timeout → retry.")
        b.add_ac("login works on 3G", verify="pytest -k slow")
        b.add_step("reproduce")
        return b

    def test_plan_gaps_by_tier(self):
        s = self.brief("S")
        self.assertEqual(sorted(c.plan_gaps(s)), ["acceptance criterion", "step"])
        s.add_ac("works")
        s.add_step("do it")
        self.assertEqual(c.plan_gaps(s), [])
        m = self.brief("M")
        m.add_ac("works")
        m.add_step("do it")
        self.assertEqual(sorted(c.plan_gaps(m)), ["Approach", "Interpretation", "verify command on criterion 1"])
        big = self.plan(self.brief("L"))
        self.assertEqual(c.plan_gaps(big), ["approval (L tier, standard autonomy)"])
        self.assertEqual(c.plan_gaps(big, autonomy="full"), [])
        big.meta["approved"] = True
        self.assertEqual(c.plan_gaps(big), [])

    def test_stage_and_next_action_follow_the_brief(self):
        b = self.brief("M", status="captured")
        self.assertEqual(c.stage(b), "captured")
        self.assertIn("fm task new", c.next_action(b))
        b.meta["status"] = "planned"
        self.assertEqual(c.stage(b), "planning")
        self.assertIn("Interpretation", c.next_action(b))
        self.plan(b)
        self.assertEqual(c.stage(b), "ready")
        self.assertIn("fm focus T-0001", c.next_action(b))
        b.meta["status"] = "active"
        self.assertEqual(c.stage(b), "executing")
        nxt = c.next_action(b)
        self.assertIn("step 1/1", nxt)
        self.assertIn("debugging.md", nxt, "FIX names its procedure")
        b.add_evidence("pytest -k slow", "1 failed as expected", step=1, ts="2026-01-01T10:00:00Z")
        b.mark_step(1)
        self.assertEqual(c.stage(b), "verifying")
        self.assertIn("fm task ac T-0001 check 1", c.next_action(b))
        b.add_evidence("pytest -k slow", "1 passed", ac=1)
        b.check_ac(1)
        self.assertEqual(c.stage(b), "auditing")
        self.assertIn("audit.md", c.next_action(b))
        b.add_audit("intent", "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        b.add_audit("edge", "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        self.assertEqual(c.stage(b), "closing")
        self.assertIn("fm task done T-0001", c.next_action(b))


class OpenEnded(unittest.TestCase):
    def test_vague_requests_are_open_ended(self):
        for text in ("Just get it done", "super improve it", "make it better!", "improve everything",
                     "brainstorm some features for this", "what should we build next?", "go wild",
                     "Just get it done etc, super improve it"):
            with self.subTest(text=text):
                self.assertTrue(c.is_open_ended(text))

    def test_concrete_requests_are_not(self):
        for text in ("fix the login timeout on slow wifi", "FIX: login times out", "improve the error message in parse_ts",
                     "add a --verbose flag to the CLI", "yes", "PAUSE", ""):
            with self.subTest(text=text):
                self.assertFalse(c.is_open_ended(text))


class Intake(unittest.TestCase):
    BLOCK = """FIX: login times out after 30s on slow networks
FEATURE: export report as CSV @src/reports #T-0003
  include the totals row
clean!: collapse the three date helpers into one
PERF?: dashboard first paint takes 4s
SECURITY: review the upload endpoint
CONTEXT: Django app; don't touch migrations
NEVER: push to main
DONE-WHEN: all tests pass and the CSV opens in Excel
SKIP: mobile layout
"""

    def test_items_tags_modifiers_and_continuations(self):
        r = c.parse_intake(self.BLOCK)
        self.assertEqual([i.type for i in r.items], ["FIX", "FEATURE", "CLEAN", "PERFORMANCE", "SECURITY"])
        feat = r.items[1]
        self.assertIn("include the totals row", feat.text)
        self.assertEqual(feat.scopes, ["src/reports"])
        self.assertEqual(feat.refs, ["T-0003"])
        self.assertTrue(r.items[2].urgent)
        self.assertTrue(r.items[3].explore)
        self.assertEqual(r.context, ["Django app; don't touch migrations"])
        self.assertEqual(r.constraints, ["NEVER: push to main"])
        self.assertEqual(r.done_when, ["all tests pass and the CSV opens in Excel"])
        self.assertEqual(r.skip, ["mobile layout"])

    def test_aliases(self):
        r = c.parse_intake("BUG: a\nREFACTOR: b\nSPIKE: c\nADD: d\nSEC: e\nNOTE: n\nMUST: m\nACCEPT: x\nOUT: o")
        self.assertEqual([i.type for i in r.items], ["FIX", "CLEAN", "RESEARCH", "FEATURE", "SECURITY"])
        self.assertEqual(r.context, ["n"])
        self.assertEqual(r.constraints, ["MUST: m"])
        self.assertEqual(r.done_when, ["x"])
        self.assertEqual(r.skip, ["o"])

    def test_untagged_request_and_non_tags(self):
        r = c.parse_intake("make the build faster\nsee http://example.com/x for details")
        self.assertEqual(r.items, [])
        self.assertIn("make the build faster", r.untagged)

    def test_override_words(self):
        self.assertEqual(c.parse_intake("NOW: prod is down").overrides, ["NOW"])
        self.assertEqual(c.parse_intake("NOW: FIX: prod is down").items[0].type, "FIX")
        self.assertTrue(c.parse_intake("NOW: FIX: prod is down").items[0].urgent)
        for word in ["pause", "PAUSE", "hold on", "stop"]:
            self.assertEqual(c.parse_intake(word).overrides, ["PAUSE"], word)
        self.assertEqual(c.parse_intake("resume").overrides, ["RESUME"])
        self.assertEqual(c.parse_intake("status").overrides, ["STATUS"])
        self.assertEqual(c.parse_intake("that's for the current task").overrides, ["STEER"])
        self.assertEqual(c.parse_intake("please stop the server when done").overrides, [])

    def test_bang_tag_marks_urgent(self):
        r = c.parse_intake("FIX!: prod 500s on login")
        self.assertTrue(r.items[0].urgent)

    def test_tier_guess(self):
        self.assertEqual(c.guess_tier("FIX", "typo in header"), "S")
        self.assertEqual(c.guess_tier("FEATURE", "export report as CSV with totals and filters"), "M")
        self.assertEqual(c.guess_tier("FEATURE", "migrate the auth schema to OAuth2"), "L")


def _b(id, type, status="planned", priority="normal", deps=()):
    b = c.Brief.new(id, f"task {id}", type, "S", now="2026-01-01T00:00:00Z")
    b.meta["status"] = status
    b.meta["priority"] = priority
    b.meta["depends_on"] = list(deps)
    return b


class Queue(unittest.TestCase):
    def test_canonical_order(self):
        briefs = [_b("T-0001", "FEATURE"), _b("T-0002", "FIX"), _b("T-0003", "CLEAN"),
                  _b("T-0004", "SECURITY"), _b("T-0005", "PERFORMANCE"), _b("T-0006", "RESEARCH")]
        q, cycles, dangling = c.order_queue(briefs)
        self.assertEqual([b.id for b in q], ["T-0006", "T-0003", "T-0005", "T-0004", "T-0002", "T-0001"])
        self.assertEqual((cycles, dangling), ([], []))

    def test_active_first_then_urgent(self):
        briefs = [_b("T-0001", "CLEAN"), _b("T-0002", "FEATURE", priority="urgent"), _b("T-0003", "FIX", status="active")]
        q, _, _ = c.order_queue(briefs)
        self.assertEqual([b.id for b in q], ["T-0003", "T-0002", "T-0001"])

    def test_dependencies_override_canonical_order(self):
        briefs = [_b("T-0001", "CLEAN", deps=["T-0002"]), _b("T-0002", "FEATURE")]
        q, _, _ = c.order_queue(briefs)
        self.assertEqual([b.id for b in q], ["T-0002", "T-0001"])

    def test_done_dependency_is_satisfied_and_dangling_reported(self):
        briefs = [_b("T-0001", "FIX", deps=["T-0009", "T-0002"]), _b("T-0002", "CLEAN", status="done")]
        q, _, dangling = c.order_queue(briefs)
        self.assertEqual([b.id for b in q], ["T-0001"])
        self.assertEqual(dangling, [("T-0001", "T-0009")])

    def test_cycles_are_reported_not_dropped(self):
        briefs = [_b("T-0001", "FIX", deps=["T-0002"]), _b("T-0002", "FIX", deps=["T-0001"]), _b("T-0003", "CLEAN")]
        q, cycles, _ = c.order_queue(briefs)
        self.assertEqual([b.id for b in q][0], "T-0003")
        self.assertEqual(sorted(b.id for b in q), ["T-0001", "T-0002", "T-0003"])
        self.assertEqual(cycles, [["T-0001", "T-0002"]])

    def test_captured_blocked_and_closed_are_not_in_queue(self):
        briefs = [_b("T-0001", "FIX", status="captured"), _b("T-0002", "FIX", status="blocked"),
                  _b("T-0003", "FIX", status="dropped"), _b("T-0004", "FIX")]
        q, _, _ = c.order_queue(briefs)
        self.assertEqual([b.id for b in q], ["T-0004"])


if __name__ == "__main__":
    unittest.main()
