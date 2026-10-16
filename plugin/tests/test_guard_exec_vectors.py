"""T-0275: commands that run a hidden command (exec options, code-loading variables, script files) are read like
bash -c; a payload the guard can't read is refused, a harmless look-alike passes."""
import os
from test_guard import GuardCase


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
