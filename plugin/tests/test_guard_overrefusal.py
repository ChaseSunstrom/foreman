"""T-2665: three over-refusals the friction pass found: git apply's read-only flags, a sys.path literal, a bare .ssh."""
from helpers import ForemanTestCase  # noqa: F401  (puts plugin/lib on the path)
from test_guard import GuardCase


class GitApply(GuardCase):
    def test_read_only_flags_allowed_plain_apply_blocked(self):
        for flag in ("--check", "--stat", "--numstat", "--summary", "--check --stat"):
            with self.subTest(flag=flag):
                self.assertIsNone(self.bash(f"git apply {flag} x.diff", cwd=self.fhome))
        for cmd in ("git apply x.diff", "git apply --stat --apply x.diff", "git apply --check --index x.diff",
                    "git apply x.diff --check --reverse"):
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(self.bash(cmd, cwd=self.fhome), cmd)


class SysPath(GuardCase):
    LIB = "{fhome}/plugin/lib"

    def test_sys_path_literal_is_not_a_write_target(self):
        for call in ("insert(0, '%s')", "append('%s')"):
            code = "import sys; sys.path." + (call % self.LIB) + "; print(1)"
            with self.subTest(call=call):
                self.assertIsNone(self.bash(f'python3 -c "{code}"', cwd=self.repo))

    def test_heredoc_that_writes_elsewhere_is_not_refused_for_its_sys_path(self):
        # the shape the guard ledger refused 7 times: a heredoc that puts plugin/lib on sys.path and writes a scratch file
        code = ("python3 - <<'EOF'\nimport sys\nsys.path.insert(0, '%s')\nopen('%s/out.txt', 'w').write('x')\nEOF"
                % (self.LIB, "{repo}"))
        self.assertIsNone(self.bash(code, cwd=self.repo))

    def test_same_literal_opened_for_write_still_blocks(self):
        code = "import sys; sys.path.insert(0, '%s'); open('%s/x.py', 'w').write('1')" % (self.LIB, self.LIB)
        self.assertIsNotNone(self.bash(f'python3 -c "{code}"', cwd=self.repo))
        code = "import sys; sys.path.insert(0, '%s'); open('%s', 'w').write('1')" % (self.LIB, self.LIB)
        self.assertIsNotNone(self.bash(f'python3 -c "{code}"', cwd=self.repo))


class HeredocFilterTail(GuardCase):
    """T-2261: a heredoc fed to python with `2>&1 | tail` after it was read as shell text, so a module named in test
    text or a quoted tower path blocked it (28 blocks in 7 days). Read-only filters keep it fed; every other tail doesn't."""
    TEXT = "import json\ns = \"from fmcore import save_brief\\nsave_brief(x)\"\nprint(json.dumps(s))"
    TOWER = "s = open('{fhome}/state/projects/x/notes.txt').read()\nopen('{repo}/out.txt', 'w').write(s)"
    READ_ONLY = ("2>&1", "| tail -5", "2>&1 | tail -20", "2>&1 | head -n 50", "| grep -E 'ok|FAIL' | wc -l",
                 "| cut -d: -f1 | sort -u | uniq -c", "| sort -k2 -n -r", "2>&1 | grep -v \"^#\" | tail -n 3")

    def run_py(self, body, tail="", pre=""):
        return self.bash(f"{pre}python3 - <<'EOF' {tail}\n{body}\nEOF", cwd=self.repo)

    def test_read_only_filter_tail_judged_as_python(self):
        for body in (self.TEXT, self.TOWER):
            self.assertIsNone(self.run_py(body), body)  # the baseline: the same heredoc with nothing after it
            for tail in self.READ_ONLY:
                with self.subTest(body=body[:20], tail=tail):
                    self.assertIsNone(self.run_py(body, tail))

    def test_other_tails_stay_refused(self):
        for tail in ("| sh", "| bash", "| python3", "| tee out.txt", "| xargs echo", "| sed -i s/a/b/ f.txt",
                     "| tail -5 > out.txt", "2>&1 | tail -5 >> out.txt", "; tail -5", "&& tail -5", "|| tail -5",
                     "| grep `echo x`", "| grep $(echo x)", "| grep \"$X\"", "| grep *", "| sort -o out.txt",
                     "| sort -uo out.txt", "| sort --compress-program=sh", "| sort --out=o.txt", "| uniq - out.txt",
                     "| uniq -c out.txt", "| tail -5 # note", "|& tail -5",
                     # review: after `--` uniq's second name is its output file, whatever it starts with
                     "| uniq -- - -d/../.bashrc", "| uniq - -", "| uniq -c --",
                     # review: a following tail never ends
                     "| tail -f", "| tail -F", "| tail -n5 -f", "| tail --follow=name", "| tail -n 3 '-f'",
                     "| tail --fo"):
            with self.subTest(tail=tail):
                self.assertIsNotNone(self.run_py(self.TEXT, tail))

    def test_redefined_filter_or_second_heredoc_stays_refused(self):
        for pre in ("tail() {{ sh; }}\n", "function tail {{ sh; }}\n", "PATH=/tmp/x:$PATH\n", "alias tail=sh\n",
                    "eval 'x'\n", "source ./env.sh\n", ". ./env.sh\n", "hash -p /bin/sh tail\n", "enable -n tail\n",
                    # review: the hash and alias tables by name, and builtins spelled with quotes or backslashes
                    "BASH_CMDS[tail]=/tmp/e.sh\n", "BASH_ALIASES[tail]=sh\n", "e\\val 'tail(){{ sh; }}'\n",
                    "ev\"\"al 'tail(){{ sh; }}'\n", "s\\ource ./env.sh\n", "'.' ./env.sh\n", "\\. ./env.sh\n",
                    "'tail'(){{ sh; }}\n"):  # bash 5 rejects a quoted function name; refused all the same
            with self.subTest(pre=pre):
                self.assertIsNotNone(self.run_py(self.TEXT, "| tail -5", pre))
        two = "python3 - <<'EOF' 2>&1 | grep -f - <<'B'\n" + self.TEXT + "\nEOF\nx\nB"
        self.assertIsNotNone(self.bash(two, cwd=self.repo))

    def test_writer_bodies_stay_refused_behind_a_filter(self):
        for body in ("import fmcore\nopen('{fhome}/plugin/lib/x.py', 'w').write('1')",
                     "from fmcore import save_brief\nsave_brief('x')",
                     "open('{fhome}/state/projects/x/tasks.json', 'w').write('1')"):
            with self.subTest(body=body):
                self.assertIsNotNone(self.run_py(body, "2>&1 | tail -5"))


class BareCredName(GuardCase):
    """T-2665: kept fail-closed. Exempting code that calls no listed read API failed open (io.FileIO, linecache and
    fileinput read a file with none of them), so a credential name beside the home folder still blocks, text test or not."""

    def test_any_credential_name_beside_home_still_blocks(self):
        for cmd in ("python3 -c \"import os; print(open(os.path.join('{home}', '.ssh', 'id_rsa')).read())\"",
                    "python3 -c \"print(open('{home}/.ssh/id_rsa').read())\"",
                    "python3 -c \"import os; os.listdir('{home}'); print('.ssh')\"",
                    "python3 -c \"import io; print(io.FileIO('{home}' + '/.ssh/' + 'id_rsa').read())\"",
                    "python3 -c \"import linecache; print(linecache.getlines('{home}' + '/.ssh/' + 'id_rsa'))\"",
                    "python3 -c \"import sys; print('.ssh' in sys.argv[0], '{home}')\""):
            with self.subTest(cmd=cmd):
                self.assertBlocked(self.bash(cmd, cwd=self.repo), "credentials")


class PrintfFirstWord(GuardCase):
    """T-3223: printf sets a variable only through -v as its first word; a later -v (command -v inside a substitution
    among its arguments) beside an unquoted $t was refused as 'IFS may be changed' though nothing names IFS."""

    def test_a_later_dash_v_in_printfs_arguments_passes(self):
        for cmd in ('for t in podman docker bwrap; do printf "%s=%s " $t "$(command -v $t || echo -)"; done; echo',
                    "printf '%s\\n' $x \"$(command -v $x)\"", 'printf "%s -v %s" $a $b'):
            with self.subTest(cmd=cmd):
                self.assertIsNone(self.bash(cmd, cwd=self.repo))

    def test_a_computed_or_hidden_dash_v_stays_refused(self):
        name = '"$(echo SFI | rev)"'
        for cmd in (f"printf -v {name} /; ls $x", f'printf "-v" {name} /; ls $x', f"printf '-v' {name} /; ls $x",
                    f"X=-v; printf $X {name} /; ls $x", f"printf {{{{-v,{name}}}}} /; ls $x",  # the helper formats {…}
                    f"printf `echo -v` {name} /; ls $x", f"true; printf -v{name} /; ls $x"):
            with self.subTest(cmd=cmd):
                self.assertBlocked(self.bash(cmd, cwd=self.repo), "system")
