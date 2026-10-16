"""fm code (T-1212): Foreman's loop run by the harness, with a model filling small slots (Foreman Code, T-1207).

    fm code "<request>" [--model NAME] [--escalate NAME] [--max-steps 40] [--dry-plan] [--no-commit] [--json]
    fm code --resume [ID]          continue a run that crashed or was killed, from its journal
    fm code models                 the model profiles (fmmodels) and where each comes from

The model never drives. It fills a PLAN slot ({type, tier S|M, title, criteria: [{text, verify}], steps}), checked
and repaired at most twice with the error quoted back; then, for each step, it picks one action at a time, as a native
tool call when its profile has tools, else a JSON object in its text ({"action": NAME, ...}):
  read {path, start?, lines?}   a file's numbered lines (or a folder's entries), inside the project
  search {pattern, glob?}       git grep -E, bounded
  edit {file, old, new}         the guard (PreToolUse Edit), then fm edit (all or nothing)
  write {file, content}         the guard (PreToolUse Write), then the file
  run {cmd}                     the guard (PreToolUse Bash), then bash at the root; output cut to head and tail
  done {summary}                the step is finished
The guard is reached exactly as other harnesses do: plugin/hooks/hook PreToolUse with a Claude-Code-shaped payload;
exit 2, a deny or an ask (nobody here to answer it) is a refusal, sent back as the action's result and never run.
The harness makes the task (fm task new --focus), runs each criterion's verify as evidence (fm task evidence --ac N
--run) before the first step and after the last, gives a failure back to the model (3 rounds, then 3 more on
--escalate's model), blocks the task when it still fails, and closes it with fm task finish (an M task's audit lenses,
docs and lesson come from one more slot). Every message and action goes in the project's code/<task>.jsonl journal.
"""
import json
import os
import signal
import subprocess
import sys
import threading
import time

import fmcore
import fmmodels as m

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FM = os.path.join(PLUGIN, "bin", "fm")
HOOK = os.path.join(PLUGIN, "hooks", "hook")
TYPES = ("FIX", "FEATURE", "CLEAN", "PERFORMANCE", "SECURITY", "RESEARCH")
REPAIRS, ROUNDS = 2, 3
CAP = 3000            # characters of a run's head, and of its tail, the model sees
READ_LINES, READ_MAX, LINE_MAX, READ_BYTES = 200, 400, 500, 16 << 20
RUN_TIMEOUT, VERIFY_TIMEOUT, FM_TIMEOUT = 120, 600, 900
MAX_TOKENS, KEEP_RESULTS, SMALL_CONTEXT = 8192, 6, 32768

TOOLS = [
    {"name": "read", "description": "Read a file's numbered lines, or list a folder, inside the project.",
     "parameters": {"type": "object", "required": ["path"], "properties": {
         "path": {"type": "string"}, "start": {"type": "integer", "description": "first line, 1-based"},
         "lines": {"type": "integer", "description": f"how many lines (at most {READ_MAX})"}}}},
    {"name": "search", "description": "Search the project's files for an extended regular expression (git grep -E).",
     "parameters": {"type": "object", "required": ["pattern"], "properties": {
         "pattern": {"type": "string"}, "glob": {"type": "string", "description": "only files matching, e.g. *.py"}}}},
    {"name": "edit", "description": "Replace the exact text old, which must occur once in file, with new.",
     "parameters": {"type": "object", "required": ["file", "old", "new"], "properties": {
         "file": {"type": "string"}, "old": {"type": "string"}, "new": {"type": "string"}}}},
    {"name": "write", "description": "Create a file, or replace all of it, with content.",
     "parameters": {"type": "object", "required": ["file", "content"], "properties": {
         "file": {"type": "string"}, "content": {"type": "string"}}}},
    {"name": "run", "description": f"Run a shell command at the project root ({RUN_TIMEOUT} s limit).",
     "parameters": {"type": "object", "required": ["cmd"], "properties": {"cmd": {"type": "string"}}}},
    {"name": "done", "description": "This step is finished.",
     "parameters": {"type": "object", "required": ["summary"], "properties": {"summary": {"type": "string"}}}},
]

PLAN_PROMPT = """You plan one coding task for Foreman's harness. Reply with only one JSON object:
{"type": "FIX|FEATURE|CLEAN|PERFORMANCE|SECURITY|RESEARCH", "tier": "S|M", "title": "...",
 "criteria": [{"text": "what is true when it is done", "verify": "a shell command that exits 0 only then"}],
 "steps": ["...", "..."]}
Tier S is a small change in one or two files; M is several files or a design choice. Each verify runs at the project
root and must fail before the work and pass after it. Steps are short and in order; the first is usually a failing
test. The project's files:
"""

ACT_PROMPT = """You do one step of a task for Foreman's harness, one action at a time. The actions:
  read {"path", "start"?, "lines"?}  search {"pattern", "glob"?}  edit {"file", "old", "new"}  write {"file", "content"}
  run {"cmd"}  done {"summary"}
Paths are relative to the project root. edit replaces exact text that occurs once; read the file first. Foreman's guard
may refuse an edit, write or run: do it another way. Call done when this step is finished (not the whole task)."""

TEXT_ACTIONS = """
Reply with exactly one action as a JSON object, such as {"action": "read", "path": "app.py"} or
{"action": "done", "summary": "what changed"}."""

CLOSE_PROMPT = """The task is verified. Before Foreman closes it, reply with only one JSON object of short notes:
{"intent": "how the change meets the request", "adversary": "what input or case could still break it, and why it
doesn't", "docs": "the docs updated, or none: why", "lesson": "what the next similar task should know, or none: why",
"why_not_caught": "the test, gate or guard that would have caught it earlier, or none: why"}"""
CLOSE_KEYS = ("intent", "adversary", "docs", "lesson", "why_not_caught")


class CodeError(Exception):
    """fm code stops: the message is the whole story (exit 1)."""


# ---------------------------------------------------------------- slots

def check_plan(v):
    """None when v is a usable plan, else what's wrong with it (quoted back to the model)."""
    if not isinstance(v, dict):
        return "the reply holds no JSON object"
    if v.get("type") not in TYPES:
        return f"type must be one of {', '.join(TYPES)}, not {v.get('type')!r}"
    if v.get("tier") not in ("S", "M"):
        return f"tier must be S or M, not {v.get('tier')!r}"
    title = v.get("title")
    if not isinstance(title, str) or not title.strip() or len(title) > 120 or "\n" in title:
        return "title must be one line of text, at most 120 characters"
    crit = v.get("criteria")
    if not isinstance(crit, list) or not 1 <= len(crit) <= 8:
        return "criteria must be a list of 1 to 8 objects"
    for i, cr in enumerate(crit, 1):
        if not isinstance(cr, dict) or not all(isinstance(cr.get(k), str) and cr[k].strip() for k in ("text", "verify")):
            return f"criterion {i} needs both text and verify, as text"
        if "::" in cr["text"] or "\n" in cr["text"] + cr["verify"]:
            return f"criterion {i}: text and verify are one line each, and text has no '::'"
    steps = v.get("steps")
    if not isinstance(steps, list) or not 1 <= len(steps) <= 12 or \
            not all(isinstance(s, str) and s.strip() and "\n" not in s for s in steps):
        return "steps must be a list of 1 to 12 one-line texts"
    if title.lstrip().startswith("-"):
        return "title must not start with '-'"
    return None


def check_close(v):
    if not isinstance(v, dict):
        return "the reply holds no JSON object"
    bad = [k for k in CLOSE_KEYS if not (isinstance(v.get(k), str) and v[k].strip())]
    return f"give {', '.join(bad)} as text" if bad else None


def slot(run, profile, messages, check, what):
    """Ask for one JSON slot; on a bad answer quote the error back, at most REPAIRS times."""
    err = None
    for _ in range(REPAIRS + 1):
        r = m.complete(profile, messages, max_tokens=MAX_TOKENS)
        run.usage(r)
        v = m.extract_json(r["text"])
        if v is None and r["tool_calls"]:
            v = r["tool_calls"][0]["args"]
        messages.append({"role": "assistant", "content": r["text"]})
        err = check(v)
        if not err:
            return v
        messages.append({"role": "user", "content": f"That is not a valid {what}: {err}. Reply with only the "
                                                    "corrected JSON object."})
    raise CodeError(f"the model gave no valid {what} after {REPAIRS} repairs: {err}")


# ---------------------------------------------------------------- the run

class Run:
    def __init__(self, args, root, jdir):
        self.args, self.root, self.jdir = args, root, jdir
        self.json = getattr(args, "json", False)
        self.tid = self.plan = self.request = self.journal = None
        self.done, self.msgs, self.turns, self.tokens = set(), {}, 0, [0, 0]
        self.baseline = self.model_name = self.close_notes = self.plan_msgs = None
        self.sensitive, self.escalate, self.cap = False, getattr(args, "escalate", None), CAP
        self.no_commit, self.max_steps = bool(getattr(args, "no_commit", False)), getattr(args, "max_steps", None)
        self.secret_envs = {cloud[4] for cloud in m.CLOUD}  # and each profile's own key_env, added as it's resolved

    # -- output and journal
    def emit(self, event, text, **data):
        if self.json:
            print(json.dumps(dict(data, event=event, text=text)), flush=True)
        else:
            print(text, flush=True)

    def log(self, **rec):
        if self.journal:
            with open(self.journal, "a", encoding="utf-8") as f:
                f.write(json.dumps(fmcore.redact_obj(dict(rec, ts=time.time()))) + "\n")

    def redact(self, text):
        """text without the values of the model key variables, then fmcore.redact's patterns."""
        for k in self.secret_envs:
            v = (os.environ.get(k) or "").strip()
            if len(v) >= 6:
                text = text.replace(v, "[REDACTED]")
        return fmcore.redact(text)

    def env(self):
        """The environment for everything fm code starts: without the model API keys, so a command the model chose
        can't print one into its own transcript or the journal."""
        return {k: v for k, v in os.environ.items() if k not in self.secret_envs}

    def offsite_ok(self, p, profile):
        """A sensitive repo's content never goes to a model off this machine (fm sensitive on, T-0784)."""
        import urllib.parse
        self.sensitive = self.sensitive if p is None else bool(fmcore.read_meta(p).get("sensitive"))
        try:
            host = urllib.parse.urlsplit(profile.get("base_url") or "").hostname or ""
        except ValueError:
            host = ""
        if profile.get("key_env"):
            self.secret_envs.add(profile["key_env"])
        if self.sensitive and not m.is_loopback(host):
            raise CodeError(f"this repo is marked sensitive (fm sensitive on), so its code can't go to {profile['name']} "
                            "off this machine: use a local model (fm code models), or fm sensitive off")

    def usage(self, r):
        self.tokens[0] += r["usage"].get("in") or 0
        self.tokens[1] += r["usage"].get("out") or 0

    # -- fm and the hook
    def fm(self, *a, stdin=None, timeout=FM_TIMEOUT):
        try:
            p = subprocess.run([sys.executable, FM, *a], cwd=self.root, input=stdin, capture_output=True, text=True,
                               timeout=timeout, env=self.env())
        except subprocess.TimeoutExpired:
            return 124, f"fm {a[0]} {a[1] if len(a) > 1 else ''} took over {timeout} s"
        return p.returncode, (p.stdout + p.stderr).strip()

    def hook(self, event, tool, tool_input, response=None):
        pl = {"session_id": f"fm-code-{self.tid or 'plan'}", "cwd": self.root, "hook_event_name": event, "tool_name": tool,
              "tool_input": tool_input}
        if response is not None:
            pl["tool_response"] = response
        return subprocess.run([sys.executable, HOOK, event], input=json.dumps(pl), capture_output=True, text=True,
                              timeout=120, cwd=self.root, env=self.env())

    def guard(self, tool, tool_input):
        """None when Foreman's guard lets this tool call run, else why not. Fails closed."""
        try:
            r = self.hook("PreToolUse", tool, tool_input)
        except (OSError, subprocess.TimeoutExpired) as e:
            return f"Foreman's guard didn't answer ({type(e).__name__}), so it's refused"
        hs = (m.extract_json(r.stdout) or {}).get("hookSpecificOutput")
        hs = hs if isinstance(hs, dict) else {}
        decision = hs.get("permissionDecision")
        if r.returncode == 0 and decision in (None, "allow"):
            return None
        why = str(hs.get("permissionDecisionReason") or r.stderr.strip() or f"the guard exited {r.returncode}")
        return ("it needs the user's yes, which fm code can't ask for: " + why) if decision == "ask" else why

    def after(self, tool, tool_input, response):
        try:  # what Claude Code's PostToolUse records (touched files, runs); never stops the run
            self.hook("PostToolUse", tool, tool_input, response)
        except (OSError, subprocess.TimeoutExpired):
            pass

    # -- actions
    def path(self, rel):
        full = os.path.realpath(os.path.join(self.root, rel))
        if full != self.root and not full.startswith(self.root + os.sep):
            raise ValueError(f"{rel} is outside the project")
        return full

    def hidden(self, full):
        """Why the model may not see this file (a credential, Git's own files), or None."""
        import fmguard
        if os.path.relpath(full, self.root).split(os.sep)[0] == ".git":
            return "Git's own files are not read"
        ctx = fmguard.Ctx(cwd=self.root, project_root=self.root, home=os.path.expanduser("~"),
                          foreman_home=fmcore.foreman_home())
        return "it looks like a credential, which never goes to the model" if fmguard._is_credential(full, ctx) else None

    def act(self, name, a):
        """(result text, step finished)."""
        if not isinstance(a, dict) or "_raw" in a:
            return "error: the action's arguments weren't a JSON object", False

        def arg(k, typ=str, default=None):
            v = default if a.get(k) is None else a[k]
            if not isinstance(v, typ) or isinstance(v, bool):
                raise ValueError(f"{name} needs {k} as {typ.__name__}")
            return v
        try:
            if name == "done":
                return "step finished", True
            if name == "read":
                return self.read(arg("path"), arg("start", int, 1), arg("lines", int, READ_LINES)), False
            if name == "search":
                return self.search(arg("pattern"), a.get("glob") if isinstance(a.get("glob"), str) else None), False
            if name == "edit":
                return self.edit(arg("file"), arg("old"), arg("new")), False
            if name == "write":
                return self.write(arg("file"), arg("content")), False
            if name == "run":
                return self.run_cmd(arg("cmd")), False
        except (ValueError, OSError) as e:
            return f"error: {e}", False
        return f"error: no action {name!r}; the actions are read, search, edit, write, run and done", False

    def read(self, rel, start, lines):
        full = self.path(rel)
        why = self.hidden(full)
        if why:
            return f"refused: {rel}: {why}"
        if os.path.isdir(full):
            names = sorted(n + "/" * os.path.isdir(os.path.join(full, n)) for n in os.listdir(full) if n != ".git")
            return "\n".join(names[:300]) + (f"\n… {len(names) - 300} more" if len(names) > 300 else "")
        if not os.path.isfile(full):
            return f"refused: {rel} is not a regular file (a pipe or a device would never end)"
        if os.path.getsize(full) > READ_BYTES:
            raise ValueError(f"{rel} is over {READ_BYTES >> 20} MB: search it instead")
        start, lines = max(start, 1), min(max(lines, 1), READ_MAX)
        out = []
        with open(full, encoding="utf-8", errors="replace") as f:
            for n, line in enumerate(f, 1):
                if n >= start + lines:
                    out.append(f"… (more after line {n - 1}; read on with start={n})")
                    break
                if n >= start:
                    out.append(f"{n:>5}  {line.rstrip()[:LINE_MAX]}")
        return "\n".join(out) or "(empty, or no lines there)"

    def search(self, pattern, glob):
        try:  # untracked pipes and devices are left out: git grep would wait on them forever
            files = subprocess.run(["git", "ls-files", "-z", "--others", "--exclude-standard"], cwd=self.root,
                                   capture_output=True, text=True, timeout=30, errors="replace").stdout.split("\0")
            odd = [f":(exclude,literal){f}" for f in files if f and not os.path.isfile(os.path.join(self.root, f))]
            p = subprocess.run(["git", "grep", "-n", "-z", "-I", "--untracked", "-E", "-e", pattern, "--",
                                glob or "."] + odd[:500], cwd=self.root, capture_output=True, text=True, timeout=30,
                               errors="replace")
        except subprocess.TimeoutExpired:
            return "error: the search took over 30 s; narrow it"
        if p.returncode == 1:
            return "no match"
        if p.returncode:
            return f"error: {p.stderr.strip()[:300]}"
        hits, seen = [], {}
        for h in p.stdout.splitlines():
            path, _, rest = h.partition("\0")
            if path not in seen:
                seen[path] = self.hidden(os.path.realpath(os.path.join(self.root, path)))
            if not seen[path]:
                hits.append(f"{path}:{rest.replace(chr(0), ':', 1)}"[:LINE_MAX])
        if not hits:
            return "no match" + (" (matches in credential files are never shown)" if seen else "")
        return "\n".join(hits[:80]) + (f"\n… {len(hits) - 80} more matches" if len(hits) > 80 else "")

    def edit(self, rel, old, new):
        full = self.path(rel)
        ti = {"file_path": full, "old_string": old, "new_string": new}
        why = self.guard("Edit", ti)
        if why:
            return f"refused by Foreman's guard: {why}"
        code, out = self.fm("edit", stdin=json.dumps([{"file": full, "old": old, "new": new}]))
        if code:
            return f"error: {out}"
        self.after("Edit", ti, {"filePath": full})
        return out or "edited"

    def write(self, rel, content):
        full = self.path(rel)
        ti = {"file_path": full, "content": content}
        why = self.guard("Write", ti)
        if why:
            return f"refused by Foreman's guard: {why}"
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        self.after("Write", ti, {"filePath": full})
        return f"wrote {rel} ({len(content)} characters)"

    def run_cmd(self, cmd):
        why = self.guard("Bash", {"command": cmd})
        if why:
            return f"refused by Foreman's guard: {why}"
        code, out = run_bounded(cmd, self.root, RUN_TIMEOUT, self.env(), self.cap)
        self.after("Bash", {"command": cmd}, {"stdout": out, "stderr": "", "interrupted": code is None})
        return (f"timed out after {RUN_TIMEOUT} s" if code is None else f"exit {code}") + (f"\n{out}" if out else "")

    # -- the stations
    def phase(self, name, profile, prompt):
        """One step's conversation: actions until done. A journaled one carries on where it stopped."""
        if name in self.done:
            return
        if name not in self.msgs:
            self.add(name, {"role": "system", "content": ACT_PROMPT + ("" if profile.get("tools") else TEXT_ACTIONS)})
            self.add(name, {"role": "user", "content": prompt})
        msgs = self.msgs[name]
        lost = ("not run (interrupted): the harness stopped before this action's result was recorded; it may have "
                "partly happened, so check before doing it again")
        answered = {x.get("tool_call_id") for x in msgs if x.get("role") == "tool"}
        for tc in [tc for x in msgs if x.get("role") == "assistant" for tc in x.get("tool_calls") or []]:
            if tc.get("id") not in answered:  # killed between the model's answer and its results
                self.add(name, {"role": "tool", "tool_call_id": tc.get("id"), "content": lost})
        if msgs[-1].get("role") == "assistant":
            self.add(name, {"role": "user", "content": lost})
        tools = TOOLS if profile.get("tools") else None
        while True:
            if self.turns >= self.max_steps:
                raise CodeError(f"stopped: the model used all {self.max_steps} turns (--max-steps) before {name} was "
                                f"done; fm code --resume {self.tid} --max-steps N carries on")
            self.turns += 1
            r = m.complete(profile, trim(msgs), tools=tools, max_tokens=MAX_TOKENS)
            self.usage(r)
            calls = r["tool_calls"]
            if r["stop"] == "length":  # a cut-off call may be missing its end: nothing in it runs
                self.add(name, {"role": "assistant", "content": r["text"]})
                self.add(name, {"role": "user", "content": "Your reply was cut off at the output limit, so nothing in "
                                                           "it was run. Use edit for a change, or a smaller action."})
                continue
            if calls:
                self.add(name, {"role": "assistant", "content": r["text"], "tool_calls": calls})
                finished = False
                for tc in calls:
                    result, fin = self.do(tc["name"], tc["args"])
                    self.add(name, {"role": "tool", "tool_call_id": tc["id"], "content": result})
                    finished = finished or fin
            else:
                self.add(name, {"role": "assistant", "content": r["text"]})
                v = m.extract_json(r["text"])
                if not isinstance(v, dict) or not isinstance(v.get("action"), str):
                    self.add(name, {"role": "user", "content": "No action found." + TEXT_ACTIONS})
                    continue
                act = v.pop("action")
                result, finished = self.do(act, v)
                self.add(name, {"role": "user", "content": f"Result of {act}:\n{result}"})
            if finished:
                break
        self.done.add(name)
        self.log(kind="phase_done", phase=name)

    def add(self, phase, msg):
        self.msgs.setdefault(phase, []).append(msg)
        self.log(kind="msg", phase=phase, msg=msg)

    def do(self, name, a):
        result, fin = self.act(name, a)
        result = self.redact(result)
        target = next((str(a.get(k)) for k in ("file", "path", "cmd", "pattern", "summary") if isinstance(a, dict)
                       and a.get(k) is not None), "")
        state = "refused" if result.startswith("refused") else "error" if result.startswith("error") else "ok"
        self.emit("action", f"  {name} {_one_line(target, 70)}: {state}" + (
            f" ({_one_line(result, 100)})" if state != "ok" else ""), action=name, target=target[:200], result=state)
        self.log(kind="action", action=name, result=state)
        return result, fin

    def verify(self, label):
        """[(n, cmd, output)] of the criteria whose verify failed; each run is recorded as its evidence."""
        failed = []
        for n, cr in enumerate(self.plan["criteria"], 1):
            why = self.guard("Bash", {"command": cr["verify"]})
            if why:
                raise Blocked(f"fm code: Foreman's guard refused criterion {n}'s verify command: {_one_line(why, 200)}")
            code, out = self.fm("task", "evidence", self.tid, "--ac", str(n), f"--run={cr['verify']}",
                                timeout=VERIFY_TIMEOUT + 60)
            self.emit("verify", f"{label} {n}: {cr['verify']} → {'pass' if code == 0 else f'exit {code}'}",
                      criterion=n, exit=code)
            if code:
                failed.append((n, cr["verify"], _cut(self.redact(out), self.cap)))
        self.log(kind="verify", label=label, failed=[n for n, *_ in failed])
        return failed


class Blocked(Exception):
    """The task can't go on: fm task block with this reason."""


def _one_line(s, n):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n - 1] + "…"


def _cut(s, cap=CAP):
    return s if len(s) <= 2 * cap else f"{s[:cap]}\n… ({len(s) - 2 * cap} characters cut) …\n{s[-cap:]}"


def _is_result(msg):
    return msg.get("role") == "tool" or msg.get("role") == "user" and str(msg.get("content")).startswith("Result of ")


def trim(msgs, keep=KEEP_RESULTS):
    """What the model is sent: the conversation with every tool result but the last `keep` cut to a one-line stub.
    The stored conversation (and the journal) keep them whole."""
    old = [i for i, x in enumerate(msgs) if _is_result(x)][:-keep]
    out = list(msgs)
    for i in old:
        first = str(msgs[i].get("content") or "").split("\n", 1)[0]
        out[i] = dict(msgs[i], content=f"(older result cut: {_one_line(first, 80)})")
    return out


def run_bounded(cmd, cwd, timeout, env=None, cap=CAP):
    """(exit code or None on timeout, output cut to head and tail). Memory stays bounded whatever the command prints;
    its whole process group is killed at the end, so nothing it started in the background outlives it."""
    p = subprocess.Popen(["bash", "-c", cmd], cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, start_new_session=True, env=env)
    head, tail, total = bytearray(), bytearray(), [0]

    def pump():
        for chunk in iter(lambda: p.stdout.read1(65536), b""):
            total[0] += len(chunk)
            take = chunk[:max(cap - len(head), 0)]
            head.extend(take)
            tail.extend(chunk[len(take):])
            del tail[:-cap]
    t = threading.Thread(target=pump, daemon=True)
    t.start()
    try:
        code = p.wait(timeout)
    except subprocess.TimeoutExpired:
        code = None
    finally:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        p.wait()
    t.join(5)
    gap = total[0] - len(head) - len(tail)
    out = head.decode("utf-8", "replace") + (f"\n… ({gap} bytes cut) …\n" if gap > 0 else "") + \
        tail.decode("utf-8", "replace")
    return code, out.strip()


def _files(root):
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.TimeoutExpired):
        return "(unknown)"
    names = out.splitlines()
    return "\n".join(names[:200]) + (f"\n… {len(names) - 200} more" if len(names) > 200 else "")


def _task_text(run):
    crit = "\n".join(f"- {cr['text']} (verify: `{cr['verify']}`)" for cr in run.plan["criteria"])
    steps = "\n".join(f"{i}. {s}" for i, s in enumerate(run.plan["steps"], 1))
    return f"Task {run.tid}: {run.plan['title']}\nRequest: {run.request}\nDone when:\n{crit}\nSteps:\n{steps}"


def _failures(failed):
    return "\n\n".join(f"criterion {n}: `{cmd}` failed:\n{out}" for n, cmd, out in failed)


# ---------------------------------------------------------------- the verb

def cmd_code(args):
    import fmcli
    words = list(args.request or [])
    if words == ["models"]:
        return _models(args, fmcli)
    p = fmcli.resolve(args)
    root = os.path.realpath(p.root)
    run = Run(args, root, os.path.join(p.dir, "code"))
    try:
        if args.resume is not None:
            _load(run, args.resume)
        elif not words:
            raise fmcli.UsageError('fm code needs a request: fm code "<what to do>" (or fm code models, '
                                   'fm code --resume)')
        else:
            run.request = " ".join(words)
        profile = m.resolve(args.model or run.model_name)
        run.model_name = profile["name"]
        run.offsite_ok(p, profile)
        run.cap = CAP if profile.get("context", 0) >= SMALL_CONTEXT else CAP // 2
        run.max_steps = run.max_steps or 40
        run.escalate = m.resolve(run.escalate) if run.escalate else None  # a bad name fails now, not 3 rounds in
        if run.escalate:
            run.offsite_ok(None, run.escalate)
        if args.resume is None:
            _plan(run, profile, args.dry_plan)
            if args.dry_plan:
                return run.emit("plan", json.dumps(run.plan, indent=2), plan=run.plan)
            _make_task(run, profile)
        else:
            code, out = run.fm("focus", run.tid)
            if code:
                raise CodeError(f"can't resume {run.tid}: {out}")
            run.emit("resume", f"resuming {run.tid} from {run.journal}", task=run.tid)
        _drive(run, profile)
    except m.ModelError as e:
        print(f"fm code: model: {e}" + (f" (fm code --resume {run.tid} carries on)" if run.tid else ""),
              file=sys.stderr)
        raise SystemExit(1)
    except CodeError as e:
        print(f"fm code: {e}", file=sys.stderr)
        raise SystemExit(1)
    except Blocked as e:
        run.fm("task", "block", run.tid, str(e)[:500])
        run.log(kind="end", status="blocked", reason=str(e))
        run.emit("blocked", f"{run.tid} blocked: {e}", task=run.tid, reason=str(e))
        raise SystemExit(1)


def _plan(run, profile, dry=False):
    msgs = [{"role": "system", "content": PLAN_PROMPT + _files(run.root)}, {"role": "user", "content": run.request}]
    run.plan = slot(run, profile, msgs, check_plan, "plan")
    why = None if dry else _plan_problem(run)  # --dry-plan runs nothing
    if why:  # one re-plan
        msgs.append({"role": "user", "content": f"{why} Reply with only the corrected plan as a JSON object."})
        run.plan = slot(run, profile, msgs, check_plan, "plan")
        why = _plan_problem(run)
        if why and why.startswith("refused"):
            raise CodeError(why)
    run.plan_msgs = msgs
    pl = run.plan
    run.emit("plan", f"plan: {pl['type']} {pl['tier']} {pl['title']} (criteria: {len(pl['criteria'])}, "
                     f"steps: {len(pl['steps'])})", plan=pl)


def _plan_problem(run):
    """Why the plan's verify commands can't stand, or None: one the guard refuses; for FIX and FEATURE, one that
    passes before any work (it proves nothing)."""
    for n, cr in enumerate(run.plan["criteria"], 1):
        why = run.guard("Bash", {"command": cr["verify"]})
        if why:
            return f"refused by Foreman's guard: criterion {n}'s verify `{cr['verify']}`: {_one_line(why, 300)}"
    if run.plan["type"] not in ("FIX", "FEATURE"):
        return None
    for n, cr in enumerate(run.plan["criteria"], 1):
        code, _ = run_bounded(cr["verify"], run.root, VERIFY_TIMEOUT, run.env(), 200)
        if code == 0:
            return (f"Criterion {n}'s verify `{cr['verify']}` already passes before any work, so it proves nothing: "
                    "give a verify that fails now and passes once the work is done.")
    return None


def _make_task(run, profile):
    pl = run.plan
    a = ["task", "new", pl["title"], "--type", pl["type"], "--tier", pl["tier"], f"--raw={run.request}",
         f"--interpretation={run.request}",
         f"--approach=fm code ({profile['name']}): the harness runs the stations; the model filled the plan and picks "
         "one action at a time", "--focus", "--json"]
    a += [f"--ac={cr['text'].strip()} :: {cr['verify'].strip()}" for cr in pl["criteria"]]
    a += [f"--step={s.strip()}" for s in pl["steps"]]
    code, out = run.fm(*a)
    made = m.extract_json(out) or {}
    if code or not made.get("id"):
        raise CodeError(f"fm task new refused the plan: {out[:500]}")
    run.tid = made["id"]
    os.makedirs(run.jdir, exist_ok=True)
    run.journal = os.path.join(run.jdir, f"{run.tid}.jsonl")
    run.log(kind="start", task=run.tid, request=run.request, plan=pl, model=profile["name"], messages=run.plan_msgs,
            options={"no_commit": run.no_commit, "escalate": run.escalate and run.escalate["name"],
                     "max_steps": run.max_steps})
    run.emit("task", f"task {run.tid} created and focused", task=run.tid)


def _drive(run, profile):
    pl = run.plan
    if run.baseline is None:
        failed = run.verify("before")
        run.baseline = _failures(failed) or "every verify passes already"
        run.log(kind="baseline", text=run.baseline)
    for n, step in enumerate(pl["steps"], 1):
        if f"step:{n}" not in run.done:
            run.emit("step", f"step {n}/{len(pl['steps'])}: {step}", step=n)
        prompt = f"{_task_text(run)}\n\nVerify results before any change:\n{run.baseline}\n\nNow do step {n}: {step}"
        run.phase(f"step:{n}", profile, prompt)
    rounds = 0
    while True:
        failed = run.verify("verify")
        if not failed:
            break
        rounds += 1
        model = profile
        if rounds > ROUNDS:
            if not run.escalate or rounds > 2 * ROUNDS:
                raise Blocked(f"fm code: the verify still fails after {rounds - 1} fix rounds: "
                              f"{_one_line(_failures(failed), 300)}")
            model = run.escalate
        if f"fix:{rounds}" not in run.done:
            run.emit("fix", f"fix round {rounds} ({model['name']}): {len(failed)} criteria fail", round=rounds)
        run.phase(f"fix:{rounds}", model, f"{_task_text(run)}\n\nEvery step is done, but these verify commands fail "
                                          f"(fix round {rounds}):\n\n{_failures(failed)}\n\nFix the work (not the "
                                          "verify commands), then call done.")
    _finish(run, profile)


def _finish(run, profile):
    pl = run.plan
    a = ["task", "finish", run.tid, f"--audit=fm code ({profile['name']}): harness-run verify",
         "--run=" + " && ".join(cr["verify"] for cr in pl["criteria"])]
    if pl["tier"] == "M":
        notes = run.close_notes
        if notes is None:
            notes = slot(run, profile, [{"role": "system", "content": CLOSE_PROMPT},
                                        {"role": "user", "content": _task_text(run)}], check_close, "set of close notes")
            run.log(kind="close_notes", notes=notes)
        a += [f"--lens=intent: {notes['intent']}", f"--lens=adversary: {notes['adversary']}",
              f"--docs={notes['docs']}", f"--lesson={notes['lesson']}"]
        if pl["type"] == "FIX":
            a += [f"--why-not-caught={notes['why_not_caught']}"]
    if not run.no_commit:
        a += ["--commit", f"{pl['title']} ({run.tid})"]
    code, out = run.fm(*a)
    if code:
        raise Blocked(f"fm code: fm task finish refused: {_one_line(out, 400)}")
    run.log(kind="end", status="done")
    landed = next((x for x in out.splitlines() if x.startswith(f"{run.tid}: committed")), "")
    run.emit("closed", f"{run.tid} closed{'; ' + landed[len(run.tid) + 2:] if landed else ''} "
                       f"(tokens: {run.tokens[0]} in, {run.tokens[1]} out)", task=run.tid, tokens=run.tokens)


def _load(run, tid):
    """Rebuild a run from its journal: the newest unfinished one, or tid's."""
    def records(path):
        out = []
        try:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    try:
                        out.append(json.loads(line))
                    except ValueError:  # a line torn by the kill
                        pass
        except OSError:
            pass
        return out
    paths = []
    if os.path.isdir(run.jdir):
        paths = sorted((os.path.join(run.jdir, n) for n in os.listdir(run.jdir) if n.endswith(".jsonl")),
                       key=os.path.getmtime, reverse=True)
    if tid:
        paths = [x for x in paths if os.path.basename(x) == f"{tid}.jsonl"]
    for path in paths:
        recs = records(path)
        if recs and recs[0].get("kind") == "start" and not any(r.get("kind") == "end" for r in recs):
            break
    else:
        raise CodeError(f"nothing to resume{' for ' + tid if tid else ''}: no unfinished fm code journal in {run.jdir}")
    start = recs[0]
    run.journal, run.tid, run.plan, run.request = path, start["task"], start["plan"], start["request"]
    run.model_name, run.close_notes = start.get("model"), None
    opts = start.get("options") or {}
    run.no_commit = run.no_commit or bool(opts.get("no_commit"))
    run.escalate = run.args.escalate or opts.get("escalate")
    run.max_steps = run.args.max_steps or opts.get("max_steps")
    for r in recs[1:]:
        k = r.get("kind")
        if k == "msg":
            run.msgs.setdefault(r["phase"], []).append(r["msg"])
            run.turns += r["msg"].get("role") == "assistant"
        elif k == "phase_done":
            run.done.add(r["phase"])
        elif k == "baseline":
            run.baseline = r["text"]
        elif k == "close_notes":
            run.close_notes = r["notes"]


def _models(args, fmcli):
    try:
        default, conf = m.configured()
        profs = m.profiles()
    except m.ModelError as e:
        raise fmcli.UsageError(str(e))
    try:
        chosen = m.resolve()["name"]
    except m.ModelError:
        chosen = None
    rows = []
    for pr in profs:
        src = "models.json" if pr["name"] in conf else "local server, answering" if not pr["key_env"] else \
            f"{pr['key_env']} is set"
        rows.append(dict(pr, source=src, default=pr["name"] == chosen))
    lines = [f"{'*' if r['default'] else ' '} {r['name']:<12} {r['kind']:<9} {r['model']:<28} {r['source']}"
             for r in rows]
    fmcli.out(args, {"profiles": rows, "default": chosen},
              "\n".join(lines) + "\n(* the one fm code uses without --model)" if rows else
              "No model: no models.json profile, no local server answering, no API key set.")
