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
    "echo a#b; {p}", "echo a#b && {p}",  # T-0161 review: a # inside a word is no comment
    "echo $(true)#x; {p}", "echo $((1))#x; {p}", "echo `true`#x; {p}", "echo ${HOME}#x; {p}",  # T-0163: nor after ) ` }
    "echo '<<EOF'\n{p}\nEOF", "echo \"x <<EOF\"\n{p}", "echo '<<-EOF' && {p}",  # T-0178: a quoted marker is text
]
# whole commands (no payload slot): variables the guard resolves (T-0151) must still resolve the way bash does
EXTRA = ['D=~; rm -rf "$D"', 'D=/; false && D=x; rm -rf "$D"', 'D=/; (D=x); rm -rf "$D"', 'D=x; D=~; rm -rf "$D"',
         'export D=~\nrm -rf "${D}"', 'D=~ ; rm -rf "$D/"',
         # T-0161 (security review of T-0151): ways bash changes a variable that a plain NAME=value doesn't show
         'D=x; D[0]=~; rm -rf "$D"', 'D=; D+=~; rm -rf "$D"', 'D=x; command export D=~; rm -rf "$D"',
         'D=x; builtin declare D=~; rm -rf "$D"', 'D=x; ! D=~; rm -rf "$D"', 'D=x; time D=~; rm -rf "$D"',
         'PWD=x; cd ~; rm -rf "$PWD"', 'OLDPWD=x; cd ~; cd /; rm -rf "$OLDPWD"', '_=x; true ~; rm -rf "$_"',
         'D=x; trap \'D=~\' DEBUG; rm -rf "$D"', 'D="a /home/sb"; rm -rf $D', 'IFS=x; D=ax/home/sb; rm -rf $D',
         'BASH_REMATCH=x; [[ ~ =~ .* ]]; rm -rf "$BASH_REMATCH"', 'D=x; D=~ :; rm -rf "$D"',
         'D=x; D=~ export Y; rm -rf "$D"', 'D=x; set -o posix; D=~ :; rm -rf "$D"',
         'shopt -s expand_aliases\nalias s=\'D=~\'\nD=x\ns\nrm -rf "$D"', 'D=x; wait -p D; rm -rf "$D"',
         'D=x; DIRSTACK=x; pushd ~; rm -rf "$DIRSTACK"', 'D=x; local D=~; rm -rf "$D"',
         # its review: words that read as an assignment once quotes are gone, but that bash runs as a command
         'D=~; command D=/tmp/x; rm -rf "$D"', 'D=~; builtin D=/tmp/x; rm -rf "$D"', 'D=~; "D=/tmp/x"; rm -rf "$D"',
         'D=~; \\D=/tmp/x; rm -rf "$D"', 'D=~; D"="/tmp/x; rm -rf "$D"', 'D=~; "time" D=/tmp/x; rm -rf "$D"',
         'D=~; echo "x D=y"; "D=/tmp/x"; rm -rf "$D"', 'readonly D=~; D=/tmp/x; rm -rf "$D"',
         'D=/tmp/x; >o read D <<< ~; rm -rf "$D"',
         # T-0162 (automated review of T-0161): a command name bash computes can turn out to be a builtin
         'D=/tmp/x; X=read; $X D <<< ~; rm -rf "$D"', 'D=/tmp/x; `echo read` D <<< ~; rm -rf "$D"',
         'D=/tmp/x; touch read; rea? D <<< ~; rm -rf "$D"',
         # T-0175: a chain joined only by && is read in order too
         'D=x && D=~ && rm -rf "$D"', 'D=~ && D=/tmp/x true && rm -rf "$D"', 'D=/tmp/x&&D=~&&rm -rf "$D"',
         'D=~ && D=/tmp/x 2>/dev/null && rm -rf "$D"', 'D=/tmp/x && cd ~ && rm -rf "$PWD"',
         'D=/tmp/x && D=~ & wait; rm -rf "$D"', 'D=~ && D=/tmp/x || true && rm -rf "$D"']
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
        for cmd in EXTRA:
            calls = [c for c in self.run_in_sandbox(cmd) if dangerous(c)]
            if calls and not g.check_bash(cmd, self.ctx):
                bypasses.append(f"extra: {cmd!r} ran {calls[0]!r}")
        self.assertGreater(ran, len(FORMS), "the stand-ins logged too little: the corpus would be vacuous")
        self.assertEqual(bypasses, [], "\n" + "\n".join(bypasses))


if __name__ == "__main__":
    unittest.main()
