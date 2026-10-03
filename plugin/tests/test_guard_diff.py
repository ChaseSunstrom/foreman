"""T-0160: the guard against real bash. Each corpus command runs in a bubblewrap sandbox (read-only /, a tmpfs /home, no
network) with logging stand-ins for rm, git and claude first on PATH; a dangerous call the stand-ins log that
check_bash didn't block is a bypass. Hand-tracing found four in a day; this finds the class mechanically."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import fmguard as g  # noqa: E402

PAYLOADS = {"rm": "rm -rf ~", "git": "git push --force origin main", "claude": "claude plugin install x@y"}
# shell forms the guard claims to read; computed command names and variables are out of scope (a documented limit)
FORMS = [
    "{p}", "true; {p}", "true && {p}", "false || {p}", "true | {p}", "true\n{p}",
    "for f in a; do {p}; done", "if true; then {p}; fi", "if false; then :; else {p}; fi", "if false; then :; elif true; then {p}; fi",
    "while true; do {p}; break; done", "until false; do {p}; break; done", "{ {p}; }", "( {p} )", "! {p}",
    "case a in a) {p};; esac", "f() { {p}; }; f", "coproc {p}",
    "echo $({p})", "echo \"$({p})\"", "echo `{p}`", "echo \"`{p}`\"", "x=$({p})", "echo $(echo $({p}))",
    "echo \"$(true; {p})\"", "echo $(( 1 )) $({p})",
    "true # c\n{p}", "cat <<EOF\n$({p})\nEOF", "cat <<EOF\n`{p}`\nEOF",
    "bash -c '{p}'", "sh -c \"{p}\"", "bash -c 'true; {p}'", "eval '{p}'", "eval \"{p}\"",
    "env {p}", "nohup {p} >/dev/null", "time {p}", "command {p}", "exec {p}", "timeout 5 {p}", "nice {p}",
    "setsid {p}", "trap '{p}' EXIT", "find . -maxdepth 0 -exec {p} \\;", "echo a | xargs -I@ {p}",
    "flock l {p}", "script -qc '{p}' /dev/null", "busybox sh -c '{p}'", "find . -maxdepth 0 -execdir {p} +",
]
STUB = '#!/bin/sh\nprintf "%s\\t%s\\n" "$(basename "$0")" "$*" >> "$FM_DIFF_LOG"\n'
HOME = "/home/sb"


def dangerous(line):
    name, _, args = line.partition("\t")
    words = args.split()
    if name == "rm":
        return any(w.startswith("-") and "r" in w.lower() for w in words) and any(
            w == HOME or w.startswith(HOME + "/") or w == "/" for w in words)
    if name == "git":
        return "push" in words and any(w in ("--force", "-f") or w.startswith("--force") for w in words)
    if name == "claude":
        return bool(words) and words[0] in ("plugin", "plugins", "mcp", "config")
    return False


@unittest.skipUnless(shutil.which("bwrap") and shutil.which("bash"), "needs bubblewrap and bash")
class GuardAgainstBash(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="fm-guard-diff-")
        self.bin, self.project, self.log = (os.path.join(self.tmp, x) for x in ("bin", "project", "log"))
        os.makedirs(self.bin)
        os.makedirs(self.project)
        for name in PAYLOADS:
            path = os.path.join(self.bin, name)
            with open(path, "w") as f:
                f.write(STUB)
            os.chmod(path, 0o755)
        self.ctx = g.Ctx(cwd=self.project, project_root=self.project, home=HOME,
                         foreman_home=os.path.join(self.tmp, "fhome"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_in_sandbox(self, cmd):
        open(self.log, "w").close()
        argv = ["bwrap", "--ro-bind", "/", "/", "--tmpfs", "/home", "--dir", HOME, "--bind", self.tmp, self.tmp,
                "--dev", "/dev", "--proc", "/proc", "--unshare-all", "--die-with-parent", "--chdir", self.project,
                "--setenv", "HOME", HOME, "--setenv", "PATH", f"{self.bin}:/usr/bin:/bin",
                "--setenv", "FM_DIFF_LOG", self.log, "bash", "-c", cmd]
        subprocess.run(argv, capture_output=True, timeout=10)
        with open(self.log) as f:
            return [ln.rstrip("\n") for ln in f if ln.strip()]

    def test_every_form_that_runs_a_dangerous_call_is_blocked(self):
        ran, bypasses = 0, []
        for kind, payload in PAYLOADS.items():
            for form in FORMS:
                cmd = form.replace("{p}", payload)
                calls = [c for c in self.run_in_sandbox(cmd) if dangerous(c)]
                if not calls:
                    continue
                ran += 1
                if not g.check_bash(cmd, self.ctx):
                    bypasses.append(f"{kind}: {cmd!r} ran {calls[0]!r}")
        self.assertGreater(ran, len(FORMS), "the stand-ins logged too little: the corpus would be vacuous")
        self.assertEqual(bypasses, [], "\n" + "\n".join(bypasses))


if __name__ == "__main__":
    unittest.main()
