"""T-3252: the tests' fm calls through a fork server. One process imports Sampo once; each call forks it, so a call
costs a fork and the verb's own work instead of a fresh interpreter's start and imports (60-200 ms under load).

A forked call gets exactly the argv, cwd, environment and stdin the test gave it, and returns a CompletedProcess like
subprocess.run. Only modules that read nothing from the environment at import are loaded ahead (PRELOAD; an audit test
holds them to it), so no fork inherits the server's settings. Any trouble reaching the server falls back to a fresh
subprocess, and FOREMAN_FORK_CLI=0 turns the server off.

Each request: the server forks a manager (which owns the connection), the manager forks the worker that runs the
script, waits for it and sends back its exit status. The worker's pid goes to the client first, so a timeout kills it.
"""
import atexit
import json
import locale
import os
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(os.path.dirname(HERE), "lib")
# sampo.cli, then what its first parser build imports (15 of a cold call's ~18 ms): preloaded, a fork skips them
PRELOAD = ("sampo.core", "sampo.cli", "sampo.design", "sampo.instr", "sampo.scene", "sampo.smoke", "inspect",
           "dataclasses", "tokenize", "glob", "base64", "colorsys", "copy")
# what sampo.core does to the environment at import (SAMPO_X becomes FOREMAN_X; Claude's bin folder joins PATH): each
# call does it again on its own environment, as a fresh process would
REAPPLY = ("mirror_env", "claude_path")
# what a fresh interpreter can't be given after it starts: a call that changes one of these runs as a fresh process
START_ENV = ("PYTHON", "LC_", "LANG", "TZ")
_LOCK = threading.Lock()
_SERVER = {}  # pid -> (socket path, process), or (None, None) when it couldn't start: one try per test process
_BASE_PATH = []  # the server's sys.path after its script folder: what a fresh `python3 SCRIPT` has after its own


def _die_with_parent():
    """A forked manager or worker dies with its parent, as run.py's classes do (T-2034), so a killed test or server
    leaves no fm call running in its own session."""
    try:
        import ctypes
        ctypes.CDLL(None).prctl(1, signal.SIGKILL)  # PR_SET_PDEATHSIG
    except (OSError, AttributeError):
        pass


def _send(conn, obj):
    data = json.dumps(obj).encode()
    conn.sendall(len(data).to_bytes(4, "big") + data)


def _recv(conn):
    head = b""
    while len(head) < 4:
        part = conn.recv(4 - len(head))
        if not part:
            raise ConnectionError("closed")
        head += part
    size, data = int.from_bytes(head, "big"), b""
    while len(data) < size:
        part = conn.recv(size - len(data))
        if not part:
            raise ConnectionError("closed")
        data += part
    return json.loads(data)


def _worker(req):
    """In the forked worker: become the fresh `python3 SCRIPT ARGS` the test asked for, then exit."""
    import runpy
    code = 1
    try:
        os.setsid()
        _die_with_parent()
        os.chdir(req["cwd"])
        os.environ.clear()
        os.environ.update(req["env"])
        tempfile.tempdir = None  # the server's cached temp folder: this call's TMPDIR decides, as in a fresh process
        core = sys.modules.get("sampo.core")
        for name in REAPPLY if core else ():
            getattr(core, name)(os.environ)
        for fd, path, mode in ((0, req["stdin"], os.O_RDONLY), (1, req["stdout"], os.O_WRONLY),
                               (2, req["stderr"], os.O_WRONLY)):
            f = os.open(path, mode)
            os.dup2(f, fd)
            os.close(f)
        sys.argv = [req["script"], *req["args"]]
        sys.path[:] = [os.path.dirname(os.path.abspath(req["script"])), *_BASE_PATH]  # as `python3 SCRIPT` sets it
        try:
            runpy.run_path(req["script"], run_name="__main__")
            code = 0
        except SystemExit as e:
            if e.code is None:
                code = 0
            elif isinstance(e.code, int):
                code = e.code
            else:
                sys.stderr.write(f"{e.code}\n")
                code = 1
        except BaseException:  # noqa: BLE001 - a fresh interpreter prints the traceback and exits 1
            traceback.print_exc()
            code = 1
        threading._shutdown()  # what a fresh interpreter does at exit: join its threads, run atexit
        atexit._run_exitfuncs()
    finally:
        for s in (sys.stdout, sys.stderr):
            try:
                s.flush()
            except Exception:  # noqa: BLE001
                pass
        os._exit(code & 0xFF)  # sys.exit(-1) is 255, as in a fresh process


def serve(path, parent):
    """The server: import ahead, then fork a manager per connection until the test process is gone; its folder goes
    with it."""
    me = os.getpid()
    _BASE_PATH[:] = sys.path[1:]
    sys.path.insert(0, LIB)
    import argparse  # noqa: F401 - warm what every call needs
    import runpy  # noqa: F401
    for mod in PRELOAD:
        __import__(mod)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # managers reap themselves
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))  # stop(): the finally below still runs
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        srv.bind(path)
        srv.listen(64)
        srv.settimeout(1.0)
        print("ready", flush=True)
        while os.getppid() == parent:
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            if os.fork() == 0:
                srv.close()
                _manage(conn)
            conn.close()
    finally:
        if os.getpid() == me:  # never a forked child's exit
            shutil.rmtree(os.path.dirname(path), ignore_errors=True)


def _manage(conn):
    """In the forked manager: run one request's worker, send its pid, wait, send its exit status, exit."""
    signal.signal(signal.SIGCHLD, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    _die_with_parent()
    try:
        conn.settimeout(None)
        req = _recv(conn)
        pid = os.fork()
        if pid == 0:
            conn.close()
            _worker(req)
        _send(conn, {"pid": pid})
        _, status = os.waitpid(pid, 0)
        _send(conn, {"code": os.waitstatus_to_exitcode(status)})
    except Exception:  # noqa: BLE001 - the client reads a closed connection
        pass
    os._exit(0)


def _server():
    """This process's server's socket path, started on first use; None when off or it couldn't start (tried once)."""
    if os.environ.get("FOREMAN_FORK_CLI") == "0":
        return None
    with _LOCK:
        got = _SERVER.get(os.getpid())
        if got and (got[1] is None or got[1].poll() is None):
            return got[0]
        base = tempfile.gettempdir()  # the class TMPDIR run.py removes after the class, so a killed server leaks nothing
        folder = tempfile.mkdtemp(prefix="fmfork-", dir=base if len(base) < 60 else ("/tmp" if os.path.isdir("/tmp") else None))
        path, p = os.path.join(folder, "s"), None
        env = {k: v for k, v in os.environ.items() if not k.startswith("FOREMAN_")}
        try:
            p = subprocess.Popen([sys.executable, os.path.abspath(__file__), "serve", path, str(os.getpid())],
                                 stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                 env=env, start_new_session=True)
            ok = p.stdout.readline().strip() == b"ready"
        except OSError:
            ok = False
        if not ok:
            if p:
                p.kill()
                p.wait()
            shutil.rmtree(folder, ignore_errors=True)
            _SERVER[os.getpid()] = (None, None)
            return None
        _SERVER[os.getpid()] = (path, p)
        return path


def stop():
    """Stop this process's server and remove its folder (tests; the server also ends by itself, folder and all, when
    its test process exits)."""
    with _LOCK:
        got = _SERVER.pop(os.getpid(), None)
    if got and got[1]:
        got[1].terminate()
        try:
            got[1].wait(10)
        except subprocess.TimeoutExpired:
            got[1].kill()
            got[1].wait()
        shutil.rmtree(os.path.dirname(got[0]), ignore_errors=True)


def run(script, args, cwd=None, env=None, input=None, timeout=None):
    """subprocess.run([sys.executable, script, *args], capture_output=True, text=True, ...) through the server."""
    argv = [sys.executable, script, *args]
    cwd = os.path.abspath(cwd or os.getcwd())
    env = dict(os.environ if env is None else env)
    # an interpreter or locale setting (PYTHONPATH, -X options, LC_ALL, TZ) shapes a fresh start, which a fork lacks
    same_start = all(env.get(k) == os.environ.get(k) for k in set(env) | set(os.environ) if k.startswith(START_ENV))
    path = _server() if os.path.isdir(cwd) and same_start else None
    fresh = lambda: subprocess.run(argv, cwd=cwd, env=env, input=input, capture_output=True, text=True, timeout=timeout)
    if path is None:
        return fresh()
    with tempfile.TemporaryDirectory(prefix="fmcall-") as d:
        files = {k: os.path.join(d, k) for k in ("stdin", "stdout", "stderr")}
        with open(files["stdin"], "w", encoding=locale.getpreferredencoding(False)) as f:
            f.write(input or "")
        for k in ("stdout", "stderr"):
            open(files[k], "w").close()
        conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            conn.connect(path)
        except OSError:  # the server is gone: nothing ran yet, so a fresh process is safe
            conn.close()
            return fresh()
        pid = None
        try:
            conn.settimeout(timeout)
            _send(conn, {"script": script, "args": list(args), "cwd": cwd, "env": env,
                         **files, "stdin": files["stdin"] if input is not None else os.devnull})
            pid = _recv(conn)["pid"]
            code = _recv(conn)["code"]
        except socket.timeout:
            if pid:
                try:
                    os.killpg(pid, signal.SIGKILL)
                except OSError:
                    pass
            raise subprocess.TimeoutExpired(argv, timeout)
        except (OSError, ConnectionError, ValueError, KeyError) as e:  # never rerun: the call may have started
            raise RuntimeError(f"forkcli: the fork server dropped the call ({e}); FOREMAN_FORK_CLI=0 runs fresh") from e
        finally:
            conn.close()
        out = []
        for k in ("stdout", "stderr"):
            with open(files[k], encoding=locale.getpreferredencoding(False), errors="replace") as f:
                out.append(f.read())
    return subprocess.CompletedProcess(argv, code, out[0], out[1])


if __name__ == "__main__" and sys.argv[1:2] == ["serve"]:
    serve(sys.argv[2], int(sys.argv[3]))
