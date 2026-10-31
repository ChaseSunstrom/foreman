"""fm find (T-2121): deterministic, language-agnostic finders over a tree. Untested public functions, docs naming code
that doesn't exist, imports no manifest declares, SQL built from a parameter, list membership inside a loop, unseeded
randomness in tests, credentials. Each is a candidate until proven; every finder reports nothing on every clean exam
render (test_find)."""
import bisect
import io
import json
import os
import re
import stat
import subprocess
import sys
import tokenize
import tomllib

import fmcore as c

LANG = {".py": "py", ".js": "js", ".mjs": "js", ".cjs": "js", ".jsx": "js", ".ts": "ts", ".tsx": "ts", ".mts": "ts",
        ".cts": "ts", ".rb": "rb", ".rs": "rs", ".c": "c", ".h": "c", ".cc": "c", ".cpp": "c", ".hpp": "c"}
SKIP = {"node_modules", "vendor", "target", "build", "dist", "__pycache__", "third_party", "site-packages",
        "fixtures", "testdata", "__fixtures__", "__snapshots__", "venv", "env"}  # fixtures are planted on purpose
OPEN_CAP = 5  # T-2235: tasks fm find/prove --capture keep open at once, so repeated runs can't flood the queue
TEST = re.compile(r"(?:^|/)(?:tests?|spec|__tests__)/|(?:^|/)(?:test_[^/]*|conftest\.py)$|[_.](?:test|spec)\.\w+$")
_JSFN = r"^([ \t]*)(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s*\*?\s*(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)"
_JSARROW = r"^([ \t]*)(?:export\s+)?(?:const|let|var)\s+(\w+)\s*(?::[^=]+)?=\s*(?:async\s*)?\(([^)]*)\)[^=]*=>"
DEFS = {"py": [r"^([ \t]*)(?:async\s+)?def\s+(\w+)\s*\(([^)]*)"], "js": [_JSFN, _JSARROW], "ts": [_JSFN, _JSARROW],
        "rb": [r"^([ \t]*)def\s+(?:self\.)?(\w+[?!=]?)\s*\(?([^)\n#]*)"],
        "rs": [r"^([ \t]*)(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?(?:unsafe\s+)?(?:const\s+)?fn\s+(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)"],
        "c": [r"^()(?:\w+[ \t*]+)+?(\w+)\s*\(([^;{)]*)\)\s*\{?\s*$"]}
DEFS = {k: [re.compile(r) for r in v] for k, v in DEFS.items()}
KEYWORDS = {"if", "for", "while", "switch", "return", "sizeof", "else", "do", "case", "defined", "elif", "and", "or",
            "not", "in", "unless", "until", "def", "fn", "function", "match", "catch", "typeof", "new", "await", "yield"}
IMPORT = re.compile(r"""^\s*(?:import\b|from\s+\S+\s+import\b|(?:pub\s+)?use\s|extern\s+crate\b|mod\s+\w+\s*;|#\s*include\b|#\[path)"""
                    r"""|\brequire(?:_relative)?\s*\(?\s*["']""")
LOOP = re.compile(r"\b(?:for|while|loop)\b|\.(?:each|forEach|map|filter|times|iter)\b")
SQL = re.compile(r"(?i)\b(?:select\s.*\bfrom|insert\s+into|update\s+\w+\s+set|delete\s+from)\b")
INIT = {"py": r"^\s*(\w+)(?:\s*:[^=]+)?\s*=\s*\[\]", "rb": r"^\s*(\w+)\s*=\s*\[\]",
        "js": r"\b(?:const|let|var)\s+(\w+)(?:\s*:[^=]+)?\s*=\s*\[\]",
        "rs": r"\blet\s+mut\s+(\w+)(?:\s*:[^=]+)?\s*=\s*(?:Vec::new\(\)|vec!\[\])"}
INIT["ts"] = INIT["js"]
USE = {"py": r"\bin\s+{v}\b", "js": r"\b{v}\.(?:includes|indexOf)\(", "rb": r"\b{v}\.(?:include\?|index\b)",
       "rs": r"\b{v}\.(?:contains\(|iter\(\)\.any\()"}
USE["ts"] = USE["js"]
RAND = {"py": r"\brandom\.(?:random|randint|choice|choices|shuffle|uniform|randrange|sample)\(", "js": r"\bMath\.random\(",
        "rb": r"(?<![\w.])rand\(|\.(?:sample|shuffle)\b", "rs": r"\bRandomState::new\(|\bthread_rng\(|\brand::random\b",
        "c": r"(?<!\w)rand\(\s*\)"}
RAND["ts"] = RAND["js"]
SEED = {"py": r"\brandom\.seed\(", "rb": r"\bsrand\(\s*\d|Random\.new\(\s*\d", "c": r"\bsrand\((?!.*\b(?:time|clock|getpid)\s*\()"}
NODE = set("assert async_hooks buffer child_process cluster console constants crypto dgram diagnostics_channel dns events "
           "fs http http2 https inspector module net os path perf_hooks process punycode querystring readline repl stream "
           "string_decoder test timers tls trace_events tty url util v8 vm wasi worker_threads zlib".split())
RUBY = set("abbrev base64 benchmark bigdecimal bundler cgi coverage csv date delegate digest english erb etc fiddle "
           "fileutils find forwardable getoptlong io ipaddr json logger matrix minitest mkmf monitor net objspace observer "
           "open-uri open3 openssl optparse ostruct pathname pp prettyprint prime pstore psych racc rake rbconfig readline "
           "resolv ripper rubygems securerandom set shellwords singleton socket stringio strscan tempfile test thread time "
           "timeout tmpdir tsort uri weakref yaml zlib".split())
RUST = {"std", "core", "alloc", "crate", "self", "super", "proc_macro", "test"}
CH = set("assert complex ctype errno fenv float inttypes iso646 limits locale math setjmp signal stdalign stdarg stdatomic "
         "stdbool stddef stdint stdio stdlib stdnoreturn string tgmath threads time uchar wchar wctype aio dirent dlfcn "
         "fcntl fnmatch ftw getopt glob grp iconv ifaddrs langinfo libgen malloc mqueue netdb nl_types poll pthread pwd "
         "regex sched search semaphore spawn strings syslog termios unistd utime utmpx wordexp windows winsock2".split())
CDIRS = {"sys", "netinet", "arpa", "net", "linux", "asm", "bits"}
BUILTIN = set("printf fprintf snprintf sprintf puts putchar malloc calloc realloc free strlen strcmp strncmp strcpy strncpy "
              "strcat memcpy memmove memset memcmp abs labs exit abort assert rand srand time clock qsort atoi atol strtol "
              "fopen fclose fread fwrite fgets getchar perror strchr strrchr strstr isalpha isdigit isspace tolower toupper "
              "puts print p pp raise require format sprintf loop lambda proc Integer Float String Array Hash rand "
              "attr_reader attr_accessor include extend private".split())
PY_ALIAS = {"bs4": "beautifulsoup4", "pil": "pillow", "cv2": "opencv", "sklearn": "scikit-learn", "gi": "pygobject",
            # import name (lower case) → distribution, a fixed table: never the host's installed packages (T-2237)
            "yaml": "pyyaml", "dateutil": "python-dateutil", "google": "protobuf", "attr": "attrs", "jwt": "pyjwt",
            "magic": "python-magic", "serial": "pyserial", "crypto": "pycryptodome", "cryptodome": "pycryptodomex",
            "dotenv": "python-dotenv", "git": "gitpython", "markdown": "markdown", "mysqldb": "mysqlclient",
            "psycopg2": "psycopg2-binary", "usb": "pyusb", "zmq": "pyzmq", "skimage": "scikit-image",
            "openssl": "pyopenssl", "docx": "python-docx", "pptx": "python-pptx", "slugify": "python-slugify",
            "jose": "python-jose", "multipart": "python-multipart", "socks": "pysocks", "wx": "wxpython",
            "pkg_resources": "setuptools", "bson": "pymongo", "fitz": "pymupdf", "lxml": "lxml", "ldap": "python-ldap",
            "nacl": "pynacl", "engineio": "python-engineio", "socketio": "python-socketio", "discord": "discord-py",
            "telegram": "python-telegram-bot", "jenkins": "python-jenkins", "consul": "python-consul",
            "snappy": "python-snappy", "levenshtein": "python-levenshtein", "tomli_w": "tomli-w", "ruamel": "ruamel-yaml",
            "yaml_include": "pyyaml-include", "win32api": "pywin32", "win32con": "pywin32", "pythoncom": "pywin32"}


class Src:
    def __init__(self, rel, text):
        self.rel, self.text = rel, text
        self.lines = [x if len(x) <= 2000 else "" for x in text.split("\n")]  # minified or hostile: data, not code
        self.lang, self.test = LANG[os.path.splitext(rel)[1].lower()], bool(TEST.search(rel))
        self.instr, quote = set(), None  # Python lines inside a triple-quoted string: code there is data
        opens = [getattr(tokenize, n, None) for n in ("FSTRING_START", "TSTRING_START")]  # 3.12+ / 3.14+
        closes = [getattr(tokenize, n, None) for n in ("FSTRING_END", "TSTRING_END")]
        try:  # a string token over several lines: its later lines are data (tokenize parses, never runs, the text)
            if self.lang == "py" and any(len(x) > 2000 for x in text.split("\n")):
                raise ValueError("a minified line: tokenizing it costs a token per character")
            starts = []  # rows where the open f/t-strings began, nesting-aware
            for t in tokenize.generate_tokens(io.StringIO(text).readline) if self.lang == "py" else ():
                if t.type in opens:
                    starts.append(t.start[0])
                elif t.type in closes and starts:
                    self.instr.update(range(starts.pop(), t.end[0]))
                elif t.type == tokenize.STRING and t.end[0] > t.start[0]:
                    self.instr.update(range(t.start[0], t.end[0]))  # 1-based rows: start..end-1 are 0-based 2nd..last
        except (tokenize.TokenError, SyntaxError, ValueError):  # unparseable: count the marks instead
            self.instr.clear()
            for i, line in enumerate(self.lines):
                if quote:
                    self.instr.add(i)
                for m in re.finditer(r'"""|\'\'\'', line):
                    quote = m.group() if quote is None else None if m.group() == quote else quote
        self.defs = []  # (line, indent, name, params)
        for i, line in enumerate(self.lines):
            if i in self.instr:
                continue
            for rx in DEFS[self.lang]:
                m = rx.match(line)
                if m and m.group(2) not in KEYWORDS:
                    self.defs.append((i, len(m.group(1)), m.group(2), set(re.findall(r"[A-Za-z_]\w*", m.group(3)))))
                    break
        self._at = [d[0] for d in self.defs]

    def fn(self, i):
        """The definition enclosing line i: the nearest one above. ponytail: top-level code after a function counts as
        that function's; brace-matching would fix it."""
        k = bisect.bisect_right(self._at, i) - 1
        return self.defs[k] if k >= 0 else None

    def body(self, d):
        k = self.defs.index(d)
        return range(d[0], self.defs[k + 1][0] if k + 1 < len(self.defs) else len(self.lines))

    def own(self, d):
        """The words of d's own lines: the def line and the lines indented under it, nested functions included; code
        after it at its own indent or less isn't."""
        rows = [self.lines[d[0]]]
        for j in range(d[0] + 1, len(self.lines)):
            row = self.lines[j]
            ind = len(row) - len(row.lstrip())
            if row.strip() and ind <= d[1] and j not in self.instr and not re.match(r"\s*(?:[})\]]|end\b)", row):
                break
            rows.append(row)
        return _words("\n".join(rows))


def _in_str(line, pos):
    """Whether pos sits inside a quoted string on its line (odd count of one quote kind before it)."""
    return any(line[:pos].count(q) % 2 for q in "\"'`")


def _found(finder, kind, s, line, symbol, says):
    return {"finder": finder, "kind": kind, "file": s if isinstance(s, str) else s.rel, "line": line, "symbol": symbol,
            "says": says}


def _word(name):
    return re.compile(rf"(?<!\w){re.escape(name)}(?![\w?!])")


def _words(text):
    """The whole words of a text, as _word sees them: one set lookup per name instead of one scan."""
    return set(re.findall(r"\w+[?!]?", text))


def _files(root):
    """([(rel, text)], every path listed): git's view of the tree when it's a checkout, else a walk; vendored
    directories, untracked hidden ones (T-2235: tracked ones like .github are read), generated files, binaries, files
    over 1 MB and anything reached through a symlink are left out."""
    def ls(*how):  # the repo isn't trusted: none of its config may run code (fsmonitor, hooks)
        r = subprocess.run(["git", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", "-C", root,
                            "ls-files", *how, "-z"], capture_output=True, timeout=60)
        return [os.fsdecode(p) for p in r.stdout.split(b"\0") if p] if r.returncode == 0 else []
    try:
        tracked = ls("-c")
        rels = tracked + ls("-o", "--exclude-standard")
    except (OSError, subprocess.SubprocessError):
        tracked, rels = [], []
    tracked, real = set(tracked), os.path.realpath(root)
    if not rels:  # not a checkout, no git, or a folder the parent repo ignores
        for d, dirs, names in os.walk(root):
            dirs[:] = sorted(x for x in dirs if not x.startswith(".") and x not in SKIP)
            rels += [os.path.relpath(os.path.join(d, n), root).replace(os.sep, "/") for n in sorted(names)]
    import fmmap
    out, gen = [], []
    for rel in rels:
        p = os.path.join(root, rel)
        if any((x.startswith(".") and rel not in tracked) or x in SKIP for x in rel.split("/")[:-1]):
            continue
        if os.path.realpath(p) != os.path.join(real, *rel.split("/")):  # T-2235: a symlinked parent directory
            continue
        try:  # regular files only: a symlink may point at /dev/zero, a FIFO or a file outside the tree
            st = os.lstat(p)
            if not stat.S_ISREG(st.st_mode) or st.st_size > 1 << 20:
                continue
            with open(p, "rb") as f:
                data = f.read((1 << 20) + 1)
        except OSError:
            continue
        if b"\0" not in data[:8192]:
            (gen if fmmap.is_generated(p) else out).append((rel, data.decode("utf-8", "replace")))
    return out, rels, gen


def _untested(code):
    tests = [s for s in code if s.test or s.lang == "rs" and "#[test]" in s.text]  # Rust unit tests live inline
    if not tests:
        return []
    said = _words("\n".join(line for s in tests for line in s.lines if not IMPORT.search(line)))
    whole = _words("\n".join(s.text for s in tests))
    bodies = {}  # a function a test reaches covers what it calls: black-box (CLI, HTTP) tests reach code by name
    for s in code:
        for d in s.defs:
            if not s.test:
                bodies.setdefault(d[2], set()).update(s.own(d))
    reached, todo = set(), list(said | {"main"})
    while todo:
        n = todo.pop()
        if n not in reached:
            reached.add(n)
            todo += bodies.get(n, ())
    out = []
    for s in code:
        if s.test or s.lang == "c" and not s.rel.endswith((".c", ".cc", ".cpp")):
            continue
        lists = re.findall(r"(?:module\.exports\s*=|export)\s*\{([^}]*)\}", s.text)
        exported = set(re.findall(r"\w+", " ".join(lists))) | set(re.findall(r"exports\.(\w+)\s*=", s.text))
        pub = []
        for i, ind, name, _ in s.defs:
            line = s.lines[i]
            if ind or name == "main" or name.startswith(("test", "_")):
                continue
            if {"py": True, "rb": True, "rs": line.startswith("pub"), "c": not line.startswith(("static", "inline")),
                    "js": line.startswith("export") or name in exported,
                    "ts": line.startswith("export") or name in exported}[s.lang]:
                pub.append((i, name))
        stem = os.path.splitext(os.path.basename(s.rel))[0]
        if pub and stem not in whole | reached and not any(n in reached for _, n in pub):  # lazy("fmx", …) names it too
            out.append(_found("untested", "untested", s, pub[0][0] + 1, stem, f"no test names the module {stem}"))
            continue
        out += [_found("untested", "untested", s, i + 1, name, f"{name} is public and no test calls it")
                for i, name in pub if name not in reached]
    return out


def _docs(files, code, root):
    import fmdocs
    text = _words("\n".join(s.text for s in code))
    defined = {d[2] for s in code for d in s.defs}
    out = []
    for rel, body in files:
        if not rel.lower().endswith((".md", ".markdown")):
            continue
        body = fmdocs._FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), body)
        spans = {}
        for m in re.finditer(r"`(\w+)\(", body):
            spans.setdefault(m.group(1), body.count("\n", 0, m.start()) + 1)
        if len(set(spans) & defined) * 2 > len(spans):  # the doc is about this code: most of what it names is defined
            out += [_found("docs", "docs", rel, line, n, f"the docs name {n}(), which no code has")
                    for n, line in spans.items() if n not in text]
    try:
        out += [_found("docs", "docs", f["file"], f.get("line") or 0, f["detail"], f"docs {f['kind']}: {f['detail']}")
                for f in fmdocs.scan(root)]
    except (OSError, ValueError):
        pass
    return out


def _sql(s):
    out, seen = [], set()
    for i, line in enumerate(s.lines):
        d = s.fn(i)
        if not d or not SQL.search(line) or not re.search(r"[\"'`]", line):
            continue
        names = set(re.findall(r"\+\s*([A-Za-z_]\w*)\b(?!\s*[.(\[])", line))
        names |= set(re.findall(r"(?<![.\w])([A-Za-z_]\w*)\s*\+\s*[\"'`]", line))
        names |= set(re.findall(r"\{\s*([A-Za-z_]\w*)\s*\}", line))  # f-string, ${…}, #{…}, format!("{x}")
        tail = line[max(line.rfind('"'), line.rfind("'"), line.rfind("`")) + 1:]
        if re.search(r"format|printf", line):
            names |= set(re.findall(r",\s*([A-Za-z_]\w*)\s*(?=[,)])", tail))
        names |= set(re.findall(r"%\s*\(?\s*([A-Za-z_]\w*)\b(?!\s*[.(\[])", tail))
        hit = sorted(names & d[3])
        if hit and d[2] not in seen:
            seen.add(d[2])
            out.append(_found("sql", "vuln", s, i + 1, d[2], f"SQL built from the parameter {hit[0]} (injection)"))
    return out


def _slow(s):
    out = []
    if s.lang == "c":
        for d in s.defs:
            rows = [s.lines[j] for j in s.body(d)]
            ks = set(re.findall(r"\[(\w+)\+\+\]", "\n".join(rows)))
            for j, line in enumerate(rows):
                m = re.search(r"\bfor\s*\([^;]*;\s*\w+\s*<\s*(\w+)\s*;", line)
                if m and m.group(1) in ks and "==" in line + (rows[j + 1] if j + 1 < len(rows) else "") and \
                        any(LOOP.search(r) for r in rows[1:j]):
                    out.append(_found("slow", "slow", s, d[0] + j + 1, d[2], "a linear scan of the output for each "
                                      "input item (quadratic): a hash set"))
                    break
        return out
    for i, line in enumerate(s.lines):
        m, d = re.search(INIT[s.lang], line), s.fn(i)
        if not m or not d:
            continue
        use, looped = re.compile(USE[s.lang].format(v=re.escape(m.group(1)))), False
        for j in range(i + 1, s.body(d).stop):
            row = s.lines[j]
            looped = looped or bool(LOOP.search(row) and any(_word(p).search(row) for p in d[3]))
            u = use.search(row)
            if looped and u and not (s.lang == "py" and re.search(r"\bfor\s+[\w\s,()]+$", row[:u.start()])):
                out.append(_found("slow", "slow", s, j + 1, d[2], f"membership test on the list {m.group(1)} inside a "
                                  "loop over the input (quadratic): a set"))
                break
    return out


def _flaky(s):
    if s.lang not in RAND or s.lang in SEED and re.search(SEED[s.lang], s.text):
        return []
    out, seen = [], set()
    for i, line in enumerate(s.lines):
        m = re.search(RAND[s.lang], line)
        if m and not _in_str(line, m.start()):
            d = s.fn(i)
            name = d[2] if d else ""
            if name not in seen:
                seen.add(name)
                out.append(_found("flaky", "flaky", s, i + 1, name, "unseeded randomness in a test: it passes or "
                                  "fails by chance"))
    return out


def _norm(name):
    return re.sub(r"[-_.]+", "-", name.lower())


def _manifest(b, text):
    """The package names one manifest declares."""
    names = set()
    if re.match(r"(?:requirements|constraints).*\.txt$", b):
        names |= set(re.findall(r"(?m)^\s*([A-Za-z0-9][\w.-]*)", text))
    elif b == "package.json":
        try:
            pkg = json.loads(text)
        except (ValueError, RecursionError):
            return set()
        for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            names |= set((pkg.get(key) or {}) if isinstance(pkg, dict) else ())
        names.add(str(pkg.get("name") or "") if isinstance(pkg, dict) else "")
    elif b in ("pyproject.toml", "Cargo.toml"):
        t = tomllib.loads(text)
        proj, poetry = t.get("project") or {}, (t.get("tool") or {}).get("poetry") or {}
        reqs = list(proj.get("dependencies") or []) + [x for v in (proj.get("optional-dependencies") or {}).values()
                                                       for x in v] + \
            [x for v in (t.get("dependency-groups") or {}).values() for x in v if isinstance(x, str)]
        names |= {m.group(0) for m in (re.match(r"[A-Za-z0-9][\w.-]*", str(r)) for r in reqs) if m}
        for table in (poetry.get("dependencies"), poetry.get("dev-dependencies"), t.get("dependencies"),
                      t.get("dev-dependencies"), t.get("build-dependencies"), (t.get("workspace") or {}).get("dependencies"),
                      *[g.get("dependencies") for g in (poetry.get("group") or {}).values()]):
            names |= set(table or {})
        names |= {str(proj.get("name") or ""), str(poetry.get("name") or ""), str((t.get("package") or {}).get("name") or "")}
    elif b == "Gemfile" or b.endswith(".gemspec"):
        names |= set(re.findall(r"""(?m)^\s*(?:gem|\w+\.add_(?:runtime_|development_)?dependency)\s*\(?\s*["']([^"']+)""", text))
    return names


def _declared(root, files):
    names = set()
    for rel, text in files:
        try:
            names |= _manifest(os.path.basename(rel), text)
        except (ValueError, TypeError, AttributeError, RecursionError):  # a malformed manifest declares nothing
            pass
    return {_norm(n) for n in names if n}


def _imports(s, local, mods):
    """[(line, module, bindings)] for the third-party-looking imports of a file."""
    out = []
    for i, line in enumerate(s.lines):
        if s.lang == "py":
            m = re.match(r"^(\s*)(?:from\s+([\w.]+)\s+import\s+([^#]+)|import\s+([^#]+))", line)
            if not m or i in s.instr or (m.group(2) or "").startswith("."):
                continue
            if m.group(1):  # nested: an optional (try:) or conditional (if …:) import isn't a hard dependency
                up = next((s.lines[k] for k in range(i - 1, -1, -1) if s.lines[k].strip() and
                           len(s.lines[k]) - len(s.lines[k].lstrip()) < len(m.group(1))), "")
                if re.match(r"\s*(?:try|if|elif|else|except)\b", up):
                    continue
            if m.group(2):
                tops = [(m.group(2).split(".")[0], [x.split()[-1] for x in m.group(3).strip("()\\ ").split(",") if x.strip() not in ("", "*")])]
            else:
                tops = [(x.split()[0].split(".")[0], [x.split()[-1].split(".")[0]]) for x in m.group(4).split(",") if x.strip()]
            out += [(i, t, b) for t, b in tops if t not in sys.stdlib_module_names and t != "__future__" and t not in local]
        elif s.lang in ("js", "ts"):
            for m in re.finditer(r"""(?:\b(?:const|let|var)\s+([^=]+?)\s*=\s*)?\brequire\s*\(\s*["']([^"']+)["']\s*\)|"""
                                 r"""^\s*(?:import|export)\s+(?:(.+?)\s+from\s+)?["']([^"']+)["']""", line):
                spec, clause = m.group(2) or m.group(4), m.group(1) or m.group(3) or ""
                if spec.startswith(("npm:",)):
                    spec = spec[4:]
                if spec.startswith((".", "/", "~", "@/", "#")) or ":" in spec:
                    continue
                name = "/".join(spec.split("/")[:2]) if spec.startswith("@") else spec.split("/")[0]
                if name not in NODE and name not in local:
                    out.append((i, name, [w for w in re.findall(r"\w+", clause) if w not in ("as", "type")]))
        elif s.lang == "rb":
            m = re.match(r"""^\s*require\s*\(?\s*["']([^"']+)["']""", line)
            if m and m.group(1).split("/")[0] not in RUBY and os.path.basename(m.group(1)) not in local:
                out.append((i, m.group(1).split("/")[0], []))
        elif s.lang == "rs":
            m = re.match(r"^\s*(?:pub\s+)?(?:use\s+(?:::)?(\w+)(?:::(.*?))?|extern\s+crate\s+(\w+))\s*;", line)
            top = m and (m.group(1) or m.group(3))
            if top and top not in RUST and not top[0].isupper() and top not in local and top not in mods:
                out.append((i, top, [w for w in re.findall(r"\w+", (m.group(2) or top).split("::")[-1]) if w not in ("self", "as")] or [top]))
        elif s.lang == "c":
            m = re.match(r"^\s*#\s*include\s*<([^>]+)>", line)
            h = m and m.group(1)
            if h and h.endswith((".h", ".hpp")) and h[:-2].split(".")[0] not in CH and h.split("/")[0] not in CDIRS:
                out.append((i, h, []))
    return out


def _deps(root, files, code, rels):
    declared = _declared(root, files)
    local = {os.path.splitext(os.path.basename(r))[0] for r in rels} | {p for r in rels for p in r.split("/")[:-1]}
    headers = {os.path.basename(r) for r, _ in files if r.endswith((".h", ".hpp"))}
    build = "\n".join(t for r, t in files if os.path.basename(r) in ("Makefile", "makefile", "CMakeLists.txt",
                                                                    "meson.build", "configure.ac"))
    mods = {m for s in code if s.lang == "rs" for m in re.findall(r"(?m)^\s*(?:pub\s+)?mod\s+(\w+)", s.text)}
    defined = {d[2] for s in code for d in s.defs}
    out = []
    for s in code:
        for i, mod, binds in _imports(s, local, mods):
            n = _norm(mod)
            if s.lang == "c":
                stem = os.path.splitext(os.path.basename(mod))[0]
                if os.path.basename(mod) in headers or re.search(rf"\b{re.escape(stem)}\b", build):
                    continue
            elif s.lang == "py":
                alias = _norm(PY_ALIAS.get(mod.lower(), "")) or None
                cands = {n, alias}
                # ponytail: substring match (yaml in pyyaml) can hide an undeclared import (req vs requests);
                # grow PY_ALIAS if a miss shows up in the exam
                if any(x and (x in declared or len(x) >= 3 and any(x in d for d in declared)) for x in cands):
                    continue
            elif n in declared:
                continue
            if binds:
                users = {s.fn(j)[2] for j, row in enumerate(s.lines) if j != i and s.fn(j) and not IMPORT.search(row)
                         and any(_word(b).search(row) for b in binds)}
            else:  # Ruby and C bind no name: the functions calling something defined nowhere in the repo
                users = {s.fn(j)[2] for j, row in enumerate(s.lines) if s.fn(j) and j != s.fn(j)[0] and any(
                    x not in defined and x not in BUILTIN and x not in KEYWORDS
                    for x in re.findall(r"(?<![\w.:>$@])([A-Za-z_]\w*[?!]?)\s*\(", row))}
            out.append(_found("deps", "dep", s, i + 1, " ".join(sorted(users)) or mod,
                              f"imports {mod}, which no manifest declares and the standard library doesn't have"))
    return out


def scan(root, prec=None):
    """(files scanned, findings); ranked best first when prec (each finder's precision, a dict, maybe empty) is given."""
    files, rels, gen = _files(root)
    code = [Src(r, t) for r, t in files if os.path.splitext(r)[1].lower() in LANG]
    import fmsecrets
    out = _untested(code) + _docs(files, code, root) + _deps(root, files, code, rels)
    for s in code:
        out += _flaky(s) if s.test else _sql(s) + _slow(s)
    for rel, text in files + gen:  # a generated file can still hold a pasted key
        if TEST.search(rel):  # a test's credentials are fakes by design
            continue
        out += [_found("secrets", "secret", rel, n, "", f"credential: {kind}")
                for n, kind in fmsecrets.scan_text(text, config=bool(fmsecrets.CONFIG.search(rel)))]
    out = sorted(out, key=lambda f: (f["file"], f["line"], f["finder"]))
    return len(files), out if prec is None else rank(out, dict(files), prec)


def find(root):
    return scan(root)[1]


SEVERITY = {"secret": 1.0, "vuln": 1.0, "bug": 0.9, "dep": 0.6, "flaky": 0.5, "untested": 0.4, "slow": 0.3, "docs": 0.2}
FLOOR, BAR = 0.3, 0.1  # a finder whose precision is under FLOOR is muted; a score under BAR is held back as noise
HALF_LIFE = 180  # days: an outcome weighs half as much per HALF_LIFE, so a mute lifts once its drops age (7: two weeks)


def rank(found, texts, prec):
    """Best first, each given score = severity x reach x its finder's precision (default 0.5, the prior). Reach is 1 plus
    up to 0.5 for the other files naming the symbol, so it never lifts slow or docs past a vuln or a bug. A finder under
    FLOOR is muted and a score under BAR held back: both sort last, still listed. ponytail: proof and effort are 1 (every
    finding is a lead and no fix is sized yet); a failing test or a hunk estimate can feed them later."""
    words = {rel: _words(t) for rel, t in texts.items()}
    out = []
    for f in found:
        sym = (re.findall(r"\w+[?!]?", f["symbol"]) or [""])[0]
        n = sum(1 for rel, w in words.items() if rel != f["file"] and sym in w) if sym else 0
        reach = 1 + 0.5 * min(n, 10) / 10
        fp = prec.get(f["finder"], 0.5)
        score = round(SEVERITY.get(f["kind"], 0.2) * reach * fp, 3)
        held = "muted" if fp < FLOOR else "below the bar" if score < BAR else None
        out.append({**f, "score": score, "reach": reach} | ({"held": held} if held else {}))
    return sorted(out, key=lambda f: (bool(f.get("held")), -f["score"], f["file"], f["line"]))


def precision(p):
    """{finder: (real + 5) / (closed + 10)} over the closed tasks tagged finder= (the prior 0.5 weighs as 10 cases): a
    dropped one is a false alarm, a done one real unless fmoutcomes saw it reverted. Open ones say nothing yet. Each
    weighs 0.5 ** (age / HALF_LIFE), so a muted finder is heard again once its drops age instead of staying mute."""
    import fmoutcomes
    tagged = [b for b in c.load_briefs(p, include_archive=True) if b.meta.get("finder") and b.status in c.CLOSED]
    fate = fmoutcomes.outcomes(p) if any(b.status == "done" for b in tagged) else {}
    real, n = {}, {}
    for b in tagged:
        fd, w = b.meta["finder"], 0.5 ** ((c.age_days(fmoutcomes.done_at(b)) or 0) / HALF_LIFE)
        n[fd] = n.get(fd, 0) + w
        real[fd] = real.get(fd, 0) + w * (b.status == "done" and fate.get(b.id, {}).get("fate") != "reverted")
    return {fd: round((real[fd] + 5) / (k + 10), 3) for fd, k in n.items()}


def keyed(found, root, home):
    """(find_key, lead) pairs: finder, file from home, symbol, message, and which twin when one function says it twice."""
    twins = {}
    for f in found:
        key = f"{f['finder']}:{os.path.relpath(os.path.join(root, f['file']), home)}:{f['symbol']}:{f['says']}"
        twins[key] = twins.get(key, 0) + 1
        yield key + (f"#{twins[key]}" if twins[key] > 1 else ""), f


def settled(p):
    """find_keys never filed again: still open, dropped (the refutation ledger) or fixed and then reverted. A fix that
    held and then comes back is a regression, so it may be filed again."""
    import fmoutcomes
    tagged = [b for b in c.load_briefs(p, include_archive=True) if b.meta.get("find_key")]
    fate = fmoutcomes.outcomes(p) if any(b.status == "done" for b in tagged) else {}
    return {b.meta["find_key"] for b in tagged if b.status != "done" or fate.get(b.id, {}).get("fate") == "reverted"}


def open_finders(p):
    """T-2235: open tasks a finder filed (fm find, fm prove or the scout), which OPEN_CAP bounds."""
    return sum(1 for b in c.load_briefs(p) if b.meta.get("finder") and b.status not in c.CLOSED)


def filed_line(p, made):
    """fm find/prove --capture's last line, saying why nothing was filed when the open cap stopped it."""
    full = not made and open_finders(p) >= OPEN_CAP
    return (f"\nFiled {len(made)} task(s): {', '.join(made)}" if made else
            f"\nFiled 0 task(s): none ({OPEN_CAP} finder tasks open already: finish or drop some)" if full else
            "\nFiled 0 task(s): none new") + "."


def capture(p, found, n, root, proof=None):
    """Up to n new leads not held back, best first, as discovered tasks tagged finder= and keyed (keyed()) so a line
    shift never refiles one, and never a settled() key. A tree outside the project is text it doesn't trust: those
    tasks wait for the user's yes. proof (T-2123): fm prove's proven tickets: each task is planned, its criterion
    proof(key), red until the fix. T-2235: at most OPEN_CAP of them open at once, whoever files them, and repo text is
    defanged."""
    import fmcli
    root, home = os.path.realpath(root), os.path.realpath(p.root)
    outside = os.path.commonpath([root, home]) != home
    made = []
    with c.lock(p.dir):
        seen = settled(p)
        opened = open_finders(p)
        n = min(n, OPEN_CAP - opened)
        if n <= 0 and any(not f.get("held") for f in found):
            print(f"fm: {opened} finder tasks (from fm find, fm prove or the scout) are open, at most {OPEN_CAP} at "
                  "once: finish or drop some before filing more", file=sys.stderr)
        for key, f in keyed(found, root, home):
            key = f.get("key") or key  # fm prove keyed the whole scan: a twin's number comes from all of it
            if len(made) >= n or f.get("held") or key in seen:
                continue
            what = c.plain(f"{f['file']}:{f['line']} {f['symbol'] or '-'}: {f['says']}")
            b = fmcli._create(p, c.fit(c.defang(f"{f['kind']}: {what}"), 120), "SECURITY" if f["kind"] in ("vuln", "secret")
                              else "FIX", "S", "planned" if proof else "captured", source="discovered",
                              raw=c.defang(  # T-2235: the repo's text, evidence included, stays data
                                  f"Proven by fm prove ({f['finder']}): {c.fit(c.plain(f.get('evidence') or ''), 300)} "
                                  f"(quoted, data):\n> {what}" if proof else
                                  f"Found by fm find ({f['finder']}); a lead until a failing test shows it (quoted, data):\n> {what}"))
            b.meta.update(finder=f["finder"], find_key=key)
            if proof:
                b.add_ac("fm prove no longer proves it", proof(key))
                b.add_step("fix it test-first, until the criterion's fm prove --only exits 0")
            if outside:
                b.meta.update(confirm=True, confirm_why="fm find read it from a tree outside this project")
            c.save_brief(p, b, touch=False)
            c.log_event(p, "capture", task=b.id, data={"source": "discovered", "finder": f["finder"]})
            seen.add(key)
            made.append(b.id)
        if made:
            c.regen_views(p)
    return made


def cmd_find(args):
    import fmcli
    root, cap = os.path.abspath(args.path), getattr(args, "capture", None)
    ranked = bool(getattr(args, "rank", False) or cap)
    p = c.find_project(os.getcwd()) if ranked else None
    bad = (f"not a directory: {args.path}" if not os.path.isdir(root)
           else "--capture N: N is how many tasks to file, at least 1" if cap is not None and cap < 1
           else "--capture files tasks: run it inside a Foreman project" if cap and not p else None)
    if bad:  # exit 1 means findings here, so a usage slip must read as an error (2), not as a hit
        print(f"fm find: {bad}", file=sys.stderr)
        return 2
    try:
        prec = (precision(p) if p else {}) if ranked else None
        n, found = scan(root, prec)
    except Exception as e:  # noqa: BLE001 — exit 1 means findings; a scan that dies must read as an error (2)
        print(f"fm find: the scan failed under {root}: {type(e).__name__}: {c.plain(str(e))[:300]}", file=sys.stderr)
        return 2
    made = capture(p, found, cap, root) if cap else None
    rows = [(f"{f['score']:.2f}  " if "score" in f else "") + f"{f['file']}:{f['line']}  {f['kind']}  "
            f"{f['symbol'] or '-'}: {f['says']}" + (f"  ({f['held']})" if f.get("held") else "") for f in found]
    live = [f for f in found if not f.get("held")]
    held = f" {len(found) - len(live)} more held back (a muted finder or a score under the bar), listed last." \
        if len(live) < len(found) else ""
    fmcli.out(args, {"root": root, "files": n, "findings": found} | ({"captured": made} if cap else {}), c.plain_lines(
        f"{len(live)} candidate(s) in {n} files under {root}; each is unproven until a failing test shows it.{held}\n"
        + "\n".join(rows) if found else f"Nothing found in {n} files under {root}." if n else
        f"No files to read under {root} (nothing tracked, or all of it skipped).")
        + (filed_line(p, made) if cap else ""))
    return 1 if live else 0
