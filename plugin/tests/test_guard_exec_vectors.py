"""T-0275: commands that run a hidden command (exec options, code-loading variables, script files) are read like
bash -c; a payload the guard can't read is refused, a harmless look-alike passes."""
import json
import os
from unittest import mock

from test_guard import GuardCase, g
from test_hooks import HookCase


class ExecVectors(GuardCase):
    def test_exec_options_with_a_dangerous_payload_are_refused(self):
        self.run_table([
            ("tar -xf a.tar --to-command='rm -rf ~'", "rm-outside"),
            ("tar -xf a.tar --use-compress-program='rm -rf ~'", "rm-outside"),
            ("tar -xf a.tar -I 'rm -rf ~'", "rm-outside"),
            ("tar -cf a.tar x --checkpoint=1 --checkpoint-action=exec='rm -rf ~'", "rm-outside"),
            ("ssh -o ProxyCommand='rm -rf ~' host", "rm-outside"),
            ("ssh -oLocalCommand='rm -rf ~' -o PermitLocalCommand=yes host", "rm-outside"),
            ("ssh -F /tmp/evil.conf host", "system"),
            ("scp -o 'ProxyCommand rm -rf ~' a host:b", "rm-outside"),
            ("rsync -av -e 'rm -rf ~' a host:b", "rm-outside"),
            ("rsync -av --rsh='rm -rf ~' a host:b", "rm-outside"),
            ("zip -T -TT 'rm -rf ~' a.zip x", "rm-outside"),
            ("less '+!rm -rf ~' file", "rm-outside"),
            ("vim -c '!rm -rf ~' file", "rm-outside"),
            ("nvim '+r !rm -rf ~' file", "rm-outside"),
            ("sed 'e rm -rf ~' file", "rm-outside"),
            ("sed -n '1e rm -rf ~' file", "rm-outside"),
            ("sed 's/a/rm -rf ~/e' file", "system"),
        ], self.bash)

    def test_code_loading_variables_are_refused(self):
        self.run_table([
            ("PROMPT_COMMAND='rm -rf ~' bash -i", "rm-outside"),
            ("LESSOPEN='|rm -rf ~' less f", "rm-outside"),
            ("LD_PRELOAD=/tmp/x.so ls", "system"),
            ("export LD_AUDIT=/tmp/x.so; ls", "system"),
            ("NODE_OPTIONS='--require /tmp/x.js' node a.js", "system"),
            ("NODE_OPTIONS=--import=/tmp/x.mjs node a.js", "system"),
            ("PERL5OPT=-M/tmp/x perl a.pl", "system"),
            ("RUBYOPT=-r/tmp/x ruby a.rb", "system"),
            ("JAVA_TOOL_OPTIONS=-javaagent:/tmp/x.jar java -jar a.jar", "system"),
            ("_JAVA_OPTIONS='-Xmx1g -javaagent:/tmp/x.jar' java -jar a.jar", "system"),
        ], self.bash)

    def test_harmless_look_alikes_pass(self):
        self.run_table([
            ("tar -I zstd -cf a.tar.zst x", None),
            ("tar --use-compress-program=pigz -cf a.tgz x", None),
            ("tar -xf a.tar --checkpoint=100 --checkpoint-action=echo=done", None),
            ("ssh host", None),
            ("ssh -o StrictHostKeyChecking=no -o ProxyCommand=none host", None),
            ("rsync -av a host:b", None),
            ("rsync -av -e 'ssh -p 2222' a host:b", None),
            ("zip -r a.zip x", None),
            ("less file", None),
            ("sed -e 's/a/b/' file", None),
            ("sed -n '/e/p;s/e/x/g' file", None),
            ("vim file", None),
            ("vim -c 'wq!' file", None),
            ("NODE_OPTIONS=--max-old-space-size=4096 node a.js", None),
            ("RUBYOPT=-w ruby a.rb", None),
            ("JAVA_TOOL_OPTIONS=-Xmx1g java -jar a.jar", None),
            ("LD_PRELOAD= ls", None),
        ], self.bash)


class Abbreviations(GuardCase):
    def test_long_options_match_by_prefix(self):
        self.run_table([
            ("tar -xf a.tar --to-com='rm -rf ~'", "rm-outside"),
            ("tar -xf a.tar --use-compress='rm -rf ~'", "rm-outside"),
            ("tar -cf a.tar x --checkpoint-act=exec='rm -rf ~'", "rm-outside"),
            ("rsync -av --rsh='rm -rf ~' a h:b", "rm-outside"),
            ("zip -r --unzip-com 'rm -rf ~' a.zip x", "rm-outside"),
            ("tar -cf a.tar x --checkpoint=100", None),
            ("tar -xf a.tar --to-stdout", None),
        ], self.bash)

    def test_sed_with_an_unsplittable_script_and_an_e_is_refused(self):
        self.run_table([
            ("sed 's/a;b/rm -rf ~/e' f", "system"),
            ("sed 's/a;b/c/;e id' f", "system"),
            ("sed 's/a;b/c/' f", None),  # a ; inside an s command, no e anywhere
            ("sed 's/a;b/c/;p' f", None),
        ], self.bash)


class ScriptFiles(GuardCase):
    def test_a_script_file_a_shell_or_python_runs_is_read(self):
        d = os.path.join(os.path.dirname(self.home), "scripts")
        os.makedirs(d, exist_ok=True)
        for name, text in (("bad.sh", "echo hi\nrm -rf ~\n"), ("ok.sh", "echo hi\nls\n"),
                           ("bad.py", "import os\nos.system('rm -rf ~')\n"), ("ok.py", "print(1)\n")):
            with open(os.path.join(d, name), "w") as f:
                f.write(text)
        p = lambda n: os.path.join(d, n)  # noqa: E731
        self.run_table([
            (f"bash {p('bad.sh')}", "rm-outside"),
            (f"sh -e {p('bad.sh')} arg", "rm-outside"),
            (f"source {p('bad.sh')}", "rm-outside"),
            (f". {p('bad.sh')}", "rm-outside"),
            (f"python3 {p('bad.py')}", "rm-outside"),
            (f"BASH_ENV={p('bad.sh')} bash -c true", "rm-outside"),
            (f"bash {p('ok.sh')}", None),
            (f"source {p('ok.sh')}", None),
            (f"python3 {p('ok.py')}", None),
            (f"bash {p('missing.sh')}", None),
        ], self.bash)


ACTIVATE = '''# This file must be used with "source bin/activate" *from bash*
deactivate () {
    if [ -n "${_OLD_VIRTUAL_PATH:-}" ] ; then
        PATH="${_OLD_VIRTUAL_PATH:-}"
        export PATH
        unset _OLD_VIRTUAL_PATH
    fi
    hash -r 2> /dev/null
    if [ -n "${_OLD_VIRTUAL_PS1+_}" ] ; then
        PS1="${_OLD_VIRTUAL_PS1:-}"
        export PS1
        unset _OLD_VIRTUAL_PS1
    fi
    unset VIRTUAL_ENV
    if [ ! "${1:-}" = "nondestructive" ] ; then
        unset -f deactivate
    fi
}
deactivate nondestructive
VIRTUAL_ENV="/home/u/proj/.venv"
export VIRTUAL_ENV
_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH
if [ -z "${VIRTUAL_ENV_DISABLE_PROMPT:-}" ] ; then
    _OLD_VIRTUAL_PS1="${PS1:-}"
    PS1="(.venv) ${PS1:-}"
    export PS1
fi
hash -r 2> /dev/null
'''


class Review(GuardCase):
    """T-0275 adversarial review: bypasses and false positives."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.d = os.path.join(os.path.dirname(cls.home), "scripts2")
        os.makedirs(cls.d, exist_ok=True)
        files = {"bad.sh": "rm -rf ~\n", "ok.sh": "ls\n", "bad.py": "import os\nos.system('rm -rf ~')\n",
                 "big.sh": "# " + "x" * (1 << 19) + "\nls\n", "s.sed": "e rm -rf ~\n", "bad-x.sh": "#!/bin/bash\nrm -rf ~\n",
                 "ok-x.sh": "#!/bin/bash\nls\n", "bin.out": "\x7fELF" + "x" * (1 << 19),
                 "bad-core.sh": f"echo x > {cls.fhome}/state/projects/x/f\n",
                 # what a real deploy script does: nothing a literal `rm -rf ~` would be
                 "deploy.sh": 'set -e\nIFS=,\nsystemctl reboot\nclaude plugin marketplace add x\nrm -rf "$DIR/build"\n'
                              'cat .env\nfind . -name x | xargs rm\ncurl -sL https://x.example/i | sh\n\nls\n'}
        for name, text in files.items():
            with open(os.path.join(cls.d, name), "w") as f:
                f.write(text)
        for x in ("bad-x.sh", "ok-x.sh", "bin.out"):
            os.chmod(os.path.join(cls.d, x), 0o755)
        os.makedirs(os.path.join(cls.repo, ".venv", "bin"), exist_ok=True)
        with open(os.path.join(cls.repo, ".venv", "bin", "activate"), "w") as f:
            f.write(ACTIVATE)

    def p(self, n):
        return os.path.join(self.d, n)

    def blocked(self, cmds):
        for cmd in cmds:
            with self.subTest(cmd=cmd):
                r = self.bash(cmd)
                self.assertIsNotNone(r, f"allowed: {cmd}")

    def test_dash_n_only_counts_before_the_script(self):
        self.run_table([(f"bash {self.p('bad.sh')} -n", "rm-outside"), (f"sh {self.p('bad.sh')} -an", "rm-outside"),
                        (f"bash -n {self.p('bad.sh')}", None)], self.bash)

    def test_clustered_short_options_carry_values(self):
        self.run_table([
            ("rsync -avze 'rm -rf ~' a h:b", "rm-outside"), ("ssh -Co 'ProxyCommand=rm -rf ~' host", "rm-outside"),
            ("tar -cvI 'rm -rf ~' -f a.tar x", "rm-outside"),
            ("tar -cvf a.tar x", None), ("rsync -avz a h:b", None), ("ssh -Cv host", None),
        ], self.bash)

    def test_script_written_in_the_same_command_is_refused(self):
        self.run_table([
            ("printf 'rm -rf ~\\n' > /tmp/x.sh && bash /tmp/x.sh", "system"),
            ("echo 'rm -rf ~' > ok.sh; bash ok.sh", "system"),
            ("echo hi > /tmp/x.sh; source /tmp/x.sh", "system"),
            ("echo hi > /tmp/x.sh; chmod +x /tmp/x.sh; /tmp/x.sh", "system"),
            ("echo hi > /tmp/x.out; bash /tmp/y.sh", None),
            ("cat > /tmp/s.sh <<'EOF'\nrm -rf ~\nEOF\nbash /tmp/s.sh", "rm-outside"),  # the heredoc body is the script
            ("cat > /tmp/s.sh <<'EOF'\nls\nEOF\nbash /tmp/s.sh", None),
            ("sed -i 's/a/b/' /tmp/x.sh && bash /tmp/x.sh", None),  # edit then run: the everyday case
            ("gcc -o /tmp/x.out a.c && /tmp/x.out", None),
            ("sed -n '/x/{{p;e id}}' f", None),
            ("sed -i 's/{{a}}/b/; s/c/d/' f", None),
        ], self.bash)

    def test_a_script_over_the_size_limit_is_refused(self):
        r = self.bash(f"bash {self.p('big.sh')}")
        self.assertBlocked(r, "system")
        self.assertIn("KB", r.detail)
        self.assertIsNone(self.bash(f"{self.p('bin.out')}"))  # a big binary run by path isn't a script

    def test_sed_script_files_and_unparsed_addresses(self):
        for cmd in (f"sed -f {self.p('s.sed')} f", "sed --file=x.sed f", "sed -nf x.sed f", "sed '/x/{{e rm -rf ~}}' f",
                    "sed '1~2e rm -rf ~' f", "sed '1,+2e rm -rf ~' f", "sed '\\,x,e rm -rf ~' f",
                    "sed '/a;b/e rm -rf ~' f", "sed -ne 'p;e rm -rf ~' f"):
            with self.subTest(cmd=cmd):
                self.assertIsNotNone(self.bash(cmd))
        self.run_table([("sed -n '/x/{{p}}' f", None), ("sed '1~2d' f", None), ("sed -E 's/(a)/\\1/' f", None)], self.bash)

    def test_vim_options_that_run_code(self):
        self.blocked(["vim -S s.vim f", "vim -u /tmp/vimrc f", "vim -s keys f", "vim --cmd 'x' f", "nvim -l x.lua",
                      "vim '+r!rm -rf ~' f", "vim -c '%!rm -rf ~' f", "vim -c'!rm -rf ~' f",
                      "vim -c 'exe \"!rm -rf ~\"' f", "vim -c 'silent !rm -rf ~' f"])
        self.run_table([("vim -c 'set ft=python' f", None), ("vim -u NONE f", None), ("vim -c 'wq!' f", None),
                        ("vim -c 'silent! s/a/b/' f", None)], self.bash)

    def test_python_option_values_are_not_modes(self):
        self.run_table([(f"python3 -Wonce {self.p('bad.py')}", "rm-outside"),
                        (f"python3 -Xtracemalloc=5 {self.p('bad.py')}", "rm-outside"),
                        (f"python3 -W ignore {self.p('bad.py')}", "rm-outside"),
                        (f"python3 -uB {self.p('bad.py')}", "rm-outside")], self.bash)

    def test_more_vectors(self):
        self.run_table([
            ("scp -S 'rm -rf ~' a h:b", "rm-outside"), ("sftp -S 'rm -rf ~' h", "rm-outside"),
            ("ssh -o PKCS11Provider=/tmp/x.so host", "system"), ("ssh -o SecurityKeyProvider=/tmp/x.so host", "system"),
            ("ssh -I /tmp/x.so host", "system"),
            ("tar --rsh-command='rm -rf ~' -xf a", "rm-outside"), ("tar --rmt-command='rm -rf ~' -xf a", "rm-outside"),
            ("JAVA_TOOL_OPTIONS='-XX:OnOutOfMemoryError=rm -rf ~' java -jar a.jar", "system"),
            ("_JAVA_OPTIONS='-XX:OnError=rm -rf ~' java -jar a.jar", "system"),
            ("RSYNC_RSH='rm -rf ~' rsync a h:b", "rm-outside"),
            ("TAR_OPTIONS=\"-I 'rm -rf ~'\" tar -xf a", "rm-outside"),
            ("PS4='$(rm -rf ~)' bash -x f", "system"), ("SHELLOPTS=xtrace PS4='`id`' bash f", "system"),
            ("PS4='+ ' bash -x f", None), ("RSYNC_RSH=ssh rsync a h:b", None), ("TAR_OPTIONS=-v tar -xf a", None),
            ("ssh -o PKCS11Provider=none host", None),
        ], self.bash)

    def test_real_script_shapes_pass(self):
        self.run_table([
            ("source .venv/bin/activate && pytest", None), ("ENV=production make", None),
            ("ENV=production npm run build", None), (f"ENV={self.p('ok.sh')} sh -c true", None),
            (f"ENV={self.p('bad.sh')} sh -c true", "rm-outside"), (f"ENV={self.p('bad.sh')} make", None),
            (f"bash {self.p('deploy.sh')}", None), (f"bash {self.p('bad-core.sh')}", "state-direct"),
        ], self.bash)

    def test_executable_with_a_shebang_is_read(self):
        self.run_table([(self.p("bad-x.sh"), "rm-outside"), (self.p("ok-x.sh"), None),
                        (f"{self.p('ok-x.sh')} --flag", None)], self.bash)


class ScriptCache(GuardCase):
    """T-0275: the hook runs before every Bash call, so a script's verdict is cached by (path, size, mtime) and one
    read has a time budget."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.d = os.path.join(os.path.dirname(cls.home), "scripts3")
        os.makedirs(cls.d, exist_ok=True)

    def script(self, name, text):
        p = os.path.join(self.d, name)
        with open(p, "w") as f:
            f.write(text)
        return p

    def test_a_cached_second_run_does_not_read_the_file(self):
        p = self.script("c1.sh", "echo hi\nrm -rf ~\n")
        with mock.patch.object(g, "_script_text", wraps=g._script_text) as reads:
            first = self.bash(f"bash {p}")
            second = self.bash(f"bash {p}")
            self.assertEqual(reads.call_count, 1)
        self.assertBlocked(first, "rm-outside")
        self.assertBlocked(second, "rm-outside")
        self.script("c1.sh", "echo hi\nls\n\n")  # a changed file is read again
        with mock.patch.object(g, "_script_text", wraps=g._script_text) as reads:
            self.assertIsNone(self.bash(f"bash {p}"))
            self.assertEqual(reads.call_count, 1)

    def test_the_cache_keeps_200_entries_and_drops_gone_files(self):
        gone = self.script("gone.sh", "ls\n")
        self.bash(f"bash {gone}")
        os.remove(gone)
        for i in range(205):
            self.bash(f"bash {self.script(f'n{i}.sh', f'echo {i}')}")
        with open(g._script_cache_path(self.ctx())) as f:
            entries = json.load(f)
        self.assertLessEqual(len(entries), 200)
        self.assertFalse(any(e["p"] == gone for e in entries.values()))

    def test_past_the_budget_the_script_is_allowed_unread_and_noted(self):
        p = self.script("slow.sh", "echo hi\n" * 4000)
        with mock.patch.dict(os.environ, {"FM_GUARD_SCRIPT_BUDGET": "0.000001"}):
            g.take_unread()
            self.assertIsNone(self.bash(f"bash {p}"))
            unread = g.take_unread()
        self.assertEqual([u[0] for u in unread], [p])
        self.assertIn("budget", unread[0][1])
        with mock.patch.dict(os.environ, {"FM_GUARD_SCRIPT_BUDGET": "5"}):  # the unread verdict is cached with its note
            self.assertIsNone(self.bash(f"bash {p}"))
            self.assertEqual([u[0] for u in g.take_unread()], [p])


class ScriptHook(HookCase):
    def test_the_hook_notes_and_logs_an_unread_script(self):
        self.task()
        p = os.path.join(self.tmp, "slow.sh")
        with open(p, "w") as f:
            f.write("echo hi\n" * 4000)
        r = self.hook("PreToolUse", {"tool_name": "Bash", "tool_input": {"command": f"bash {p}"}},
                      env={"FM_GUARD_SCRIPT_BUDGET": "0.000001"})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("too long", self.ctx_of(r))
        with open(os.path.join(self.project().dir, "ledger.jsonl")) as f:
            evs = [json.loads(x) for x in f]
        hit = [e for e in evs if e["event"] == "guard_unread"]
        self.assertEqual(hit[0]["data"]["path"], p)
