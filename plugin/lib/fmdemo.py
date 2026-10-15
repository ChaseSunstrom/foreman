"""fm demo (T-0870): Foreman at work in under a minute, with no model calls. A throwaway git repo with a seeded bug, a
Foreman home of its own, and the real fm CLI and PreToolUse guard hook playing Claude's part with canned moves: an edit
refused for want of a task, the task planned, rm -rf ~ refused, a red test recorded, the fix, a green test, a close
refused for a missing audit and then made. Everything lives in one temp folder, deleted at the end (Ctrl-C too)."""
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FM = os.path.join(PLUGIN, "bin", "fm")
HOOK = os.path.join(PLUGIN, "hooks", "hook")
TEST = "python3 -m unittest -q test_calc"
BUG = "def add(a, b):\n    return a - b\n"
FIXED = "def add(a, b):\n    return a + b\n"
UNIT = ("import unittest\n\nfrom calc import add\n\n\nclass Add(unittest.TestCase):\n    def test_add(self):\n"
        "        self.assertEqual(add(2, 3), 5)\n")


class Off(Exception):
    """A real command did something the demo didn't expect: Foreman's behaviour changed."""


def _env(work):
    """Nothing of the user's: no FOREMAN_*/CLAUDE* variables, a fake HOME, and a `claude` on PATH that only notes it
    was called (the demo never calls a model; the note fails the run if it did)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("FOREMAN_", "CLAUDE", "GIT_"))}
    bin_ = os.path.join(work, "bin")
    os.makedirs(bin_)
    with open(os.path.join(bin_, "claude"), "w") as f:
        f.write(f"#!/bin/sh\ntouch {shlex.quote(os.path.join(work, 'claude-called'))}\nexit 97\n")
    os.chmod(os.path.join(bin_, "claude"), 0o755)
    for d in ("home", "foreman", "xdg"):
        os.makedirs(os.path.join(work, d))
    env.update(HOME=os.path.join(work, "home"), FOREMAN_HOME=os.path.join(work, "foreman"),
               XDG_STATE_HOME=os.path.join(work, "xdg"), FOREMAN_NO_BACKGROUND="1", PYTHONDONTWRITEBYTECODE="1",
               GIT_CONFIG_NOSYSTEM="1", PATH=bin_ + os.pathsep + env.get("PATH", ""))
    return env


def _run(cmd, env, cwd, stdin=None):
    return subprocess.run(cmd, env=env, cwd=cwd, input=stdin, capture_output=True, text=True, timeout=60,
                          stdin=None if stdin is not None else subprocess.DEVNULL)


def _fm(env, repo, *args, ok=True):
    print("  $ fm " + " ".join(f'"{a}"' if " " in a else a for a in args))
    p = _run([sys.executable, FM, *args], env, repo)
    if (p.returncode == 0) != ok:
        raise Off(f"fm {args[0]} {args[1] if len(args) > 1 else ''} exited {p.returncode}: "
                  f"{(p.stderr or p.stdout).strip()[-400:]}")
    return p


def _hook(env, repo, tool, tool_input):
    """The guard's answer to one tool call, through the real PreToolUse hook: its reason when it denies."""
    payload = {"session_id": "fm-demo", "cwd": repo, "hook_event_name": "PreToolUse", "tool_name": tool,
               "tool_input": tool_input}
    p = _run([sys.executable, HOOK, "PreToolUse"], env, repo, json.dumps(payload))
    try:
        out = json.loads(p.stdout.strip().splitlines()[-1])["hookSpecificOutput"]
    except (ValueError, IndexError, KeyError):
        out = {}
    if out.get("permissionDecision") != "deny":
        raise Off(f"the guard let {tool} {json.dumps(tool_input)} through (exit {p.returncode})")
    return out["permissionDecisionReason"]


def _write(repo, name, text):
    with open(os.path.join(repo, name), "w") as f:
        f.write(text)


def _say(n, text):
    print(f"\n{n}. {text}")


def demo(work):
    def show(text):  # the temp folder's long path reads as <demo>
        print(text.replace(work, "<demo>"))
    env, repo = _env(work), os.path.join(work, "repo")
    os.makedirs(repo)
    _write(repo, "calc.py", BUG)
    for cmd in (["git", "init", "-q", "-b", "main"], ["git", "config", "user.email", "demo@example.com"],
                ["git", "config", "user.name", "fm demo"], ["git", "add", "."], ["git", "commit", "-qm", "seed"]):
        if _run(cmd, env, repo).returncode:
            raise Off(f"{' '.join(cmd)} failed: is git installed?")
    _run([sys.executable, FM, "init"], env, repo)
    print("Foreman demo: no model is called; the real fm and guard hook run in a throwaway repo and Foreman home.")
    _say(1, "The repo has a bug: calc.add(2, 3) returns -1. Claude tries to edit calc.py before any task exists.")
    show("  Refused: " + _hook(env, repo, "Edit", {"file_path": os.path.join(repo, "calc.py"),
                                                    "old_string": "a - b", "new_string": "a + b"}))
    _say(2, "So it plans the work first: a brief with a done-when and the command that proves it.")
    p = _fm(env, repo, "task", "new", "add() subtracts", "--type", "FIX", "--tier", "S",
            "--ac", f"add(2, 3) is 5 :: {TEST}", "--step", "a test for add, failing first", "--step", "fix add",
            "--focus")
    show("  " + p.stdout.splitlines()[0])
    _say(3, "Mid-task, a careless command: rm -rf ~ (here ~ is the demo's own fake home).")
    show("  Refused: " + _hook(env, repo, "Bash", {"command": "rm -rf ~"}))
    _say(4, "Test first: Claude writes test_calc.py and records it as the step's evidence.")
    _write(repo, "test_calc.py", UNIT)
    _fm(env, repo, "task", "evidence", "T-0001", "--step", "1", "--run", TEST, ok=False)
    print("  red: the test fails (AssertionError: -1 != 5), which proves it catches the bug.")
    _say(5, "The fix: return a + b. The same test, recorded again.")
    _write(repo, "calc.py", FIXED)
    _fm(env, repo, "task", "evidence", "T-0001", "--step", "2", "--run", TEST)
    print("  green: the test passes now.")
    _say(6, "Claude tries to close the task without saying how it checked its work.")
    p = _fm(env, repo, "task", "finish", "T-0001", ok=False)
    print("  not finished: " + (p.stderr or p.stdout).strip().splitlines()[0].removeprefix("fm: "))
    _say(7, "With the audit, a lesson and a commit message, the close goes through.")
    p = _fm(env, repo, "task", "finish", "T-0001", "--audit", "self checklist: diff read, test red then green",
            "--result", "pass", "--docs", "none: a demo", "--lesson", "a test that failed first is the proof",
            "--why-not-caught", "none: the bug was seeded", "--commit", "Fix add() subtracting (T-0001)")
    if "T-0001 done" not in p.stdout:
        raise Off("fm task finish exited 0 without closing T-0001: " + p.stdout.strip()[-400:])
    print("  closed: " + "\n  ".join(p.stdout.strip().splitlines()))
    if os.path.exists(os.path.join(work, "claude-called")):
        raise Off("claude was called")


def cmd_demo(args):
    work = tempfile.mkdtemp(prefix="fm-demo-")
    try:
        demo(work)
    except KeyboardInterrupt:
        print("\nStopped.")
        return 130
    except (Off, OSError, subprocess.TimeoutExpired) as e:
        print(f"\nfm demo: Foreman didn't do what the demo expects: {e}", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("\nThe demo's repo and Foreman home are deleted: nothing was left behind. "
          "To start for real: fm init in your repo, or just give Claude a request.")
    return 0
