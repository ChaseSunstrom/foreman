"""T-0957: idle stops are recorded and counted, plan mode holds the drive, prompts are logged (redacted, with the
permission mode; never in a sensitive project), and the first session after an upgrade says what's new once."""
import json
import os

from test_hooks import HookCase

import fmcore as c
import fmdoctor as d
import fmhooks


def parse(proc):
    return json.loads(proc.stdout) if proc.stdout.strip() else {}


class BoardHooks(HookCase):
    def stop(self, session="s1"):
        return parse(self.hook("Stop", {"last_assistant_message": "Paused here.", "session_id": session}))

    def events(self, name):
        return [e for e in c.ledger_tail(self.project(), 300) if e.get("event") == name]

    def test_a_stop_with_open_work_and_no_nudge_is_an_idle_stop_doctor_counts(self):
        self.fm("init")
        self.task()
        self.fm("drive", "off")
        self.assertIsNone(self.stop().get("decision"))
        self.assertEqual(len(self.events("idle_stop")), 1)
        self.assertIn("1 idle stop", d.check_idle_stops(self.project()).detail)
        self.fm("drive", "on")
        self.assertEqual(self.stop().get("decision"), "block")  # the drive nudged: not idle
        self.assertEqual(len(self.events("idle_stop")), 1)

    def test_plan_permission_mode_holds_the_drive(self):
        self.fm("init")
        self.task()
        self.hook("UserPromptSubmit", {"prompt": "carry on with it", "session_id": "s1", "permission_mode": "plan"})
        self.assertIsNone(self.stop().get("decision"))
        self.hook("UserPromptSubmit", {"prompt": "carry on with it", "session_id": "s1", "permission_mode": "default"})
        self.assertEqual(self.stop().get("decision"), "block")

    def test_prompts_are_logged_redacted_and_capped_with_the_mode_but_not_in_a_sensitive_project(self):
        self.fm("init")
        secret = "ghp_" + "a1B2" * 9
        self.hook("UserPromptSubmit", {"prompt": f"use {secret} " + "x" * 3000, "session_id": "s1",
                                       "permission_mode": "bypassPermissions"})
        ev = self.events("prompt")
        self.assertEqual(len(ev), 1)
        self.assertNotIn(secret, ev[0]["data"]["text"])
        self.assertLessEqual(len(ev[0]["data"]["text"]), 2000)
        self.assertEqual(ev[0]["data"]["mode"], "bypassPermissions")
        self.fm("sensitive", "on")
        self.hook("UserPromptSubmit", {"prompt": "private words", "session_id": "s1"})
        self.assertEqual(len(self.events("prompt")), 1)


class WhatsNew(HookCase):
    LOG = ("# Changelog\n\n## Unreleased\n- not yet\n\n## 9.9.9 — 2099-01-01\n- First thing.\n  - a detail\n"
           "- Second thing.\n\n## 9.9.8 — 2098-01-01\n- Old.\n")

    def test_bullets_of_one_version(self):
        self.assertEqual(fmhooks.whats_new("9.9.9", self.LOG), ["First thing.", "Second thing."])
        self.assertEqual(fmhooks.whats_new("1.0.0", self.LOG), [])

    def test_the_first_session_after_an_upgrade_says_whats_new_once(self):
        rev = fmhooks._rev()
        log = os.path.join(self.tmp, "CHANGELOG.md")
        with open(log, "w") as f:
            f.write(self.LOG.replace("9.9.9", rev))
        seen = os.path.join(c.state_dir(), "seen-version")
        self.assertIsNone(fmhooks._whats_new_note(log))  # a fresh install isn't an upgrade
        with open(seen, "w") as f:
            f.write("0.0.1")
        self.assertIsNone(fmhooks._whats_new_note(os.path.join(self.tmp, "missing.md")))  # no notes here: kept for later
        self.assertIsNone(fmhooks._whats_new_note(log, headless=True))  # a headless run never uses it up
        msg = fmhooks._whats_new_note(log)
        self.assertIn(f"Foreman {rev}", msg)
        self.assertIn("• First thing.", msg)
        self.assertIsNone(fmhooks._whats_new_note(log))  # once

    def test_session_start_carries_it_as_a_system_message(self):
        self.fm("init")
        with open(os.path.join(c.state_dir(), "seen-version"), "w") as f:
            f.write("0.0.1")
        first = parse(self.hook("SessionStart", {"source": "startup", "session_id": "s1"}))
        again = parse(self.hook("SessionStart", {"source": "startup", "session_id": "s1"}))
        self.assertNotIn("What's new", again.get("systemMessage", ""))
        self.assertTrue("What's new" in first.get("systemMessage", "") or not fmhooks.whats_new(
            fmhooks._rev(), open(os.path.join(os.path.dirname(c.PLUGIN_ROOT), "CHANGELOG.md")).read()))

    def test_a_stop_waiting_on_background_work_isnt_idle(self):
        self.fm("init")
        self.task()
        self.hook("UserPromptSubmit", {"prompt": "go", "session_id": "s1"})
        out = parse(self.hook("Stop", {"last_assistant_message": "waiting", "session_id": "s1",
                                       "background_tasks": [{"id": "bg1", "type": "agent"}], "stop_hook_active": True},
                                 env={"FOREMAN_DRIVE_TASK": "T-0001"}))  # fm run: the drive waits, returns nothing
        self.assertIn("waits for background work", out.get("systemMessage", ""))
        self.assertEqual([e for e in c.ledger_tail(self.project(), 300) if e.get("event") == "idle_stop"], [])
