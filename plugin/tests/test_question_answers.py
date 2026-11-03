"""T-2688 (M-13's need): each AskUserQuestion answer is a ledger row, so what the user takes, overrides or dismisses
can be learned from. The ledger held 55 approvals and no refusal: chat-ask declines were logged, questions never."""
import json
import os

from helpers import ForemanTestCase

from sampo import core as c
from sampo import hooks


class QuestionAnswers(ForemanTestCase):
    def setUp(self):
        super().setUp()
        self.fm("init")
        self.p = c.find_project(self.repo)

    def rows(self):
        path = os.path.join(self.p.dir, "ledger.jsonl")
        return [json.loads(x)["data"] for x in open(path, encoding="utf-8")
                if json.loads(x).get("event") == "question_answered"]

    def payload(self, answers):
        qs = [{"question": "Which store?", "header": "Store", "multiSelect": False,
               "options": [{"label": "SQLite (Recommended)"}, {"label": "Postgres"}]},
              {"question": "Ship now?", "header": "Ship", "multiSelect": False,
               "options": [{"label": "Yes"}, {"label": "No"}]},
              {"question": "Name?", "header": "Name", "multiSelect": False,
               "options": [{"label": "alpha"}, {"label": "beta"}]}]
        return {"tool_name": "AskUserQuestion", "tool_use_id": "q1", "session_id": "s", "cwd": self.repo,
                "tool_input": {"questions": qs, "answers": answers}, "tool_response": {}}

    def test_answers_split_into_default_other_and_typed(self):
        hooks.post_tool_use(self.payload({"Which store?": "SQLite (Recommended)", "Ship now?": "No",
                                            "Name?": "gamma, my own"}))
        (row,) = self.rows()
        self.assertEqual((row["asked"], row["default"], row["other"], row["typed"], row["dismissed"]),
                         (3, 1, 1, 1, False))
        self.assertEqual(row["headers"], ["Store", "Ship", "Name"])

    def test_a_dismissed_question_is_a_row(self):
        hooks.post_tool_use_failure(dict(self.payload({}), error="The user doesn't want to proceed"))
        (row,) = self.rows()
        self.assertEqual((row["asked"], row["dismissed"]), (3, True))

    def test_other_tools_log_nothing(self):
        hooks.post_tool_use({"tool_name": "Read", "tool_input": {"file_path": "x"}, "session_id": "s",
                               "cwd": self.repo})
        self.assertEqual(self.rows(), [])

    def test_outcomes_questions_counts_since_and_none_fails_when_any_was_asked(self):
        # T-2840: the 'stop asking me questions' steer (2026-11-03) needs a check fm decide --check can run
        self.assertEqual(self.fm("outcomes", "--questions", "--none").returncode, 0, "none asked yet")
        hooks.post_tool_use(self.payload({"Which store?": "SQLite (Recommended)", "Ship now?": "No"}))
        got = self.fm_json("outcomes", "--questions")
        self.assertEqual((got["calls"], got["asked"], got["default"], got["other"], got["dismissed"]), (1, 3, 1, 1, 0))
        self.assertEqual(self.fm("outcomes", "--questions", "--none", check=False).returncode, 1)
        later = self.fm_json("outcomes", "--questions", "--since", "2999-01-01")
        self.assertEqual(later["calls"], 0, "nothing at or after --since")
