"""T-2847: what Sampo says (hook notes, guard refusals, drive reasons, the Next: line, CLI hints) teaches `sampo <verb>`.
Matchers keep accepting fm (T-2845); only printed messages are checked here."""
import json
import os
import re
import unittest

from test_hooks import HookCase

OLD = re.compile(r"(?<![\w./-])fm (?:task|next|check|focus|ask|edit|quiet|find|prove|drive|lane|capture|checkpoint|"
                 r"gates|init|doctor|decide|autonomy|audit|batch|lease|status|sync|queue|outcomes|plugins|tidy)\b")


class Spelling(HookCase):
    def said(self, text, where):
        bad = sorted(set(OLD.findall(text)))
        self.assertEqual(bad, [], f"{where} still says fm: {bad}")

    def test_hook_notes_the_next_line_and_refusals_say_sampo(self):
        self.fm("init")
        self.task()
        self.said(self.ctx_of(self.hook("SessionStart", {"source": "startup"})), "SessionStart")
        self.said(self.fm("next").stdout, "fm next")
        edit = {"tool_name": "Edit", "tool_input": {"file_path": os.path.join(self.repo, "a.py")}, "session_id": "s2847"}
        for i in range(3):
            self.said(self.hook("PostToolUse", edit).stdout, f"PostToolUse {i}")
        # an out-of-scope or unplanned edit, a guard refusal and a drive Stop
        self.said(self.hook("PreToolUse", {"tool_name": "Bash", "session_id": "s2847",
                                           "tool_input": {"command": "git push origin main"}}).stdout, "guard refusal")
        self.said(self.hook("PreToolUse", {"tool_name": "Bash", "session_id": "s2847",
                                           "tool_input": {"command": "fm check | tail -3"}}).stdout, "gate pipe")
        self.fm("drive", "on")
        self.said(self.hook("Stop", {"session_id": "s2847"}).stdout, "drive Stop")
        self.said(self.hook("UserPromptSubmit", {"session_id": "s2847", "prompt": "add a feature"}).stdout, "prompt")

    def test_cli_hints_say_sampo(self):
        self.fm("init")
        for args in (("task", "done", "T-9999"), ("focus", "T-9999"), ("task", "show", "T-9999")):
            p = self.fm(*args, check=False)
            self.said(p.stdout + p.stderr, " ".join(args))


if __name__ == "__main__":
    unittest.main()
