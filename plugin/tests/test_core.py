"""Unit tests for fmcore: paths, locking, writes, redaction, ledger, briefs, intake, queue."""
import json
import multiprocessing
import os
import re
import subprocess
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

    def test_fallback_is_sticky_and_shared_and_migrates_existing_state(self):
        # A sandboxed fm (default read-only) and the hooks (default writable) must end up in the same place.
        os.environ["XDG_STATE_HOME"] = os.path.join(self.tmp, "xdg")
        alt = os.path.join(self.tmp, "xdg", "foreman")
        p = c.init_project(self.repo)
        c.log_event(p, "note", data={"x": 1})
        default = os.path.join(self.home, "state")
        os.chmod(self.home, 0o500)
        os.chmod(default, 0o500)
        try:
            self.assertEqual(c.state_dir(), alt)  # the sandboxed side activates the fallback
        finally:
            os.chmod(self.home, 0o700)
            os.chmod(default, 0o700)
        self.assertEqual(c.state_dir(), alt, "the unsandboxed side (hooks) follows the marker")
        self.assertTrue(any(e["event"] == "note" for e in c.ledger_tail(c.find_project(self.repo))),
                        "existing state was copied across")

    def test_a_link_someone_else_planted_is_refused(self):
        # T-1317: _private stat'ed through links, so another user's /tmp/foreman-state-<uid> link to one of our 0700
        # dirs (~/.ssh) passed, and the fallback copied state into it
        from unittest import mock
        victim, link = os.path.join(self.tmp, "ssh"), os.path.join(self.tmp, "fallback")
        os.makedirs(victim, mode=0o700)
        os.symlink(victim, link)
        real = os.lstat

        def lstat(path, *a, **k):
            st = real(path, *a, **k)
            return os.stat_result(tuple(st)[:4] + (os.getuid() + 1,) + tuple(st)[5:]) if str(path) == link else st
        default = os.path.join(self.home, "state")
        os.makedirs(default, exist_ok=True)
        os.chmod(self.home, 0o500)
        os.chmod(default, 0o500)
        try:
            with mock.patch.object(c, "state_fallbacks", lambda: [link]):
                with mock.patch.object(c.os, "lstat", lstat):
                    self.assertEqual(c.state_dir(), default, "someone else's link is never a fallback")
                self.assertEqual(os.listdir(victim), [])
                self.assertEqual(c.state_dir(), link, "a link of our own still is")
        finally:
            os.chmod(self.home, 0o700)
            os.chmod(default, 0o700)

    def test_a_marker_others_could_have_planted_is_ignored(self):
        # /tmp is shared: a marker in a dir other users can write would redirect all of this user's state.
        alt = os.path.join(self.tmp, "xdg", "foreman")
        os.makedirs(alt)
        with open(os.path.join(alt, ".foreman-state.json"), "w") as f:
            json.dump({"default": os.path.join(self.home, "state")}, f)
        os.chmod(alt, 0o777)
        self.assertEqual(c.state_dir(), os.path.join(self.home, "state"))
        os.chmod(alt, 0o755)
        self.assertEqual(c.state_dir(), alt)

    def test_restore_moves_fallback_state_back_once_the_default_is_writable(self):
        default = os.path.join(self.home, "state")
        c.init_project(self.repo)
        os.chmod(self.home, 0o500)
        os.chmod(default, 0o500)
        try:
            alt = c.state_dir()
            self.assertNotEqual(alt, default)
            with self.assertRaises(OSError):  # still read-only (the sandbox is still there): nothing moves
                c.restore_default_state()
            self.assertEqual(c.state_dir(), alt)
        finally:
            os.chmod(self.home, 0o700)
            os.chmod(default, 0o700)
        c.log_event(c.find_project(self.repo), "note", data={"in": "fallback"})
        self.assertEqual(c.restore_default_state(), default)
        self.assertEqual(c.state_dir(), default)
        self.assertTrue(any(e["event"] == "note" for e in c.ledger_tail(c.find_project(self.repo))))
        c.log_event(c.find_project(self.repo), "note", data={"in": "default"})
        os.chmod(self.home, 0o500)
        os.chmod(default, 0o500)
        try:  # a later fallback starts from the current default, not the stale copy left behind
            self.assertEqual(c.state_dir(), alt)
            self.assertIn({"in": "default"}, [e.get("data") for e in c.ledger_tail(c.find_project(self.repo))])
        finally:
            os.chmod(self.home, 0o700)
            os.chmod(default, 0o700)

    def test_worktree_id_tracks_edits_and_leaves_the_real_index_alone(self):
        f = os.path.join(self.repo, "README.md")
        index = os.path.join(self.repo, ".git", "index")
        before = c.worktree_id(self.repo)
        with open(index, "rb") as fh:
            idx = fh.read()
        with open(f, "w") as fh:  # same size, same second as the commit: stat data alone can't tell
            fh.write("# APP\n")
        after = c.worktree_id(self.repo)
        self.assertNotEqual(before, after)
        with open(os.path.join(self.repo, "new.py"), "w") as fh:
            fh.write("x = 1\n")
        self.assertNotEqual(after, c.worktree_id(self.repo), "untracked files count")
        with open(index, "rb") as fh:
            self.assertEqual(fh.read(), idx)
        subprocess.run(["git", "-C", self.repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.repo, "commit", "-qm", "x"], check=True)
        self.assertEqual(c.worktree_id(self.repo), c.worktree_id(self.repo))

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
        "export ANTHROPIC_API_KEY=sk-ant-api03-abcdefghijklmnop",  # pragma: allowlist secret
        "token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ012345",  # pragma: allowlist secret
        "curl -H 'Authorization: Bearer abc.def.ghi' https://x",
        "password=hunter2hunter2",
        "aws AKIAABCDEFGHIJKLMNOP",  # pragma: allowlist secret
        "git clone https://user:s3cretpass@github.com/x/y",  # pragma: allowlist secret
        "-----BEGIN OPENSSH PRIVATE KEY-----\nAAAA\n-----END OPENSSH PRIVATE KEY-----",  # pragma: allowlist secret
        "jwt eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",  # pragma: allowlist secret
    ]
    SECRETS = ["sk-ant-api03-abcdefghijklmnop", "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ012345", "abc.def.ghi",  # pragma: allowlist secret
               "hunter2hunter2", "AKIAABCDEFGHIJKLMNOP", "s3cretpass", "AAAA", "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"]  # pragma: allowlist secret

    def test_known_secret_shapes_are_redacted(self):
        for text, secret in zip(self.CASES, self.SECRETS):
            with self.subTest(text=text):
                out = c.redact(text)
                self.assertNotIn(secret, out)
                self.assertIn("REDACTED", out)

    def test_ordinary_text_is_untouched(self):
        for text in ["run pytest -q", "the token count is 400", "password field validation", "key: value"]:
            self.assertEqual(c.redact(text), text)

    def test_a_credential_named_json_key_is_redacted(self):  # T-1733
        for s in (json.dumps({"password": "hunter2x", "user": "ann"}), "{'api_key': 'abcd1234'}",  # pragma: allowlist secret
                  json.dumps(json.dumps({"client_secret": "s3cr3tvalue"})),  # pragma: allowlist secret
                  '"auth_token" : "zzzz9999"'):  # pragma: allowlist secret
            with self.subTest(s=s):
                out = c.redact(s)
                for secret in ("hunter2x", "abcd1234", "s3cr3tvalue", "zzzz9999"):
                    self.assertNotIn(secret, out)
                self.assertIn("REDACTED", out)
        self.assertIsInstance(json.loads(c.redact(json.dumps({"password": "hunter2x"}))), dict)  # pragma: allowlist secret
        self.assertEqual(c.redact('{"tokens": 1234, "token_count": "5000", "secret_kinds": "a JWT"}'),
                         '{"tokens": 1234, "token_count": "5000", "secret_kinds": "a JWT"}')

    def test_redact_obj_reads_key_names(self):  # T-1733: log_event stored {"password": "x"} as it was
        got = c.redact_obj({"password": "x", "nested": [{"apiKey": "abcd"}, {"AUTH_TOKEN": "t"}], "tokens": 400,
                            "subagent_tokens": 12, "token_count": 3, "secret_kinds": ["a JWT"], "pwd": None})
        self.assertEqual(got["password"], "[REDACTED]")
        self.assertEqual(got["nested"], [{"apiKey": "[REDACTED]"}, {"AUTH_TOKEN": "[REDACTED]"}])
        self.assertEqual((got["tokens"], got["subagent_tokens"], got["token_count"], got["secret_kinds"], got["pwd"]),
                         (400, 12, 3, ["a JWT"], None))

    def test_redacted_json_stays_valid(self):
        s = json.dumps({"cmd": "export TOKEN=abcd1234efgh && curl -H \"Authorization: Bearer xyz123\""})
        self.assertIsInstance(json.loads(c.redact(s)), dict)


class Ledger(ForemanTestCase):
    def test_lane_worktree_paths_map_to_repo_paths(self):
        # T-0807: builders edit in .claude/worktrees/<lane>/, so after the merge the close's scope check saw those
        # paths, not the repo files they stand for (T-0779, T-0786, T-0804 each needed a logged reason)
        p = c.init_project(self.repo)
        wt = os.path.join(p.root, ".claude", "worktrees", "agent-a1b2", "plugin", "lib", "a.py")
        c.log_event(p, "touched", task="T-0001", data={"file": wt})
        c.log_event(p, "touched", task="T-0001", data={"file": os.path.join(p.root, "README.md")})
        self.assertEqual(sorted(c.task_touches(p, "T-0001")), ["README.md", "plugin/lib/a.py"])

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
        self.assertEqual(set(rec), {"prev", "ts", "session_id", "project", "task", "event", "data"})  # T-1065: chained
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

    def test_plain_strips_hidden_characters_and_passes_printable_text_through(self):
        # T-2017: plain() checked every character in Python; printable text now skips the scan
        for bad in ("\x1b", "\x07", "\n", "‮", "​", " ", " ", "️", "\U000e0100"):
            self.assertEqual(c.plain(f"a{bad}b"), "ab", repr(bad))
        for good in ("café 日本 ✓", "a b", "x" * 500, ""):
            self.assertEqual(c.plain(good), good)
        self.assertEqual(c.plain(None), "")

    def test_sections_are_split_only_when_read_and_copies_stay_apart(self):
        # T-2015: a hook loads every brief but reads few past their frontmatter; splitting 9 MB of sections cost ~50 ms
        b = c.Brief.parse(SAMPLE)
        self.assertIsInstance(b._sections, str, "parse leaves the sections unsplit")
        self.assertEqual(b.title, "Fix login timeout on slow networks")
        x = b.copy()
        x.set_section("Log", "changed\n")
        self.assertEqual(b.render(), SAMPLE, "a copy's edit never reaches the original")
        self.assertIn("## Log\nchanged\n", x.render())
        self.assertIn("Add retry with backoff", b.section("Steps"))

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

    def _finished(self, tier, docs=True):
        b = c.Brief.new("T-0001", "Do a thing", "FEATURE", tier, now="2026-01-01T00:00:00Z")
        if docs and tier in ("M", "L"):
            b.set_section("Docs impact", "none: test fixture")
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

    def test_m_and_l_need_a_docs_impact_before_done(self):
        m = self._finished("M", docs=False)
        m.add_audit("intent", "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        m.add_audit("edge", "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        self.assertIn("docs impact", " ".join(m.done_blockers()))
        m.set_section("Docs impact", "none: internal refactor, no user-visible change")
        self.assertEqual(m.done_blockers(), [])
        s = self._finished("S")
        s.add_audit("self", "checklist", "ok", ts="2026-01-01T11:00:00Z")
        self.assertEqual(s.done_blockers(), [], "S tasks don't need it")

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


class BriefLines(unittest.TestCase):
    """T-1616: step and criterion lines parse in linear time (a lazy scan before \\s*$ was quadratic on a run of
    spaces: 20,000 took 1.5 s, and a pulled brief can hold one)."""

    def test_a_long_run_of_spaces_parses_fast_with_the_same_groups(self):
        import time
        for rx, line in ((c._STEP_RE, "1. [ ] a" + " " * 50000 + "b  <- CURRENT"), (c._AC_RE, "- [ ] a" + " " * 50000 + "b")):
            t = time.perf_counter()
            m = rx.match(line)
            self.assertLess(time.perf_counter() - t, 0.5)
            self.assertTrue(m.groups()[-2 if rx is c._STEP_RE else -1].endswith("b"))
        self.assertEqual(c._STEP_RE.match("1. [x] build it  <- CURRENT").groups(), ("1", "x", "build it", "  <- CURRENT"))
        self.assertEqual(c._STEP_RE.match("3. [X]  <- CURRENT").groups(), ("3", "X", "<- CURRENT", None))  # as before
        self.assertEqual(c._STEP_RE.match("3. [ ] <- CURRENT x").groups(), ("3", " ", "<- CURRENT x", None))
        self.assertEqual(c._AC_RE.match("- [x] a  b  ").groups(), ("x", "a  b"))
        self.assertEqual(c._AC_RE.match("- [ ]  ").groups(), (" ", ""))


class Stages(unittest.TestCase):
    """The harness derives stage and the one next required action from the brief itself (T-0012)."""

    def brief(self, tier="S", type_="FIX", status="planned"):
        b = c.Brief.new("T-0001", "Fix login", type_, tier, now="2026-01-01T00:00:00Z", status=status)
        return b

    def plan(self, b):
        b.set_section("Interpretation", "Reading 1: login times out on slow networks.\nReading 2: the server is slow.")
        b.set_section("Approach (options → choice → why)",
                      "1) retry with backoff 2) a longer timeout 3) a queue. Choice 1: cheapest.")
        b.set_section("Risks and rollback", "Retries pile up; revert the commit.")
        b.add_ac("login works on 3G", verify="pytest -k slow")
        b.add_step("reproduce")
        return b

    def test_plan_gaps_check_content_by_tier(self):  # T-2269
        def gaps(b):
            return " | ".join(c.plan_gaps(b, "full"))
        AP = "Approach (options → choice → why)"
        for tier in ("M", "L"):
            b = self.plan(self.brief(tier))
            self.assertEqual(c.plan_gaps(b, "full"), [])
            b.set_section(AP, "Retry with backoff vs longer timeout → retry. Choice: retry. In 2 steps, 3 files.")
            self.assertIn("3+ options", gaps(b))
            self.assertIn("fm task set", gaps(b))  # the gap names its fix
            for text in ("1. a\n2. b\n3. c\nChosen: a", "- a\n- b\n- c\nchose a", "Option A: a\nOption B: b\nOption C: c\nChoice: B"):
                b.set_section(AP, text)
                self.assertEqual(c.plan_gaps(b, "full"), [], text)
            b.set_section(AP, "1) a 2) b 3) c")
            self.assertIn("choice", gaps(b))
        m = self.plan(self.brief("M"))
        m.set_section("Interpretation", "One reading.")
        m.set_section("Risks and rollback", "")
        self.assertEqual(c.plan_gaps(m, "full"), [])  # M needs neither
        big = self.plan(self.brief("L"))
        big.set_section("Interpretation", "One reading.")
        self.assertIn("2+ readings", gaps(big))
        big.set_section("Interpretation", "1. this\n2. that")
        self.assertEqual(c.plan_gaps(big, "full"), [])
        big.set_section("Risks and rollback", "")
        self.assertIn("Risks and rollback", gaps(big))

    def test_a_low_confidence_assumption_waits_for_research_or_a_spike(self):  # T-2269
        b = self.plan(self.brief("M"))
        b.add_assumption("the API is paged (low)")
        self.assertIn("research", " ".join(c.plan_gaps(b, "full")))
        b.set_section(c.Brief.ASSUMPTIONS, "- [assumed] the API is paged (low)\n- [assumed] other (high)\n")
        self.assertIn("research", " ".join(c.plan_gaps(b, "full")))
        for line in ("- [assumed] the API is paged (low); see research/api-paging",
                     "- [assumed] the API is paged (low); spike T-0042",
                     "- [verified: ran it] the API is paged (low)"):
            b.set_section(c.Brief.ASSUMPTIONS, line + "\n")
            self.assertEqual(c.plan_gaps(b, "full"), [], line)
        s = self.brief("S")
        s.add_ac("works")
        s.add_step("do it")
        s.add_assumption("x (low)")
        self.assertIn("research", " ".join(c.plan_gaps(s, "full")))  # any tier

    def test_a_task_already_started_is_not_regated(self):  # T-2269
        b = self.plan(self.brief("L"))
        b.set_section("Approach (options → choice → why)", "just do it")
        b.add_assumption("x (low)")
        self.assertTrue(c.plan_gaps(b, "full"))
        for st in ("active", "verifying", "done"):
            b.meta["status"] = st
            self.assertEqual(c.plan_gaps(b, "full"), [], st)
        b.meta["status"] = "planned"  # a paused task is planned again: ever started is what exempts it
        self.assertTrue(c.plan_gaps(b, "full"))
        for key in ("plan0_at", "base", "base_tree"):
            q = self.plan(self.brief("L"))
            q.set_section("Approach (options → choice → why)", "just do it")
            q.meta[key] = "x"
            self.assertEqual(c.plan_gaps(q, "full"), [], key)
        q = self.plan(self.brief("L"))
        q.set_section("Approach (options → choice → why)", "just do it")
        q.add_evidence("true", "ok", step=1)
        q.mark_step(1)
        self.assertEqual(c.plan_gaps(q, "full"), [], "a done step")
        d = self.plan(self.brief("L"))
        d.set_section("Approach (options → choice → why)", "just do it")
        d.add_evidence("true", "ok", ac=1)
        self.assertEqual(c.plan_gaps(d, "full"), [], "evidence")

    def test_option_formats_and_hollow_markers(self):  # T-2269 review
        AP = "Approach (options → choice → why)"
        real = ("Options: (1) one (2) two (3) three Choice 2: two",
                "1) --bench on evidence 2) `fm bench` verb 3) \"last commit\" compare. Choice 1",  # T-2285: flags, code
                "1) one 2) two 3) three Choice 1",
                "Options: (A) a (B) b (C) c Choice: A",
                "A) a\nB. b\nC) c\nDecision: A",
                "Option A: a\nApproach B: b\nOption C: c\nGo with B",
                "**Option 1** a\n**Option 2** b\n### Option 3\nc\nChoose 1",
                "1. a 2. b 3. c Chosen: 1")
        for text in real:
            b = self.plan(self.brief("M"))
            b.set_section(AP, text)
            self.assertEqual(c.plan_gaps(b, "full"), [], text)
        for text in ("1) … 2) … 3) … Choice 1: …", "- …\n- …\n- …\nChoice: …", "Option A:\nOption B:\nOption C:\nChoice"):
            b = self.plan(self.brief("M"))
            b.set_section(AP, text)
            self.assertTrue(c.plan_gaps(b, "full"), text)
        b.set_section(AP, "1) a 2) b Choice 1")
        self.assertIn("names 2 options", " ".join(c.plan_gaps(b, "full")))
        self.assertIn("T-0001", " ".join(c.plan_gaps(b, "full")))
        big = self.plan(self.brief("L"))
        big.set_section("Interpretation", "A reading of the request that reads it once; reading it again changes nothing, reading.")
        self.assertIn("2+ readings", " ".join(c.plan_gaps(big, "full")))
        big.set_section("Interpretation", "- first\n- second")
        self.assertEqual(c.plan_gaps(big, "full"), [])

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

    def test_a_confirm_gap_says_why_the_task_waits(self):  # T-1750
        s = self.brief("S")
        s.add_ac("works")
        s.add_step("do it")
        s.meta["confirm"] = True
        self.assertIn("a child found this request in an old session", c.plan_gaps(s)[0])  # the default
        s.meta["confirm_why"] = "it arrived from the repo's .foreman/ (fm sync)\x1b[2J"
        gap = c.plan_gaps(s)[0]
        self.assertIn("it arrived from the repo's .foreman/ (fm sync)", gap)
        self.assertNotIn("\x1b", gap)

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
        self.assertIn("Skill foreman:debug-test", c.skill_for(b, c.stage(b)), "FIX names its procedure (T-1701)")
        self.assertNotIn("debug-test", nxt, "once a stage through the hooks, not on every step's line (T-1697)")
        b.add_evidence("pytest -k slow", "1 failed as expected", step=1, ts="2026-01-01T10:00:00Z")
        b.mark_step(1)
        self.assertEqual(c.stage(b), "verifying")
        self.assertIn("fm task finish T-0001", c.next_action(b), "finish runs the criterion's own check")
        b.add_evidence("pytest -k slow", "1 passed", ac=1)
        b.check_ac(1)
        self.assertEqual(c.stage(b), "documenting")
        self.assertIn("Docs impact", c.next_action(b))
        b.set_section("Docs impact", "README usage updated")
        self.assertEqual(c.stage(b), "auditing")
        self.assertIn("audit.md", c.next_action(b))
        b.add_audit("intent", "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        b.add_audit("edge", "fm-reviewer", "ok", ts="2026-01-01T11:00:00Z")
        self.assertEqual(c.stage(b), "closing")
        self.assertIn("fm task done T-0001", c.next_action(b))

    def test_every_skill_a_hint_loads_exists_and_the_model_may_load_it(self):
        # T-1701: FIX and RESEARCH name the job skills; a hint naming a missing or user-only skill sends Claude nowhere
        self.assertIn("Skill foreman:research", c.SKILL_FOR["RESEARCH"])
        for key, hint in c.SKILL_FOR.items():
            for name in re.findall(r"Skill foreman:([\w-]+)", hint):
                with self.subTest(key=key, skill=name):
                    path = os.path.join(c.PLUGIN_ROOT, "skills", name, "SKILL.md")
                    self.assertTrue(os.path.isfile(path))
                    with open(path, encoding="utf-8") as f:
                        self.assertNotIn("\ndisable-model-invocation: true", f.read())


    def test_next_moves_past_a_step_with_evidence_and_ends_at_finish(self):
        # T-0193: fm next said 'step 1/2 … fm task step done' until fm task finish marked the steps, with typed
        # evidence; fm usage: followed 2 of 7 times
        b = self.plan(self.brief("S"))
        b.add_step("fix it")
        b.meta["status"] = "active"
        b.add_evidence("pytest -k slow", "✗ exit 1", step=1)
        nxt = c.next_action(b)
        self.assertIn("step 2/2", nxt)
        self.assertIn("fm task evidence T-0001 --step 2 --run", nxt)
        b.add_evidence("pytest -k slow", "exit 0", step=2)
        self.assertIn("fm task finish T-0001", c.next_action(b))


class WorkRequests(unittest.TestCase):
    def test_plain_work_requests(self):
        for text in ("add a --verbose flag to the CLI", "fix the login timeout on slow wifi",
                     "Please refactor the date helpers", "can you rename add to add_numbers?"):
            with self.subTest(text=text):
                self.assertTrue(c.is_work_request(text))
        for text in ("what does this function do?", "yes", "FIX: login", "super improve it", "thanks!", ""):
            with self.subTest(text=text):
                self.assertFalse(c.is_work_request(text))


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
                self.assertFalse(c.is_exhaustive(text))
                self.assertFalse(c.is_broad(text))

    def test_real_phrasings_reach_the_brainstorm(self):
        # T-0364: the user's own words from Volt and Foreman sessions; none reached a brainstorm, so plans covered only
        # what came to mind first and the user asked for the rest one request at a time
        for text in ("can you make the language interop limitless? no caveats or non implemented things for rust, zig, "
                     "c, especially C++, etc.?",
                     "the recursive brainstorm isn't great, it doesn't think of every possible solution/capability",
                     "make it more featurefull", "support all possible shapes"):
            with self.subTest(text=text):
                self.assertTrue(c.is_exhaustive(text))
        for text in ("can you add even more benchmarks to compare against C/C++? like a lot more, not just simple things "
                     "either, like a ton of C++/C/Volt language features, truly showcasing the speed",
                     "add tons of tests for the parser"):
            with self.subTest(text=text):
                self.assertTrue(c.is_broad(text))
                self.assertFalse(c.is_exhaustive(text))
        for text in ("make it way better", "make the app much nicer"):
            with self.subTest(text=text):
                self.assertTrue(c.is_open_ended(text))
        for text in ("there's a lot of chat spam from your messages", "every test passes now", "no caveats here, ship it",
                     "is this a lot more readable?"):
            with self.subTest(text=text):
                self.assertFalse(c.is_exhaustive(text) or c.is_broad(text))

    def test_a_repo_cleanup_is_a_sweep(self):
        # T-0364: "clean up all docs, code, UI, settings, environment" was tiered S and closed after a few files
        for text in ("clean up all docs, code, UI, settings, environment stuff",
                     "clean up the repo, docs, briefs, dead code, unused functionality that's been replaced",
                     "remove dead code", "CLEAN: the whole codebase"):
            with self.subTest(text=text):
                self.assertTrue(c.is_sweep(text))
        for text in ("clean up the panel spacing", "fix the login timeout", "clean up after the test in test_io",
                     "clean up all of the panels, they still look weird"):
            with self.subTest(text=text):
                self.assertFalse(c.is_sweep(text))

    def test_a_long_request_with_a_work_verb_is_still_a_work_request(self):
        # T-0364: "can you make music-findr which is basically spot dl, but…" (90 words) got no intake note at all
        self.assertTrue(c.is_work_request("can you make a web app that " + "does one more thing and " * 20 + "works"))


class PlanOnly(unittest.TestCase):
    def test_plan_only_requests_hold_drive(self):
        for text in ("FIX: a\n\nCapture and plan these; don't implement anything yet.", "Just plan it.",
                     "Plan only, no code.", "don't implement yet", "Do not change anything for now.",
                     "only plan this", "no code yet please", "capture only"):
            with self.subTest(text=text):
                self.assertTrue(c.is_plan_only(text))

    def test_constraints_and_mentions_of_a_plan_do_not(self):
        for text in ("fix the login bug; don't change the API", "the plan only covers X", "don't write to the db",
                     "don't build a new parser, reuse the old one", "add retries, don't change anything else",
                     "is the plan first-class?", "the only plan we have is this one"):
            with self.subTest(text=text):
                self.assertFalse(c.is_plan_only(text))


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

    def test_an_at_path_line_under_an_item_scopes_it(self):
        # T-1989: an unindented "@path" line under an item went to untagged text, its scope lost
        r = c.parse_intake("FIX: totals are wrong\n@src/reports @src/csv.py\n  in every report\nFEATURE: export\n"
                           "DONE-WHEN: it opens\n@src/export.py\n  and keeps the header\n\n@stray/path")
        self.assertEqual(r.items[0].scopes, ["src/reports", "src/csv.py"])
        self.assertEqual(r.items[1].scopes, ["src/export.py"])
        self.assertEqual(r.untagged, "@stray/path")  # after a blank line it belongs to no item

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


class HookImportCost(unittest.TestCase):
    """Round 6: every tool call starts a hook process; traceback (~15 ms) and dataclasses (~9 ms) stay off its path."""

    def test_hook_modules_do_not_import_the_slow_ones(self):
        import subprocess
        import sys
        code = ("import sys; sys.path.insert(0, %r); import fmhooks, fmguard; "
                "print(sorted(m for m in ('traceback', 'dataclasses', 'inspect') if m in sys.modules))") % os.path.join(c.PLUGIN_ROOT, "lib")
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout.strip()
        self.assertEqual(out, "[]")

    def test_record_behaves_like_the_dataclasses_it_replaced(self):
        @c.record
        class R:
            a: int
            b: list = []
            c_: str = "x"
        r1, r2 = R(1), R(a=1)
        self.assertEqual(r1, r2)
        r1.b.append(5)
        self.assertEqual(r2.b, [], "list defaults are per instance")
        self.assertEqual(repr(R(2, [3], "y")), "R(a=2, b=[3], c_='y')")
        with self.assertRaises(TypeError):
            R()
        with self.assertRaises(TypeError):
            R(1, nope=2)
        self.assertNotEqual(R(1), R(2))


class RunCommand(unittest.TestCase):
    def test_a_pipe_cannot_hide_a_failing_test_run(self):
        # T-0773: 'unittest … | tail -3' exits with tail's 0; evidence read "exit 0 · FAILED (errors=1)" twice in a day
        root = os.path.dirname(__file__)
        for summary in ("FAILED (errors=1)", "FAILED (failures=2, errors=1)", "==== 3 failed, 10 passed in 1.2s ====",
                        "Tests:       1 failed, 4 passed, 5 total", "test result: FAILED. 3 passed; 1 failed",
                        "--- FAIL: TestX (0.00s)"):
            code, out = c.run_command(root, f"printf 'Ran 3 tests in 0.1s\\n\\n{summary}\\n' | tail -3")
            self.assertNotEqual(code, 0, summary)
            self.assertIn("reports failing tests", out)
        for ok in ("Ran 3 tests in 0.1s\\n\\nOK", "==== 10 passed in 1.2s ====", "test result: ok. 3 passed; 0 failed"):
            code, _ = c.run_command(root, f"printf '{ok}\\n' | tail -3")
            self.assertEqual(code, 0, ok)
        import tempfile  # the real producer, not a hand-written summary (T-0750's lesson)
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "test_x.py"), "w") as f:
                f.write("import unittest\nclass T(unittest.TestCase):\n    def test_a(self):\n        self.fail('no')\n")
            code, out = c.run_command(d, "python3 -m unittest test_x 2>&1 | tail -3")
            self.assertEqual(code, 1, out)

    def test_kill_group_takes_the_children_and_never_raises(self):
        # T-1094: fmbench's own killpg had no except, so a child that exited first crashed the bench
        import subprocess
        import time
        pr = subprocess.Popen(["sh", "-c", "sleep 30 & echo $!; wait"], stdout=subprocess.PIPE, text=True,
                              start_new_session=True)
        child = int(pr.stdout.readline())
        c.kill_group(pr)
        pr.wait(timeout=5)
        time.sleep(0.2)
        self.assertFalse(os.path.exists(f"/proc/{child}") and "Z" not in open(f"/proc/{child}/stat").read().split()[2])
        c.kill_group(pr)  # already gone: no exception
        done = subprocess.Popen(["true"], start_new_session=True)
        done.wait()
        c.kill_group(done)

    def test_a_run_never_inherits_the_test_skip_list(self):
        # T-1114: an exported FOREMAN_SKIP_TESTS would make an evidence run of run.py leave modules out silently
        from unittest import mock
        with mock.patch.dict(os.environ, {"FOREMAN_SKIP_TESTS": "test_guard"}):
            _, out = c.run_command(os.path.dirname(__file__), 'echo "skip=${FOREMAN_SKIP_TESTS:-none}"')
        self.assertIn("skip=none", out)


class NativeClaude(unittest.TestCase):
    def test_the_native_install_is_found_when_path_lacks_it(self):
        # T-0990: the npm claude was removed; the native one is in ~/.local/bin, which fm's shells didn't have
        import tempfile
        with tempfile.TemporaryDirectory() as home:
            local = os.path.join(home, ".local", "bin")
            os.makedirs(local)
            exe = os.path.join(local, "claude")
            with open(exe, "w") as f:
                f.write("#!/bin/sh\n")
            os.chmod(exe, 0o755)
            empty = os.path.join(home, "empty")  # never the host's PATH: its claude comes and goes
            os.makedirs(empty)
            env = {"HOME": home, "PATH": empty}
            self.assertEqual(c.claude_path(env)["PATH"].split(os.pathsep)[0], local)
            other = os.path.join(home, "other")
            os.makedirs(other)
            os.symlink(exe, os.path.join(other, "claude"))
            env = {"HOME": home, "PATH": other + ":" + empty}
            self.assertEqual(c.claude_path(env)["PATH"], other + ":" + empty, "one on PATH already wins")
            os.remove(exe)
            self.assertEqual(c.claude_path({"HOME": home, "PATH": empty})["PATH"], empty)


class ActiveFast(ForemanTestCase):
    def test_the_fast_active_brief_matches_the_full_scan(self):
        # T-1140: PreToolUse parsed every brief (1,069 here) to find the active one, half of each hook call
        self.fm("init")
        p = c.find_project(self.repo)
        for i in range(5):
            self.fm("task", "new", f"t{i}", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        self.assertIsNone(c.active_brief_fast(p))
        self.fm("focus", "T-0003")
        self.assertEqual(c.active_brief_fast(p).id, c.active_brief(c.load_briefs(p)).id)
        b = c.find_brief(p, "T-0004")
        b.meta.update(status="verifying", lane="/elsewhere")  # another lane's active task
        c.save_brief(p, b)
        self.assertEqual(c.active_brief_fast(p).id, "T-0003")
        self.assertEqual(c.active_brief_fast(p, "/elsewhere").id, "T-0004")
        self.assertIsNone(c.active_brief_fast(p, "/nowhere"))


class WaitWhile(unittest.TestCase):
    """T-2010: one wait for fm check and fm ship: says what it waits for, and when it stops waiting and goes ahead."""
    def test_wait_while_says_what_it_waits_for_and_when_it_gives_up(self):
        import io
        out = io.StringIO()
        self.assertFalse(c.wait_while(lambda: False, "x", "fm t", limit=1, out=out))
        self.assertEqual(out.getvalue(), "", "nothing running: no wait, no line")
        left = [2]

        def busy():
            left[0] -= 1
            return left[0] >= 0
        self.assertTrue(c.wait_while(busy, "a running fm check", "fm t", limit=30, out=out, step=0.01))
        self.assertIn("fm t: waiting for a running fm check to finish first (at most 30 seconds)", out.getvalue())
        self.assertNotIn("going ahead", out.getvalue())
        out = io.StringIO()
        t0 = time.time()
        self.assertTrue(c.wait_while(lambda: True, "the ambient test run", "fm t", limit=1, out=out, step=0.05))
        self.assertLess(time.time() - t0, 3)
        self.assertIn("the ambient test run is still running after 1 seconds; going ahead beside it", out.getvalue())


class LazyPatterns(unittest.TestCase):
    """T-2020: every hook spent ~25 ms compiling ~190 module-level patterns; a PreToolUse call uses about 44."""

    def test_lazy_importing_the_hook_modules_compiles_no_module_level_pattern(self):
        import sys
        from helpers import LIB
        code = ("import re, sys\nsys.path.insert(0, sys.argv[1])\norig, hits = re.compile, []\n"
                "def counting(*a, **k):\n"
                "    f = sys._getframe(1)\n"
                "    while f and f.f_code.co_name != '<module>':\n"
                "        f = f.f_back\n"
                "    name = f.f_code.co_filename.rsplit('/', 1)[-1] if f else ''\n"
                "    if name.startswith('fm'):\n"
                "        hits.append(f'{name}:{f.f_lineno}')\n"
                "    return orig(*a, **k)\n"
                "re.compile = counting\nimport fmcore, fmguard, fmhooks\nprint(hits)\n")
        out = subprocess.run([sys.executable, "-c", code, LIB], capture_output=True, text=True, timeout=60)
        self.assertEqual(out.stdout.strip(), "[]", out.stderr)

    def test_lazy_a_pattern_compiles_on_first_use_and_keeps_its_methods(self):
        rx = c.lazy(r"a+", re.I)
        self.assertEqual(rx.search("bAab").group(), "Aa")
        self.assertIs(rx.search, rx.search)  # compiled once, then a plain attribute
        self.assertEqual((rx.pattern, rx.flags & re.I), ("a+", re.I))

    def test_lazy_every_deferred_pattern_still_compiles(self):
        import fmguard
        import fmhooks
        found = []

        def walk(v):
            if type(v).__name__ == "lazy":
                found.append(v)
            elif isinstance(v, (list, tuple, set, frozenset)):
                for x in v:
                    walk(x)
            elif isinstance(v, dict):
                for x in v.values():
                    walk(x)
        for mod in (c, fmguard, fmhooks):
            for v in list(vars(mod).values()):
                walk(v)
        for rx in found:
            rx.flags  # a bad pattern raises re.error here, not at import
        self.assertGreater(len(found), 150)


class BriefIndex(ForemanTestCase):
    """T-2022: closed briefs load from a stat-checked index instead of 1,100+ file reads per hook."""

    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)
        for i in range(3):
            self.fm("task", "new", f"t{i}", "--type", "FIX", "--tier", "S", "--ac", "ok :: true", "--step", "s")
        b = c.find_brief(self.p, "T-0001")
        b.meta["status"] = "done"
        c.save_brief(self.p, b)
        self.age()
        c._BRIEF_MEMO.clear()

    def age(self, secs=60):
        for path in c.brief_paths(self.p):
            os.utime(path, (time.time() - secs, time.time() - secs))

    def opened(self, fn):
        from unittest import mock
        real, seen = open, []

        def spy(f, *a, **k):
            seen.append(str(f))
            return real(f, *a, **k)
        with mock.patch("builtins.open", spy):
            out = fn()
        c._BRIEF_MEMO.clear()
        return out, seen

    def test_brief_index_closed_briefs_load_without_opening_their_files(self):
        first = c.load_briefs(self.p)
        c._BRIEF_MEMO.clear()
        self.assertTrue(os.path.exists(os.path.join(self.p.dir, "briefs-index.json")))
        second, seen = self.opened(lambda: c.load_briefs(self.p))
        done = c.find_brief(self.p, "T-0001").path
        self.assertNotIn(done, seen)
        self.assertIn(c.find_brief(self.p, "T-0002").path, seen, "open briefs are read as before")
        for a, b in zip(first, second):
            self.assertEqual((a.id, a.meta, a.title, a.preamble), (b.id, b.meta, b.title, b.preamble))
            self.assertEqual(a.render(), b.render())
            self.assertEqual([list(x) for x in a.sections], [list(x) for x in b.sections])
        _, seen = self.opened(lambda: c.active_brief_fast(self.p))
        self.assertNotIn(done, seen, "the fast active scan skips indexed closed briefs too")

    def test_brief_index_an_edited_brief_is_read_again(self):
        c.load_briefs(self.p)
        c._BRIEF_MEMO.clear()
        path = c.find_brief(self.p, "T-0001").path
        with open(path, encoding="utf-8") as f:
            text = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace("# t0", "# renamed"))
        self.age(30)
        c._BRIEF_MEMO.clear()
        b = [x for x in c.load_briefs(self.p) if x.id == "T-0001"][0]
        self.assertEqual(b.title, "renamed")

    def test_brief_index_a_corrupt_index_is_ignored(self):
        want = [x.render() for x in c.load_briefs(self.p)]
        idx = os.path.join(self.p.dir, "briefs-index.json")
        name = os.path.basename(c.find_brief(self.p, "T-0001").path)
        for bad in ("{", "[]", '{"v":1,"e":[]}', json.dumps({"v": 1, "e": {name: [1]}}),
                    json.dumps({"v": 1, "e": {name: "x"}}), json.dumps({"v": 1, "e": {name: [1, 2, 3, [], ""]}})):
            with open(idx, "w", encoding="utf-8") as f:
                f.write(bad)
            c._BRIEF_MEMO.clear()
            self.assertEqual([x.render() for x in c.load_briefs(self.p)], want, bad)
            c._BRIEF_MEMO.clear()
            self.assertIsNone(c.active_brief_fast(self.p), bad)

    def test_brief_index_the_fast_scan_reads_only_the_closed_keys(self):
        # T-2031: once the small keys file exists, the fast scan never opens the 700 KB index
        c.load_briefs(self.p)
        c._BRIEF_MEMO.clear()
        keys, idx = (os.path.join(self.p.dir, n) for n in ("briefs-closed.json", "briefs-index.json"))
        done = c.find_brief(self.p, "T-0001")
        got, seen = self.opened(lambda: c.active_brief_fast(self.p))
        self.assertIsNone(got)
        self.assertNotIn(idx, seen)
        self.assertNotIn(done.path, seen)
        for bad in ("{", "[]"):  # unreadable: back to the index, still skipping the closed brief
            with open(keys, "w", encoding="utf-8") as f:
                f.write(bad)
            got, seen = self.opened(lambda: c.active_brief_fast(self.p))
            self.assertIsNone(got, bad)
            self.assertNotIn(done.path, seen, bad)
        os.remove(keys)
        c._BRIEF_MEMO.clear()
        c.load_briefs(self.p)
        self.assertTrue(os.path.exists(keys), "a missing keys file is written again")
        done.meta["status"] = "active"  # reopened: a stale key no longer matches, so the brief is read
        c.save_brief(self.p, done)
        self.age(30)
        c._BRIEF_MEMO.clear()
        self.assertEqual(c.active_brief_fast(self.p).id, "T-0001")

    def test_brief_index_a_just_written_brief_is_not_indexed(self):
        b = c.find_brief(self.p, "T-0002")
        b.meta["status"] = "done"
        c.save_brief(self.p, b)
        c._BRIEF_MEMO.clear()
        c.load_briefs(self.p)
        with open(os.path.join(self.p.dir, "briefs-index.json"), encoding="utf-8") as f:
            names = json.load(f)["e"]
        self.assertIn(os.path.basename(c.find_brief(self.p, "T-0001").path), names)
        self.assertNotIn(os.path.basename(b.path), names, "a same-tick rewrite could pass for it")

    def test_brief_index_a_stub_copies_edits_and_renders_like_a_parsed_brief(self):
        c.load_briefs(self.p)
        c._BRIEF_MEMO.clear()
        path = c.find_brief(self.p, "T-0001").path
        c._BRIEF_MEMO.clear()
        stub = [x for x in c.load_briefs(self.p) if x.id == "T-0001"][0]
        with open(path, encoding="utf-8") as f:
            text = f.read()
        full = c.Brief.parse(text, path)
        self.assertEqual(stub.copy().render(), text)
        for b in (stub, full):
            b.meta["status"] = "dropped"
            b.sections[0][1] += "more\n"
        self.assertEqual(stub.render(), full.render())
        stub2 = [x for x in c.load_briefs(self.p) if x.id == "T-0001"][0]
        stub2.sections = [["Only", "x\n"]]
        self.assertTrue(stub2.render().endswith("## Only\nx\n"))


class LaterImports(ForemanTestCase):
    """T-2023: every hook paid ~5 ms importing subprocess, shutil and glob, which an ordinary tool call never uses."""
    HEAVY = ("subprocess", "glob")  # not shutil: tempfile imports it, and the guard needs tempfile each call

    def loaded_after(self, event, payload):
        site = os.path.join(self.tmp, "report")
        os.makedirs(site, exist_ok=True)
        out = os.path.join(site, "loaded")
        with open(os.path.join(site, "sitecustomize.py"), "w") as f:
            f.write(f"import atexit, sys\natexit.register(lambda: open({out!r}, 'w').write("
                    f"' '.join(m for m in {self.HEAVY!r} if m in sys.modules)))\n")
        r = self.hook(event, payload, env={"PYTHONPATH": site})
        with open(out) as f:
            return r, f.read().split()

    def test_later_a_plain_tool_call_loads_no_heavy_module(self):
        self.fm("init")
        r, loaded = self.loaded_after("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": "ls"}})
        self.assertEqual((r.returncode, loaded), (0, []), r.stderr)

    def test_later_a_stand_in_imports_on_first_use_and_mocks_still_reach_callers(self):
        from unittest import mock
        s = c._Later("subprocess")
        self.assertIs(s.PIPE, subprocess.PIPE)
        with mock.patch("subprocess.run", return_value="patched"):
            self.assertEqual(s.run(["true"]), "patched")
        with mock.patch.object(c.subprocess, "run", return_value="via fmcore"):
            self.assertEqual(c.subprocess.run(["true"]), "via fmcore")
        self.assertIs(c.subprocess.run, subprocess.run)

    def test_later_claude_path_still_adds_the_native_folder_only_when_needed(self):
        native = os.path.join(self.tmp, "native")
        os.makedirs(native)
        claude = os.path.join(native, "claude")
        with open(claude, "w") as f:
            f.write("#!/bin/sh\n")
        os.chmod(claude, 0o755)
        env = c.claude_path({"FOREMAN_NATIVE_BIN": native, "PATH": "/nonexistent"})
        self.assertEqual(env["PATH"], native + os.pathsep + "/nonexistent")
        on = native + os.pathsep + "/usr/bin"
        self.assertEqual(c.claude_path({"FOREMAN_NATIVE_BIN": native, "PATH": on})["PATH"], on)
