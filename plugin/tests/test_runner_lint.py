"""T-1395: a code.toml runner that turns its CLI's own approvals off waits for an acknowledgement of its exact template;
fm code runners grades whether Foreman's guard confines each runner's shell; a link-local model endpoint is refused."""
import hashlib
import json
import os
import subprocess
import sys
import unittest

from helpers import ForemanTestCase
import fmcode
import fmmodels

FM = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin", "fm")


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


class RunnerLint(ForemanTestCase):
    def conf(self, text):
        with open(os.path.join(self.home, "code.toml"), "w") as f:
            f.write(text)

    def test_each_dangerous_flag_is_refused_until_acknowledged(self):
        for tpl in ("gemini --yolo -p {prompt}", "claude -p {prompt} --dangerously-skip-permissions",
                    "codex exec --sandbox danger-full-access {prompt}", "codex exec -s=danger-full-access {prompt}",
                    "codex exec --dangerously-bypass-approvals-and-sandbox {prompt}",
                    "claude -p {prompt} --permission-mode bypassPermissions",
                    # review: the shell joins quoted pieces into the real flag; --flag=value forms
                    'claude -p {prompt} --dangerously"-skip-permissions"', "claude -p {prompt} --yolo=true",
                    "gemini --approval-mode yolo -p {prompt}", "gemini --approval-mode=yolo -p {prompt}",
                    "gemini -y -p {prompt}", "/opt/bin/gemini -p {prompt} -y",
                    "codex exec -a never {prompt}", "codex exec --ask-for-approval never {prompt}",
                    "codex exec --ask-for-approval=never {prompt}",
                    'codex exec -c sandbox_mode="danger-full-access" {prompt}',
                    """codex exec -c 'approval_policy="never"' {prompt}"""):
            with self.subTest(tpl=tpl):
                body = json.dumps(tpl)[1:-1]  # as a TOML basic string
                self.conf(f'[runners.mine]\nwork = "{body}"\n')
                with self.assertRaises(fmcode.CodeError) as e:
                    fmcode.all_runners()
                self.assertIn(f'mine = "{sha(tpl)}"', str(e.exception), "it prints the exact line to add")
                self.assertIn("[ack]", str(e.exception))
                self.conf(f'[runners.mine]\nwork = "{body}"\n[ack]\nmine = "{sha(tpl)}"\n')
                self.assertEqual(fmcode.all_runners()["mine"]["work"], tpl)

    def test_gemini_y_is_only_a_flag_for_gemini_and_safe_lookalikes_pass(self):
        for tpl in ("mycli -y {prompt}", "codex exec -a on-request {prompt}", "gemini --approval-mode auto_edit -p {prompt}",
                    "mycli --yolo-not {prompt}", "codex exec --sandbox workspace-write {prompt}"):
            with self.subTest(tpl=tpl):
                self.conf(f'[runners.mine]\nwork = "{tpl}"\n')
                self.assertIn("mine", fmcode.all_runners())

    def test_a_changed_template_voids_the_acknowledgement(self):
        old = "gemini --yolo -p {prompt}"
        self.conf(f'[runners.mine]\nwork = "gemini --yolo --debug -p {{prompt}}"\n[ack]\nmine = "{sha(old)}"\n')
        with self.assertRaises(fmcode.CodeError):
            fmcode.all_runners()
        self.conf(f'[runners.other]\nwork = "{old}"\n[ack]\nmine = "{sha(old)}"\n')
        with self.assertRaises(fmcode.CodeError, msg="an ack is for one runner's name"):
            fmcode.all_runners()

    def test_a_dangerous_plan_needs_its_own_hash_too(self):
        work, plan = "gemini --yolo -p {prompt}", "gemini --yolo --approval-mode plan -p {prompt}"
        self.conf(f'[runners.mine]\nwork = "{work}"\nplan = "{plan}"\n[ack]\nmine = "{sha(work)}"\n')
        with self.assertRaises(fmcode.CodeError):
            fmcode.all_runners()
        self.conf(f'[runners.mine]\nwork = "{work}"\nplan = "{plan}"\n[ack]\nmine = ["{sha(work)}", "{sha(plan)}"]\n')
        self.assertEqual(fmcode.all_runners()["mine"]["plan"], plan)

    def test_a_safe_template_and_the_builtins_need_no_ack(self):
        self.conf('[runners.mine]\nwork = "mycli --yolo-not {prompt}"\n')
        self.assertIn("mine", fmcode.all_runners())
        self.conf('[runners.mine]\nwork = "mycli --auto {prompt}"\n')
        self.assertIn("claude", fmcode.all_runners())

    def grades(self, *args):
        env = dict(os.environ, FOREMAN_HOME=self.home, FOREMAN_INHIBITED="1")
        r = subprocess.run([sys.executable, FM, "code", "runners", *args], cwd=self.repo, env=env,
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return {x["name"]: x["guard"] for x in json.loads(r.stdout)["runners"]} if args else r.stdout

    def test_runners_json_grades_the_guard_per_runner(self):
        self.conf('[runners.mine]\nwork = "mycli {prompt}"\n[runners.wrap]\nwork = "/usr/bin/claude -p {prompt}"\n')
        got = self.grades("--json")
        self.assertEqual(got["claude"], "confined", "the built-in claude runs with Foreman's guard as --settings")
        self.assertEqual(got["wrap"], "not confined", "a template of the user's own gets no guard settings")
        for n in ("codex", "gemini", "mine", "opencode"):
            self.assertEqual(got[n], "not confined", n)
        self.assertIn("guard doesn't confine", self.grades())

    def test_what_drops_the_guard_settings_drops_the_grade(self):
        for conf in ('lean = false\n', '[runners.claude]\nwork = "claude -p {prompt} --permission-mode acceptEdits"\n',
                     'lean = "x"\n'):
            with self.subTest(conf=conf):
                self.conf(conf)
                self.assertEqual(self.grades("--json")["claude"], "not confined")

    def test_bare_drops_the_grade(self):
        r = dict(fmcode.RUNNERS["claude"], work=fmcode.RUNNERS["claude"]["work"] + " --bare")
        self.assertEqual(fmcode._guard_grade("claude", r), "not confined")
        self.assertEqual(fmcode._guard_grade("claude", fmcode.RUNNERS["claude"]), "confined")

    def test_the_tui_picker_says_what_is_wrong_in_code_toml(self):
        import fmcodetui
        self.conf('[runners.mine]\nwork = "gemini --yolo -p {prompt}"\n')
        real, fmmodels.profiles = fmmodels.profiles, lambda: [{"name": "local"}]
        try:
            app = fmcodetui.App(fmcodetui.DEFAULTS, spawn=lambda *a, **k: None)
            app.show_picker()
        finally:
            fmmodels.profiles = real
        self.assertEqual(app.items, [("model", "local")], "the models still list")
        self.assertIn("[ack]", app.message)
        self.assertNotIn("no models", app.message)


class LinkLocal(unittest.TestCase):
    def test_link_local_base_urls_are_refused_before_any_request(self):
        for url in ("http://169.254.169.254/v1", "https://169.254.0.1", "http://[fe80::1]/v1",
                    "http://[::ffff:169.254.169.254]/v1", "http://2852039166/v1", "http://0xa9.0xfe.0xa9.0xfe/",
                    "http://１６９.２５４.１６９.２５４/", "http://169。254。169。254/", "http://169．254．169．254/",
                    "http://[fd00:ec2::254]/", "http://[FD00:EC2::254]/latest"):
            with self.subTest(url=url):
                with self.assertRaises(fmmodels.ModelError) as e:
                    fmmodels.complete({"name": "x", "kind": "openai", "base_url": url, "model": "m"},
                                      [{"role": "user", "content": "hi"}], timeout=1)
                self.assertIn("link-local", str(e.exception))

    def test_ordinary_hosts_pass_the_check(self):
        for url in ("http://127.0.0.1:1/v1", "https://api.example.com/v1", "http://10.0.0.5/v1"):
            fmmodels._check_url({"name": "x"}, url, None)


if __name__ == "__main__":
    unittest.main()
